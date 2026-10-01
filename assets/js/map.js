// 오시는 길: 카카오맵 (도메인이 Kakao Developers에 등록되지 않았으면 안내 링크로 대체)
document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("map");
  if (!el) return;
  const ADDR = "경기 구리시 갈매순환로166번길 46";
  const fallback = () => { el.innerHTML = `<div>지도를 불러올 수 없습니다.<br><a href="https://map.kakao.com/?q=${encodeURIComponent(ADDR)}" target="_blank" rel="noopener" style="text-decoration:underline">카카오맵에서 보기 →</a></div>`; };
  const s = document.createElement("script");
  s.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=84c40287426ed1f4fbbbaa04e4d73a54&libraries=services&autoload=false";
  s.onerror = fallback;
  s.onload = () => {
    if (!window.kakao || !kakao.maps) return fallback();
    kakao.maps.load(() => {
      el.style.display = "block"; el.style.padding = 0;
      const map = new kakao.maps.Map(el, { center: new kakao.maps.LatLng(37.6423, 127.1467), level: 4 });
      new kakao.maps.services.Geocoder().addressSearch(ADDR, (r, st) => {
        if (st !== kakao.maps.services.Status.OK) return;
        const pos = new kakao.maps.LatLng(r[0].y, r[0].x);
        map.setCenter(pos); new kakao.maps.Marker({ position: pos, map });
      });
    });
  };
  document.head.appendChild(s);
});
