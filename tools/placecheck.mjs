// npm run places -- DO THE PLACES GOD MODE LISTS ACTUALLY EXIST IN THE REAL KIT CITY?
//
// Builds the kit city's REAL collider (his collision GLB, plus the visual's lots and dirt decoded
// with draco, the way `buildTCity` captures them), the island, and every farm builder, then calls
// the shipped `godPlace` for each GOD place in `tkit` and prints where it put the player.
// Written because the farm was built for nine builds against a ground it does not fit on: the real
// island ring is 14.9 m wide at its widest, `buildFarm` wants 18, it returned with
// `FARM NO ROOM 15`, and every farm place in the GOD menu went nowhere. (m302: that 14.9 was itself
// misread -- the grass index was wrong, see `ISLE_J0` -- but the farm still did not exist, which is
// the half that mattered. It now exits 1 when any tkit GOD place is BAD.) A place that does not
// exist in the real world is not built, however good it looks in a fabricated test.
import fs from 'fs';
import os from 'os';
import path from 'path';
import { pathToFileURL } from 'url';

// ---- AND IT IS SEEDED, BECAUSE A RANDOMLY RED ROW IS WORSE THAN A PERMANENTLY RED ONE ----
// `foeRoll` gives every body its own pace, nerve, react and guard out of `Math.random`, which is
// exactly right in the game and makes this suite report a different answer every run: two rows
// failed one run and one the next, on code that had not changed. A result you cannot reproduce
// is not a measurement, and a suite that cries wolf every third run is a suite nobody reads.
// One fixed stream, so a red row is a fact about the code and can be chased.
// **THE VARIETY CASES STILL MEAN SOMETHING** -- they roll MANY bodies out of this one stream, so
// what they measure is the spread across a roster rather than one lucky draw.
let _seed = 0x2f6e2b1;
Math.random = () => { _seed = (_seed * 1664525 + 1013904223) >>> 0; return _seed / 4294967296; };

// ---- the same headless page the boot gate builds, lifted between its own markers ----
const boot = fs.readFileSync('tools/boot.mjs', 'utf8');
const stubs = boot.slice(boot.indexOf('// STUBS:START'), boot.indexOf('// STUBS:END'));
(0, eval)(stubs);

