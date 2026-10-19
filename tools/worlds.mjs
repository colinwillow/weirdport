// npm run worlds [world ...] -- WHAT EACH WORLD COSTS A PHONE, measured on the shipped page (m416, ROADMAP F0a-1).
//
// Headless Chromium (SwiftShader, the same harness as `npm run shot`) boots the SHIPPED index.html in every world, waits
// for the boot card to go, stands him at the world's GOD places (the spawn, then the regions), lets the frame loop settle
// so the cell culling has done its work, renders one frame from the game's own camera and reads what the renderer did and
// what it holds: draw calls, triangles, the textures every material references and their RESIDENT bytes (a KTX2 at its mip
// chain's size, anything else at w x h x 4 x 4/3), the geometry bytes, and the boot time from the page's start to the
// card going. Against a BUDGET for a phone. Exits 1 on any OVER -- which is the list of what F0a's next builds cut.
//
// The boot time here is SwiftShader's, not a phone's: a ratio between worlds, never a number to believe.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const req = createRequire(import.meta.url);
let pw;
for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright', '/opt/node-tools/node_modules/playwright']) { try { pw = req(p); break; } catch (e) {} }
if (!pw) { console.error('no playwright'); process.exit(1); }

// THE BUDGET. "Draw calls in the low hundreds, textures KTX2, nothing resident that isn't on screen" (ROADMAP F0a).
//   dc     a mobile GPU driver's draw-call overhead is the first thing that costs anything here (CLAUDE.md); 300 a frame
//   kT     a 2023 phone at dpr 2-3 fills ~1M triangles a frame at 30 fps with room for the rest
//   texMB  one 2K RGBA is 22 MB resident; iOS kills a tab somewhere past a gigabyte; 160 MB leaves room for the rest
//   geoMB  vertex buffers; 128 MB
const BUDGET = { dc: 300, kT: 1000, texMB: 160, geoMB: 128 };
// where to stand in each world: the spawn (`''`), then the GOD places that put him in each region
const WORLDS = {
  tkit: ['', 'oldtown', 'camp', 'pearl', 'overlook', 'farmyard', 'hcmill', 'hctrail', 'wfquay', 'wfstacks', 'islanding', 'isneedle', 'isship', 'iscore'],
  toon: ['', 'toon'], kit: ['', 'kit'], weirdport: ['', 'weirdport'], test: ['', 'test'],
  alien: ['', 'awskyway', 'awcoast', 'awsummit', 'awisles', 'awfire', 'awgoo', 'awcrater'],   // m432
  plaza: ['', 'pl_bell_1', 'pl_trig_vault', 'pl_launch_pad', 'pl_fuel_cell', 'pl_portal_exit'],   // m438: Glowtide (its places are its markers, live)
};

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.wasm': 'application/wasm', '.glb': 'model/gltf-binary',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ktx2': 'image/ktx2', '.mp3': 'audio/mpeg', '.webmanifest': 'application/manifest+json' };
const server = http.createServer((q, r) => {
  const u = decodeURIComponent(new URL(q.url, 'http://x').pathname), f = path.join(ROOT, u === '/' ? 'index.html' : u);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end(); return; }
  let body = fs.readFileSync(f);
  if (f.endsWith('index.html')) {
    const s = body.toString(), k = 'window.melee = window.mel = {';
    if (!s.includes(k)) { console.error('worlds: no mel handle in index.html'); process.exit(1); }
    body = s.replace(k, 'window.__shot = { renderer, scene, camera, MISSING, CELL, stepCam, cellStep, perfStep, bodyCull, cam, player, GODPLACES, DUMMIES, PERF }; ' + k);
  }
  r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(body);
});
await new Promise(ok => server.listen(0, ok));
const port = server.address().port;
const WHO = process.argv.includes('--who');     // print who draws at every place
const AT = (process.argv.find(a => a.startsWith('--at=')) || '').slice(5).split(',').filter(Boolean);   // only these places
const want = process.argv.slice(2).filter(a => !a.startsWith('--')).length ? process.argv.slice(2).filter(a => !a.startsWith('--')) : Object.keys(WORLDS);
const t0 = Date.now(), el = () => ((Date.now() - t0) / 1000).toFixed(0) + 's';
const browser = await pw.chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const rows = [];
let code = 0;
for (const w of want) {
  const places = AT.length ? AT : WORLDS[w]; if (!places) { console.log('no world', w, '--', Object.keys(WORLDS).join(' ')); code = 1; continue; }
  const page = await browser.newPage({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 1 });
  const errs = []; page.on('pageerror', e => errs.push(e.message.split('\n')[0]));
  const tw = Date.now();
  try {
    await page.goto(`http://127.0.0.1:${port}/index.html?w=${w}&god`, { timeout: 120000 });
    await page.waitForFunction(() => document.getElementById('boot').classList.contains('gone') && window.__shot && window.mel, null, { timeout: 240000, polling: 1000 });
    const boot = await page.evaluate(() => ({ ms: mel.PERF.bootMs, notes: (window.__shot.MISSING || []).join(', ') }));
    const R = { w, bootS: boot.ms / 1000, wall: (Date.now() - tw) / 1000, at: [], errs, notes: boot.notes.trim() };
    for (const pl of places) {
      const went = pl ? await page.evaluate(id => mel.go(id), pl) : 'spawn';
      // THE HEADING IS SET, NOT INHERITED: a place with no heading of its own kept the last place's, and Old Town read 534 one
      // run and 678 the next depending on which way he arrived. The place's own `at()[3]` if it has one, else due +z.
      await page.evaluate(id => { const S = window.__shot, P = id && S.GODPLACES.find(q => q.id === id); let a = null; try { a = P && P.at && P.at(); } catch (e) {}
        const h = a && a[3] != null ? a[3] : 0; S.cam.az = S.player.faceH = S.player.heading = h; }, pl);
      // THE GAME'S OWN LOOP IS NOT WAITED FOR. Under SwiftShader it runs seconds a frame (or not at all for a minute), and a
      // 2.5 s wait measured the THREE camera where the LAST place had left it (pearl and overlook came back identical): `godPlace`
      // moves `cam.pos`, but only `stepCam` copies that into the camera. So the move is settled by hand -- `stepCam` ten times
      // (the camera arrives at `cam.pos`), then `cellStep` (the fog culling), then the one frame we read.
      await page.waitForTimeout(300);
      const m = await page.evaluate(() => { const S = window.__shot; for (let k = 0; k < 10; k++) S.stepCam(1 / 30);
        // the body cull is `bodyCull` (m417 put it there, not in `perfStep`): it reads the camera's inverse, which `render` would
        // refresh -- so refresh it by hand, then cull, then the fog and far-copy pass
        S.camera.updateMatrixWorld(true); S.camera.matrixWorldInverse.copy(S.camera.matrixWorld).invert(); for (let k = 0; k < 3; k++) S.bodyCull(); S.cellStep();
        // WHO is drawing: every draw call of this frame counted by the object's family -- its name with the digits taken out, or
        // the nearest named ancestor's -- so an OVER has a name to cut rather than a number to stare at
        const who = {}, R = S.renderer, orig = R.renderBufferDirect, fam = o => { for (let a = o; a; a = a.parent) { const n = a.name || (a === o && a.material && a.material.name ? 'mat:' + a.material.name : '') || (a.userData && a.userData.fbatch !== undefined ? 'fbatch' : ''); if (n) return n.replace(/[0-9]+/g, '#').replace(/_i_#$/, '').slice(0, 26); }
          // nameless all the way up: say what it IS -- the geometry, the material, a map, instanced, skinned -- and how many vertices
          const g = o.geometry, m = o.material, nv = g && g.attributes.position ? g.attributes.position.count : 0;
          return (o.isInstancedMesh ? 'inst:' : o.isSkinnedMesh ? 'skin:' : o.isSprite ? 'sprite:' : '') + (g ? g.type.replace('Geometry', '') : '?') + '/' + (m ? m.type.replace('Mesh', '').replace('Material', '') : '?') + (m && m.map ? ':map' : '') + (m && m.transparent ? ':tr' : '') + ' v' + (nv < 1000 ? nv : (nv / 1000).toFixed(0) + 'k'); };
        const where = {}; R.renderBufferDirect = function (cam, sc, geo, mat, obj, grp) { const k = fam(obj); who[k] = (who[k] || 0) + 1;
          if (!obj.name && !(obj.material && obj.material.name)) { const L = where[k] || (where[k] = []); if (L.length < 4) { obj.updateWorldMatrix(true, false); const e = obj.matrixWorld.elements, P = { x: e[12], y: e[13], z: e[14] }; let chain = []; for (let a = obj.parent; a && a !== sc; a = a.parent) chain.push(a.name || a.type); L.push(P.x.toFixed(0) + ',' + P.y.toFixed(0) + ',' + P.z.toFixed(0) + (chain.length ? ' <' + chain.join('<') : ' <scene') + (obj.material && obj.material.color ? ' #' + obj.material.color.getHexString() : '')); } }
          return orig.call(this, cam, sc, geo, mat, obj, grp); };
        S.renderer.render(S.scene, S.camera); R.renderBufferDirect = orig; const top = Object.entries(who).sort((a, b) => b[1] - a[1]).slice(0, 14).map(([k, v]) => k + ' ' + v + (where[k] ? ' {' + where[k].join(' | ') + '}' : '')); const i = S.renderer.info.render, M = mel.perfMem(6);
        return { dc: i.calls, kT: i.triangles / 1000, tex: M.tex, texMB: M.texMB, geo: M.geo, geoMB: M.geoMB, top: M.top, topG: M.topG, glTex: M.glTex, glGeo: M.glGeo, programs: M.programs, cells: (S.CELL && S.CELL.list.length ? S.CELL.shown + '/' + S.CELL.list.length : '-'), who: top,
          bodies: (() => { const cp = S.camera.position; let vis = 0, near = 0, all = 0; for (const d of S.DUMMIES) { if (d.gone || !d.root) continue; all++; if (d.root.visible) vis++; if (Math.hypot(d.root.position.x - cp.x, d.root.position.z - cp.z) <= (S.PERF.bodyFar || 1e9)) near++; } return vis + ' drawn/' + near + ' near/' + all; })(), md: S.PERF.multi ? 1 : 0 }; });
      R.at.push({ pl: pl || 'spawn', went, ...m });
    }
    rows.push(R);
    const worst = R.at.reduce((a, b) => (b.dc > a.dc ? b : a), R.at[0]), m0 = R.at[0];
    console.log(`\n== ${w}  boot ${R.bootS.toFixed(1)} s (swiftshader)  ${m0.tex} textures ${m0.texMB.toFixed(0)} MB (gl ${m0.glTex})  ${m0.geo} geometries ${m0.geoMB.toFixed(0)} MB (gl ${m0.glGeo})  ${m0.programs} programs  ${el()}` + (R.notes ? `  NOTE: ${R.notes}` : '') + (errs.length ? `  PAGEERROR: ${errs[0]}` : ''));
    for (const a of R.at) { console.log(`   ${a.pl.padEnd(10)} ${String(a.dc).padStart(5)} DC ${a.kT.toFixed(0).padStart(5)} kT  cells ${a.cells.padEnd(8)}` + (a.dc > BUDGET.dc ? '  OVER dc' : '') + (a.kT > BUDGET.kT ? '  OVER kT' : ''));
      if (WHO) console.log(`              who: ${a.who.join(', ')}  | bodies ${a.bodies}${a.md ? ' | multi-draw' : ''}`); }
    console.log(`   textures: ${m0.top.join(', ')}`); console.log(`   geometry: ${m0.topG.join(', ')}`);
    const over = []; if (worst.dc > BUDGET.dc) over.push(`dc ${worst.dc} > ${BUDGET.dc} at ${worst.pl}`); if (worst.kT > BUDGET.kT) over.push(`kT ${worst.kT.toFixed(0)} > ${BUDGET.kT}`);
    if (m0.texMB > BUDGET.texMB) over.push(`textures ${m0.texMB.toFixed(0)} MB > ${BUDGET.texMB}`); if (m0.geoMB > BUDGET.geoMB) over.push(`geometry ${m0.geoMB.toFixed(0)} MB > ${BUDGET.geoMB}`);
    R.over = over; if (over.length || errs.length) code = 1;
    console.log(`   ${over.length ? 'OVER: ' + over.join(' | ') : 'inside the budget'}`);
  } catch (e) { console.log(`\n== ${w}  FAIL ${el()} ${e.message.split('\n')[0]}` + (errs.length ? `  PAGEERROR: ${errs[0]}` : '')); code = 1; }
  await page.close();
}
console.log(`\nbudget: ${BUDGET.dc} DC, ${BUDGET.kT} kT, ${BUDGET.texMB} MB textures, ${BUDGET.geoMB} MB geometry | ` + rows.map(R => `${R.w} ${R.over.length ? 'OVER' : 'ok'}`).join(', ') + ` | ${el()}`);
await browser.close(); server.close();
process.exit(code);
