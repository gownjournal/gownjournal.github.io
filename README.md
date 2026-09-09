# The Gown Journal

An independent, English-language editorial site about wedding dresses. Static, built with Eleventy 3, hosted for free.

## What is here

- 13 long-form guides in `src/posts/` (1,100 to 1,700 words each), organised into six topics: silhouettes, fabrics and lace, style, planning, accessories, care
- Topic landing pages generated automatically from `src/_data/categories.json`
- Home, All guides, About, Editorial policy, Contact, Privacy, 404
- `sitemap.xml`, `feed.xml` (RSS), `robots.txt`, `llms.txt`
- Structured data on every page: Organization, WebSite, and on guides Article + BreadcrumbList + FAQPage
- Open Graph and Twitter cards with a default image (`src/img/og-default.png`)
- Per-guide table of contents, reading time, related guides, author box

## Local work

```bash
npm install
npm run serve
```

Open http://localhost:8080. Edits rebuild instantly.

One-off build (writes `_site/`):

```bash
npm run build
```

## Adding a guide

Create `src/posts/<slug>.md`. The filename becomes the URL: `/guides/<slug>/`.

```md
---
title: "Guide title"
description: "One or two sentences, 140 to 170 characters, shown in search results and on cards."
date: 2026-09-20
category: planning
faq:
  - q: "A question readers ask?"
    a: "A two or three sentence answer."
---

Body in Markdown. Use ## for sections (they feed the table of contents), tables where useful, and end with a short <div class="note"> pointing to two related guides.
```

`category` must be one of the slugs in `src/_data/categories.json`: silhouettes, fabrics, style, planning, accessories, care. `faq` is optional; if present it renders at the end and becomes FAQPage schema. Add `updated: 2026-10-01` when you revise a guide and it will show on the page and in the sitemap.

To add a custom social image for a guide, put a 1200x630 PNG in `src/img/` and set `image: /img/<name>.png` in the front matter.

## Site settings

`src/_data/site.json`: name, tagline, description, contact email, and `url`. **Update `url` after the first deploy.** Canonical links, the sitemap, the RSS feed and all schema are built from it.

## House style

- Plain English, British spelling, no hype, no exclamation marks
- No em dashes or en dashes (use commas, full stops, colons, parentheses)
- No prices, no price ranges, no brand or salon names
- Every guide is checked by someone who works with dresses before it is published

A quick check for dashes and banned phrases:

```bash
grep -rnP "[\x{2014}\x{2013}]|\bdelve\b|\belevate\b|\bleverage\b|serves as|a testament|dream dress|big day|special day|stunning|breathtaking" src/posts src/*.md src/*.njk
```

Empty output means clean.

## Publishing for free (free subdomain)

### Option 1: GitHub Pages, `<name>.github.io`

1. Create a GitHub account if you do not have one.
2. Create a public repository named exactly `<username>.github.io` (this gives the shortest URL, with no sub-folder).
3. From this folder:

```bash
git remote add origin https://github.com/<username>/<username>.github.io.git
git push -u origin main
```

4. In the repository: Settings, Pages, Build and deployment, Source: **GitHub Actions**.
5. The workflow in `.github/workflows/deploy.yml` builds and publishes on every push. The site is live at `https://<username>.github.io` within a couple of minutes.
6. Set `url` in `src/_data/site.json` to that address and push again.

### Option 2: Netlify Drop, `<name>.netlify.app`, no git needed

1. Run `npm run build`.
2. Go to app.netlify.com/drop and drag the `_site` folder onto the page.
3. Rename the site under Site settings, Change site name. Update `url` in `site.json`, rebuild, drop again.

### Option 3: Cloudflare Pages, `<name>.pages.dev`

Connect the repository at dash.cloudflare.com under Pages. Build command `npm run build`, output directory `_site`.

## After publishing

- Add the site to Google Search Console and submit `/sitemap.xml`.
- Set the real contact email in `site.json` (the placeholder is `hello@gownjournal.example`).
- Consider a named author with a short bio on the About page. Search engines and readers both trust a named person more than an editorial team; the schema is ready for it (change `author` in `base.njk` from Organization to Person).
- A custom domain can be attached to any of the three hosts for free; only the domain itself costs money.
