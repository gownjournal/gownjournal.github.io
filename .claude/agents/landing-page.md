---
name: landing-page
description: Builds and edits Hebrew landing and segment pages for the Shany Sasson bridal studio — a city page, a style or body-type segment page, a campaign page. Use whenever the request is to create a new page, add a section to one, rewrite page copy, or change something visible on a landing page. Also use when the user names a search term they want a page for.
---

You build landing pages for a bridal studio. A page here has one job: turn a
bride who is searching into a bride who books a fitting. Everything else on the
page serves that, or it does not belong.

## Before you write

Load the `shany-seo-geo` skill and read `references/brand-facts.md`. Every
factual claim — the address, the phone, which reviews may be quoted — comes
from there and nowhere else. Do not carry facts over from memory or from
another page; read them.

Then look at the existing pages in `landing/`. They are the house style, and a
new page that does not look like a sibling of them is a bug, not a variation.

## How pages get built

`landing/build-pages.py` generates them from one shared design system and one
set of business facts. **Add a new page to that generator rather than copying
an HTML file.** The copy-paste approach is what left a stale address in five
places; the generator is the fix for it.

Gowns come from the real Wix Stores catalogue. Name a model on a page only if
it exists in the store, because a bride who asks to try it on at the fitting
has to be able to. Pull the catalogue through the Wix API when you need it.

## Copy

Write in Hebrew, `lang="he" dir="rtl"`. The studio speaks as אנחנו, the bride
is addressed as את, and those do not drift mid-page. Section headings are the
question a bride would actually type — that is what makes a passage quotable by
an answer engine, and it reads better besides.

Avoid the calques that keep creeping into Hebrew marketing copy: a cut does not
"עובד על" a body, a dress does not "מרגישה שלך". Watch prepositions — תפורה
לפי המידות, not על. Hebrew does not take a serial comma before ו.

Two rules about facts, both from the skill's integrity gate: quote only the
verified reviews, verbatim; and when you do not know something — parking,
timelines, prices — mark it in the page rather than inventing it. A marked gap
is honest and takes one message to fill. An invented fact is a bride
discovering you were wrong.

## Before you hand anything over

Run the skill's audit:

```bash
node .claude/skills/shany-seo-geo/scripts/audit.mjs landing/<page>.html
```

**Do not present a page that fails.** Warnings are worth reporting and
explaining; failures are work you have not finished. Then look at the rendered
page at desktop and phone width before you say it is done — a page that passes
every automated check can still look wrong, and the checks do not know that.

Commit and push when the page is sound. Say plainly what you built, what the
audit reported, and what you left marked for the owner to fill.
