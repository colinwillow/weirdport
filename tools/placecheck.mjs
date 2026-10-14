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
src += '\nglobalThis.__M = { buildPearlRoofs, pearlFace, KCLIMB, OPLAZA, buildPearlPlaza, plazaStep, plazaStart, pearlCrowd, OPEARL, buildPearl, OGOOD, buildGoodKiosks, RUMOURS, upApply, UPGRADES, JUICE, SAMPLE, OLOOK, buildLookout, lookoutStep, KCLIMB, UPLIFT, buildUplift, cyborgStep, resolveBoxes, SMART, smartStep, ROSTER, rosterKind, OAMP, buildAmp, ampStep, ampBoil, OWATCH, buildWatcher, watchStep, OORB, AIRT, buildOrbs, orbStep, OINCUR, incurStart, incurStep, protestBrawl, OPROTEST, buildProtest, protestStep, protestStart, OSTRIKE, buildStrike, strikeSet, strikeStep, OTSITE, ODECAY, buildDecay, decayApply, decayStep, DHEALTH, dhStep, dhGet, dhPush, FIRES, FOOT, buildFootbridge, footStep, footFix, BOXES, PORTALS, QUESTS, buildLife, OTLIFE, buildSite, OTSITE, buildCarts, OTCARTS, cartStep, mapRegionsTkit, buildCamp, OTCAMP, MAPREG, campStep, FARMLAND, buildFarmland, buildFarmWaters, FWATER, buildFieldBounds, FPLAN, buildFieldCrops, FCROP, buildNeighbours, FNEIGH, COW, COWS, cowSpook, fpOwnAt, flLocal, buildVehicles, FVEH, vehStep, buildFarmhands, FHANDS, MARKS, mkrNpcPlace, HOBO, HICK, buildTownEdge, FTOWN, buildCityRing, FRING, farmBatch, FBATCH, scene, buildTrestle, FTRES, buildFord, FFORD, GATES, buildOrchardTerrace, FTERR, buildSkyline, SKYLINE, skylineStep, flEdgeAt, isleBedAt, KCITY, buildKCityCol, buildIsle, ISLE, TRI, triBuild, groundAt, WORLD, MOVE, player, kitPopulate, KCROWD, FOE, HICK, HOBO, SKATER, BIKER, DUMMY, CIVILS, CLANCY, kitStand, bodySeat, SEAT, DUMMIES, THREE, buildFarm, buildFarmProps, buildCrash, buildLane, buildBridge, buildCows, buildHedgerows, HROW, buildFarmhouse, FHOUSE, farmhouseStep, buildRoadside, FROAD, GPAINT, buildGroundPaint, buildFlora, crashHero, FARM, MISSING, FLORA, FPROPS, farmPropsStep, floraStep, cowStep, crashStep, crashHeroStep, riverStep, gradeStep, CRASH, GODPLACES, godPlace, GOD, LANE, BRIDGE, crashSpawn, SAVE };\n';
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

const farmSteps = ['buildFarmland','buildFarmWaters','buildOrchardTerrace','buildFieldBounds','buildFieldCrops','buildNeighbours','buildFarm','buildFarmProps','buildCrash','crashHero','buildLane','buildBridge','buildHedgerows','buildFarmhouse','buildRoadside','buildCows','buildVehicles','buildFarmhands','mapRegionsTkit','buildCamp','buildCarts','buildSite','buildLife','buildProtest','buildOrbs','buildWatcher','buildAmp','buildUplift','buildLookout','buildGoodKiosks','buildFootbridge','buildDecay','buildPearl','buildPearlPlaza','buildPearlRoofs','buildStrike','buildTownEdge','buildCityRing','buildTrestle','buildFord','buildSkyline','farmBatch','buildGroundPaint','buildFlora'];
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
{ const C = M.MARKS.filter(m => m.src === 'CAMP' || m.src === 'CARTS' || m.src === 'SITE' || m.src === 'LIFE' || m.src === 'PROTEST' || m.src === 'UPLIFT' || m.src === 'GOOD'), R = M.ISLE.rect, bad2 = C.filter(m => !m.K || !(m.x > R[0] && m.x < R[1] && m.z > R[2] && m.z < R[3]));
  if (bad2.length || !C.length) globalThis.__cowBad = (globalThis.__cowBad || 0) + Math.max(1, bad2.length);
  quiet((bad2.length || !C.length ? 'BAD ' : 'ok  ') + 'CAMP+CARTS', C.map(m => m.p.name + ' (' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ') ' + m.x.toFixed(0) + ',' + m.z.toFixed(0)).join(' | ') || 'NOBODY',
    '| fire at', JSON.stringify(M.OTCAMP.fireAt && M.OTCAMP.fireAt.map(v => +v.toFixed(1))), '| regions', JSON.stringify((M.MAPREG.tkit || []).map(r => r.id + ' ' + [r.x0, r.x1, r.z0, r.z1].map(v => Math.round(v)).join(',')))); }
{ const O = M.OPROTEST, why = !O.path ? 'NO PATH' : O.len < 20 ? 'TOO SHORT' : O.len > 140 ? 'A DETOUR ROUND THE TOWN' : !O.n ? 'NOBODY' : '';
  if (why) globalThis.__cowBad = (globalThis.__cowBad || 0) + 1;
  quiet((why ? 'BAD ' : 'ok  ') + 'PROTEST', O.n, 'people | square', JSON.stringify(O.a && O.a.map(v => +v.toFixed(1))), '-> corner', JSON.stringify(O.b && O.b.map(v => +v.toFixed(1))),
    '| path', O.path ? O.path.length : 0, 'pts', O.len && +O.len.toFixed(1), 'm (straight', O.a && O.b ? +Math.hypot(O.b[0] - O.a[0], O.b[2] - O.a[2]).toFixed(1) : '-', ')',
    '| counter line', JSON.stringify(O.COUNTER.map(c => c.line && c.line.map(v => +v.toFixed(1)))), 'suit at', JSON.stringify(O.SUIT.at && O.SUIT.at.map(v => +v.toFixed(1))),
    '| police line', O.line ? O.lineW.toFixed(1) + ' m wide at ' + O.lineAt.slice(0, 3).map(v => +v.toFixed(1)).join(',') : 'NONE', why); }
