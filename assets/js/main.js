// 공통: 모바일 메뉴 토글 + 히어로 캐러셀
document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const mobileMenu = document.querySelector(".mobile-menu");
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", String(isOpen));
    });
    mobileMenu.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => mobileMenu.classList.remove("open"));
    });
  }

  const heroSlides = document.querySelectorAll(".hero-slide");
  const heroDotsWrap = document.querySelector(".hero-dots");
  if (heroSlides.length > 1 && heroDotsWrap) {
    let current = 0;
    heroSlides.forEach((_, i) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.setAttribute("aria-label", `${i + 1}번째 배너`);
      if (i === 0) dot.classList.add("active");
      dot.addEventListener("click", () => showSlide(i));
      heroDotsWrap.appendChild(dot);
    });
    const dots = heroDotsWrap.querySelectorAll("button");

    function showSlide(index) {
      heroSlides[current].classList.remove("active");
      dots[current].classList.remove("active");
      current = index;
      heroSlides[current].classList.add("active");
      dots[current].classList.add("active");
    }

    setInterval(() => {
      showSlide((current + 1) % heroSlides.length);
    }, 5000);
  }

  // 네이버 스마트스토어 바로가기 (모든 페이지 우측 하단 고정)
  const storeLink = document.createElement("a");
  storeLink.href = "https://smartstore.naver.com/sunbong_food";
  storeLink.target = "_blank";
  storeLink.rel = "noopener";
  storeLink.className = "smartstore-float";
  storeLink.setAttribute("aria-label", "네이버 스마트스토어로 이동 (새 창)");
  storeLink.innerHTML = '<span class="smartstore-badge">N</span><span>스마트스토어 바로가기</span>';
  document.body.appendChild(storeLink);
});
