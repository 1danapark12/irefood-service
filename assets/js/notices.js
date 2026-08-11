// 공지사항: /data/notices.json을 읽어 목록/상세/HOME 미리보기를 렌더링
// 주의: file://로 직접 열면 fetch()가 CORS로 차단됨 — 반드시 로컬 서버로 접속할 것
(function () {
  const dataUrl = (window.SITE_ROOT || "./") + "data/notices.json";

  function formatDate(str) {
    return str;
  }

  async function loadNotices() {
    const res = await fetch(dataUrl);
    if (!res.ok) throw new Error("공지사항 데이터를 불러오지 못했습니다.");
    return res.json();
  }

  function renderPreview(notices, wrap, limit) {
    wrap.innerHTML = "";
    notices.slice(0, limit).forEach((n) => {
      const li = document.createElement("li");
      li.className = "notice-item";
      li.innerHTML = `
        <a href="${window.SITE_ROOT || "./"}pages/notice-detail.html?id=${n.id}">${n.title}</a>
        <span class="date">${formatDate(n.date)}</span>
      `;
      wrap.appendChild(li);
    });
  }

  function renderList(notices, wrap) {
    renderPreview(notices, wrap, notices.length);
  }

  function renderDetail(notices, wrap) {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const notice = notices.find((n) => String(n.id) === id) || notices[0];
    if (!notice) {
      wrap.innerHTML = "<p>등록된 공지사항이 없습니다.</p>";
      return;
    }
    document.title = `${notice.title} — 이레푸드서비스 주식회사`;
    wrap.innerHTML = `
      <p class="date" style="margin-bottom:8px;">${formatDate(notice.date)}</p>
      <h1>${notice.title}</h1>
      <div class="notice-body">${notice.body}</div>
    `;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const previewWrap = document.querySelector("[data-notice-preview]");
    const listWrap = document.querySelector("[data-notice-list]");
    const detailWrap = document.querySelector("[data-notice-detail]");
    if (!previewWrap && !listWrap && !detailWrap) return;

    loadNotices()
      .then((notices) => {
        const sorted = [...notices].sort((a, b) => (a.date < b.date ? 1 : -1));
        if (previewWrap) renderPreview(sorted, previewWrap, 3);
        if (listWrap) renderList(sorted, listWrap);
        if (detailWrap) renderDetail(sorted, detailWrap);
      })
      .catch((err) => {
        const target = previewWrap || listWrap || detailWrap;
        if (target) target.innerHTML = `<p>${err.message}</p>`;
      });
  });
})();
