# Dokki Scan — Static Website Rebuild

A pure static HTML/CSS/JS rebuild of the **structure and public facts** of
[dokki-scan.com](https://dokki-scan.com/ar/) (reverse-engineered 2026-11-24),
made to be hosted on GitHub Pages. No WordPress, no PHP, no build step.

## What this is — and is not

- **Structure + facts only.** Page map, exam categories, preparation lists,
  booking fields, contact details and opening hours mirror the original site.
- **Original text.** All copy was rewritten in short original Arabic/English
  wording; no marketing text was copied verbatim from the original site.
- **No copied photos.** Exam visuals are CSS gradients with the exam code
  (XR / CT / MRI …). The only external media is the centre's own public
  YouTube video (`xV0NcnKyXdI`) embedded on the home page, plus a public
  Google Maps embed for the address.
- **No tracking.** The original site's GA4/GTM IDs were deliberately *not*
  copied — add your own analytics if you want them.

## Structure

```
build.py            # generator: one template + data.json -> all pages
data.json           # exams (11), blog articles (5), site facts
assets/css/style.css
assets/js/main.js   # mobile menu, counters, booking -> WhatsApp
index.html          # English home (generated)
ar/index.html       # Arabic home (generated)
mri-examination/ ...            # 11 English service pages
ar/mri-examination-ar/ ...     # 11 Arabic service pages
exams-preparations/ ...         # English prep index + 11 prep pages
ar/exams-preparations-ar/ ...  # Arabic prep index + 11 prep pages
blog/ ...           # English blog index + 5 articles
ar/blog-ar/ ...     # Arabic blog index + 5 articles
why-dokki-scan/ full-check-up/ my-results/ find-us/ book-appointment/
  (+ Arabic -ar mirrors under ar/)
404.html  sitemap.xml  robots.txt
.github/workflows/deploy-pages.yml
```

Total: **70 content pages** (35 English + 35 Arabic) + `404.html`.

## Booking behaviour

Same as the original: the booking form (`ds_booking_ar`) does **not** book a
slot. It validates name / mobile / exam / day / hour, then opens WhatsApp
(`wa.me/201000010144`) with a prefilled Arabic/English message. Reception
confirms manually. The "My Results" page is likewise **not** a login portal:
reports arrive by WhatsApp/email when ready.

## Build & preview

```bash
python3 build.py --check   # regenerate everything + verify internal links
python3 -m http.server 8000
# open http://localhost:8000/  (and /ar/ for Arabic)
```

All links are **relative** (`../assets/...`), so the site works both at a
domain root and under a GitHub Pages subpath (`/<repo-name>/`).

## Deploy to GitHub Pages

1. Create a repo (e.g. `dokki-scan-website`) and push this folder.
2. Settings → Pages → Source: **GitHub Actions**.
3. The workflow in `.github/workflows/deploy-pages.yml` deploys on every
   push to `main`.
4. If your repo name differs, update `base_url` in `data.json` and rebuild
   so `sitemap.xml` points at the right place.

## Facts used (verified 2026-11-24)

Dokki Scan, 92 Saridar Tower, El Tahrir St, Dokki, Giza, Egypt · Hotline
15669 · WhatsApp/mobile 01000010144 · info@dokki-scan.com · Open 24/7 ·
30+ years · 3-stage report review · Reports via WhatsApp/email.
