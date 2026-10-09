// Smoke test: opens every visualization and checks it renders without errors.
// Needs Playwright:  npm i -g playwright   (then: node site/tests/smoke.js)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 400, height: 860 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../dist/index.html'));
  await p.waitForSelector('.island');
  const lc = [509,206,231,67,69,169,1150,1971,997,1791,733,111,463,104,112,703,1046,70,746,118,1137,121,303,392,1710,455,860,2037,252,605,28,459,796,14,1455];
  let bad = 0;
  for (const n of lc) for (const k of ['i' + n, 's' + n]) {
    const r = await p.evaluate(k => { try { window.__vizOpen(k); return { c: document.getElementById('vcount').textContent, w: document.querySelectorAll('#vstage .warn').length }; } catch (e) { return { e: String(e) }; } }, k);
    if (r.e || r.w || !r.c) { bad++; console.log('BAD', k, JSON.stringify(r)); }
    await p.evaluate(() => { const x = document.querySelector('[data-vact=close]'); x && x.click(); });
  }
  console.log('checked', lc.length * 2, 'bad', bad, 'page errors', errs.length);
  await b.close();
  process.exit(bad || errs.length ? 1 : 0);
})();
