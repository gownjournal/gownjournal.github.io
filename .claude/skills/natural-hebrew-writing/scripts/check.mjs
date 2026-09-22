#!/usr/bin/env node
/**
 * Find the mechanical failures in Hebrew copy.
 *
 *   node check.mjs page.html [more.html ...]
 *
 * Exits non-zero when anything is found, so it can gate a publish.
 *
 * It reads the visible copy only — script, style and comments are stripped, so
 * a calque in a code comment is not reported as a problem for readers. Text
 * inside <blockquote> is skipped too: a quotation is evidence about a named
 * person, and correcting their Hebrew makes it something they did not write.
 */
import { readFileSync, existsSync } from 'node:fs';

const files = process.argv.slice(2).filter(a => !a.startsWith('--'));
if (!files.length) { console.error('usage: node check.mjs <file.html> [...]'); process.exit(2); }

// Each rule: what to look for, what it is, and what to write instead.
const CALQUES = [
  [/עובד(ת|ים|ות)?\s+על\s+ה?(גוף|גזרה|מבנה)/, 'עובד על', 'מחמיא ל / מתאים ל — "works on"'],
  [/תפור(ה|ים|ות)?\s+על\s+ה?מידות/, 'תפורה על המידות', 'תפורה לפי המידות'],
  [/מעוצב(ת|ים|ות)?\s+במידות/, 'מעוצבת במידות', 'מעוצבת לפי המידות'],
  [/מרגיש(ה|ים|ות)?\s+שלך/, 'מרגישה שלך', 'הופכת להיות שלך — "feels yours"'],
  [/לחץ\s+למכור/, 'לחץ למכור', 'לחץ של מכירה'],
  [/בסופו\s+של\s+יום/, 'בסופו של יום', 'בסופו של דבר'],
  [/להתמקד\s+על/, 'להתמקד על', 'להתמקד ב'],
  [/תרגיש(י|ו)?\s+חופשי/, 'תרגישי חופשי', 'אל תהססי'],
  [/ת(ן|ני|נו)\s+לנו\s+לדעת/, 'תני לנו לדעת', 'עדכני אותנו'],
  [/לקחת\s+את\s+הזמן/, 'לקחת את הזמן', 'בלי למהר'],
  [/לשלב\s+הבא/, 'לשלב הבא', '"to the next level" — cut or rephrase'],
  [/ברמה\s+אחרת/, 'ברמה אחרת', 'recast — sports cliché in Hebrew'],
  [/לעשות\s+הבדל/, 'לעשות הבדל', 'לחולל שינוי'],
];

const HEB = /[֐-׿]/;
let total = 0;

for (const file of files) {
  if (!existsSync(file)) { console.error(`  missing: ${file}`); total++; continue; }
  let html = readFileSync(file, 'utf8');

  html = html.replace(/<script[\s\S]*?<\/script>/g, ' ')
             .replace(/<style[\s\S]*?<\/style>/g, ' ')
             .replace(/<!--[\s\S]*?-->/g, ' ');

  // quotations are somebody's own words; they are not ours to correct
  const quotes = [...html.matchAll(/<blockquote[\s\S]*?<\/blockquote>/g)].map(m => m[0]);
  html = html.replace(/<blockquote[\s\S]*?<\/blockquote>/g, ' ');

  const findings = [];
  const text = html.replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ').replace(/\s+/g, ' ');

  for (const [re, name, fix] of CALQUES) {
    const m = text.match(re);
    if (m) findings.push(['calque', `"${m[0].trim()}"`, fix]);
  }

  // Hebrew takes no serial comma: a comma, another comma, then ו
  for (const s of text.split(/(?<=[.!?])\s+/)) {
    if (!HEB.test(s)) continue;
    // a comma before ו is correct when ו opens a contrast (ולא, ואילו…), so those
    // are not flagged. \b is useless here: Hebrew letters are not \w in JS.
    const m = s.match(/[֐-׿]+\s*,\s*[֐-׿\s]+,\s+(?:ו(?!(?:לא|אילו|אף|אכן)(?![\u0590-\u05FF]))|או(?![\u0590-\u05FF]))/);
    if (m) findings.push(['serial comma', `"…${m[0].trim()}…"`, 'drop the comma before ו / או']);
  }

  const dash = text.match(/[–—]/g);
  if (dash) findings.push(['dash', `${dash.length} en/em dash${dash.length > 1 ? 'es' : ''}`,
                           'Hebrew prose takes a comma, colon or full stop']);

  const maqaf = text.match(/־/g);
  if (maqaf) findings.push(['maqaf ־', `${maqaf.length}`, 'renders as a raised bar — use a plain hyphen']);

  // Latin runs adrift in RTL: a phone-shaped string with no dir on its element
  for (const m of html.matchAll(/<([a-z]+)([^>]*)>([^<]*\d{2,}[-.]\d{3,}[^<]*)</gi)) {
    if (!/\bdir\s*=/.test(m[2])) findings.push(['unwrapped LTR', `"${m[3].trim()}"`, `<${m[1]}> needs dir="ltr"`]);
  }

  if (/font-style\s*:\s*italic/.test(readFileSync(file, 'utf8')) && HEB.test(text))
    findings.push(['italic', 'font-style: italic', 'Hebrew has no italic cut — the browser fakes a slant']);

  const icon = findings.length ? '\x1b[31m✗\x1b[0m' : '\x1b[32m✓\x1b[0m';
  console.log(`\n  ${icon} ${file}${quotes.length ? `  \x1b[2m(${quotes.length} quotation${quotes.length > 1 ? 's' : ''} skipped)\x1b[0m` : ''}`);
  for (const [kind, found, fix] of findings)
    console.log(`      \x1b[33m${kind}\x1b[0m  ${found}\n        → ${fix}`);
  total += findings.length;
}

console.log(`\n  ${total} finding${total === 1 ? '' : 's'}\n`);
process.exit(total ? 1 : 0);