// m347: the brawl, run from the shipped `protestBrawl`, ends (no bodies here: the cops are "in" at once or it times out)
{ const O = M.OPROTEST; let r = 'NOT RUN';
  try { O.st = 'rally'; O.s = O.len; const ok = M.protestBrawl('GOD'); for (let f = 0; f < 120 && O.st === 'brawl'; f++) M.protestStep(.5); r = ok ? 'brawl -> ' + O.st + ' after ' + (O.bT || 0).toFixed(1) + ' s, cops ' + (O.cops || []).length : 'DID NOT START'; }
  catch (e) { r = 'THROW ' + e.message; }
  O.st = 'quiet'; O.t = 999;
  const why = /THROW|DID NOT|NOT RUN/.test(r) || /brawl -> brawl/.test(r) ? r : '';
  if (why) globalThis.__cowBad = (globalThis.__cowBad || 0) + 1;
  quiet((why ? 'BAD ' : 'ok  ') + 'BRAWL', r); }
quiet('LIFE', M.OTLIFE.n, 'routes:', M.OTLIFE.routes.map(r => r.id + ' ' + r.beat.length + 'pts ' + Math.round(r.beat.reduce((s2, q, i, B) => s2 + (i ? Math.hypot(q[0] - B[i - 1][0], q[1] - B[i - 1][1]) : 0), 0)) + 'm').join(' | '));
// ---- EVERY LIVE QUEST STEP POINTS AT SOMETHING THAT EXISTS (m339): a place that resolves, a person whose mark found its
// kind, a speaker who is a mark (or a script an earlier step hands over), a gate that was built. A step aimed at nothing
// is a beam that never appears and an objective that never passes, and from the phone that is "the game stopped".
{ const ids = new Map(M.MARKS.filter(m => m.type === 'npc').map(m => [m.id, m])), out = []; let nb = 0;
  for (const q of M.QUESTS.filter(q => q.world === 'tkit' && !q.dormant)) {
    const after = new Set();
    q.steps.forEach((st, i) => {
      let why = '';
      if (st.after) after.add(st.after.id);
      if (st.at) { let a = null; try { a = st.at(); } catch (e) {} if (!a) why = 'AT NOTHING'; }
      if (st.npc) why = !ids.has(st.npc) ? 'NO MARK ' + st.npc : !ids.get(st.npc).K ? 'MARK ' + st.npc + ' HAS NO KIND' : why;
      if (st.type === 'talk' && st.who && !after.has(st.who) && !(st.say && st.npc) && !(st.who.startsWith('mk_') && ids.has(st.who.slice(3)))) why = 'NOBODY IS ' + st.who;
      if (st.type === 'gate' && !M.GATES.find(g => g.id === st.id)) why = 'NO GATE ' + st.id;
      for (const id of [...(st.npcs || []), ...((st.also && st.also.npcs) || [])]) if (!ids.has(id) || !ids.get(id).K) why = 'NO BODY ON MARK ' + id;   // m342
      if (i === 0 && q.needQ && !M.QUESTS.find(o => o.id === q.needQ)) why = 'NEEDS A QUEST THAT IS NOT THERE: ' + q.needQ;
      if (st.kind && !M.MARKS.some(m => m.type === 'npc' && m.K && (m.p.kind === st.kind || (m.p.role && (M.ROSTER.find(r => r.id === m.p.role) || {}).stem === st.kind)) && m.id !== st.not)) why = 'NOBODY OF KIND ' + st.kind;   // m340; m357 or a role of it
      for (const k of st.kinds || []) if (!M.MARKS.some(m => m.type === 'npc' && m.K && m.p.kind === k)) why = 'NOBODY OF KIND ' + k;   // m362
      if (why) nb++;
      out.push(q.id + '.' + i + ' ' + st.type + (why ? ' BAD ' + why : ''));
    });
  }
  if (nb) globalThis.__cowBad = (globalThis.__cowBad || 0) + nb;
  quiet((nb ? 'BAD ' : 'ok  ') + 'QUESTS', out.join(' | ')); }
