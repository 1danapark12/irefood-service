#!/usr/bin/env python3
"""공통 헤더/푸터를 모든 페이지에 일관되게 넣어 HTML을 생성한다. 실행: python3 build.py"""
import os, re, json, datetime, html as _html

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(os.path.dirname(ROOT), "irefood", "pages")  # 기존 사이트 약관 본문 재사용

SITE = "https://www.irefood.com"  # 정식 주소 (canonical, sitemap, og:url 기준)
TODAY = datetime.date.today()
FOUNDED = 1998
YEARS = TODAY.year - FOUNDED  # 업력: 빌드할 때마다 자동 계산 (숫자를 직접 쓰지 말 것)
NAVER_VERIFY = "d1232523adb4906833ea39d5c0562d66070a8a9a"  # 네이버 서치어드바이저 소유확인
GOOGLE_VERIFY = "5jVOTsCNLuo-kjPYA45SDNmiX0FaXkE50mFVW6SGGp4"  # 구글 서치콘솔 소유확인
# 방문 분석. 값을 비우면("") 그 태그는 들어가지 않는다.
GOOGLE_TAG = "GTM-578KTM5N"  # 구글 애널리틱스(GA4)가 준 설치 태그. 속성 「irefood.com」, 측정 ID G-00BR4PVW5E
NAVER_WA = ""  # 네이버 애널리틱스 사이트 ID (발급받으면 넣는다)


def analytics():
    """<head> 맨 앞에 넣는 방문 분석 태그."""
    out = ""
    if GOOGLE_TAG:
        out += f"""<script async src="https://www.googletagmanager.com/gtm.js?id={GOOGLE_TAG}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
"""
    if NAVER_WA:
        out += f"""<script src="//wcs.naver.net/wcslog.js"></script>
<script>if(!wcs_add) var wcs_add = {{}}; wcs_add["wa"] = "{NAVER_WA}"; if(window.wcs) {{ wcs_do(); }}</script>
"""
    return out

TEL, TEL_RAW, MAIL = "010-4751-1668", "01047511668", "irefood@irefood.com"
ADDR = "경기 구리시 갈매순환로166번길 46 금강펜테리움 IX타워 B2 8,9호 (우:11901)"
SNS = {
    "스마트스토어": "https://smartstore.naver.com/sunbong_food",
    "YouTube": "https://www.youtube.com/channel/UCzcJfWSfV6122N1JzlV9mwQ",
    "Instagram": "https://www.instagram.com/sunbong_food/?hl=ko",
}
PRIVACY_NAME = "개인정보처리방침"

PRODUCTS = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))
NOTICES = sorted(json.load(open(os.path.join(ROOT, "data", "notices.json"), encoding="utf-8")), key=lambda n: n["date"], reverse=True)
CAT_ORDER = ["마라탕", "김치 장아찌 절임", "냉동냉장", "수산건어물육류", "쌀계란두부나물떡면", "일회용품포장세제", "장류,소스,기름,분말,통조림", "채소"]


# 검색에서 잡으려는 말. meta keywords · 구조화 데이터 · llms.txt 가 함께 쓴다.
KEYWORDS = [
    "식자재 도매", "식자재 납품", "식자재 납품업체", "업소용 식자재", "식자재 유통", "식자재 매일 배송",
    "마라탕 재료 도매", "마라탕 식자재", "마라탕 소스 도매", "훠궈 재료 도매", "훠궈 식자재",
    "중국식자재 도매", "중국식품 도매", "분모자 도매", "피쉬볼 도매", "중국당면 도매",
    "식당 창업 식자재", "마라탕 창업 재료", "프랜차이즈 식자재 공급", "단체급식 식자재",
    "구리 식자재", "남양주 식자재", "하남 식자재", "서울 식자재 납품", "이레푸드서비스",
]
# 강점 4가지 — 홈·사업소개·llms.txt 가 함께 쓴다. (경쟁사 언급 없이 우리 서비스만 말한다)
STRENGTHS = [
    ("중국식품 전문 구색", "마라탕·훠궈 소스, 분모자, 피쉬볼, 중국당면 등 시중에서 구하기 어려운 중국 식자재를 여러 품목 보유하고 도매로 납품합니다."),
    ("친절하고 빠른 상담", "중국 식자재가 처음이어도 괜찮습니다. 필요한 재료와 규격을 한국어로 쉽고 빠르게 안내해 드립니다."),
    ("식자재 원스톱 공급", "중국식품에 설탕·조미료·밀가루 등 일반 식자재와 육류, 매일 가락시장·구리시장에서 들여오는 채소까지 한 번에 공급합니다."),
    ("월~토 매일 배송", "서울·수도권 전역에 월요일부터 토요일까지 매일 납품합니다."),
]
TARGETS = [
    ("마라탕·훠궈 식당", "운영 중인 매장의 재료 정기 납품"),
    ("신규 오픈 준비 식당", "초도 재료 구성부터 상담"),
    ("한식·분식 등 일반 식당", "업종별 식자재 맞춤 공급"),
]


def esc(s):
    return _html.escape(str(s), quote=True)


def categories():
    """[(분류명, [제품명...])] — products.js 의 분류 순서를 따른다."""
    cats = {}
    for p in PRODUCTS:
        for c in p["categories"]:
            cats.setdefault(c, []).append(p["name"])
    order = [c for c in CAT_ORDER if c in cats] + sorted(c for c in cats if c not in CAT_ORDER)
    return [(c, cats[c]) for c in order]


