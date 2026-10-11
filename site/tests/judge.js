// Judge test: for each problem in data/judge.json, submits the reference solution (expects Accepted)
// and the empty starter (expects anything else), then checks that an infinite loop gets Time Limit Exceeded.
// Needs Playwright:  npm i -g playwright   (then: python3 site/build.py && node site/tests/judge.js)
// Without internet access to cdn.jsdelivr.net, point PYODIDE_DIR at an unpacked `npm pack pyodide@0.26.4` (its package/ folder).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const dist = path.resolve(__dirname, '../dist'), root = path.resolve(__dirname, '../..');
const judge = JSON.parse(fs.readFileSync(path.join(root, 'data/judge.json'), 'utf8')).problems;
const roadmap = JSON.parse(fs.readFileSync(path.join(root, 'data/leetcode.json'), 'utf8')).questions;
(async () => {
  // Blob workers need an http origin, so serve dist/ instead of opening the file directly.
  const srv = http.createServer((req, res) => {
    const f = path.join(dist, decodeURIComponent(req.url.split('?')[0]).replace(/^\/$/, '/index.html'));
    if (!f.startsWith(dist) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': (f.endsWith('.html') ? 'text/html' : 'text/javascript') + '; charset=utf-8' }); res.end(fs.readFileSync(f));
  }).listen(0);
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  await ctx.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  if (process.env.PYODIDE_DIR) await ctx.route(/cdn\.jsdelivr\.net\/pyodide\/v[\d.]+\/full\/(.*)$/, r => {
    const f = path.join(process.env.PYODIDE_DIR, new URL(r.request().url()).pathname.split('/full/')[1]);
    const ct = f.endsWith('.wasm') ? 'application/wasm' : f.endsWith('.json') ? 'application/json' : f.endsWith('.zip') ? 'application/zip' : 'text/javascript';
    r.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': ct, 'access-control-allow-origin': '*' } });
  });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://127.0.0.1:${srv.address().port}/index.html`);
  await p.waitForTimeout(500); await p.keyboard.press('Escape');
  const submit = async (code) => {
    await p.fill('#jcode', code); await p.click('#jsub');
    await p.waitForFunction(() => !document.getElementById('jsub').disabled && document.querySelector('#jres h3'), null, { timeout: 90000 });
    return p.textContent('#jres h3');
  };
  let bad = 0;
  for (const n of Object.keys(judge)) {
    const node = roadmap.find(q => String(q.number) === n).nodes[0];
    await p.click(`[data-act=node][data-id="${node}"]`);
    await p.click(`[data-act=judge][data-n="${n}"]`);
    await p.waitForFunction(() => !document.getElementById('jsub').disabled, null, { timeout: 90000 });
    const starter = await submit(await p.inputValue('#jcode'));
    const ref = await submit(fs.readFileSync(path.join(root, 'data/judge/solutions', n + '.py'), 'utf8'));
    const ok = /Accepted/.test(ref) && !/Accepted/.test(starter);
    if (!ok) bad++;
    console.log(ok ? 'ok ' : 'BAD', n, '| starter:', starter.trim(), '| reference:', ref.trim());
    if (n === Object.keys(judge)[0]) {
      const tle = await submit(`class Solution:\n    def ${judge[n].method}(self, *a):\n        while True:\n            pass\n`);
      if (!/Time Limit/.test(tle)) { bad++; console.log('BAD infinite loop:', tle); } else console.log('ok  infinite loop -> Time Limit Exceeded');
    }
    await p.keyboard.press('Escape'); await p.keyboard.press('Escape');
  }
  console.log('problems', Object.keys(judge).length, 'bad', bad, 'page errors', errs.length);
  await b.close(); srv.close();
  process.exit(bad || errs.length ? 1 : 0);
})();
