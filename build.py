#!/usr/bin/env python3
"""Dokki Scan — static site generator.

Generates the full Arabic + English site from data.json (exams, blog, site facts)
and one shared HTML template in this file. No build step, no server code.

Usage:  python3 build.py        (writes pages into this directory)
        python3 build.py --check (also verifies every internal link resolves)
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
SITE = DATA["site"]
EXAMS = DATA["exams"]
BLOG = DATA["blog"]
BASE = SITE["base_url"].rstrip("/")

# ---------------------------------------------------------------- strings
S = {
    "ar": {
        "dir": "rtl", "lang": "ar", "lang_name": "English", "lang_code": "en",
        "tagline": "مركز أشعة تشخيصية متقدم في الدقي",
        "open": "مفتوح 24 ساعة / 7 أيام في الأسبوع",
        "nav_home": "الرئيسية", "nav_results": "نتائجي", "nav_preps": "الفحوصات والتحضيرات",
        "nav_checkup": "الفحص الشامل", "nav_why": "لماذا دقي سكان", "nav_find": "اعثر علينا",
        "nav_blog": "المدونة", "nav_book": "احجز موعداً",
        "hero_badge": "مفتوح 24 ساعة / 7 أيام في الأسبوع",
        "hero_title": "مستعدون لجميع الطوارئ",
        "hero_text": "المركز مجهز بالكامل لاستقبال الحالات الحرجة في أي وقت، براحة وسرعة وأمان. لا يلزم تحديد موعد مسبق.",
        "hero_cta_book": "احجز موعداً", "hero_cta_call": "اتصل 15669",
        "hero_art_big": "دقي سكان", "hero_art_small": "أشعة تشخيصية متقدمة — الدقي، الجيزة",
        "trust_title": "أحدث تقنيات الأشعة لأدق تشخيص ممكن",
        "trust_text": "على مدار أكثر من 30 عاماً، يجمع دقي سكان بين أحدث أجهزة الأشعة في مصر ونخبة من الاستشاريين المتخصصين لتقديم تشخيص دقيق وتقارير أسرع ورعاية أكثر أماناً.",
        "stat_years": "سنة خبرة", "stat_emergency": "طوارئ جاهزة", "stat_review": "مراحل مراجعة للتقرير",
        "stat_rooms": "غرف أشعة", "stat_doctors": "أطباء متخصصون", "stat_partners": "شركاء محليون", "stat_clients": "عملاء راضون",
        "steps_title": "ثلاث خطوات بسيطة",
        "step1_t": "تشخيص دقيق", "step1_d": "أجهزة متقدمة ومراجعة بقيادة استشاريين لفحوصات الرنين والمقطعية والـ PET-CT والسونار والأشعة العادية وتصوير الثدي والمزيد.",
        "step2_t": "بدون حجز مسبق", "step2_d": "نعمل 24 ساعة يومياً طوال أيام الأسبوع، ومجهزون لاستقبال الحالات الحرجة براحة وسرعة.",
        "step3_t": "استلام النتائج", "step3_d": "يمكن إرسال تقارير الأشعة رقمياً عبر واتساب أو البريد الإلكتروني فور جاهزيتها.",
        "exams_title": "الفحوصات والتحضيرات", "exams_sub": "كل فئة فحص تعرض التحضير والرابط الصحيح للتفاصيل.",
        "prep_link": "التحضير والتفاصيل ←", "details_link": "التفاصيل ←",
        "checkup_title": "الفحص الشامل", "checkup_text": "فحوصات تشخيصية لتقييم شامل لحالتك الصحية — للرجال والنساء — لاكتشاف أي مشكلة صحية في مرحلة مبكرة، مع مراجعة نخبة من الاستشاريين وتقرير تفصيلي واضح.",
        "checkup_cta": "اعرف المزيد عن الفحص الشامل",
        "video_title": "شاهد دقي سكان من الداخل", "video_text": "من مراجعة الصور حتى التقرير، دقي سكان مصمم للتشخيص الدقيق وسلامة المريض وسرعة الخدمة.",
        "video_cta": "اكتشف تقنياتنا",
        "branch": "الفرع الرئيسي", "phone": "الهاتف", "email": "البريد الإلكتروني",
        "hours": "مفتوح ٢٤/٧", "rights": "جميع الحقوق محفوظة.",
        "footer_about": "مزود رائد لخدمات التصوير الطبي المتطورة في مصر. صحتك أولويتنا.",
        "quick_links": "روابط سريعة", "services": "خدماتنا", "contact": "تواصل معنا",
        "book_now": "احجز الآن", "whatsapp": "واتساب", "call": "اتصل", "directions": "الاتجاهات",
        "uses_title": "يُستخدم في", "prep_title": "التحضير للفحص",
        "back_exams": "← كل الفحوصات", "back_preps": "← كل التحضيرات", "back_blog": "← كل مقالات المدونة",
    },
    "en": {
        "dir": "ltr", "lang": "en", "lang_name": "العربية", "lang_code": "ar",
        "tagline": "Advanced diagnostic imaging centre in Dokki",
        "open": "Open 24 hours / 7 days a week",
        "nav_home": "Home", "nav_results": "My Results", "nav_preps": "Exams & Preparations",
        "nav_checkup": "Full Check-up", "nav_why": "Why Dokki Scan", "nav_find": "Find Us",
        "nav_blog": "Blog", "nav_book": "Book Appointment",
        "hero_badge": "Open 24 hours / 7 days a week",
        "hero_title": "Ready for every emergency",
        "hero_text": "The centre is fully equipped to receive critical cases at any time, with comfort, speed and safety. No prior appointment is needed.",
        "hero_cta_book": "Book Appointment", "hero_cta_call": "Call 15669",
        "hero_art_big": "Dokki Scan", "hero_art_small": "Advanced diagnostic imaging — Dokki, Giza",
        "trust_title": "The latest imaging technology for the most accurate diagnosis",
        "trust_text": "For over 30 years, Dokki Scan has combined the latest imaging equipment in Egypt with a team of specialist consultants to deliver accurate diagnoses, faster reports and safer care.",
        "stat_years": "years of experience", "stat_emergency": "emergency ready", "stat_review": "report review stages",
        "stat_rooms": "imaging rooms", "stat_doctors": "specialist doctors", "stat_partners": "local partners", "stat_clients": "happy clients",
        "steps_title": "Three simple steps",
        "step1_t": "Accurate diagnosis", "step1_d": "Advanced equipment and consultant-led review for MRI, CT, PET-CT, ultrasound, plain X-ray, breast imaging and more.",
        "step2_t": "No prior booking", "step2_d": "We work 24 hours a day, every day of the week, and are equipped to receive critical cases with comfort and speed.",
        "step3_t": "Receive your results", "step3_d": "Radiology reports can be sent digitally by WhatsApp or email as soon as they are ready.",
        "exams_title": "Exams & Preparations", "exams_sub": "Every exam category shows its preparation and the right link for details.",
        "prep_link": "Preparation & details →", "details_link": "Details →",
        "checkup_title": "Full Check-up", "checkup_text": "Diagnostic tests for a complete assessment of your health — for men and women — to detect any health problem early, reviewed by leading consultants, with a clear detailed report.",
        "checkup_cta": "Learn more about the full check-up",
        "video_title": "See Dokki Scan from the inside", "video_text": "From image review to the final report, Dokki Scan is designed for accurate diagnosis, patient safety and fast service.",
        "video_cta": "Discover our technology",
        "branch": "Main branch", "phone": "Phone", "email": "Email",
        "hours": "Open 24/7", "rights": "All rights reserved.",
        "footer_about": "A leading provider of advanced medical imaging services in Egypt. Your health comes first.",
        "quick_links": "Quick links", "services": "Our services", "contact": "Contact us",
        "book_now": "Book now", "whatsapp": "WhatsApp", "call": "Call", "directions": "Directions",
        "uses_title": "Used for", "prep_title": "Preparing for the exam",
        "back_exams": "← All exams", "back_preps": "← All preparations", "back_blog": "← All blog articles",
    },
}

PREP_SLUG = {  # service slug -> preparation page slug (EN / AR)
    "mri-examination": "mri-examination", "ct-examination": "ct-multislice-examination",
    "ultrasound-colour-doppler-examination": "ultrasound-colour-doppler",
    "x-ray-examination": "x-ray-examination", "breast-examination": "breast-examination",
    "pet-ct-examination": "pet-ct", "dexa-bone-densitometry-examination": "dexa-bone-densitometry",
    "dental-examination": "dental-examination", "echo-ecg-examination": "echo-ecg-examination",
    "interventional-radiology-examination": "interventional-radiology-examination",
    "3d-imaging-examination": "3d-imaging-examination",
}


def prefix_for(out: str) -> str:
    """Relative path from a generated page back to the site root."""
    depth = len(Path(out).parent.parts) if str(Path(out).parent) != "." else 0
    return "../" * depth


def dir_url(out: str) -> str:
    """Directory-style URL of a generated page, relative to site root."""
    p = Path(out)
    return "" if str(p.parent) == "." else str(p.parent) + "/"


def exam_name(e, lang):
    return e["name_ar"] if lang == "ar" else e["name_en"]


def exam_slug(e, lang):
    return e["slug_ar"] if lang == "ar" else e["slug_en"]


def prep_slug(e, lang):
    base = PREP_SLUG[e["slug_en"]]
    return base + "-ar" if lang == "ar" else base


def service_url(e, lang, prefix):
    return prefix + (("ar/" + exam_slug(e, lang)) if lang == "ar" else exam_slug(e, lang)) + "/"


def prep_url(e, lang, prefix):
    base = "ar/exams-preparations-ar/" if lang == "ar" else "exams-preparations/"
    return prefix + base + prep_slug(e, lang) + "/"


# ---------------------------------------------------------------- template
def render(lang, out, title, desc, body, active, counterpart_out):
    t = S[lang]
    p = prefix_for(out)
    counter = dir_url(counterpart_out) if counterpart_out else ""
    nav = [
        ("home", t["nav_home"], "" if lang == "en" else "ar/"),
        ("results", t["nav_results"], ("ar/my-results-ar/" if lang == "ar" else "my-results/")),
        ("preps", t["nav_preps"], ("ar/exams-preparations-ar/" if lang == "ar" else "exams-preparations/")),
        ("checkup", t["nav_checkup"], ("ar/full-check-up-ar/" if lang == "ar" else "full-check-up/")),
        ("why", t["nav_why"], ("ar/why-dokki-scan-ar/" if lang == "ar" else "why-dokki-scan/")),
        ("find", t["nav_find"], ("ar/find-us-ar/" if lang == "ar" else "find-us/")),
        ("blog", t["nav_blog"], ("ar/blog-ar/" if lang == "ar" else "blog/")),
    ]
    def _href(u):
        return u if u else "./"

    nav_html = "".join(
        f'<a href="{_href(p + href)}" class="{"active" if key == active else ""}">{label}</a>'
        for key, label, href in nav
    )
    book_href = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    lang_href = _href(p + counter)
    home_href = _href(p + ("" if lang == "en" else "ar/"))
    services_links = "".join(
        f'<li><a href="{service_url(e, lang, p)}">{exam_name(e, lang)}</a></li>' for e in EXAMS[:6]
    )
    quick_links = "".join(
        f'<li><a href="{_href(p + href)}">{label}</a></li>'
        for label, href in [
            (t["nav_home"], "" if lang == "en" else "ar/"),
            (t["nav_why"], "ar/why-dokki-scan-ar/" if lang == "ar" else "why-dokki-scan/"),
            (t["nav_preps"], "ar/exams-preparations-ar/" if lang == "ar" else "exams-preparations/"),
            (t["nav_checkup"], "ar/full-check-up-ar/" if lang == "ar" else "full-check-up/"),
            (t["nav_results"], "ar/my-results-ar/" if lang == "ar" else "my-results/"),
            (t["nav_blog"], "ar/blog-ar/" if lang == "ar" else "blog/"),
            (t["nav_find"], "ar/find-us-ar/" if lang == "ar" else "find-us/"),
        ]
    )
    return f"""<!DOCTYPE html>