def org_ld():
    """회사 정보 구조화 데이터 (검색엔진·AI가 읽는 회사 명함)."""
    return {
        "@context": "https://schema.org",
        "@type": "WholesaleStore",
        "@id": SITE + "/#organization",
        "name": "이레푸드서비스 주식회사",
        "alternateName": ["이레푸드서비스", "이레푸드", "IREFOOD SERVICE CORPORATION", "이레유통", "이레글로벌"],
        "url": SITE + "/",
        "logo": SITE + "/assets/images/logo-color.png",
        "image": SITE + "/assets/images/og-image.jpg",
        "description": f"{FOUNDED}년 설립된 요식업용 식자재 전문 유통·공급 회사. 마라탕·훠궈 재료 등 중국식품과 한식·중식·분식·일식·양식 일반 식자재, 채소를 서울·수도권 음식점, 프랜차이즈, 단체급식에 월~토 매일 배송합니다.",
        "foundingDate": "1998-05",
        "telephone": "+82-10-4751-1668",
        "email": MAIL,
        "taxID": "557-81-02236",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "갈매순환로166번길 46 금강펜테리움 IX타워 B2 8,9호",
            "addressLocality": "구리시",
            "addressRegion": "경기도",
            "postalCode": "11901",
            "addressCountry": "KR",
        },
        "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in ("서울특별시", "경기도", "인천광역시")],
        "sameAs": list(SNS.values()),
        "slogan": "모든 식자재 월~토 매일 배송",
        "keywords": ", ".join(KEYWORDS),
        "knowsAbout": ["식자재 유통", "마라탕 재료", "훠궈 재료", "중국식품", "업소용 식자재", "프랜차이즈 식자재 공급", "단체급식 식자재"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "취급 식자재", "itemListElement": [
            {"@type": "OfferCatalog", "name": c, "numberOfItems": len(ns)} for c, ns in categories()]},
    }


def ld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in objs)


def crumbs(*items):
    """BreadcrumbList. items: (이름, 경로)"""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + p} for i, (n, p) in enumerate(items)]}
PHONE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>'

MENU = [
    ("COMPANY", "company.html", [("인사말", "company.html#greeting"), ("연혁", "company.html#history"), ("오시는 길", "company.html#location")]),
    ("BUSINESS", "business.html", []),
    ("PRODUCT", "product.html", []),
    ("CUSTOMER", "customer.html", [("공지사항", "customer.html#notice"), ("1:1 문의", "customer.html#inquiry")]),
]


def head(title, desc, root, path=None, extra=""):
    """path: 사이트 루트 기준 경로 ("" = 홈). None 이면 canonical 을 넣지 않는다 (?id= 로 내용이 바뀌는 상세 페이지)."""
    url = SITE + "/" + path if path is not None else None
    canon = f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n' if url else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
{analytics()}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{", ".join(KEYWORDS)}">
{canon}<meta property="og:site_name" content="이레푸드서비스 주식회사">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="naver-site-verification" content="{NAVER_VERIFY}">
<meta name="google-site-verification" content="{GOOGLE_VERIFY}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" href="{root}assets/images/favicon.png?v=2">
<link rel="stylesheet" href="{root}assets/css/style.css">
<script>window.SITE_ROOT = "{root}";</script>
{extra}</head>
"""


def header(root, active="", solid=False):
    pages = "" if root == "../" else root + "pages/"
    lis = ""
    for name, href, subs in MENU:
        sub = "".join(f'<li><a href="{pages}{h}">{t}</a></li>' for t, h in subs)
        sub = f'<ul class="submenu">{sub}</ul>' if sub else ""
        on = " on" if name == active else ""
        lis += f'<li class="{on.strip()}"><a href="{pages}{href}">{name}</a>{sub}</li>'
    am = ""
    for name, href, subs in MENU:
        if subs:
            am += f'<dl><dt>{name}</dt><dd>' + "".join(f'<a href="{pages}{h}">{t}</a>' for t, h in subs) + "</dd></dl>"
        else:
            am += f'<dl><dt><a href="{pages}{href}">{name}</a></dt></dl>'
    home = root  # "./" 또는 "../" — /index.html 과 / 이 중복 주소로 잡히지 않게 루트로 연결
    return f"""<body>
<header{' class="solid"' if solid else ''}>
  <div class="header-inner">
    <a href="{home}" class="logo" aria-label="이레푸드서비스 주식회사 홈"><img src="{root}assets/images/logo-white.png?v=2" alt="이레푸드서비스 주식회사"></a>
    <div class="header-gnb">
      <ul class="gnb-menu">{lis}</ul>
      <a href="tel:{TEL_RAW}" class="call-btn pcbtn" aria-label="전화 {TEL}">{PHONE_SVG}{TEL}</a>
      <button type="button" class="gnb-btn" aria-label="전체 메뉴 열기"><span></span><span></span><span></span></button>
    </div>
    <div class="submenubg"></div>
  </div>
</header>
<div class="all-menu" aria-label="전체 메뉴">
  <button type="button" class="close-btn" aria-label="메뉴 닫기">&times;</button>
  {am}
  <div class="am-info"><a href="tel:{TEL_RAW}">{TEL}</a><br>{MAIL}<br>{ADDR}</div>
</div>
"""


def footer(root, scripts):
    pages = "" if root == "../" else root + "pages/"
    sns = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SNS.items())
    return f"""<footer>
  <img src="{root}assets/images/logo-white.png?v=2" alt="이레푸드서비스 주식회사" class="foot-logo">
  <ul>
    <li>사업자등록번호 : 557-81-02236</li>
    <li>주소 : {ADDR}</li>
    <li>전화번호 : <a href="tel:{TEL_RAW}">{TEL}</a> · 이메일 : {MAIL}</li>
  </ul>
  <div class="foot-links"><a href="{pages}terms.html">이용약관</a><a href="{pages}privacy.html">{PRIVACY_NAME}</a><a href="{pages}email-policy.html">이메일무단수집거부</a>{sns}</div>
  <p class="foot-txt02">Copyright &copy; {TODAY.year} IREFOOD SERVICE CORPORATION. All rights reserved.</p>
  <a href="#top" class="scroll-top" aria-label="맨 위로">&uarr;</a>
</footer>
<div class="float-call">
  <a href="tel:{TEL_RAW}" aria-label="전화 상담">{PHONE_SVG}<span class="t">전화 상담</span></a>
  <a href="{SNS['스마트스토어']}" target="_blank" rel="noopener" class="store" aria-label="네이버 스마트스토어 (새 창)"><b>N</b><span class="t">스마트스토어</span></a>
</div>
<script src="{root}assets/js/main.js"></script>
{scripts}</body>
</html>
"""


def sub_hero(title, sub, tabs, bg, brand=False):
    """title: 굵은 한글 제목(H1). brand=True 면 H1 앞에 회사명을 검색엔진·스크린리더용으로만 넣는다."""
    t = "".join(f'<a href="{h}">{n}</a>' for n, h in tabs)
    t = f'<nav class="sub-tabs">{t}</nav>' if tabs else ""
    k = '<span class="sr-only">이레푸드서비스 </span>' if brand else ""
    p = f"<p>{sub}</p>" if sub else ""
    return f"""<section class="sub-hero"><div class="bg" style="background-image:url({bg})"></div>
  <h1>{k}{title}</h1>{p}{t}</section>
