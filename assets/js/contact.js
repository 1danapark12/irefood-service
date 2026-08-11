// 1:1 문의: Formspree AJAX 제출
// ⚠️ 각 페이지 <form data-contact-form action="https://formspree.io/f/YOUR_FORM_ID"> 의
// action 값을 실제 발급받은 Formspree 엔드포인트로 교체할 것 (README 참고)
// Formspree endpoint는 서버 시크릿이 아닌 공개 식별자이므로 코드에 직접 넣어도 안전함

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  const consent = form.querySelector("#consent");
  const submitBtn = form.querySelector('button[type="submit"]');
  const statusEl = form.querySelector("[data-form-status]");

  if (consent && submitBtn) {
    submitBtn.disabled = true;
    consent.addEventListener("change", () => {
      submitBtn.disabled = !consent.checked;
    });
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // 허니팟: 봇이 채운 경우 조용히 무시
    const honeypot = form.querySelector('input[name="_gotcha"]');
    if (honeypot && honeypot.value) return;

    if (consent && !consent.checked) {
      statusEl.textContent = "개인정보 수집·이용에 동의해주세요.";
      statusEl.className = "form-status error";
      return;
    }

    submitBtn.disabled = true;
    statusEl.textContent = "전송 중...";
    statusEl.className = "form-status";

    try {
      const res = await fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      });

      if (res.ok) {
        statusEl.textContent = "문의가 접수되었습니다. 빠른 시일 내에 답변드리겠습니다.";
        statusEl.className = "form-status success";
        form.reset();
      } else {
        throw new Error("전송에 실패했습니다. 잠시 후 다시 시도해주세요.");
      }
    } catch (err) {
      statusEl.textContent = err.message || "전송 중 오류가 발생했습니다.";
      statusEl.className = "form-status error";
    } finally {
      submitBtn.disabled = !(consent ? consent.checked : true);
    }
  });
});
