---
name: bridal-competitor-intel
description: Competitor and market research for the Shany Sasson bridal studio — who ranks for the searches brides make, what those studios put on their pages, how they position and price, and which search terms nobody has claimed. Use whenever the user asks about competitors, the market, what others are doing, who ranks for a term, whether a page idea is worth building, which terms to target next, or asks for research before writing a page. Also use when deciding what landing page to build, since the answer depends on what is already taken.
---

# Competitor research for a bridal studio

The useful question is rarely "who are my competitors". It is "which searches
does a bride make that somebody else is answering and I am not". That is
answerable, repeatable, and it points at work.

## What you can and cannot know

Be strict about this, because the gap between the two is where confident
nonsense comes from.

**You cannot see a competitor's traffic, conversion rate or revenue.** Nobody
outside the business can. So "their best page" is not a claim you can make.
What you can observe is which pages rank for which searches, and ranking is a
defensible proxy for organic success — but say which one you mean.

**You usually cannot fetch a competitor's site.** Outbound access is blocked
for most domains here, so work from what search returns: titles, URLs,
descriptions and snippets. That is genuinely informative — a title is a
positioning statement and a URL structure is a site architecture — but it is
not the page. **Never describe how a competitor's page looks unless you have
actually seen it.**

**Search results lag.** They are a snapshot of an index, not of today. A change
made this week may not show. Date every finding.

## The method

1. **Search the way a bride searches.** Not "bridal studios Israel" but the
   phrases someone types with a wedding coming: style, body type, city, price,
   fabric, sleeve. Run several; one query gives you one slice of the market.

2. **Read the titles and URLs as architecture.** This is where the real finding
   usually is. A studio holding eight URLs for eight different searches is
   running a different strategy from one holding a homepage, and you can see
   that without ever loading a page.

3. **Note each competitor's stated differentiator.** It is almost always in the
   title: modest, all sizes, couture, one fixed price, a city. A crowded axis
   is expensive to compete on; an empty one is an opening.

4. **Check coverage.** Which target terms have a page here and which do not:

   ```bash
   node .claude/skills/bridal-competitor-intel/scripts/coverage.mjs
   ```

5. **Record it.** Add what you found to `references/competitors.md` and a dated
   entry to `references/findings.md`, so the next run compares against this one
   instead of starting over. Research that is not written down gets redone.

## Reporting

Lead with the finding that changes what to build next, not with a roster of
competitors. "Nobody holds your city term" is worth more than nine studio
descriptions.

Separate what you observed from what you infer. "Six of their page titles carry
the same price" is an observation. "They compete on price" is an inference, and
a sound one, but the reader deserves to see which is which.

When a finding contradicts a decision the owner already made, say it once,
plainly, with the evidence — then let it go. They own the business.

## What not to do

**Do not copy competitor copy.** Their phrasing is theirs, and a page assembled
from competitors reads like every other page in the category, which is the
opposite of useful.

**Do not treat a gap as automatically worth filling.** Sometimes nobody holds a
term because nobody searches it. Weigh whether the studio can genuinely serve
what the term promises — a page for a service the studio does not offer costs
more than the traffic is worth.

**Do not invent numbers.** No made-up search volumes, no estimated traffic, no
invented market share. If a figure matters and you do not have it, say what it
would take to get it.