<html lang="{t["lang"]}" dir="{t["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {SITE["name_ar"] if lang == "ar" else SITE["name_en"]}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">{"تخطي إلى المحتوى الرئيسي" if lang == "ar" else "Skip to main content"}</a>
<div class="topbar"><div class="container">
<span>{t["open"]}</span>
<span><span class="dot">●</span> <a href="tel:{SITE["hotline"]}">{SITE["hotline"]}</a> &nbsp;·&nbsp; <a href="https://wa.me/{SITE["phone_intl"]}">{SITE["phone"]}</a></span>
</div></div>
<header class="site-header"><div class="container header-inner">
<a class="logo" href="{home_href}">Dokki<span>Scan</span></a>
<button class="menu-toggle" aria-expanded="false" aria-label="Menu">☰</button>
<nav class="main-nav" aria-label="Main">{nav_html}
<a class="btn" href="{book_href}">{t["nav_book"]}</a>
<a class="lang-switch" href="{lang_href}">{t["lang_name"]}</a>
</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><h3>Dokki Scan</h3><p>{t["footer_about"]}</p>
<p><a href="{SITE["facebook"]}">Facebook</a> · <a href="{SITE["instagram"]}">Instagram</a> · <a href="https://wa.me/{SITE["phone_intl"]}">WhatsApp</a></p></div>
<div><h3>{t["quick_links"]}</h3><ul>{quick_links}</ul></div>
<div><h3>{t["services"]}</h3><ul>{services_links}</ul></div>
</div>
<div class="copyright">
<p><strong>{t["branch"]}:</strong> {SITE["address_ar"] if lang == "ar" else SITE["address_en"]}<br>
{t["phone"]}: <a href="tel:{SITE["hotline"]}">{SITE["hotline"]}</a> · <a href="tel:{SITE["phone_intl"]}">{SITE["phone"]}</a> · <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> · {t["hours"]}</p>
<p>© 2026 {SITE["name_ar"] if lang == "ar" else SITE["name_en"]} — {t["rights"]}</p>
</div>
</div></footer>
<script src="{p}assets/js/main.js"></script>
</body>
</html>
"""


def exam_card(e, lang, p, i):
    t = S[lang]
    v = ["", " v2", " v3"][i % 3]
    return f"""<article class="card">