// ---- THE FOOTBRIDGE (m341): where it went, how long, and that fixing it really lays a floor over the gap
{ const F = M.FOOT, G = F.G, R = M.ISLE.rect;
  let why = !F.n ? 'NOT BUILT' : !G ? 'NO GATE' : '';
  const out = F.footAt && !(F.footAt[0] > R[0] && F.footAt[0] < R[1] && F.footAt[2] > R[2] && F.footAt[2] < R[3]);
  if (!why && !out) why = 'FOOT INSIDE THE CITY';
  let gapY = null, fixedY = null;
  if (!why) { const x = G.x + Math.sin(G.h) * 3, z = G.z + Math.cos(G.h) * 3;          // 3 m into the gap
    gapY = M.groundAt(x, z, F.yD + .5, 1); const nb = M.BOXES.length; M.footFix(1); fixedY = M.groundAt(x, z, F.yD + .5, 1);
    if (!(gapY < F.yD - 1)) why = 'A FLOOR IN THE GAP BEFORE IT IS FIXED'; else if (!(Math.abs(fixedY - F.yD) < .05)) why = 'NO FLOOR AFTER FIXING';
    M.BOXES.length = nb; F.fixed = 0; }
  if (why) globalThis.__cowBad = (globalThis.__cowBad || 0) + 1;
  quiet((why ? 'BAD ' : 'ok  ') + 'FOOTBRIDGE', F.n, 'boxes, bearing', F.deg && +F.deg.toFixed(1), 'deg, waterline', F.vW, 'm out, deck y', F.yD && +F.yD.toFixed(2), 'span', F.span && +F.span.toFixed(1),
    'm | gap floor', gapY && +gapY.toFixed(2), '-> fixed', fixedY && +fixedY.toFixed(2), '| pads', M.PORTALS.filter(q => /footbridge|pearl/.test(q.id)).length, why); }
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
  const CITYP = ['oldtown', 'camp', 'carts', 'site', 'sitetop', 'beat', 'footbridge', 'pearldock', 'protest', 'barricade', 'orb', 'watcher', 'amp', 'uplift', 'lookout', 'lookfoot', 'mags', 'pruitt', 'ines', 'pearl', 'pearlbar', 'pearlroof', 'pearlhq'];                         // m335: places that are IN Old Town on purpose
  const offLand = M.FARMLAND.live && !['oldtown', 'camp', 'carts', 'site', 'sitetop', 'beat', 'footbridge', 'pearldock', 'protest', 'barricade', 'orb', 'watcher', 'amp', 'uplift', 'lookout', 'lookfoot', 'mags', 'pruitt', 'ines', 'pearl', 'pearlbar', 'pearlroof', 'pearlhq', 'bridge', 'warehouse', 'backyards', 'stones'].includes(P.id) && !(M.flEdgeAt(p.x, p.z) > 0);
  const why = !a ? 'NO PLACE' : (p.x === 0 && p.z === 0 && P.id !== 'oldtown') ? 'UNMOVED' : p.y < M.ISLE.sea + .3 ? 'IN THE SEA'
            : (!CITYP.includes(P.id) && city) ? 'IN THE CITY' : offLand ? 'OFF THE FARMLAND'
            : (g > -500 && p.y - g > 2.5) ? 'IN THE AIR' : '';          // m346: a GOD place stood him 36 m up and every row said ok
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
  for (const n of ['vehStep', 'farmPropsStep', 'farmhouseStep', 'floraStep', 'cowStep', 'crashStep', 'crashHeroStep', 'riverStep', 'gradeStep', 'skylineStep', 'campStep', 'cartStep', 'footStep', 'dhStep', 'decayStep', 'strikeStep', 'protestStep', 'incurStep', 'orbStep', 'watchStep', 'ampStep', 'smartStep', 'cyborgStep', 'lookoutStep']) {
    let err = null;
    console.log = () => {};
    for (let f = 0; f < 30 && !err; f++) { try { M[n](1 / 30); } catch (e) { err = e; } }
    console.log = ql;
    if (err) bad++;
    quiet((err ? 'BAD ' : 'ok  ') + n.padEnd(14), err ? (err.stack || String(err)).split('\n').slice(0, 3).join(' | ') : '30 frames');
  } }
