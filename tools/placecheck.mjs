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
src += '\nglobalThis.__M = { islLocal, IJUMP, isJump, IKITE, isKite, islMoversStep, buildIslandMovers, IBASE, buildIslandBase, ISKATE, buildIslandSkate, ISLES, buildIslands, islHeight, islEdge, islWorld, FOE, wfLineOff, wfFree, WBOT, wfBot, wfBotStep, WTUR, wfTurretStep, WFSEC, wfSecStep, ROLEFORM, formNow, formKind, socialMe, gateLets, GATE_TYPES, engineerOn, OSWING, swingStep, swingPlace, buildSwing, OFERRY, ferryStep, ferryPlace, buildFerry, WCRANE, wfCraneStep, WFCONV, wfConvStep, wfRide, wfAt, WFLINE, wfLineStep, WFRONT, buildWaterfront, wfEdge, HCRACE, raceStep, raceAt, BIKE, PBIKE, bikeOn, BIKER, SK8, HCRALLY, buildRally, rallyStep, rallyStart, HCROAD, buildHighway, gatePush, HCTRAIN, buildFreight, trainStep, trainUnder, BDYN, HCBIKE, buildBikeTrack, bikeLoop, HCFAIR, buildFairground, fairStep, HCMILL, buildMill, HCTRAIL, buildTrailerPark, HCREEK, buildHollowLand, hcHeight, hcLocal, hcWorld, hcEdge, hcGorgeAt, buildPearlRoofs, pearlFace, KCLIMB, OPLAZA, buildPearlPlaza, plazaStep, plazaStart, pearlCrowd, OPEARL, buildPearl, OGOOD, buildGoodKiosks, RUMOURS, upApply, UPGRADES, JUICE, SAMPLE, OLOOK, buildLookout, lookoutStep, KCLIMB, UPLIFT, buildUplift, cyborgStep, resolveBoxes, SMART, smartStep, ROSTER, rosterKind, OAMP, buildAmp, ampStep, ampBoil, OWATCH, buildWatcher, watchStep, OORB, AIRT, buildOrbs, orbStep, OINCUR, incurStart, incurStep, protestBrawl, OPROTEST, buildProtest, protestStep, protestStart, OSTRIKE, buildStrike, strikeSet, strikeStep, OTSITE, ODECAY, buildDecay, decayApply, decayStep, DHEALTH, dhStep, dhGet, dhPush, FIRES, FOOT, buildFootbridge, footStep, footFix, BOXES, PORTALS, QUESTS, buildLife, OTLIFE, buildSite, OTSITE, buildCarts, OTCARTS, cartStep, mapRegionsTkit, buildCamp, OTCAMP, MAPREG, campStep, FARMLAND, buildFarmland, buildFarmWaters, FWATER, buildFieldBounds, FPLAN, buildFieldCrops, FCROP, buildNeighbours, FNEIGH, COW, COWS, cowSpook, fpOwnAt, flLocal, buildVehicles, FVEH, vehStep, buildFarmhands, FHANDS, MARKS, mkrNpcPlace, HOBO, HICK, buildTownEdge, FTOWN, buildCityRing, FRING, farmBatch, FBATCH, scene, buildTrestle, FTRES, buildFord, FFORD, GATES, buildOrchardTerrace, FTERR, buildSkyline, SKYLINE, skylineStep, flEdgeAt, isleBedAt, KCITY, buildKCityCol, buildIsle, ISLE, TRI, triBuild, groundAt, WORLD, MOVE, player, kitPopulate, KCROWD, FOE, HICK, HOBO, SKATER, BIKER, DUMMY, CIVILS, CLANCY, kitStand, bodySeat, SEAT, DUMMIES, THREE, buildFarm, buildFarmProps, buildCrash, buildLane, buildBridge, buildCows, buildHedgerows, HROW, buildFarmhouse, FHOUSE, farmhouseStep, buildRoadside, FROAD, GPAINT, buildGroundPaint, buildFlora, crashHero, FARM, MISSING, FLORA, FPROPS, farmPropsStep, floraStep, cowStep, crashStep, crashHeroStep, riverStep, gradeStep, CRASH, GODPLACES, godPlace, GOD, LANE, BRIDGE, crashSpawn, SAVE };\n';
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

const farmSteps = ['buildFarmland','buildHollowLand','buildWaterfront','buildFerry','buildIslands','buildIslandSkate','buildIslandBase','buildIslandMovers','buildSwing','buildFarmWaters','buildOrchardTerrace','buildFieldBounds','buildFieldCrops','buildNeighbours','buildFarm','buildFarmProps','buildCrash','crashHero','buildLane','buildBridge','buildHedgerows','buildFarmhouse','buildRoadside','buildCows','buildVehicles','buildFarmhands','mapRegionsTkit','buildCamp','buildCarts','buildSite','buildLife','buildProtest','buildOrbs','buildWatcher','buildAmp','buildUplift','buildLookout','buildGoodKiosks','buildFootbridge','buildDecay','buildPearl','buildPearlPlaza','buildPearlRoofs','buildTrailerPark','buildMill','buildFairground','buildBikeTrack','buildFreight','buildHighway','buildRally','buildStrike','buildTownEdge','buildCityRing','buildTrestle','buildFord','buildSkyline','farmBatch','buildGroundPaint','buildFlora'];
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
      if (st.form && Object.values(M.ROLEFORM).some(r => r.name === st.form) && !M.MARKS.some(m => m.type === 'npc' && m.K && m.p.role && M.ROLEFORM[m.p.role] && M.ROLEFORM[m.p.role].name === st.form)) why = 'NOBODY TO SAMPLE AS ' + st.form;   // m386: a role's form
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
  const CITYP = ['oldtown', 'camp', 'carts', 'site', 'sitetop', 'beat', 'footbridge', 'pearldock', 'protest', 'barricade', 'orb', 'watcher', 'amp', 'uplift', 'lookout', 'lookfoot', 'mags', 'pruitt', 'ines', 'pearl', 'pearlbar', 'pearlroof', 'pearlhq', 'otfreight', 'otroad', 'gangbridge', 'otferry', 'otswing'];                         // m335: places that are IN Old Town on purpose
  const offLand = M.FARMLAND.live && !['oldtown', 'camp', 'carts', 'site', 'sitetop', 'beat', 'footbridge', 'pearldock', 'protest', 'barricade', 'orb', 'watcher', 'amp', 'uplift', 'lookout', 'lookfoot', 'mags', 'pruitt', 'ines', 'pearl', 'pearlbar', 'pearlroof', 'pearlhq', 'otfreight', 'otroad', 'gangbridge', 'otferry', 'otswing', 'bridge', 'warehouse', 'backyards', 'stones'].includes(P.id) && !/^hc/.test(P.id) && !/^wf/.test(P.id) && !/^is/.test(P.id) && !(M.flEdgeAt(p.x, p.z) > 0);
  // m365: a Hollow Creek place (`hc...`) is on ITS land
  const offHC = /^hc/.test(P.id) && !(M.HCREEK.live && (([a, b]) => M.hcEdge(a, b))(M.hcLocal(p.x, p.z)) > 0);
  const offWF = /^wf/.test(P.id) && !(M.WFRONT.live && M.wfEdge(p.x, p.z) > 0);          // m377: a Waterfront place is on ITS land
  const offIS = /^is/.test(P.id) && !(M.ISLES.live && M.islEdge(p.x, p.z) > 0);            // m389: an islands place on the chain
  const why = !a ? 'NO PLACE' : (p.x === 0 && p.z === 0 && P.id !== 'oldtown') ? 'UNMOVED' : p.y < M.ISLE.sea + .3 ? 'IN THE SEA'
            : (!CITYP.includes(P.id) && city) ? 'IN THE CITY' : offLand ? 'OFF THE FARMLAND' : offHC ? 'OFF HOLLOW CREEK' : offWF ? 'OFF THE WATERFRONT' : offIS ? 'OFF THE ISLANDS'
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
// m368: WALK IT -- along a polyline of world points in 10 cm steps, the floor re-found each step the way the player's own is
// (`groundAt` from his height, `MOVE.step` up and no more): the height he ends at. A riser over the step is a wall to this
// exactly as it is to him -- which no probe here asked until m368 found .37 and .375 risers that were walls.
const walkUp = (pts, y0) => { let y = y0; for (let i = 0; i < pts.length - 1; i++) { const [ax, az] = pts[i], [bx2, bz] = pts[i + 1], n = Math.max(1, Math.ceil(Math.hypot(bx2 - ax, bz - az) / .1));
  for (let k = 1; k <= n; k++) { const g = M.groundAt(ax + (bx2 - ax) * k / n, az + (bz - az) * k / n, y, M.MOVE.step); if (g > -500) y = g; } } return y; };
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
    if (off.length) why = 'NO FLOOR WHERE ' + off.map(o => o[0]).join(', ').toUpperCase();
    // m368: up every warehouse's steps onto its loading platform, walking
    const ups = O.WAREHOUSES.map(W => W.climb ? +(walkUp(W.climb, F.y) - F.y).toFixed(2) : -1);
    r += ' | platforms walked up to ' + ups.join(', ');
    if (ups.some(h => Math.abs(h - 1.1) > .05)) why = 'STEPS YOU CANNOT WALK UP'; } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'PEARL', r, why); }
// ---- THE WATERFRONT (m377): built, clear of every other land; its quay at the height it should be; the dry dock WALKED --
// down its head stair from the quay to the floor and back up, room under the ship, up the stair tower and over the gangway
// onto her deck; up the crate stairs onto the stacks; the high road's links walkable; every ladder in; its people have kinds
{ const W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (W.live) {
    const at = (u, v) => [W.O[0] + u * W.C + v * W.S, W.O[1] - u * W.S + v * W.C], R = M.ISLE.rect, pr = (M.MAPREG.tkit || []).find(q => q.id === 'pearl'), hb = M.HCREEK.bbox;
    let clash = [];
    for (let u = W.U[0]; u <= W.U[1]; u += 10) for (const v of [W.V[0], 0, 70, W.V[1]]) { const [x, z] = at(u, v);
      if (M.FARMLAND.live && M.flEdgeAt(x, z) > -15) clash.push('the farm');
      if (x > R[0] - 40 && x < R[1] + 40 && z > R[2] - 40 && z < R[3] + 40) clash.push('the island');
      if (pr && x > pr.x0 - 30 && x < pr.x1 + 30 && z > pr.z0 - 30 && z < pr.z1 + 30) clash.push('the pearl');
      if (hb && x > hb.x0 - 30 && x < hb.x1 + 30 && z > hb.z0 - 30 && z < hb.z1 + 30) clash.push('hollow creek'); }
    clash = [...new Set(clash)];
    const want = [[10, 12, 'the container quay'], [-90, -30, 'pier 1'], [34, -26, 'pier 2'], [-14, 80, 'the dock lane'], [-38, 120, 'behind the dock head'], [-70, 46, 'the factory yard'], [100, 25, 'the far quay']];
    const off = want.map(([u, v, nm]) => { const [x, z] = at(u, v), g = M.groundAt(x, z, W.Y + .5, 1); return [nm, +(g - W.Y).toFixed(2)]; }).filter(([, d]) => Math.abs(d) > .1);
    const D = W.DOCK, [fx, fz] = at(D.u + 2.5, 50), fl = M.groundAt(fx, fz, W.floor + .5, .6), depth = W.Y - fl;
    const head = (() => { let lo = 1e9; for (const b of M.BOXES) { if (fx < b.minx || fx > b.maxx || fz < b.minz || fz > b.maxz || b.miny < fl + .1) continue; lo = Math.min(lo, b.miny); } return lo - fl; })();
    const s0 = W.dockStair[0], down = walkUp(W.dockStair, M.groundAt(s0[0], s0[1], W.floor + .5, .6));
    const t0 = W.shipWalk[0], deck = walkUp(W.shipWalk, M.groundAt(t0[0], t0[1], W.Y + .5, .6));
    const crates = W.BLOCKS.filter(B => B.climb).map(B => +(walkUp(B.climb, W.Y) - W.Y).toFixed(2));
    const links = W.links.map(([x, y, z]) => +(M.groundAt(x, z, y + .8, 1.6) - y).toFixed(2));
    const ladders = M.KCLIMB.filter(L => /^wf_/.test(L.nm || L.name || '')).length;
    const ppl = M.MARKS.filter(m => m.src === 'WFRONT'), nok = ppl.filter(m => !m.K && !(m.p && m.p.kind) && !(m.p && m.p.role && M.rosterKind(M.ROSTER.find(q => q.id === m.p.role))));
    r = W.n + ' boxes, ' + W.cont + ' containers | centre ' + W.O.map(v => v.toFixed(0)).join(',') + ' | clear of ' + (clash.length ? 'NOT ' + clash.join(', ') : 'the farm, the island, the pearl, hollow creek') +
      ' | quay ' + (off.length ? 'OFF: ' + off.map(o => o.join(' ')).join(', ') : 'level at ' + W.Y) + ' | dock floor ' + fl.toFixed(2) + ' (' + depth.toFixed(1) + ' m down), ' + head.toFixed(2) + ' m under the hull' +
      ' | head stair floor -> ' + down.toFixed(2) + ' (quay ' + W.Y + ') | stair tower -> ' + deck.toFixed(2) + ' (deck ' + W.deck.toFixed(2) + ') | crate stairs up ' + crates.join(', ') + ' | high road ' + links.join(', ') +
      ' | ladders ' + W.ladders + ' (' + ladders + ' climbs) | people ' + ppl.map(m => m.name).join(', ');
    why = clash.length ? 'IT OVERLAPS ANOTHER LAND' : off.length ? 'THE QUAY IS NOT LEVEL' : !(depth > 4.5) || fl < M.ISLE.sea ? 'THE DRY DOCK IS NOT A DOCK' : head < 1.9 ? 'NO ROOM UNDER THE SHIP'
      : Math.abs(down - W.Y) > .1 ? 'THE DOCK STAIR DOES NOT REACH' : Math.abs(deck - W.deck) > .1 ? 'THE SHIP CANNOT BE BOARDED' : crates.some(c => Math.abs(c - 2.6) > .1) ? 'A CRATE STAIR FALLS SHORT'
      : links.some(l => Math.abs(l) > .1) ? 'A HIGH ROAD LINK HAS NO FLOOR' : ladders < W.ladders ? 'A LADDER IS NOT A CLIMB' : nok.length ? 'SOMEBODY WITH NO KIND' : ppl.length < W.PEOPLE.length ? 'SOMEBODY MISSING' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'WATERFRONT', r, why); }