"""


def sec(title, desc=""):
    """하위 페이지 섹션 제목 (+ 설명)."""
    d = f'<p class="sec-desc">{desc}</p>' if desc else ""
    return f'<h2 class="sec-title{" has-desc" if desc else ""}">{title}</h2>{d}'


def notice_rows(ns, root):
    """notices.js 의 row() 와 같은 마크업. JS 가 없어도(크롤러) 공지가 보이도록 미리 그려 둔다."""
    return "".join(f'<li><a href="{root}pages/notice-detail.html?id={n["id"]}"><div><p class="tx">{esc(n["title"])}</p></div><span class="dt">{n["date"].replace("-", ".")}</span></a></li>' for n in ns)


FAQ_TOP = 4  # 홈에 보여 줄 질문 수 (FAQ 앞에서부터)
FAQ = [
    ("마라탕·훠궈 재료를 도매로 살 수 있나요?",
     f"네. 마라탕 소스, 훠궈 소스, 분모자, 피쉬볼, 중국당면, 건두부, 목이버섯 등 마라탕·훠궈 재료를 여러 품목 보유하고 음식점과 프랜차이즈에 도매로 납품합니다. 전화({TEL})나 1:1 문의로 품목을 알려 주시면 견적을 드립니다."),
    ("식자재는 어느 지역에, 무슨 요일에 배송하나요?",
     "서울과 수도권 전역에 월요일부터 토요일까지 매일 배송합니다. 본사가 경기 구리시에 있어 구리·남양주·하남 등 경기 동북부와 서울 동부권도 매일 납품합니다."),
    ("식당 창업을 준비 중인데 식자재 거래처로 이용할 수 있나요?",
     "네. 오픈에 필요한 초도 물량 구성부터 상담해 드립니다. 중국식품, 일반 식자재(설탕·조미료·밀가루 등), 채소, 육류를 한 곳에서 받을 수 있어 거래처를 여러 곳 둘 필요가 없습니다."),
    ("분모자·피쉬볼·중국당면 같은 품목만 따로 주문할 수 있나요?",
     "네. 필요한 품목만 골라 견적을 받을 수 있고, 소량은 네이버 스마트스토어에서 바로 주문하실 수 있습니다. 마라탕 소스 1kg, 즈마장 2.5kg 같은 업소용 대용량 제품도 취급합니다."),
    ("이레푸드서비스는 어떤 회사인가요?",
     f"1998년 서울 강동구 천호동에서 '이레유통'으로 시작해 {YEARS}년째 식자재를 유통하고 있는 회사입니다. 2014년 '이레글로벌', 2025년 6월 '이레푸드서비스 주식회사'로 사명을 바꿨고, 본사는 경기 구리시 갈매순환로166번길 46 금강펜테리움 IX타워에 있습니다."),
    ("어떤 식자재를 공급하나요?",
     "마라탕·훠궈 재료와 중국식품을 중심으로 소스·장류·기름·분말, 면류·떡·두부, 냉동·냉장식품, 수산·건어물·육류, 채소, 김치·절임류, 일회용품·포장재까지 요식업에 필요한 품목을 함께 공급합니다. "
     f"홈페이지 제품 목록에 등록된 대표 품목만 {len(PRODUCTS)}개이며, 목록에 없는 제품도 문의하시면 확인해 드립니다."),
    ("수도권 밖 지역도 배송되나요?",
     "서울·수도권은 자체 물류망으로 납품합니다. 그 밖의 지역은 전화나 1:1 문의로 가능 여부를 확인해 주세요."),
    ("중국식품과 일반 식자재를 한 곳에서 받을 수 있나요?",
     "가능합니다. 마라탕·훠궈 재료 등 중국식품과 설탕·조미료·밀가루 같은 일반 식자재, 육류, 채소를 함께 납품합니다. 채소는 매일 가락시장·구리시장에서 들여옵니다."),
    ("마라탕·훠궈 식당 창업 재료도 상담할 수 있나요?",
     f"가능합니다. 소스·분모자·피쉬볼·중국당면 등 중국 식자재부터 일반 식자재, 채소, 육류까지 오픈에 필요한 초도 물량 구성을 한국어로 상담해 드립니다. 전화({TEL})나 1:1 문의로 연락해 주세요."),
    ("어떤 거래처와 거래하나요?",
     "한식·중식·분식·일식·양식 일반 음식점, 프랜차이즈 본사·가맹점, 단체급식이 주요 거래처입니다. 훠궈·마라탕 프랜차이즈(2025), 숯불갈비 프랜차이즈(2025), 분식 프랜차이즈(2023), 일식 프랜차이즈(2018)와 식자재 공급 업무협약을 맺었고, 서울 소재 보건소 구내식당(2013)에도 납품했습니다."),
    ("프랜차이즈 전용상품 물류도 가능한가요?",
     "가능합니다. 매장 단위 표준화 공급과 전용상품 물류를 지원하며, 정기 납품 체계로 운영합니다."),
    ("소량으로도 구매할 수 있나요?",
     "소량 구매는 네이버 스마트스토어에서 바로 주문하실 수 있고, 식자재 종합 쇼핑몰 '식봄'에서도 구매하실 수 있습니다. 대량·정기 납품은 견적 문의를 남겨 주세요."),
    ("견적은 어떻게 받나요?",
     f"제품 목록에서 원하는 품목을 '견적 담기'로 고른 뒤 1:1 문의를 보내시거나, 전화({TEL})로 문의하시면 됩니다. 견적 상담은 무료입니다."),
]


def faq_html(items=None):
    items = FAQ if items is None else items
    rows = "".join(f'<details class="faq-item"><summary><h3>{esc(q)}</h3></summary><p>{esc(a)}</p></details>' for q, a in items)
    return f'<div class="faq">{rows}</div>'


def faq_ld(items=None):
    items = FAQ if items is None else items
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def write(rel, html):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)


def js(root, *names):
    return "".join(f'<script src="{root}assets/js/{n}.js"></script>\n' for n in names)


# ---------------------------------------------------------------- HOME
def home():
    # 첫 장은 대표 문구, 이어서 원래 문구 3장
    slides = [
        ("sourcing", "LOGISTICS", "Delivered with Care", "수도권 전역을 잇는 물류망", "안정적인 납품을 약속합니다."),
        ("quality", "QUALITY", "Quality You Can Trust", "검수부터 콜드체인까지", "품질을 끝까지 책임집니다."),
        ("partners", "PARTNERS", "Partner of Every Kitchen", "모든 주방의 든든한 파트너", "음식점·프랜차이즈·단체급식에 식자재를 공급합니다."),
    ]
    sl = """
      <li class="slide active">
        <div class="bg"><span style="background-image:url(assets/images/hero/coldchain.webp)"></span></div>
        <div class="slide-txt main"><h1><span class="sr-only">모든 식자재 월~토 매일 배송</span><span class="split gold" aria-hidden="true" data-split>모든 식자재</span><span class="split" aria-hidden="true" data-split>월~토 매일 배송</span></h1><p>서울·수도권 음식점·프랜차이즈·단체급식 식자재 납품</p></div>
      </li>"""
    for img, tag, en, h, d in slides:
        sl += f"""
      <li class="slide">
        <div class="bg"><span style="background-image:url(assets/images/hero/{img}.webp)"></span></div>
        <div class="slide-txt"><span class="tag">{tag}<i>{en}</i></span><h2>{h}</h2><p>{d}</p></div>
      </li>"""
    n = {c: len(ns) for c, ns in categories()}
    biz = [
        ("coldchain", "공산품 · 중국식품", f"마라탕·훠궈 재료 여러 품목, 장류·소스·기름·분말 {n['장류,소스,기름,분말,통조림']}개 품목"),
        ("sourcing", "신선식품 · 수산물", "매일 가락시장·구리시장에서 들여오는 채소, 수산·건어물"),
        ("quality", "육류 · 냉동식품", f"냉동·냉장식품 {n['냉동냉장']}개, 수산·건어물·육류 {n['수산건어물육류']}개 품목"),
        ("partners", "프랜차이즈 · 단체급식", "매장 단위 표준화 공급, 전용상품 물류, 정기 납품"),
    ]
    bz = "".join(f'<a href="pages/business.html" class="biz-card"><div class="bg" style="background-image:url(assets/images/hero/{i}.webp)"></div><h3>{t}</h3><p>{d}</p></a>' for i, t, d in biz)
    # 강점 줄마다 사진 한 장 (assets/images/why/). 실제 촬영본이 생기면 같은 파일 이름으로 바꿔 넣는다.
    why_img = [("chinese", "분모자, 중국당면, 피쉬볼, 건두부 등 마라탕·훠궈 재료"), ("consult", "식자재 견적 상담 책상"),
               ("onestop", "채소 상자와 밀가루, 식용유, 육류를 한데 모은 식자재"), ("delivery", "식당 뒷문에 도착한 식자재 배송 상자")]
    why = "".join(f'<li{" class=on" if i == 0 else ""}><h3>{t}</h3><p>{d}</p><img src="assets/images/why/{im}.jpg" alt="{alt}" width="960" height="1200" loading="lazy"></li>'
                  for i, ((t, d), (im, alt)) in enumerate(zip(STRENGTHS, why_img)))
    why_ph = "".join(f'<img src="assets/images/why/{im}.jpg" alt="" width="960" height="1200" loading="lazy"{" class=on" if i == 0 else ""}>' for i, (im, alt) in enumerate(why_img))
    tg = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in TARGETS)
    asks = [
        ("마라탕·훠궈 재료", "소스·분모자·피쉬볼·중국당면 등 중국 식자재 견적"),
        ("창업 식자재", "오픈 준비 매장의 초도 재료 구성 상담"),
        ("정기 납품", "음식점·프랜차이즈·단체급식 대량·정기 납품 견적"),
    ]
    ak = "".join(f'<a href="pages/customer.html#inquiry" class="ask-card"><h3>{t}</h3><p>{d}</p><span>상담하기<i aria-hidden="true">&rarr;</i></span></a>' for t, d in asks)
    body = f"""
