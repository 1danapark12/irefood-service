#!/usr/bin/env python3
"""공통 헤더/푸터를 모든 페이지에 일관되게 넣어 HTML을 생성한다. 실행: python3 build.py"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(os.path.dirname(ROOT), "irefood", "pages")  # 기존 사이트 약관 본문 재사용

TEL, TEL_RAW, MAIL = "010-4751-1668", "01047511668", "irefood@irefood.com"
ADDR = "경기 구리시 갈매순환로166번길 46 금강펜테리움 IX타워 B2 8,9호 (우:11901)"
SNS = {
    "스마트스토어": "https://smartstore.naver.com/sunbong_food",
    "YouTube": "https://www.youtube.com/channel/UCzcJfWSfV6122N1JzlV9mwQ",
    "Instagram": "https://www.instagram.com/sunbong_food/?hl=ko",
}
PHONE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>'

MENU = [
    ("COMPANY", "company.html", [("인사말", "company.html#greeting"), ("연혁", "company.html#history"), ("오시는 길", "company.html#location")]),
    ("BUSINESS", "business.html", []),
    ("PRODUCT", "product.html", []),
    ("CUSTOMER", "customer.html", [("공지사항", "customer.html#notice"), ("1:1 문의", "customer.html#inquiry")]),
]


def head(title, desc, root, extra=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="식자재유통, 식자재공급, 마라탕 식자재, 훠궈 식자재, 중국식품 유통, 이레푸드서비스">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{root}assets/images/building.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" href="{root}assets/images/favicon.png?v=2">
<link rel="stylesheet" href="{root}assets/css/style.css">
<script>window.SITE_ROOT = "{root}";</script>
{extra}</head>
"""


def header(root, active="", solid=False):
    pages = root + "pages/" if root == "./" else ""
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
    home = root + "index.html"
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
    pages = root + "pages/" if root == "./" else ""
    sns = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SNS.items())
    return f"""<footer>
  <img src="{root}assets/images/logo-white.png?v=2" alt="이레푸드서비스 주식회사" class="foot-logo">
  <ul>
    <li>사업자등록번호 : 557-81-02236</li>
    <li>주소 : {ADDR}</li>
    <li>전화번호 : <a href="tel:{TEL_RAW}">{TEL}</a> · 이메일 : {MAIL}</li>
  </ul>
  <div class="foot-links"><a href="{pages}terms.html">이용약관</a><a href="{pages}privacy.html">개인정보취급방침</a><a href="{pages}email-policy.html">이메일무단수집거부</a>{sns}</div>
  <p class="foot-txt02">Copyright &copy; 2026 IREFOOD SERVICE CORPORATION. All rights reserved.</p>
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


def sub_hero(title, sub, tabs, bg):
    t = "".join(f'<a href="{h}"{" class=on" if i == 0 and False else ""}>{n}</a>' for i, (n, h) in enumerate(tabs))
    t = f'<nav class="sub-tabs">{t}</nav>' if tabs else ""
    return f"""<section class="sub-hero"><div class="bg" style="background-image:url({bg})"></div>
  <h1>{title}</h1><p>{sub}</p>{t}</section>
"""


def write(rel, html):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)


def js(root, *names):
    return "".join(f'<script src="{root}assets/js/{n}.js"></script>\n' for n in names)


# ---------------------------------------------------------------- HOME
def home():
    slides = [
        ("coldchain", "SOURCING", "Fresh from the Source,", "산지에서 고른 신선한 식자재를 셰프의 주방까지 전해드립니다."),
        ("sourcing", "LOGISTICS", "Delivered with Care,", "수도권 전역을 잇는 물류망으로 안정적인 납품을 약속합니다."),
        ("quality", "QUALITY", "Quality You Can Trust.", "검수부터 콜드체인까지, 품질을 끝까지 책임집니다."),
        ("partners", "PARTNERS", "Partner of Every Kitchen.", "음식점·프랜차이즈·단체급식, 모든 주방의 든든한 파트너입니다."),
    ]
    sl = ""
    for i, (img, tag, h, p) in enumerate(slides):
        sl += f"""
      <li class="slide{' active' if i == 0 else ''}">
        <div class="bg"><span style="background-image:url(assets/images/hero/{img}.jpg)"></span></div>
        <img class="slide-logo" src="assets/images/logo-white.png?v=2" alt="" aria-hidden="true">
        <div class="slide-txt"><span class="tag">{tag}</span><h2>{h}</h2><p>{p}</p></div>
      </li>"""
    biz = [
        ("coldchain", "01 · SOURCING", "공산품 · 중국식품", "마라탕·훠궈 재료부터 소스·면류까지 폭넓은 품목을 취급합니다."),
        ("sourcing", "02 · LOGISTICS", "신선식품 · 수산물", "정교한 콜드체인으로 신선도를 지켜 배송합니다."),
        ("quality", "03 · QUALITY", "육류 · 냉동식품", "엄격한 검수를 거친 육류와 냉동식품을 공급합니다."),
        ("partners", "04 · PARTNERS", "프랜차이즈 · 단체급식", "전국 매장 표준화 공급과 정기 납품 체계를 갖췄습니다."),
    ]
    bz = "".join(f'<a href="pages/business.html" class="biz-card"><div class="bg" style="background-image:url(assets/images/hero/{i}.jpg)"></div><small>{s}</small><h3>{t}</h3><p>{d}</p></a>' for i, s, t, d in biz)
    body = f"""