// ---- UPLIFT'S FACTORY, INSIDE (m378): WALKED up the west wall's stair to the third level, from the landing along the second
// level into the control room, and from the quay up the outfeed tower and along the gallery into the hall; the intake's
// doorway open; a belt CARRIES him (the shipped `wfLineStep`), and nobody is carried off one
{ const W = M.WFRONT, L = M.WFLINE; let r = 'NOT BUILT', why = '';
  if (W.live && L.belts.length) {
    const Y = W.Y, L2 = Y + L.L2, L3 = Y + L.L3, at = (u, v) => [W.O[0] + u * W.C + v * W.S, W.O[1] - u * W.S + v * W.C];
    const from = (pts, y) => walkUp(pts, M.groundAt(pts[0][0], pts[0][1], y + .5, .6));
    const hall = from(W.hallWalk, Y), ctrl = from(W.ctrlWalk, L2), tower = from(W.towerWalk, Y);
    const [dx, dz] = at(-87, W.FACTORY.v - W.FACTORY.d / 2 + .2), door = M.BOXES.filter(b => dx > b.minx && dx < b.maxx && dz > b.minz && dz < b.maxz && b.miny < Y + 1.5 && b.maxy > Y + 1.5 && (!b.hx || Math.abs((dx - b.cx) * b.cs - (dz - b.cz) * b.sn) <= b.hx && Math.abs((dx - b.cx) * b.sn + (dz - b.cz) * b.cs) <= b.hz)).length;
    const p = M.player, A = L.belts[0], keep = p.pos.clone(), gr = p.grounded, vy = p.vel.y;
    p.pos.set(A.ax + A.dx * 5, A.ya, A.az + A.dz * 5); p.grounded = true; p.vel.y = 0; const s0 = p.pos.clone(), id = M.wfLineStep(.5), moved = p.pos.distanceTo(s0), along = ((p.pos.x - s0.x) * A.dx + (p.pos.z - s0.z) * A.dz);
    p.pos.set(A.ax - 20, Y, A.az - 20); const off = M.wfLineStep(.5);
    p.pos.copy(keep); p.grounded = gr; p.vel.y = vy;
    r = L.belts.length + ' belts (' + L.belts.map(B => B.id + ' ' + B.len.toFixed(1) + 'm').join(', ') + ') | west stair floor -> ' + hall.toFixed(2) + ' (third level ' + L3.toFixed(2) + ') | landing -> control room ' + ctrl.toFixed(2) + ' (' + L2.toFixed(2) + ')' +
      ' | quay -> tower -> gallery -> hall ' + tower.toFixed(2) + ' | intake doorway ' + (door ? door + ' BOXES IN IT' : 'open') + ' | on belt ' + id + ' carried ' + along.toFixed(2) + ' m along it in .5 s (' + (L.speed * .5).toFixed(2) + ' wanted), off the line: ' + (off || 'nothing');
    why = Math.abs(hall - L3) > .1 ? 'THE WEST STAIR DOES NOT REACH' : Math.abs(ctrl - L2) > .1 ? 'THE CONTROL ROOM CANNOT BE REACHED' : Math.abs(tower - L3) > .1 ? 'THE TOWER WAY IN IS BROKEN'
      : door ? 'THE INTAKE IS SHUT' : id !== 'A' || Math.abs(along - L.speed * .5) > .02 || Math.abs(moved - along) > .02 ? 'THE BELT DOES NOT CARRY' : off ? 'IT CARRIES HIM OFF THE LINE' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'FACTORY', r, why); }