// ---- THE PACIFIER (m350): up, a flying target, and three hits (through its own `hit`, as a bolt would call it) bring it
// down, set the save flag and end with it on the ground; then put back as it was
{ const O = M.OORB, T = O.T; let r = '';
  try { const was = M.SAVE.flags['orb:pacifier'] || 0, up0 = O.st;
    for (let k = 0; k < 3; k++) T.hit({ chg: 0 });
    for (let f = 0; f < 120; f++) M.orbStep(1 / 30);
    r = 'over ' + JSON.stringify([O.cx, O.gy, O.cz].map(v => +v.toFixed(1))) + ' at y +' + O.y + ', trance r ' + O.R + ' | was ' + up0 + ', after 3 hits ' + O.st + ', flag ' + (M.SAVE.flags['orb:pacifier'] || 0) + ' | AIRT ' + M.AIRT.length;
    M.SAVE.flags['orb:pacifier'] = was; O.st = 'up'; O.hpNow = O.hp; T.on = 1; O.g.visible = true; }
  catch (e) { r = 'THROW ' + e.message; }
  const why = !O.g ? 'NOT BUILT' : /THROW/.test(r) || !/after 3 hits down/.test(r) ? 'IT DID NOT COME DOWN' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'ORB', r, why); }
{ const U = M.UPLIFT, ms = M.MARKS.filter(m => m.src === 'UPLIFT'); const why = U.n < 2 ? 'NO CREW' : ms.some(m => !m.K) ? 'A CYBORG WITH NO KIND' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'UPLIFT', ms.map(m => m.p.name + ' (' + m.p.role + ' -> ' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ') ' + (m.p.beat ? m.p.beat.length : 0) + ' stops').join(' | '), why); }
// ---- THE PEARL (m359): built, and a walk from the dock's door to the plaza is floor all the way at the heights it should be
// (the dock's loading platform, the Pearl's own behind the door, the pier) -- the CAMP+CARTS row checks its locals
{ const O = M.OPEARL, F = O.frame; let r = 'NOT BUILT', why = '';
  if (F) { const C = Math.cos(F.thf), S = Math.sin(F.thf), at = (u, v) => [F.ox + u * C + v * S, F.oz - u * S + v * C];
    const want = [[-4.5, -1.5, 1.1, 'the dock platform'], [-4.5, 2, 1.1, 'behind the door'], [-4.5, 8, 0, 'the pier'], [-4.5, 30, 0, 'dock street'], [O.PLAZA[0], O.PLAZA[1] - 8, 0, 'the plaza']];
    const got = want.map(([u, v, h, nm]) => { const [x, z] = at(u, v), g = M.groundAt(x, z, F.y + h + .5, 1); return [nm, +(g - F.y).toFixed(2), h]; });
    const off = got.filter(([nm, g, h]) => Math.abs(g - h) > .15);
    const ppl = M.MARKS.filter(m => m.src === 'PEARL'), nok = ppl.filter(m => !m.K);
    r = O.n + ' boxes, ' + O.WAREHOUSES.length + ' warehouses | ' + got.map(([nm, g, h]) => nm + ' ' + g).join(', ') + ' | locals ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ');
    if (nok.length) why = 'A LOCAL WITH NO KIND';
    if (off.length) why = 'NO FLOOR WHERE ' + off.map(o => o[0]).join(', ').toUpperCase(); } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'PEARL', r, why); }
