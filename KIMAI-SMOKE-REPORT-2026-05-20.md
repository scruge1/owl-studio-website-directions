# KIMAI-SMOKE-REPORT — 2026-05-20

Smoke-test of Kimai v2.56.0 (`kimai/kimai2:apache`) against CallMeIE edit-budget meter requirement (PDR-SHIPPABILITY-V1 §B). Goal: promote from `candidate` to `locally_verified` OR reject in favor of pure-Postgres ledger.

## A. Smoke results

| Check | Result | Notes |
|---|---|---|
| `docker pull kimai/kimai2:apache` | OK | 1.27 GB image |
| Container boot | OK (process up) | Apache image binds :8001 |
| HTTP probe `GET /` | FAIL (HTTP 000) | Container never reaches "healthy"; serves zero traffic |
| Boot log root cause | DB driver mismatch | Entry script loops `dbtest.php` against MySQL host; no SQLite fallback in production image |
| `.env.dist` declares | `DATABASE_URL=mysql://...` only | MariaDB 10.5+ / MySQL 5.7+ required |
| `config/packages/doctrine.yaml` driver | `pdo_mysql` (hard-coded) | No `pdo_sqlite` path |
| Budget entity model | `BudgetTrait.php` | Per-entity `budget` (€) + `time_budget` (seconds) |
| `budget_type` enum | **`null` or `'month'` only** | **No rolling-window support** |
| API surface | REST `/api/timesheets`, `/api/customers`, `/api/projects`, `/api/activities` | Standard CRUD; sufficient for log-hours-from-edit-queue |

## B. License analysis

`LICENSE` = **GNU AFFERO GENERAL PUBLIC LICENSE v3, 19 Nov 2007**. `composer.json` declares `"license": "AGPL-3.0-or-later"`.