// ---- THE CONVERSION LINE (m379): its riders have marks with kinds; a rider (a body fabricated the way the game holds one)
// rides the WHOLE route through the shipped `wfRide` -- on the belts at the belts' own floor all the way, every station in
// order, a docker in and a cyborg out, the line-up on the quay -- and goes back to the queue a docker when he is away
{ const C = M.WFCONV, W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (C.route && W.live) {
    const marks = M.MARKS.filter(m => m.src === 'WFCONV'), nok = marks.filter(m => !m.K);
    const d = { root: new M.THREE.Group(), model: new M.THREE.Group(), K: { clips: { idle: 'idle', walk: 'walk_fwd' } }, mats: [new M.THREE.MeshStandardMaterial({ color: 0x808080 })], st: 'idle', markId: 'wf_line_0', talk: { lines: ['human'], name: 'a dock worker' }, role: 'docker' };
    const Rr = C.riders[0], keep = { s: Rr.s, st: Rr.st, d: Rr.d, ev: { ...Rr.ev }, lost: Rr.lost }, run = C.running, clk = C.clk, pk = M.player.pos.clone();
    Rr.d = null; Rr.s = 0; Rr.st = 'ride'; Rr.ev = {}; Rr.lost = 0; C.running = 1; C.clk = -1e9;
    M.DUMMIES.push(d); M.wfConvStep(0);
    const order = [], kinds = new Set(); let offBelt = 0, beltN = 0, stair = 0, worst = 0, role = '', steps = 0;
    for (; steps < 4000 && Rr.st !== 'muster'; steps++) { const before = Object.keys(Rr.ev).length; M.wfRide(d, .25, {}); const k = Object.keys(Rr.ev); if (k.length > before) order.push(k[k.length - 1]);
      const P = d.root.position, here = M.wfAt(Rr.s); kinds.add(here.k);
      if (here.k === 'belt') { beltN++; const g = M.groundAt(P.x, P.z, P.y + .3, .6), e = Math.abs(P.y - g); if (e > .15) offBelt++; worst = Math.max(worst, e); }
      if (here.k === 'walk' && P.y > W.Y + .5 && P.y < W.Y + 9.5) { const g = M.groundAt(P.x, P.z, P.y + .4, .8); if (Math.abs(P.y - g) > .4) stair++; } }
    role = d.role; const conv = role === 'cyborg' && d.talk.lines[0] !== 'human';
    M.player.pos.set(W.O[0] + 400, 0, W.O[1] + 400); for (let k = 0; k < 400 && Rr.st === 'muster'; k++) { M.wfRide(d, .25, {}); M.wfConvStep(.25); }
    const back = Rr.st === 'ride' && Rr.s === 0 && d.role === 'docker' && d.talk.lines[0] === 'human';
    M.DUMMIES.splice(M.DUMMIES.indexOf(d), 1); Object.assign(Rr, keep); C.running = run; C.clk = clk; M.player.pos.copy(pk);
    const want = C.STATIONS.map(S => S.id).join(' > ');
    r = marks.length + ' riders (' + (marks.length - nok.length) + ' with kinds) | route ' + C.len.toFixed(0) + ' m over ' + [...kinds].join('/') + ', ' + (steps * .25).toFixed(0) + ' s a lap | stations ' + order.join(' > ') +
      ' | on the belts ' + (beltN - offBelt) + '/' + beltN + ' samples on the floor (worst ' + worst.toFixed(2) + ' m), the tower stair ' + (stair ? stair + ' OFF' : 'on its steps') + ' | out a ' + role + (conv ? ', talking like one' : '') + ' | back to the queue a docker: ' + back;
    why = nok.length ? 'A RIDER WITH NO KIND' : marks.length !== C.n ? 'RIDERS MISSING' : order.join(' > ') !== want ? 'THE STATIONS ARE OUT OF ORDER' : offBelt ? 'A RIDER FLOATS OFF THE BELTS' : stair ? 'A RIDER WALKS OFF THE STAIR'
      : !conv ? 'NOBODY IS CONVERTED' : !back ? 'THE SHIFT NEVER COMES ROUND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'CONVERSION', r, why); }
// ---- THE GANTRY CRANES (m380): the ladders climbs; the landing and the catwalk floor at their heights; the crate stair onto
// the box at its pad; a whole cycle of each crane through the shipped `wfCraneStep` -- every hold with the box ON the floor
// under it (the quay, the barge, the pier), the swing bounded -- and him stood on crane 1's box carried up and out with it
{ const C = M.WCRANE, W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (C.cranes.length && C.cranes[0].tg && W.live) {
    const Y = W.Y, B = Y + C.boom, at = (u, v) => [W.O[0] + u * W.C + v * W.S, W.O[1] - u * W.S + v * W.C];
    const lad = M.KCLIMB.filter(L => /^wf_crane_/.test(L.name || '')).length;
    const floors = C.cranes.map(cr => { const u = cr.K.u, [lx, lz] = at(u + 9.4, 24), [cx, cz] = at(u + 4.25, -20); return [+(M.groundAt(lx, lz, Y + 17.5, 1) - Y).toFixed(2), +(M.groundAt(cx, cz, B + .5, 1) - Y).toFixed(2)]; });
    const pads = C.cranes.map(cr => +(walkUp(cr.climb, Y) - Y).toFixed(2));
    const p = M.player, keep = p.pos.clone(), state = C.cranes.map(cr => ({ v: cr.v, vel: cr.vel, h: cr.h, th: cr.th, om: cr.om, st: cr.st, t: cr.t, at: cr.at })), was = C.on;
    C.on = 1; p.pos.set(W.O[0] + 500, 0, W.O[1] + 500);
    const holds = C.cranes.map(() => []), seq = C.cranes.map(() => []); let swing = 0;
    for (let f = 0; f < 2400; f++) { const st0 = C.cranes.map(cr => cr.st); M.wfCraneStep(.1);
      C.cranes.forEach((cr, i) => { swing = Math.max(swing, Math.abs(cr.th)); if (cr.st !== st0[i]) { if (seq[i][seq[i].length - 1] !== cr.st) seq[i].push(cr.st);
        if (cr.st === 'hold') { const b = cr.bb; b._off = 1; const g = M.groundAt(b.cx, b.cz, b.miny + .3, 1); b._off = 0; holds[i].push(cr.at + ' ' + (b.miny - g).toFixed(2)); } } }); }
    // the ride: on crane 1's box at its land hold, carried to the far hold
    const c1 = C.cranes[0]; Object.assign(c1, { v: c1.K.land, vel: 0, h: Y, th: 0, om: 0, st: 'hold', t: .5, at: 'land' }); M.wfCraneStep(0);
    p.pos.set(c1.bb.cx + .5, c1.bb.maxy, c1.bb.cz); const p0 = p.pos.clone(); let top = 0, rode = 0;
    for (let f = 0; f < 1200 && !(c1.st === 'hold' && c1.at === 'sea'); f++) { p.grounded = true; p.vel.y = 0; M.wfCraneStep(.1); top = Math.max(top, p.pos.y); }
    rode = Math.abs(p.pos.y - c1.bb.maxy) < .1 && Math.hypot(p.pos.x - c1.bb.cx - .5 * 0, p.pos.z - c1.bb.cz) < 7 ? Math.hypot(p.pos.x - p0.x, p.pos.z - p0.z) : 0;
    C.cranes.forEach((cr, i) => Object.assign(cr, state[i])); C.on = was; M.wfCraneStep(0); p.pos.copy(keep);
    const bad1 = holds.flat().filter(h => Math.abs(+h.split(' ')[1]) > .05);
    r = C.cranes.length + ' cranes | ladders ' + lad + ' | landing / catwalk ' + floors.map(f => f.join(' / ')).join(', ') + ' (want 17 / ' + C.boom + ') | crate stairs onto the box ' + pads.join(', ') + ' (want 3)' +
      ' | cycles ' + seq.map(q => q.join('>')).join(' ; ') + ' | holds on the floor: ' + holds.map(h => h.join(', ')).join(' ; ') + ' | swing ' + swing.toFixed(2) + ' rad | rode crane 1\'s box ' + rode.toFixed(1) + ' m out, up to ' + (top - Y).toFixed(1) + ' m';
    why = lad !== 2 * C.cranes.length ? 'A CRANE LADDER IS NOT A CLIMB' : floors.some(([a, b]) => Math.abs(a - 17) > .1 || Math.abs(b - C.boom) > .1) ? 'NO FLOOR UP THE CRANE' : pads.some(v => Math.abs(v - 3) > .1) ? 'THE BOX CANNOT BE BOARDED'
      : seq.some(q => q.join('>').indexOf('up>go>down>hold') < 0) ? 'A CRANE NEVER WORKS ITS CYCLE' : bad1.length ? 'A BOX HOLDS OFF THE FLOOR: ' + bad1.join(', ') : swing > .34 ? 'THE BOX SWINGS WILD' : rode < 25 || top - Y < C.hoist ? 'THE BOX DOES NOT CARRY HIM' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'CRANES', r, why); }
// ---- THE FERRY (m381): Old Town's landing on the shore with nothing else standing on its stage; WALKED from the grass to
// the pontoon, and from pier 1 down its stair to the far one; the boat's own cycle through the shipped `ferryStep`, boarded
// from each pontoon, and him on its deck carried the whole way over
{ const O = M.OFERRY, W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (O.frame && W.live) {
    const Fr = O.frame, at = (u, v) => [Fr.R0[0] + u * Fr.C + v * Fr.S, Fr.R0[1] - u * Fr.S + v * Fr.C], pont = Fr.sea + O.pont, deckY = Fr.sea + O.boatH;
    const otw = walkUp(O.otWalk, M.groundAt(O.otWalk[0][0], O.otWalk[0][1], 30, 40)), wfw = walkUp(O.wfWalk, M.groundAt(O.wfWalk[0][0], O.wfWalk[0][1], W.Y + .5, .6));
    // the stage clear: nothing but its own on its 10 x 10
    const [s0x, s0z] = at(0, 5), clut = M.BOXES.filter(b => b.farm !== 'ferry' && b.maxy > Fr.dy + .2 && b.miny < Fr.dy + 2 && (() => { const cx = (b.minx + b.maxx) / 2 - s0x, cz = (b.minz + b.maxz) / 2 - s0z, lu = cx * Fr.C - cz * Fr.S, lv = cx * Fr.S + cz * Fr.C; return Math.abs(lu) < 5.5 && Math.abs(lv) < 5.5; })()).length;
    const keep = { s: O.s, st: O.st, t: O.t, at: O.at, v: O.v }, p = M.player, pk = p.pos.clone();
    // boarding at each end: from the pontoon onto the deck's middle, by a walk
        const board = e => { O.s = O.ends[e]; O.at = e; M.ferryPlace(); const [a, b2] = e ? [Fr.vFP, O.s] : [Fr.vEnd + 4.8, O.s], A = at(0, a), B = at(0, b2); return walkUp([A, B], pont); };
    Object.assign(O, { st: 'dock', t: 1e9 }); const b0 = board(0), b1 = board(1);
    // the crossing, him on the deck
    Object.assign(O, { s: O.ends[0], st: 'dock', t: .2, at: 0, v: 0 }); M.ferryPlace();
    const [dx0, dz0] = at(0, O.ends[0] - 4); p.pos.set(dx0, deckY, dz0); const p0 = p.pos.clone(); let f = 0;
    for (; f < 1500 && !(O.st === 'dock' && O.at === 1); f++) { p.grounded = true; p.vel.y = 0; M.ferryStep(.1); }
    const rode = Math.abs(p.pos.y - deckY) < .05 ? Math.hypot(p.pos.x - p0.x, p.pos.z - p0.z) : 0, want = Math.abs(O.ends[1] - O.ends[0]);
    Object.assign(O, keep); M.ferryPlace(); p.pos.copy(pk);
    const ppl = M.MARKS.filter(m => m.src === 'FERRY'), nok = ppl.filter(m => !m.K);
    r = 'the landing at ' + O.deg.toFixed(0) + ' deg, ' + clut + ' foreign boxes on its stage | grass -> jetty -> pontoon ' + (otw - pont).toFixed(2) + ' | pier 1 -> stair -> pontoon ' + (wfw - pont).toFixed(2) +
      ' (pontoons at ' + pont.toFixed(2) + ') | boarded ' + (b0 - deckY).toFixed(2) + ' / ' + (b1 - deckY).toFixed(2) + ' (deck ' + deckY.toFixed(2) + ') | crossing ' + want.toFixed(0) + ' m in ' + (f * .1).toFixed(0) + ' s, rode it ' + rode.toFixed(1) + ' m | people ' + ppl.map(m => m.name).join(', ');
    why = clut ? 'SOMETHING STANDS ON THE LANDING' : Math.abs(otw - pont) > .1 ? 'THE LANDING DOES NOT REACH ITS PONTOON' : Math.abs(wfw - pont) > .1 ? 'PIER 1 DOES NOT REACH ITS PONTOON'
      : Math.abs(b0 - deckY) > .05 || Math.abs(b1 - deckY) > .05 ? 'THE BOAT CANNOT BE BOARDED' : Math.abs(rode - want) > .5 ? 'THE BOAT DOES NOT CARRY HIM' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'FERRY', r, why); }
// ---- THE SWING BRIDGE (m382): WALKED from the island's grass up the ramp, over the shut span to the quay; the same walk
// with it open goes in the river; nothing foreign on its ramp; a whole swing through the shipped `swingStep`, him stood on the
// span carried round a quarter turn about the pivot and still on its deck
{ const O = M.OSWING, W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (O.grp && W.live) {
    const keep = { st: O.st, t: O.t, a: O.a }, p = M.player, pk = p.pos.clone(), Y = W.Y;
    const go = () => walkUp(O.walk, M.groundAt(O.walk[0][0], O.walk[0][1], 30, 40));
    Object.assign(O, { st: 'shut', t: 1e9, a: 0 }); M.swingPlace(); const shut = go();
    Object.assign(O, { st: 'open', t: 1e9, a: Math.PI / 2 }); M.swingPlace(); const open = go();
    // foreign boxes on the ramp and the island span (not its own, not the island's ground)
    const at = (u, v) => [W.O[0] + u * W.C + v * W.S, W.O[1] - u * W.S + v * W.C], { vW, vF, gF } = O.frame;
    const clut = M.BOXES.filter(b => b.farm !== 'swing' && !b.dyn && b.maxy > Math.min(gF, Y) + .3 && (() => { const cx = (b.minx + b.maxx) / 2 - W.O[0], cz = (b.minz + b.maxz) / 2 - W.O[1], u = cx * W.C - cz * W.S, v = cx * W.S + cz * W.C;
      return Math.abs(u - O.u) < O.w / 2 + 1 && v < O.ends[1] && v > vF - 3; })()).map(b => b.farm || 'box');
    // the ride: on the shut span 12 m out from the pivot, through the warning and the opening
    Object.assign(O, { st: 'shut', t: .1, a: 0 }); M.swingPlace();
    const [sx, sz] = at(O.u + 1, O.pivot + 12), [px, pz] = at(O.u, O.pivot); p.pos.set(sx, Y, sz); const r0 = Math.atan2(sz - pz, sx - px); let f = 0, seen = [O.st];
    for (; f < 800 && O.st !== 'open'; f++) { p.grounded = true; p.vel.y = 0; M.swingStep(.1); if (seen[seen.length - 1] !== O.st) seen.push(O.st); }
    const turned = Math.atan2(p.pos.z - pz, p.pos.x - px) - r0, dr = Math.abs(Math.hypot(p.pos.x - px, p.pos.z - pz) - Math.hypot(sx - px, sz - pz)), onDeck = Math.abs(p.pos.y - O.boxes[0].maxy) < .05;
    const turnAbs = Math.abs(((turned + Math.PI * 3) % (Math.PI * 2)) - Math.PI);
    Object.assign(O, keep); M.swingPlace(); p.pos.copy(pk);
    const ppl = M.MARKS.filter(m => m.src === 'SWING'), nok = ppl.filter(m => !m.K);
    r = 'landing at ' + O.deg.toFixed(0) + ' deg, ramp ' + (vW - vF).toFixed(1) + ' m down to ' + gF.toFixed(2) + ' | grass -> quay shut ' + shut.toFixed(2) + ' (quay ' + Y + '), open ' + open.toFixed(2) + ' | foreign on its ramp: ' + (clut.length ? clut.join(', ') : 'none') +
      ' | ' + seen.join(' > ') + ': carried ' + (turnAbs * 180 / Math.PI).toFixed(1) + ' deg round the pivot (radius kept to ' + dr.toFixed(3) + ' m), ' + (onDeck ? 'still on the deck' : 'OFF THE DECK') + ' | people ' + ppl.map(m => m.name).join(', ');
    why = Math.abs(shut - Y) > .1 ? 'THE SHUT BRIDGE IS NOT A WAY OVER' : open > Y - 1 ? 'THE OPEN BRIDGE IS STILL A WAY OVER' : clut.length ? 'SOMETHING STANDS ON THE RAMP' : Math.abs(turnAbs - Math.PI / 2) > .03 || dr > .05 || !onDeck ? 'THE SPAN DOES NOT CARRY HIM ROUND' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'SWING', r, why); }
// ---- THE ENGINEER (m383): a ROLE's form -- the engineers have kinds, `ENGINEER` resolves to one and is a form apart from
// the same body worn plain; Uplift's gate (a real `GATES` gate, fence 3.4 m) turns away the plain body and lets the engineer
// through (the shipped `gatePush`); the bridge's control box ignores the plain body and swings for the engineer
{ const W = M.WFRONT, O = M.OSWING; let r = 'NOT BUILT', why = '';
  const G = M.GATES.find(g => g.id === 'wf_gate');
  if (W.live && G && O.ctl) {
    const ppl = M.MARKS.filter(m => /^wf_(ivy|dex)$/.test(m.id)), nok = ppl.filter(m => !m.K), rk = M.rosterKind(M.ROSTER.find(q => q.id === 'hacker')), K = M.formKind('ENGINEER') || (rk === (ppl[0] && ppl[0].K) ? rk : null);   // no skins here, so `dnaOK` is false: the role's kind IS the engineers' kind
    const p = M.player, keep = { K: p.mphK, R: p.mphRole, St: p.mphSt, pos: p.pos.clone() }, sw = { st: O.st, t: O.t, a: O.a };
    const as = role => { p.mphK = K; p.mphRole = role; p.mphSt = 0; return [M.formNow(), M.socialMe(), M.gateLets(M.GATE_TYPES.uplift)]; };
    const plain = as(null), eng = as('hacker');
    // through the gate: outside the fence to inside, a step at a time
    const s = Math.sin(G.h), c = Math.cos(G.h), cross = role => { as(role); G.side = 0; let v = -1.4; for (; v <= 1.4; v += .1) { p.pos.set(G.x + s * v, G.y, G.z + c * v); M.gatePush(.016); const vv = (p.pos.x - G.x) * s + (p.pos.z - G.z) * c; if (vv < v - .05) return false; } return true; };
    const passPlain = cross(null), passEng = cross('hacker');
    // the bridge's control box: shut bridge, at the box
    const ctl = role => { Object.assign(O, { st: 'shut', t: 30, a: 0 }); M.WFSEC.ctlT = 0; as(role); p.pos.set(O.ctl[0], W.Y, O.ctl[1]); M.wfSecStep(.016); return O.t; };
    const tPlain = ctl(null), tEng = ctl('hacker');
    Object.assign(O, sw); Object.assign(p, { mphK: keep.K, mphRole: keep.R, mphSt: keep.St }); p.pos.copy(keep.pos); G.side = 0; M.WFSEC.ctlT = 0; M.WFSEC.sayT = 0;
    const fenceTop = Math.max(...M.BOXES.filter(b => b.farm === 'wfront' && b.maxy - b.miny > 3 && b.maxy - b.miny < 3.6 && Math.abs(b.miny - W.Y) < .01).map(b => b.maxy - b.miny), 0);
    r = 'engineers ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ') + ' | ENGINEER -> ' + (K ? 'a kind' : 'NOTHING') + ' | the plain body is ' + plain.join('/') + ', the engineer ' + eng.join('/') +
      ' | the gate: plain ' + (passPlain ? 'THROUGH' : 'turned back') + ', engineer ' + (passEng ? 'through' : 'TURNED BACK') + ' | fence ' + fenceTop.toFixed(1) + ' m | the bridge box: plain ' + (tPlain > 0 ? 'ignored' : 'SWUNG IT') + ', engineer ' + (tEng <= 0 ? 'swung it' : 'IGNORED');
    why = nok.length ? 'AN ENGINEER WITH NO KIND' : !K ? 'THE ENGINEER FORM RESOLVES TO NOTHING' : plain[0] === eng[0] || eng[0] !== 'ENGINEER' ? 'THE ROLE IS NOT A FORM' : plain[2] || !eng[2] ? 'THE GATE ASKS THE WRONG THING'
      : passPlain || !passEng ? 'THE GATE DOES NOT SORT THEM' : fenceTop < 3.2 ? 'THE FENCE CAN BE HOPPED' : tPlain <= 0 || tEng > 0 ? 'THE BRIDGE BOX DOES NOT SORT THEM' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'ENGINEER', r, why); }
// ---- UPLIFT'S TURRETS (m384): built and each panel on a floor; through the shipped `wfTurretStep` they fire on the alien
// out in the lot, not on him inside the factory (the walls between), not on the engineer, and not once the engineer has
// turned them -- and a turned one stays turned
{ const U = M.WTUR, W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (U.list.length && W.live) {
    const at = (u, v) => [W.O[0] + u * W.C + v * W.S, W.O[1] - u * W.S + v * W.C], p = M.player, keep = { K: p.mphK, R: p.mphRole, St: p.mphSt, pos: p.pos.clone() };
    const flags = U.list.map(R => [R.ours, M.SAVE.flags['wf:turret:' + R.i]]);
    const panels = U.list.map(R => +(M.groundAt(R.panel[0] + .9, R.panel[2], R.panel[1] + .5, 1) - R.panel[1]).toFixed(2));
    const run = (u, v, y, role, K, s) => { U.list.forEach(R => Object.assign(R, { st: 'sweep', t: 0, n: 0, yaw: R.rest, shots: 0 })); Object.assign(p, { mphK: K, mphRole: role, mphSt: 0 });
      const [x, z] = at(u, v); p.pos.set(x, y, z); p.vel.set(0, 0, 0); for (let f = 0; f < (s || 120); f++) M.wfTurretStep(.05); return U.list.map(R => R.shots); };
    const Ke = (M.MARKS.find(m => m.id === 'wf_ivy') || {}).K;
    const open = run(-78, 59, W.Y, null, null), inside = run(-70, 70, W.Y, null, null), eng = run(-78, 59, W.Y, 'hacker', Ke);
    // the engineer at each panel turns it, then the alien in the open again
    U.list.forEach(R => { Object.assign(p, { mphK: Ke, mphRole: 'hacker', mphSt: 0 }); p.pos.set(R.panel[0], R.panel[1], R.panel[2]); M.wfTurretStep(.05); });
    const turned = U.list.filter(R => R.ours).length, after = run(-78, 59, W.Y, null, null);
    U.list.forEach((R, i) => { R.ours = flags[i][0]; if (!flags[i][1]) delete M.SAVE.flags['wf:turret:' + R.i]; Object.assign(R, { st: 'sweep', t: 0, n: 0, yaw: R.rest }); R.laser.visible = false; });
    Object.assign(p, { mphK: keep.K, mphRole: keep.R, mphSt: keep.St }); p.pos.copy(keep.pos);
    const sum = a => a.reduce((x, y) => x + y, 0);
    r = U.list.length + ' turrets | panels on their floors ' + panels.join(', ') + ' | in 6 s the alien out in the lot drew ' + open.join('/') + ' rounds, inside the hall ' + inside.join('/') + ', the engineer ' + eng.join('/') + ' | the engineer turned ' + turned + ', then the alien drew ' + after.join('/');
    why = panels.some(v => Math.abs(v) > .1) ? 'A PANEL OFF ITS FLOOR' : sum(open) < 3 ? 'THE TURRETS DO NOT FIRE' : sum(inside) ? 'A TURRET FIRES THROUGH THE WALLS' : sum(eng) ? 'A TURRET FIRES ON THE ENGINEER' : turned < U.list.length ? 'A TURRET CANNOT BE TURNED' : sum(after) ? 'A TURNED TURRET STILL FIRES' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'TURRETS', r, why); }
// ---- UPLIFT'S ROBOTS (m385): their marks have kinds and their beats are floor; a robot (a body fabricated the way the game
// holds one) through the shipped `wfBot` walks its beat, runs at the alien in its sight and shoves him, stands down for the
// engineer; and a turned turret fires on a robot it can see
{ const U = M.WBOT, W = M.WFRONT; let r = 'NOT BUILT', why = '';
  if (U.list.length && W.live) {
    const marks = M.MARKS.filter(m => m.src === 'WBOT'), nok = marks.filter(m => !m.K);
    const beats = U.list.map(R => R.pts.filter(([x, z]) => Math.abs(M.groundAt(x, z, W.Y + .5, 1) - W.Y) > .1).length);
    const p = M.player, keep = { K: p.mphK, R: p.mphRole, St: p.mphSt, pos: p.pos.clone(), g: p.grounded }, Ke = (M.MARKS.find(m => m.id === 'wf_ivy') || {}).K;
    const K = Object.assign({}, (marks[0] && marks[0].K) || {}, { clips: { idle: 'idle', walk: 'walk', run: 'run' }, r: .42, h: 1.75, turn: 6 });
    const R = U.list[1], fake = () => { const d = { root: new M.THREE.Group(), model: new M.THREE.Group(), K, st: 'idle', stuckT: 0, slideT: 0, h: 0, wbR: R }; d.root.position.set(R.pts[0][0], W.Y, R.pts[0][1]); return d; };
    const keepR = { d: R.d, st: R.st, wp: R.wp, t: R.t, seenT: R.seenT, parts: R.parts }; R.parts = null;
    // its beat, with him far off
    let d = fake(); Object.assign(R, { d, st: 'patrol', wp: 1, t: 0, seenT: 0 }); p.pos.set(W.O[0] + 500, 0, W.O[1] + 500);
    let walked = 0, lx = d.root.position.x, lz = d.root.position.z, off = 0;
    for (let f = 0; f < 400; f++) { M.wfBot(d, .05, {}); const q = d.root.position; walked += Math.hypot(q.x - lx, q.z - lz); lx = q.x; lz = q.z; if (Math.abs(q.y - W.Y) > .1) off++; }
    // the alien in its sight, 8 m off along the lane
    const near = role => { d = fake(); Object.assign(R, { d, st: 'patrol', wp: 1, t: 0, seenT: 0 }); const s0 = U.shoves; Object.assign(p, { mphK: role ? Ke : null, mphRole: role, mphSt: 0 });
      const [x0, z0] = R.pts[0], [x1, z1] = R.pts[1], L = Math.hypot(x1 - x0, z1 - z0); p.pos.set(x0 + (x1 - x0) / L * 8, W.Y, z0 + (z1 - z0) / L * 8);
      for (let f = 0; f < 80; f++) M.wfBot(d, .05, {}); return [+Math.hypot(p.pos.x - d.root.position.x, p.pos.z - d.root.position.z).toFixed(1), U.shoves - s0, R.st]; };
    const alien = near(null), eng = near('hacker');
    Object.assign(R, keepR); Object.assign(p, { mphK: keep.K, mphRole: keep.R, mphSt: keep.St, grounded: keep.g }); p.pos.copy(keep.pos);
    // a turned turret and a robot in its sight
    const T2 = M.WTUR.list[1], b = fake(); b.root.position.set(T2.x - 6, W.Y, T2.z - 4); const R1 = U.list[0], kd = R1.d; R1.d = b; const ours = T2.ours, sh = M.WTUR.botShots || 0;
    const tk = M.WTUR.list.map(T => [T.ours, T.st, T.yaw]); M.WTUR.list.forEach(T => { T.ours = T === T2 ? 1 : T.ours; T.st = 'sweep'; });
    let blowErr = 0; for (let f = 0; f < 80; f++) { try { M.wfTurretStep(.05); } catch (e) { blowErr++; b.st = 'idle'; } }    // a fabricated body is not every field `dummyBlow` reads: the SHOTS are what is counted
    const fired = (M.WTUR.botShots || 0) - sh; M.WTUR.list.forEach((T, i) => { T.ours = tk[i][0]; T.st = tk[i][1]; T.yaw = tk[i][2]; T.laser.visible = false; T.tracer.visible = false; }); R1.d = kd; T2.ours = ours;
    r = marks.length + ' robots (' + (marks.length - nok.length) + ' with kinds) | beats off the floor ' + beats.join('/') + ' | unit 2 walked ' + walked.toFixed(1) + ' m of its beat in 20 s' + (off ? ', ' + off + ' frames OFF THE FLOOR' : '') +
      ' | the alien 8 m off: it closed to ' + alien[0] + ' m and shoved ' + alien[1] + ' (' + alien[2] + ') | the engineer: ' + eng[0] + ' m, ' + eng[1] + ' shoves (' + eng[2] + ') | a turned turret fired ' + fired + ' rounds at a robot it could see';
    why = nok.length ? 'A ROBOT WITH NO KIND' : beats.some(n => n) ? 'A BEAT OFF THE FLOOR' : walked < 15 || off ? 'A ROBOT CANNOT WALK ITS BEAT' : alien[0] > U.shoveR + .3 || alien[1] < 1 ? 'A ROBOT DOES NOT SEE HIM OFF' : eng[1] || eng[2] !== 'stand' || eng[0] < 7 ? 'A ROBOT DOES NOT STAND DOWN' : fired < 1 ? 'A TURNED TURRET IGNORES THE ROBOTS' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'ROBOTS', r, why); }
// ---- CHAPTER 4 OPENS (m386): arriving on the Waterfront's land sets `wf:in` (the shipped `wfSecStep`), and the chapter's
// first task is the one picked in chapter 4
{ const F = M.SAVE.flags, p = M.player, W = M.WFRONT, keep = { pos: p.pos.clone(), g: p.grounded, ch: M.SAVE.ch }, was = F['wf:in']; let r = '', why = '';
  delete F['wf:in']; const [x, , z] = W.quayAt; p.pos.set(x, W.Y, z); p.grounded = true; M.wfSecStep(.016); const set = !!F['wf:in'];
  if (was) F['wf:in'] = was; else delete F['wf:in']; p.pos.copy(keep.pos); p.grounded = keep.g;
  const q = M.QUESTS.find(q => q.id === 'ch4');
  r = 'on the quay: wf:in ' + (set ? 'set' : 'NOT SET') + ' | ch4 ' + (q ? q.steps.map(s => s.type).join(' > ') : 'MISSING');
  why = !set ? 'ARRIVING IS NOT NOTICED' : !q ? 'NO CHAPTER 4' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'CH4', r, why); }
