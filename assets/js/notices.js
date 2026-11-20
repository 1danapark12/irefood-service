// 공지사항: data/notices.json → 홈 리스트 / 목록 / 상세
(function () {
  const ROOT = window.SITE_ROOT || "./";
  const dot = (d) => d.replace(/-/g, ".");
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const row = (n) => `<li><a href="${ROOT}pages/notice-detail.html?id=${n.id}"><div><p class="lt">Notice</p><p class="tx">${esc(n.title)}</p></div><span class="dt">${dot(n.date)}</span></a></li>`;
  document.addEventListener("DOMContentLoaded", () => {
    const prev = document.querySelector("[data-notice-preview]");
    const lst = document.querySelector("[data-notice-list]");
    const det = document.querySelector("[data-notice-detail]");
    if (!prev && !lst && !det) return;
    fetch(ROOT + "data/notices.json").then((r) => r.json()).then((ns) => {
      ns.sort((a, b) => b.date.localeCompare(a.date));
      if (prev) prev.innerHTML = ns.slice(0, 4).map(row).join("");
      if (lst) lst.innerHTML = ns.map(row).join("");
      if (det) {
        const n = ns.find((x) => String(x.id) === new URLSearchParams(location.search).get("id")) || ns[0];
        document.title = `${n.title} — 이레푸드서비스 주식회사`;
        det.innerHTML = `<p class="lt" style="color:var(--gold);font-weight:700;letter-spacing:.1em;margin:0">Notice · ${dot(n.date)}</p><h2 style="font-size:34px;line-height:1.4;margin:10px 0 36px">${esc(n.title)}</h2><div class="notice-body">${n.body}</div>`;
      }
    }).catch(() => {
      // 목록은 빌드 시 미리 그려 둔 HTML 이 있으면 그대로 둔다
      if (det) det.innerHTML = "<p>공지를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.</p>";
      [prev, lst].forEach((el) => { if (el && !el.children.length) el.innerHTML = "<li>공지를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.</li>"; });
    });
  });
})();