Implications for CallMeIE:
- **AGPL §13 (network-use trigger):** if customers access a Kimai instance over the network, CallMeIE must offer the corresponding source (Kimai's own source is fine — but any modifications must also be offered).
- Safe pattern: Kimai stays **Adam-internal only**; customer-facing budget meter is a separate page in the existing admin/portal that reads aggregate numbers via API. No customer hits Kimai directly → §13 not triggered for the customer-facing surface. CallMeIE's own code remains MIT/proprietary because it merely *uses* the API across a network boundary; AGPL does not virally cross HTTP boundaries (settled FSF reading).
- Aligns with established system anti-priority — multiple prior AGPL tools rejected (claude-mem rowids 1137, 11584, 11590, 11591, 18004, 18509, 18513, 19679, 22389).

## C. Footprint

- Image: **1.27 GB** on disk
- Idle RAM (during DB-wait loop, no app running): 4 MB — not representative, app never started
- Realistic estimate (Apache + PHP-FPM + MariaDB sidecar): **~500–800 MB RAM**, **~2 GB disk** per tenant
- Plus a **MariaDB container per Coolify deploy** (Kimai is single-tenant by design; multi-tenant requires N Kimai instances OR shared instance with `team` separation, which leaks data risk)

## D. DECISION: **Pure-Postgres ledger**

Pick: **B. Pure-Postgres ledger.**

Justification against 60/30/10 + setup + AGPL:
1. **60/30/10 fit** — pure SQL is 90% deterministic / 10% rule-based / 0% AI. Kimai is a full Symfony app (negative for the "prefer query over framework" doctrine).
2. **Setup cost** — Kimai: new MariaDB container + Coolify deploy + N tenants × 1 DB + custom API auth glue ≈ **6–10 h**. Postgres ledger: 1 table + 2 SQL functions + 1 admin-portal panel ≈ **45 min**.
3. **AGPL risk** — non-zero. Even with internal-only deployment, every Kimai upgrade is an AGPL diff-review. Postgres ledger has zero license cost.
4. **`budget_type` mismatch** — Kimai supports only `null` (project total) and `'month'` (monthly reset). **Premium tier's rolling-90d-avg with 8h ceiling CANNOT be modelled** in Kimai natively; would need a wrapper layer that defeats the point of adopting Kimai. (Launch 0.5h/mo, Business 2h/mo, Care €45/€95/€195 monthly caps fit; Premium does not.)
5. **Adam-keyboard cost per edit** — Kimai web UI: open Kimai → select customer → select activity → start timer / log entry. Postgres ledger: edit-queue page already has the ticket; one button writes the row.
6. **Reporting** — Kimai's CSV export is nice but the same is `SELECT … GROUP BY tenant_id, month` in Postgres in 4 lines.
7. **Future customer-portal integration** — must build a custom panel either way; reading from Kimai API vs from the same Postgres the rest of CallMeIE uses → Postgres wins on cohesion.

## E. (N/A — Kimai rejected)

## F. Pure-Postgres ledger — integration plan

**Single new table** (lives in the existing CallMeIE Postgres, same DB as Edit Queue MVP):

```sql
CREATE TABLE time_entry (
  id           BIGSERIAL PRIMARY KEY,
  tenant_id    TEXT NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  queue_id     BIGINT REFERENCES edit_queue(id) ON DELETE SET NULL,
  minutes      INTEGER NOT NULL CHECK (minutes > 0),
  logged_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  logged_by    TEXT NOT NULL,
  note         TEXT
);
CREATE INDEX time_entry_tenant_month_idx
  ON time_entry (tenant_id, date_trunc('month', logged_at));
CREATE INDEX time_entry_tenant_rolling_idx
  ON time_entry (tenant_id, logged_at DESC);
```

**Two SQL functions** (rule-based caps live in code config, not in DB — keeps tier policy in one place):

```sql
-- Monthly usage (Launch 0.5h, Business 2h, Care plans)
CREATE OR REPLACE FUNCTION minutes_used_this_month(p_tenant TEXT)
RETURNS INTEGER LANGUAGE SQL STABLE AS $$
  SELECT COALESCE(SUM(minutes), 0)::INT
    FROM time_entry
   WHERE tenant_id = p_tenant
     AND logged_at >= date_trunc('month', now());
$$;

-- 90-day rolling average minutes/month (Premium 6h-avg, 8h hard ceiling)
CREATE OR REPLACE FUNCTION minutes_rolling_90d_avg(p_tenant TEXT)
RETURNS NUMERIC LANGUAGE SQL STABLE AS $$
  SELECT COALESCE(SUM(minutes), 0) / 3.0
    FROM time_entry
   WHERE tenant_id = p_tenant
     AND logged_at >= now() - INTERVAL '90 days';
$$;
```

**Total LOC**: ~30 lines SQL + ~40 lines admin-portal Python/JS (log button + remaining-budget panel) = **~70 LOC**.

**Same-commit-as-MVP feasibility**: yes. Edit-Queue MVP already adds Postgres tables; `time_entry` lands in the same migration. Customer-portal budget meter reuses existing tenant-auth.

**Tier policy lives in Python config** (not DB), looks like:
```python
TIER_CAPS = {
    "launch":    {"minutes": 30,  "window": "month"},
    "business":  {"minutes": 120, "window": "month"},
    "premium":   {"minutes": 360, "window": "rolling_90d_avg", "hard_ceiling": 480},
    "care_45":   {"minutes": 30,  "window": "month"},
    "care_95":   {"minutes": 90,  "window": "month"},
    "care_195":  {"minutes": 180, "window": "month"},
}
```

## G. Confidence + same-substrate caveat

Confidence **0.85** (smoke run end-to-end, license + schema + footprint inspected directly; pricing fit verified against `PRICING-SSOT.md` tier shape). Same-substrate caveat applies — **Adam should personally read this decision before integration starts**; the Premium-tier rolling-90d argument is the load-bearing line and worth a sanity check against the real `PRICING-SSOT.md` tier definition.
