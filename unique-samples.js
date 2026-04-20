const UNIQUE_SALES_EMAIL = "callmeie@proton.me";

const uniqueSamples = [
  {
    id: "copper",
    ref: "KNOB product page",
    name: "Copper Product Studio",
    market: "Premium product",
    copy: "Warm product storytelling for makers, hardware, homeware, and premium local products.",
    palette: ["#f4bf80", "#160c06", "#d88947", "#f8dfb4"],
    modules: ["Product theatre", "Material story", "Shop-ready CTA"]
  },
  {
    id: "chrome",
    ref: "eBarista commerce",
    name: "Chrome Commerce",
    market: "Futuristic ecommerce",
    copy: "A dark launch page for products that need energy, scarcity, and a sharp buy path.",
    palette: ["#040807", "#ecfff0", "#a6ff2d", "#cfd6d1"],
    modules: ["Launch drop", "Product grid", "Checkout strip"]
  },
  {
    id: "quiet",
    ref: "Linear / Vercel",
    name: "Quiet SaaS",
    market: "B2B software",
    copy: "A restrained product surface for tools, agencies, dashboards, and technical services.",
    palette: ["#0e1018", "#eef1ff", "#8277ff", "#1a1d2d"],
    modules: ["Command hero", "Metric rail", "Product surface"]
  },
  {
    id: "trust",
    ref: "Stripe trust page",
    name: "Trust Ledger",
    market: "Finance and legal",
    copy: "A structured trust page for finance, accounting, legal, and payment businesses.",
    palette: ["#f6f8ff", "#101a34", "#0c2f66", "#dceeff"],
    modules: ["Compliance proof", "Document flow", "Consultation CTA"]
  },
  {
    id: "editorial",
    ref: "Notion editorial",
    name: "Editorial House",
    market: "Consultants and writers",
    copy: "A content-first layout for consultants, experts, educators, and personal brands.",
    palette: ["#fbf5e9", "#24150c", "#b8563e", "#ead8bd"],
    modules: ["Masthead", "Essay lead", "Newsletter CTA"]
  },
  {
    id: "growth",
    ref: "Local SEO landing",
    name: "Local Growth Engine",
    market: "Local lead generation",
    copy: "A phone-and-map led page for trades, dentists, clinics, and service-area businesses.",
    palette: ["#022d1e", "#f1fff2", "#28e28b", "#0c563c"],
    modules: ["Service map", "Phone CTA", "Area pages"]
  },
  {
    id: "clinic",
    ref: "Apple hospitality",
    name: "Clinic Calm",
    market: "Wellness clinic",
    copy: "A calm appointment page for clinics, therapists, aesthetics, and private practices.",
    palette: ["#f1e6d9", "#25160e", "#8c634f", "#d6bbae"],
    modules: ["Treatment menu", "Booking panel", "Trust notes"]
  },
  {
    id: "ops",
    ref: "Agent ops dashboard",
    name: "Agent Ops",
    market: "AI operations",
    copy: "A live control-room interface for automation services, workflows, and managed ops.",
    palette: ["#071016", "#e8f9ff", "#39d6f6", "#102632"],
    modules: ["Live feed", "Cost panel", "Approval queue"]
  },
  {
    id: "trades",
    ref: "Emergency trades ad",
    name: "Bold Trades",
    market: "Trades and repairs",
    copy: "A loud, phone-first service page for builders, roofers, plumbers, and repairs.",
    palette: ["#fff238", "#11110f", "#11110f", "#f7d900"],
    modules: ["24HR poster", "Call bar", "Proof list"]
  },
  {
    id: "heritage",
    ref: "Archive editorial",
    name: "Heritage Story",
    market: "Story-led brands",
    copy: "An archive-style site for family businesses, photographers, makers, and heritage work.",
    palette: ["#17110d", "#f7eadb", "#b6844c", "#5b5149"],
    modules: ["Timeline", "Image archive", "Founder story"]
  }
];

function uniqueStyle(sample) {
  const [bg, fg, accent, soft] = sample.palette;
  return `--u-bg:${bg};--u-fg:${fg};--u-accent:${accent};--u-soft:${soft};`;
}

function subject(sample) {
  return encodeURIComponent(`Website style enquiry - ${sample.name}`);
}

function mailLink(sample, label = "Contact") {
  return `<a href="mailto:${UNIQUE_SALES_EMAIL}?subject=${subject(sample)}">${label}</a>`;
}

function openButton(sample, label = "Open this style") {
  return `<button type="button" data-unique-open="${sample.id}">${label}</button>`;
}