<main id="top">
<section class="sec01">
  <ul class="slides">{sl}
  </ul>
  <div class="hero-fixed">
    <div class="hero-cta"><a class="primary" href="tel:{TEL_RAW}">{PHONE_SVG}{TEL}</a><a class="txt" href="pages/customer.html#inquiry">무료 견적 문의<i aria-hidden="true">&rarr;</i></a></div>
    <div class="hero-group"><strong>이레푸드서비스(주)</strong><span class="lbl"><span>자회사</span></span><ul><li>이레글로벌</li><li>(주)강한글로벌</li><li>(주)창신주류</li></ul></div>
  </div>
  <div class="navi-bar">
    <div><div class="progress"><span class="num"></span><span class="bar"><span class="fill"></span></span></div>
      <button type="button" class="pp" aria-label="슬라이드 멈춤"><i></i><i></i></button></div>
    <div><button type="button" class="arrow prev" aria-label="이전">&larr;</button><button type="button" class="arrow next" aria-label="다음">&rarr;</button></div>
  </div>
</section>

<section class="sec-why">
  <div class="why-inner">
    <div class="why-head"><h2 class="hd-title">이레푸드서비스 강점</h2>
      <p>중국식품부터 채소까지,<br>거래처 하나로 매일 받으세요.</p></div>
    <div class="why-body">
      <ul class="why-rows" data-peek>{why}</ul>
      <div class="why-photo" aria-hidden="true">{why_ph}</div>
    </div>
    <div class="why-for"><strong>주요 거래처</strong><ul>{tg}</ul></div>
  </div>
</section>

<section class="sec02">
  <div class="sec02-inner">
    <div class="sec02-div01">
      <div>
        <h2>마라탕·훠궈 재료부터 <br class="pc">한식·중식·분식·일식·양식까지, <br class="pc">요식업을 위한 <br class="mo">식자재 전문 공급</h2>
        <div class="stats">
          <div><strong>{YEARS}</strong><span>년 업력</span></div>
          <div><strong>{len(PRODUCTS)}+</strong><span>대표 취급 품목</span></div>
        </div>
      </div>
      <a href="pages/product.html" class="more-btn">제품 전체 보기</a>
    </div>
    <div class="sec02-div02"><div class="scrolling" data-rolling></div></div>
  </div>
</section>