<div class="exam-visual{v}" aria-hidden="true">{e["code"]}</div>
<h3>{exam_name(e, lang)}</h3>
<p>{e["short_ar"] if lang == "ar" else e["short_en"]}</p>
<p>{e["desc_ar"] if lang == "ar" else e["desc_en"]}</p>
<a class="more" href="{service_url(e, lang, p)}">{t["details_link"]}</a>
<a class="more" href="{prep_url(e, lang, p)}">{t["prep_link"]}</a>
</article>"""


def stats_section(lang):
    t = S[lang]
    return f"""<section class="stats"><div class="container stats-grid">
<div class="stat"><b><span data-count="30" data-suffix="+">30+</span></b><span>{t["stat_years"]}</span></div>
<div class="stat"><b>24/7</b><span>{t["stat_emergency"]}</span></div>
<div class="stat"><b><span data-count="3" data-suffix="">3</span></b><span>{t["stat_review"]}</span></div>
<div class="stat"><b><span data-count="11" data-suffix="">11</span></b><span>{"فئة فحص" if lang == "ar" else "exam categories"}</span></div>
</div></section>"""


def video_section(lang, p):
    t = S[lang]
    return f"""<section class="section alt"><div class="container">
<p class="eyebrow">{"شاهد المركز أثناء العمل" if lang == "ar" else "See the centre at work"}</p>
<h2>{t["video_title"]}</h2><p class="lead">{t["video_text"]}</p>
<div class="video-wrap"><iframe src="https://www.youtube.com/embed/{SITE["youtube_id"]}?rel=0&amp;modestbranding=1&amp;playsinline=1" title="Dokki Scan video" allowfullscreen loading="lazy"></iframe></div>
<p style="margin-top:16px"><a class="btn" href="{p}{"ar/exams-preparations-ar/" if lang == "ar" else "exams-preparations/"}">{t["video_cta"]}</a></p>
</div></section>"""

# ---------------------------------------------------------------- page bodies
def home_body(lang, p):
    t = S[lang]
    cards = "".join(exam_card(e, lang, p, i) for i, e in enumerate(EXAMS))
    steps = "".join(
        f'<div class="step"><div class="num">{i+1}</div><h3>{tt}</h3><p>{dd}</p></div>'
        for i, (tt, dd) in enumerate([(t["step1_t"], t["step1_d"]), (t["step2_t"], t["step2_d"]), (t["step3_t"], t["step3_d"])])
    )
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    check = p + ("ar/full-check-up-ar/" if lang == "ar" else "full-check-up/")
    return f"""<section class="hero"><div class="container hero-grid">
