/**
 * Owl Studio sample-preview nav bar.
 * Loaded from every demo/sample page via:
 *   - demos/*/index.html  →  <script src="/samples/industries/_owl-nav.js" defer></script>
 *   - samples/industries/*.html  →  <script src="_owl-nav.js" defer></script>
 *
 * Fixed bottom-centre bar: back to gallery, ← Prev, 01/10, Next →, "Build this", ×
 */
(function () {
  "use strict";

  var SAMPLES = [
    { slug: "slaney-dental-wexford",   url: "/demos/slaney-dental-wexford/",                    name: "Slaney Dental",     style: "Typographic-First"     },
    { slug: "strand-road-dental",      url: "/demos/strand-road-dental/",                       name: "Strand Road Dental",style: "Luxury Minimal"         },
    { slug: "vetcare-limerick",        url: "/demos/vetcare-limerick/",                         name: "Vetcare Limerick",  style: "Warm & Approachable"   },
    { slug: "murphy-plumbing-cork",    url: "/demos/murphy-plumbing-cork/",                     name: "Murphy Plumbing",   style: "Bold Utility"          },
    { slug: "curtin-electrical",       url: "/demos/curtin-electrical/",                        name: "Curtin Electrical", style: "Technical Split-Panel" },
    { slug: "clancys-restaurant-cork", url: "/demos/clancys-restaurant-cork/",                  name: "Clancy's Cork",     style: "Fine Dining Cinematic" },
    { slug: "wildflour-bakery-galway", url: "/demos/wildflour-bakery-galway/",                  name: "Wildflour Bakery",  style: "Warm Craft"            },
    { slug: "01-dental-swiss",         url: "/samples/industries/01-dental-swiss.html",         name: "Dental Practice",   style: "Swiss Editorial"       },
    { slug: "02-solicitor-swiss",      url: "/samples/industries/02-solicitor-swiss.html",      name: "Solicitors",        style: "Swiss Authority"       },
    { slug: "06-trade-pro-dark-oled",  url: "/samples/industries/06-trade-pro-dark-oled.html",  name: "Trade Pro",         style: "Dark OLED"             }
  ];

  var GALLERY_URL = "https://websites.owlzone.trade/#styles";
  var BUILD_URL   = "https://websites.owlzone.trade/#pricing";

  // Resolve current entry from pathname — works for both
  //   /demos/slaney-dental-wexford/     (last non-empty segment = slug)
  //   /samples/industries/01-dental-swiss.html  (filename without .html = slug)
  var path = (location.pathname || "").replace(/\.html?$/i, "").replace(/\/+$/, "");
  var fname = path.substring(path.lastIndexOf("/") + 1);
  var idx = -1;
  for (var i = 0; i < SAMPLES.length; i++) {
    if (SAMPLES[i].slug === fname) { idx = i; break; }
  }
  if (idx === -1) return;

  // Session-level dismiss
  try { if (sessionStorage.getItem("owl-nav-hidden")) return; } catch (e) {}

  // Screenshot/snapshot escape hatch
  if (/[?&]hide-nav=1\b/.test(location.search)) return;

  var current = SAMPLES[idx];
  var prev    = SAMPLES[(idx - 1 + SAMPLES.length) % SAMPLES.length];
  var next    = SAMPLES[(idx + 1) % SAMPLES.length];

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
  bar.setAttribute("aria-label", "Owl Studio demo navigation");
  bar.innerHTML =
    '<a href="' + GALLERY_URL + '" title="Back to all 10 demos">' +
      '<span class="owl-label">Owl Studio · </span>← Gallery</a>' +
    '<span class="owl-div"></span>' +
    '<a href="' + prev.url + '" title="Previous: ' + prev.name + ' — ' + prev.style + '">← Prev</a>' +
    '<span class="owl-idx">' + String(idx + 1).padStart(2, "0") + ' / 10</span>' +
    '<a href="' + next.url + '" title="Next: ' + next.name + ' — ' + next.style + '">Next →</a>' +
    '<span class="owl-div"></span>' +
    '<a class="owl-build" href="' + BUILD_URL + '" title="Build this direction for your business">Build this →</a>' +
    '<button type="button" class="owl-close" aria-label="Hide preview bar" title="Hide preview bar">×</button>';

  document.body.appendChild(bar);

  bar.querySelector(".owl-close").addEventListener("click", function () {
    bar.remove();
    try { sessionStorage.setItem("owl-nav-hidden", "1"); } catch (e) {}
  });
})();