<section class="sec-biz on-dark">
  <div class="biz-head"><h2 class="hd-title">사업 영역</h2>
    <p>공산품·중국식품부터 신선식품, 육류, 프랜차이즈 납품까지 한 회사가 맡습니다.</p></div>
  <div class="biz-grid">{bz}</div>
</section>

<section class="sec03">
  <div class="sec03-inner">
    <div class="sec03-title"><h2 class="hd-title">공지사항</h2><a href="pages/customer.html#notice" class="more-btn">전체 보기</a></div>
    <ul class="list-rows" data-notice-preview>{notice_rows(NOTICES[:4], "./")}</ul>
  </div>
</section>

<section class="sec-faq">
  <div class="faq-inner">
    <h2 class="hd-title">자주 묻는 질문</h2>
    {faq_html(FAQ[:FAQ_TOP])}
    <a href="pages/business.html#faq" class="more-btn faq-more">질문 전체 보기</a>
  </div>
</section>

<section class="sec-ask">
  <div class="ask-inner">
    <div class="ask-head"><h2 class="hd-title">무료 견적 상담</h2>
      <p>소량 구매는 스마트스토어에서 바로 주문하실 수 있습니다.</p></div>
    <div class="ask-grid">{ak}</div>
    <div class="ask-tel"><div><small>전화 상담</small><a class="num" href="tel:{TEL_RAW}">{PHONE_SVG}{TEL}</a></div>
      <a href="{SNS['스마트스토어']}" target="_blank" rel="noopener" class="pill line">스마트스토어 (소량 구매)</a></div>
  </div>
</section>
</main>
"""
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
               "name": "이레푸드서비스 주식회사", "inLanguage": "ko-KR", "publisher": {"@id": SITE + "/#organization"}}
    extra = '<link rel="preload" as="image" href="assets/images/hero/coldchain.webp" fetchpriority="high">\n' + ld(org_ld(), website, faq_ld(FAQ[:FAQ_TOP]))
    return (head("식자재 도매·납품 이레푸드서비스 | 마라탕·훠궈 재료, 월~토 매일 배송",
                 "식자재 도매·납품 전문 이레푸드서비스. 마라탕·훠궈 재료 등 중국식품과 일반 식자재, 채소, 육류를 서울·수도권 음식점·프랜차이즈·단체급식에 월~토 매일 배송합니다. 1998년 설립, 무료 견적 상담.", "./", "", extra)
            + header("./") + body + footer("./", js("./", "products", "notices")))


# ---------------------------------------------------------------- SUB PAGES
R = "../"
HIST = [
    ("2025", [("10월", "훠궈·마라탕 프랜차이즈 중국식품·신선식품 공급 업무협약"), ("6월", "숯불갈비 프랜차이즈 식자재 공급 업무협약"), ("6월", "'이레푸드서비스 주식회사'로 사명 변경 및 물류창고 확장 이전")]),
    ("2023", [("11월", "분식 프랜차이즈 식자재 공급 업무협약"), ("11월", "식자재 종합 쇼핑몰 '식봄' 입점"), ("11월", "중국 허베이성 소재 중국당면·분모자 생산 공장 국제무역부 담당자 미팅 및 중국 식품 직수입 협의"), ("6월", "유튜브·인스타그램 개설"), ("5월", "네이버 스마트스토어 입점"), ("1월", "한 식품 유통사와 중국식품·주류 수입 업무협약")]),
    ("2022", [("3월", "서울 강남구 대형 한식 식당 식자재 공급 업무협약")]),
    ("2021", [("8월", "자회사 (주)강한글로벌 설립 (충청·전라권 식자재 및 주류 공급)")]),
    ("2020", [("3월", "통신판매업 신고")]),
    ("2018", [("6월", "일식 프랜차이즈 식자재 공급 및 전용상품 물류 공급 업무협약")]),
    ("2017", [("7월", "물류창고 이전 (경기도 하남시)")]),
    ("2014", [("5월", "'이레글로벌'로 사명 변경")]),
    ("2013", [("8월", "서울 소재 보건소 구내식당 납품 협약")]),
    ("2009", [("2월", "종합식자재 도소매로 업무 확장")]),
    ("1998", [("5월", "이레유통 설립 (서울시 강동구 천호동)")]),
]


def company():
    tl = "".join(f'<div class="tl-year"><h3>{y}</h3><ul>' + "".join(f"<li><b>{m}</b> {t}</li>" for m, t in it) + "</ul></div>" for y, it in HIST)
    body = sub_hero("회사소개", "1998년부터 이어온 신뢰, 이레푸드서비스", [("인사말", "#greeting"), ("연혁", "#history"), ("오시는 길", "#location")], R + "assets/images/hero/sourcing.webp", True) + f"""
<main id="top">
<section class="wrap-in" id="greeting">
  {sec("인사말")}
  <div class="greeting">
    <div class="poster"><img src="{R}assets/images/poster-malatang.jpg" alt="이레푸드서비스 마라탕 식자재 유통 포스터" loading="lazy"></div>
    <div>
      <p class="lead">산지에서 셰프의 주방까지,<br>품질과 신선도를 지키는 절제된 신뢰.</p>
      <p>1998년 서울 강동구 천호동에서 이레유통으로 시작한 이레푸드서비스 주식회사는 {YEARS}년간 신뢰를 최우선 가치로 삼아 식자재 유통업의 길을 걸어왔습니다.</p>
      <p>중국식품, 마라탕·훠궈 식자재를 비롯해 한식·중식·분식·일식·양식까지 폭넓은 품목을 취급하며, 일반 음식점부터 대형 프랜차이즈, 단체급식까지 다양한 고객군에 안정적인 공급망을 제공하고 있습니다.</p>
      <p>다음 30년도 변함없는 신뢰로 준비하겠습니다.</p>
    </div>
  </div>
</section>
<section class="bg-beige" id="history"><div class="wrap-in">
  {sec("연혁")}
  <div class="timeline">{tl}</div>