<div><span class="badge">{t["hero_badge"]}</span>
<h1>{t["hero_title"]}</h1>
<p class="lead">{t["hero_text"]}</p>
<div class="hero-actions">
<a class="btn" href="{book}">{t["hero_cta_book"]}</a>
<a class="btn btn-outline" href="tel:{SITE["hotline"]}">{t["hero_cta_call"]}</a>
<a class="btn btn-whatsapp" href="https://wa.me/{SITE["phone_intl"]}">WhatsApp</a>
</div></div>
<div class="hero-art"><div class="big">{t["hero_art_big"]}</div><small>{t["hero_art_small"]}</small>
<small>CT · PET-CT · MRI · {"سونار" if lang == "ar" else "Ultrasound"} · {"أشعة سينية" if lang == "ar" else "X-Ray"}</small></div>
</div></section>
{stats_section(lang)}
<section class="section"><div class="container">
<p class="eyebrow">{"أحدث تقنيات الأشعة" if lang == "ar" else "The latest imaging technology"}</p>
<h2>{t["trust_title"]}</h2><p class="lead">{t["trust_text"]}</p>
<h2 style="margin-top:40px">{t["steps_title"]}</h2><div class="steps">{steps}</div>
</div></section>
<section class="section alt"><div class="container">
<p class="eyebrow">{"الفحوصات والتحضيرات" if lang == "ar" else "Exams & preparations"}</p>
<h2>{t["exams_title"]}</h2><p class="lead">{t["exams_sub"]}</p>
<div class="grid">{cards}</div>
</div></section>
<section class="section"><div class="container">
<h2>{t["checkup_title"]}</h2><p class="lead">{t["checkup_text"]}</p>
<p><a class="btn" href="{check}">{t["checkup_cta"]}</a></p>
</div></section>
{video_section(lang, p)}
<section class="section"><div class="container">
<div class="card"><h2>{t["branch"]}</h2>
<p>{SITE["address_ar"] if lang == "ar" else SITE["address_en"]}</p>
<p>{t["phone"]}: <a href="tel:{SITE["hotline"]}">{SITE["hotline"]}</a> · {SITE["phone"]} · <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> · {t["hours"]}</p>
<p><a class="btn" href="{book}">{t["book_now"]}</a> <a class="btn btn-outline" href="{SITE["maps_link"]}" target="_blank" rel="noopener">{t["directions"]}</a></p>
</div></div></section>"""


def why_body(lang, p):
    t = S[lang]
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    points_ar = [
        ("خبرة تزيد عن 30 عاماً", "فريق من الاستشاريين المتخصصين يراجع كل تقرير قبل إصداره."),
        ("أجهزة حديثة", "مقطعية ورنين وPET-CT وسونار وأشعة سينية رقمية في مكان واحد."),
        ("مفتوح دائماً", "24 ساعة في اليوم، 7 أيام في الأسبوع — بما فيها الطوارئ، وبدون حجز مسبق."),
        ("مراجعة من ثلاث مراحل", "كل تقرير يمر بثلاث مراحل مراجعة قبل أن يصل إليك أو إلى طبيبك."),
        ("نتائج رقمية سريعة", "تقريرك يصلك عبر واتساب أو البريد الإلكتروني فور جاهزيته."),
        ("راحة المريض أولاً", "دخول سهل من الدور الأرضي والأول في برج ساريدار، وفريق استقبال يساعدك في كل خطوة."),
    ]
    points_en = [
        ("Over 30 years of experience", "A team of specialist consultants reviews every report before it is issued."),
        ("Modern equipment", "CT, MRI, PET-CT, ultrasound and digital X-ray in one place."),
        ("Always open", "24 hours a day, 7 days a week — including emergencies, with no prior booking."),
        ("Three-stage review", "Every report passes three review stages before it reaches you or your doctor."),
        ("Fast digital results", "Your report reaches you by WhatsApp or email as soon as it is ready."),
        ("Patient comfort first", "Easy access from the ground and first floors of Saridar Tower, with a reception team that helps at every step."),
    ]
    items = "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p></div>' for a, b in (points_ar if lang == "ar" else points_en))
    return f"""<section class="section"><div class="container">
<p class="eyebrow">Dokki Scan</p>
<h1>{"لماذا دقي سكان؟" if lang == "ar" else "Why Dokki Scan?"}</h1>
<p class="lead">{t["trust_text"]}</p>
<div class="grid two">{items}</div>
<p style="margin-top:28px"><a class="btn" href="{book}">{t["book_now"]}</a></p>
</div></section>
{stats_section(lang)}"""


def checkup_body(lang, p):
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    if lang == "ar":
        intro = "فحص شامل للرجال والنساء لاكتشاف أي مشكلة صحية في مرحلة مبكرة، مع مراجعة نخبة من الاستشاريين وتقرير تفصيلي واضح."
        rows = [
            ("للرجال", "فحوصات تصوير وتحاليل مخبرية مختارة حسب العمر وعوامل الخطر، مع تقرير موحد يراجعه استشاري."),
            ("للنساء", "فحوصات تصوير وتحاليل مخبرية مختارة حسب العمر وعوامل الخطر، مع تقرير موحد يراجعه استشاري."),
            ("كيف يتم؟", "احجز موعداً، واحضر في اليوم المحدد، وستمر بكل الفحوصات في زيارة واحدة منظمة، ثم يصلك التقرير رقمياً."),
            ("التحضير", "قد يلزم الصيام لبعض الفحوصات — يؤكد لك فريق الاستقبال التفاصيل عند الحجز."),
        ]
    else:
        intro = "A complete check-up for men and women to detect any health problem early, reviewed by leading consultants, with a clear detailed report."
        rows = [
            ("For men", "Imaging and selected laboratory tests chosen by age and risk factors, with one unified report reviewed by a consultant."),
            ("For women", "Imaging and selected laboratory tests chosen by age and risk factors, with one unified report reviewed by a consultant."),
            ("How it works", "Book an appointment, attend on the chosen day, complete all tests in one organised visit, then receive your report digitally."),
            ("Preparation", "Fasting may be needed for some tests — the reception team confirms the details when you book."),
        ]
    cards = "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p></div>' for a, b in rows)
    return f"""<section class="section"><div class="container">
