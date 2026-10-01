// 공지사항: data/notices.json → 홈 리스트 / 목록 / 상세
(function () {
  const ROOT = window.SITE_ROOT || "./";
  const dot = (d) => d.replace(/-/g, ".");
  const row = (n) => `<li><a href="${ROOT}pages/notice-detail.html?id=${n.id}"><div><p class="lt">Notice</p><p class="tx">${n.title}</p></div><span class="dt">${dot(n.date)}</span></a></li>`;
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
        det.innerHTML = `<p class="lt" style="color:var(--gold);font-weight:700;letter-spacing:.1em;margin:0">Notice · ${dot(n.date)}</p><h2 style="font-size:34px;line-height:1.4;margin:10px 0 36px">${n.title}</h2><div class="notice-body">${n.body}</div>`;
      }
    }).catch(() => { (prev || lst || det).innerHTML = "<li>공지를 불러오지 못했습니다. 로컬 서버(http://localhost)로 열어주세요.</li>"; });
  });
})();
