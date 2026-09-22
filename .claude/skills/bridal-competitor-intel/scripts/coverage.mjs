#!/usr/bin/env node
/**
 * Which target search terms have a page, and which do not.
 *
 *   node coverage.mjs [--pages landing] [--terms <path>]
 *
 * The competitive finding behind this is that studios in this category rank by
 * holding one page per search intent. That turns into a number you can watch:
 * terms covered out of terms targeted.
 *
 * Matching is by significant words rather than exact substring, so a term is
 * covered when a page's title or h1 contains all of its meaningful words in
 * any order — "שמלות כלה למלאות" matches "שמלות כלה למלאות · שני ששון".
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i === -1 ? d : args[i + 1]; };

const TERMS = resolve(opt('terms', join(HERE, '..', 'references', 'target-terms.md')));
const PAGES = resolve(opt('pages', 'landing'));

if (!existsSync(TERMS)) { console.error(`no terms file at ${TERMS}`); process.exit(2); }
if (!existsSync(PAGES)) { console.error(`no pages directory at ${PAGES}`); process.exit(2); }

// Terms live under headings; anything after "Deliberately not targeted" is
// recorded for context, not counted against coverage.
const raw = readFileSync(TERMS, 'utf8');
const active = raw.split(/^##\s+Deliberately not targeted\s*$/m)[0];
const terms = [...active.matchAll(/^-\s+(.+?)\s*$/gm)].map(m => m[1]);

// Words too common to carry meaning: every term here contains them.
const STOP = new Set(['שמלות', 'שמלת', 'כלה']);
const words = t => t.split(/\s+/).filter(w => w && !STOP.has(w));

const pages = readdirSync(PAGES).filter(f => f.endsWith('.html')).map(f => {
  const html = readFileSync(join(PAGES, f), 'utf8');
  const strip = s => s ? s.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : '';
  return {
    file: f,
    title: strip(html.match(/<title>(.*?)<\/title>/s)?.[1]),
    h1: strip(html.match(/<h1[^>]*>(.*?)<\/h1>/s)?.[1]),
  };
});

const covered = [], gaps = [];
for (const term of terms) {
  const w = words(term);
  const hit = pages.find(p => {
    const hay = (p.title + ' ' + p.h1);
    return w.length > 0 && w.every(x => hay.includes(x));
  });
  (hit ? covered : gaps).push({ term, page: hit?.file });
}

const green = s => `\x1b[32m${s}\x1b[0m`, dim = s => `\x1b[2m${s}\x1b[0m`, red = s => `\x1b[31m${s}\x1b[0m`;
console.log(`\n  ${pages.length} pages in ${PAGES}, ${terms.length} terms targeted\n`);
console.log(`  ${green('covered')}`);
for (const c of covered) console.log(`    ✓ ${c.term.padEnd(34)} ${dim(c.page)}`);
console.log(`\n  ${red('no page')}`);
for (const g of gaps) console.log(`    · ${g.term}`);

const pct = terms.length ? Math.round(covered.length / terms.length * 100) : 0;
console.log(`\n  ${covered.length}/${terms.length} covered (${pct}%)\n`);
