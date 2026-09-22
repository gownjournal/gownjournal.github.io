#!/usr/bin/env node
/**
 * Audit a page for the things a machine can check reliably.
 *
 *   node audit.mjs path/to/page.html [--width 1280] [--mobile 390]
 *
 * Exits non-zero if anything FAILs, so it can gate a publish.
 *
 * It renders the page in a real browser rather than parsing the HTML, because
 * the failures that actually ship — overflow, a collapsed image box, schema
 * that drifted from the copy — only exist once CSS has been applied.
 */
// A missing dependency should explain itself rather than throw a stack trace at
// someone who just wanted to check a page.
let chromium;
try {
  ({ chromium } = await import('playwright'));
} catch {
  console.error(`
  This audit renders the page in a real browser, so it needs Playwright.

      npm install                 # playwright is in this repo's devDependencies
      npx playwright install chromium   # only if no browser is present

  If Chromium already exists somewhere, point at it instead:

      CHROMIUM_PATH=/path/to/chrome node <this script> page.html
`);
  process.exit(2);
}
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';

const args = process.argv.slice(2);
const file = args.find(a => !a.startsWith('--'));
const flag = (n, d) => { const i = args.indexOf('--' + n); return i === -1 ? d : Number(args[i + 1]); };
const DESKTOP = flag('width', 1280), MOBILE = flag('mobile', 390);

if (!file || !existsSync(file)) {
  console.error('usage: node audit.mjs path/to/page.html [--width 1280] [--mobile 390]');
  process.exit(2);
}
const url = 'file://' + resolve(file);

const EXEC = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const results = [];
const add = (level, check, detail) => results.push({ level, check, detail });

const browser = await chromium.launch({
  executablePath: existsSync(EXEC) ? EXEC : undefined,
  args: ['--no-sandbox']
});

// ---- overflow, at both widths -------------------------------------------
for (const [label, width] of [['desktop', DESKTOP], ['mobile', MOBILE]]) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle' }).catch(() => page.goto(url));
  const { sw, cw } = await page.evaluate(() => ({
    sw: document.documentElement.scrollWidth,
    cw: document.documentElement.clientWidth
  }));
  if (sw > cw) {
    // name the culprits rather than just reporting the symptom
    const who = await page.evaluate(vw => [...document.querySelectorAll('*')]
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(({ r }) => r.width > 0 && (r.right > vw + 1 || r.left < -1))
      .slice(0, 5)
      .map(({ el, r }) => `<${el.tagName.toLowerCase()}${el.className ? '.' + String(el.className).split(' ')[0] : ''}> right=${Math.round(r.right)}`), width);
    add('FAIL', `no horizontal overflow (${label} ${width}px)`, `${sw}px in ${cw}px — ${who.join(', ')}`);
  } else {
    add('PASS', `no horizontal overflow (${label} ${width}px)`, `${sw}px`);
  }
  await page.close();
}

// ---- everything else, once ----------------------------------------------
const page = await browser.newPage({ viewport: { width: DESKTOP, height: 900 } });
const jsErrors = [];
page.on('pageerror', e => jsErrors.push(e.message));
await page.goto(url, { waitUntil: 'networkidle' }).catch(() => page.goto(url));

const d = await page.evaluate(() => {
  const txt = el => (el.textContent || '').replace(/\s+/g, ' ').trim();
  const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => {
    try { return { ok: true, data: JSON.parse(s.textContent) }; }
    catch (e) { return { ok: false, error: e.message }; }
  });
  // pair each <summary> with the disclosure body that follows it
  const faqOnPage = {};
  for (const s of document.querySelectorAll('details > summary')) {
    const body = [...s.parentElement.children].filter(c => c !== s).map(txt).join(' ').trim();
    faqOnPage[txt(s)] = body;
  }
  return {
    lang: document.documentElement.lang,
    dir: document.documentElement.dir,
    title: document.title,
    desc: document.querySelector('meta[name="description"]')?.content || '',
    canonical: document.querySelector('link[rel="canonical"]')?.href || '',
    ogImage: document.querySelector('meta[property="og:image"]')?.content || '',
    robots: document.querySelector('meta[name="robots"]')?.content || '',
    h1: [...document.querySelectorAll('h1')].map(txt),
    headings: [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]),
    imgsNoAlt: [...document.images].filter(i => !i.getAttribute('alt')).length,
    imgCount: document.images.length,
    collapsed: [...document.images].filter(i => { const r = i.getBoundingClientRect(); return r.width < 40 || r.height < 40; }).length,
    ld, faqOnPage,
    words: (document.body.innerText.trim().match(/\S+/g) || []).length
  };
});
await browser.close();