if (!fs.existsSync('node_modules/three/package.json')) {
  fs.mkdirSync('node_modules/three', { recursive: true });
  fs.writeFileSync('node_modules/three/package.json', JSON.stringify({
    name: 'three', version: '0.180.0-vendored', type: 'module', main: 'index.js', exports: { '.': './index.js' } }));
  fs.writeFileSync('node_modules/three/index.js', "export * from '../../vendor/three.module.min.js';\n");
}
const TMP = path.join(os.tmpdir(), 'melee-sim');
fs.mkdirSync(TMP, { recursive: true });
const ROOT = pathToFileURL(process.cwd() + '/').href;
fs.writeFileSync(path.join(TMP, 'three-shim.mjs'), `
export * from '${ROOT}vendor/three.module.min.js';
import * as T from '${ROOT}vendor/three.module.min.js';
class R { constructor(){ this.domElement = globalThis.document.createElement('canvas');
  this.shadowMap={enabled:false,type:0}; this.info={autoReset:true,render:{calls:0,triangles:0},reset(){}};
  this.extensions={has:()=>false,get:()=>undefined,init(){}}; this.capabilities={isWebGL2:true,getMaxAnisotropy:()=>1,precision:'highp'};
  this.outputColorSpace=''; this.toneMapping=0; this.toneMappingExposure=1; }
  setSize(){} setPixelRatio(){} setClearColor(){} setRenderTarget(){} clear(){} render(){} dispose(){}
  compile(){} initTexture(){} getContext(){return{getParameter:()=>0};} getDrawingBufferSize(v){return v.set(1280,720);} }
export { R as WebGLRenderer };
class T2 { constructor(){ this.texture = new T.Texture(); } setSize(){} dispose(){} }
export { T2 as WebGLRenderTarget };
class P { fromEquirectangular(){ return { texture: new T.Texture() }; } compileEquirectangularShader(){} dispose(){} }
export { P as PMREMGenerator };
`);
const html = fs.readFileSync('index.html', 'utf8');
let src = html.match(/<script type="module">([\s\S]*?)<\/script>/)[1];
src = src.replace(/(from\s*)['"]three['"]/g, `$1'${pathToFileURL(path.join(TMP, 'three-shim.mjs')).href}'`)
         .replace(/(from\s*)['"]\.\/vendor\//g, `$1'${ROOT}vendor/`);
src += '\nglobalThis.__M = { mapRegionsTkit, buildCamp, OTCAMP, MAPREG, campStep, FARMLAND, buildFarmland, buildFarmWaters, FWATER, buildFieldBounds, FPLAN, buildFieldCrops, FCROP, buildNeighbours, FNEIGH, COW, COWS, cowSpook, fpOwnAt, flLocal, buildVehicles, FVEH, vehStep, buildFarmhands, FHANDS, MARKS, mkrNpcPlace, HOBO, HICK, buildTownEdge, FTOWN, buildCityRing, FRING, farmBatch, FBATCH, scene, buildTrestle, FTRES, buildFord, FFORD, GATES, buildOrchardTerrace, FTERR, buildSkyline, SKYLINE, skylineStep, flEdgeAt, isleBedAt, KCITY, buildKCityCol, buildIsle, ISLE, TRI, triBuild, groundAt, WORLD, MOVE, player, kitPopulate, KCROWD, FOE, HICK, HOBO, SKATER, BIKER, DUMMY, CIVILS, CLANCY, kitStand, bodySeat, SEAT, DUMMIES, THREE, buildFarm, buildFarmProps, buildCrash, buildLane, buildBridge, buildCows, buildHedgerows, HROW, buildFarmhouse, FHOUSE, farmhouseStep, buildRoadside, FROAD, GPAINT, buildGroundPaint, buildFlora, crashHero, FARM, MISSING, FLORA, FPROPS, farmPropsStep, floraStep, cowStep, crashStep, crashHeroStep, riverStep, gradeStep, CRASH, GODPLACES, godPlace, GOD, LANE, BRIDGE, crashSpawn, SAVE };\n';
const f2 = path.join(TMP, 'placecheck.mjs'); fs.writeFileSync(f2, src);
const quiet = console.error, qw = console.warn, ql = console.log;
console.error = () => {}; console.warn = () => {};
await import(pathToFileURL(f2).href + '?t=' + Date.now());
await new Promise(r => setTimeout(r, 250));
console.error = quiet; console.warn = qw;
const M = globalThis.__M;
M.WORLD.now = 'tkit';
// the collision file as a scene, read straight out of the GLB (it is not draco)
const { openGLB } = await import(ROOT + 'tools/glb.mjs');
const T = await import(ROOT + 'vendor/three.module.min.js');
const { json: g, read } = openGLB('models/toon_city_kit/toon_city_collision.glb');
const objs = g.nodes.map(n => { const o = new T.Object3D(); o.name = n.name || '';
  if (n.translation) o.position.fromArray(n.translation); if (n.rotation) o.quaternion.fromArray(n.rotation); if (n.scale) o.scale.fromArray(n.scale); return o; });
g.nodes.forEach((n, i) => {
  (n.children || []).forEach(c => objs[i].add(objs[c]));
  if (n.mesh == null) return;
  for (const pr of g.meshes[n.mesh].primitives) {
    const geo = new T.BufferGeometry();
    geo.setAttribute('position', new T.BufferAttribute(new Float32Array(read(pr.attributes.POSITION)), 3));
    if (pr.indices != null) geo.setIndex(new T.BufferAttribute(new Uint32Array(read(pr.indices)), 1));
    const m = new T.Mesh(geo, new T.MeshBasicMaterial()); m.name = n.name || ''; objs[i].add(m);
  }
});
const scene = new T.Group(); for (const i of g.scenes[0].nodes) scene.add(objs[i]); scene.updateMatrixWorld(true);
const FILL = [];
// ---- THE DRAWN GROUND against the collider, on a 0.5 m grid
const VH = await import(ROOT + 'tools/vishelp.mjs');
const { json: vg, bin } = VH.readGLB('models/toon_city_kit/toon_city_visual.glb');
const W = VH.nodeWorld(vg), C = .5, X0 = -95, NX = 380;
const top = new Float32Array(NX * NX).fill(-9), who = new Array(NX * NX);
for (let i = 0; i < vg.nodes.length; i++) {
  const n = vg.nodes[i]; if (n.mesh === undefined || !/^(ground_wr|road_wr)/.test(n.name || '')) continue; const fill = /^ground_wr_(lots|dirt)/.test(n.name);
  for (const pr of vg.meshes[n.mesh].primitives) {
    const d = await VH.decodePrim(vg, bin, pr); if (!d) continue;
    const p = d.pos, ix = d.index, m = W[i];
    for (let t = 0; t < ix.length; t += 3) {
      const P = [0, 1, 2].map(k => VH.xf(m, p[ix[t + k] * 3], p[ix[t + k] * 3 + 1], p[ix[t + k] * 3 + 2])); if (fill) FILL.push(...P[0], ...P[1], ...P[2]);
      const ux = P[1][0] - P[0][0], uy = P[1][1] - P[0][1], uz = P[1][2] - P[0][2], vx = P[2][0] - P[0][0], vy = P[2][1] - P[0][1], vz = P[2][2] - P[0][2];
      const ny = uz * vx - ux * vz, nl = Math.hypot(uy * vz - uz * vy, ny, ux * vy - uy * vx);
      if (nl < 1e-9 || Math.abs(ny / nl) < .7) continue;
      const x0 = Math.min(P[0][0], P[1][0], P[2][0]), x1 = Math.max(P[0][0], P[1][0], P[2][0]);
      const z0 = Math.min(P[0][2], P[1][2], P[2][2]), z1 = Math.max(P[0][2], P[1][2], P[2][2]);
      for (let gx = Math.max(0, Math.ceil((x0 - X0) / C)); gx <= Math.min(NX - 1, Math.floor((x1 - X0) / C)); gx++)
        for (let gz = Math.max(0, Math.ceil((z0 - X0) / C)); gz <= Math.min(NX - 1, Math.floor((z1 - X0) / C)); gz++) {
          const x = X0 + gx * C, z = X0 + gz * C;
          const d0 = (P[1][2] - P[2][2]) * (P[0][0] - P[2][0]) + (P[2][0] - P[1][0]) * (P[0][2] - P[2][2]);
          const l1 = ((P[1][2] - P[2][2]) * (x - P[2][0]) + (P[2][0] - P[1][0]) * (z - P[2][2])) / d0;
          const l2 = ((P[2][2] - P[0][2]) * (x - P[2][0]) + (P[0][0] - P[2][0]) * (z - P[2][2])) / d0, l3 = 1 - l1 - l2;
          if (l1 < -1e-6 || l2 < -1e-6 || l3 < -1e-6) continue;
          const h = l1 * P[0][1] + l2 * P[1][1] + l3 * P[2][1], o = gx * NX + gz;
          if (h > top[o]) { top[o] = h; who[o] = n.name; }
        }
    }
  }
}
M.KCITY.fill.push(new Float32Array(FILL));
console.log = () => {};
M.buildKCityCol({ scene });
try { M.buildIsle(); } catch (e) { quiet('isle', e.message); }
console.log = ql;

const farmSteps = ['buildFarmland','buildFarmWaters','buildOrchardTerrace','buildFieldBounds','buildFieldCrops','buildNeighbours','buildFarm','buildFarmProps','buildCrash','crashHero','buildLane','buildBridge','buildHedgerows','buildFarmhouse','buildRoadside','buildCows','buildVehicles','buildFarmhands','mapRegionsTkit','buildCamp','buildTownEdge','buildCityRing','buildTrestle','buildFord','buildSkyline','farmBatch','buildGroundPaint','buildFlora'];
console.log = () => {};
for (const n of farmSteps) { try { M[n](); quiet('ok  ', n); } catch (e) { quiet('FAIL', n, e && e.stack ? e.stack.split('\n').slice(0,3).join(' | ') : e); } }
console.log = ql;
// the grass a ray really has is its own `gw` (m302: `smp[12]` was a fifth of the way across it -- see `ISLE_J0`)
{ const R = M.ISLE.rays; let w = R[0];
  for (const r of R) if (r.gw > w.gw) w = r;
  const H = M.ISLE.head, hr = R[((Math.round(H.th / (Math.PI * 2) * R.length) % R.length) + R.length) % R.length];
  quiet('widest grass', w.gw.toFixed(1), 'at', (Math.atan2(w.dz, w.dx) * 180 / Math.PI).toFixed(0) + 'deg', '| headland ray', (H.th * 180 / Math.PI).toFixed(0) + 'deg',
        'grass', hr.gw.toFixed(1), 'need', M.FARM.need, '| rays', R.length, 'rect', JSON.stringify(M.ISLE.rect.map(v => +v.toFixed(1)))); }
quiet('FARM.at', JSON.stringify(M.FARM.at && { x: +M.FARM.at.x.toFixed(1), z: +M.FARM.at.z.toFixed(1), th: +M.FARM.at.th.toFixed(3) }),
      '| CRASH.at', M.CRASH.at ? 'yes' : 'NO', '| LANE.at', M.LANE.at ? 'yes' : 'NO', '| BRIDGE.gate', M.BRIDGE.gate ? 'yes (side ' + M.BRIDGE.side + ')' : 'NO', '| ISLE.live', M.ISLE.live);
quiet('FARMLAND', M.FARMLAND.live ? 'live' : 'NOT BUILT', M.FARMLAND.O && M.FARMLAND.O.map(v => +v.toFixed(0)), 'chunks', M.FARMLAND.chunks, 'floor tris', M.FARMLAND.tris, 'water tris', M.FARMLAND.wtris,
  '| BRIDGE len', M.BRIDGE.len && +M.BRIDGE.len.toFixed(0), 'piers', M.BRIDGE.piers, 'gate', JSON.stringify(M.BRIDGE.gate && [+M.BRIDGE.gate.x.toFixed(0), +M.BRIDGE.gate.z.toFixed(0)]));
quiet('FWATER', M.FWATER.n, 'boxes, reeds', M.FWATER.reeds, '| pond level', M.FARMLAND.pondY && +M.FARMLAND.pondY.toFixed(2), '| creek bed', M.FARMLAND.cbed && [+M.FARMLAND.cbed.y[0].toFixed(2), +M.FARMLAND.cbed.y[M.FARMLAND.cbed.y.length - 1].toFixed(2)], 'len', M.FARMLAND.cbed && +M.FARMLAND.cbed.len.toFixed(0));
{ const P = M.FPLAN; const cnt = {}; if (P.owners) for (const o of P.owners) cnt[o] = (cnt[o] || 0) + 1;
  const area = o => ((cnt[o] || 0) * P.grid * P.grid / 1000).toFixed(1) + 'k';
  quiet('FPLAN', P.n, 'boxes: hedge', P.pieces, 'fence', P.fences, 'hedge oaks', P.trees, 'tree line', P.lines, '| m2:', 'margins', area(-1), P.yards.map((y, k) => y.id + ' ' + area(-2 - k)).join(', '), P.FIELDS.map((f, i) => f.id + ' ' + area(i)).join(', ')); }
quiet('FCROP', M.FCROP.n, 'clumps in', M.FCROP.chunks.length, 'chunks', JSON.stringify(M.FCROP.per));
{ const by = {}; for (const c of M.COWS) { const k = c.field == null ? 'paddock' : M.FPLAN.FIELDS[c.field].id; by[k] = (by[k] || 0) + 1; }
  // every herd cow starts INSIDE its own pasture (its owner on the lattice is its field)
  const astray = M.COWS.filter(c => c.field != null && M.fpOwnAt(...M.flLocal(c.x, c.z)) !== c.field).length;
  globalThis.__cowBad = astray;          // `bad` is declared below: carried, not read above its own `let`
  quiet((astray ? 'BAD ' : 'ok  ') + 'COWS', M.COW.n, JSON.stringify(by), astray ? astray + ' OUTSIDE THEIR PASTURE' : 'all in their pastures'); }
quiet('FVEH', M.FVEH.list.map(c => c.id + ' ' + c.pts.length + ' pts').join(', '));
// m332: and each npc mark RESOLVES TO A KIND (`mkrNpcPlace` -> `mkrKind`) -- from m293 none did (`mphName` is the display
// form, the stems are files), so not one farmhand ever existed while this row said ok off the marks' positions alone
try { M.mkrNpcPlace(); } catch (e) { quiet('mkrNpcPlace throw', e.message); }
// (m334: the checkpoint's officers are `town` -- at the bridge's town end, within 12 m of `BRIDGE.gate` rather than on the farmland)
{ const F = M.MARKS.filter(m => m.src === 'FARMHANDS'), G = M.BRIDGE.gate, nok = F.filter(m => !m.K);
  const off = F.filter(m => m.p.town ? !(G && Math.hypot(m.x - G.x, m.z - G.z) < 12) : !(M.flEdgeAt(m.x, m.z) > 0));
  if (off.length + nok.length) globalThis.__cowBad = (globalThis.__cowBad || 0) + off.length + nok.length;
  quiet((off.length + nok.length ? 'BAD ' : 'ok  ') + 'FARMHANDS', F.map(m => m.p.name + ' (' + m.p.kind + ' -> ' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ') ' + m.x.toFixed(0) + ',' + m.z.toFixed(0)).join(' | '),
    off.length ? off.length + ' OFF THE FARMLAND (or away from the checkpoint)' : '', nok.length ? nok.length + ' WITH NO KIND' : ''); }
{ let meshes = 0; M.scene.traverse(o => { if (o.isMesh && o.visible) meshes++; });
  quiet('FBATCH', M.FBATCH.on ? 'on' : 'OFF', M.FBATCH.before, 'static meshes ->', M.FBATCH.after, 'batched,', M.FBATCH.kept, 'left out,', M.FBATCH.tris, 'tris | meshes in the scene now', meshes); }
{ const C = M.MARKS.filter(m => m.src === 'CAMP'), R = M.ISLE.rect, bad2 = C.filter(m => !m.K || !(m.x > R[0] && m.x < R[1] && m.z > R[2] && m.z < R[3]));
  if (bad2.length || !C.length) globalThis.__cowBad = (globalThis.__cowBad || 0) + Math.max(1, bad2.length);
  quiet((bad2.length || !C.length ? 'BAD ' : 'ok  ') + 'CAMP', C.map(m => m.p.name + ' (' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ') ' + m.x.toFixed(0) + ',' + m.z.toFixed(0)).join(' | ') || 'NOBODY',
    '| fire at', JSON.stringify(M.OTCAMP.fireAt && M.OTCAMP.fireAt.map(v => +v.toFixed(1))), '| regions', JSON.stringify((M.MAPREG.tkit || []).map(r => r.id + ' ' + [r.x0, r.x1, r.z0, r.z1].map(v => Math.round(v)).join(',')))); }
quiet('FFORD', M.FFORD.n, 'stones over', M.FFORD.at && M.FFORD.cityAt && +Math.hypot(M.FFORD.cityAt[0] - M.FFORD.at[0], M.FFORD.cityAt[1] - M.FFORD.at[1]).toFixed(1), 'm, washed gap', M.FFORD.gapM && +M.FFORD.gapM.toFixed(1), 'm | culvert', JSON.stringify(M.FWATER.culvertAt && M.FWATER.culvertAt.map(v => +v.toFixed(1))), 'bed', M.FWATER.culvertY && +M.FWATER.culvertY.toFixed(2));
quiet('GATES', M.GATES.map(g => g.id + ' ' + g.type + ' w' + g.w.toFixed(1) + ' y' + g.y.toFixed(2) + ' @' + g.x.toFixed(0) + ',' + g.z.toFixed(0)).join(' | ') || 'NONE');
quiet('FTERR', M.FTERR.n, 'wall pieces,', M.FTERR.trees, 'apple trees, tiers', JSON.stringify(M.FTERR.top.map(v => +v.toFixed(2))), 'steps', M.FTERR.steps.length, 'base R', M.FTERR.R ? [+Math.min(...M.FTERR.R).toFixed(1), +Math.max(...M.FTERR.R).toFixed(1)] : 'NONE');
quiet('SKYLINE', M.SKYLINE.n, 'boxes, centre', JSON.stringify(M.SKYLINE.c && M.SKYLINE.c.map(v => Math.round(v))), M.SKYLINE.g ? 'one mesh' : 'NOT BUILT');
quiet('FTRES', M.FTRES.n, 'boxes+tris, farm end', JSON.stringify(M.FTRES.at && M.FTRES.at.map(v => +v.toFixed(1))), 'city end', JSON.stringify(M.FTRES.cityAt && M.FTRES.cityAt.map(v => +v.toFixed(1))));
quiet('FTOWN', M.FTOWN.n, 'boxes, poles', M.FTOWN.poles, '| FRING', M.FRING.n, 'boxes, houses', M.FRING.houses, 'trees', M.FRING.trees);
quiet('FROAD', M.FROAD.n, 'road pts', M.GPAINT.roadPts ? M.GPAINT.roadPts.length : 'NONE', 'foot', JSON.stringify(M.BRIDGE.foot && M.BRIDGE.foot.map(v => +v.toFixed(1))), '|', 'FHOUSE', M.FHOUSE.n, 'chimney', JSON.stringify(M.FHOUSE.chim && M.FHOUSE.chim.map(v => +v.toFixed(1))), '|', 'HROW', M.HROW.n, 'boxes', M.HROW.trees, 'trees', M.HROW.gates, 'gates | FLORA', JSON.stringify(M.FLORA.counts));
quiet('notes', JSON.stringify(M.MISSING));
globalThis.toast = (t) => {};
let bad = globalThis.__cowBad || 0;
for (const P of M.GODPLACES.filter(p => p.world === 'tkit')) {
  M.player.pos.set(0, 0, 0);
  let a = null; try { a = P.at && P.at(); } catch (e) { a = 'THROW ' + e.message; }
  try { M.godPlace(P); } catch (e) { quiet('godPlace throw', P.id, e.message); }
  const p = M.player.pos, g = M.groundAt(p.x, p.z, p.y + .3, .6), R = M.ISLE.rect;   // m327: the floor UNDER him, from his own height
  const city = p.x > R[0] && p.x < R[1] && p.z > R[2] && p.z < R[3];
  // sensible: it moved him, he is not under the sea, and a farm place is OUT on the island, not in the city
  // m306: a farm place is ON THE FARMLAND (its own landmass), except the bridge's checkpoint, which is on the deck
  const CITYP = ['oldtown', 'camp'];                         // m335: places that are IN Old Town on purpose
  const offLand = M.FARMLAND.live && !['oldtown', 'camp', 'bridge', 'warehouse', 'backyards', 'stones'].includes(P.id) && !(M.flEdgeAt(p.x, p.z) > 0);
  const why = !a ? 'NO PLACE' : (p.x === 0 && p.z === 0 && P.id !== 'oldtown') ? 'UNMOVED' : p.y < M.ISLE.sea + .3 ? 'IN THE SEA'
            : (!CITYP.includes(P.id) && city) ? 'IN THE CITY' : offLand ? 'OFF THE FARMLAND' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + P.id.padEnd(10), '-> player', p.toArray().map(v => v.toFixed(1)).join(','), 'ground', (g > -500 ? g.toFixed(2) : 'none'), why);
}
// ---- THE NEW GAME LANDS AT THE WRECK (m321, STEER step 8): chapter 0, never in town, the shipped `crashSpawn`
{ const S = M.SAVE, ch = S.ch, it = S.flags.inTown; S.ch = 0; S.flags.inTown = false; M.player.pos.set(0, 0, 0);
  let r = 0; try { r = M.crashSpawn(); } catch (e) { quiet('crashSpawn throw', e.message); }
  const p = M.player.pos, C = M.CRASH.at, d = C ? Math.hypot(C.x - p.x, C.z - p.z) : -1, g = M.groundAt(p.x, p.z, 4, 8);
  const why = !r ? 'DID NOT SPAWN' : d > 30 ? 'FAR FROM THE WRECK' : !(g > M.ISLE.sea + .3) ? 'NO GROUND' : !(M.flEdgeAt(p.x, p.z) > 0) ? 'OFF THE FARMLAND' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'NEW GAME  -> player', p.x.toFixed(1) + ',' + p.z.toFixed(1), 'ground', g > -500 ? g.toFixed(2) : 'none', '|', d.toFixed(1), 'm from the wreck', why);
  S.ch = ch; S.flags.inTown = it; }
quiet(bad ? bad + ' GOD place(s) BAD' : 'every tkit GOD place is somewhere');
// ---- AND THE FARM'S OWN STEPS RUN (m302). Until m302 none of them had ever run against a real farm -- they all
// return early on a null `FARM.at` -- and one that throws is caught by `frame()` and aborts EVERY frame from there
// on: a frozen picture with a crash card. A second at 30 fps, standing at the crash, each step on its own.
{ const crash = M.GODPLACES.find(q => q.id === 'crash'); if (crash) M.godPlace(crash);
  quiet('cowSpook', M.cowSpook(), '(m329: so the 30 frames below run the stampede branch too)');
  for (const n of ['vehStep', 'farmPropsStep', 'farmhouseStep', 'floraStep', 'cowStep', 'crashStep', 'crashHeroStep', 'riverStep', 'gradeStep', 'skylineStep', 'campStep']) {
    let err = null;
    console.log = () => {};
    for (let f = 0; f < 30 && !err; f++) { try { M[n](1 / 30); } catch (e) { err = e; } }
    console.log = ql;
    if (err) bad++;
    quiet((err ? 'BAD ' : 'ok  ') + n.padEnd(14), err ? (err.stack || String(err)).split('\n').slice(0, 3).join(' | ') : '30 frames');
  } }
process.exit(bad ? 1 : 0);