// ---- THE LEVER (m387): the plain body at it does nothing, the engineer stops the line (`line:off`) and the line's clock with
// it; then the converted come back to themselves one at a time through the shipped `wfSecStep` (two fabricated cyborgs on
// the quay), and when the last is back, `line:freed`
{ const F = M.SAVE.flags, W = M.WFRONT, L = M.WFLINE, C = M.WFCONV, S = M.WFSEC; let r = 'NOT BUILT', why = '';
  if (W.live && L.leverAt) {
    const p = M.player, keep = { K: p.mphK, R: p.mphRole, St: p.mphSt, pos: p.pos.clone() }, kf = { off: F['line:off'], fr: F['line:freed'] }, kc = { running: C.running, clk: C.clk, off: C.off }, ks = { quietT: S.quietT, waveT: S.waveT, sayT: S.sayT, red: S.red };
    const Ke = (M.MARKS.find(m => m.id === 'wf_ivy') || {}).K, Lv = L.leverAt;
    delete F['line:off']; delete F['line:freed']; S.quietT = 0; S.sayT = 0;
    Object.assign(p, { mphK: Ke, mphRole: null, mphSt: 0 }); p.pos.set(Lv[0], Lv[1], Lv[2]); M.wfSecStep(.016); const plain = !!F['line:off'];
    Object.assign(p, { mphRole: 'hacker' }); M.wfSecStep(.016); const eng = !!F['line:off']; M.wfConvStep(.016); const stopped = !C.running && !L.run;
    // two converted on the quay
    const mk = (u, v) => { const d = { root: new M.THREE.Group(), model: new M.THREE.Group(), K: { clips: {} }, mats: [new M.THREE.MeshStandardMaterial({ color: 0x8090a0 })], role: 'cyborg', cyDone: 0, talk: { lines: ['OPTIMAL.'] } }; d.matCol0 = [new M.THREE.Color(0x806040)];
      d.root.position.set(W.O[0] + u * W.C + v * W.S, W.Y, W.O[1] - u * W.S + v * W.C); M.DUMMIES.push(d); return d; };
    const a = mk(-35, 122), b = mk(-41, 122); p.pos.set(a.root.position.x + 200, W.Y, a.root.position.z); let f = 0, order = [];
    for (; f < 200 && !F['line:freed']; f++) { M.wfSecStep(.05); for (const d of [a, b]) if (d.cyDone && !order.includes(d)) order.push(d); }
    const back = [a, b].filter(d => d.cyDone && d.role === null && d.talk.lines[0] !== 'OPTIMAL.').length, freed = !!F['line:freed'];
    M.DUMMIES.splice(M.DUMMIES.indexOf(a), 1); M.DUMMIES.splice(M.DUMMIES.indexOf(b), 1);
    for (const k of ['line:off', 'line:freed']) delete F[k]; if (kf.off) F['line:off'] = kf.off; if (kf.fr) F['line:freed'] = kf.fr; Object.assign(C, kc); Object.assign(S, ks);
    if (!kf.off && W.MAT && W.MAT.screen) W.MAT.screen.emissive.setHex(0x3aff6a);
    Object.assign(p, { mphK: keep.K, mphRole: keep.R, mphSt: keep.St }); p.pos.copy(keep.pos);
    r = 'the plain body at the lever: ' + (plain ? 'PULLED IT' : 'nothing') + ' | the engineer: ' + (eng ? 'pulled it' : 'NOTHING') + ', the line ' + (stopped ? 'stopped' : 'STILL RUNNING') + ' | two converted on the quay: ' + back + ' back to themselves in ' + (f * .05).toFixed(1) + ' s, one at a time: ' + (order.length === 2) + ' | line:freed ' + freed;
    why = plain ? 'ANYBODY CAN STOP THE LINE' : !eng ? 'THE ENGINEER CANNOT STOP THE LINE' : !stopped ? 'THE LINE KEEPS RUNNING' : back < 2 ? 'THE CONVERTED STAY CONVERTED' : !freed ? 'THE LAST ONE BACK IS NOT NOTICED' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'LEVER', r, why); }
