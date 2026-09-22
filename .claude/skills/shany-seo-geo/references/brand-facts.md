# Brand facts

The canonical record. Everything on every property copies from here. When
something here changes, it changes here first, then everywhere in the
propagation checklist at the bottom.

## Identity

| Field | Value |
|---|---|
| Hebrew name | שני ששון שמלות כלה |
| English name | Lace & Love by Shany Sasson |
| Founder | שני ששון — third generation of bridal designers |
| Street | עין חי 7 |
| City | הוד השרון |
| Country | IL |
| Phone | +972-52-555-7106 (display in Hebrew as 052-555-7106) |
| Email | shanysasson@gmail.com |
| Currency / TZ | ILS · Asia/Jerusalem |
| Serves | Israel, United States, Europe |

Write the phone as `+972-52-555-7106` in schema and `tel:` links, and as
`052-555-7106` in visible Hebrew copy. Wrap it in `dir="ltr"` inside RTL text or
the digits reorder.

## Addresses — read before writing one

**The studio moved to עין חי 7.** Business directories and Waze still carry the
previous address, Yehoshua Ben Gamla 39. Anything stating an address uses עין חי
7 unless the owner says otherwise.

Two records are known to be wrong or incomplete and are worth fixing at source:

- **The Wix site's own business location** stores only `הוד השרון, ישראל` — no
  street. Its geocode is `32.149961, 34.8838788`, which should be confirmed
  against the current studio before it is trusted.
- **Waze** resolves the business to the old street. This is the most damaging
  one: it misroutes a bride who is already on her way.

## Properties

| Property | Platform | Language | Role |
|---|---|---|---|
| shanysasson.com | Wix (Velo on, Stores catalog V1) | Hebrew | Main site and catalogue |
| shany-sasson-wedding-dresses.com | Shopify | English | International store |
| gownjournal.github.io | Eleventy | English | The Gown Journal, editorial |
| kala-magazine.github.io | Eleventy | Hebrew | מגזין הכלה, editorial |

The two editorial sites are positioned as independent and carry no promotional
content. Do not add landing pages, offers or calls to book to them — that
positioning is the reason they are worth anything.

## sameAs

Use this exact list wherever `sameAs` appears:

```
https://www.instagram.com/lace_and_love_brides/
https://www.facebook.com/shanysasson.bridal.fashion.home
https://www.pinterest.com/LaceandLoveBrides
https://www.etsy.com/shop/LaceAndLoveBrides
https://shany-sasson-wedding-dresses.com/
```

## Propagation checklist

Each of these is a separate record with its own login. Updating one updates
none of the others, which is why a change made in only one place quietly
decays into inconsistent business data — the thing both Google's local
algorithm and AI answer engines use to decide the business is real.

- [ ] Google Business Profile — highest weight, and where the reviews live
- [ ] Wix site business location (has no street address today)
- [ ] Shopify store settings
- [ ] Waze — misroutes brides while it is wrong
- [ ] Apple Maps, Bing Places
- [ ] d.co.il (דפי זהב)
- [ ] easy.co.il
- [ ] t.co.il (טופר)
- [ ] mit4mit.co.il
- [ ] Instagram and Facebook profile addresses
- [ ] Any landing page carrying the address in copy and in JSON-LD

## Verified reviews

Only these three are confirmed verbatim from the owner's Google Business
Profile. They may be quoted and marked up. Any other review needs its source
produced before it goes anywhere.

**ליאור דגן · 2026 · 5★**
> ממש נוח שאפשר להתבסס על דגם ששני עיצבה ולהתאים אותו בדיוק אלייך בתפירה הייחודית שלה. לכל מי שמתחברת לסגנון הבוהו-שיק, תחרה ולמראה הרומנטי, אמליץ בחום.

**אביה פלד · 2026 · 5★**
> מהרגע הראשון שנכנסתי לסטודיו הרגשתי בידיים הכי טובות שיש. שני קשובה, סבלנית, יצירתית, מקצועית ומשרה המון רוגע בתקופה הלחוצה הזו.

**עדי · 2019 · 5★**
> שני הייתה נעימה וסבלנית כבר מהפעם הראשונה שנכנסנו לסטודיו שלה. בכל מדידה היא הייתה מדייקת, מקצועית ונעימה, והתוצאה הייתה מהממת - שמלה מותאמת ומעוצבת במיוחד בשבילי.

The aggregate rating and total review count are **not known**. Until the owner
supplies them from the Business Profile, no `aggregateRating` goes anywhere.