</div></section>
<section class="wrap-in" id="location">
  {sec("오시는 길")}
  <figure class="bldg"><img src="{R}assets/images/building.jpg" alt="이레푸드서비스 주식회사 본사 사옥, 금강펜테리움 IX타워" loading="lazy"></figure>
  <div class="loc">
    <div id="map" role="img" aria-label="이레푸드서비스 주식회사 위치 지도">지도를 불러오는 중…</div>
    <dl>
      <dt>ADDRESS</dt><dd>{ADDR}</dd>
      <dt>TEL</dt><dd><a href="tel:{TEL_RAW}">{TEL}</a></dd>
      <dt>E-MAIL</dt><dd>{MAIL}</dd>
      <dt>TRANSPORT</dt><dd>경춘선·8호선 갈매역 인근</dd>
      <dt>PARKING</dt><dd>건물 내 방문객 주차 가능 (사전 연락 권장)</dd>
      <a class="pill" href="https://map.kakao.com/?q={ADDR.split(' (')[0].replace(' ', '%20')}" target="_blank" rel="noopener">카카오맵에서 길찾기</a>
    </dl>
  </div>
</section>
</main>
"""
    return (head("회사소개 | 구리 식자재 유통 이레푸드서비스", "1998년 이레유통으로 시작한 이레푸드서비스 주식회사의 인사말과 연혁, 오시는 길(경기 구리시 갈매동 금강펜테리움 IX타워).", R, "pages/company.html",
                 ld(org_ld(), crumbs(("홈", ""), ("회사소개", "pages/company.html"))))
            + header(R, "COMPANY", True) + body + footer(R, js(R, "map")))


def business():
    cats = categories()
    st = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in STRENGTHS)
    cat_rows = "".join(f'<li><b>{esc(c)}</b><span>{len(ns)}개 품목</span></li>' for c, ns in cats)
    body = sub_hero("사업소개", "산지-물류-주방을 하나로 잇는 유통망", [], R + "assets/images/hero/quality.webp", True) + f"""
<main id="top">
<section class="wrap-in">
  <p class="biz-intro">이레푸드서비스 주식회사는 공산품부터 신선식품, 수산물, 육류까지 폭넓은 카테고리를 취급하며, 산지–물류–주방을 하나로 잇는 유통망을 갖추고 있습니다.</p>
  <div class="flow">
    <div><h3>공산품 / 중국식품</h3><p>마라탕·훠궈 재료, 소스, 면류</p></div>
    <div><h3>신선식품 / 수산물</h3><p>콜드체인 신선 배송</p></div>
    <div><h3>육류 / 냉동식품</h3><p>검수된 원재료 공급</p></div>
    <div><h3>프랜차이즈 / 단체급식</h3><p>표준화·정기 납품</p></div>
  </div>
</section>
<section class="bg-beige"><div class="wrap-in">
  {sec("주요 거래처 유형")}
  <div class="three">
    <div><h3>일반 음식점</h3><p>한식·중식·분식·일식·양식 등 업종을 가리지 않는 맞춤 공급</p></div>
    <div><h3>프랜차이즈</h3><p>매장 단위 표준화 공급 및 전용상품 물류 지원</p></div>
    <div><h3>단체급식</h3><p>대량 수요에 대응하는 안정적인 정기 납품 체계</p></div>
  </div>
</div></section>
<section class="wrap-in">
  {sec("이레푸드서비스 강점")}
  <div class="strength">{st}</div>
  <div class="more-row"><a class="pill" style="background:#111;color:#fff" href="customer.html#inquiry">무료 견적 문의</a></div>
</section>
<section class="bg-beige" id="items"><div class="wrap-in">
  {sec("대표 취급 품목", f"분류별 총 {len(PRODUCTS)}개 (홈페이지 등록 기준)")}
  <ul class="cat-count">{cat_rows}</ul>
  <div class="more-row"><a class="pill line" style="color:#111;border-color:#111" href="product.html">전체 제품 보기</a></div>
</div></section>
<section class="wrap-in" id="faq">
  {sec("자주 묻는 질문")}
  {faq_html()}
</section>
</main>
"""
    return (head("식자재 납품·프랜차이즈 공급 사업소개 | 이레푸드서비스", f"마라탕·훠궈 재료, 중국식품, 신선식품, 수산물, 육류를 서울·수도권 음식점·프랜차이즈·단체급식에 월~토 매일 배송하는 이레푸드서비스의 사업소개, 대표 취급 품목 {len(PRODUCTS)}개, 자주 묻는 질문.", R, "pages/business.html",
                 ld(org_ld(), faq_ld(FAQ[FAQ_TOP:]), crumbs(("홈", ""), ("사업소개", "pages/business.html"))))
            + header(R, "BUSINESS", True) + body + footer(R, ""))


def product():
    by_cat = {}
    for x in PRODUCTS:
        for c in x["categories"]:
            by_cat.setdefault(c, []).append(x)
    groups = "".join(f'<h3>{esc(c)} <small>({len(ns)})</small></h3><p>' + " · ".join(f'<a href="products/{x["id"]}.html">{esc(x["name"])}</a>' for x in by_cat[c]) + "</p>" for c, ns in categories())
    body = sub_hero("취급 제품", "마라탕·훠궈 재료를 비롯한 식자재 제품 목록", [], R + "assets/images/hero/coldchain.webp", True) + """
<main id="top"><section class="wrap-in">
  <p class="prod-note">아래는 대표 제품 일부이며, 이 밖에도 훨씬 더 많은 품목을 취급하고 있습니다. 찾으시는 제품이 없다면 <a href="customer.html#inquiry">문의</a> 또는 <a href="tel:__TELRAW__">전화(__TEL__)</a>로 알려주세요.</p>
  <input type="search" class="search" data-product-search placeholder="제품명 검색 (예: 당면, 마라)" aria-label="제품명 검색">
  <div class="filter" data-product-filter></div>
  <div class="pgrid" data-product-grid></div>
  <div class="more-row"><button type="button" class="pill line" style="color:#111;border-color:#111" data-more>더보기</button></div>
  <details class="all-items"><summary>분류별 전체 품목명 한눈에 보기 (__N__개)</summary>__GROUPS__</details>