// ---- CHAPTER 4's BOSS (m388): while the thing wearing the supervisor stands the robots chase even the engineer (`alarm`), and
// once he is beaten (`qdone:ch4c`) the robots and the turrets power down for good -- both through the shipped steps
{ const U = M.WBOT, T = M.WTUR, W = M.WFRONT, F = M.SAVE.flags; let r = 'NOT BUILT', why = '';
  const sup = M.MARKS.find(m => m.id === 'wf_super');
  if (U.list.length && T.list.length && sup) {
    const p = M.player, keep = { K: p.mphK, R: p.mphRole, St: p.mphSt, pos: p.pos.clone() }, Ke = (M.MARKS.find(m => m.id === 'wf_ivy') || {}).K, was = F['qdone:ch4c'];
    const K = Object.assign({}, (M.MARKS.find(m => m.src === 'WBOT') || {}).K || {}, { clips: { idle: 'idle', walk: 'walk', run: 'run' }, r: .42, h: 1.75, turn: 6 });
    const R = U.list[1], keepR = { d: R.d, st: R.st, wp: R.wp, t: R.t, seenT: R.seenT, parts: R.parts }; R.parts = null;
    const chase = () => { const d = { root: new M.THREE.Group(), model: new M.THREE.Group(), K, st: 'idle', stuckT: 0, slideT: 0, h: 0, wbR: R }; d.root.position.set(R.pts[0][0], W.Y, R.pts[0][1]);
      Object.assign(R, { d, st: 'patrol', wp: 1, t: 0, seenT: 0 }); const s0 = U.shoves; Object.assign(p, { mphK: Ke, mphRole: 'hacker', mphSt: 0 });
      const [x0, z0] = R.pts[0], [x1, z1] = R.pts[1], L = Math.hypot(x1 - x0, z1 - z0); p.pos.set(x0 + (x1 - x0) / L * 8, W.Y, z0 + (z1 - z0) / L * 8);
      for (let f = 0; f < 80; f++) { M.wfBotStep(.05); M.wfBot(d, .05, {}); } return [R.st, U.shoves - s0]; };
    const boss = { root: new M.THREE.Group(), K: M.FOE, qTag: 'ch4boss', gone: 0 }; M.DUMMIES.push(boss);
    const inAlarm = chase(); M.DUMMIES.splice(M.DUMMIES.indexOf(boss), 1); const after = chase();
    F['qdone:ch4c'] = 1; Object.assign(p, { mphK: null, mphRole: null }); const dead = chase();
    T.list.forEach(t => Object.assign(t, { st: 'sweep', t: 0, n: 0, yaw: t.rest, shots: 0 })); const [lx, lz] = [W.O[0] + -78 * W.C + 59 * W.S, W.O[1] - -78 * W.S + 59 * W.C]; p.pos.set(lx, W.Y, lz);
    for (let f = 0; f < 120; f++) M.wfTurretStep(.05); const tShots = T.list.reduce((a, t) => a + t.shots, 0);
    if (was) F['qdone:ch4c'] = was; else delete F['qdone:ch4c']; T.list.forEach(t => { t.st = 'sweep'; t.lensM.emissive.setHex(t.ours ? 0x3aff6a : 0xff3a3a); });
    Object.assign(R, keepR); Object.assign(p, { mphK: keep.K, mphRole: keep.R, mphSt: keep.St }); p.pos.copy(keep.pos);
    r = 'the supervisor (' + (sup.K ? 'a kind' : 'NO KIND') + ') | with the boss standing, unit 2 and the engineer: ' + inAlarm.join(', ') + ' shoves | after it: ' + after.join(', ') + ' | beaten: robots ' + dead.join(', ') + ' shoves, turrets ' + tShots + ' rounds at the alien in the open';
    why = !sup.K ? 'THE SUPERVISOR HAS NO KIND' : inAlarm[0] !== 'chase' ? 'THE ROBOTS STAND DOWN IN THE ALARM' : after[0] !== 'stand' ? 'THE ALARM NEVER ENDS' : dead[1] || dead[0] === 'chase' ? 'THE ROBOTS ARE STILL ON AFTER HIM' : tShots ? 'THE TURRETS ARE STILL ON AFTER HIM' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'BOSS4', r, why); }
// ---- THE RIVER ISLANDS (m389): built and clear of every other land; each island's top at its height; WATER in every gap
// between neighbours (the region's problem); every ladder a climb, standing on the beach and topping out on the top; the
// landing rock walked from its beach to its top
{ const I = M.ISLES; let r = 'NOT BUILT', why = '';
  if (I.live) {
    const sea = M.ISLE.sea, R = M.ISLE.rect, pr = (M.MAPREG.tkit || []).find(q => q.id === 'pearl'); let clash = [];
    for (const K of I.ISLANDS) for (let k = 0; k < 24; k++) { const a = k / 24 * Math.PI * 2, [x, z] = M.islWorld(K.u + Math.cos(a) * K.r * 1.2, K.v + Math.sin(a) * K.r * 1.2);
      if (M.FARMLAND.live && M.flEdgeAt(x, z) > -15) clash.push('the farm');
      if (M.HCREEK.live && M.hcEdge(...M.hcLocal(x, z)) > -15) clash.push('hollow creek');
      if (M.WFRONT.live && M.wfEdge(x, z) > -20) clash.push('the waterfront');
      if (x > R[0] - 40 && x < R[1] + 40 && z > R[2] - 40 && z < R[3] + 40) clash.push('the island');
      if (pr && x > pr.x0 - 30 && x < pr.x1 + 30 && z > pr.z0 - 30 && z < pr.z1 + 30) clash.push('the pearl'); }
    clash = [...new Set(clash)];
    const g = (u, v) => { const [x, z] = M.islWorld(u, v); return M.groundAt(x, z, 60, 80); };
    const tops = I.ISLANDS.map(K => [K.id, +(g(K.u + K.r * .3, K.v) - sea).toFixed(1), K.kind === 'humps' ? null : K.h]);      // .3 r in: off the lighthouse, on the top
    const offTop = tops.filter(([, h, want]) => want != null && Math.abs(h - want) > 1.2);
    const pairs = [['landing', 'mesa'], ['mesa', 'needle'], ['needle', 'pier'], ['landing', 'pier'], ['mesa', 'humps'], ['needle', 'light'], ['humps', 'light']];
    const Kn = id => I.ISLANDS.find(q => q.id === id);
    const gaps = pairs.map(([a, b]) => { const A = Kn(a), B = Kn(b); let lo = 1e9; for (let t = .3; t <= .7; t += .02) lo = Math.min(lo, g(A.u + (B.u - A.u) * t, A.v + (B.v - A.v) * t)); return [a + '-' + b, lo < -100 ? 'sea' : +(lo - sea).toFixed(1)]; });
    const dry = gaps.filter(([, h]) => h !== 'sea' && h > -.2);
    const lads = M.KCLIMB.filter(L => /^is_/.test(L.name || '')).length;
    const ladOff = I.ladderAt.filter(([lu, lv, y0, top, mu, mv]) => Math.abs(g(lu + .0, lv) - y0) > .5 && Math.abs(g(lu, lv) - y0) > .5 || Math.abs(g(mu, mv) - top) > .4);
    const L = Kn('landing'), [bx0, bz0] = M.islWorld(L.u, L.v - L.r * .92), [cx0, cz0] = M.islWorld(L.u, L.v), up = walkUp([[bx0, bz0], [cx0, cz0]], M.groundAt(bx0, bz0, 60, 80));
    r = I.chunks + ' chunks, ' + I.tris + ' floor tris | centre ' + I.O.map(v => v.toFixed(0)).join(',') + ' | clear of ' + (clash.length ? 'NOT ' + clash.join(', ') : 'the farm, hollow creek, the waterfront, the island, the pearl') +
      ' | tops ' + tops.map(([id, h]) => id + ' ' + h).join(', ') + ' | the gaps (lowest, over the sea) ' + gaps.map(q => q.join(' ')).join(', ') + ' | ladders ' + I.ladders + ' (' + lads + ' climbs: ' + I.ladderAt.map(([lu, lv, y0, top, mu, mv]) => (g(lu, lv) - y0).toFixed(2) + '/' + (g(mu, mv) - top).toFixed(2) + ' h' + (top - y0).toFixed(1)).join(', ') + ') | landing rock walked to ' + (up - sea).toFixed(1);
    why = clash.length ? 'IT OVERLAPS ANOTHER LAND' : offTop.length ? 'AN ISLAND AT THE WRONG HEIGHT: ' + offTop.map(q => q[0]).join(', ') : dry.length ? 'NO WATER BETWEEN ' + dry.map(q => q[0]).join(', ')
      : lads < I.ladders || I.ladders < 4 ? 'A LADDER IS NOT A CLIMB' : ladOff.length ? 'A LADDER OFF ITS BEACH OR ITS TOP' : Math.abs(up - sea - L.h) > 1.2 ? 'THE LANDING ROCK CANNOT BE WALKED' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'ISLANDS', r, why); }
// ---- THE OLD PIER'S SKATE PARK (m390): built on the pier island; the deck floor at its height and walked onto from the
// island; every surface the board rides at the height it was built to (the quarter pipe's curve and its top, the funbox's
// banks and top, the kickers, the ledge up its steps); the four locals each a real body, Rollergirl among them
{ const S = M.ISKATE, I = M.ISLES; let r = 'NOT BUILT', why = '';
  if (S.n && S.y != null) {
    const y = S.y, g = (u, v, h) => { const [x, z] = M.islWorld(u, v); return +(M.groundAt(x, z, y + h, .3) - y).toFixed(2); };
    const qu0 = S.u1 - 5.5, a50 = 50 * Math.PI / 180;
    const want = [['deck', 75, 23, 0], ['deck far', 96, 24, 0], ['qp low', qu0 + 4 * Math.sin(a50 / 2), 24, 4 * (1 - Math.cos(a50 / 2))], ['qp high', qu0 + 4 * Math.sin(a50), 24, 4 * (1 - Math.cos(a50))],
      ['qp deck', 104, 24, S.qpTop], ['funbox bank', 80.5, 24, .35], ['funbox top', 84, 24, .7], ['kicker', 71, 19.5, .45], ['kicker 2', 71, 28.5, .45], ['ledge', 95, 31.4, .9], ['manual', 78, 31.6, .25]];
    const got = want.map(([nm, u, v, h]) => [nm, g(u, v, h), +h.toFixed(2)]), off = got.filter(([, a, b]) => Math.abs(a - b) > .12);
    const W = (pts, h0) => { const P = pts.map(([u, v]) => M.islWorld(u, v)); return +(walkUp(P, h0) - y).toFixed(2); };
    const [lx, lz] = M.islWorld(52, 24), onto = W([[52, 24], [66, 24], [77, 24]], M.groundAt(lx, lz, 60, 80)), fun = W([[77, 24], [84, 24]], y), ledge = W([[90, 31.4], [95, 31.4]], y);
    const ppl = M.MARKS.filter(m => m.src === 'ISKATE'), nok = ppl.filter(m => !m.K), rg = ppl.find(m => m.id === 'is_rollergirl');
    const inl = M.islEdge(...M.islWorld((S.u0 + S.u1) / 2, (S.v0 + S.v1) / 2).slice(0, 2)) > 0;
    r = S.n + ' boxes, ' + S.tris + ' tris | deck ' + (y - M.ISLE.sea).toFixed(1) + ' over the sea | ' + got.map(([nm, a, b]) => nm + ' ' + a + '/' + b).join(', ') +
      ' | walked on from the island ' + onto + ', up the funbox ' + fun + ', up the ledge steps ' + ledge + ' | ' + ppl.map(m => m.p.name + ' (' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ')').join(', ');
    why = !inl ? 'THE PIER IS OFF THE ISLANDS' : off.length ? 'A SURFACE AT THE WRONG HEIGHT: ' + off.map(q => q[0]).join(', ') : Math.abs(onto) > .1 ? 'THE PIER CANNOT BE WALKED ONTO'
      : Math.abs(fun - .7) > .1 ? 'THE FUNBOX CANNOT BE RIDDEN UP' : Math.abs(ledge - .9) > .1 ? 'THE LEDGE STEPS ARE NOT STEPS' : ppl.length < 4 || nok.length ? 'A LOCAL WITH NO BODY' : !rg || !/rollerskate/.test(rg.K.file) ? 'NO ROLLERGIRL' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'SKATE', r, why); }