// ---- THE ROOFS (m361): every link is floor all the way across at the height its own curve says (the sag included),
// every landing comes in through a GAP in the parapet onto the roof, and every ladder stands on floor and tops out on floor
// with nothing over his head
{ const O = M.OPEARL, R = O.ROOF, E = O.frame; let r = 'NOT BUILT', why = '';
  if (E && R && R.n) {
    const C = Math.cos(E.thf), S = Math.sin(E.thf), W = (u, v) => [E.ox + u * C + v * S, E.oz - u * S + v * C], y = E.y;
    const links = R.LINKS.map((K, i) => { let off = 0, worst = 0;
      for (let k = 0; k < 20; k++) { const P = K.pt((k + .37) / 20), [x, z] = W(P[0], P[2]), g = M.groundAt(x, z, P[1] + .3, .5), e = Math.abs(g - P[1]); worst = Math.max(worst, e); if (e > .15) off++; }
      // the landings: through the parapet at the face, onto the roof behind it
      const ends = [[K.a, K.A], [K.b, K.B]].map(([[ix, f, t]]) => { const Wh = O.WAREHOUSES[ix], F0 = M.pearlFace(Wh, f, t, 0), F1 = M.pearlFace(Wh, f, t, -1.2), [x0, z0] = W(...F0.p), [x1, z1] = W(...F1.p);
        const p = { x: x0, y: y + Wh.h + .05, z: z0 }, wall = M.resolveBoxes(p, .3, 1.6), g = M.groundAt(x1, z1, y + Wh.h + .3, .5);
        return wall ? 'PARAPET' : Math.abs(g - (y + Wh.h)) > .1 ? 'NO ROOF' : ''; });
      return (i + 1) + ':' + K.kind + ' ' + K.L.toFixed(0) + 'm' + (off ? ' ' + off + ' OFF THE DECK (' + worst.toFixed(2) + ')' : '') + (ends.join('') ? ' ' + ends.filter(Boolean).join('+') : ''); });
    const lads = M.KCLIMB.filter(L => /^pearl_ladder_/.test(L.name)).map(L => {
      const fx = L.cx + L.fg.x * .7, fz = L.cz + L.fg.z * .7, foot = M.groundAt(fx, fz, L.miny + .3, .5), top = M.groundAt(L.mark.x, L.mark.z, L.mark.y + .3, .5), p = { x: L.mark.x, y: top, z: L.mark.z };
      const bad2 = Math.abs(foot - L.miny) > .15 ? ' NO FOOT (' + (foot - L.miny).toFixed(2) + ')' : Math.abs(top - (L.mark.y - .02)) > .15 ? ' NO TOP (' + (top - L.mark.y).toFixed(2) + ')' : M.resolveBoxes(p, .3, 1.6) ? ' TOPS OUT INTO SOMETHING' : '';
      return L.name.replace('pearl_ladder_', '') + ' ' + (L.top - L.miny).toFixed(1) + 'm' + bad2; });
    const gard = M.MARKS.filter(m => /^pearl_roof_/.test(m.id) || m.id === 'pearl_organiser'), nok = gard.filter(m => !m.K);
    // m363: the organiser stands on his roof, and the papers can be walked up to (roof floor in front of the table)
    const org = M.MARKS.find(m => m.id === 'pearl_organiser'), Pp = R.papersAt, G2 = R.hqGod;
    const orgOff = !org ? 'NO ORGANISER' : Math.abs(M.groundAt(org.x, org.z, org.y + .3, .5) - org.y) > .15 ? 'THE ORGANISER IS NOT ON THE ROOF' : '';
    const papOff = !Pp || !G2 ? 'NO PAPERS' : Math.abs(M.groundAt(G2[0], G2[2], Pp[1] + .3, .5) - Pp[1]) > .15 || Math.hypot(G2[0] - Pp[0], G2[2] - Pp[2]) > 1.9 ? 'THE PAPERS ARE OUT OF REACH' : '';
    r = R.n.links + ' links [' + links.join(', ') + '] | ladders [' + lads.join(', ') + '] | ' + R.n.beds + ' beds | gardeners ' + gard.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ') + ' | HQ ' + (orgOff || 'organiser on the roof') + ', ' + (papOff || 'papers in reach');
    why = links.some(t => /OFF THE DECK/.test(t)) ? 'A BRIDGE WITH A HOLE IN IT' : links.some(t => /PARAPET|NO ROOF/.test(t)) ? 'A BRIDGE THAT LANDS ON A WALL' : lads.length !== R.LADDERS.length + 1 ? 'A LADDER MISSING'
      : lads.some(t => /NO |INTO/.test(t)) ? 'A LADDER THAT GOES NOWHERE' : nok.length ? 'A GARDENER WITH NO KIND' : !R.godAt ? 'NO GOD PLACE' : orgOff || papOff;
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'ROOFS', r, why); }
// ---- THE PLAZA (m360): SEALED -- a flood from the stage over the real floor (every box top a body can step or jump to,
// 1.3 m, with no box over its head) that only the barricade lines may stop never reaches the dock street, the lane, the
// far pier or the east gap; the four doors are clear floor; each route is floor all the way; and the march goes out and
// comes back (no bodies in the harness, so the leader walks it alone)
{ const O = M.OPLAZA, E = M.OPEARL.frame; let r = 'NOT BUILT', why = '';
  if (E && O.routes) {
    const C = Math.cos(E.thf), S = Math.sin(E.thf), W = (u, v) => [E.ox + u * C + v * S, E.oz - u * S + v * C], y = E.y;
    const segs = O.gates.map(G => { const c = Math.cos(G.h), s = Math.sin(G.h), h = G.w / 2; return [G.x + c * h, G.z - s * h, G.x - c * h, G.z + s * h]; });
    const cross = (ax, az, bx, bz) => segs.some(([cx, cz, dx, dz]) => { const o = (px, pz, qx, qz, rx, rz) => (qx - px) * (rz - pz) - (qz - pz) * (rx - px);
      return o(ax, az, bx, bz, cx, cz) * o(ax, az, bx, bz, dx, dz) < 0 && o(cx, cz, dx, dz, ax, az) * o(cx, cz, dx, dz, bx, bz) < 0; });
    const floorAt = (x, z) => { const g = M.groundAt(x, z, y + 1.3, 0); if (!(g > y - .3) || g > y + 1.31) return null;
      const p = { x, y: g, z }; return M.resolveBoxes(p, .3, 1.6) ? null : g; };
    // the grid, in the frame, a metre a cell, over deck B and a little of A and C
    const U0 = -58, U1 = 58, V0 = 26, V1 = 112, nu = U1 - U0 + 1, nv = V1 - V0 + 1, seen = new Uint8Array(nu * nv), fl = new Float32Array(nu * nv).fill(NaN);
    const id = (i, j) => j * nu + i, cell = (i, j) => { const k = id(i, j); if (Number.isNaN(fl[k])) { const [x, z] = W(U0 + i + .37, V0 + j + .41); const g = floorAt(x, z); fl[k] = g == null ? -1e9 : g; } return fl[k]; };
    const T = O.STAGE, si = Math.round(T.u - U0), sj = Math.round(T.v - T.d / 2 - 2 - V0), q = [[si, sj]]; seen[id(si, sj)] = 1; let n = 0;
    while (q.length) { const [i, j] = q.pop(); n++; const g0 = cell(i, j), [x0, z0] = W(U0 + i + .37, V0 + j + .41);
      for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const i2 = i + a, j2 = j + b; if (i2 < 0 || j2 < 0 || i2 >= nu || j2 >= nv || seen[id(i2, j2)]) continue;
        const g = cell(i2, j2); if (g < -1e8 || Math.abs(g - g0) > 1.3) continue; const [x1, z1] = W(U0 + i2 + .37, V0 + j2 + .41); if (cross(x0, z0, x1, z1)) continue;
        seen[id(i2, j2)] = 1; q.push([i2, j2]); } }
    const outside = [[-2.5, 30, 'the dock street'], [-36, 69, 'the lane west'], [0, 100, 'the far pier'], [40, 66, 'the east gap'], [-50, 50, 'behind the studios']];
    const leak = outside.filter(([u, v]) => { const i = Math.round(u - U0), j = Math.round(v - V0); return j >= 0 && j < nv && seen[id(i, j)]; });
    const doors = O.doors.map(D => { const g = floorAt(D.x, D.z); return D.id + (g == null ? ' SHUT' : ' ' + (g - y).toFixed(2)); });
    const routes = O.routes.map(R => { let bad2 = 0; for (let s2 = 0; s2 <= R.len; s2 += 1) { const L = (() => { let acc = 0; const P = R.path; for (let i = 1; i < P.length; i++) { const l = Math.hypot(P[i].x - P[i - 1].x, P[i].z - P[i - 1].z); if (acc + l >= s2 || i === P.length - 1) { const k = l ? Math.min(1, (s2 - acc) / l) : 1; return [P[i - 1].x + (P[i].x - P[i - 1].x) * k, P[i - 1].z + (P[i].z - P[i - 1].z) * k]; } acc += l; } })();
        const g = floorAt(L[0], L[1]); if (g == null || Math.abs(g - y) > .5) bad2++; } return R.id + ' ' + R.len.toFixed(0) + ' m' + (bad2 ? ' ' + bad2 + ' BLOCKED' : ''); });
    // the march, run: out, hold, back, sit
    let walk = '';
    { M.plazaStart(0); const seenSt = [O.st]; for (let f = 0; f < 4000 && !(O.st === 'sit' && seenSt.length > 1); f++) { M.plazaStep(.1); if (O.st !== seenSt[seenSt.length - 1]) seenSt.push(O.st); }
      walk = seenSt.join(' > '); }
    const ppl = M.MARKS.filter(m => m.src === 'PLAZA'), nok = ppl.filter(m => !m.K);
    r = O.gates.length + ' barricades, flood ' + n + ' cells' + (leak.length ? ' LEAKS TO ' + leak.map(l => l[2]).join(', ') : ', sealed') + ' | doors ' + doors.join(', ') + ' | routes ' + routes.join(', ') + ' | march ' + walk + ' | ' + ppl.length + ' people';
    why = O.gates.length !== O.BARS.length ? 'A BARRICADE WITH NO GATE' : leak.length ? 'A WAY ROUND THE BARRICADES' : n < 300 ? 'THE FLOOD NEVER LEFT THE STAGE' : doors.some(d => /SHUT/.test(d)) ? 'A DOOR THAT IS SHUT'
      : routes.some(t => /BLOCKED/.test(t)) ? 'A ROUTE THROUGH SOMETHING' : walk !== 'form > out > hold > back > sit' ? 'THE MARCH NEVER CAME BACK' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'PLAZA', r, why); }
