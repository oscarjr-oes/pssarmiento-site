#!/usr/bin/env node
/**
 * Measure page weight of a built copy of the site (jekyll build -d <dir>).
 *
 *   node scripts/measure_page_weight.js <site-dir> [--react-dir <dir>] [--json out.json]
 *
 * Needs Playwright (npm i -D playwright). Serves <site-dir> on localhost, loads
 * each page in an emulated phone (390x844 @2x, the typical srcset case), and
 * reports bytes in two phases:
 *   initial  – everything fetched at load, without scrolling
 *   scrolled – plus everything fetched after scrolling to the bottom
 * It never clicks anything, so "on user action" assets (360 video, .ply, press
 * zips, lightbox images) show up as 0 unless the page loads them eagerly.
 *
 * Text responses are counted gzip-compressed (as GitHub Pages serves them);
 * images/video/binary are counted as-is. Same-origin and third-party bytes are
 * reported separately. If unpkg.com is unreachable from where you run this, pass
 * --react-dir with the unpacked `react` and `react-dom` npm tarballs
 * (<dir>/react/umd/..., <dir>/react-dom/umd/...) and they're served in its place.
 */
const http = require('http'), fs = require('fs'), path = require('path'), zlib = require('zlib');
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const siteDir = path.resolve(args[0] || '_site');
const opt = (n) => { const i = args.indexOf(n); return i > -1 ? args[i + 1] : null; };
const reactDir = opt('--react-dir'), jsonOut = opt('--json');

const PAGES = [
  ['home',                     '/'],
  ['news post (MOU, 17 imgs)', '/news/mou-signing-flp-and-mhsd/'],
  ['news post (typical)',      '/news/new-hq-soon-to-rise/'],
  ['contact',                  '/contact.html'],
  ['banwag',                   '/banwag.html'],
];
const MIME = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.jpg':'image/jpeg',
  '.png':'image/png', '.webp':'image/webp', '.svg':'image/svg+xml', '.mp4':'video/mp4', '.ply':'application/octet-stream',
  '.zip':'application/zip', '.json':'application/json' };

const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  let f = path.join(siteDir, p);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end('nf'); }
  res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

const isText = (ct) => /text|javascript|json|svg|xml/.test(ct || '');
const kb = (n) => (n / 1024).toFixed(0);

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch();
  const out = {};
  for (const [name, url] of PAGES) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    const seen = new Map(); // url -> {bytes, third, phase, type}
    if (reactDir) {
      await page.route(/unpkg\.com\/(react|react-dom)@18\.3\.1\//, (route) => {
        const u = route.request().url();
        const f = path.join(reactDir, u.includes('react-dom@') ? 'react-dom' : 'react', 'umd', path.basename(u));
        route.fulfill({ status: 200, contentType: 'text/javascript', body: fs.readFileSync(f),
          headers: { 'access-control-allow-origin': '*' } });
      });
    }
    // Analytics / form endpoints are not controlled by this repo; keep them out of the numbers.
    await page.route(/googletagmanager|google-analytics|formspree/, r => r.abort());
    let phase = 'initial';
    page.on('response', async (resp) => {
      try {
        const u = resp.url(); if (u.startsWith('data:')) return;
        const body = await resp.body();
        const ct = resp.headers()['content-type'] || '';
        const bytes = isText(ct) ? zlib.gzipSync(body).length : body.length;
        seen.set(u, { bytes, third: !u.startsWith(origin), phase, type: ct.split(';')[0] });
      } catch (e) { /* aborted/redirect */ }
    });
    await page.goto(origin + url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
    await page.waitForTimeout(1500);
    phase = 'scrolled';
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < h + 844; y += 400) { await page.evaluate(v => window.scrollTo(0, v), y); await page.waitForTimeout(120); }
    await page.waitForTimeout(1500);
    const sum = (f) => [...seen.values()].filter(f).reduce((a, v) => a + v.bytes, 0);
    const res = {
      requests: seen.size,
      initial_own: sum(v => v.phase === 'initial' && !v.third),
      initial_third: sum(v => v.phase === 'initial' && v.third),
      scrolled_own: sum(v => !v.third),
      scrolled_third: sum(v => v.third),
      images_own: sum(v => !v.third && /^image\//.test(v.type)),
      heavy_loaded: [...seen.entries()].filter(([u]) => /\.(ply|mp4|zip)(\?|$)/.test(u)).map(([u, v]) => u.replace(origin, '') + ' ' + kb(v.bytes) + ' KB'),
    };
    out[name] = res;
    console.log(`${name.padEnd(26)} initial: ${kb(res.initial_own).padStart(6)} KB own + ${kb(res.initial_third).padStart(4)} KB 3rd | after scroll: ${kb(res.scrolled_own).padStart(6)} KB own + ${kb(res.scrolled_third).padStart(4)} KB 3rd | ${res.requests} req | heavy: ${res.heavy_loaded.join(', ') || 'none'}`);
    await ctx.close();
  }
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(out, null, 2));
  await browser.close(); server.close();
})();