</section></main>
"""
    body = body.replace("__TELRAW__", TEL_RAW).replace("__TEL__", TEL).replace("__N__", str(len(PRODUCTS))).replace("__GROUPS__", groups)
    return (head("마라탕·훠궈 재료, 업소용 식자재 제품 목록 | 이레푸드서비스", f"이레푸드서비스 주식회사 취급 제품 목록 {len(PRODUCTS)}개: 마라탕·훠궈 재료, 소스·장류, 면류, 냉동·냉장식품, 수산·육류, 채소, 일회용품.", R, "pages/product.html",
                 ld(crumbs(("홈", ""), ("취급 제품", "pages/product.html"))))
            + header(R, "PRODUCT", True) + body + footer(R, js(R, "products")))


def product_detail():
    """예전 주소(product-detail.html?id=N). products.js 가 pages/products/N.html 로 넘긴다."""
    body = sub_hero("제품 상세", "", [("← 제품 목록", "product.html")], R + "assets/images/hero/coldchain.webp") + '<main id="top"><section class="wrap-in"><div class="detail" data-product-detail>불러오는 중…</div></section></main>\n'
    return head("제품 상세 | 이레푸드서비스", "이레푸드서비스 취급 제품 상세", R, None, '<meta name="robots" content="noindex,follow">\n') + header(R, "PRODUCT", True) + body + footer(R, js(R, "products"))


RR = "../../"  # pages/products/ 에서 본 사이트 루트


def product_page(x, related):
    """제품 한 개의 고정 주소 페이지. 검색에 품목 이름으로 잡히도록 내용을 HTML 로 미리 그려 둔다."""
    name, cat = x["name"], x["categories"][0]
    path = f"pages/products/{x['id']}.html"
    img = f'<img src="{RR}{x["image"]}" alt="{esc(name)}">' if x.get("image") else "<span>이미지 준비 중</span>"
    rel = "".join(f'<a href="{r["id"]}.html" class="rel-card">' + (f'<img src="{RR}{r["image"]}" alt="" loading="lazy">' if r.get("image") else "<span></span>") + f"<p>{esc(r['name'])}</p></a>" for r in related)
    body = sub_hero("취급 제품", "", [("← 제품 목록", "../product.html")], RR + "assets/images/hero/coldchain.webp") + f"""
<main id="top"><section class="wrap-in">
  <div class="detail" data-static-product data-id="{x['id']}" data-name="{esc(name)}">
    <div class="im">{img}</div>
    <div><h1>{esc(name)}</h1>
      <div class="info-row"><strong>보관방법</strong><span>{esc(x.get('storage') or '-')}</span></div>
      <div class="info-row"><strong>원산지</strong><span>{esc(x.get('origin') or '-')}</span></div>
      <div class="info-row"><strong>카테고리</strong><span>{esc(' · '.join(x['categories']))}</span></div>
      <p class="detail-note">이레푸드서비스가 음식점·프랜차이즈·단체급식에 도매로 납품하는 품목입니다. 서울·수도권에 월~토 매일 배송하며, 견적 상담은 무료입니다.</p>
      <div class="btns"><button type="button" class="pill" data-add>+ 견적 담기</button><a class="pill line" href="tel:{TEL_RAW}">전화 {TEL}</a><a class="pill line" href="../customer.html#inquiry">견적 문의</a></div>
    </div>
  </div>
  <h2 class="rel-title">{esc(cat)} 분류의 다른 제품</h2>
  <div class="rel-grid">{rel}</div>
</section></main>
"""
    prod = {"@context": "https://schema.org", "@type": "Product", "name": name, "category": cat, "url": SITE + "/" + path,
            "description": f"{name} 업소용 도매 납품. 서울·수도권 월~토 매일 배송.",
            "brand": {"@type": "Organization", "@id": SITE + "/#organization", "name": "이레푸드서비스 주식회사"}}
    if x.get("image"):
        prod["image"] = SITE + "/" + x["image"]
    return (head(f"{name} 도매·업소 납품 | 이레푸드서비스", f"{name} 업소용 도매 납품. 서울·수도권 음식점·프랜차이즈·단체급식에 월~토 매일 배송, 무료 견적 {TEL}.", RR, path,
                 ld(prod, crumbs(("홈", ""), ("취급 제품", "pages/product.html"), (name, path))))
            + header(RR, "PRODUCT", True) + body + footer(RR, js(RR, "products")))


def product_pages():
    """모든 제품 페이지를 쓰고, 목록에서 빠진 제품의 예전 페이지는 지운다. 사이트맵에 넣을 경로를 돌려준다."""
    by_cat = {}
    for x in PRODUCTS:
        by_cat.setdefault(x["categories"][0], []).append(x)
    paths = []
    for x in PRODUCTS:
        sib = by_cat[x["categories"][0]]
        i = sib.index(x)
        related = [sib[(i + k) % len(sib)] for k in range(1, min(8, len(sib) - 1) + 1)]
        path = f"pages/products/{x['id']}.html"
        write(path, product_page(x, related))
        paths.append(path)
    folder = os.path.join(ROOT, "pages", "products")
    keep = {f"{x['id']}.html" for x in PRODUCTS}
    for f in os.listdir(folder):
        if re.fullmatch(r"\d+\.html", f) and f not in keep:
            os.remove(os.path.join(folder, f))
    return paths


def customer():
    body = sub_hero("공지사항·문의", "대량·정기 납품 무료 견적 상담", [("공지사항", "#notice"), ("1:1 문의", "#inquiry")], R + "assets/images/hero/partners.webp", True) + f"""
<main id="top">
<section class="wrap-in" id="notice">
  {sec("공지사항")}
  <ul class="list-rows" data-notice-list>{notice_rows(NOTICES, R)}</ul>
</section>
<section class="bg-beige" id="inquiry"><div class="wrap-in">
  {sec("1:1 문의", f'대량·정기 납품 상담은 문의를 남겨주세요. 급하시면 <a href="tel:{TEL_RAW}" style="text-decoration:underline">{TEL}</a> 로 전화 주세요.')}
  <div class="quote-box" data-quote-box hidden><h4>견적 요청 제품</h4><ul></ul></div>
  <form class="form" data-contact-form action="https://formspree.io/f/xzezqbll" method="POST">
    <input type="text" name="_gotcha" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fg"><label for="name">이름</label><input type="text" id="name" name="name" required></div>
    <div class="fg"><label for="phone">연락처</label><input type="tel" id="phone" name="phone" required></div>
    <div class="fg"><label for="email">이메일</label><input type="email" id="email" name="email" required></div>
    <div class="fg"><label for="message">문의내용</label><textarea id="message" name="message" required></textarea></div>
    <div class="fg ck"><input type="checkbox" id="consent" name="consent" required><label for="consent" style="margin:0;font-weight:400">개인정보 수집·이용에 동의합니다. (<a href="privacy.html" style="text-decoration:underline">{PRIVACY_NAME} 보기</a>) — 수집 항목: 이름, 연락처, 이메일, 문의내용 / 목적: 문의 응대 / 보유기간: 문의 처리 완료 후 지체 없이 파기(관계 법령상 보관 의무가 있는 경우 그 기간) / 문의 내용은 폼 전송 서비스 Formspree(미국)를 거쳐 담당자 이메일로 전달됩니다.</label></div>
    <button type="submit">문의 보내기</button>
    <p class="form-status" data-form-status role="status"></p>
  </form>