const miniTemplates = {
  copper: (s) => `
    <article class="u-site u-product" style="${uniqueStyle(s)}">
      <header><span>${s.ref}</span>${mailLink(s, "Commission")}</header>
      <section>
        <div>
          <p>${s.market}</p>
          <h3>${s.name}</h3>
          <small>${s.copy}</small>
          ${openButton(s, "View product story")}
        </div>
        <div class="product-object"><i></i><b></b></div>
      </section>
      <footer><span>Walnut finish</span><span>Studio grade</span><span>Made local</span></footer>
    </article>`,

  chrome: (s) => `
    <article class="u-site u-commerce" style="${uniqueStyle(s)}">
      <nav><strong>DROP 02</strong><span>Cart 01</span>${mailLink(s, "Buy path")}</nav>
      <main>
        <div class="product-glow"></div>
        <div class="commerce-copy">
          <p>${s.market}</p>
          <h3>${s.name}</h3>
          <small>${s.copy}</small>
          ${openButton(s, "Launch preview")}
        </div>
        <aside><span>$149</span><span>Ships Friday</span></aside>
      </main>
    </article>`,

  quiet: (s) => `
    <article class="u-site u-saas" style="${uniqueStyle(s)}">
      <aside><b>QS</b><span>Inbox</span><span>Runs</span><span>Deploys</span></aside>
      <main>
        <header><span>Command centre</span>${mailLink(s, "Demo")}</header>
        <h3>${s.name}</h3>
        <p>${s.copy}</p>
        <div class="saas-grid"><b>98%</b><b>24m</b><b>12k</b></div>
        ${openButton(s, "Inspect product")}
      </main>
    </article>`,

  trust: (s) => `
    <article class="u-site u-trust" style="${uniqueStyle(s)}">
      <header><strong>${s.name}</strong>${mailLink(s, "Consult")}</header>
      <main>
        <section><p>${s.market}</p><h3>Clear terms. Clean trust.</h3><small>${s.copy}</small></section>
        <div class="ledger-doc"><span></span><span></span><span></span><b>VERIFIED</b></div>
      </main>
      ${openButton(s, "Review structure")}
    </article>`,

  editorial: (s) => `
    <article class="u-site u-editorial" style="${uniqueStyle(s)}">
      <div class="masthead">${s.name}</div>
      <div class="issue-line"><span>Issue 01</span><span>${s.market}</span><span>Long read</span></div>
      <main>
        <h3>Authority before persuasion.</h3>
        <p>${s.copy}</p>
        ${openButton(s, "Read the page")}
      </main>
      ${mailLink(s, "Request an editorial site")}
    </article>`,

  growth: (s) => `
    <article class="u-site u-growth" style="${uniqueStyle(s)}">
      <header><strong>${s.name}</strong>${mailLink(s, "Plan funnel")}</header>
      <main>
        <div class="map-card"><span></span><span></span><span></span></div>
        <section><p>${s.market}</p><h3>Be the business they find first.</h3><small>${s.copy}</small>${openButton(s, "View local funnel")}</section>
      </main>
    </article>`,

  clinic: (s) => `
    <article class="u-site u-clinic" style="${uniqueStyle(s)}">
      <header><span>Private appointments</span>${mailLink(s, "Book")}</header>
      <main>
        <div class="arch-photo"></div>
        <section><p>${s.market}</p><h3>${s.name}</h3><small>${s.copy}</small>${openButton(s, "Preview clinic")}</section>
      </main>
      <footer><span>Skin</span><span>Therapy</span><span>Wellness</span></footer>
    </article>`,

  ops: (s) => `
    <article class="u-site u-ops" style="${uniqueStyle(s)}">
      <header><strong>${s.name}</strong><span>Live</span>${mailLink(s, "Ops call")}</header>
      <main>
        <div class="ops-metrics"><b>87</b><b>$0.47</b><b>12</b></div>
        <section><p>${s.market}</p><h3>Approvals, costs, tasks, live.</h3><small>${s.copy}</small>${openButton(s, "Open control room")}</section>
      </main>
    </article>`,

  trades: (s) => `
    <article class="u-site u-trades" style="${uniqueStyle(s)}">
      <header><strong>24HR</strong>${mailLink(s, "Quote")}</header>
      <main><h3>${s.name}</h3><p>${s.copy}</p><div class="hazard">FAST QUOTE</div>${openButton(s, "See emergency page")}</main>
    </article>`,

  heritage: (s) => `
    <article class="u-site u-heritage" style="${uniqueStyle(s)}">
      <header><span>Archive 1926</span>${mailLink(s, "Tell story")}</header>
      <main>
        <ol><li></li><li></li><li></li><li></li></ol>
        <section><p>${s.market}</p><h3>${s.name}</h3><small>${s.copy}</small>${openButton(s, "Open archive")}</section>
      </main>
    </article>`
};

function renderUniqueCard(sample) {
  return miniTemplates[sample.id](sample);
}

function renderUniqueFull(sample) {
  return `
    <div class="u-modal-shell ${`u-${sample.id}`}" style="${uniqueStyle(sample)}">
      <div class="modal-top">
        <strong>${sample.name}</strong>
        <button class="modal-close" type="button" data-close>Close preview</button>
      </div>
      <section class="u-full">
        <div class="u-full-copy">
          <p class="eyebrow" style="color:color-mix(in srgb, var(--u-fg) 52%, transparent);">${sample.ref}</p>
          <h2>${sample.name}</h2>
          <p>${sample.copy} These examples are starting points only. We can design any visual direction around your business, audience, offer, and content.</p>
          <div class="u-full-actions">
            <a href="mailto:${UNIQUE_SALES_EMAIL}?subject=${subject(sample)}">Book this style</a>
            <button type="button" data-scroll-modules>See sections</button>
          </div>
        </div>
        <div class="u-full-stage">
          ${miniTemplates[sample.id](sample)}
        </div>
        <div class="u-full-modules" id="modalModules">
          ${sample.modules.map((module) => `<div><strong>${module}</strong><span>Rebuilt with your real copy, proof, images, and conversion path.</span></div>`).join("")}
        </div>
      </section>
    </div>`;
}

gallery.innerHTML = uniqueSamples.map(renderUniqueCard).join("");

gallery.addEventListener("click", (event) => {
  const open = event.target.closest("[data-unique-open]");
  if (!open) return;
  const sample = uniqueSamples.find((item) => item.id === open.dataset.uniqueOpen);
  modalPanel.innerHTML = renderUniqueFull(sample);
  modal.style.cssText = uniqueStyle(sample);
  modal.classList.add("open");
  document.body.style.overflow = "hidden";
});