<main id="top">
<section class="sec01">
  <ul class="slides">{sl}
  </ul>
  <div class="navi-bar">
    <div><div class="progress"><span class="num"></span><span class="bar"><span class="fill"></span></span></div>
      <button type="button" class="pp" aria-label="슬라이드 멈춤"><i></i><i></i></button></div>
    <div><button type="button" class="arrow prev" aria-label="이전">&larr;</button><button type="button" class="arrow next" aria-label="다음">&rarr;</button></div>
  </div>
</section>

<section class="sec02">
  <div class="sec02-inner">
    <div class="sec02-div01">
      <div>
        <h2 class="eyebrow reveal">Our Products</h2>
        <p class="reveal">마라탕·훠궈 재료부터 <br class="pc">한식·중식·분식·일식·양식까지, <br class="pc"><b>요식업을 위한 <br class="mo">식자재 전문 공급</b>.</p>
        <div class="stats reveal">
          <div><strong>27</strong><span>년 업력 (1998~)</span></div>
        </div>
      </div>
      <a href="pages/product.html" class="more-btn reveal">MORE</a>
    </div>
    <div class="sec02-div02"><div class="scrolling" data-rolling></div></div>
  </div>
</section>

<section class="sec-biz">
  <div class="biz-head"><h2 class="eyebrow reveal">Business</h2>
    <p class="reveal">산지 → 물류 → 셰프의 주방.<br>엄선한 소싱부터 정교한 콜드체인, 주방까지 이레푸드서비스가 책임지고 연결합니다.</p></div>
  <div class="biz-grid">{bz}</div>
</section>

<section class="sec03">
  <div class="sec03-inner">
    <div class="sec03-title"><h2 class="eyebrow reveal">Notice</h2><a href="pages/customer.html#notice" class="more-btn reveal">MORE</a></div>
    <ul class="list-rows reveal" data-notice-preview></ul>
  </div>
</section>

<section class="sec04">
  <h2 class="eyebrow reveal">Inquiry</h2>
  <p class="reveal">대량·정기 납품, 프랜차이즈 공급 문의를 남겨주세요.<br>소량 구매는 스마트스토어에서 바로 주문하실 수 있습니다.</p>
  <div class="btns reveal"><a href="pages/customer.html#inquiry" class="pill">무료 견적 문의</a><a href="tel:{TEL_RAW}" class="pill line">전화 {TEL}</a><a href="{SNS['스마트스토어']}" target="_blank" rel="noopener" class="pill line">스마트스토어 (소량 구매)</a></div>