// ---- assertions ----------------------------------------------------------
const t = (c, ok, detail, soft) => add(ok ? 'PASS' : (soft ? 'WARN' : 'FAIL'), c, detail);

t('lang and dir set', !!d.lang && !!d.dir, `lang="${d.lang}" dir="${d.dir}"`);
t('exactly one <h1>', d.h1.length === 1, `${d.h1.length}: ${d.h1.join(' | ') || '(none)'}`);

let skip = null;
for (let i = 1; i < d.headings.length; i++) {
  if (d.headings[i] - d.headings[i - 1] > 1) { skip = `h${d.headings[i - 1]} -> h${d.headings[i]}`; break; }
}
t('heading levels do not skip', !skip, skip || d.headings.map(n => 'h' + n).join(' '));

t('every image has alt', d.imgsNoAlt === 0, `${d.imgsNoAlt} of ${d.imgCount} missing`);
t('no collapsed images', d.collapsed === 0,
  d.collapsed ? `${d.collapsed} rendered under 40px — a width/height attribute beating aspect-ratio usually causes this` : 'none');

t('title length 20-65', d.title.length >= 20 && d.title.length <= 65, `${d.title.length}: "${d.title}"`, true);
t('description length 70-160', d.desc.length >= 70 && d.desc.length <= 160, `${d.desc.length} chars`, true);
t('og:image present', !!d.ogImage, d.ogImage || 'missing — shared links render with no preview');
t('canonical present', !!d.canonical, d.canonical || 'missing', true);
t('robots meta present', !!d.robots, d.robots || 'missing (defaults are usually fine)', true);

const bad = d.ld.filter(b => !b.ok);
t('JSON-LD parses', bad.length === 0, bad.length ? bad.map(b => b.error).join('; ') : `${d.ld.length} block(s)`);

const types = d.ld.filter(b => b.ok).map(b => [].concat(b.data['@type'] || '?').join('+'));
t('structured data present', types.length > 0, types.join(', ') || 'none');

// schema that disagrees with the page is cloaking, so check it rather than trust it
const faqBlocks = d.ld.filter(b => b.ok && b.data['@type'] === 'FAQPage');
if (faqBlocks.length) {
  const drift = [];
  for (const b of faqBlocks) {
    for (const q of b.data.mainEntity || []) {
      const onPage = d.faqOnPage[q.name];
      const inSchema = (q.acceptedAnswer?.text || '').replace(/\s+/g, ' ').trim();
      if (onPage === undefined) drift.push(`"${q.name}" is in schema but not on the page`);
      else if (onPage !== inSchema) drift.push(`"${q.name}" answer differs from the page`);
    }
  }
  const qCount = faqBlocks.reduce((n, b) => n + (b.data.mainEntity || []).length, 0);
  t('FAQ schema matches the page', drift.length === 0, drift.join(' · ') || `${qCount} Q&A verified against the page`);
}

// the rule that costs rich results across the whole site if broken
const agg = JSON.stringify(d.ld).includes('aggregateRating');
t('no aggregateRating', !agg, agg ? 'present — publish only with a real count and average' : 'absent');

t('no JavaScript errors', jsErrors.length === 0, jsErrors.join('; ') || 'none');
add('INFO', 'word count', String(d.words));

// ---- report --------------------------------------------------------------
const icon = { PASS: '\x1b[32m✓\x1b[0m', FAIL: '\x1b[31m✗\x1b[0m', WARN: '\x1b[33m!\x1b[0m', INFO: '\x1b[36mi\x1b[0m' };
console.log(`\n  ${file}\n`);
for (const r of results) console.log(`  ${icon[r.level]} ${r.check.padEnd(38)} ${r.detail}`);
const fails = results.filter(r => r.level === 'FAIL').length;
const warns = results.filter(r => r.level === 'WARN').length;
console.log(`\n  ${results.filter(r => r.level === 'PASS').length} passed · ${warns} warnings · ${fails} failed\n`);
process.exit(fails ? 1 : 0);
