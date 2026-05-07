# FAS Medical Summit — Premium Website

A custom-built marketing website for **FAS Medical Summit RCM**, a medical billing & revenue cycle management company in Frisco, Texas serving surgical specialty practices.

## Quick start

The site is **24 static HTML files**, fully self-contained. Each page has all CSS and JavaScript inlined — no build step, no dependencies, no external runtime.

To preview locally:

```bash
# Just open in any browser:
open index.html

# Or run a simple local server (recommended for testing):
python3 -m http.server 8000
# then visit http://localhost:8000
```

To deploy:
- **Easiest:** Drag the entire folder onto Netlify or Cloudflare Pages
- **WordPress:** See `docs/WORDPRESS_DEPLOYMENT.md`

## Project structure

```
fas-website/
├── index.html              # Homepage (~227 KB — large because everything inlined)
├── about.html              # Company story & leadership
├── contact.html            # Consultation request form
├── insights.html           # Blog landing (10 linked articles with SVG illustrations)
├── blog-*.html             # Individual blog article pages
├── process.html            # 8-stage onboarding process
├── why-fas.html            # FAS vs generic billers comparison
├── privacy.html            # Privacy Policy (legal)
├── terms.html              # Terms & Conditions (legal)
├── hipaa.html              # HIPAA Notice (legal)
│
├── services/               # 9 service detail pages
│   ├── patient-onboarding.html
│   ├── charge-capture-coding.html
│   ├── claims-submission.html
│   ├── payment-posting.html
│   ├── denial-management.html
│   ├── ar-follow-up.html
│   ├── patient-billing.html
│   ├── reporting-analytics.html
│   └── credentialing.html
│
├── specialties/            # 6 specialty detail pages
│   ├── ambulatory-surgery.html
│   ├── anesthesiology.html
│   ├── pain-management.html
│   ├── cardiology.html
│   ├── emergency-medicine.html
│   └── family-practice.html
│
├── docs/                   # Documentation for development
│   ├── DESIGN_SYSTEM.md      # Colors, fonts, spacing — the visual language
│   ├── CONTENT_GUIDELINES.md # Tone, voice, what numbers to use
│   ├── WORDPRESS_DEPLOYMENT.md  # How to migrate to WordPress
│   └── PENDING_TASKS.md      # What still needs doing
│
├── assets/                 # (empty — for future images, og-image.png, etc.)
│
├── CLAUDE.md               # Context for Claude Code sessions
├── README.md               # This file
└── .gitignore
```

## Site features

- **24 fully-linked pages** with consistent nav, mobile menu, footer
- **Top contact strip** with click-to-call phone + click-to-email
- **3D Revenue Pipeline visualization** on homepage (6 cards showing the RCM stages)
- **3D interactive services grid** with mouse-tracking tilt + radial glow
- **3D dashboard mockup** in Why-FAS section (DENIAL_TREND, UNDERPAYMENT_RECOVERY, REVENUE_DASHBOARD)
- **3D platform/growth section** with floating cards (Client Growth, Integrations, Department Structure)
- **Practice Revenue Health Check** — 4-step interactive audit form with personalized leak estimate, fit score, and recovery potential
- **10 custom SVG blog illustrations** matching each article's topic, with linked article pages
- **Free Consultation form** with double-submit prevention + honeypot anti-spam
- **Per-page SEO** — meta titles, descriptions, OG tags, Twitter Cards, JSON-LD structured data
- **Full mobile responsive** with reduced-motion support

## Design language

- **Dark navy** (`#0A1220`) base with **warm gold** (`#C9A961`) accents and **cream** (`#F4EFE6`) text
- **Fraunces** serif for display, **Plus Jakarta Sans** for body, **JetBrains Mono** for technical labels
- Premium Apple-inspired aesthetic — see `docs/DESIGN_SYSTEM.md` for the full token reference

## What's verified vs illustrative

Every number on the site is either **verified canonical FAS data** or **clearly labeled "EXAMPLE"**. No fabricated live data, no untrue claims.

**Verified canonical metrics** (used freely in headlines):
- 25+ years experience (founded 2000)
- 450+ specialists on team
- $2.7B processed since 2022
- 96% first-pass acceptance rate
- 32-day average A/R
- 200+ active clients
- 50+ ongoing projects
- Up to 30% revenue growth for clients
- 3 departments: Medical Coding (150+), Transaction Processing (200+), A/R Management (100+)

**Clearly-labeled illustrative content** (in 3D mockups, all tagged "EXAMPLE"):
- Sample dashboard numbers (`$184,200`, `$142,860`, etc.)
- Sample chart trends
- Sample integration partner names

See `docs/CONTENT_GUIDELINES.md` for the full canonical data sheet and what to ask FAS to verify.

## Status

**Ready to launch except for:**

1. `og-image.png` — referenced in OG meta tags but file doesn't exist yet (1200×630 PNG needed)
2. Email notifications — consultation forms now store leads in private Vercel Blob records; add `RESEND_API_KEY` if owners want inbox notifications too
3. Real client logos / leadership photos — currently using anonymized placeholder names
4. Some service-page stats need owner verification (e.g., 78% IDR win rate, 67% appeal win rate, 94% prior auth approval)

See `docs/PENDING_TASKS.md` for the full launch checklist.

## Built with

- Pure HTML, CSS, and vanilla JavaScript
- Zero build step; one serverless dependency (`@vercel/blob`) for private lead storage
- Google Fonts (Fraunces, Plus Jakarta Sans, JetBrains Mono)
- Hand-coded SVG illustrations (no image files needed)
- ~2.4 MB total site weight

## License

Proprietary. Built for FAS Medical Summit RCM.
