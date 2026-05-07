# WordPress Deployment Guide

How to migrate this static site into WordPress on the existing fasmedicalsummitrcm.com.

## Why migrate to WordPress

- **FAS already has a WP team.** The existing site is WordPress, so they have hosting, login credentials, and someone who knows how to update content.
- **CMS for the blog.** The 10 blog posts will eventually need real content — WP makes that easy for non-technical admins.
- **SEO continuity.** Existing WP plugins (Yoast, RankMath) will pick up the meta tags we've already written.
- **Form backend included.** Contact Form 7 or WPForms handles consultation submissions.

## Approach: Custom Theme Conversion

The cleanest migration is to convert this static HTML into a custom WordPress theme. This is **$3-8K and 2-3 weeks** with a competent WP developer.

### Theme structure

```
wp-content/themes/fas-medical-summit/
├── style.css                  (theme metadata header + main stylesheet)
├── functions.php              (theme setup, enqueue scripts, custom post types)
├── header.php                 (extracted from <head> + nav of any page)
├── footer.php                 (extracted footer of any page)
├── index.html → index.php     (homepage template)
├── front-page.php             (alias for homepage)
├── page.php                   (default page template)
├── single.php                 (default blog post template)
├── single-service.php         (custom post type: service detail)
├── single-specialty.php       (custom post type: specialty detail)
├── archive-service.php        (services listing)
├── archive-specialty.php      (specialties listing)
├── page-templates/
│   ├── about.php
│   ├── contact.php
│   ├── insights.php           (blog landing)
│   ├── process.php
│   ├── why-fas.php
│   ├── privacy.php
│   ├── terms.php
│   └── hipaa.php
└── assets/
    ├── images/
    └── fonts/                 (optional — currently using Google Fonts)
```

### Migration steps

1. **Extract the shared shell** from any HTML file:
   - Everything from `<!DOCTYPE html>` through `</nav>` → `header.php`
   - Everything from `<footer>` through `</html>` → `footer.php`
   - Replace at the top of each page template:
     ```php
     <?php get_header(); ?>
     <!-- page content -->
     <?php get_footer(); ?>
     ```

2. **Convert the homepage** (`index.html` → `front-page.php`):
   - Most sections can stay as static HTML inside the PHP file
   - The Specialties grid should pull from custom post type `specialty`
   - The Services grid should pull from custom post type `service`
   - The Blog preview should pull from default `post` type

3. **Create custom post types** in `functions.php`:
   ```php
   register_post_type('service', [
     'public' => true,
     'has_archive' => true,
     'rewrite' => ['slug' => 'services'],
     'supports' => ['title', 'editor', 'thumbnail', 'custom-fields'],
     'menu_icon' => 'dashicons-clipboard',
   ]);

   register_post_type('specialty', [
     'public' => true,
     'has_archive' => true,
     'rewrite' => ['slug' => 'specialties'],
     'supports' => ['title', 'editor', 'thumbnail', 'custom-fields'],
     'menu_icon' => 'dashicons-heart',
   ]);
   ```

4. **Migrate the 9 service pages → service CPT entries.** Each existing HTML file becomes a service post in WP admin. Body content goes into the editor; meta data (icon, number, intro) into ACF (Advanced Custom Fields) fields.

5. **Migrate the 6 specialty pages → specialty CPT entries.** Same pattern.

6. **Migrate the 10 blog topics → standard `post` entries.** The SVG illustrations can either:
   - Stay as inline SVG in the post template
   - Be converted to PNG/JPG images and assigned via Featured Image
   - Be stored as a custom field `illustration_svg` (string)