// ---- THE MESA'S EXIT POINT AND THE GAP RAMP (m391): the deck walked onto from the mesa's top and out to its end, the end
// over the drop and OPEN; the in-run ridden from its top to the lip with floor under every step, the lip a real kicker (its
// angle, its height over the ground), water between the lip and the beach it points at; the four locals real bodies, the
// BASE jumper's role a kind, Lou standing dry across the gap
{ const B = M.IBASE, I = M.ISLES; let r = 'NOT BUILT', why = '';
  if (B.deck && B.ramp) {
    const sea = M.ISLE.sea, D = B.deck, Rp = B.ramp, K = I.ISLANDS.find(q => q.id === 'mesa'), W = (u, v) => M.islWorld(u, v);
    const [mx, mz] = W(K.u, K.v), path = [[K.u, K.v], D.P(D.s0 - 2, 0), D.P(D.s1 - .4, 0)].map(([u, v]) => W(u, v));
    const walked = +(walkUp(path, M.groundAt(mx, mz, 60, 80)) - D.y).toFixed(2);
    const [ex, ez] = W(...D.P(D.s1 - .4, 0)), under = +(M.islHeight(...D.P(D.s1 - .4, 0)) - sea).toFixed(1);
    const [ox, oz] = W(...D.P(D.s1 + .4, 0)), past = M.groundAt(ox, oz, D.y + .5, 1), open = past < D.y - 5;
    const P0 = Rp.pts[0], PL = Rp.pts[Rp.pts.length - 1], P1 = Rp.pts[Rp.pts.length - 2];
    const drop = +(P0[1] - PL[1]).toFixed(1), lipA = +(Math.atan2(PL[1] - P1[1], PL[0] - P1[0]) * 180 / Math.PI).toFixed(1);
    const [lx, lz] = W(...Rp.R(PL[0] + .3, 0)), lipH = +(PL[1] - M.groundAt(lx, lz, PL[1] - .5, 0)).toFixed(1);
    const rideP = Rp.pts.map(([s]) => W(...Rp.R(s - (s === PL[0] ? .05 : 0), 0))), rode = +(walkUp(rideP, P0[1]) - PL[1]).toFixed(2);
    // each quad at its MIDDLE (its corners are shared with the next quad, so they cannot see one missing)
    const offPts = Rp.pts.slice(1).filter(([sB, yB], i) => { const [sA, yA] = Rp.pts[i], [x, z] = W(...Rp.R((sA + sB) / 2, .8)), yy = (yA + yB) / 2; return Math.abs(M.groundAt(x, z, yy + .05, .3) - yy) > .1; }).length;
    const ppl = M.MARKS.filter(m => m.src === 'IBASE'), nok = ppl.filter(m => !m.K), lou = ppl.find(m => m.id === 'is_lou'), sasha = ppl.find(m => m.id === 'is_sasha');
    const bj = M.rosterKind(M.ROSTER.find(q => q.id === 'basejumper'));
    r = 'exit point: ' + B.n + ' boxes, ' + B.tris + ' tris | deck ' + (D.y - sea).toFixed(1) + ' over the sea, ' + (D.s1 - D.dE).toFixed(1) + ' m past the edge, walked out from the mesa\'s middle ' + walked +
      ', the ground under its end ' + under + ', past its end ' + (open ? 'open' : 'NOT OPEN (' + past.toFixed(1) + ')') + ' | ramp: ' + Rp.pts.length + ' pts, a ' + drop + ' m drop over ' + PL[0].toFixed(1) + ' m, ridden top to lip ' + rode +
      ', lip ' + lipA + ' deg and ' + lipH + ' m over the ground, the gap ' + (Rp.gapTo ? (Rp.gapTo - PL[0]).toFixed(1) + ' m of water to the mesa\'s beach' : 'NO WATER') + ', ' + offPts + ' pts off the floor | ' +
      ppl.map(m => m.p.name + ' (' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ') ' + (m.y - sea).toFixed(1)).join(', ') + ' | basejumper -> ' + (bj ? bj.file.split('/').pop() : 'NO KIND');
    why = Math.abs(walked) > .05 ? 'THE EXIT POINT CANNOT BE WALKED OUT ONTO' : under > 2 ? 'ITS END IS NOT OVER THE DROP' : !open ? 'ITS END IS NOT OPEN' : !B.sock ? 'NO WINDSOCK'
      : drop < 8 ? 'THE IN-RUN DROPS ONLY ' + drop : Math.abs(rode) > .1 ? 'THE IN-RUN CANNOT BE RIDDEN TO THE LIP' : offPts ? 'THE RAMP IS NOT FLOOR' : Math.abs(lipA - B.lip) > 3 ? 'THE LIP IS NOT A KICKER' : lipH < .6 ? 'THE LIP IS ON THE GROUND'
      : !Rp.gapTo ? 'NO GAP UNDER THE RAMP' : ppl.length < 4 || nok.length || !bj ? 'A LOCAL WITH NO BODY' : !(lou.y > sea + .2) ? 'LOU IS IN THE SEA' : Math.abs(sasha.y - D.y) > .05 ? 'SASHA IS OFF THE DECK' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'BASE+RAMP', r, why); }
// ---- THE ISLANDS' PEOPLE WHO MOVE (m392): the shipped `isJump` driven through a whole cycle on a stand-in body (wait, run,
// leap, canopy, splash, swim, the beach, the ladder, back to the deck) -- the splash in the water, the climb topping out on
// the mesa, home on the deck; the shipped `isKite` for 40 s on each rider -- never off the water, and jumping
{ const J = M.IJUMP, U = M.IKITE, D = M.IBASE.deck; let r = 'NOT BUILT', why = '';
  if (J.on && D && U.list.length) {
    const sea = M.ISLE.sea, dt = 1 / 30, fake = (x, y, z) => { const d = { root: new M.THREE.Group(), K: { clips: { idle: 'idle', walk: 'walk', run: 'run' } }, actions: null, st: 'idle', h: 0, t: 0 }; d.root.position.set(x, y, z); return d; };
    const wet = (x, z) => M.islHeight(...M.islLocal(x, z)) < sea - .3;
    const keepP = M.player.pos.clone(), mk = M.MARKS.find(m => m.id === J.id), d = fake(mk.x, mk.y, mk.z), R = { d, st: 'wait', t: 1 }; d.ijR = R;
    M.player.pos.set(mk.x, mk.y, mk.z);
    const seq = [], tIn = {}; let T = 0, splash = null, topY = null, lowWalk = 1e9, err = '';
    for (let k = 0; k < 30 * 400; k++) {
      const was = R.st; d.t += dt; T += dt;
      try { M.isJump(d, dt, {}); } catch (e) { err = e.message; break; }
      tIn[was] = (tIn[was] || 0) + dt;
      if (R.st !== was) { seq.push(R.st); if (R.st === 'swim' && !splash) splash = [d.root.position.x, d.root.position.z]; if (was === 'climb') topY = d.root.position.y; }
      if (R.st === 'walk') lowWalk = Math.min(lowWalk, d.root.position.y - sea);
      if (seq.includes('climb') && R.st === 'wait' && T > 5 && Math.hypot(...(([x, z]) => [x - d.root.position.x, z - d.root.position.z])(M.islWorld(...D.P(D.s0 + 4.5, 0)))) < .2) break;
    }
    M.player.pos.copy(keepP);
    const home = R.st === 'wait' && Math.abs(d.root.position.y - D.y) < .05, inWater = splash && wet(...splash), topOk = topY != null && Math.abs(topY - sea - M.ISLES.ISLANDS.find(q => q.id === 'mesa').h) < 1.2;
    // the kites
    const kr = U.list.map(Rk => { const mk2 = M.MARKS.find(m => m.id === Rk.B.id), d2 = fake(mk2.x, mk2.y, mk2.z); d2.ikR = Rk; const keepK = Rk.kite; Rk.kite = Rk.kite || new M.THREE.Group(); const j0 = U.jumps;
      let dry = 0, top = 0, e2 = '', lap = 0, th0 = Rk.th; for (let k = 0; k < 30 * 40; k++) { d2.t += dt; try { M.isKite(d2, dt, {}); } catch (e) { e2 = e.message; break; } const p = d2.root.position; if (!wet(p.x, p.z)) dry++; top = Math.max(top, p.y - sea); }
      lap = Math.abs(Rk.th - th0) / (Math.PI * 2); const o = { name: Rk.B.name, dry, top: +top.toFixed(1), jumps: U.jumps - j0, laps: +lap.toFixed(1), err: e2 }; Rk.kite = keepK; Rk.th = th0; Rk.air = 0; Rk.y = sea + .05; return o; });
    const ppl = M.MARKS.filter(m => m.src === 'IKITE'), nok = ppl.filter(m => !m.K);
    r = 'Sasha: ' + seq.join(' > ') + ' in ' + T.toFixed(0) + ' s (' + Object.entries(tIn).map(([k, v]) => k + ' ' + v.toFixed(0)).join(', ') + ') | splash ' + (splash ? (inWater ? 'in the water' : 'NOT IN WATER') : 'NONE') +
      ', topped out ' + (topY != null ? (topY - sea).toFixed(1) : '-') + ' over the sea, lowest walk ' + lowWalk.toFixed(2) + ', home ' + (home ? 'on the deck' : 'NOT (' + R.st + ' ' + (d.root.position.y - D.y).toFixed(2) + ')') + (err ? ' THREW ' + err : '') +
      ' | kites: ' + kr.map(o => o.name + ' ' + o.laps + ' laps, ' + o.jumps + ' jumps to ' + o.top + ' m, ' + o.dry + ' frames dry' + (o.err ? ' THREW ' + o.err : '')).join('; ') + ' | ' + ppl.map(m => m.p.name + ' (' + (m.K ? m.K.file.split('/').pop() : 'NO KIND') + ')').join(', ');
    why = err ? 'THE JUMPER THREW' : !seq.includes('canopy') ? 'NO CANOPY' : !inWater ? 'SHE DOES NOT LAND IN THE WATER' : !seq.includes('climb') ? 'SHE NEVER GETS BACK TO THE LADDER' : !topOk ? 'THE CLIMB DOES NOT TOP OUT' : lowWalk < -.35 ? 'SHE WALKS UNDER THE GROUND' : !home ? 'SHE NEVER GETS HOME'
      : kr.some(o => o.err) ? 'A KITE THREW' : kr.some(o => o.dry) ? 'A KITE SURFER OFF THE WATER' : kr.some(o => !o.jumps || o.top < 1.5) ? 'A KITE SURFER NEVER JUMPS' : ppl.length < 2 || nok.length ? 'A KITE SURFER WITH NO BODY' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'MOVERS', r, why); }
// ---- HOLLOW CREEK'S LAND (m365): built, clear of every other land (its coast sampled against the farm's, the island's
// rectangle and The Pearl's), the gorge cut at least 5 m under its rims down its length and running out to the sea, the
// two flats level, and a forest standing on it
{ const F = M.HCREEK; let r = 'NOT BUILT', why = '';
  if (F.live) {
    const R = M.ISLE.rect, pr = (M.MAPREG.tkit || []).find(q => q.id === 'pearl'); let clash = [];
    for (let k = 0; k < 96; k++) { const t = k / 96 * Math.PI * 2; let lo = 0, hi = 1.6; for (let it = 0; it < 22; it++) { const m = (lo + hi) / 2; if (M.hcEdge(Math.cos(t) * F.A * m, Math.sin(t) * F.B * m) > 0) lo = m; else hi = m; }
      const [x, z] = M.hcWorld(Math.cos(t) * F.A * lo, Math.sin(t) * F.B * lo);
      if (M.FARMLAND.live && M.flEdgeAt(x, z) > -15) clash.push('the farm');
      if (x > R[0] - 40 && x < R[1] + 40 && z > R[2] - 40 && z < R[3] + 40) clash.push('the island');
      if (pr && x > pr.x0 - 30 && x < pr.x1 + 30 && z > pr.z0 - 30 && z < pr.z1 + 30) clash.push('the pearl'); }
    clash = [...new Set(clash)];
    // the gorge: rim (12 m out either side, the lower) over the bed, at its quarter points; the mouth at the sea
    const G = F.GORGE, P = G.pts, depth = [];
    for (const f of [.2, .4, .6, .8]) { const s = f * F.gbed.len; let acc = 0;
      for (let i = 0; i < P.length - 1; i++) { const L = Math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]); if (acc + L >= s) { const t = (s - acc) / L, a = P[i][0] + (P[i + 1][0] - P[i][0]) * t, b = P[i][1] + (P[i + 1][1] - P[i][1]) * t, ux = (P[i + 1][0] - P[i][0]) / L, uz = (P[i + 1][1] - P[i][1]) / L;
        const bed = M.hcHeight(a, b), rim = Math.min(M.hcHeight(a + uz * 12, b - ux * 12), M.hcHeight(a - uz * 12, b + ux * 12)); depth.push(+(rim - bed).toFixed(1)); break; } acc += L; } }
    const mouth = M.hcHeight(...P[P.length - 1]) - M.ISLE.sea;
    const flats = F.FLATS.map(Fl => { let lo = 1e9, hi = -1e9; for (let k = 0; k < 16; k++) { const t = k / 16 * Math.PI * 2, y = M.hcHeight(Fl.a + Math.cos(t) * Fl.r * .45, Fl.b + Math.sin(t) * Fl.r * .45); lo = Math.min(lo, y); hi = Math.max(hi, y); } return +(hi - lo).toFixed(2); });
    const hill = M.hcHeight(F.HILLS[0].a, F.HILLS[0].b) - M.ISLE.sea;
    r = F.chunks + ' chunks, ' + F.tris + ' floor tris, ' + F.trees + ' trees | centre ' + F.O.map(v => v.toFixed(0)).join(',') + ' | clear of ' + (clash.length ? 'NOT ' + clash.join(', ') : 'the farm, the island, the pearl') +
      ' | gorge depth ' + depth.join(', ') + ' m, mouth ' + mouth.toFixed(2) + ' over the sea | flats level to ' + flats.join(', ') + ' | hill ' + hill.toFixed(1) + ' m';
    why = clash.length ? 'IT LANDS ON ' + clash.join(', ').toUpperCase() : depth.some(d => d < 5) ? 'A GORGE NOT 5 M DEEP' : mouth > 1 ? 'THE CREEK NEVER REACHES THE SEA' : flats.some(f => f > .4) ? 'A FLAT THAT IS NOT' : F.trees < 300 ? 'NO FOREST' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'HOLLOW', r, why); }
// ---- THE TRAILER PARK (m366): the walk is floor its whole length, every porch and platform is floor at its height from
// the walk, each ramp is floor from the walk up onto the rim, and the ladder stands on the creek's bed and tops out on the walk
{ const T = M.HCTRAIL; let r = 'NOT BUILT', why = '';
  if (T.frame) { const { Ox, Oz, th, cU, Y } = T.frame, C = Math.cos(th), S = Math.sin(th), W = (u, v) => [Ox + u * C + v * S, Oz - u * S + v * C];
    const fl = (u, v, y) => { const [x, z] = W(u, v); return M.groundAt(x, z, y + .3, .5); };
    let walkOff = 0; for (let v = -T.half + 1; v < T.half - 1; v += 1.7) if (Math.abs(fl(cU(v), v, Y) - Y) > .1) walkOff++;
    const homes = T.homes.map(h => { const g = fl(h.u - h.side * 1.2, h.v, h.y), pg = fl(cU(h.v - h.len * .1) + h.side * 2.5, h.v - h.len * .1, Math.max(Y, h.y));
      return Math.abs(g - h.y) > .1 ? 'NO PLATFORM' : Math.abs(pg - Math.max(Y, h.y)) > .1 ? 'NO PORCH' : 'ok'; });
    const ramps = (T.ramps || []).map(K => { let off = 0; for (let k = 0; k < 10; k++) { const P = K.pt((k + .37) / 10), [x, z] = W(P[0], P[2]); if (Math.abs(M.groundAt(x, z, P[1] + .3, .5) - P[1]) > .15) off++; }
      return (K.B[1] - Y).toFixed(1) + ' m up' + (off ? ' ' + off + ' OFF' : ''); });
    const L = T.lad, foot = L && M.groundAt(L.cx + L.fg.x * .7, L.cz + L.fg.z * .7, L.miny + .3, .5), top = L && M.groundAt(L.mark.x, L.mark.z, L.mark.y + .3, .5);
    const lad = !L ? 'NONE' : Math.abs(foot - L.miny) > .15 ? 'NO FOOT' : Math.abs(top - Y) > .12 ? 'NO TOP' : (Y - L.miny).toFixed(1) + ' m';
    const ppl = M.MARKS.filter(m => m.src === 'HCTRAIL'), nok = ppl.filter(m => !m.K);
    r = T.n + ' boxes | walk at ' + (Y - M.ISLE.sea).toFixed(1) + ' m over the sea, ' + (walkOff ? walkOff + ' HOLES' : 'floor all along') + ' | homes ' + homes.join(', ') + ' | ramps ' + ramps.join(', ') + ' | ladder ' + lad + ' | ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ');
    why = walkOff ? 'A HOLE IN THE WALK' : homes.some(h => h !== 'ok') ? 'A HOME YOU CANNOT GET TO' : ramps.length < 2 || ramps.some(t => /OFF/.test(t)) ? 'A RAMP WITH A HOLE' : /NO|NONE/.test(lad) ? 'THE LADDER GOES NOWHERE' : nok.length ? 'SOMEBODY WITH NO KIND' : ppl.length < 4 ? 'NOBODY HOME' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'TRAILERS', r, why); }