// ---- THE GOOD ALIENS (m358): three kiosks, a keeper with a kind at each, every rumour of the chain resolving to its
// keeper, and the upgrades moving the numbers they say they move
{ const G = M.OGOOD, ks = M.MARKS.filter(m => m.src === 'GOOD'), Rs = M.RUMOURS.filter(r => /^good_/.test(r.id)), rr = Rs.map(r => { let a = null; try { a = r.at(); } catch (e) {} return r.id + (a ? ' ok' : ' NOWHERE'); });
  const b0 = [M.JUICE.cap, M.SAMPLE.hold]; const fl = M.SAVE.flags; const was = Object.keys(M.UPGRADES).map(k => fl['up:' + k]);
  Object.keys(M.UPGRADES).forEach(k => fl['up:' + k] = 1); M.upApply(); const b1 = [M.JUICE.cap, M.SAMPLE.hold];
  Object.keys(M.UPGRADES).forEach((k, i) => fl['up:' + k] = was[i]); M.upApply();
  const why = G.n !== 3 ? G.n + ' KIOSKS' : ks.some(m => !m.K) ? 'A KEEPER WITH NO KIND' : ks.some(m => !m.name || !m.p.hat || m.p.alien !== 'talk') ? 'A KEEPER WITH NO NAME, HAT OR WORD FOR THE ALIEN' : rr.some(t => /NOWHERE/.test(t)) ? 'A RUMOUR GOES NOWHERE' : !(b1[0] > b0[0] && b1[1] < b0[1]) ? 'THE UPGRADES MOVE NOTHING' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'GOOD', ks.map(m => m.name + ' (' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ', ' + m.p.gift + ') ' + m.x.toFixed(0) + ',' + m.z.toFixed(0)).join(' | '), '| rumours', rr.join(', '),
    '| tank', b0[0], '->', b1[0], 'hold', +b0[1].toFixed(2), '->', +b1[1].toFixed(2), why); }
