# Hebrew on a web page

## Typography

**No italic.** Hebrew has no italic cut. `font-style: italic` makes the browser
slant the upright glyphs, and the result looks like a rendering fault. Use
colour, weight, or size for emphasis.

**No uppercase.** Hebrew is unicase, so `text-transform: uppercase` does
nothing. An eyebrow or label that relies on caps in English needs a different
device in Hebrew — smaller size, letter-spacing, and the accent colour.

**Letter-spacing sparingly.** It works, but Hebrew tolerates less of it than
Latin before words stop holding together. Around .04–.08em for labels.

**Fonts.** Most Latin display faces have no Hebrew. Cormorant, Inter, Playfair
and their kind will silently fall back to a system font for Hebrew glyphs,
which is how a page ends up in two unrelated typefaces without anyone
noticing. Either pick a Hebrew face, or stack them so each script gets its own:

```css
--heading: "Cormorant", "Frank Ruhl Libre", Georgia, serif;
--body: "Inter", "Heebo", sans-serif;
```

Latin glyphs come from the first family, Hebrew falls through to the second.
Frank Ruhl Libre is the closest Hebrew answer to an old-style serif; Heebo is
Roboto-derived and sits well beside Inter.

## Direction

`<html lang="he" dir="rtl">` on the document.

**Latin and digits inside Hebrew reorder.** Phone numbers, emails, URLs and
model codes need their own `dir="ltr"`:

```html
<a href="tel:+972525557106" dir="ltr">052-555-7106</a>
```

Without it, `052-555-7106` can render with its segments rearranged.

**Use logical properties in CSS.** `margin-inline-start`, `padding-inline-end`,
`border-inline-start`, `inset-inline-start`. A `border-left` that framed a
quotation in English lands on the wrong side in Hebrew, and `text-align: left`
should almost always be `start`.

## Punctuation

**No serial comma.** מודדות, מדברות ומחליטות — not …, ומחליטות.

**No comma before ו** joining two predicates of one subject: *עומדת מולך
ויודעת*, not *עומדת מולך, ויודעת*.

**The maqaf ־ (U+05BE) is not a hyphen.** It is the biblical connector, and in
most web fonts it renders as a raised bar that looks like a mistake. Write
בוהו-שיק with a plain hyphen.

**Dashes.** The em dash — is Latin punctuation. Hebrew prose generally takes a
comma, a colon or a full stop instead. It is not an error, but a page full of
them reads as translated.

**Quotation marks.** Hebrew uses gershayim ״ inside abbreviations and units:
ס״מ, not ס"מ with a straight double quote.

## Gendered address

Hebrew forces a choice English does not. Decide the audience's gender and hold
it — a page addressed to a bride is את, תנעלי, השאירי throughout. When the
audience is genuinely mixed and no form fits, recast to the infinitive or to
first person plural rather than alternating.
