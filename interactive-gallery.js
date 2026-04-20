const SALES_EMAIL = "callmeie@proton.me";

const samples = [
  {
    id: "copper",
    layout: "product",
    name: "Copper Product Studio",
    type: "Premium product",
    copy: "For craft brands, makers, hardware, and premium local products that need warmth and sales clarity.",
    bg: "#f4bf80",
    fg: "#160c06",
    accent: "#1f1007",
    shape: "#d7b39d",
    headline: "var(--serif)",
    buttonText: "#fff4de",
    visual: "shapes",
    proof: ["Serif-first product story", "Premium launch layout", "Photography-ready structure"]
  },
  {
    id: "chrome",
    layout: "commerce",
    name: "Chrome Commerce",
    type: "Futuristic commerce",
    copy: "For ecommerce, coffee, tech retail, and product launches that need dark atmosphere and sharp contrast.",
    bg: "#040807",
    fg: "#f3fff0",
    accent: "#a6ff2d",
    shape: "#dcff83",
    headline: "var(--display)",
    buttonText: "#061006",
    visual: "shapes",
    proof: ["Product launch hero", "High-contrast checkout story", "Motion-ready catalog blocks"]
  },
  {
    id: "quiet",
    layout: "saas",
    name: "Quiet SaaS",
    type: "B2B software",
    copy: "For software, agencies, tools, and operator dashboards that need restraint over hype.",
    bg: "#0e1018",
    fg: "#eef1ff",
    accent: "#8277ff",
    shape: "#1a1d2d",
    headline: "var(--display)",
    buttonText: "#f9f7ff",
    visual: "dashboard",
    proof: ["Clear product surface", "Low-noise conversion", "Operator-focused sections"]
  },
  {
    id: "trust",
    layout: "trust",
    name: "Trust Ledger",
    type: "Finance trust",
    copy: "For accountants, payment tools, legal firms, and subscription services that need calm authority.",
    bg: "#f6f8ff",
    fg: "#101a34",
    accent: "#0c2f66",
    shape: "#dceeff",
    headline: "var(--display)",
    buttonText: "#f8fbff",
    visual: "lines",
    proof: ["Trust-first hierarchy", "Compliance-safe tone", "Conversion without pressure"]
  },
  {
    id: "editorial",
    layout: "editorial",
    name: "Editorial House",
    type: "Consultant editorial",
    copy: "For consultants, writers, educators, and personal brands that need voice, authority, and depth.",
    bg: "#fbf5e9",
    fg: "#24150c",
    accent: "#2d1710",
    shape: "#c46b4d",
    headline: "var(--serif)",
    buttonText: "#fff8ef",
    visual: "shapes",
    proof: ["Magazine-like flow", "Authority-led copy", "Article and newsletter ready"]
  },
  {
    id: "growth",
    layout: "growth",
    name: "Local Growth Engine",
    type: "Local SEO",
    copy: "For trades, dentists, clinics, and local offers where ranking, calls, and booked work matter.",
    bg: "#022d1e",
    fg: "#f1fff2",
    accent: "#28e28b",
    shape: "#0c563c",
    headline: "var(--display)",
    buttonText: "#02180f",
    visual: "lines",
    proof: ["GBP conversion sections", "Service-area targeting", "Lead-focused page logic"]
  },
  {
    id: "clinic",
    layout: "clinic",
    name: "Clinic Calm",
    type: "Wellness clinic",
    copy: "For aesthetic clinics, therapists, wellness brands, and private practices that need calm premium trust.",
    bg: "#f1e6d9",
    fg: "#25160e",
    accent: "#22140d",
    shape: "#d6bbae",
    headline: "var(--serif)",
    buttonText: "#fff8ef",
    visual: "shapes",
    proof: ["Soft appointment flow", "Private practice tone", "Service menu ready"]
  },
  {
    id: "ops",
    layout: "ops",
    name: "Agent Ops",
    type: "AI operations",
    copy: "For AI automation, managed workflows, support desks, and internal tools that need a visible control room.",
    bg: "#071016",
    fg: "#e8f9ff",
    accent: "#39d6f6",
    shape: "#102632",
    headline: "var(--display)",
    buttonText: "#031017",
    visual: "dashboard",
    proof: ["Live status language", "Automation proof blocks", "Ops dashboard aesthetic"]
  },
  {
    id: "trades",
    layout: "trades",
    name: "Bold Trades",
    type: "Trade services",
    copy: "For builders, roofers, plumbers, and emergency services that need instant clarity and phone-first action.",
    bg: "#fff238",
    fg: "#11110f",
    accent: "#11110f",
    shape: "#fff238",
    headline: "var(--display)",
    buttonText: "#fff238",
    visual: "badge",
    proof: ["24-hour call focus", "Service proof fast", "High-contrast mobile CTA"]
  },
  {
    id: "heritage",
    layout: "heritage",
    name: "Heritage Story",
    type: "Archive brand",
    copy: "For family businesses, photographers, heritage brands, and story-led work that needs depth and memory.",
    bg: "#17110d",
    fg: "#f7eadb",
    accent: "#b6844c",
    shape: "#5b5149",
    headline: "var(--serif)",
    buttonText: "#1a1009",
    visual: "lines",
    proof: ["Archive-style narrative", "Image-led story pages", "Family business authority"]
  }
];

