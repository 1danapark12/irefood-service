// 1:1 문의: 담아둔 견적 제품 표시 + 동의 체크 시 전송 활성화 + Formspree(AJAX), 미설정 시 메일 앱으로 대체
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;
  const btn = form.querySelector("button[type=submit]");
  const consent = form.querySelector("#consent");
  const status = form.querySelector("[data-form-status]");
  const msg = form.querySelector("#message");
  const box = document.querySelector("[data-quote-box]");
  const sync = () => { btn.disabled = !consent.checked; };
  consent.addEventListener("change", sync); sync();

  const items = () => (window.IRE_CART ? window.IRE_CART.get() : (() => { try { return JSON.parse(localStorage.getItem("irefood_quote")) || []; } catch (e) { return []; } })());
  function renderBox() {
    const c = items();
    if (!box) return;
    box.hidden = !c.length;
    box.querySelector("ul").innerHTML = c.map((x) => `<li><span>${x.name}</span><button type="button" data-rm="${x.id}">삭제</button></li>`).join("");
  }
  box?.addEventListener("click", (e) => {
    const id = e.target.dataset.rm; if (!id) return;
    const c = items().filter((x) => String(x.id) !== id);
    try { localStorage.setItem("irefood_quote", JSON.stringify(c)); } catch (er) {}
    renderBox();
  });
  renderBox();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (form.querySelector(".honeypot").value) return;
    const c = items();
    const quote = c.length ? `\n\n[견적 요청 제품]\n${c.map((x) => "- " + x.name).join("\n")}` : "";
    const data = new FormData(form);
    data.set("message", msg.value + quote);
    const endpoint = form.getAttribute("action");
    if (/YOUR_FORM_ID/.test(endpoint)) {
      // Formspree 미설정: 메일 앱으로 대체 전송
      const body = `이름: ${data.get("name")}\n연락처: ${data.get("phone")}\n이메일: ${data.get("email")}\n\n${data.get("message")}`;
      location.href = `mailto:irefood@irefood.com?subject=${encodeURIComponent("[홈페이지 문의] " + data.get("name"))}&body=${encodeURIComponent(body)}`;
      status.textContent = "메일 앱이 열립니다. 전송 버튼을 눌러 문의를 완료해주세요.";
      return;
    }
    btn.disabled = true; status.textContent = "전송 중…";
    try {
      const r = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
      if (!r.ok) throw 0;
      form.reset(); sync();
      try { localStorage.removeItem("irefood_quote"); } catch (er) {}
      renderBox();
      status.textContent = "문의가 접수되었습니다. 확인 후 빠르게 연락드리겠습니다.";
    } catch (er) { status.textContent = "전송에 실패했습니다. 전화(010-4751-1668)로 문의해주세요."; btn.disabled = false; }
  });
});
