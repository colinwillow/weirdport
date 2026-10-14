// npm run shot [name ...] -- headless Chromium (SwiftShader) boots the SHIPPED index.html, sends him to a GOD place,
// lets the frame loop settle round him, then renders ONE frame from an authored camera and saves it as a JPEG.
//
// m295 tried `page.screenshot` and dropped it: it waits for the compositor to produce a frame, and the kit city under
// software GL takes longer than its 30 s timeout. This never asks the compositor. It renders inside `page.evaluate`
// and reads the canvas with `toDataURL` in the SAME task, before the drawing buffer is cleared. The only thing added
// to the served text is a handle on `renderer`, `scene` and `camera` (`window.__shot`), spliced in front of `mel`.
//
// Every shot is a row in SHOTS: a GOD place to stand at, and a camera written in the page from the live game state.
// Output: the scratch dir given by SHOT_DIR, or ./shots (gitignored).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const OUT = process.env.SHOT_DIR || path.join(ROOT, 'shots');
const req = createRequire(import.meta.url);
let pw;
for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright', '/opt/node-tools/node_modules/playwright']) {
  try { pw = req(p); break; } catch (e) {}
}
if (!pw) { console.error('no playwright'); process.exit(1); }

// The cameras. Each runs in the page with `S` = window.__shot and `mel`, after him standing at `place` for `settle` s.
// Returns [eye x, y, z, target x, y, z]. Heights are over his feet.
const SHOTS = {
  ridge: { place: 'overlook', settle: 3, why: 'a wide shot from the west hill: fields, buildings and the skyline',
    cam: `(() => { const p = mel.player.pos, I = mel.ISLE.rect, cx = (I[0] + I[1]) / 2, cz = (I[2] + I[3]) / 2;
      const O = mel.FARMLAND.O, dx = O[0] - p.x, dz = O[1] - p.z, L = Math.hypot(dx, dz), tx = cx * .35 + O[0] * .65, tz = cz * .35 + O[1] * .65;
      return [p.x - dx / L * 10, p.y + 14, p.z - dz / L * 10, tx, p.y - 6, tz]; })()` },
  town: { place: 'road', settle: 3, why: 'the road through the transition: the fingerpost, the edge of town, the bridge',
    cam: `(() => { const p = mel.player.pos, B = mel.BRIDGE.gate || mel.BRIDGE.at, bx = B.x != null ? B.x : B[0], bz = B.z != null ? B.z : B[1];
      const dx = bx - p.x, dz = bz - p.z, L = Math.hypot(dx, dz);
      return [p.x - dx / L * 14, p.y + 7, p.z - dz / L * 14, p.x + dx / L * 60, p.y - 2, p.z + dz / L * 60]; })()` },
  skyline: { place: 'crash', settle: 3, why: 'the city from the crash site: a skyline on the horizon (STEER 1)',
    cam: `(() => { const p = mel.player.pos, I = mel.ISLE.rect, cx = (I[0] + I[1]) / 2, cz = (I[2] + I[3]) / 2, dx = cx - p.x, dz = cz - p.z, L = Math.hypot(dx, dz);
      return [p.x - dx / L * 3, p.y + 2.2, p.z - dz / L * 3, cx, p.y + 6, cz]; })()` },
  overcity: { place: 'overlook', settle: 3, why: 'the city from the west hill, square on',
    cam: `(() => { const p = mel.player.pos, I = mel.ISLE.rect, cx = (I[0] + I[1]) / 2, cz = (I[2] + I[3]) / 2, dx = cx - p.x, dz = cz - p.z, L = Math.hypot(dx, dz);
      return [p.x - dx / L * 3, p.y + 3, p.z - dz / L * 3, cx, p.y - 4, cz]; })()` },
  yard: { place: 'farmyard', settle: 3, why: 'the farmyard from behind him: barn, silo, house',
    cam: `(() => { const p = mel.player.pos, h = mel.player.heading || 0, fx = Math.sin(h), fz = Math.cos(h);
      return [p.x - fx * 9, p.y + 4.5, p.z - fz * 9, p.x + fx * 20, p.y + 1, p.z + fz * 20]; })()` },
  gas: { place: 'gas', settle: 3, why: 'the edge of town: the gas station, the trailers, the bridge beyond',
    cam: `(() => { const p = mel.player.pos, h = mel.player.heading || 0, fx = Math.sin(h), fz = Math.cos(h);
      return [p.x - fx * 22, p.y + 14, p.z - fz * 22, p.x + fx * 25, p.y, p.z + fz * 25]; })()` },
  house: { place: 'farmhouse', settle: 3, why: 'the farmhouse and its yard',
    cam: `(() => { const p = mel.player.pos, h = mel.player.heading || 0, fx = Math.sin(h), fz = Math.cos(h);
      return [p.x - fx * 12 + fz * 6, p.y + 6, p.z - fz * 12 - fx * 6, p.x + fx * 15, p.y + 2, p.z + fz * 15]; })()` },
  herd: { place: 'herd', settle: 3, why: 'a herd in its pasture',
    cam: `(() => { const p = mel.player.pos, h = mel.player.heading || 0, fx = Math.sin(h), fz = Math.cos(h);
      return [p.x - fx * 8, p.y + 3.5, p.z - fz * 8, p.x + fx * 25, p.y, p.z + fz * 25]; })()` },
  terrace: { place: 'orchard', settle: 3, why: 'the orchard terrace from the foot of its steps',
    cam: `(() => { const p = mel.player.pos, A = mel.FTERR.at, dx = A[0] - p.x, dz = A[2] - p.z, L = Math.hypot(dx, dz);
      return [p.x - dx / L * 10 - dz / L * 8, p.y + 6, p.z - dz / L * 10 + dx / L * 8, A[0], A[1] - 3, A[2]]; })()` },
  topcity: { place: 'oldtown', settle: 4, why: 'Old Town from straight above: streets, lots and buildings, for placing things',
    cam: `(() => { const I = mel.ISLE.rect, cx = (I[0] + I[1]) / 2, cz = (I[2] + I[3]) / 2; return [cx, 240, cz + .01, cx, 0, cz]; })()` },
  camp: { place: 'camp', settle: 4, why: 'the camp at the west edge of Old Town',
    cam: `(() => { const p = mel.player.pos, h = mel.player.heading || 0, fx = Math.sin(h), fz = Math.cos(h);
      return [p.x - fx * 6 + fz * 3, p.y + 4.5, p.z - fz * 6 - fx * 3, p.x + fx * 7, p.y, p.z + fz * 7]; })()` },
  carts: { place: 'carts', settle: 5, why: 'the food-cart pod and Chef Norrie',
    cam: `(() => { const p = mel.player.pos, h = mel.player.heading || 0, fx = Math.sin(h), fz = Math.cos(h);
      return [p.x - fx * 3, p.y + 3.2, p.z - fz * 3, p.x + fx * 9, p.y + 1, p.z + fz * 9]; })()` },
  wreck: { place: 'crash', settle: 3, why: 'the wreck from above and to the side: the hero moment',
    cam: `(() => { const p = mel.player.pos, C = mel.CRASH.at, dx = C.x - p.x, dz = C.z - p.z, L = Math.hypot(dx, dz), sx = -dz / L, sz = dx / L;
      return [C.x + sx * 16 - dx / L * 6, p.y + 7, C.z + sz * 16 - dz / L * 6, C.x, p.y + .5, C.z]; })()` },
  crash: { place: 'crash', settle: 3, why: 'the wreck from where the new game starts',
    cam: `(() => { const p = mel.player.pos, C = mel.CRASH.at, dx = C.x - p.x, dz = C.z - p.z, L = Math.hypot(dx, dz);
      return [p.x - dx / L * 8, p.y + 4, p.z - dz / L * 8, C.x, p.y + 1, C.z]; })()` },
};

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.wasm': 'application/wasm', '.glb': 'model/gltf-binary', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.ktx2': 'image/ktx2', '.mp3': 'audio/mpeg', '.ogg': 'audio/ogg', '.webmanifest': 'application/manifest+json' };
const server = http.createServer((q, r) => {
  const u = decodeURIComponent(new URL(q.url, 'http://x').pathname), f = path.join(ROOT, u === '/' ? 'index.html' : u);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end(); return; }
  let body = fs.readFileSync(f);
  if (f.endsWith('index.html')) {
    const s = body.toString(), k = 'window.melee = window.mel = {';
    if (!s.includes(k)) { console.error('shot: no mel handle in index.html'); process.exit(1); }
    body = s.replace(k, 'window.__shot = { renderer, scene, camera }; ' + k);
  }
  r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(body);
});
await new Promise(ok => server.listen(0, ok));
const port = server.address().port;