// ---- THE RACE (m375): lined up at the gate on a bike it counts down and goes; a rider who takes the loop at 21 m/s
// through every checkpoint WINS (`gang:respect`), one who sits at the gate LOSES to Rae; and cutting across does not count
{ const R = M.HCRACE, S = M.HCBIKE.startAt; let r = 'NOT BUILT', why = '';
  if (S) { const p = M.player, F = M.SAVE.flags, was = F['gang:respect'];
    const run = (mode) => { delete F['gang:respect']; R.st = 'idle'; R.cool = 0; p.board = 1; p.bike = 1; p.vel.set(0, 0, 0); p.pos.set(S[0], S[1], S[2]);
      let s = 0, f = 0, seen = []; for (; f < 2400; f++) { const st0 = R.st;
        if (R.st === 'race' && mode !== 'sit') { s += 21 * .1; const A = mode === 'cut' ? M.raceAt(f % 40 < 20 ? 0 : R.len * .5) : M.raceAt(s); p.pos.set(A.x, A.y, A.z); p.vel.set(21, 0, 0); }
        else if (R.st === 'count') p.vel.set(0, 0, 0);
        M.raceStep(.1); if (R.st !== st0) seen.push(R.st); if (seen.length && R.st === 'idle' && st0 === 'race') break; }
      return { won: !!F['gang:respect'], t: (f * .1).toFixed(0), seen: seen.join('>'), lap: R.lap, sR: R.sR.toFixed(0) }; };
    const A = run('ride'), B = run('sit'), C = run('cut');
    p.board = 0; p.bike = 0; if (was) F['gang:respect'] = was; else delete F['gang:respect'];
    r = 'loop ' + R.len.toFixed(0) + ' m x ' + R.laps + ' laps, ' + R.cps + ' checkpoints | riding it: ' + (A.won ? 'WON' : 'lost') + ' in ' + A.t + ' s (' + A.seen + ') | sitting at the gate: ' + (B.won ? 'WON' : 'lost') + ' (Rae ' + B.sR + ' m) | cutting start-to-halfway across the middle: ' + (C.won ? 'WON' : 'lost');
    why = !A.won ? 'A GOOD RIDE DOES NOT WIN' : B.won ? 'SITTING STILL WINS' : C.won ? 'CUTTING ACROSS WINS' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'RACE', r, why); }
// ---- THE BIKE (m374): the biker is a hero kind that rides, every Hollow Creek biker IS him (so his sample is the ride),
// the bike's numbers sit over the board's, and with no bike loaded (this harness: draco) nothing claims he is on one
{ const ms = M.MARKS.filter(m => m.p && /biker/.test(m.p.kind || '') && /^hc_/.test(m.id)), notHim = ms.filter(m => m.K !== M.BIKER);
  const r = 'mode ' + M.BIKER.mode + ' | ' + ms.length + ' Hollow Creek bikers, ' + (ms.length - notHim.length) + ' of them the riding biker | top ' + M.BIKE.top + ' (board ' + M.SK8.top + '), acc ' + M.BIKE.acc + ', ollie ' + M.BIKE.ollie + ', the rest the board\'s (trick fill ' + M.BIKE.trick.fill + ') | bike loaded ' + !!M.PBIKE.up + ', riding ' + M.bikeOn();
  const why = M.BIKER.mode !== 'bike' ? 'THE BIKER DOES NOT RIDE' : notHim.length ? 'A BIKER WHO IS NOT HIM: ' + notHim.map(m => m.name).join(', ') : !(M.BIKE.top > M.SK8.top) || !M.BIKE.trick ? 'THE BIKE IS NOT OVER THE BOARD' : M.bikeOn() ? 'RIDING A BIKE THAT IS NOT THERE' : '';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'BIKE', r, why); }
// ---- THE RALLY (m372): its people have kinds and their homes and spots are floor, and a whole rally runs -- the trucks up
// the road and into their slots ON THE GROUND, the speech, the brawl, the trucks gone again, quiet
{ const O = M.HCRALLY; let r = 'NOT BUILT', why = '';
  if (O.trucks) {
    const ppl = M.MARKS.filter(m => m.src === 'HCRALLY'), nok = ppl.filter(m => !m.K);
    const spots = [...O.GOERS.map(G => G.spot), ...O.PEARL.map(P => P.spot)].filter(([x, z]) => Math.abs(M.groundAt(x, z, O.y + 1, .5) - O.y) > .3).length;
    M.rallyStart(); const seen = [O.st]; let parked = 0, maxPark = 0;
    for (let f = 0; f < 3000 && !(O.st === 'quiet' && seen.length > 1); f++) { M.rallyStep(.1); if (O.st !== seen[seen.length - 1]) seen.push(O.st); parked = O.trucks.filter(T => T.st === 'park').length; maxPark = Math.max(maxPark, parked); }
    const slots = O.trucks.map(T => { const [x, z] = T.slot; return +(M.groundAt(x, z, O.y + 3, .6) - O.y).toFixed(2); });
    for (let f = 0; f < 600 && !O.trucks.every(T => T.st === 'gone'); f++) M.rallyStep(.1);          // they are still driving off when it goes quiet
    const gone = O.trucks.every(T => T.st === 'gone' && !T.g.visible && T.box._off);
    let stage = false, over = '';                                              // m376: the stage is noticed in the speech, the boss ends it all
    { const F = M.SAVE.flags, p = M.player, [x, z] = O.W(...O.LEADER.at), was = F['rally:stage']; delete F['rally:stage'];
      O.st = 'speech'; O.t = 30; O.tick = 0; p.pos.set(x + 1, O.y + M.HCFAIR.STAGE.h, z); M.rallyStep(.6); stage = !!F['rally:stage'];
      F['qdone:ch3c'] = 1; O.st = 'quiet'; O.t = 5; O.tick = 0; M.rallyStep(.6); over = (O.t > 1e8 ? 'no more rallies' : 'STILL RALLYING') + ', ' + (M.HCROAD.gate && M.HCROAD.gate.open ? 'the road open' : 'THE ROAD SHUT');
      delete F['qdone:ch3c']; if (was) F['rally:stage'] = was; else delete F['rally:stage']; O.over = 0; O.st = 'quiet'; O.t = 60; if (M.HCROAD.gate) M.HCROAD.gate.open = 0; }
    r = ppl.length + ' people (' + ppl.filter(m => m.p.role === 'rallyboss').length + ' rally man) | spots off the floor ' + spots + ' | ' + seen.join(' > ') + ' | trucks parked ' + maxPark + '/' + O.trucks.length + ' (slots ' + slots.join(', ') + ' over the fair), gone after ' + gone + ' | on the stage in the speech: ' + (stage ? 'noticed' : 'NOT NOTICED') + ' | after the boss: ' + over;
    why = nok.length ? 'SOMEBODY WITH NO KIND' : spots ? 'A SPOT NOT ON THE FIELD' : seen.join(' > ') !== 'build > speech > brawl > disperse > quiet' ? 'THE RALLY NEVER RAN ITS COURSE' : maxPark < O.trucks.length ? 'A TRUCK NEVER ARRIVED' : !gone ? 'THE TRUCKS NEVER LEFT' : slots.some(h => Math.abs(h) > 1.2) ? 'A TRUCK SLOT OFF THE GROUND' : !stage ? 'THE STAGE IS NOT NOTICED' : /STILL|SHUT/.test(over) ? 'THE BOSS CHANGES NOTHING' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'RALLY', r, why); }
// ---- THE HIGHWAY (m371): WALKED from Old Town's grass over the arch to the gang, the gang's gate turns the alien round
// and lets anybody LEAVE Hollow Creek by it, the road on up the land is on its mesh with no tree on it, and the gang
{ const O = M.HCROAD; let r = 'NOT BUILT', why = '';
  if (O.frame && O.gate) { const { A, th, L, yv } = O.frame, C = Math.cos(th), S = Math.sin(th), W = (u, v) => [A[0] + u * C + v * S, A[1] - u * S + v * C], gv = L - O.gateBack;
    const w0 = W(0, .5), up = walkUp([w0, W(0, gv - 1)], M.groundAt(w0[0], w0[1], 30, 0)), want = yv(gv - 1);
    const p = M.player, G = O.gate, at = v => { const [x, z] = W(0, v); p.pos.set(x, yv(v) + .02, z); };
    at(gv - .8); M.gatePush(.016); at(gv + .1); M.gatePush(.016); const [bx2, bz2] = [p.pos.x - A[0], p.pos.z - A[1]], vBack = bx2 * S + bz2 * C;
    at(gv + 1); M.gatePush(.016); at(gv - .1); M.gatePush(.016); const [ex, ez] = [p.pos.x - A[0], p.pos.z - A[1]], vOut = ex * S + ez * C;
    const turned = vBack < gv - .3, leaves = Math.abs(vOut - (gv - .1)) < .05;
    let trees = 0; for (const q of O.roadPts) { const [x, z] = M.hcWorld(q[0], q[1]); trees += M.BOXES.filter(b => b.farm === 'creek' && b.maxx - b.minx < .7 && Math.hypot((b.minx + b.maxx) / 2 - x, (b.minz + b.maxz) / 2 - z) < O.w / 2 + .5).length; }
    const ppl = M.MARKS.filter(m => m.src === 'HCROAD'), nok = ppl.filter(m => !m.K);
    r = 'bridge ' + L.toFixed(0) + ' m, arch ' + O.arch + ' m, at ' + O.deg.toFixed(0) + ' deg | walked from the grass to the gang: ' + (up - M.ISLE.sea).toFixed(2) + ' (of ' + (want - M.ISLE.sea).toFixed(2) + ') | gate: the alien ' + (turned ? 'turned round' : 'GOT THROUGH') + ', out of the creek ' + (leaves ? 'free' : 'BLOCKED') + ' | road ' + O.roadPts.length + ' pts, trees on it ' + trees + ' | ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ');
    why = Math.abs(up - want) > .1 ? 'A BRIDGE YOU CANNOT WALK' : !turned ? 'THE GANG LETS ANYBODY IN' : !leaves ? 'YOU CANNOT LEAVE' : trees ? 'TREES ON THE ROAD' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'HIGHWAY', r, why); }
// ---- THE FREIGHT LINE (m370): the line over the highest ground under it, the platforms level with the cars' decks, both
// stairs WALKED, the train runs out to Hollow Creek and back, and a man standing on the flatcar's open deck is CARRIED --
// the floor under him the car's (BDYN), and his distance moved the car's
{ const T = M.HCTRAIN; let r = 'NOT BUILT', why = '';
  if (T.cars) {
    const stairs = T.plats.map(Pl => +(walkUp([Pl.foot, Pl.top], M.groundAt(Pl.foot[0], Pl.foot[1], 200, 0)) - T.deck).toFixed(2));
    // the ride: on the flatcar's open deck, parked at Old Town, then it runs
    const flat = T.cars.find(C => C.def.id === 'flat'), deckB = flat.boxes[0], ub = T.dir;
    const pz = flat.def.len / 2 - 1.5, px0 = deckB.cx + ub[0] * pz, pz0 = deckB.cz + ub[1] * pz, p = M.player;
    p.pos.set(px0, deckB.maxy, pz0); p.grounded = true; p.vel.set(0, 0, 0);
    const floor0 = M.groundAt(p.pos.x, p.pos.z, p.pos.y + .1, M.MOVE.step), sStart = T.s;
    T.st = 'wait'; T.t = 0; T.at = 0; let seen = [];
    for (let f = 0; f < 400 && T.at === 0; f++) { M.trainStep(.1); p.pos.y = deckB.maxy; p.grounded = true; if (!seen.includes(T.st)) seen.push(T.st); }
    const moved = Math.hypot(p.pos.x - px0, p.pos.z - pz0), carMoved = T.s - sStart, onIt = !!M.trainUnder(p.pos);
    // and back
    T.t = 0; let back = 0; for (let f = 0; f < 400 && T.at === 1; f++) { M.trainStep(.1); back = 1; }
    const home = T.at === 0;
    r = 'line ' + T.len.toFixed(0) + ' m at ' + (T.yr - M.ISLE.sea).toFixed(1) + ' m over the sea, decks at ' + (T.deck - M.ISLE.sea).toFixed(1) + ' | stairs walked up to the deck ' + stairs.join(', ') + ' (steps ' + T.plats.map(P => P.steps).join(', ') + ')' +
      ' | floor on the flatcar ' + (floor0 - deckB.maxy).toFixed(2) + ' | out: the car ' + carMoved.toFixed(1) + ' m, him ' + moved.toFixed(1) + ' m, still on it ' + onIt + ' | back ' + (home ? 'home' : 'NOT HOME') + ' | ' + T.trips + ' trips';
    why = stairs.some(h => Math.abs(h) > .05) ? 'A PLATFORM YOU CANNOT WALK UP TO' : Math.abs(floor0 - deckB.maxy) > .05 ? 'THE FLATCAR IS NOT A FLOOR' : carMoved < T.len * .5 ? 'THE TRAIN NEVER LEFT'
      : Math.abs(moved - carMoved) > .2 || !onIt ? 'IT DID NOT CARRY HIM' : !home ? 'THE TRAIN NEVER CAME BACK' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'FREIGHT', r, why); }