</div></section>
</main>
"""
    return head("식자재 납품 무료 견적 문의 | 이레푸드서비스", "식자재 대량·정기 납품, 마라탕·훠궈 재료 도매, 프랜차이즈 식자재 공급 무료 견적 문의와 이레푸드서비스 공지사항.", R, "pages/customer.html",
                ld(crumbs(("홈", ""), ("공지사항·문의", "pages/customer.html")))) + header(R, "CUSTOMER", True) + body + footer(R, js(R, "notices", "contact", "products"))


def notice_detail():
    body = sub_hero("공지사항", "", [("← 공지 목록", "customer.html#notice")], R + "assets/images/hero/partners.webp") + '<main id="top"><section class="wrap-in"><div data-notice-detail>불러오는 중…</div><a class="back more-btn" href="customer.html#notice" style="width:auto;padding:0 28px">목록으로</a></section></main>\n'
    return head("공지사항 | 이레푸드서비스 주식회사", "이레푸드서비스 공지사항", R, None) + header(R, "CUSTOMER", True) + body + footer(R, js(R, "notices"))


def legal(slug, title):
    """약관 본문: legal/{slug}.html 이 있으면 그것을, 없으면 기존 사이트(OLD) 본문을 재사용한다."""
    own = os.path.join(ROOT, "legal", f"{slug}.html")
    if os.path.exists(own):
        inner = open(own, encoding="utf-8").read()
    else:
        src = open(os.path.join(OLD, f"{slug}.html"), encoding="utf-8").read()
        m = re.search(r'<h1>.*?</h1>(.*?)</div>\s*</section>', src, re.S)
        inner = m.group(1) if m else ""
        inner = re.sub(r'<p[^>]*>※[^<]*</p>', '', inner)
        inner = re.sub(r'\sstyle="[^"]*"', '', inner)
    body = sub_hero(title, "", [], R + "assets/images/hero/sourcing.webp") + f'<main id="top"><section class="wrap-in"><div class="doc">{inner}</div></section></main>\n'
    return head(f"{title} | 이레푸드서비스 주식회사", f"이레푸드서비스 주식회사 {title}", R, f"pages/{slug}.html") + header(R, "", True) + body + footer(R, "")


SITEMAP = [("", "1.0"), ("pages/company.html", "0.8"), ("pages/business.html", "0.9"), ("pages/product.html", "0.9"),
           ("pages/customer.html", "0.7"), ("pages/terms.html", "0.2"), ("pages/privacy.html", "0.2"), ("pages/email-policy.html", "0.2")]


def sitemap(extra=()):
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{pr}</priority></url>\n" for p, pr in list(SITEMAP) + [(e, "0.5") for e in extra])
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"


def llms():
    """AI 검색엔진용 요약 안내문 (llms.txt)."""
    cats = "\n".join(f"- {c}: {len(ns)}개 (예: {', '.join(ns[:4])})" for c, ns in categories())
    faq = "\n\n".join(f"### {q}\n{a}" for q, a in FAQ)
    hist = "\n".join(f"- {y}년 {m} {t}" for y, it in HIST for m, t in it)
    strengths = "\n".join(f"- {t}: {d}" for t, d in STRENGTHS)
    targets = "\n".join(f"- {t}: {d}" for t, d in TARGETS)
    kw = "\n".join(f"- {k}" for k in KEYWORDS if k != "이레푸드서비스")
    return f"""# 이레푸드서비스 주식회사 (IREFOOD SERVICE CORPORATION)

> {FOUNDED}년 설립된 요식업용 식자재 전문 유통·공급 회사. 마라탕·훠궈 재료 등 중국식품과 한식·중식·분식·일식·양식 일반 식자재, 채소를 서울·수도권의 일반 음식점, 프랜차이즈, 단체급식에 월~토 매일 배송합니다.

## 강점
{strengths}

## 주요 거래처
{targets}

## 이런 것을 찾는 분께 맞습니다
{kw}

## 기본 정보
- 회사명: 이레푸드서비스 주식회사 (구 이레유통 → 이레글로벌 → 2025년 6월 현 사명)
- 설립: 1998년 5월, 서울 강동구 천호동 (업력 {YEARS}년)
- 본사: {ADDR}
- 사업자등록번호: 557-81-02236
- 전화: {TEL} / 이메일: {MAIL}
- 공급 지역: 서울·수도권 (월~토 매일 배송)
- 거래처 유형: 일반 음식점, 프랜차이즈, 단체급식
- 온라인 주문(소량): 네이버 스마트스토어 {SNS['스마트스토어']}, 식자재 쇼핑몰 '식봄'

## 주요 페이지
- [회사소개·연혁·오시는 길]({SITE}/pages/company.html)
- [사업소개·자주 묻는 질문]({SITE}/pages/business.html)
- [취급 제품 목록]({SITE}/pages/product.html)
- [공지사항·견적 문의]({SITE}/pages/customer.html)

## 분류별 대표 취급 품목 (총 {len(PRODUCTS)}개, 홈페이지 등록 기준)
{cats}

## 연혁
{hist}

## 자주 묻는 질문
{faq}
"""


if __name__ == "__main__":
    write("index.html", home())
    write("pages/company.html", company())
    write("pages/business.html", business())
    write("pages/product.html", product())
    write("pages/product-detail.html", product_detail())
    write("pages/customer.html", customer())
    write("pages/notice-detail.html", notice_detail())
    # 약관 3종 본문은 legal/*.html 에서 고친다.
    write("pages/terms.html", legal("terms", "이용약관"))
    write("pages/privacy.html", legal("privacy", PRIVACY_NAME))
    write("pages/email-policy.html", legal("email-policy", "이메일무단수집거부"))
    write("sitemap.xml", sitemap(product_pages()))
    write("robots.txt", robots())
    write("llms.txt", llms())
    print("built")
