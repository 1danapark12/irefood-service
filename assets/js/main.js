// 공통: 헤더 스크롤/메뉴, 히어로 슬라이더, 스크롤 등장, 맨 위로
document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // 헤더: 아래로 스크롤 시 숨기고, 위로 스크롤 시 어두운 배경으로 다시 표시
  let last = 0;
  window.addEventListener("scroll", () => {
    const cur = window.scrollY;
    if (cur > 30) {
      header.classList.add("scrolled");
      header.classList.toggle("show", cur < last);
    } else {
      header.classList.remove("scrolled", "show");
    }
    $(".float-call")?.classList.toggle("show", cur > window.innerHeight * 0.6);
    last = cur <= 0 ? 0 : cur;
  }, { passive: true });

  // GNB 서브메뉴(데스크톱 hover)
  const bg = $(".submenubg");
  $$(".gnb-menu > li").forEach((li) => {
    const sub = $(".submenu", li);
    if (!sub) return;
    li.addEventListener("mouseenter", () => {
      $$(".submenu").forEach((s) => { s.style.display = "none"; });
      sub.style.display = "block"; sub.style.opacity = 1;
      if (bg) { bg.style.display = "block"; bg.style.height = "130px"; bg.style.opacity = 1; }
    });
    li.addEventListener("mouseleave", () => {
      sub.style.display = "none"; sub.style.opacity = 0;
      if (bg) { bg.style.height = "0"; bg.style.opacity = 0; }
    });
  });

  // 모바일 전체 메뉴
  const all = $(".all-menu");
  const toggle = (open) => { all.classList.toggle("open", open); document.body.classList.toggle("lock", open); };
  $(".gnb-btn")?.addEventListener("click", () => toggle(true));
  $(".all-menu .close-btn")?.addEventListener("click", () => toggle(false));
  $$(".all-menu a").forEach((a) => a.addEventListener("click", () => toggle(false)));

  // 맨 위로
  $(".scroll-top")?.addEventListener("click", (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); });

  // 히어로 제목: 글자 단위 등장 (처음 한 번)
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let n = 0;
    $$("[data-split]").forEach((el) => {
      const cs = [...el.textContent].map((ch) => { const s = document.createElement("span"); s.className = "split-c"; s.textContent = ch; s.style.animationDelay = 0.15 + n++ * 0.045 + "s"; return s; });
      el.replaceChildren(...cs);
    });
  }

  // 강점 줄에 올리거나 누르면 오른쪽 사진이 그 줄의 것으로 바뀐다
  const peek = $("[data-peek]");
  if (peek) {
    const rows = $$("li", peek), shots = $$(".why-photo img");
    const pick = (i) => { rows.forEach((r, k) => r.classList.toggle("on", k === i)); shots.forEach((im, k) => im.classList.toggle("on", k === i)); };
    rows.forEach((r, i) => { r.addEventListener("mouseenter", () => pick(i)); r.addEventListener("click", () => pick(i)); });
  }

  // 히어로 슬라이더
  const slides = $$(".slide");
  if (slides.length) {
    const DUR = 6000;
    const fill = $(".progress .fill"), num = $(".progress .num"), pp = $(".pp");
    let cur = 0, playing = true, start = performance.now(), elapsed = 0, raf;
    const pad = (n) => String(n).padStart(2, "0");
    const show = (i) => {
      slides[cur].classList.remove("active");
      cur = (i + slides.length) % slides.length;
      slides[cur].classList.add("active");
      num.textContent = `${pad(cur + 1)} / ${pad(slides.length)}`;
      elapsed = 0; start = performance.now();
    };
    const tick = (t) => {
      if (playing) elapsed = t - start;
      fill.style.width = Math.min(elapsed / DUR, 1) * 100 + "%";
      if (elapsed >= DUR) show(cur + 1);
      raf = requestAnimationFrame(tick);
    };
    $(".prev")?.addEventListener("click", () => show(cur - 1));
    $(".next")?.addEventListener("click", () => show(cur + 1));
    pp?.addEventListener("click", () => {
      playing = !playing;
      pp.classList.toggle("paused", !playing);
      pp.setAttribute("aria-label", playing ? "슬라이드 멈춤" : "슬라이드 재생");
      if (playing) start = performance.now() - elapsed;
    });
    num.textContent = `${pad(1)} / ${pad(slides.length)}`;
    raf = requestAnimationFrame(tick);
  }
});
