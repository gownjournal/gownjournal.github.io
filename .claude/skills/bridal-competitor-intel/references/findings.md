# Findings log

Newest first. Each entry is a dated snapshot so the next run can diff against
it rather than starting from nothing. Note what changed since the previous
entry, not just what is true now.

---

## 2026-09-22 — first survey

**Method.** Six searches across style, city, price and segment terms. Titles
and URLs only; no competitor page was loaded, since outbound access to those
domains is blocked here.

**Findings.**

1. The category competes through **one page per search intent**, not through a
   single site. Clair Bridal holds at least eight; this studio held one.
2. **Price in the title is the norm.** Range observed, 2,500–6,000 ₪.
3. **Every competitor states a differentiator in the title** — modest, all
   sizes, couture, fixed price, or a city.
4. **הוד השרון was unclaimed.** Competitors hold their own city terms.
5. **International shipping is unclaimed by all nine**, and this studio
   genuinely does it.
6. A leading competitor runs a **separate domain** for its campaign landing
   page.

**Acted on.** Built `landing/hod-hasharon.html` for the city term and
`landing/shmalot-im-sharvulim.html` for a catalogue segment.

**Decided.** The international shipping page — the highest-potential term in
the set — will not be built; the owner declined it. Recorded in
target-terms.md under "deliberately not targeted" so it is a known choice, not
a gap.

**Watch next time.** Whether Clair refreshes its titles to 2027; whether anyone
claims הוד השרון; whether any competitor starts advertising shipping abroad.
