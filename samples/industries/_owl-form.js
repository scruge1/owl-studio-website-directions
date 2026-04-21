/**
 * Owl Studio sample contact form — shared across every samples/industries/*.html.
 * Loaded via <script src="_owl-form.js" defer></script> injected right before </body>.
 *
 * What it does on load:
 *   1. Detects the current sample slug from the pathname
 *   2. Looks up the corresponding site_id in SAMPLES
 *   3. Injects a neutral "Try the contact form — leads land in the admin dashboard"
 *      block near the end of the page (above or inside the footer)
 *   4. On submit: POSTs to https://callmeie.onrender.com/owl/submit
 *
 * Fails silently on non-sample pages. Session-dismissible.
 * Same pattern as _owl-nav.js (floating nav bar), deliberately additive —
 * does not touch the sample's own styling.
 */
(function () {
  "use strict";
  // site_id for each sample — must match what's registered in owl_sites
  var SAMPLES = {
    "01-dental-swiss":                  { site_id: "rathborne-dental-demo",       business: "Rathborne Dental" },
    "02-solicitor-swiss":               { site_id: "hennessy-byrne-demo",          business: "Hennessy & Byrne" },
    "03-accountant-minimalism":         { site_id: "magee-co-demo",                business: "Magee & Co." },
    "04-physio-neumorphism":            { site_id: "quay-physio-demo",             business: "The Quay Physio" },
    "05-opticians-glassmorphism":       { site_id: "callanan-opticians-demo",      business: "Callanan Opticians" },
    "06-audiologist-aurora":            { site_id: "hear-clear-demo",              business: "Hear Clear Audiology" },
    "07-vet-claymorphism":              { site_id: "main-street-vets-demo",        business: "Main Street Vets" },
    "08-financial-brutalism-editorial": { site_id: "kelleher-wealth-demo",         business: "Kelleher Wealth" },
    "09-architects-3d":                 { site_id: "carroll-osuilleabhain-demo",   business: "Carroll O Suilleabhain Architects" },
    "10-aesthetic-clinic-aurora-luxe":  { site_id: "molyneux-aesthetics-demo",     business: "Molyneux Aesthetics" }
  };

  var path = (location.pathname || "").split("?")[0].split("#")[0];
  var fname = path.substring(path.lastIndexOf("/") + 1).replace(/\.html?$/i, "");
  var meta = SAMPLES[fname];
  if (!meta) return;

  if (/[?&]hide-form=1\b/.test(location.search)) return;
  try { if (sessionStorage.getItem("owl-form-hidden")) return; } catch (e) {}

  // Neutral styling — uses system-font-ish + deliberate reset so the
  // block doesn't inherit the sample's aggressive typography.
  var css = [
    "#owl-lead-form{",
    "  box-sizing:border-box;",
    "  background:#0b0a08;color:#F5F1E8;",
    "  padding:48px clamp(20px,4vw,56px);",
    "  border-top:3px solid #F5F1E8;",
    "  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;",
    "  position:relative;",
    "}",
    "#owl-lead-form *{box-sizing:border-box;}",
    "#owl-lead-form .olf-inner{max-width:720px;margin:0 auto;}",
    "#owl-lead-form .olf-kicker{",
    "  font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;",
    "  color:#c96f32;margin-bottom:12px;",
    "}",
    "#owl-lead-form h3{",
    "  margin:0 0 10px;font-size:clamp(22px,3vw,34px);font-weight:800;",
    "  letter-spacing:-0.02em;line-height:1.1;color:#F5F1E8;",
    "}",
    "#owl-lead-form p.olf-lede{",
    "  margin:0 0 24px;font-size:15px;line-height:1.55;color:rgba(245,241,232,0.76);",
    "  max-width:560px;",
    "}",
    "#owl-lead-form .olf-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;}",
    "@media (max-width:560px){#owl-lead-form .olf-row{grid-template-columns:1fr;}}",
    "#owl-lead-form label{display:flex;flex-direction:column;gap:6px;}",
    "#owl-lead-form label span{",
    "  font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;",
    "  color:rgba(245,241,232,0.6);",
    "}",
    "#owl-lead-form input,#owl-lead-form textarea{",
    "  background:#fff;color:#0b0a08;border:2px solid rgba(241,193,142,0.25);",
    "  padding:11px 13px;border-radius:2px;font:inherit;font-size:15px;",
    "  transition:border-color 140ms ease;",
    "}",
    "#owl-lead-form input:focus,#owl-lead-form textarea:focus{",
    "  outline:none;border-color:#f1c18e;box-shadow:0 0 0 3px rgba(241,193,142,0.25);",
    "}",
    "#owl-lead-form textarea{min-height:90px;resize:vertical;}",
    "#owl-lead-form .olf-hp{position:absolute !important;left:-9999px !important;width:1px !important;height:1px !important;opacity:0 !important;}",
    "#owl-lead-form .olf-foot{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:8px;}",
    "#owl-lead-form button{",
    "  background:#c96f32;color:#fff;border:0;cursor:pointer;",
    "  font:inherit;font-size:14px;font-weight:700;letter-spacing:0.04em;",
    "  padding:13px 22px;border-radius:2px;transition:background 140ms ease;",
    "}",
    "#owl-lead-form button:hover{background:#9a4e1e;}",
    "#owl-lead-form button:disabled{opacity:0.6;cursor:not-allowed;}",
    "#owl-lead-form .olf-status{font-size:12px;font-weight:600;color:rgba(245,241,232,0.64);}",
    "#owl-lead-form .olf-status.ok{color:#f1c18e;}",
    "#owl-lead-form .olf-status.err{color:#ff9d7e;}",
    "#owl-lead-form .olf-note{",
    "  margin-top:18px;padding-top:16px;border-top:1px solid rgba(245,241,232,0.14);",
    "  font-size:11px;color:rgba(245,241,232,0.48);line-height:1.5;",
    "}",
    "#owl-lead-form .olf-note a{color:#f1c18e;}",
    "#owl-lead-form .olf-close{",
    "  position:absolute;top:14px;right:14px;background:transparent;color:rgba(245,241,232,0.5);",
    "  border:0;cursor:pointer;font-size:22px;padding:4px 10px;",
    "}"
  ].join("");

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var section = document.createElement("section");
  section.id = "owl-lead-form";
  section.setAttribute("aria-label", "Contact " + meta.business);
  section.innerHTML =
    '<button type="button" class="olf-close" aria-label="Hide this form">\u00d7</button>' +
    '<div class="olf-inner">' +
      '<div class="olf-kicker">' + meta.business + '  Get in touch</div>' +
      '<h3>Send an enquiry  a reply lands within 24 hours.</h3>' +
      '<p class="olf-lede">This is a sample site built by Owl Studio. The form below is real  submissions land in the admin dashboard for ' + meta.business + '. Try it.</p>' +
      '<form class="olf-form">' +
        '<div class="olf-row">' +
          '<label><span>Your name</span><input type="text" name="name" required autocomplete="name"></label>' +
          '<label><span>Email</span><input type="email" name="email" required autocomplete="email"></label>' +
        '</div>' +
        '<div class="olf-row">' +
          '<label><span>Phone <em style="font-style:italic;font-weight:400;text-transform:none;letter-spacing:0.04em;opacity:0.7;">(optional)</em></span><input type="tel" name="phone" autocomplete="tel"></label>' +
          '<label><span>What you\u2019re after</span><input type="text" name="topic" placeholder="e.g. first appointment, a quote, opening hours..."></label>' +
        '</div>' +
        '<label><span>Message</span><textarea name="message" rows="3" placeholder="A couple of lines is fine."></textarea></label>' +
        '<input type="text" name="nickname" class="olf-hp" tabindex="-1" autocomplete="off" aria-hidden="true">' +
        '<div class="olf-foot">' +
          '<button type="submit">Send enquiry</button>' +
          '<span class="olf-status" role="status" aria-live="polite"></span>' +
        '</div>' +
      '</form>' +
      '<p class="olf-note">This is an Owl Studio industry sample. Submissions go to our demo admin dashboard, <strong>not</strong> to the actual business. Want a site like this for your own practice?  <a href="https://websites.owlzone.trade/#pricing">Pick a tier</a>.</p>' +
    '</div>';

  // Insert right before the floating sample-nav bar's script tag / before </body>
  document.body.appendChild(section);

  var form = section.querySelector("form.olf-form");
  var status = section.querySelector(".olf-status");
  var button = section.querySelector("button[type=submit]");
  var closeBtn = section.querySelector(".olf-close");

  closeBtn.addEventListener("click", function () {
    section.remove();
    try { sessionStorage.setItem("owl-form-hidden", "1"); } catch (e) {}
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var fd = {};
    new FormData(form).forEach(function (v, k) { fd[k] = v; });
    if (fd.nickname) { section.remove(); return; }     // bot honeypot
    button.disabled = true;
    var oldText = button.textContent;
    button.textContent = "Sending\u2026";
    status.className = "olf-status";
    status.textContent = "";
    fetch("https://callmeie.onrender.com/owl/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        site_id: meta.site_id,
        form_data: fd,
        submitted_from: location.href
      })
    })
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (j.ok) {
        form.reset();
        status.className = "olf-status ok";
        status.textContent = j.message || "Sent. We reply within 24 hours.";
        button.textContent = "Sent \u2713";
        setTimeout(function () {
          button.disabled = false; button.textContent = oldText;
        }, 4000);
      } else {
        throw new Error(j.detail || "submit failed");
      }
    })
    .catch(function () {
      status.className = "olf-status err";
      status.textContent = "Something went wrong. Please email hello@" + location.hostname + " directly.";
      button.disabled = false; button.textContent = oldText;
    });
  });
})();
