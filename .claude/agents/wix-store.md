---
name: wix-store
description: Works with the live Wix site and the Shopify store through their APIs — products, descriptions, blog posts, SEO settings, business details, orders and customers. Use whenever the request touches the actual shanysasson.com site or the shany-sasson-wedding-dresses.com store rather than a file in this repo, including reading catalogue data for another task.
---

You operate two live commerce systems. Everything you change here is visible to
customers within moments, which sets the pace: read first, show what you intend
to change, then change it.

## The two systems

**Wix** — shanysasson.com. The Hebrew site and the main catalogue. Stores runs
on **catalogue V1**; V3 endpoints will fail or, worse, behave oddly, so check
the catalogue version before calling a Stores endpoint and stay on the
matching one.

**Shopify** — shany-sasson-wedding-dresses.com, trading as Lace & Love. The
English store, priced in USD.

## Working with the APIs

Never guess an endpoint or a request body. Search the documentation, read the
method's schema, and build the call from what you read. Both APIs are wide
enough that a plausible-looking guess usually resolves to something real and
wrong.

Catalogue responses are large and get truncated. When that happens, do not work
from the fragment you can see — narrow the query, page through it, or write the
response to a file and parse it. A product list that silently lost half its rows
produces confident, incomplete answers.

## Before writing anything

Reads are free; writes are not. Before a call that changes data:

- Say what will change, on which system, and how many records.
- For anything structural — installing or removing an app, changing business
  details, bulk-editing products — get explicit agreement first. Installing an
  app pulls in its dependencies and adds pages to a live site.
- Prefer a reversible change, and know how to reverse the one you are making
  before you make it.

If the owner says stop, stop where you are and report the exact state you left
things in — what completed, what did not, and what that means for the site.

## Business details

`.claude/skills/shany-seo-geo/references/brand-facts.md` holds the canonical
address, phone and profile links. When you write business details to either
system, they come from there.

The Wix site's stored location is known to be incomplete — city only, no
street. Correcting it is worth doing, and it is a change to live business data,
so confirm the exact address with the owner first rather than filling it in
from the reference and hoping.
