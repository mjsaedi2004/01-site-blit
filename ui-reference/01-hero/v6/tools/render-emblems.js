// Renders the ready-made objects in emblems.html to transparent PNGs (needs Node + Playwright with Chromium).
//   node render-emblems.js [spotlight balloons microphone discoball daf]
// Then crop each to its content and save it as WebP (max 1100px) in ../assets/emblems/.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : ['spotlight', 'balloons', 'microphone', 'discoball', 'daf'];
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  await p.goto('file://' + __dirname + '/emblems.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
  for (const n of names) {
    const url = await p.evaluate((n) => window.renderEmblem(n), n);
    fs.writeFileSync(`${n}-raw.png`, Buffer.from(url.split(',')[1], 'base64')); console.log('rendered', n);
  }
  await b.close();
})();