<p class="eyebrow">{"الفحص الشامل" if lang == "ar" else "Full check-up"}</p>
<h1>{"الفحص الشامل" if lang == "ar" else "Full Check-up"}</h1>
<p class="lead">{intro}</p>
<div class="grid two">{cards}</div>
<p style="margin-top:28px"><a class="btn" href="{book}">{"احجز الفحص الشامل" if lang == "ar" else "Book the full check-up"}</a></p>
</div></section>"""


def results_body(lang, p):
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    if lang == "ar":
        steps = [
            ("بعد الفحص", "يتم تجهيز الصور ومراجعة التقرير من الفريق المختص في ثلاث مراحل."),
            ("إرسال رقمي", "يمكن إرسال التقرير عبر واتساب أو البريد الإلكتروني عند الجاهزية."),
            ("دعم المتابعة", "فريق المركز يساعدك في أي استفسار عن الاستلام أو التحضير — 24 ساعة."),
        ]
        cards = [
            ("واتساب", "استلام التقرير مباشرة على واتساب.", "https://wa.me/" + SITE["phone_intl"]),
            ("البريد الإلكتروني", "إرسال النتائج والتقرير بصيغة رقمية.", "mailto:" + SITE["email"]),
            ("دعم سريع", "فريق المركز متاح للمساعدة في أي وقت — اتصل 15669.", "tel:" + SITE["hotline"]),
        ]
        title, lead = "نتائجي", "استلم نتائجك بسهولة: تقارير الأشعة متاحة عبر واتساب أو البريد الإلكتروني فور جاهزيتها. لا يوجد تسجيل دخول هنا — فقط أخبرنا عند الحجز كيف تفضل استلام تقريرك."
    else:
        steps = [
            ("After the scan", "Images are prepared and the report is reviewed by the specialist team in three stages."),
            ("Digital delivery", "The report can be sent by WhatsApp or email when it is ready."),
            ("Follow-up support", "The centre team helps with any question about collection or preparation — 24 hours."),
        ]
        cards = [
            ("WhatsApp", "Receive your report directly on WhatsApp.", "https://wa.me/" + SITE["phone_intl"]),
            ("Email", "Results and the report sent digitally.", "mailto:" + SITE["email"]),
            ("Fast support", "The centre team is available to help at any time — call 15669.", "tel:" + SITE["hotline"]),
        ]
        title, lead = "My Results", "Receive your results easily: radiology reports are available by WhatsApp or email as soon as they are ready. There is no login here — just tell us when you book how you would like to receive your report."
    step_html = "".join(f'<div class="step"><div class="num">{i+1}</div><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(steps))
    card_html = "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p><a class="more" href="{c}">{"تواصل ←" if lang == "ar" else "Contact →"}</a></div>' for a, b, c in cards)
    return f"""<section class="section"><div class="container">
<p class="eyebrow">{"النتائج أونلاين" if lang == "ar" else "Results online"}</p>
<h1>{title}</h1><p class="lead">{lead}</p>
<div class="grid">{card_html}</div>
<h2 style="margin-top:40px">{"كيف تصل إليك النتائج؟" if lang == "ar" else "How do your results reach you?"}</h2>
<div class="steps">{step_html}</div>
<div class="note"><p>{"<strong>ملاحظة:</strong> هذه الصفحة ليست بوابة دخول ولا تطلب أي بيانات. إذا لم يصلك تقريرك، تواصل معنا على واتساب أو اتصل على 15669." if lang == "ar" else "<strong>Note:</strong> this page is not a login portal and asks for no details. If your report has not arrived, message us on WhatsApp or call 15669."}</p></div>
<p><a class="btn" href="{book}">{"احجز فحصاً" if lang == "ar" else "Book a scan"}</a></p>
</div></section>"""


def findus_body(lang, p):
    t = S[lang]
    return f"""<section class="section"><div class="container">
<p class="eyebrow">{"اعثر علينا" if lang == "ar" else "Find us"}</p>
<h1>{"اعثر علينا" if lang == "ar" else "Find Us"}</h1>
<p class="lead">{t["tagline"]} — {SITE["address_ar"] if lang == "ar" else SITE["address_en"]}</p>
<div class="contact-cards">
<div class="card"><h3>{t["branch"]}</h3><p>{SITE["address_ar"] if lang == "ar" else SITE["address_en"]}</p><p>{t["hours"]}</p></div>
<div class="card"><h3>{t["phone"]}</h3><p><a href="tel:{SITE["hotline"]}">{SITE["hotline"]}</a><br><a href="tel:{SITE["phone_intl"]}">{SITE["phone"]}</a></p><p><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p></div>
<div class="card"><h3>{t["directions"]}</h3><p>{"برج ساريدار، شارع التحرير، الدقي — دخول سهل من الدور الأرضي والأول." if lang == "ar" else "Saridar Tower, El Tahrir St, Dokki — easy access from the ground and first floors."}</p><p><a class="btn" href="{SITE["maps_link"]}" target="_blank" rel="noopener">{t["directions"]}</a></p></div>
</div>
<div class="map-wrap"><iframe title="Dokki Scan map" src="{SITE["maps_url"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="placeholder-note" style="margin-top:12px">{"الخريطة مضمّنة من خرائط جوجل (رابط عام للعنوان)." if lang == "ar" else "Map embedded from Google Maps (public link to the address)."}</p>
</div></section>"""


def blog_index_body(lang, p):
    base = "ar/blog-ar/" if lang == "ar" else "blog/"
    items = ""
    for i, b in enumerate(BLOG):
        slug = b["slug_ar"] if lang == "ar" else b["slug_en"]
        title = b["title_ar"] if lang == "ar" else b["title_en"]
        summ = b["summary_ar"] if lang == "ar" else b["summary_en"]
        items += f"""<article class="card post-card"><div class="post-thumb" aria-hidden="true">{"✚" if i % 2 == 0 else "◉"}</div>
