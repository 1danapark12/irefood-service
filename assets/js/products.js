// 제품: /data/products.json을 읽어 HOME 미리보기, 제품 목록(필터), 제품 상세를 렌더링
(function () {
  const dataUrl = (window.SITE_ROOT || "./") + "data/products.json";

  async function loadProducts() {
    const res = await fetch(dataUrl);
    if (!res.ok) throw new Error("제품 데이터를 불러오지 못했습니다.");
    return res.json();
  }

  function cardHTML(p) {
    const href = `${window.SITE_ROOT || "./"}pages/product-detail.html?id=${p.id}`;
    return `
      <a class="card" href="${href}" style="display:block;">
        <div class="img-placeholder" role="img" aria-label="${p.name} 이미지 (준비 중)">이미지 준비 중<br>${p.name}</div>
        <div class="card-body">
          <h3>${p.name}</h3>
          <p>${p.spec} · ${p.origin}</p>
        </div>
      </a>
    `;
  }

  function renderPreview(products, wrap) {
    wrap.innerHTML = products.slice(0, 6).map((p) => cardHTML(p)).join("");
  }

  function renderGrid(products, wrap) {
    wrap.innerHTML = products.map((p) => cardHTML(p)).join("");
  }

  function renderFilterBar(products, bar, grid) {
    const categories = ["전체", ...new Set(products.map((p) => p.category))];
    bar.innerHTML = categories
      .map((c, i) => `<button type="button" class="${i === 0 ? "active" : ""}" data-category="${c}">${c}</button>`)
      .join("");
    bar.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        bar.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const cat = btn.dataset.category;
        const filtered = cat === "전체" ? products : products.filter((p) => p.category === cat);
        renderGrid(filtered, grid);
      });
    });
  }

  function renderDetail(products, wrap) {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const product = products.find((p) => String(p.id) === id) || products[0];
    if (!product) {
      wrap.innerHTML = "<p>등록된 제품이 없습니다.</p>";
      return;
    }
    document.title = `${product.name} — 이레푸드서비스 주식회사`;
    wrap.innerHTML = `
      <div class="img-placeholder" style="min-height:320px;" role="img" aria-label="${product.name} 이미지 (준비 중)">이미지 준비 중<br>${product.name}</div>
      <h1 style="margin-top:24px;">${product.name}</h1>
      <div class="info-row"><strong>규격</strong><span>${product.spec}</span></div>
      <div class="info-row"><strong>원산지</strong><span>${product.origin}</span></div>
      <div class="info-row"><strong>카테고리</strong><span>${product.category}</span></div>
      <p style="margin-top:16px;">${product.description}</p>
    `;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const previewWrap = document.querySelector("[data-product-preview]");
    const gridWrap = document.querySelector("[data-product-grid]");
    const filterBar = document.querySelector("[data-product-filter]");
    const detailWrap = document.querySelector("[data-product-detail]");
    if (!previewWrap && !gridWrap && !detailWrap) return;

    loadProducts()
      .then((products) => {
        if (previewWrap) renderPreview(products, previewWrap);
        if (gridWrap) {
          renderGrid(products, gridWrap);
          if (filterBar) renderFilterBar(products, filterBar, gridWrap);
        }
        if (detailWrap) renderDetail(products, detailWrap);
      })
      .catch((err) => {
        const target = previewWrap || gridWrap || detailWrap;
        if (target) target.innerHTML = `<p>${err.message}</p>`;
      });
  });
})();