const gallery = document.querySelector("#gallery");
const modal = document.querySelector("#modal");
const modalPanel = document.querySelector("#modalPanel");

function styles(sample) {
  return [
    `--bg:${sample.bg}`,
    `--fg:${sample.fg}`,
    `--accent:${sample.accent}`,
    `--shape:${sample.shape}`,
    `--headline:${sample.headline}`,
    `--buttonText:${sample.buttonText}`
  ].join(";");
}

function visual(sample) {
  if (sample.visual === "dashboard") {
    return `<div class="visual-dashboard"><span>87</span><span>$0.47</span><span>live pipeline</span></div>`;
  }
  if (sample.visual === "lines") {
    return `<div class="visual-lines"><span></span><span></span><span></span></div>`;
  }
  if (sample.visual === "badge") {
    return `<div class="visual-lines"><span></span><span></span><span></span></div><div class="shape one" style="border-radius:0;transform:rotate(-4deg);width:55%;height:38%;left:25%;top:30%;background:transparent;border:6px solid var(--fg);box-shadow:none;"></div><strong class="trade-badge">24HR</strong>`;
  }
  return `<div class="shape one"></div><div class="shape two"></div>`;
}

function card(sample, index) {
  const subject = encodeURIComponent(`Website style enquiry - ${sample.name}`);
  return `
    <article class="site-card layout-${sample.layout}" style="${styles(sample)}">
      <div class="mini-browser">
        <nav class="mini-nav">
          <span>${String(index + 1).padStart(2, "0")} / ${sample.type}</span>
          <div class="mini-nav-links">
            <button type="button" data-panel="0">Work</button>
            <button type="button" data-panel="1">Offer</button>
            <a href="mailto:${SALES_EMAIL}?subject=${subject}">Contact</a>
          </div>
        </nav>
        <div class="mini-hero">
          <div class="mini-copy">
            <h3>${sample.name}</h3>
            <p>${sample.copy}</p>
            <div class="mini-cta">
              <button type="button" data-open="${sample.id}">Preview homepage</button>
              <button type="button" class="ghost" data-cycle>${sample.layout === "trades" ? "Emergency offer" : sample.layout === "editorial" ? "Read approach" : "Switch panel"}</button>
            </div>
          </div>
          <div class="mini-visual" aria-hidden="true">${visual(sample)}</div>
        </div>
      </div>
      <div class="mini-detail">
        ${sample.proof.map((item, proofIndex) => `<button type="button" data-detail ${proofIndex === 0 ? "class='active'" : ""}><strong>${item}</strong><span>${proofIndex === 0 ? "First impression" : proofIndex === 1 ? "Customer path" : "Conversion"} built into this direction.</span></button>`).join("")}
      </div>
      <footer class="card-footer">
        <div>
          <strong>${sample.name}</strong>
          <span>${sample.type} website direction</span>
        </div>
        <button class="open-demo" type="button" data-open="${sample.id}">Open this style</button>
      </footer>
    </article>
  `;
}