</section>
</main>
"""
    return (head("이레푸드서비스 주식회사 | 식자재 전문 유통·공급",
                 "이레푸드서비스 주식회사 — 마라탕·훠궈·한식·중식 등 요식업용 식자재 전문 유통·공급. 일반 음식점, 프랜차이즈, 단체급식을 위한 신뢰할 수 있는 파트너입니다.", "./")
            + header("./") + body + footer("./", js("./", "products", "notices")))


# ---------------------------------------------------------------- SUB PAGES
R = "../"
HIST = [
    ("2025", [("10월", "훠궈·마라탕 프랜차이즈 중국식품·신선식품 공급 업무협약"), ("6월", "숯불갈비 프랜차이즈 식자재 공급 업무협약"), ("6월", "'이레푸드서비스 주식회사'로 사명 변경 및 물류창고 확장 이전")]),
    ("2023", [("11월", "분식 프랜차이즈 식자재 공급 업무협약"), ("11월", "식자재 종합 쇼핑몰 '식봄' 입점"), ("11월", "중국 허베이성 소재 중국당면·분모자 생산 공장 국제무역부 담당자 미팅 및 중국 식품 직수입 협의"), ("6월", "유튜브·인스타그램 개설"), ("5월", "네이버 스마트스토어 입점"), ("1월", "한 식품 유통사와 중국식품·주류 수입 업무협약")]),
    ("2022", [("3월", "서울 강남구 대형 한식 식당 식자재 공급 업무협약")]),
    ("2021", [("8월", "자회사 (주)강한글로벌 설립 — 충청·전라권 식자재 및 주류 공급")]),
    ("2020", [("3월", "통신판매업 신고")]),
    ("2018", [("6월", "일식 프랜차이즈 식자재 공급 및 전용상품 물류 공급 업무협약")]),
    ("2017", [("7월", "물류창고 이전 — 경기도 하남시")]),
    ("2014", [("5월", "'이레글로벌'로 사명 변경")]),
    ("2013", [("8월", "서울 소재 보건소 구내식당 납품 협약")]),
    ("2009", [("2월", "종합식자재 도소매로 업무 확장")]),
    ("1998", [("5월", "이레유통 설립 — 서울시 강동구 천호동")]),
]


def company():
    tl = "".join(f'<div class="tl-year reveal"><h3>{y}</h3><ul>' + "".join(f"<li><b>{m}</b> {t}</li>" for m, t in it) + "</ul></div>" for y, it in HIST)
    body = sub_hero("Company", "1998년부터 이어온 신뢰, 이레푸드서비스", [("인사말", "#greeting"), ("연혁", "#history"), ("오시는 길", "#location")], R + "assets/images/hero/sourcing.jpg") + f"""
<main id="top">
<section class="wrap-in" id="greeting">
  <h2 class="sec-title">Greeting</h2><p class="sec-sub">인사말</p>
  <div class="greeting">
    <div class="poster reveal"><img src="{R}assets/images/poster-malatang.jpg" alt="이레푸드서비스 마라탕 식자재 유통 포스터" loading="lazy"></div>
    <div class="reveal">
      <p class="lead">산지에서 셰프의 주방까지,<br>품질과 신선도를 지키는 절제된 신뢰.</p>
      <p>1998년 서울 강동구 천호동에서 이레유통으로 시작한 이레푸드서비스 주식회사는 30여 년간 신뢰를 최우선 가치로 삼아 식자재 유통업의 길을 걸어왔습니다.</p>
      <p>중국식품, 마라탕·훠궈 식자재를 비롯해 한식·중식·분식·일식·양식까지 폭넓은 품목을 취급하며, 일반 음식점부터 대형 프랜차이즈, 단체급식까지 다양한 고객군에 안정적인 공급망을 제공하고 있습니다.</p>
      <p>다음 30년도 변함없는 신뢰로 준비하겠습니다.</p>
    </div>
  </div>
</section>
<section class="bg-beige" id="history"><div class="wrap-in">
  <h2 class="sec-title">History</h2><p class="sec-sub">연혁</p>
  <div class="timeline">{tl}</div>
</div></section>
<section class="wrap-in" id="location">
  <h2 class="sec-title">Location</h2><p class="sec-sub">오시는 길</p>
  <figure class="bldg reveal"><img src="{R}assets/images/building.jpg" alt="이레푸드서비스 주식회사 사옥 — 금강펜테리움 IX타워" loading="lazy"><figcaption>이레푸드서비스 본사 · 금강펜테리움 IX타워 B2</figcaption></figure>
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
    return head("COMPANY | 이레푸드서비스 주식회사", "1998년 이레유통으로 시작한 이레푸드서비스 주식회사의 인사말과 연혁, 오시는 길.", R) + header(R, "COMPANY", True) + body + footer(R, js(R, "map"))


