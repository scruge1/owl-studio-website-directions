# Fulfillment Audit Log — append-only delta history

Per-run deltas from `/audit-fulfillment-gap`, newest first. Baseline = `FULFILLMENT-AUDIT-BASELINE.md`.

---

## 2026-06-07 — Document Ops withdrawn from sale

**Trigger:** session edited PRICING-SSOT.md §3 + INFRA.md §14 + callmeie-hub site (DocOps removal).

**Delta vs 2026-05-20 baseline:**

```
Tier                                      Was        Now              Change
──────────────────────────────────────────────────────────────────────────
Doc Ops Pilots (€500 / €1500)             sell:yes   WITHDRAWN        gap resolved (not sold)
                                          7/10
Doc Ops Auto subs (€99/249/499/1500)      sell:yes   WITHDRAWN        gap resolved + integrity
                                          3/10                        exposure removed (98% claim)
```

**Why:** Adam decision (REPOSITION-PDR-IRISH-ACCOUNTANTS, 2026-06-07). Standalone DocOps-OCR commoditised (free Xero/QB capture; Dext/AutoEntry/Datamolino own paid lane). Live `/docs/` page oversold: "98%-auto-post" claim vs 65–89%/field engine; medical-exempt + intra-EU-FX correctness unvalidated → integrity exposure to LEO/bank assessors (anti-priority-9355572e).

**What changed on the sell-side:** `/docs/` product page + `#pricing` cards removed (301 `/docs/* → /`); nav/footer/strip refs stripped across 88 pages; sitemap `/docs/` dropped; homepage product-row + hero/price/about copy removed; "Three products"→"Two". Legal/terms dead `/docs/#pricing` link fixed + DocOps month-to-month clause dropped. Stripe products LEFT LIVE but de-listed (no CTA reaches them). OCR retained as internal ingestion arm (portal/backend §14 unchanged).

**Net:** the two highest-integrity-risk DocOps gaps (3/10 "email-us-first" oversell + 7/10 pilots) are no longer sell-side promises. Marketing-vs-delivery gap for DocOps = closed by removal, not by building capability.

**Gap list impact:** no baseline gap #1–11 was a DocOps gap (Receptionist/D5/Local-SEO/care-plan), so the §6 gap list is unchanged.

**NOT done (flagged for Adam — legal review, out of marketing-removal scope):**
- `legal/privacy.html` v1.0 version note still says "covers all three products (... Document Ops ...)".
- `legal/dpa.html` meta + sub-processor schedule still describe the Document Ops sandbox extractor + processing. GDPR Article 28 contract text — revise via Adam/solicitor, not freehand. Zero DocOps customers exist, so dormant; reconcile when the DPA is next touched.

**Baseline updated:** yes — two DocOps rows marked WITHDRAWN in `FULFILLMENT-AUDIT-BASELINE.md`.