function fullSite(sample) {
  const subject = encodeURIComponent(`Website style enquiry - ${sample.name}`);
  return `
    <div class="layout-${sample.layout}" style="${styles(sample)}">
      <div class="modal-top">
        <strong>${sample.name}</strong>
        <button class="modal-close" type="button" data-close>Close sample</button>
      </div>
      <section class="full-site">
        <nav class="full-nav">
          <strong>${sample.name}</strong>
          <div>
            <button type="button" data-scroll-modules>Work</button>
            <button type="button" data-scroll-modules>Offer</button>
            <button type="button" data-scroll-modules>Proof</button>
            <a href="mailto:${SALES_EMAIL}?subject=${subject}">Contact</a>
          </div>
        </nav>
        <div class="full-hero">
          <div>
            <p class="eyebrow" style="color:color-mix(in srgb, var(--fg) 52%, transparent);">${sample.type}</p>
            <h2>${sample.name}</h2>
            <p>${sample.copy} Start with this direction and we will replace the sample content with your offer, photography, service areas, proof, and contact path.</p>
            <div class="full-actions">
              <a class="button" style="background:var(--accent);color:var(--buttonText);" href="mailto:${SALES_EMAIL}?subject=${subject}">Book this style</a>
              <button class="button secondary" style="color:var(--fg);border-color:color-mix(in srgb, var(--fg) 14%, transparent);background:color-mix(in srgb, var(--fg) 8%, transparent);" type="button" data-scroll-modules>See modules</button>
            </div>
          </div>
          <div class="full-visual" aria-hidden="true"></div>
        </div>
        <div class="full-proof" id="modalModules">
          ${sample.proof.map((item) => `<div class="proof"><strong>${item}</strong><span>This section would be rebuilt around your business, using your offer, proof, location, images, and customer journey.</span></div>`).join("")}
        </div>
        <div class="booking-panel" id="bookingPanel">
          <p class="eyebrow" style="color:color-mix(in srgb, var(--fg) 52%, transparent);">Selected direction</p>
          <h3>${sample.name}</h3>
          <p>Want this direction adapted for your business? Send the style name with your business type and the main action you want customers to take.</p>
          <a class="button" style="background:var(--accent);color:var(--buttonText);" href="mailto:${SALES_EMAIL}?subject=${subject}">Email about ${sample.name}</a>
        </div>
      </section>
    </div>
  `;
}

gallery.innerHTML = samples.map(card).join("");

gallery.addEventListener("click", (event) => {
  const detail = event.target.closest(".mini-detail button");
  if (detail) {
    const group = detail.closest(".mini-detail");
    group.querySelectorAll("button").forEach((button) => button.classList.remove("active"));
    detail.classList.add("active");
  }

  const panel = event.target.closest("[data-panel]");
  if (panel) {
    const group = panel.closest(".site-card").querySelector(".mini-detail");
    const buttons = Array.from(group.querySelectorAll("button"));
    buttons.forEach((button) => button.classList.remove("active"));
    buttons[Number(panel.dataset.panel)]?.classList.add("active");
  }

  const cycle = event.target.closest("[data-cycle]");
  if (cycle) {
    const group = cycle.closest(".site-card").querySelector(".mini-detail");
    const buttons = Array.from(group.querySelectorAll("button"));
    const current = buttons.findIndex((button) => button.classList.contains("active"));
    buttons.forEach((button) => button.classList.remove("active"));
    buttons[(current + 1) % buttons.length].classList.add("active");
  }

  const open = event.target.closest("[data-open]");
  if (open) {
    const sample = samples.find((item) => item.id === open.dataset.open);
    modalPanel.innerHTML = fullSite(sample);
    modal.style.cssText = styles(sample);
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
  }
});

modal.addEventListener("click", (event) => {
  if (event.target === modal || event.target.closest("[data-close]")) {
    modal.classList.remove("open");
    modalPanel.innerHTML = "";
    document.body.style.overflow = "";
    return;
  }

  if (event.target.closest("[data-scroll-modules]")) {
    modalPanel.querySelector("#modalModules")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && modal.classList.contains("open")) {
    modal.classList.remove("open");
    modalPanel.innerHTML = "";
    document.body.style.overflow = "";
  }
});
