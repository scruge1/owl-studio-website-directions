/**
 * Owl Studio sample-preview nav bar.
 * Loaded from every samples/industries/*.html via <script src="_owl-nav.js" defer></script>.
 *
 * Injects a fixed bottom-centre bar so the prospect can:
 *   - go back to the main gallery (no browser-back required)
 *   - page prev/next across all 10 samples without returning first
 *   - click "Build this style" to jump back to pricing with the style pre-selected
 *   - dismiss the bar for the rest of the session if it's in the way
 *
 * Self-contained: one script tag, zero DOM prerequisites. The bar fails
 * silently if the page isn't one of the 10 industry samples.
 */
(function () {
  "use strict";

  var SAMPLES = [
    { slug: "01-dental-swiss",                  name: "Dental Practice",       style: "Swiss Editorial" },
    { slug: "02-solicitor-swiss",               name: "Solicitors",            style: "Swiss Authority" },
    { slug: "03-accountant-minimalism",         name: "Chartered Accountants", style: "Numbers-forward" },
    { slug: "04-physio-neumorphism",            name: "Physiotherapy",         style: "Soft Neumorphism" },
    { slug: "05-opticians-glassmorphism",       name: "Opticians",             style: "Glassmorphism" },
    { slug: "06-audiologist-aurora",            name: "Audiology",             style: "Aurora Calm" },
    { slug: "07-vet-claymorphism",              name: "Veterinary",            style: "Claymorphism" },
    { slug: "08-financial-brutalism-editorial", name: "Wealth Advisor",        style: "Editorial Brutalism" },
    { slug: "09-architects-3d",                 name: "Architects",            style: "3D Hyperrealism" },
    { slug: "10-aesthetic-clinic-aurora-luxe",  name: "Aesthetic Clinic",      style: "Aurora Luxe" }
  ];

  var GALLERY_URL = "https://websites.owlzone.trade/#styles";

  // Resolve current sample from the pathname
  var path = (location.pathname || "").split("?")[0].split("#")[0];
  var fname = path.substring(path.lastIndexOf("/") + 1).replace(/\.html?$/i, "");
  var idx = -1;
  for (var i = 0; i < SAMPLES.length; i++) {
    if (SAMPLES[i].slug === fname) { idx = i; break; }
  }
  if (idx === -1) return;

  // Allow a previously-dismissed bar to stay dismissed for the session
  try {
    if (sessionStorage.getItem("owl-nav-hidden")) return;
  } catch (e) { /* ignore */ }

  var current = SAMPLES[idx];
  var prev = SAMPLES[(idx - 1 + SAMPLES.length) % SAMPLES.length];
  var next = SAMPLES[(idx + 1) % SAMPLES.length];
  var buildUrl = "https://websites.owlzone.trade/#pricing";

  // Shadow-DOM avoided on purpose — some samples (3D, glass) play heavy with
  // CSS; a plain root-level div with scoped selectors is enough and respects
  // the sample's aesthetic without competing fonts. All styles inline + scoped.
  var css = [
    "#owl-sample-nav{",
    "  position:fixed;z-index:2147483647;",
    "  bottom:18px;left:50%;transform:translateX(-50%);",
    "  background:#0b0a08;color:#F5F1E8;",
    "  display:flex;align-items:center;gap:6px;",
    "  padding:8px 10px;max-width:calc(100vw - 20px);",
    "  font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;",
    "  font-size:11px;font-weight:600;letter-spacing:0.04em;line-height:1;",
    "  border:1px solid rgba(245,241,232,0.14);",
    "  box-shadow:0 14px 34px rgba(0,0,0,0.38);",
    "  border-radius:2px;flex-wrap:nowrap;",
    "}",
    "#owl-sample-nav a,#owl-sample-nav button{",
    "  background:transparent;color:#F5F1E8;border:0;cursor:pointer;",
    "  font:inherit;letter-spacing:inherit;text-decoration:none;",
    "  padding:8px 10px;border-radius:2px;white-space:nowrap;",
    "  transition:color 140ms ease,background 140ms ease;",
    "}",
    "#owl-sample-nav a:hover,#owl-sample-nav button:hover{color:#f1c18e;}",
    "#owl-sample-nav .owl-div{width:1px;height:18px;background:rgba(245,241,232,0.2);margin:0 2px;flex:0 0 auto;}",
    "#owl-sample-nav .owl-idx{color:rgba(245,241,232,0.54);font-weight:400;padding:0 6px;}",
    "#owl-sample-nav .owl-build{background:#c96f32;color:#fff;padding:8px 14px;border-radius:2px;font-weight:700;}",
    "#owl-sample-nav .owl-build:hover{background:#9a4e1e;color:#fff;}",
    "#owl-sample-nav .owl-close{color:rgba(245,241,232,0.5);padding:6px 8px;font-size:14px;}",
    "#owl-sample-nav .owl-label{color:rgba(245,241,232,0.7);padding:0 4px;font-weight:500;}",
    "@media (max-width:720px){",
    "  #owl-sample-nav{font-size:10px;padding:6px 8px;gap:2px;}",
    "  #owl-sample-nav a,#owl-sample-nav button{padding:7px 8px;}",
    "  #owl-sample-nav .owl-label{display:none;}",
    "  #owl-sample-nav .owl-div{height:16px;}",
    "}"
  ].join("");

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var bar = document.createElement("div");
  bar.id = "owl-sample-nav";
  bar.setAttribute("role", "navigation");
  bar.setAttribute("aria-label", "Owl Studio sample preview navigation");
  bar.innerHTML =
    '<a href="' + GALLERY_URL + '" title="Back to all 10 samples">' +
      '<span class="owl-label">Owl Studio · </span>← Gallery</a>' +
    '<span class="owl-div"></span>' +
    '<a href="' + prev.slug + '.html" title="Previous sample: ' + prev.name + ' (' + prev.style + ')">← Prev</a>' +
    '<span class="owl-idx">' + String(idx + 1).padStart(2, "0") + ' / 10</span>' +
    '<a href="' + next.slug + '.html" title="Next sample: ' + next.name + ' (' + next.style + ')">Next →</a>' +
    '<span class="owl-div"></span>' +
    '<a class="owl-build" href="' + buildUrl + '" title="Build this direction for your business">Build this →</a>' +
    '<button type="button" class="owl-close" aria-label="Hide preview bar" title="Hide preview bar">×</button>';

  document.body.appendChild(bar);

  bar.querySelector(".owl-close").addEventListener("click", function () {
    bar.remove();
    try { sessionStorage.setItem("owl-nav-hidden", "1"); } catch (e) { /* ignore */ }
  });
})();