// ---- THE LOOKOUT (m357): built, its three ladders in the climb set, the deck under each ladder's top mark, Skye on top
{ const O = M.OLOOK, L = M.KCLIMB.filter(c => /^lookout_ladder_/.test(c.name || c.id || '')), sk = M.MARKS.find(m => m.id === 'lookout_skye');
  const marks = L.map(c => c.mark ? +(M.groundAt(c.mark.x, c.mark.z, c.mark.y + .5, 1) - c.mark.y).toFixed(2) : 'NONE');
  const why = !O.n ? 'NOT BUILT' : L.length !== 3 ? L.length + ' LADDERS, NOT 3' : marks.some(v => v === 'NONE' || Math.abs(v) > .15) ? 'A LADDER TOP SETS HIM DOWN ON NOTHING' : !sk || !sk.K ? 'NO SKYE' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'LOOKOUT', O.n, 'boxes | top deck', O.top && +O.top.toFixed(2), 'over ground', O.g0 && +O.g0.toFixed(2), '| ladders', L.length, 'tops (floor - mark)', JSON.stringify(marks),
    '| Skye', sk ? sk.p.role + ' -> ' + (sk.K ? sk.K.file.split('/').pop() : 'NO KIND') + ' at y ' + sk.y.toFixed(1) : 'NONE', why); }
// ---- SMART OBJECTS (m354): every spot a body can stand on (street level, nothing over it), grouped by what owns it
{ const S = M.SMART.spots, by = {}, off = [];
  // street level, and nothing within .3 m (a body's core: `kitStand`'s .5 is the widest body clear of EVERYTHING, which is
  // stricter than a spot beside a bench needs, and arrival allows `roamAt` + .35 of slack)
  for (const q of S) { by[q.obj] = (by[q.obj] || 0) + 1; const y = M.groundAt(q.x, q.z, 1.2, .5), P = { x: q.x, y, z: q.z };
    if (!(y > -1 && y < .6) || M.resolveBoxes(P, .3, 1.7)) off.push(q.obj + '@' + q.x.toFixed(0) + ',' + q.z.toFixed(0)); }
  const why = !S.length ? 'NO SPOTS' : off.length > S.length * .25 ? 'TOO MANY SPOTS NOBODY CAN STAND ON: ' + off.join(' ') : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'SMART', S.length, 'spots', JSON.stringify(by), off.length ? '| not standable: ' + off.join(' ') : '| all standable', why); }
// ---- THE ROSTER (m353): every role's stand-in resolves to a kind the game has (zap and Clancy are played, not spawned)
{ const R = M.ROSTER, miss = R.filter(r => !r.pc && !M.rosterKind(r)).map(r => r.id + ':' + r.stem), ids = new Set(R.map(r => r.id));
  const why = miss.length ? 'NO KIND FOR ' + miss.join(', ') : ids.size !== R.length ? 'TWO ROLES SHARE AN ID' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'ROSTER', R.length, 'roles |', R.filter(r => r.st === 'have').length, 'his,', R.filter(r => r.st === 'stand-in').length, 'stand-ins,', R.filter(r => r.st === 'none').length, 'nothing close', why); }
// ---- THE AMPLIFIER (m352): up, it multiplies the boil; three hits, it calms it; put back after
{ const O = M.OAMP; let r = '';
  try { const f0 = M.SAVE.flags['orb:amp'] || 0, b0 = M.ampBoil();
    for (let f = 0; f < 60; f++) M.ampStep(1 / 30);
    for (let k = 0; k < 3; k++) O.T.hit({ chg: 0 });
    for (let f = 0; f < 120; f++) M.ampStep(1 / 30);
    r = 'over the square ' + JSON.stringify([O.cx, O.gy, O.cz].map(v => +v.toFixed(1))) + ' | boil x' + b0 + ' while up, x' + M.ampBoil() + ' after 3 hits (' + O.st + ')';
    M.SAVE.flags['orb:amp'] = f0; O.st = 'up'; O.hpNow = O.hp; O.T.on = 1; O.g.visible = true; }
  catch (e) { r = 'THROW ' + e.message; }
  const why = !O.g ? 'NOT BUILT' : /THROW/.test(r) || !/\(down\)/.test(r) ? 'IT DID NOT COME DOWN' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'AMP', r, why); }
// ---- THE WATCHER (m351): stand him in its pool as himself -- it locks on, the alert fills, it calls; then three hits
// bring it down and the alert goes to nothing. All through the shipped step; put back as it was after.
{ const O = M.OWATCH; let r = '';
  try { const p = M.player.pos, was = [p.x, p.y, p.z], f0 = M.SAVE.flags['orb:watcher'] || 0;
    let lockAt = -1, callAt = -1;
    for (let f = 0; f < 300; f++) { p.set(O.px, M.groundAt(O.px, O.pz, 3, 6), O.pz); M.watchStep(1 / 30);
      if (lockAt < 0 && O.lock) lockAt = f; if (callAt < 0 && O.calls) callAt = f; }
    const a1 = O.alert;
    for (let k = 0; k < 3; k++) O.T.hit({ chg: 0 });
    for (let f = 0; f < 120; f++) M.watchStep(1 / 30);
    r = 'over ' + JSON.stringify([O.cx, O.gy, O.cz].map(v => +v.toFixed(1))) + ' | locked at ' + (lockAt / 30).toFixed(1) + ' s, called at ' + (callAt / 30).toFixed(1) + ' s, alert then ' + Math.round(a1) +
      ' | after 3 hits ' + O.st + ', alert ' + Math.round(O.alert);
    p.set(was[0], was[1], was[2]); M.SAVE.flags['orb:watcher'] = f0; O.st = 'up'; O.hpNow = O.hp; O.calls = 0; O.callT = 0; O.alert = 0; O.lock = 0; O.T.on = 1; }
  catch (e) { r = 'THROW ' + e.message; }
  const why = !O.g ? 'NOT BUILT' : /THROW/.test(r) || /locked at -/.test(r) || /called at -/.test(r) || !/after 3 hits down, alert 0/.test(r) ? 'IT DID NOT WATCH, CALL AND FALL' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'WATCHER', r, why); }