const want = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(SHOTS);
fs.mkdirSync(OUT, { recursive: true });
const t0 = Date.now(), el = () => ((Date.now() - t0) / 1000).toFixed(0) + 's';
const browser = await pw.chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.log('  pageerror', e.message));
let code = 0;
try {
  await page.goto(`http://127.0.0.1:${port}/index.html?w=tkit&god`, { timeout: 120000 });
  await page.waitForFunction(() => document.getElementById('boot').classList.contains('gone') && window.__shot && window.mel, null, { timeout: 180000, polling: 1000 });
  console.log(`booted ${el()} | FARMLAND ${await page.evaluate(() => mel.FARMLAND.live)}`);
  for (const id of want) {
    const S = SHOTS[id]; if (!S) { console.log('no shot', id, '--', Object.keys(SHOTS).join(' ')); code = 1; continue; }
    const went = await page.evaluate(pl => mel.go(pl), S.place);
    await page.waitForTimeout(S.settle * 1000);
    const url = await page.evaluate(cam => {
      const { renderer, scene, camera } = window.__shot, c = eval(cam);
      camera.position.set(c[0], c[1], c[2]); camera.lookAt(c[3], c[4], c[5]); camera.far = Math.max(camera.far, 600); camera.updateProjectionMatrix(); camera.updateMatrixWorld(true);
      renderer.render(scene, camera);
      return renderer.domElement.toDataURL('image/jpeg', .85);
    }, S.cam);
    const f = path.join(OUT, id + '.jpg');
    fs.writeFileSync(f, Buffer.from(url.split(',')[1], 'base64'));
    console.log(`ok  ${id.padEnd(6)} ${el()} at "${went}" -> ${path.relative(ROOT, f)} | ${S.why}`);
  }
} catch (e) { console.log('FAIL', el(), e.message.split('\n')[0]); code = 1; }
await browser.close(); server.close();
process.exit(code);
