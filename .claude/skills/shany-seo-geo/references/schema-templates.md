# JSON-LD templates

Fill from `brand-facts.md`. Emit as `<script type="application/ld+json">` in the
head. Keep Hebrew as real characters, not escapes — it stays readable and both
Google and the answer engines handle UTF-8 fine.

A page normally carries the business block plus whichever content block fits.
Two or three blocks is plenty; more is noise.

## LocalBusiness — every page on the main site

`@id` is the stable identifier for the business across pages. Keep it identical
everywhere so the graph resolves to one entity rather than several.

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "ClothingStore"],
  "@id": "https://www.shanysasson.com/#studio",
  "name": "שני ששון שמלות כלה",
  "alternateName": "Lace & Love by Shany Sasson",
  "description": "סטודיו שמלות כלה בוהו שיק בהוד השרון. כל שמלה מעוצבת ונתפרת בסטודיו לפי המידות של הכלה.",
  "url": "https://www.shanysasson.com/",
  "image": "<1200x630 absolute URL>",
  "telephone": "+972-52-555-7106",
  "email": "shanysasson@gmail.com",
  "inLanguage": "he-IL",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "עין חי 7",
    "addressLocality": "הוד השרון",
    "addressCountry": "IL"
  },
  "founder": { "@type": "Person", "name": "שני ששון", "jobTitle": "מעצבת שמלות כלה" },
  "areaServed": [
    { "@type": "Country", "name": "ישראל" },
    { "@type": "Country", "name": "ארצות הברית" },
    { "@type": "Place", "name": "אירופה" }
  ],
  "sameAs": ["<the sameAs list from brand-facts.md>"]
}
```

Add `geo` and `openingHoursSpecification` once those are confirmed. Leave out
`priceRange` — the owner has decided not to publish price information, and an
invented range is exactly the kind of unverifiable claim this skill exists to
prevent.

## FAQPage — any page with a question list

The answer text has to be byte-identical to what the page renders. Generate both
from one source where you can; `scripts/audit.mjs` fails the build if they
drift.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "inLanguage": "he-IL",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "<the question, exactly as the page shows it>",
      "acceptedAnswer": { "@type": "Answer", "text": "<the answer, exactly as the page shows it>" }
    }
  ]
}
```

## Service — made-to-measure design

Worth its own block on a page selling the service rather than a garment. This is
also the type that can legitimately carry reviews, when the reviews are about
the service itself.

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "עיצוב ותפירת שמלת כלה בהתאמה אישית",
  "provider": { "@id": "https://www.shanysasson.com/#studio" },
  "areaServed": { "@type": "Country", "name": "ישראל" },
  "audience": { "@type": "Audience", "audienceType": "כלות" }
}
```

## Review — only from the verified list

Three are verified in `brand-facts.md`. Nothing else is quotable.

```json
{
  "@type": "Review",
  "reviewRating": { "@type": "Rating", "ratingValue": 5, "bestRating": 5 },
  "author": { "@type": "Person", "name": "<name as published>" },
  "datePublished": "<year as published>",
  "reviewBody": "<verbatim, trimmed with ellipses at most>"
}
```

`aggregateRating` is deliberately absent from every template here. Add it only
when the real count and average are in hand — see the integrity gate in
SKILL.md for why this one is not negotiable.

## Article — the editorial sites

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "<title>",
  "datePublished": "<ISO>",
  "dateModified": "<ISO>",
  "author": { "@type": "Person", "name": "Shany Sasson" },
  "inLanguage": "en"
}
```

Do not attach the `LocalBusiness` block to editorial pages. Those sites are
positioned as independent, and wiring the studio into their markup contradicts
that in the one place a machine is certain to read.

## Head tags that belong with every page

```html
<html lang="he" dir="rtl">
<title><!-- what a bride searches, then the brand, ~60 chars --></title>
<meta name="description" content="<!-- 70-160 chars -->">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="<absolute URL>">
<meta property="og:title" content="">
<meta property="og:description" content="">
<meta property="og:image" content="<absolute, 1200x630>">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="">
<meta property="og:locale" content="he_IL">
<meta name="twitter:card" content="summary_large_image">
```

For Wix-hosted images, request the size you need rather than scaling a thumbnail
in CSS: append `/v1/fill/w_1200,h_630,al_t,q_85/file.jpg` to the media URL.
`al_t` keeps the top of a portrait shot, which on a full-length gown photo is
the part worth showing.
