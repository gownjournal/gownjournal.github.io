---
name: natural-hebrew-writing
description: Write and edit Hebrew prose so it reads like a Hebrew speaker wrote it, rather than like English translated word by word. Use whenever writing, drafting, rewriting or proofreading any Hebrew text meant for readers — landing pages, product descriptions, blog posts, emails, ads, social copy, FAQ answers, button labels. Also use when Hebrew text sounds translated, stiff or off and the reason is not obvious, when checking Hebrew before publishing, and whenever Hebrew and English versions of the same page are written together, since that is when English structure leaks across.
---

# Writing Hebrew that does not read as translated

Hebrew written by someone thinking in English is rarely wrong in a way that
trips a spellchecker. It is wrong in a way native readers feel immediately and
usually cannot name: the words are Hebrew and the sentence is English.

The failures below all came from one real page. None was a typo.

## The four that do the most damage

**Calques.** English idioms carried across intact. A cut does not עובד על a
body — that is "works on". A dress does not מרגישה שלך — that is "feels
yours". The full list, with what to write instead, is in
`references/calques.md`. Read it when editing; these are the hardest errors to
catch by ear once you have been reading English all day.

**Prepositions.** Hebrew is strict where English is loose. תפורה **לפי**
המידות, never על. מעוצבת **לפי** המידות, not ב. The preposition is part of the
verb, not a detail — getting it wrong is the single clearest tell.

**Punctuation.** Hebrew has no serial comma. *מודדות, מדברות, ומחליטות* is
English punctuation in Hebrew words; write *מודדות, מדברות ומחליטות*. And do
not put a comma before ו joining two clauses about the same subject.

**Register drift.** Decide who speaks and who is addressed, then hold it. A
page that says אנחנו in one paragraph, slips into impersonal masculine plural
(מודדים, לוקחים, יוצאים) in the next, and addresses the reader as את in the
third reads as three different writers. Impersonal plural is not neutral in
Hebrew — it is a different voice.

## Agreement attaches to the right noun

מגוון שמלות **ממתין**, not ממתינות — the subject is מגוון, which is singular.
When that reads badly, the fix is to recast so the plural is genuinely the
subject: *שמלות במגוון גזרות ממתינות לך*. Forcing the verb to agree with the
noun you meant rather than the noun you wrote is the wrong repair.

Watch pronouns with two possible referents. *כל שמלה עברה דרך המדידות שלה* —
whose? The dress's. Name the person.

## Mechanics of Hebrew on a page

`references/mechanics.md` covers RTL typography in full. The three that bite
most often:

**There is no Hebrew italic.** The browser slants the glyphs itself and the
result looks broken. Emphasise with colour, weight or size.

**Latin runs inside RTL text reorder.** Phone numbers, emails and URLs need
`dir="ltr"` or the digits scramble.

**The maqaf ־ is not a hyphen.** In most web fonts it renders as a raised bar.
Write בוהו-שיק with a plain hyphen.

## The check that runs

```bash
node .claude/skills/natural-hebrew-writing/scripts/check.mjs <file>
```

It catches the mechanical failures — calques from the list, wrong prepositions
in known patterns, serial commas, stray dashes, unwrapped Latin runs. It exits
non-zero when it finds any, so it can gate a publish.

It cannot hear register drift or a sentence that is grammatical and lifeless.
Read the copy aloud after the script passes. If it sounds like a translation,
it is one, and the script will not tell you.

## When the text is quoted

Never fix someone's Hebrew inside a quotation. A customer review is evidence
about a named person; correcting their grammar makes it something they did not
write. Trim with ellipses if you must, and leave the rest exactly as it stands.
