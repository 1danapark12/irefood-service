# 이레푸드서비스 홈페이지 (ktlea 레이아웃 기반)

## 로컬 미리보기 (file:// 로 열면 JSON 로딩이 막힙니다)
    cd irefood-ktlea && python3 -m http.server 8766   # http://localhost:8766

## 구조
- `build.py` : 공통 헤더/푸터를 모든 HTML에 넣어 생성 → 메뉴·연락처·연혁을 고칠 땐 이 파일 수정 후 `python3 build.py` (약관 3종은 `pages/`의 HTML을 직접 수정)
- `data/products.json` (제품 487개), `data/notices.json` (공지) : 항목 추가로 운영
- `assets/images/hero/` 히어로 사진, `assets/images/products/` 제품 사진(483개)

## 배포 전 확인
1. 문의 폼: `build.py`의 `YOUR_FORM_ID`를 Formspree 폼 ID로 교체 (미설정 시 메일 앱으로 대체 전송)
2. 카카오맵: Kakao Developers > 플랫폼 > Web 에 배포 도메인 등록
3. 약관 3종은 예시 초안 → 게시 전 검토
