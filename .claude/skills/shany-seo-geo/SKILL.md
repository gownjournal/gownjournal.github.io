---
name: shany-seo-geo
description: Search and AI-answer optimisation for the Shany Sasson / Lace & Love bridal properties — shanysasson.com (Wix), shany-sasson-wedding-dresses.com (Shopify), The Gown Journal, and מגזין הכלה. Use this whenever you write, edit or review a page, landing page, product page, blog post or collection for any of these sites, in Hebrew or English; whenever structured data, JSON-LD, schema, meta tags, page titles, og:image, sitemaps or robots.txt come up; whenever the user asks about Google rankings, local search, Google Business Profile, being found, being cited by ChatGPT or Perplexity, SEO or GEO; and whenever a page is about to be published or handed over. Also use it before quoting a customer review anywhere, because the review-integrity rules live here.
---

# SEO and GEO for the Shany Sasson properties

Two audiences read these pages. A bride searching Google, and a language model
answering "where do I find a boho wedding dress in Israel". They reward
overlapping but not identical things, and this skill covers both.

Everything factual about the business — name, address, phone, profile links —
lives in `references/brand-facts.md`. Read it before writing anything that
states a fact about the studio. Getting an address wrong on a landing page
sends a bride to the wrong building; there is no cheaper mistake to avoid.

## The order of work

1. Read `references/brand-facts.md` for the canonical business data.
2. Write or edit the page.
3. Apply the title and description rules below.
4. Add JSON-LD from `references/schema-templates.md`.
5. Run `scripts/audit.mjs` and fix what it reports.
6. Walk the integrity gate below before anything is published.

## Titles and descriptions

A `<title>` is the headline in search results, not a name badge. Lead with what
someone types, then the brand.

- Hebrew: `שמלות כלה בוהו בהוד השרון · שני ששון`
- English: `Made-to-Measure Boho Wedding Dresses · Lace & Love`

Keep the title near 60 characters and the description between 70 and 160. The
description is advertising copy that happens to live in a meta tag — write it to
earn the click, not to list keywords. State what the page offers and where.

Hebrew pages need `lang="he" dir="rtl"`, and every page needs an `og:image`.
Skipping og:image is the most expensive omission on this brand's pages: these
links travel by WhatsApp, and a link with no preview image reads as spam.

## What GEO actually needs

Full findings and sources are in `references/geo-2026.md`. The short version,
because two widely repeated beliefs are wrong:

**Structured data on the page moves AI citation more than llms.txt does.** As of
2026 no major engine consumes llms.txt at inference time. It is a navigation
convention, not an access control and not a ranking input. Spend the effort on
JSON-LD.

**robots.txt is the real lever for AI access, and the bots split by purpose.**
GPTBot trains; OAI-SearchBot, Claude-SearchBot and PerplexityBot build the
search indexes that produce citations. Blocking training does not have to cost
citations — but blocking the search bots does.

Three things make a passage quotable by a model, and they cost nothing:

- **Ask the reader's question as the heading.** An H2 phrased as the question a
  bride would actually type lines up with the prompt a model is answering.
- **Be specific and attributable.** Concrete figures, named sources and direct
  quotes get picked up; vague superlatives do not.
- **Name the entity explicitly.** "הסטודיו של שני ששון בהוד השרון" is
  resolvable. "אנחנו" is not.

## Local search

Local ranking weight sits mostly outside any page: the Google Business Profile
is roughly a third of it, review signals a sixth, citation consistency a
fourteenth. A page can be perfect and still lose to a competitor with a better
profile.

Citation consistency is the part that silently rots. Every directory carrying
the business is a separate record with its own edit screen, and updating Google
updates none of the others. `references/brand-facts.md` lists the known ones and
their state. When the address, phone or name changes, that list is the checklist
— not an afterthought.

## The integrity gate

These are not style preferences. Each one is either a Google policy violation or
a claim about a real person that the business cannot back up.

**Never invent an `aggregateRating`.** Not an estimate, not a placeholder, not
"about 5 stars". Publish the rating only when the real count and average are in
hand. Fabricated ratings are a structured-data violation and can cost every rich
result the site has.

**Schema text must match the page text.** If `FAQPage` says one thing and the
page says another, that is cloaking. Assert the match in code rather than
trusting a careful read — `scripts/audit.mjs` does this.

**Quote reviews verbatim.** Trim with ellipses, never reword, and attribute to
the name and year as published. A reworded review is a fabricated testimonial
about a named person. If the source cannot be produced on request, it does not
go on the page.

**Know where review markup is allowed.** Google has not shown review stars for
self-serving `LocalBusiness` or `Organization` markup since 2019. Reviews
attached to a specific `Service` or `Product` remain eligible. Marking up the
business itself is not a violation and still feeds AI answers — it just will not
produce stars, so do not promise the user that it will.

**One canonical per page.** A page reachable at two addresses without a
canonical splits its own ranking.

## Running the audit

```bash
node scripts/audit.mjs path/to/page.html
```

It reports horizontal overflow at desktop and phone widths, heading structure,
missing alt text, JSON-LD validity, FAQ schema drift against the rendered
answers, missing og:image, and title and description lengths. It needs Playwright
and Chromium; in this environment Chromium is at
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.

The audit checks what a machine can check. It cannot tell you whether the copy
is worth reading, whether a claim is true, or whether the address is current.