// ---- THE BIKE TRACK (m369): its ribbon lies on the floor all the way round, no tree stands on it, every tabletop and the
// start hill are WALKED up to their tops, the tower's ladder works, and the bikers
{ const O = M.HCBIKE; let r = 'NOT BUILT', why = '';
  if (O.frame) {
    const LP = M.bikeLoop(), pts = LP.pts; let off = 0, worst = 0;
    // (away from what is BUILT on it -- a tabletop or the start hill is a floor over the ribbon on purpose)
    const built = [...O.tables.map(T => T.at), O.startAt];
    for (let i = 0; i < pts.length; i += 3) { const p = pts[i], [x, z] = M.hcWorld(p[0], p[1]); if (built.some(B => Math.hypot(B[0] - x, B[2] - z) < 12)) continue;
      const g = M.groundAt(x, z, 200, 0), e = Math.abs(g - M.HCREEK.meshH(p[0], p[1])); worst = Math.max(worst, e); if (e > .35) off++; }
    const trees = M.BOXES.filter(b => b.farm === 'creek' && b.maxx - b.minx < .7 && b.maxz - b.minz < .7 && pts.some(p => { const [x, z] = M.hcWorld(p[0], p[1]); return Math.hypot((b.minx + b.maxx) / 2 - x, (b.minz + b.maxz) / 2 - z) < O.w / 2 + .5; })).length;
    const W = ([u, v]) => { const { Ox, Oz, th } = O.frame, C = Math.cos(th), S = Math.sin(th); return [Ox + u * C + v * S, Oz - u * S + v * C]; };
    // walked from the floor where the walk STARTS (the land is not level along a track)
    const y0 = ([x, z]) => M.groundAt(x, z, 200, 0), tUp = T => walkUp([W(T.from), W(T.to)], y0(W(T.from))) - T.g0;
    const tabs = O.tables.map(T => +tUp(T).toFixed(2) + '/' + T.ht);
    const start = +(walkUp(O.startWalk, y0(O.startWalk[0])) - O.startY[0]).toFixed(2), startWant = +(O.startY[1] - O.startY[0]).toFixed(2);
    const L = O.lad, foot = L && M.groundAt(L.cx + L.fg.x * .7, L.cz + L.fg.z * .7, L.miny + .3, .5), top = L && M.groundAt(L.mark.x, L.mark.z, L.mark.y + .3, .5);
    const lad = !L ? 'NONE' : Math.abs(foot - L.miny) > .2 ? 'NO FOOT (' + (foot - L.miny).toFixed(2) + ')' : Math.abs(top - (L.mark.y - .02)) > .15 ? 'NO TOP' : (L.top - L.miny).toFixed(1) + ' m';
    const ppl = M.MARKS.filter(m => m.src === 'HCBIKE'), nok = ppl.filter(m => !m.K);
    r = O.n + ' boxes | loop ' + O.len.toFixed(0) + ' m, ' + O.berms + ' berm pieces | ribbon off the floor at ' + off + ' of ' + Math.ceil(pts.length / 3) + ' (worst ' + worst.toFixed(2) + ') | trees on it ' + trees + ' | tabletops walked up ' + tabs.join(', ') + ' | start hill ' + start + ' (of ' + startWant + ') | tower ladder ' + lad + ' | ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ');
    why = off ? 'THE TRACK FLOATS OR SINKS' : trees ? 'TREES ON THE TRACK' : O.tables.some(T => Math.abs(tUp(T) - T.ht) > .12) ? 'A TABLETOP YOU CANNOT RIDE UP' : Math.abs(start - startWant) > .05 ? 'A START HILL YOU CANNOT WALK UP'
      : /NO/.test(lad) ? 'THE TOWER LADDER GOES NOWHERE' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'BIKES', r, why); }
// ---- THE FAIRGROUND (m368): the stage walked up both sets of steps, the grandstand walked up to its top row, the truss's
// ladder from the ground to its catwalk, the Ferris wheel turning, and the people
{ const O = M.HCFAIR; let r = 'NOT BUILT', why = '';
  if (O.frame) { const { cx, cz, th, y } = O.frame, C = Math.cos(th), S = Math.sin(th), W = (u, v) => [cx + u * C + v * S, cz - u * S + v * C], St = O.STAGE;
    const stage = [-1, 1].map(s => +(walkUp([W(s * (St.w / 2 - 1), St.v + St.d / 2 + 3.2), W(s * (St.w / 2 - 1), St.v)], y) - y).toFixed(2));
    const T = O.standTop, stand = +(walkUp([W(16, T[2]), W(T[0], T[2])], y) - y).toFixed(2), standWant = +(T[1] - y).toFixed(2);
    const L = O.lad, foot = L && M.groundAt(L.cx + L.fg.x * .7, L.cz + L.fg.z * .7, L.miny + .3, .5), top = L && M.groundAt(L.mark.x, L.mark.z, L.mark.y + .3, .5);
    const lad = !L ? 'NONE' : Math.abs(foot - L.miny) > .15 ? 'NO FOOT' : Math.abs(top - (L.mark.y - .02)) > .15 ? 'NO TOP' : (L.top - L.miny).toFixed(1) + ' m';
    const a0 = O.wheel ? O.wheel.rotation.z : 0; M.fairStep(1); const turns = O.wheel && O.wheel.rotation.z !== a0;
    const ppl = M.MARKS.filter(m => m.src === 'HCFAIR'), nok = ppl.filter(m => !m.K);
    r = O.n + ' boxes | stage walked up to ' + stage.join(', ') + ' (of ' + St.h + ') | grandstand ' + stand + ' (of ' + standWant + ') | truss ladder ' + lad + ' | wheel ' + (turns ? 'turns' : 'STILL') + ' | ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ');
    why = stage.some(h => Math.abs(h - St.h) > .05) || Math.abs(stand - standWant) > .05 ? 'STEPS YOU CANNOT WALK UP' : /NO/.test(lad) ? 'THE TRUSS LADDER GOES NOWHERE' : !turns ? 'THE WHEEL DOES NOT TURN' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'FAIR', r, why); }
// ---- THE MILL (m367): the upper floor and the stair up to it are floor, both conveyors and the flume are floor all along
// (the flume ends OUT OVER the gorge, the creek well below its end), the piles' tops are floors, the crane's ladder works
{ const O = M.HCMILL; let r = 'NOT BUILT', why = '';
  if (O.frame) { const { cx, cz, th, y, my } = O.frame, C = Math.cos(th), S = Math.sin(th), W = (u, v) => [cx + u * C + v * S, cz - u * S + v * C];
    const fl = (u, v, h) => { const [x, z] = W(u, v); return M.groundAt(x, z, h + .3, .5); };
    const mez = Math.abs(fl(-4, -12, my) - my) < .1, stairTop = Math.abs(walkUp([W(10, -1.25), W(10, -7.6)], y) - my) < .05;   // m368: WALKED, at his step
    const span = K => { let off = 0; for (let k = 0; k < 10; k++) { const P = K.pt((k + .37) / 10); if (Math.abs(fl(P[0], P[2], P[1]) - P[1]) > .15) off++; } return off; };
    const b1 = span(O.belt1) + (Math.abs(walkUp([W(O.belt1.A[0], O.belt1.A[2] + 2), W(O.belt1.B[0], O.belt1.B[2] - .3)], y) - my) > .05 ? 100 : 0), b2 = span(O.belt2);
    let fOff = 0; const fp = O.flumePts; for (let i = 0; i < fp.length - 1; i++) { const P = fp[i], Q = fp[i + 1], u = (P[0] + Q[0]) / 2, v = P[2] * .63 + Q[2] * .37, h = P[1] * .63 + Q[1] * .37; if (Math.abs(fl(u, v, h) - h) > .15) fOff++; }
    const E = fp[fp.length - 1], [ex, ez] = W(E[0], E[2] + 1), below = E[1] - M.hcHeight(...M.hcLocal(ex, ez));
    const piles = O.PILES.map(P => +(fl(P.u, P.v, P.top) - P.top).toFixed(2));
    const L = O.lad, foot = L && M.groundAt(L.cx + L.fg.x * .7, L.cz + L.fg.z * .7, L.miny + .3, .5), top = L && M.groundAt(L.mark.x, L.mark.z, L.mark.y + .3, .5);
    const lad = !L ? 'NONE' : Math.abs(foot - L.miny) > .15 ? 'NO FOOT' : Math.abs(top - (L.mark.y - .02)) > .15 ? 'NO TOP' : 'ok';
    const ppl = M.MARKS.filter(m => m.src === 'HCMILL'), nok = ppl.filter(m => !m.K);
    r = O.n + ' boxes | upper floor ' + (mez ? 'ok' : 'NONE') + ', stair ' + (stairTop ? 'ok' : 'SHORT') + ' | belts ' + (b1 ? b1 + ' OFF' : 'ok') + ', ' + (b2 ? b2 + ' OFF' : 'ok') + ' | flume ' + fp.length + ' pts ' + (fOff ? fOff + ' OFF' : 'floor all along') + ', ends ' + below.toFixed(1) + ' m over the gorge' +
      ' | piles ' + piles.join(', ') + ' | crane ladder ' + lad + ' | ' + ppl.map(m => m.name + (m.K ? '' : ' NO KIND')).join(', ');
    why = !mez || !stairTop ? 'NO WAY UPSTAIRS' : b1 || b2 ? 'A CONVEYOR WITH A HOLE' : fOff ? 'A FLUME WITH A HOLE' : below < 5 ? 'THE FLUME DOES NOT REACH THE GORGE' : piles.some(d => Math.abs(d) > .12) ? 'A PILE YOU CANNOT STAND ON' : lad !== 'ok' ? 'THE CRANE LADDER GOES NOWHERE' : nok.length ? 'SOMEBODY WITH NO KIND' : '';
  } else why = 'NOT BUILT';
  if (why) bad++;
  quiet((why ? 'BAD ' : 'ok  ') + 'MILL', r, why); }
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
    // m364: the call -- Marisol has the receipts: the organiser to the stage (on its floor), the march held; then done: the doors open
    let call = '';
    { const F = M.SAVE.flags, m = M.MARKS.find(q => q.id === 'pearl_organiser'), y0 = m && m.y;
      F['talk:ch2_receipts'] = 1; O.st = 'sit'; O.t = 0; for (let f = 0; f < 12; f++) M.plazaStep(.1);
      const g = m && M.groundAt(m.x, m.z, m.y + .3, .5), onStage = m && Math.abs(g - (y + O.STAGE.h)) < .1 && Math.abs(m.y - (y + O.STAGE.h)) < .1;
      const held = O.hold && O.st === 'sit';
      F['qdone:ch2c'] = 1; O.called = 0; for (let f = 0; f < 6; f++) M.plazaStep(.1);
      const open = O.gates.every(G => G.open);
      call = (onStage ? 'organiser on the stage' : 'ORGANISER NOT ON THE STAGE (' + (m ? (g - y).toFixed(2) + ' from ' + (y0 - y).toFixed(1) : 'no mark') + ')') + ', ' + (held ? 'march held' : 'MARCH NOT HELD') + ', ' + (open ? 'doors open after' : 'DOORS STILL SHUT AFTER');
      delete F['talk:ch2_receipts']; delete F['qdone:ch2c']; for (const G of O.gates) G.open = 0; O.opened = 0; O.called = 0; O.hold = 0; }
    const ppl = M.MARKS.filter(m => m.src === 'PLAZA'), nok = ppl.filter(m => !m.K);
    r = O.gates.length + ' barricades, flood ' + n + ' cells' + (leak.length ? ' LEAKS TO ' + leak.map(l => l[2]).join(', ') : ', sealed') + ' | doors ' + doors.join(', ') + ' | routes ' + routes.join(', ') + ' | march ' + walk + ' | ' + ppl.length + ' people | call: ' + call;
    why = O.gates.length !== O.BARS.length ? 'A BARRICADE WITH NO GATE' : leak.length ? 'A WAY ROUND THE BARRICADES' : n < 300 ? 'THE FLOOD NEVER LEFT THE STAGE' : doors.some(d => /SHUT/.test(d)) ? 'A DOOR THAT IS SHUT'
      : routes.some(t => /BLOCKED/.test(t)) ? 'A ROUTE THROUGH SOMETHING' : walk !== 'form > out > hold > back > sit' ? 'THE MARCH NEVER CAME BACK' : nok.length ? 'SOMEBODY WITH NO KIND' : /[A-Z]{4,} [A-Z]/.test(call) ? 'THE CALL: ' + call : '';
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