def business():
    body = sub_hero("Business", "산지-물류-주방을 하나로 잇는 유통망", [], R + "assets/images/hero/quality.jpg") + f"""
<main id="top">
<section class="wrap-in">
  <p class="biz-intro reveal">이레푸드서비스 주식회사는 공산품부터 신선식품, 수산물, 육류까지 폭넓은 카테고리를 취급하며, 산지–물류–주방을 하나로 잇는 유통망을 갖추고 있습니다.</p>
  <div class="flow reveal">
    <div><small>SOURCING</small><h3>공산품 / 중국식품</h3><p>마라탕·훠궈 재료, 소스, 면류</p></div>
    <div><small>COLD CHAIN</small><h3>신선식품 / 수산물</h3><p>콜드체인 신선 배송</p></div>
    <div><small>QUALITY</small><h3>육류 / 냉동식품</h3><p>검수된 원재료 공급</p></div>
    <div><small>PARTNERS</small><h3>프랜차이즈 / 단체급식</h3><p>표준화·정기 납품</p></div>
  </div>
</section>
<section class="bg-beige"><div class="wrap-in">
  <h2 class="sec-title">Clients</h2><p class="sec-sub">주요 거래처 유형</p>
  <div class="three reveal">
    <div><h3>일반 음식점</h3><p>한식·중식·분식·일식·양식 등 업종을 가리지 않는 맞춤 공급</p></div>
    <div><h3>프랜차이즈</h3><p>전국 매장 단위 표준화 공급 및 전용상품 물류 지원</p></div>
    <div><h3>단체급식</h3><p>대량 수요에 대응하는 안정적인 정기 납품 체계</p></div>
  </div>
</div></section>
<section class="wrap-in">
  <h2 class="sec-title">Strength</h2><p class="sec-sub">이레푸드서비스의 강점</p>
  <div class="strength reveal">
    <div><span>01</span><h3>품질</h3><p>산지부터 검수된 원재료와 콜드체인 유지로 신선도를 지킵니다.</p></div>
    <div><span>02</span><h3>가격</h3><p>대량 유통망을 기반으로 합리적인 단가를 제공합니다.</p></div>
    <div><span>03</span><h3>유통망</h3><p>서울, 수도권 전역을 아우르는 물류 네트워크를 갖추고 있습니다.</p></div>
  </div>
  <div class="more-row"><a class="pill" style="background:#111;color:#fff" href="customer.html#inquiry">무료 견적 문의</a></div>
</section>
</main>
"""
    return head("BUSINESS | 이레푸드서비스 주식회사", "공산품·신선식품·수산물·육류를 취급하는 이레푸드서비스의 사업소개, 거래처 유형, 강점.", R) + header(R, "BUSINESS", True) + body + footer(R, "")


def product():
    body = sub_hero("Product", "마라탕·훠궈 재료를 비롯한 식자재 제품 목록", [], R + "assets/images/hero/coldchain.jpg") + """
<main id="top"><section class="wrap-in">
  <p class="prod-note">아래는 대표 제품 일부이며, 이 밖에도 훨씬 더 많은 품목을 취급하고 있습니다. 찾으시는 제품이 없다면 <a href="customer.html#inquiry">문의</a> 또는 <a href="tel:__TELRAW__">전화(__TEL__)</a>로 알려주세요.</p>
  <input type="search" class="search" data-product-search placeholder="제품명 검색 (예: 당면, 마라)" aria-label="제품명 검색">
  <div class="filter" data-product-filter></div>
  <div class="pgrid" data-product-grid></div>
  <div class="more-row"><button type="button" class="pill line" style="color:#111;border-color:#111" data-more>더보기</button></div>
</section></main>
"""
    body = body.replace("__TELRAW__", TEL_RAW).replace("__TEL__", TEL)
    return head("PRODUCT | 이레푸드서비스 주식회사", "이레푸드서비스 주식회사 취급 제품 목록 — 마라탕·훠궈 재료, 소스, 면류, 냉동식품, 육류 등.", R) + header(R, "PRODUCT", True) + body + footer(R, js(R, "products"))


def product_detail():
    body = sub_hero("Product", "제품 상세", [("← 제품 목록", "product.html")], R + "assets/images/hero/coldchain.jpg") + '<main id="top"><section class="wrap-in"><div class="detail" data-product-detail>불러오는 중…</div></section></main>\n'
    return head("제품 상세 | 이레푸드서비스 주식회사", "이레푸드서비스 취급 제품 상세", R) + header(R, "PRODUCT", True) + body + footer(R, js(R, "products"))