<div><h3><a href="{p}{base}{slug}/">{title}</a></h3><p>{summ}</p>
<a class="more" href="{p}{base}{slug}/">{"اقرأ المقال ←" if lang == "ar" else "Read the article →"}</a></div></article>"""
    return f"""<section class="section"><div class="container">
<p class="eyebrow">{"المدونة" if lang == "ar" else "Blog"}</p>
<h1>{"المدونة" if lang == "ar" else "Blog"}</h1>
<p class="lead">{"مقالات قصيرة تشرح فحوصات الأشعة بلغة بسيطة." if lang == "ar" else "Short articles explaining imaging tests in plain language."}</p>
<div class="post-list">{items}</div>
</div></section>"""


def article_body(lang, p, b):
    title = b["title_ar"] if lang == "ar" else b["title_en"]
    paras = b["body_ar"] if lang == "ar" else b["body_en"]
    back = p + ("ar/blog-ar/" if lang == "ar" else "blog/")
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    body = "".join(f"<p>{x}</p>" for x in paras)
    return f"""<section class="section"><div class="container article-body">
<p><a href="{back}">{"← كل مقالات المدونة" if lang == "ar" else "← All blog articles"}</a></p>
<h1>{title}</h1>{body}
<div class="note"><p>{"هل تحتاج هذا الفحص؟ احجز موعداً وسيتواصل معك فريق الاستقبال للتأكيد." if lang == "ar" else "Do you need this test? Book an appointment and the reception team will confirm with you."}</p></div>
<p><a class="btn" href="{book}">{"احجز موعداً" if lang == "ar" else "Book appointment"}</a></p>
</div></section>"""


def book_body(lang, p):
    if lang == "ar":
        labels = {"title": "احجز موعداً", "lead": "احجز فحصك في دقي سكان. املأ البيانات وسيقوم فريق الاستقبال بالتواصل معك لتأكيد الموعد والتحضيرات المطلوبة. بعد الإرسال سيتم فتح واتساب برسالة جاهزة لتأكيد الطلب بسرعة.",
                  "name": "الاسم بالكامل", "mobile": "رقم الموبايل", "exam": "نوع الفحص", "day": "يوم الحجز", "hour": "ساعة الحجز",
                  "flex": "مرونة الموعد", "notes": "ملاحظات أو اسم الطبيب", "submit": "إرسال طلب الحجز",
                  "flex_opts": ["الوقت المفضل تحديداً", "الصباح مناسب", "بعد الظهر مناسب", "المساء مناسب", "طوارئ / في أسرع وقت"],
                  "ok": "تم تجهيز طلبك — ستفتح واتساب الآن برسالة جاهزة. إذا لم تفتح، أرسل رسالتك يدوياً إلى 01000010144.",
                  "choose": "— اختر —", "other": "أخرى", "privacy": "سنستخدم هذه البيانات للتواصل معك فقط."}
    else:
        labels = {"title": "Book Appointment", "lead": "Book your scan at Dokki Scan. Fill in the details and the reception team will contact you to confirm the appointment and the required preparations. After sending, WhatsApp will open with a ready message to confirm your request quickly.",
                  "name": "Full name", "mobile": "Mobile number", "exam": "Exam type", "day": "Booking day", "hour": "Booking hour",
                  "flex": "Appointment flexibility", "notes": "Notes / doctor name", "submit": "Send booking request",
                  "flex_opts": ["Preferred time exactly", "Morning works", "Afternoon works", "Evening works", "Emergency / as soon as possible"],
                  "ok": "Your request is ready — WhatsApp will open now with a prepared message. If it does not open, send your message manually to 01000010144.",
                  "choose": "— Choose —", "other": "Other", "privacy": "We will use these details only to contact you."}
    exam_opts = "".join(f'<option value="{exam_name(e, lang)}">{exam_name(e, lang)}</option>' for e in EXAMS)
    exam_opts += f'<option value="{"الفحص الشامل" if lang == "ar" else "Full Check-up"}">{"الفحص الشامل" if lang == "ar" else "Full Check-up"}</option><option value="{labels["other"]}">{labels["other"]}</option>'
    flex_opts = "".join(f'<option>{x}</option>' for x in labels["flex_opts"])
    return f"""<section class="section"><div class="container">
<p class="eyebrow">{"طلب حجز سريع" if lang == "ar" else "Quick booking request"}</p>
<h1>{labels["title"]}</h1><p class="lead">{labels["lead"]}</p>
<div class="contact-cards">
<div class="card"><h3>{"الخط الساخن" if lang == "ar" else "Hotline"}</h3><p>{"اتصل على 15669 للتواصل مع فريق الاستقبال وحجز الفحص المناسب." if lang == "ar" else "Call 15669 to reach the reception team and book the right scan."}</p><p><a class="btn" href="tel:{SITE["hotline"]}">{labels.get("call", "Call")} 15669</a></p></div>
<div class="card"><h3>WhatsApp</h3><p>{"أرسل طلبك أو تقرير الطبيب على واتساب وسنساعدك في اختيار التحضير الصحيح." if lang == "ar" else "Send your request or your doctor's referral on WhatsApp and we will help you choose the right preparation."}</p><p><a class="btn btn-whatsapp" href="https://wa.me/{SITE["phone_intl"]}">WhatsApp</a></p></div>
<div class="card"><h3>{S[lang]["directions"]}</h3><p>{SITE["address_ar"] if lang == "ar" else SITE["address_en"]}</p><p><a class="btn btn-outline" href="{SITE["maps_link"]}" target="_blank" rel="noopener">{S[lang]["directions"]}</a></p></div>
</div>
<form class="form" id="booking-form" name="ds_booking_ar" data-lang="{lang}" novalidate>
<p class="placeholder-note">{labels["privacy"]} · {"متاح ٢٤/٧ · تأكيد عبر واتساب" if lang == "ar" else "Available 24/7 · Confirmation via WhatsApp"}</p>
<label for="f-name">{labels["name"]}</label><input id="f-name" name="name" type="text" autocomplete="name" required>
<label for="f-mobile">{labels["mobile"]}</label><input id="f-mobile" name="mobile" type="tel" autocomplete="tel" placeholder="01xxxxxxxxx" required>
<label for="f-exam">{labels["exam"]}</label><select id="f-exam" name="exam" required><option value="">{labels["choose"]}</option>{exam_opts}</select>
<div class="row"><div><label for="f-day">{labels["day"]}</label><input id="f-day" name="day" type="date" required></div>
<div><label for="f-hour">{labels["hour"]}</label><input id="f-hour" name="hour" type="time" required></div></div>
<label for="f-flex">{labels["flex"]}</label><select id="f-flex" name="flexibility">{flex_opts}</select>
<label for="f-notes">{labels["notes"]}</label><textarea id="f-notes" name="notes" rows="3"></textarea>
<p class="form-error" id="form-error" role="alert"></p>
<button class="btn" type="submit">{labels["submit"]}</button>
<div class="form-ok" id="form-ok">{labels["ok"]}</div>
</form>
</div></section>"""


def preps_index_body(lang, p):
    t = S[lang]
    cards = ""
    for i, e in enumerate(EXAMS):
        prep = e["prep_ar"] if lang == "ar" else e["prep_en"]
        cards += f"""<article class="card"><div class="exam-visual{["", " v2", " v3"][i % 3]}" aria-hidden="true">{e["code"]}</div>
