# 이레푸드서비스 주식회사 홈페이지

`website-build-prompt-final.md` 프롬프트를 기반으로 제작된 GitHub Pages 정적 사이트입니다. 순수 HTML/CSS/JS(바닐라)로 제작되어 빌드 도구 없이 그대로 배포할 수 있습니다.

## 폴더 구조

```
index.html                 ← 루트 진입점 (HOME)
pages/
  company.html              COMPANY (인사말/연혁/오시는 길)
  business.html              BUSINESS (사업소개)
  product.html                PRODUCT (제품 목록/필터)
  product-detail.html         제품 상세 템플릿
  customer.html                CUSTOMER (공지사항 + 1:1 문의)
  notice-detail.html           공지사항 상세 템플릿
  terms.html / privacy.html / email-policy.html  ← 하단 법적 고지 페이지
assets/
  css/style.css
  js/main.js        (모바일 메뉴, 히어로 캐러셀)
  js/notices.js      (공지사항 렌더링)
  js/products.js       (제품 렌더링/필터)
  js/contact.js          (Formspree 문의 폼 제출)
data/
  notices.json        공지사항 데이터
  products.json         제품 데이터
```

### 이미지 자산

| 파일 | 용도 | 비고 |
|---|---|---|
| `assets/images/logo.png` | 헤더 로고 | 원본 로고 파일에서 여백 제거 후 크롭 |
| `assets/images/favicon.png` | 파비콘 | 로고의 원형 심볼만 정사각형으로 크롭 |
| `assets/images/poster-malatang.jpg` | HOME "CAMPAIGN" 섹션 이미지 | 원본을 웹용으로 리사이즈(900px)/압축 |

나머지 카드/히어로/제품 이미지는 아직 회색 placeholder 박스입니다. 실제 촬영 이미지가 준비되면 같은 방식(`assets/images/`에 넣고 `<img>` 태그로 교체)으로 추가하면 됩니다.

모든 리소스 경로는 **상대경로**로 작성되어 있어, User/Org 페이지(`사용자명.github.io`)와 프로젝트 페이지(`사용자명.github.io/저장소명`) 어느 쪽으로 배포해도 정상 동작합니다.

## 1. GitHub Pages 배포 방법

1. 이 폴더 전체를 GitHub 저장소로 push
2. 저장소 Settings → Pages 이동
3. **Source**: `Deploy from a branch` 선택
4. **Branch**: `main` (또는 사용 브랜치) / **Folder**: `/ (root)` 선택 → Save
5. 몇 분 후 `https://사용자명.github.io/저장소명/` (또는 `https://사용자명.github.io/`)에서 접속 확인

## 2. 로컬 미리보기

⚠️ **`index.html`을 더블클릭해서 `file://`로 직접 열면 안 됩니다.** 공지사항/제품 데이터를 `fetch()`로 불러오는데, 브라우저가 로컬 파일 간 fetch를 CORS로 차단합니다. 반드시 로컬 서버를 통해 열어주세요.

```bash
# 방법 1: Node.js가 있다면
npx live-server

# 방법 2: Python이 있다면 (프로젝트 루트에서 실행)
python3 -m http.server 8000
# 이후 브라우저에서 http://localhost:8000 접속
```

## 3. 공지사항 추가 방법

`data/notices.json`에 아래 형식으로 항목을 추가하면 자동으로 HOME 미리보기와 CUSTOMER 목록에 반영됩니다. 코드 수정은 필요 없습니다.

```json
{
  "id": 6,
  "date": "2026-08-11",
  "title": "새 공지 제목",
  "body": "<p>공지 본문 (HTML 사용 가능)</p>"
}
```

## 4. 제품 정보 수정 방법

`data/products.json`의 각 항목이 예시 데이터입니다. `category`(필터 분류), `name`, `spec`, `origin`, `description`을 실제 취급 제품으로 교체해주세요. 이미지 파일 없이 회색 placeholder 박스로 표시되며, 실제 사진이 준비되면 `assets/js/products.js`의 `cardHTML`/`renderDetail` 함수에서 `<img>` 태그로 교체하면 됩니다.

## 5. Formspree 설정 방법 (1:1 문의 폼)

1. [formspree.io](https://formspree.io)에서 무료 계정 생성 후 새 폼 생성, 알림 받을 이메일(`irefood@irefood.com`) 등록
2. 발급된 엔드포인트 URL(`https://formspree.io/f/xxxxxxx`)을 아래 3개 파일의 `action` 속성에 동일하게 입력
   - `pages/customer.html`의 `<form data-contact-form action="...">`
3. Formspree endpoint는 서버 시크릿이 아닌 공개 식별자이므로 코드에 그대로 넣어도 안전합니다.
4. **무료 플랜은 월 50건 제출 제한**이 있습니다. 문의량이 많아지면 유료 플랜으로 업그레이드하세요.
5. 스팸 방지를 위해 숨겨진 허니팟 필드(`_gotcha`)가 이미 적용되어 있습니다. 필요 시 Formspree 대시보드에서 reCAPTCHA도 추가로 설정할 수 있습니다.

## 6. Kakao Map 설정 방법 (오시는 길)

1. [Kakao Developers](https://developers.kakao.com)에서 애플리케이션 생성
2. 앱 키 중 **JavaScript 키** 복사
3. `pages/company.html` 하단 `const KAKAO_MAP_APP_KEY = "";` 에 붙여넣기
4. Kakao Developers → 해당 앱 → **플랫폼 → Web 플랫폼 등록**에서 실제 배포 도메인(`https://사용자명.github.io`)을 등록 (등록하지 않으면 배포 후 지도가 표시되지 않습니다)
5. 키를 입력하지 않은 상태에서는 "지도 API 키 등록 후 표시됩니다" 안내 문구가 대신 표시됩니다.

## 7. 배포 전 체크리스트

- [ ] `data/products.json`을 실제 취급 제품(4~6개)으로 교체했는가
- [ ] `pages/customer.html`의 Formspree `action`을 실제 엔드포인트로 교체했는가
- [ ] `pages/company.html`의 `KAKAO_MAP_APP_KEY`를 발급받아 입력하고, 배포 도메인을 Kakao Developers에 등록했는가
- [ ] 통신판매업신고번호(각 페이지 푸터, 필요 시 별도 표기)를 실제 값으로 채웠는가 — 2020년 3월 신고 이력 있음, 스마트스토어 판매자 정보에서 확인 가능
- [ ] `pages/privacy.html`, `pages/terms.html`은 예시 초안이므로 실제 게시 전 법무 검토를 받았는가
- [ ] 실제 촬영 이미지가 준비되면 회색 placeholder 박스를 `<img>` 태그로 교체했는가