def customer():
    body = sub_hero("Customer", "공지사항과 1:1 문의", [("공지사항", "#notice"), ("1:1 문의", "#inquiry")], R + "assets/images/hero/partners.jpg") + f"""
<main id="top">
<section class="wrap-in" id="notice">
  <h2 class="sec-title">Notice</h2><p class="sec-sub">공지사항</p>
  <ul class="list-rows" data-notice-list></ul>
</section>
<section class="bg-beige" id="inquiry"><div class="wrap-in">
  <h2 class="sec-title">Inquiry</h2><p class="sec-sub">대량·정기 납품 상담은 문의를 남겨주세요. 급하시면 <a href="tel:{TEL_RAW}" style="text-decoration:underline">{TEL}</a> 로 전화 주세요.</p>
  <div class="quote-box" data-quote-box hidden><h4>견적 요청 제품</h4><ul></ul></div>
  <form class="form" data-contact-form action="https://formspree.io/f/xzezqbll" method="POST">
    <input type="text" name="_gotcha" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fg"><label for="name">이름</label><input type="text" id="name" name="name" required></div>
    <div class="fg"><label for="phone">연락처</label><input type="tel" id="phone" name="phone" required></div>
    <div class="fg"><label for="email">이메일</label><input type="email" id="email" name="email" required></div>
    <div class="fg"><label for="message">문의내용</label><textarea id="message" name="message" required></textarea></div>
    <div class="fg ck"><input type="checkbox" id="consent" name="consent" required><label for="consent" style="margin:0;font-weight:400">개인정보 수집·이용에 동의합니다. (<a href="privacy.html" style="text-decoration:underline">개인정보취급방침 보기</a>) — 수집 항목: 이름, 연락처, 이메일 / 목적: 문의 응대 / 보유기간: 처리 완료 후 즉시 파기</label></div>
    <button type="submit">문의 보내기</button>
    <p class="form-status" data-form-status role="status"></p>
  </form>
</div></section>
</main>
"""
    return head("CUSTOMER | 이레푸드서비스 주식회사", "이레푸드서비스 공지사항 및 1:1 문의.", R) + header(R, "CUSTOMER", True) + body + footer(R, js(R, "notices", "contact", "products"))


def notice_detail():
    body = sub_hero("Notice", "공지사항", [("← 공지 목록", "customer.html#notice")], R + "assets/images/hero/partners.jpg") + '<main id="top"><section class="wrap-in"><div data-notice-detail>불러오는 중…</div><a class="back more-btn" href="customer.html#notice" style="width:auto;padding:0 28px">목록으로</a></section></main>\n'
    return head("공지사항 | 이레푸드서비스 주식회사", "이레푸드서비스 공지사항", R) + header(R, "CUSTOMER", True) + body + footer(R, js(R, "notices"))


def legal(slug, title):
    """기존 사이트의 약관 본문을 재사용. '예시 초안' 등 내부 메모 문구는 제거."""
    src = open(os.path.join(OLD, f"{slug}.html"), encoding="utf-8").read()
    m = re.search(r'<h1>.*?</h1>(.*?)</div>\s*</section>', src, re.S)
    inner = m.group(1) if m else ""
    inner = re.sub(r'<p[^>]*>※[^<]*</p>', '', inner)
    inner = re.sub(r'\sstyle="[^"]*"', '', inner)
    body = sub_hero(title, "", [], R + "assets/images/hero/sourcing.jpg") + f'<main id="top"><section class="wrap-in"><div class="doc">{inner}</div></section></main>\n'
    return head(f"{title} | 이레푸드서비스 주식회사", f"이레푸드서비스 주식회사 {title}", R) + header(R, "", True) + body + footer(R, "")


if __name__ == "__main__":
    write("index.html", home())
    write("pages/company.html", company())
    write("pages/business.html", business())
    write("pages/product.html", product())
    write("pages/product-detail.html", product_detail())
    write("pages/customer.html", customer())
    write("pages/notice-detail.html", notice_detail())
    # 약관 3종은 pages/*.html 에 이미 생성돼 있음. 원본 폴더(OLD)가 있을 때만 다시 생성한다.
    if os.path.isdir(OLD):
        write("pages/terms.html", legal("terms", "이용약관"))
        write("pages/privacy.html", legal("privacy", "개인정보취급방침"))
        write("pages/email-policy.html", legal("email-policy", "이메일무단수집거부"))
    print("built")