<h3>{exam_name(e, lang)}</h3><p>{prep[0]}</p>
<a class="more" href="{prep_url(e, lang, p)}">{t["prep_link"]}</a></article>"""
    return f"""<section class="section"><div class="container">
<p class="eyebrow">{"الفحوصات والتحضيرات" if lang == "ar" else "Exams & preparations"}</p>
<h1>{"تحضيرات الفحوصات" if lang == "ar" else "Exam Preparations"}</h1>
<p class="lead">{"قبل كل فحص، اعرف التحضير المطلوب حتى تكون النتيجة دقيقة. اختر الفحص لعرض تعليماته الكاملة." if lang == "ar" else "Before each exam, know the preparation needed so the result is accurate. Choose an exam to see its full instructions."}</p>
<div class="grid">{cards}</div></div></section>"""


def prep_detail_body(lang, p, e):
    t = S[lang]
    prep = e["prep_ar"] if lang == "ar" else e["prep_en"]
    items = "".join(f"<li>{x}</li>" for x in prep)
    back = p + ("ar/exams-preparations-ar/" if lang == "ar" else "exams-preparations/")
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    return f"""<section class="section"><div class="container">
<p><a href="{back}">{t["back_preps"]}</a></p>
<p class="eyebrow">{"التحضير" if lang == "ar" else "Preparation"}</p>
<h1>{"تحضير: " if lang == "ar" else "Preparation: "}{exam_name(e, lang)}</h1>
<p class="lead">{e["desc_ar"] if lang == "ar" else e["desc_en"]}</p>
<h2>{t["prep_title"]}</h2><ul class="checklist">{items}</ul>
<div class="note"><p>{"إذا لم تكن متأكداً من أي نقطة، اتصل على 15669 أو راسلنا واتساب قبل موعدك." if lang == "ar" else "If you are unsure about any point, call 15669 or message us on WhatsApp before your appointment."}</p></div>
<p><a class="btn" href="{book}">{t["book_now"]}</a> <a class="btn btn-outline" href="{service_url(e, lang, p)}">{t["details_link"]}</a></p>
</div></section>"""


def service_body(lang, p, e):
    t = S[lang]
    uses = e["uses_ar"] if lang == "ar" else e["uses_en"]
    items = "".join(f"<li>{x}</li>" for x in uses)
    book = p + ("ar/book-appointment-ar/" if lang == "ar" else "book-appointment/")
    home = p + ("" if lang == "en" else "ar/")
    return f"""<section class="section"><div class="container">
