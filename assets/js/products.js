// 제품: data/products.json → 홈 롤링, 제품 목록(필터·검색·더보기), 상세, 견적 담기
(function () {
  const ROOT = window.SITE_ROOT || "./";
  const KEY = "irefood_quote";
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const cart = {
    get() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } },
    set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} document.dispatchEvent(new Event("cart:change")); },
    has(id) { return this.get().some((x) => x.id === id); },
    toggle(p) {
      const c = this.get();
      const i = c.findIndex((x) => x.id === p.id);
      i >= 0 ? c.splice(i, 1) : c.push({ id: p.id, name: p.name });
      this.set(c);
    },
  };
  window.IRE_CART = cart;

  const meta = (p) => [p.storage, p.origin].filter((v) => v && v !== "-").join(" · ") || p.categories.join(" · ");
  const imgTag = (p, cls = "") => p.image ? `<img src="${ROOT}${p.image}" alt="${esc(p.name)}" loading="lazy" ${cls}>` : `<span>이미지 준비 중</span>`;

  function card(p) {
    return `<article class="pcard">
      <a href="${ROOT}pages/product-detail.html?id=${p.id}" class="im">${imgTag(p)}</a>
      <div class="bd"><h3>${esc(p.name)}</h3><small>${esc(meta(p))}</small></div>
      <button type="button" class="add ${cart.has(p.id) ? "on" : ""}" data-id="${p.id}">${cart.has(p.id) ? "✓ 견적 담김" : "+ 견적 담기"}</button>
    </article>`;
  }

  // 홈: 세로 롤링 (마라탕·훠궈 재료 우선, 사진 있는 제품만)
  function rolling(products, wrap) {
    const pool = products.filter((p) => p.image);
    const first = pool.filter((p) => p.categories.includes("마라탕·훠궈 재료"));
    const picks = [...first.slice(0, 7), ...pool.filter((p) => !first.slice(0, 7).includes(p)).filter((_, i) => i % 29 === 0).slice(0, 5)];
    const html = picks.map((p) => `<a href="${ROOT}pages/product-detail.html?id=${p.id}"><img src="${ROOT}${p.image}" alt="${esc(p.name)}" loading="lazy"><p>${esc(p.name)}</p></a>`).join("");
    wrap.innerHTML = html + html; // 무한 롤링용 복제
  }

  const PAGE = 24;
  function list(products, grid, filterBar, search, moreBtn) {
    let cat = "전체", shown = PAGE, rows = products;
    const cats = ["전체", "마라탕·훠궈 재료", ...[...new Set(products.flatMap((p) => p.categories))].filter((c) => c !== "마라탕·훠궈 재료")];
    filterBar.innerHTML = cats.map((c, i) => `<button type="button" class="${i ? "" : "active"}" data-c="${esc(c)}">${esc(c)}</button>`).join("");
    const render = () => {
      grid.innerHTML = rows.length ? rows.slice(0, shown).map(card).join("") : `<p>검색 결과가 없습니다.</p>`;
      moreBtn.style.display = rows.length > shown ? "" : "none";
    };
    const apply = () => {
      const q = search.value.trim().toLowerCase();
      rows = products.filter((p) => (cat === "전체" || p.categories.includes(cat)) && (!q || p.name.toLowerCase().includes(q)));
      shown = PAGE; render();
    };
    filterBar.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      filterBar.querySelectorAll("button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active"); cat = b.dataset.c; apply();
    });
    search.addEventListener("input", apply);
    moreBtn.addEventListener("click", () => { shown += PAGE; render(); });
    document.addEventListener("cart:change", () => grid.querySelectorAll(".add").forEach((b) => {
      const on = cart.has(Number(b.dataset.id)); b.classList.toggle("on", on); b.textContent = on ? "✓ 견적 담김" : "+ 견적 담기";
    }));
    render();
  }

  function detail(products, wrap) {
    const id = new URLSearchParams(location.search).get("id");
    const p = products.find((x) => String(x.id) === id) || products[0];
    document.title = `${p.name} — 이레푸드서비스 주식회사`;
    wrap.innerHTML = `<div class="im">${imgTag(p)}</div>
      <div><h1>${esc(p.name)}</h1>
        <div class="info-row"><strong>보관방법</strong><span>${esc(p.storage || "-")}</span></div>
        <div class="info-row"><strong>원산지</strong><span>${esc(p.origin || "-")}</span></div>
        <div class="info-row"><strong>카테고리</strong><span>${esc(p.categories.join(" · "))}</span></div>
        <div class="btns"><button type="button" class="pill" data-add>${cart.has(p.id) ? "✓ 견적 담김" : "+ 견적 담기"}</button><a class="pill line" href="${ROOT}pages/customer.html#inquiry">견적 문의하러 가기</a></div>
      </div>`;
    wrap.querySelector("[data-add]").addEventListener("click", (e) => { cart.toggle(p); e.target.textContent = cart.has(p.id) ? "✓ 견적 담김" : "+ 견적 담기"; });
  }

  // 하단 견적 바
  function cartBar() {
    const bar = document.createElement("div");
    bar.className = "cart-bar";
    bar.innerHTML = `<span data-n></span><a class="pill" href="${ROOT}pages/customer.html#inquiry">견적 문의하기</a>`;
    document.body.appendChild(bar);
    const upd = () => { const n = cart.get().length; bar.querySelector("[data-n]").textContent = `담은 제품 ${n}개`; bar.classList.toggle("show", n > 0); };
    document.addEventListener("cart:change", upd); upd();
  }

  document.addEventListener("DOMContentLoaded", () => {
    const roll = document.querySelector("[data-rolling]");
    const grid = document.querySelector("[data-product-grid]");
    const det = document.querySelector("[data-product-detail]");
    if (!roll && !grid && !det) return;
    fetch(ROOT + "data/products.json").then((r) => { if (!r.ok) throw 0; return r.json(); }).then((products) => {
      if (roll) rolling(products, roll);
      if (grid) { list(products, grid, document.querySelector("[data-product-filter]"), document.querySelector("[data-product-search]"), document.querySelector("[data-more]")); cartBar(); grid.addEventListener("click", (e) => { const b = e.target.closest(".add"); if (b) cart.toggle(products.find((x) => x.id === Number(b.dataset.id))); }); }
      if (det) { detail(products, det); cartBar(); }
    }).catch(() => { (roll || grid || det).innerHTML = "<p>제품 데이터를 불러오지 못했습니다. 로컬 서버(http://localhost)로 열어주세요.</p>"; });
  });
})();