7. **Wire up Contact Form 7 or WPForms** for the consultation forms:
   - Replace the existing `<form>` with the CF7 / WPForms shortcode
   - Configure email recipients to info@fasmedicalsummitrcm.com
   - Keep the honeypot anti-spam logic (or rely on the plugin's spam filter)

8. **Install SEO plugin** (Yoast or RankMath):
   - The hand-written meta titles, descriptions, OG tags, and canonicals will get picked up automatically
   - JSON-LD structured data should remain in `<head>` (the SEO plugin will warn but won't conflict)

9. **Configure permalinks** to match the existing URL structure:
   - `/` → homepage
   - `/services/{slug}/` → service detail
   - `/specialties/{slug}/` → specialty detail
   - `/blog/` → blog landing (insights.html)
   - `/blog/{slug}/` → individual articles
   - `/about/`, `/contact/`, `/process/`, `/why-fas/`, `/privacy/`, `/terms/`, `/hipaa/`

10. **Set up redirects** if URLs change:
    - The existing fasmedicalsummitrcm.com may have URLs like `/services/medical-coding/` that don't exactly match this site's `/services/charge-capture-coding.html`
    - Use a Redirection plugin to map old URLs → new ones, preserving SEO equity

## Plugins recommended

| Plugin | Purpose |
|---|---|
| **Yoast SEO** or **Rank Math** | SEO meta, sitemaps, structured data |
| **Contact Form 7** or **WPForms** | Form handling |
| **Advanced Custom Fields (ACF)** | Custom fields for service/specialty meta |
| **Redirection** | URL redirects from old site |
| **Wordfence** | Security (HIPAA-adjacent business — security matters) |
| **WP Rocket** or **W3 Total Cache** | Performance |
| **UpdraftPlus** | Automated backups |

## Plugins to AVOID

- **Page builders (Elementor, Divi, WPBakery).** This site has hand-tuned 3D animations, mouse-tracking, and intricate CSS that page builders will mangle. Keep the theme code-based.
- **Heavy "all-in-one" themes (Avada, Salient, etc.).** Same problem. Stick with a custom theme.

## Alternative: lighter approach

If FAS doesn't want a full theme conversion, the static HTML can be embedded into WordPress via:

- **Custom HTML blocks** in Gutenberg — paste each page's body HTML into a custom HTML block on a WP page. Forms still work via Formspree.
- **Tradeoff:** No CMS for blog. No easy edits for FAS team. But can be done in a few hours instead of weeks.

## Hosting recommendations

The existing fasmedicalsummitrcm.com is on shared WordPress hosting. For a production site that handles HIPAA-adjacent inquiries:

- **Kinsta** — managed WP, ~$35/mo, fast
- **WP Engine** — managed WP, ~$30/mo, established
- **Pressable** — managed WP, ~$25/mo, Automattic-owned
- **SiteGround** — budget option, ~$15/mo (lower performance)

Avoid GoDaddy / Bluehost shared hosting for this kind of business site — slow, oversold, frequent issues.

## SSL / Security notes

- **Force HTTPS** on every page. WordPress + a hosting provider above will do this automatically.
- **Don't store PHI** in WordPress. Consultation forms should NOT include "describe your medical condition" fields. Anything HIPAA-touching should redirect to a secure portal — not WP.
- **WAF** (Web Application Firewall) — Cloudflare Pro tier or Wordfence Premium.

## Estimated total cost (one-time)

| Item | Cost |
|---|---|
| WP developer (custom theme conversion) | $3,000 - $8,000 |
| ACF Pro license (one-time) | $50 |
| Premium plugins (Yoast SEO Premium, WPForms Pro, etc.) | $200/yr |
| Quality stock photos (10-15) | $100-300 |
| Custom photography (optional) | $1,500-5,000 |
| **Total** | **~$5K - $15K** |

## Estimated ongoing cost

| Item | Monthly |
|---|---|
| Managed WP hosting | $30-50 |
| Premium plugin renewals | ~$20 |
| **Total** | **~$50-70/mo** |

## Timeline

- **Week 1:** Theme conversion (header, footer, homepage, basic CPTs)
- **Week 2:** Service and specialty CPT migration, blog migration
- **Week 3:** Forms, SEO, redirects, testing, content review
- **Week 4 (buffer):** Bug fixes, performance tuning, launch

Move slowly. The current site has SEO equity that a botched migration could lose. Use a staging environment first.