<p><a href="{home}">{t["back_exams"]}</a></p>
<p class="eyebrow">{e["code"]}</p>
<h1>{exam_name(e, lang)}</h1>
<p class="lead">{e["desc_ar"] if lang == "ar" else e["desc_en"]}</p>
<div class="exam-visual" style="max-width:420px" aria-hidden="true">{e["code"]}</div>
<h2 style="margin-top:28px">{t["uses_title"]}</h2><ul class="checklist">{items}</ul>
<p><a class="btn" href="{book}">{t["book_now"]}</a> <a class="btn btn-outline" href="{prep_url(e, lang, p)}">{t["prep_link"]}</a></p>
</div></section>"""

# ---------------------------------------------------------------- page list
def pages():
    """Return list of (out_path, lang, active, title, desc, body, counterpart_out)."""
    out = []

    def add(out_path, lang, active, title, desc, body, counterpart):
        out.append((out_path, lang, active, title, desc, body, counterpart))

    for lang in ("en", "ar"):
        t = S[lang]
        pre = "ar/" if lang == "ar" else ""
        suf = "-ar" if lang == "ar" else ""
        other = "ar" if lang == "en" else "en"
        opre = "ar/" if lang == "en" else ""   # prefix of the *counterpart* language
        osuf = "-ar" if lang == "en" else ""   # suffix of the *counterpart* language

        def P(out_path):
            return prefix_for(out_path)

        # Home
        add(f"{pre}index.html", lang, "home",
            "Dokki Scan" if lang == "en" else "دقي سكان",
            t["tagline"], home_body(lang, P(f"{pre}index.html")),
            f"{opre}index.html")
        # Core pages
        core = [
            (f"why-dokki-scan{suf}", "why", "لماذا دقي سكان؟" if lang == "ar" else "Why Dokki Scan?", t["trust_text"], why_body(lang, P(f"{pre}why-dokki-scan{suf}/index.html"))),
            (f"full-check-up{suf}", "checkup", "الفحص الشامل" if lang == "ar" else "Full Check-up", t["checkup_text"], checkup_body(lang, P(f"{pre}full-check-up{suf}/index.html"))),
            (f"my-results{suf}", "results", "نتائجي" if lang == "ar" else "My Results", "Reports by WhatsApp or email" if lang == "en" else "تقارير عبر واتساب أو البريد الإلكتروني", results_body(lang, P(f"{pre}my-results{suf}/index.html"))),
            (f"find-us{suf}", "find", "اعثر علينا" if lang == "ar" else "Find Us", SITE["address_en"] if lang == "en" else SITE["address_ar"], findus_body(lang, P(f"{pre}find-us{suf}/index.html"))),
            (f"blog{suf}", "blog", "المدونة" if lang == "ar" else "Blog", "Short articles explaining imaging tests" if lang == "en" else "مقالات قصيرة تشرح فحوصات الأشعة", blog_index_body(lang, P(f"{pre}blog{suf}/index.html"))),
            (f"book-appointment{suf}", "book", "احجز موعداً" if lang == "ar" else "Book Appointment", "Book your scan — confirmation via WhatsApp" if lang == "en" else "احجز فحصك — التأكيد عبر واتساب", book_body(lang, P(f"{pre}book-appointment{suf}/index.html"))),
            (f"exams-preparations{suf}", "preps", "تحضيرات الفحوصات" if lang == "ar" else "Exam Preparations", t["exams_sub"], preps_index_body(lang, P(f"{pre}exams-preparations{suf}/index.html"))),
        ]
        for slug, active, title, desc, body in core:
            add(f"{pre}{slug}/index.html", lang, active, title, desc, body,
                f"{opre}{slug.replace('-ar', '') if lang == 'ar' else slug + '-ar'}/index.html" if slug not in (f"blog{suf}",) else f"{opre}blog{osuf}/index.html")
        # Blog articles
        for b in BLOG:
            slug = b["slug_ar"] if lang == "ar" else b["slug_en"]
            oslug = b["slug_en"] if lang == "ar" else b["slug_ar"]
            title = b["title_ar"] if lang == "ar" else b["title_en"]
            summ = b["summary_ar"] if lang == "ar" else b["summary_en"]
            out_path = f"{pre}blog{suf}/{slug}/index.html"
            add(out_path, lang, "blog", title, summ,
                article_body(lang, P(out_path), b),
                f"{opre}blog{osuf}/{oslug}/index.html")
        # Service pages
        for e in EXAMS:
            slug = exam_slug(e, lang)
            oslug = exam_slug(e, other)
            out_path = f"{pre}{slug}/index.html"
            add(out_path, lang, "preps", exam_name(e, lang),
                e["desc_ar"] if lang == "ar" else e["desc_en"],
                service_body(lang, P(out_path), e), f"{opre}{oslug}/index.html")
        # Preparation detail pages
        for e in EXAMS:
            slug = prep_slug(e, lang)
            oslug = prep_slug(e, other)
            out_path = f"{pre}exams-preparations{suf}/{slug}/index.html"
            add(out_path, lang, "preps",
                ("تحضير: " if lang == "ar" else "Preparation: ") + exam_name(e, lang),
                (e["prep_ar"] if lang == "ar" else e["prep_en"])[0],
                prep_detail_body(lang, P(out_path), e),
                f"{opre}exams-preparations{osuf}/{oslug}/index.html")
    return out


def build():
    all_pages = pages()
    written = []
    for out_path, lang, active, title, desc, body, counterpart in all_pages:
        html = render(lang, out_path, title, desc, body, active, counterpart)
        dest = ROOT / out_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        written.append(out_path)

    # 404 page (English, root)
    notfound = render("en", "404.html", "Page not found", "This page does not exist.",
                      '<section class="section"><div class="container"><h1>Page not found</h1>'
                      '<p class="lead">The page you are looking for does not exist or was moved.</p>'
                      '<p><a class="btn" href="./">Back to home</a></p></div></section>',
                      "", "index.html")
    (ROOT / "404.html").write_text(notfound, encoding="utf-8")
    written.append("404.html")

    # robots.txt + sitemap.xml
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n", encoding="utf-8")
    urls = []
    for out_path, *_ in all_pages:
        loc = BASE + "/" + dir_url(out_path)
        urls.append(f"  <url><loc>{loc}</loc></url>")
    urls.append(f"  <url><loc>{BASE}/404.html</loc></url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    return written


def check(written):
    """Verify every internal link in generated HTML points to an existing file."""
    files = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()
             and ".git" not in p.parts}
    problems = []
    href_re = re.compile(r'(?:href|src)="([^"]+)"')
    for rel in written:
        html = (ROOT / rel).read_text(encoding="utf-8")
        base = Path(rel).parent
        for m in href_re.finditer(html):
            u = m.group(1)
            if u.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                continue
            u = u.split("#")[0].split("?")[0]
            if not u or u == "./":
                u = "index.html"
            target = os.path.normpath(base / u) if not u.startswith("/") else u.lstrip("/")
            # directory URL (no file extension) -> index.html
            if not os.path.splitext(target)[1]:
                target = os.path.normpath(target + "/index.html")
            if target not in files:
                problems.append(f"{rel} -> {u} (missing {target})")
    return problems


if __name__ == "__main__":
    written = build()
    print(f"Generated {len(written)} HTML pages (+ sitemap.xml, robots.txt).")
    for w in sorted(written):
        print("  " + w)
    if "--check" in sys.argv:
        problems = check(written)
        if problems:
            print(f"\nBROKEN LINKS: {len(problems)}")
            for p in problems:
                print("  " + p)
            sys.exit(1)
        print("\nLink check OK: no broken internal links.")
