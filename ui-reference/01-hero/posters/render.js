// Renders every .poster in source.html to ../assets/posters/<id>.webp (1200×1800) and <id>-thumb.webp (400×600).
// Needs Playwright and Python Pillow:  node render.js  (serve the folder over HTTP first, see README)
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8765/posters/source.html';
const out = path.join(__dirname, '..', 'assets', 'posters');
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const ids = await page.$$eval('.poster', (els) => els.map((e) => e.id));
  for (const id of ids) {
    const png = path.join(out, `${id}.png`);
    await page.locator(`#${id}`).screenshot({ path: png });
    execFileSync('python3', ['-c', `
from PIL import Image
im = Image.open(${JSON.stringify(png)}).convert('RGB')
im.save(${JSON.stringify(path.join(out, id + '.webp'))}, 'WEBP', quality=90, method=6)
im.resize((400, 600), Image.LANCZOS).save(${JSON.stringify(path.join(out, id + '-thumb.webp'))}, 'WEBP', quality=88, method=6)
`]);
    fs.unlinkSync(png);
    console.log('rendered', id);
  }
  await browser.close();
})();