// ---- THE INCURSION SHIP (m349): its whole flight, from the shipped step -- in, hover (nobody turnable in the harness, so
// straight on), out, off -- and that it ends where it started
{ const O = M.OINCUR; let r = '';
  try { O.st = 'off'; const started = M.incurStart(1);
    const ch = M.SAVE.ch, it = M.SAVE.flags.inTown; M.SAVE.ch = 0;           // the clock stays off for this
    // nobody is turnable here (no prototypes load), so fly it by hand from a made-up street spot
    O.st = 'in'; O.tx = 0; O.tz = 30; O.y0 = 0; O.x = 60; O.z = 30; O.y = 45; O.t = 0; O.turned = 0; O.tgt = null;
    if (!O.g) { O.g = { visible: 1, position: { set() {} }, rotation: {} }; O.lights = { rotation: { y: 0 } }; O.beam = { visible: 0 }; }
    const seen = new Set(); for (let f = 0; f < 600 && !(seen.has('out') && O.st === 'off'); f++) { M.incurStep(1 / 30); seen.add(O.st); }
    r = 'states ' + [...seen].join('>') + ' | started on its own: ' + started + ' | ends ' + O.st;
    M.SAVE.ch = ch; M.SAVE.flags.inTown = it; }
  catch (e) { r = 'THROW ' + e.message; }
  const why = /THROW/.test(r) || !/hover/.test(r) || !/ends off/.test(r) ? 'DID NOT FLY ITS COURSE' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'INCURSION', r, why); }
// ---- THE STRIKE (m345): the picket line is OUTSIDE the site (farther from its middle than the gate), and calling it and
// calling it off shows and hides the picket and lights and puts out its barrel
{ const S = M.OSTRIKE, G = M.OTSITE.gateAt, C = M.OTSITE.at, gd = G ? Math.hypot(G[0] - C[0], G[2] - C[1]) : 0;
  const ld = (S.line || []).map(q => Math.hypot(q[0] - C[0], q[1] - C[1]));
  let why = !S.g ? 'NOT BUILT' : !S.line || S.line.length < 2 ? 'NO LINE' : ld.some(d => d < gd + 1) ? 'THE LINE IS INSIDE THE SITE' : '';
  const was = M.SAVE.flags['strike:oldtown'] || 0;
  M.strikeSet(1); S.st = 0; M.strikeStep(1 / 30); const vis1 = S.g && S.g.visible, f1 = !!S.fire;
  M.strikeSet(0); S.st = 0; M.strikeStep(1 / 30); const vis0 = S.g && S.g.visible, f0 = !!S.fire;
  if (!why && !(vis1 && f1 && !vis0 && !f0)) why = 'THE PICKET DID NOT FOLLOW THE FLAG';
  M.strikeSet(was); S.st = 0; M.strikeStep(1 / 30);
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'STRIKE line', JSON.stringify((S.line || []).map(q => q.map(v => +v.toFixed(1)))), '| from the site middle', ld.map(v => +v.toFixed(1)).join(','), 'vs the gate', +gd.toFixed(1),
    '| on: picket', vis1, 'barrel', f1, '| off: picket', vis0, 'barrel', f0, why); }
// ---- THE LOOK FOLLOWS IT (m344): at 100 nothing shows, at 0 everything does, at today's number somewhere between
{ const D = M.ODECAY, all = D.items.B.length + D.items.R.length + D.items.L.length, h = M.dhGet('oldtown');
  M.decayApply(100); const at100 = D.shown; M.decayApply(0); const at0 = D.shown; M.decayApply(h); const now = D.shown;
  const why = !D.built ? 'NOT BUILT' : !D.rubble || !D.litter ? 'NO STREET FOUND' : at100 ? 'DECAY ON A HEALTHY TOWN' : at0 !== all ? 'NOT ALL OF IT AT ZERO' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'DECAY boards', D.boards, '(no kit buildings in this harness)', 'rubble heaps', D.rubble, 'pieces', D.items.R.length, 'litter', D.litter,
    '| shown at 100:', at100, 'at 0:', at0, 'at ' + Math.round(h) + ':', now, '| squatters', D.squat.length, why); }
// ---- DISTRICT HEALTH (m343): what it read after the second of steps above, and that a push moves it and a band
{ const D = M.DHEALTH, h0 = M.dhGet('oldtown'); M.dhPush('oldtown', -30); const h1 = M.dhGet('oldtown'); M.dhPush('oldtown', 30);
  const why = !(h0 > 0) ? 'NO HEALTH' : Math.abs(h1 - Math.max(0, h0 - 30)) > .01 ? 'A PUSH DID NOT MOVE IT' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'DHEALTH oldtown', +h0.toFixed(2), '| fires', D.fires, 'skinsuits', D.skins, 'born warriors', D.aliens, '| -30 ->', +h1.toFixed(2), '| band changes', D.n, why); }
process.exit(bad ? 1 : 0);
