# 이레푸드서비스 홈페이지 (ktlea 레이아웃 기반)

## 로컬 미리보기 (file:// 로 열면 JSON 로딩이 막힙니다)
    cd irefood-ktlea && python3 -m http.server 8766   # http://localhost:8766

## 구조
- `build.py` : 공통 헤더/푸터를 모든 HTML에 넣어 생성 → 메뉴·연락처·연혁을 고칠 땐 이 파일 수정 후 `python3 build.py` (약관 3종은 `pages/`의 HTML을 직접 수정)
- `build.py` 가 함께 만드는 파일: `sitemap.xml`, `robots.txt`, `llms.txt`(AI 검색용 회사 요약), 각 페이지의 canonical·구조화 데이터(JSON-LD)·FAQ. 업력(년수)·저작권 연도·품목 수는 빌드할 때 자동 계산되므로 **데이터를 바꾼 뒤엔 반드시 `python3 build.py`** 를 다시 실행
- `legal/*.html` : 이용약관·개인정보처리방침·이메일무단수집거부 본문 (여기를 고치고 build)
- 사업소개 FAQ 문답은 `build.py` 의 `FAQ` 목록에서 수정
- `data/products.json` (제품 459개), `data/notices.json` (공지) : 항목 추가로 운영
- `assets/images/hero/` 히어로 사진, `assets/images/products/` 제품 사진(655개)

## 배포 전 확인
1. 문의 폼: `build.py`의 `YOUR_FORM_ID`를 Formspree 폼 ID로 교체 (미설정 시 메일 앱으로 대체 전송)
2. 카카오맵: Kakao Developers > 플랫폼 > Web 에 배포 도메인 등록
3. 약관 3종(`legal/`)은 게시 전 검토 — 개인정보처리방침의 보호책임자 성명/직책 기재 권장
4. 배포 후 네이버 서치어드바이저·구글 서치콘솔에 `https://www.irefood.com/sitemap.xml` 제출
