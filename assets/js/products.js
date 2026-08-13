// 제품: /data/products.json을 읽어 HOME 미리보기, 제품 목록(필터+검색), 제품 상세를 렌더링
(function () {
  const dataUrl = (window.SITE_ROOT || "./") + "data/products.json";

  async function loadProducts() {
    const res = await fetch(dataUrl);
    if (!res.ok) throw new Error("제품 데이터를 불러오지 못했습니다.");
    return res.json();
  }

  function metaLine(p) {
    const parts = [p.storage, p.origin].filter((v) => v && v !== "-");
    return parts.length ? parts.join(" · ") : p.categories.join(" · ");
  }

  function cardHTML(p) {
    const root = window.SITE_ROOT || "./";
    const href = `${root}pages/product-detail.html?id=${p.id}`;
    const img = p.image
      ? `<img src="${root}${p.image}" alt="${p.name}" loading="lazy">`
      : `<div class="img-placeholder" role="img" aria-label="${p.name} 이미지 (준비 중)">이미지 준비 중<br>${p.name}</div>`;
    return `
      <a class="card" href="${href}" style="display:block;">
        ${img}
        <div class="card-body">
          <h3>${p.name}</h3>
          <p>${metaLine(p)}</p>
        </div>
      </a>
    `;
  }

  function renderPreview(products, wrap) {
    // 주력 매출 카테고리인 마라탕·훠궈 재료 위주로 노출 (같은 재료군 내에서 다양하게 선정)
    const malatang = products.filter((p) => p.categories.includes("마라탕·훠궈 재료"));
    const seen = new Set();
    const picks = [];
    for (const p of malatang) {
      const otherCat = p.categories.find((c) => c !== "마라탕·훠궈 재료") || "마라탕·훠궈 재료";
      if (seen.has(otherCat)) continue;
      seen.add(otherCat);
      picks.push(p);
      if (picks.length === 6) break;
    }
    for (const p of malatang) {
      if (picks.length === 6) break;
      if (!picks.includes(p)) picks.push(p);
    }
    wrap.innerHTML = picks.map((p) => cardHTML(p)).join("");
  }

  function renderGrid(products, wrap) {
    wrap.innerHTML = products.length
      ? products.map((p) => cardHTML(p)).join("")
      : `<p style="color:var(--color-stone);">검색 결과가 없습니다.</p>`;
  }

  function renderFilterBar(products, bar, grid, searchInput) {
    const rest = [...new Set(products.flatMap((p) => p.categories))].filter(
      (c) => c !== "마라탕·훠궈 재료"
    );
    const categories = ["전체", "마라탕·훠궈 재료", ...rest];
    bar.innerHTML = categories
      .map((c, i) => `<button type="button" class="${i === 0 ? "active" : ""}" data-category="${c}">${c} (${c === "전체" ? products.length : products.filter((p) => p.categories.includes(c)).length})</button>`)
      .join("");

    function applyFilter() {
      const activeBtn = bar.querySelector("button.active");
      const cat = activeBtn ? activeBtn.dataset.category : "전체";
      const q = (searchInput ? searchInput.value : "").trim();
      let filtered = cat === "전체" ? products : products.filter((p) => p.categories.includes(cat));
      if (q) filtered = filtered.filter((p) => p.name.includes(q));
      renderGrid(filtered, grid);
    }

    bar.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        bar.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        applyFilter();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", applyFilter);
    }
  }

  function renderDetail(products, wrap) {
    const root = window.SITE_ROOT || "./";
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const product = products.find((p) => String(p.id) === id) || products[0];
    if (!product) {
      wrap.innerHTML = "<p>등록된 제품이 없습니다.</p>";
      return;
    }
    document.title = `${product.name} — 이레푸드서비스 주식회사`;
    const img = product.image
      ? `<img src="${root}${product.image}" alt="${product.name}" style="width:100%; max-width:420px; display:block;">`
      : `<div class="img-placeholder" style="min-height:320px;" role="img" aria-label="${product.name} 이미지 (준비 중)">이미지 준비 중<br>${product.name}</div>`;
    wrap.innerHTML = `
      ${img}
      <h1 style="margin-top:24px;">${product.name}</h1>
      <div class="info-row"><strong>보관방법</strong><span>${product.storage}</span></div>
      <div class="info-row"><strong>원산지</strong><span>${product.origin}</span></div>
      <div class="info-row"><strong>카테고리</strong><span>${product.categories.join(" · ")}</span></div>
    `;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const previewWrap = document.querySelector("[data-product-preview]");
    const gridWrap = document.querySelector("[data-product-grid]");
    const filterBar = document.querySelector("[data-product-filter]");
    const searchInput = document.querySelector("[data-product-search]");
    const detailWrap = document.querySelector("[data-product-detail]");
    if (!previewWrap && !gridWrap && !detailWrap) return;

    loadProducts()
      .then((products) => {
        if (previewWrap) renderPreview(products, previewWrap);
        if (gridWrap) {
          renderGrid(products, gridWrap);
          if (filterBar) renderFilterBar(products, filterBar, gridWrap, searchInput);
        }
        if (detailWrap) renderDetail(products, detailWrap);
      })
      .catch((err) => {
        const target = previewWrap || gridWrap || detailWrap;
        if (target) target.innerHTML = `<p>${err.message}</p>`;
      });
  });
})();
