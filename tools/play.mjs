// THE HEADLESS PLAYTHROUGH (m429, ROADMAP F0b-1; m430 Chapter 1). `npm run play [ch0 ch1 ...] [--draw] [--fps=30] [--budget=120]`
// With no chapters named it plays every chapter the drivers cover (`DRIVEN`), in order, on one save.
//
// Boots the SHIPPED `index.html` in headless Chromium (SwiftShader) through the real loader, in the real world (`tkit`) on a
// FRESH save -- so the game begins where a new game begins, at the crash -- and drives a chapter's quest to its end through
// the shipped machinery, one quest step at a time:
//   the loop      `frameBody()` stepped by hand on a fake clock (`performance.now` is ours; rAF never fires under
//                 SwiftShader, NOTES m416), 1/fps s a frame, `renderer.render` a no-op unless `--draw` (the raster is 100x
//                 too slow here and the picture is not what a playthrough tests; every other system in the frame runs as shipped)
//   walking       the LEFT STICK (`stick.L.x/y`, the object the pads write), mapped from a world direction by the inverse of
//                 the shipped `stickWorld`, so he walks the collider, the river's rule, the gates and the crowd like a thumb would
//   a strike      the shipped `dummyBlow(body, heading, power 1, dmg null)` -- what `strikeSweep` calls when a limb reaches a
//                 body -- from within arm's reach, so the knock-down is the shipped decision (`hp`, `K.hard`)
//   the sample    the RIGHT STICK held still over the downed body (`sampleStep` reads `stick.R`), for the shipped `SAMPLE.hold`
//   a talk        the shipped `talkTap()` within reach
//   a gate        walked through from the side he is on to the other; the flag is the shipped `gateStep`'s, and a gate that
//                 pushes him back fails the step (a teleport lands OUTSIDE the span and sets no flag -- it cannot cheat a gate)
//   the step      the shipped `questTest`, read off `quest.step` advancing; `quest.tgt` is where the shipped beam points
// `godTo` (the shipped GOD teleport, `mel.go` for a place) is used ONLY when a walk has made no progress for `STUCK` seconds,
// and the row says so -- a place that cannot be walked to is a finding, not a failure. One row per step: ok / BAD, what it
// was, game seconds, metres walked, teleports. Exit 1 on any BAD step, any uncaught frame error, or a chapter that did not
// end (`qdone:<id>` in the save). Run it before any build that touches a quest, a gate or a chapter (ROADMAP F0b).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const req = createRequire(import.meta.url);
let pw = null; for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright', '/usr/lib/node_modules/playwright']) { try { pw = req(p); break; } catch (e) {} }
if (!pw) { console.error('play: playwright is not installed (npm i -D playwright, Chromium is pre-installed at /opt/pw-browsers)'); process.exit(2); }
const ROOT = process.cwd();
const ARGS = process.argv.slice(2), opt = k => (ARGS.find(a => a.startsWith('--' + k + '=')) || '').split('=')[1];
const DRAW = ARGS.includes('--draw'), FPS = +(opt('fps') || 30), BUDGET = +(opt('budget') || 120), STUCK = 4, SEED = +(opt('seed') || 1);
const DRIVEN = ['ch0', 'ch1', 'ch2'];   // the chapters the drivers cover so far (F0b-2 adds one per build)
const CHAPTERS = ARGS.filter(a => !a.startsWith('--')); if (!CHAPTERS.length) CHAPTERS.push(...DRIVEN);

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.wasm': 'application/wasm', '.glb': 'model/gltf-binary',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ktx2': 'image/ktx2', '.mp3': 'audio/mpeg', '.webmanifest': 'application/manifest+json' };
const server = http.createServer((q, r) => {
  const u = decodeURIComponent(new URL(q.url, 'http://x').pathname), f = path.join(ROOT, u === '/' ? 'index.html' : u);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end(); return; }
  let body = fs.readFileSync(f);
  if (f.endsWith('index.html')) {
    // THE SHIPPED TEXT, with one handle spliced in beside the game's own: the things the driver reads and writes
    const s = body.toString(), k = 'window.melee = window.mel = {';
    if (!s.includes(k)) { console.error('play: no mel handle in index.html'); process.exit(1); }
    body = s.replace(k, 'window.__play = { frameBody, player, cam, stick, quest, QUESTS, SAVE, DUMMIES, dummyBlow, godTo, GATES, ISLE, mphName, talkTap, renderer, rig, GODPLACES, MISSING, SAMPLE, MOVE, CRASH, progFlag, GATE_TYPES, melPower, MELEE, FOE, mphFold, socialMe, socialOk, formPick, formNow, progForm, HCRACE, raceAt, HCBIKE, FVEH, inTK, RBK, FBK, OFERRY, socialGroup, socialOf, ROLEFORM, OORB, kitPick, WEAP, slotNow, IXING, islWorld, wingTapR, rosterOf, mphFold, IBASE, islLocal, boardMount, groundAt, boardGrade, SK8, talk, TALK, boardStepOff, ISHIP, formNow }; ' + k);
  }
  r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(body);
});
await new Promise(ok => server.listen(0, ok));
const port = server.address().port, t0 = Date.now(), el = () => ((Date.now() - t0) / 1000).toFixed(0) + 's';

const browser = await pw.chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 640, height: 360 }, deviceScaleFactor: 1 });
// `Math.random` is a seeded PRNG (mulberry32) from before the page boots, so a run with the same seed is the same run and a
// row that differs between builds is the build's doing; `--seed=N` for another
await page.addInitScript(seed => { let a = seed >>> 0; Math.random = () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }, SEED);
const errs = []; page.on('pageerror', e => errs.push(e.message.split('\n')[0]));
page.on('console', m => { const t = m.text(); if (process.env.PLAYLOG && (/warn|error/.test(m.type()) || /FAIL|spawn|wreck|vehicle/i.test(t))) console.log('   [page] ' + t.slice(0, 200)); if (/\[melee\] (quest|frame|FRAME)/i.test(t)) errs.push(t.slice(0, 160)); });
let code = 0;
try {
  // A FRESH SAVE: a new browser context has no `mel.*` keys, so `SAVE` is a new game, chapter 0, and the crash spawn takes him
  await page.goto(`http://127.0.0.1:${port}/index.html?w=tkit`, { timeout: 120000 });
  await page.waitForFunction(() => document.getElementById('boot').classList.contains('gone') && window.__play && window.__play.rig.ready, null, { timeout: 240000, polling: 1000 });
  const head = await page.evaluate(({ draw, fps }) => {
    const S = window.__play;
    // the clock is ours from here: every frame is exactly 1/fps s, whatever the machine is doing
    const t = performance.now(); window.__clock = { t, dt: 1000 / fps }; performance.now = () => window.__clock.t;
    if (!draw) S.renderer.render = () => {};
    window.__crash = m => { (window.__crashes = window.__crashes || []).push(String(m).split('\n').slice(0, 2).join(' | ')); };
    const P = S.player.pos, c = S.CRASH.at;
    return { pos: [P.x, P.y, P.z].map(v => +v.toFixed(1)), ch: S.SAVE.ch, crash: c ? [c.x, c.z].map(v => +v.toFixed(1)).join(',') + (S.CRASH && S.CRASH.model_ok ? ' (his model)' : ' (code-built)') + ' | spawned ' + S.CRASH.spawned + ' inTK ' + S.inTK() + ' ch ' + S.SAVE.ch + ' inTown ' + S.SAVE.flags.inTown + ' | trucks ' + (S.FVEH ? JSON.stringify(S.FVEH.draws) : '?') + ' | bushes ' + (S.FBK ? S.FBK.n + ' in ' + S.FBK.draws + ' draws' : '?') + ' | roadblocks ' + (S.RBK ? S.RBK.n + ' dressed, ' + S.RBK.solid + ' solid' : '?') : null, bodies: S.DUMMIES.length, notes: (S.MISSING || []).join(', ') };
  }, { draw: DRAW, fps: FPS });
  console.log(`== play  tkit, fresh save (chapter ${head.ch}), seed ${SEED}  spawn ${head.pos}  crash ${head.crash}  ${head.bodies} bodies  ${el()}` + (head.notes ? `  NOTE: ${head.notes}` : ''));

  // THE DRIVER lives in the page: `__drive(n)` runs n frames, applying the current step's policy before each, and returns where
  // the quest stands. Policies act through the pads and the shipped functions named above, never by writing the save.
  await page.evaluate(({ STUCK }) => {
    const S = window.__play, st = { key: '', t: 0, best: 1e9, bestT: 0, walked: 0, tele: 0, px: 0, pz: 0, blowT: 0, talkT: 0, holdT: 0, log: [], lastNpc: null };
    const stepKey = () => (S.quest.cur ? S.quest.cur.id + '.' + S.quest.step : '-');
    const stickOff = () => { const L = S.stick.L, R = S.stick.R; L.x = L.y = 0; L.down = 0; R.x = R.y = 0; R.down = 0; R.far = 0; };
    // a world direction onto the left pad: the inverse of the shipped `stickWorld` (dx = -ly sa - lx ca, dz = -ly ca + lx sa)
    const push = (wx, wz, m) => { const sa = Math.sin(S.cam.az), ca = Math.cos(S.cam.az); S.stick.L.down = 1; S.stick.L.y = -(wx * sa + wz * ca) * m; S.stick.L.x = (wz * sa - wx * ca) * m; };
    // a thumb's walk, not a straight line: into a wall he takes COVER (`wallSt`, the shipped hold pins him, and undoes a
    // teleport), so off a wall he pushes away from it first; and a walk that stalls side-steps (alternate sides) before it
    // counts as stuck. Both are what a thumb does; neither writes his position.
    const walk = (tx, tz, run) => { const p = S.player, P = p.pos, dx = tx - P.x, dz = tz - P.z, d = Math.hypot(dx, dz) || 1; let wx = dx / d, wz = dz / d; const m = run ? 1 : .55;
      if (p.wallSt) { const W = p.wall; if (W && W.nx !== undefined) { wx = W.nx; wz = W.nz; } else { wx = -wx; wz = -wz; } st.walls++; push(wx, wz, 1); return d; }
      if (st.side > 0) { st.side -= window.__clock.dt / 1000; const sg = st.sideSign; push(-wz * sg, wx * sg, 1); return d; }
      push(wx, wz, m); return d; };
    const near = (tx, tz) => { const P = S.player.pos; return Math.hypot(tx - P.x, tz - P.z); };
    const bodyAt = pos => S.DUMMIES.find(d => d.root && d.root.position === pos) || null;
    // A STRIKE'S OWN POWER AND DAMAGE (m430): the chain's grading (`melPower`: the opener, the build, the finisher) and the
    // fist's damage -- power 1 was the finisher every time, and a skinny man flung 6 m on the opener is out of reach
    // before the sample can start. Blows inside 1.5 s of each other advance the chain, as flicks do.
    const blow = d => { const P = S.player.pos, R = d.root.position, h = Math.atan2(R.x - P.x, R.z - P.z);
      st.chain = st.t - st.blowT < 1.5 ? st.chain + 1 : 0; const pw = S.melPower(st.chain % S.MELEE.links, S.MELEE.links);
      S.dummyBlow(d, h, pw, S.FOE.dmg.fist); st.blowT = st.t; st.log.push('blow ' + (d.markId || S.mphName(d.K)) + ' p' + pw.toFixed(2) + ' @' + st.t.toFixed(1)); };
    const downBody = () => S.DUMMIES.find(d => d.st === 'down' && !d.wasK && !d.K.pal && !/alien/i.test(S.mphName(d.K))) || null;
    // the stuck rule: no progress toward the walk target for STUCK s -> the shipped teleport, said so in the row
    const progress = d => { if (d < st.best - .3) { st.best = d; st.bestT = st.t; } return st.t - st.bestT; };
    // m484: to a target's own LEVEL, beside it (0.8 m) -- a few metres short toward him is open water off a rock's edge
    const teleport = (tx, tz, back, ty) => { const P = S.player.pos, dx = tx - P.x, dz = tz - P.z, d = Math.hypot(dx, dz) || 1, b = Math.min(ty != null ? .8 : back, d * .9);
      st.log.push('TELEPORT ' + st.walked.toFixed(0) + 'm from ' + P.x.toFixed(0) + ',' + P.y.toFixed(1) + ',' + P.z.toFixed(0) + ' to ' + tx.toFixed(0) + ',' + (ty != null ? (+ty).toFixed(1) : '-') + ',' + tz.toFixed(0) + ' @' + st.t.toFixed(1)); st.tele++;
      // the target's own level when it has one (`godTo` with no y lands on the highest floor it finds, which beside a
      // scaffold is the scaffold); a body's root y is where its feet are
      S.godTo(tx - dx / d * b, ty !== undefined && ty !== null ? ty : null, tz - dz / d * b); stickOff(); st.best = 1e9; st.bestT = st.t; };
    // reached in xz but a floor apart (a roof over him, a walkway under) is not reached: it counts as stuck, so the walk
    // side-steps and, if allowed, the teleport takes him to the target's level
    const goTo = (tx, tz, r, run, mayTele, ty) => { const d = walk(tx, tz, run), P = S.player.pos, dy = ty !== undefined && ty !== null ? Math.abs(P.y - ty) : 0;
      if (d < r && dy < 1.5) { stickOff(); return true; }
      const stall = progress(d < r ? d + dy : d);
      if (stall > 1.2 && st.side <= 0 && st.t - st.sideT > 2.2) { st.side = .8; st.sideT = st.t; st.sideSign = -st.sideSign; st.sides++; }
      if (stall > STUCK && mayTele) teleport(tx, tz, d < r ? 0 : r * .6, ty); return false; };
    const policy = (s0, T00) => {
      const q = S.quest.cur; if (!q) return 'no quest';
      const s = s0 || q.steps[S.quest.step], T0 = s0 ? (T00 || null) : S.quest.tgt, P = S.player.pos;
      // m452: a target with a non-finite coordinate is NEVER walked to -- the stick would carry the NaN into the player (it did,
      // twice, on the building site's ladder, and looked like a game NaN). The step is named in the log instead.
      const T = T0 && Number.isFinite(T0.x) && Number.isFinite(T0.z) ? T0 : null;
      if (T0 && !T) { if (!st.nanT) { st.nanT = 1; st.log.push('NaN TARGET from the game at ' + stepKey() + ' ' + [T0.x, T0.y, T0.z].join(',')); } stickOff(); return 'the game gave a NaN target'; }
      // m485: OFF THE BOARD for anything but the gap it was taken out for -- nobody talks to a man on a deck (`talk.near` is
      // null while riding) and a boss fought from one took 195 of its 200 s. The left pad's down-flick, as a thumb does it.
      if (S.player.riding && !(s.type === 'flag' && s.flag === 'isl:gap')) { if (!S.boardStepOff()) stickOff(); return ''; }
      switch (s.type) {
        case 'goto': { if (!T) return 'goto: no target yet'; goTo(T.x, T.z, (s.r || 3) * .6, true, true); return ''; }
        case 'reach': { if (!T) return 'reach: no target'; goTo(T.x, T.z, (s.r || 4) * .6, true, true, Number.isFinite(T.y) ? T.y : undefined); return ''; }
        case 'talk': { if (!T) return 'talk: nobody to talk to';

          // m452: a speaker who would not talk to him as he is (`socialOk` -- most flee an alien): put on a form they will,
          // through the shipped picker, the way a player does at the forms wheel
          { const d = bodyAt(T); if (d && d.talk && !S.socialOk(d) && !st.formT) { st.formT = 1;
              // m479: the form whose GROUP this speaker talks to (`socialOf` and `talks`), not merely the first that changes him
              const want = [S.socialOf(d), ...((d.talk.talks) || [])], grp = nm => (S.ROLEFORM[nm] && S.ROLEFORM[nm].group) || S.socialGroup(nm);
              const pick = S.SAVE.forms.find(nm => nm !== 'zap' && (want.includes('*') || want.includes(grp(nm)))) || S.SAVE.forms.find(nm => nm !== 'zap');
              if (pick) { S.formPick(pick); st.log.push('form ' + pick + ' (' + grp(pick) + ' for ' + want.join('/') + ') @' + st.t.toFixed(1)); } } } if (st.t - (st.tkLogT || -9) > 4) { st.tkLogT = st.t; const d2 = bodyAt(T); if (d2) { const R = d2.root.position; st.log.push(`spk ${d2.st} y${R.y.toFixed(1)} me${P.y.toFixed(1)} d${Math.hypot(R.x - P.x, R.z - P.z).toFixed(1)} v${[d2.vx || 0, d2.vy || 0].map(v => (+v).toFixed(1))} flee${(+d2.fleeT || 0).toFixed(1)} wasK${d2.wasK ? 1 : 0} talk${d2.talk ? 1 : 0} id ${d2.talk && d2.talk.id} | near ${S.talk.near ? (S.talk.near.markId || (S.talk.near.talk && S.talk.near.talk.id)) : '-'} cur ${S.talk.cur ? (S.talk.cur.talk && S.talk.cur.talk.id) : '-'} line ${S.talk.line} brush ${S.talk.brush ? 1 : 0} knock ${S.player.knock ? 1 : 0}`); } }
          if (goTo(T.x, T.z, 2.0, false, true, T.y) && st.t - st.talkT > .6) { st.talkT = st.t; S.talkTap(); st.log.push('talk @' + st.t.toFixed(1)); } return ''; }
        case 'defeat': { if (!T) return 'defeat: nobody left to knock down'; const d = bodyAt(T); if (!d) return 'defeat: target is not a body';
          st.lastNpc = d.markId || null; if (goTo(T.x, T.z, 1.6, true, true, T.y) && st.t - st.blowT > .5) blow(d); return ''; }
        // the turn is the shipped test's own doing (it fires `virusGo` when he is within `r`): walk up and watch
        case 'skin': { if (!T) return 'skin: nobody to turn'; goTo(T.x, T.z, Math.max(2, (s.r || 15) * .4), true, true); return ''; }
        // the thing wearing them: knocked down each time it is UP (a blow on a downed body only punts it; the count is at
        // the get-up, `d.downs` against `qDowns`), until the shipped turn-back takes it
        case 'unskin': { if (!T) return 'unskin: nobody tagged'; const d = bodyAt(T); if (!d) { goTo(T.x, T.z, 3, true, true); return ''; }
          if (st.t - (st.ukT || -9) > 3) { st.ukT = st.t; const R = d.root.position; st.log.push(`boss ${d.st} ${[R.x, R.y, R.z].map(v => v.toFixed(0))} ok ${d.okY != null ? d.okY.toFixed(1) : '-'} v ${[d.vx || 0, d.vy || 0, d.vz || 0].map(v => (+v).toFixed(1))} me ${P.y.toFixed(1)}`); }
          // m484: never walk or teleport to a body under the world (the level a body falls to over open sea)
          if (T.y < -50) { stickOff(); return 'unskin: the body is under the world'; }
          if (goTo(T.x, T.z, 1.8, true, true, T.y) && d.st !== 'down' && st.t - st.blowT > .6) blow(d); return ''; }
        case 'sample': { let d = downBody();
          // m452: a step that names KINDS (any of them will do): one of those, downed -- knocked down first if none is
          // m479: a step naming a ROLE's form (`form: 'ENGINEER'`: Ivy by crane 1) finds the bodies wearing that role
          const roleOf = x => x.role && S.ROLEFORM[x.role] ? S.ROLEFORM[x.role].name : null;
          const roleStep = s.form && Object.values(S.ROLEFORM).some(R => R.name === s.form);
          if (s.kinds || s.kind || roleStep) { const ks = (s.kinds || (s.kind ? [s.kind] : [])).map(S.mphFold), ok = x => !x.wasK && !x.gone && x.root && x.root.position.y > -100 && (roleStep ? roleOf(x) === s.form : ks.includes(S.mphName(x.K)));   // m469: not one under the world
            d = S.DUMMIES.find(x => x.st === 'down' && ok(x)) || null;
            { const lost = S.DUMMIES.find(x => x.root && x.root.position.y <= -100 && ks.includes(S.mphName(x.K)) && !x.gone); if (lost && !st.lostLog) { st.lostLog = 1; st.log.push('BODY UNDER THE WORLD ' + (lost.markId || S.mphName(lost.K)) + ' y ' + lost.root.position.y.toFixed(0)); } }
            if (!d) { let f = null, fd = 1e9; for (const x of S.DUMMIES) { if (!ok(x) || !x.root) continue; const q = near(x.root.position.x, x.root.position.z); if (q < fd) { fd = q; f = x; } }
              if (!f) return 'sample: nobody of ' + ks.join('/');
              const F = f.root.position; if (goTo(F.x, F.z, 1.6, true, true, F.y) && st.t - st.blowT > .5) blow(f); return ''; } }
          if (!d) { const f = S.DUMMIES.find(x => x.markId && x.markId === st.lastNpc && !x.wasK) || null; if (!f) return 'sample: nobody is down and the last target is gone';
            if (goTo(f.root.position.x, f.root.position.z, 1.6, true, true, f.root.position.y) && st.t - st.blowT > .5) blow(f); return ''; }
          const R = d.root.position; if (goTo(R.x, R.z, S.SAMPLE.reach * .7, true, true, R.y)) { const RS = S.stick.R; RS.down = 1; RS.x = RS.y = 0; RS.far = 0; st.holdT += window.__clock.dt / 1000; } return ''; }
        case 'gate': { const G = S.GATES.find(g => g.id === s.id); if (!G) return 'gate: no such gate ' + s.id;
          // m486: THE FORM THE GATE WANTS (its type's own rule: `ride` the biker on his bike, `groups` a form of that group, `crowd`
          // the city's, `need` a stem or a role's name; 'human' anything but himself) -- put on once, through the forms wheel's picker
          { const GT = S.GATE_TYPES[G.type], grp = nm => (S.ROLEFORM[nm] && S.ROLEFORM[nm].group) || S.socialGroup(nm), F = S.SAVE.forms.filter(nm => nm !== 'zap');
            const want = GT.ride ? F.find(nm => /BIKER/.test(nm)) : GT.groups ? F.find(nm => GT.groups.includes(grp(nm))) : GT.crowd ? F.find(nm => grp(nm) === 'city')
              : GT.need === 'human' ? F[0] : F.find(nm => nm === S.mphFold(GT.need) || nm === GT.need);
            if (want && S.formNow() !== want && st.gForm !== want) { st.gForm = want; S.formPick(want); st.log.push('form ' + want + ' for ' + G.type + ' @' + st.t.toFixed(1)); return ''; }
            if (S.player.mphSt) { stickOff(); return ''; } }
          const sn = Math.sin(G.h), cn = Math.cos(G.h), v = (P.x - G.x) * sn + (P.z - G.z) * cn, side = v >= 0 ? 1 : -1;
          // a `fix` gate is mended by LEANING on it as the right body (`gateStep`: in its span for `GATE.fixT`), so he walks
          // straight at the slab and keeps pushing -- no side-step, which would take him out of the span and reset the lean
          st.gate = `gate v ${v.toFixed(2)} u ${((P.x - G.x) * cn - (P.z - G.z) * sn).toFixed(2)} fixT ${(G.fixT || 0).toFixed(2)} open ${G.open ? 1 : 0} lets ${S.GATE_TYPES[G.type] && (S.GATE_TYPES[G.type].need || '')} side ${G.side}`;
          if (S.GATE_TYPES[G.type] && S.GATE_TYPES[G.type].pass === 'fix' && !G.open) { st.side = 0; if (!st.gateIn) { if (goTo(G.x + sn * 5 * side, G.z + cn * 5 * side, 1.2, true, true, G.y)) st.gateIn = 1; return ''; } walk(G.x, G.z, false); return ''; }
          // first the approach point 7 m out on his side, then straight through to 7 m past it; no teleport: a gate is walked
          const ax = G.x + sn * 7 * side, az = G.z + cn * 7 * side, bx = G.x - sn * 7 * side, bz = G.z - cn * 7 * side;
          if (!st.gateIn) { if (goTo(ax, az, 1.2, true, true, G.y)) st.gateIn = 1; return ''; }   // m486: at the gate's own level
          goTo(bx, bz, 1.0, false, false); return ''; }
        // m469: THE RACE (`raceStep`): on the bike (the biker form IS the bike), stopped at the gate for the countdown, then
        // the loop's own line ridden like a thumb would -- the stick at a point ~10 m ahead on `raceAt`, never a teleport
        case 'flag': if (s.flag === 'gang:respect') {
          const R = S.HCRACE, G = S.HCBIKE.startAt;
          if (!S.player.bike) { if (!st.formT) { st.formT = 1; S.formPick('FAT BIKER'); st.log.push('form FAT BIKER @' + st.t.toFixed(1)); } }
          if (R.st === 'race') {
            if (st.raceN !== R.runs) { st.raceN = R.runs; st.raceS = R.lap * R.len + Math.max(0, R.cp - 1) / R.cps * R.len; st.log.push('race ' + R.runs + ' GO @' + st.t.toFixed(1)); }
            // where he IS on the line: the nearest point in a window just behind to well ahead of the last one (never behind it by
            // more than the window, so running wide cannot turn him round), then aim 14 m past it
            { let bs = st.raceS, bd = 1e9; for (let q = st.raceS - 6; q <= st.raceS + 60; q += 2) { const B = S.raceAt(q), e = Math.hypot(B.x - P.x, B.z - P.z); if (e < bd) { bd = e; bs = q; } } st.raceS = Math.max(st.raceS, bs); }
            // m496: IN THE AIR THE THUMB HOLDS ITS LINE. Steering for the next point mid-jump turned the deck under him, and a
            // straight landing snaps his speed onto the deck's heading -- so he came down pointed off the track and rode 20 m wide
            const A = S.raceAt(st.raceS + 14), pl = S.player;
            if (!pl.grounded) push(Math.sin(pl.boardH), Math.cos(pl.boardH), 1); else walk(A.x, A.z, true); st.lapSeen = R.lap + ':' + R.cp + ' v ' + Math.hypot(S.player.vel.x, S.player.vel.z).toFixed(1) + ' her ' + (R.sR / R.len).toFixed(2) + ' laps, me ' + ((R.lap * R.cps + R.cp - 1) / R.cps).toFixed(2) + ' @' + R.t.toFixed(0) + 's'; return '';
          }
          if (st.raceN && st.raceN === R.runs && R.st === 'idle' && st.raceLost !== R.runs) { st.raceLost = R.runs; st.log.push('race ' + R.runs + ' LOST at lap:cp ' + st.lapSeen + ' @' + st.t.toFixed(1)); }
          if (R.st === 'count') { stickOff(); return ''; }
          if (st.t - (st.raceLogT || -99) > 15) { st.raceLogT = st.t; const p = S.player; st.log.push(`gate? st ${R.st} cool ${(+R.cool).toFixed(1)} board ${p.board} bike ${p.bike} mph ${p.mphK ? S.mphName(p.mphK) : '-'} d ${Math.hypot(P.x - G[0], P.z - G[2]).toFixed(1)} v ${Math.hypot(p.vel.x, p.vel.z).toFixed(1)} | PBIKE.up ${mel.PBIKE.up} mode ${p.mphK && p.mphK.mode} mph ${!!(p.mphK && p.mphK.mph)} rigIs ${!!(p.mphK && p.mphK.mph && S.rig.model === p.mphK.mph.model)} mphSt ${p.mphSt} bikeOn ${mel.bikeOn()} sk8 ${mel.SK8 && mel.SK8.on}`); }
          if (goTo(G[0], G[2], 3, false, true, G[1])) stickOff();
          return '';
        }
        // m479: THE FERRY (`ferryStep`): wait at Old Town's landing for it to be docked there, walk onto its deck clear of the
        // cabin, stand still while it crosses (it carries whoever is grounded on its boxes), then walk off along its own
        // Waterfront walk-off points and on inland until the shipped "on the Waterfront" test passes
        if (s.flag === 'wf:in' && S.OFERRY.grp && S.OFERRY.frame) {
          const O = S.OFERRY, B = O.grp.position, Fr = O.frame, dir = [Fr.S, Fr.C], toOT = Math.sign((O.otAt[0] - B.x) * dir[0] + (O.otAt[2] - B.z) * dir[1]) || 1;
          const al = (P.x - B.x) * dir[0] + (P.z - B.z) * dir[1], ac = (P.x - B.x) * dir[1] - (P.z - B.z) * dir[0];
          const onBoat = Math.abs(al) < O.len / 2 - .4 && Math.abs(ac) < O.beam / 2 - .3;   // inside the deck's own rectangle
          const deckAt = (A, C) => [B.x + dir[0] * A * toOT + dir[1] * C, B.z + dir[1] * A * toOT - dir[0] * C];
          const boardStep = () => { const W3 = [deckAt(O.len / 2 + 1, 0), deckAt(4.5, O.beam / 2 - .9), deckAt(-4.5, O.beam / 2 - .9)]; st.boardI = st.boardI || 0;
            const Q = W3[Math.min(st.boardI, 2)]; if (Math.hypot(P.x - Q[0], P.z - Q[1]) < .8 && st.boardI < 3) st.boardI++;
            if (st.boardI >= 3) stickOff(); else walk(Q[0], Q[1], false); };
          if (st.t - (st.fLogT || -99) > 15) { st.fLogT = st.t; st.log.push(`ferry at ${O.at} ${O.st} t${(+O.t).toFixed(0)} boat ${B.x.toFixed(0)},${B.z.toFixed(0)} y${(Fr.sea + O.boatH).toFixed(1)} ot ${O.otAt.map(v => v.toFixed(0))} me ${[P.x, P.y, P.z].map(v => v.toFixed(1))} on${onBoat ? 1 : 0}`); }
          if (!onBoat && !st.offBoat) {
            // the ferry's own way down to its pontoon (`otWalk`), point by point, then aboard when it is docked here
            const Wk = O.otWalk || [[O.otAt[0], O.otAt[2]]]; st.otI = st.otI || 0;
            if (st.otI < Wk.length) { const Q = Wk[st.otI]; if (goTo(Q[0], Q[1], 1.2, false, true)) st.otI++; return ''; }
            if (O.at === 0 && O.st === 'dock' && O.t > 1) boardStep(); else stickOff();
            return '';
          }
          // aboard at Old Town and still docked: on round the cabin (4 m wide amidships) to the FAR half, so the way off at the
          // Waterfront is a few metres and not past it in a 10 s stop
          if (onBoat && O.at === 0 && O.st === 'dock' && (st.boardI || 0) < 3) { boardStep(); return ''; }
          if (onBoat && !(O.at === 1 && O.st === 'dock')) { stickOff(); if (!st.ferryLog) { st.ferryLog = 1; st.log.push('aboard @' + st.t.toFixed(1)); } return ''; }
          st.offBoat = 1; st.wfI = st.wfI || 0;
          const Wk = O.wfWalk || [[O.wfAt[0], O.wfAt[2]]], last = Wk[Wk.length - 1], prev = Wk[Wk.length - 2] || [O.wfAt[0], O.wfAt[2]];
          // off over the boat's OWN end (its sides are railed), then the pontoon, the pier walk, and on inland
          if (!st.endAt) st.endAt = [B.x - dir[0] * (O.len / 2 + 1.6) * toOT, B.z - dir[1] * (O.len / 2 + 1.6) * toOT];
          const pts = [st.endAt, [O.wfAt[0], O.wfAt[2]], ...Wk, [last[0] + (last[0] - prev[0]) * 3, last[1] + (last[1] - prev[1]) * 3]];
          const Q = pts[Math.min(st.wfI, pts.length - 1)]; if (Math.hypot(P.x - Q[0], P.z - Q[1]) < 1.5 && st.wfI < pts.length - 1) st.wfI++;
          walk(Q[0], Q[1], false); return '';
        }
        // m480: THE PACIFIER ORB (`orbHit`, `airAim`): within 18 m of it, the blaster out (`kitPick`, the left wheel's own
        // press), the camera turned onto it (what a thumb's drag does: `airAim` takes any orb inside 0.19 rad of the lens),
        // and the trigger pulled straight up past `fireAt` and let go -- a charged shot, which counts twice
        if (s.flag === 'orb:pacifier' && S.OORB.T) {
          const O = S.OORB, Tg = O.T, d = Math.hypot(Tg.x - P.x, Tg.z - P.z);
          if (d > 18) { goTo(Tg.x, Tg.z, 14, true, true); return ''; }
          const L = S.stick.L; L.x = L.y = 0; L.down = 0;
          const bi = S.WEAP.slots.findIndex(w => w.key === 'blaster'); if (!S.slotNow().aim && bi >= 0) { S.kitPick(bi); return ''; }
          S.cam.az = Math.atan2(Tg.x - P.x, Tg.z - P.z);
          st.fireT = (st.fireT || 0) + window.__clock.dt / 1000; const ph = st.fireT % 1.5, R = S.stick.R;
          if (ph < 1.15) { R.down = 1; R.x = 0; R.y = -1; R.far = 1; } else { R.down = 0; R.x = R.y = 0; R.far = 0; }
          if (!st.orbLog || st.t - st.orbLog > 6) { st.orbLog = st.t; st.log.push('orb hp ' + O.hpNow + ' d ' + d.toFixed(0) + ' slot ' + S.slotNow().key + ' @' + st.t.toFixed(1)); }
          return '';
        }
        // m481: THE ROPE BRIDGES (`IXING.spans`, each its own sag `pt(t)` in the islands' frame): walked, not run -- the deck
        // is 1.4 m wide -- sample by sample along every span in the chain, then onto the landing field
        if (s.flag === 'isl:in' && S.IXING.spans && S.IXING.spans.length) {
          if (!st.rope) { st.rope = []; for (const Sp of S.IXING.spans) for (let t = 0; t <= 1.0001; t += .08) { const q = Sp.pt(t), [x, z] = S.islWorld(q[0], q[2]); st.rope.push([x, z]); }
            if (S.IXING.fieldAt) st.rope.push([S.IXING.fieldAt[0], S.IXING.fieldAt[2]]); st.ropeI = 0;
            // start at the sample nearest him that is not behind the first one he can reach
            let bd = 1e9; st.rope.forEach((q, i) => { const e = Math.hypot(q[0] - P.x, q[1] - P.z); if (e < bd) { bd = e; st.ropeI = i; } }); }
          const Q = st.rope[Math.min(st.ropeI, st.rope.length - 1)];
          if (Math.hypot(Q[0] - P.x, Q[1] - P.z) < (st.ropeI === 0 ? 3 : 1.2) && st.ropeI < st.rope.length - 1) st.ropeI++;
          if (st.ropeI === 0) goTo(Q[0], Q[1], 2, true, true); else { st.side = 0; walk(Q[0], Q[1], false); }
          if (!st.ropeLog || st.t - st.ropeLog > 15) { st.ropeLog = st.t; st.log.push('rope ' + st.ropeI + '/' + st.rope.length + ' y ' + P.y.toFixed(1) + ' @' + st.t.toFixed(1)); }
          return '';
        }
        // m482: A FLIGHT DOWN ON RUE'S FIELD (`isl:landed`: out of a flight, grounded inside the cones' 6.5 m). Skye's form
        // first (the `glider` stem: the ordinary sample driver, on his kind), then from 7 m short of the cross, heading at it,
        // the right pad double-tapped (`wingTapR`, a frame apart), and at once a dive with the stick (down = dive, his
        // default) steering onto the cross (+x turns him right: heading -= x). Down outside the ring, round again.
        if (s.flag === 'isl:landed' && S.IXING.fieldAt) {
          const stem = S.mphFold(S.rosterOf('glider').stem), p = S.player, C = S.IXING.fieldAt, L = S.stick.L;
          if (!p.wing && !(p.mphK && S.mphName(p.mphK) === stem)) {
            if (S.SAVE.forms.includes(stem)) { if (!st.flForm) { st.flForm = 1; S.formPick(stem); st.log.push('form ' + stem + ' @' + st.t.toFixed(1)); } return ''; }
            return policy({ type: 'sample', kind: S.rosterOf('glider').stem });
          }
          if (p.mphSt) { stickOff(); return ''; }
          const hC = Math.atan2(C[0] - P.x, C[2] - P.z), dC = Math.hypot(C[0] - P.x, C[2] - P.z);
          if (!p.wing) {
            if (st.flPh === 2) { st.flPh = 0; st.flTries = (st.flTries || 0) + 1; st.log.push('landed ' + dC.toFixed(1) + ' m from the cross @' + st.t.toFixed(1)); }
            const T1 = [C[0] - Math.sin(st.flA || 0) * 7, C[2] - Math.cos(st.flA || 0) * 7];
            if (!st.flPh) { if (goTo(T1[0], T1[1], .8, false, true, C[1])) { st.flPh = 1; st.flT = 0; } return ''; }
            // face the cross for a beat, then the double tap on two consecutive frames
            st.flT += window.__clock.dt / 1000; walk(C[0], C[2], false);
            if (st.flT > .25 && !st.tap1) { st.tap1 = 1; S.wingTapR(); } else if (st.tap1) { st.tap1 = 0; S.wingTapR(); st.flPh = 2; st.flA = (st.flA || 0) + .9; }
            return '';
          }
          L.down = 1; const err = Math.atan2(Math.sin(hC - p.heading), Math.cos(hC - p.heading));
          L.x = Math.max(-1, Math.min(1, -err * 2)); L.y = 1;
          return '';
        }
        // m482: THE GAP (`isl:gap`: airborne off the humps' lip, down dry 12 m or more past it). As himself (a disguise cannot
        // take the board), the deck out (`kitPick`) and stepped on (the left pad's up-flick, `boardMount`), from the ramp's own
        // top (`godRamp`), then flat out along the ramp's line and never braking; down short, back to the top and again
        if (s.flag === 'isl:gap' && S.IBASE.ramp && S.IBASE.godRamp) {
          const p = S.player, Rp = S.IBASE.ramp, G = S.IBASE.godRamp;
          if (p.mphK && !p.mphSt) { if (!st.gZap) { st.gZap = 1; S.formPick('zap'); st.log.push('as himself @' + st.t.toFixed(1)); } return ''; }
          if (p.mphSt) { stickOff(); return ''; }
          const far = S.islWorld(...Rp.R(Rp.sL + 40, 0));
          if (!st.gMeas) { st.gMeas = 1; const m = []; for (const ss of [-3, -1.5, 0, .5, 2, 4, 8]) { const [x, z] = S.islWorld(...Rp.R(ss, 0)); m.push(ss + ':' + S.groundAt(x, z, 40, 60).toFixed(1) + '/' + Rp.tg(ss).toFixed(1)); } st.log.push('ramp floor/tg ' + m.join(' ') + ' y0 ' + Rp.y0.toFixed(1) + ' sL ' + Rp.sL.toFixed(1)); }
          if (!p.riding) {
            const bi = S.WEAP.slots.findIndex(w => w.board);
            if (!st.gRun && !st.gAt) { if (goTo(G[0], G[2], 1.2, false, true, G[1])) { st.gAt = 1; st.gFace = 0; } return ''; }
            // FACING DOWN THE LINE FIRST: on the deck a stick more than 90 degrees off its nose is the BRAKE, never a turn
            if (!st.gRun) { st.gFace += window.__clock.dt / 1000; walk(far[0], far[1], false);
              if (st.gFace < .5) return ''; if (!S.slotNow().board) { S.kitPick(bi); return ''; }
              if (!p.swap) { S.boardMount(0, -1); st.gRun = 1; st.gAt = 0; st.gTry = (st.gTry || 0) + 1; st.log.push('board run ' + st.gTry + ' @' + st.t.toFixed(1)); } }
            return '';
          }
          // riding: flat out at the far end of the line; once he is down again past the lip and it did not count, back to the top
          const [u, v] = S.islLocal(P.x, P.z), [lu, lv] = Rp.R(Rp.sL, 0), sNow = (u - lu) * Rp.dir[0] + (v - lv) * Rp.dir[1];
          // m483: THE TRACE -- every 0.2 s of the first 3 s of each run: where on the line, speed along it, the grade the board
          // reads, grounded, height over the floor straight under him
          if ((st.gTrN || 0) < 34 && st.t - (st.gTrT || 0) > .1 && (st.gTrN || 0) < 34) { st.gTrT = st.t; st.gTrN = (st.gTrN || 0) + 1;
            (st.gTr = st.gTr || []).push(sNow.toFixed(1) + '|' + (p.vel.x * Math.sin(p.boardH) + p.vel.z * Math.cos(p.boardH)).toFixed(1) + '|' + S.boardGrade(p.boardH).toFixed(2) + '|' + (p.grounded ? 'g' : 'a') + '|' + (P.y - S.groundAt(P.x, P.z, P.y + .3, 2)).toFixed(2) + '|' + (S.IXING.gapArm ? 'A' + (+S.IXING.gapT).toFixed(1) : '-') + (S.SAVE.flags['isl:gap'] ? 'F' : '') + '|' + P.y.toFixed(1));
            if (st.gTrN === 34) st.log.push('trace s|v|grade|g|dy ' + st.gTr.slice(12).join(' ')); }
          if (S.IXING.gapArm && st.gArmPrev !== 1) st.gArmS = sNow; st.gArmPrev = S.IXING.gapArm ? 1 : 0;
          if (sNow >= -.3 && !st.gLip) { st.gLip = 1; st.log.push('lip v ' + Math.hypot(p.vel.x, p.vel.z).toFixed(1) + ' vy ' + p.vel.y.toFixed(1) + ' y ' + P.y.toFixed(1) + ' top ' + (S.SK8 ? S.SK8.top : '?')); }
          if (sNow < -5) st.gLip = 0;
          // m484: a beat on the ground before calling it short -- the game's own gap test reads `grounded` a frame later
          st.gDown = p.grounded && sNow > 4 ? (st.gDown || 0) + window.__clock.dt / 1000 : 0;
          if (st.gDown > .5 && !S.SAVE.flags['isl:gap']) { st.gDown = 0; st.log.push('down at ' + sNow.toFixed(1) + ' m past the lip, across ' + (-(u - lu) * Rp.dir[1] + (v - lv) * Rp.dir[0]).toFixed(1) + ' y ' + P.y.toFixed(1) + ' sea ' + (S.ISLE ? S.ISLE.sea : '?') + ' arm ' + S.IXING.gapArm + ' armedAt ' + (st.gArmS != null ? st.gArmS.toFixed(1) : '-')); st.gRun = 0; S.godTo(G[0], G[1], G[2]); stickOff(); return ''; }
          if ((st.gLogN || 0) < 3 && (!st.gLogT || st.t - st.gLogT > 2)) { st.gLogT = st.t; st.gLogN = (st.gLogN || 0) + 1; const hl = Math.atan2(far[0] - P.x, far[1] - P.z); st.log.push('s ' + sNow.toFixed(1) + ' v ' + Math.hypot(p.vel.x, p.vel.z).toFixed(1) + ' y ' + P.y.toFixed(1) + (p.grounded ? ' g' : ' air') + ' bH ' + (+p.boardH).toFixed(2) + ' line ' + hl.toFixed(2) + ' near ' + S.DUMMIES.filter(d => d.root && Math.hypot(d.root.position.x - P.x, d.root.position.z - P.z) < 3).map(d => d.markId || S.mphName(d.K)).join('/')); }
          walk(far[0], far[1], true); return '';
        }
        // m486: THE TETHER'S POD (`shipPodStep`): onto its top while it is down (in place of the thermal flight up to it -- a
        // teleport, said in the row), still while it rises, and at the top off it to the hull's middle at its floor
        if (s.flag === 'ms:in' && S.ISHIP.P && S.ISHIP.P.box) {
          const I = S.ISHIP, Q = I.P, B = Q.box, p = S.player;
          const on = Math.abs(P.y - B.maxy) < .3 && Math.abs(P.x - B.cx) <= I.pod + .05 && Math.abs(P.z - B.cz) <= I.pod + .05;
          if (st.t - (st.podLog || -9) > 5) { st.podLog = st.t; st.log.push(`pod ${Q.st} y${(+Q.y).toFixed(1)} me ${P.y.toFixed(1)} on${on ? 1 : 0}`); }
          if (Q.st === 'top' && (on || Math.abs(P.y - I.floorY) < 3)) { walk(I.axis[0], I.axis[1], false); return ''; }
          if (on) { stickOff(); return ''; }
          if (Q.st === 'down') { S.godTo(B.cx, B.maxy + .05, B.cz); stickOff(); st.tele++; st.log.push('TELEPORT onto the pod @' + st.t.toFixed(1)); }
          else stickOff();
          return '';
        }
        // falls through to the ordinary flag driver
        { if (T) { goTo(T.x, T.z, 1.2, true, true, T.y); return ''; }   // m466: inside the game's own radius (the papers: 1.9 m), not at the edge of it
          if (s.flag === 'inTown' && S.ISLE.rect) { const R = S.ISLE.rect, tx = Math.min(Math.max(P.x, R[0] + 8), R[1] - 8), tz = Math.min(Math.max(P.z, R[2] + 8), R[3] - 8); goTo(tx, tz, 1, true, true); return ''; }
          return 'flag: no driver for ' + s.flag; }
      }
      return 'no driver for step type ' + s.type;
    };
    const ring = [];
    window.__drive = n => {
      const out = { frames: 0, err: null, why: '' };
      for (let i = 0; i < n; i++) {
        const k = stepKey(); if (k !== st.key) { stickOff(); Object.assign(st, { key: k, t: 0, best: 1e9, bestT: 0, walked: 0, tele: 0, blowT: -9, talkT: -9, holdT: 0, gateIn: 0, log: [], side: 0, sideT: -9, sides: 0, sideSign: 1, walls: 0, gate: '', formT: 0 }); st.px = S.player.pos.x; st.pz = S.player.pos.z; }
        const why = policy(); if (why) out.why = why;
        window.__clock.t += window.__clock.dt;
        try { S.frameBody(); } catch (e) { out.err = String(e && e.stack || e).split('\n').slice(0, 2).join(' | '); break; }
        const P = S.player.pos, p = S.player; st.walked += Math.hypot(P.x - st.px, P.z - st.pz); st.px = P.x; st.pz = P.z; st.t += window.__clock.dt / 1000; out.frames++;
        // THE NaN WATCHDOG: a coordinate that stops being a number is a bug in the frame that made it, and the frames before
        // it are the only trace there is (`ring`: the last 8 frames of his state) -- the step fails on the spot with them
        ring.push(`t${st.t.toFixed(2)} pos ${[P.x, P.y, P.z].map(v => +v.toFixed(2))} vel ${[p.vel.x, p.vel.y, p.vel.z].map(v => +v.toFixed(2))} g${p.grounded ? 1 : 0} knock${p.knock ? 1 : 0} wall:${p.wallSt || ''} ledge:${p.ledgeSt || ''} climb${p.climb ? 1 : 0} hang${p.hang ? 1 : 0} ride${p.riding ? 1 : 0} hp${p.hp !== undefined ? +(+p.hp).toFixed(0) : '?'} stick ${S.stick.L.x.toFixed(2)},${S.stick.L.y.toFixed(2)} az ${(+S.cam.az).toFixed(3)} face ${(+p.faceH).toFixed(3)} lock ${p.lock ? (p.lock.markId || S.mphName(p.lock.K)) + '@' + [p.lock.root.position.x, p.lock.root.position.y, p.lock.root.position.z].map(v => (+v).toFixed(1)) : '-'} step ${stepKey()} tgt ${S.quest.tgt ? [S.quest.tgt.x, S.quest.tgt.y, S.quest.tgt.z].map(v => (+v).toFixed(1)) : '-'} climbL ${p.climb ? [p.climb.cx, p.climb.cz, p.climb.top, p.climb.nx, p.climb.nz, p.climb.ux, p.climb.uz, p.climb.ha].map(v => (+v).toFixed(2)).join(',') : '-'} side ${p.climbSide} badBodies ${S.DUMMIES.filter(d => d.root && !Number.isFinite(d.root.position.x + d.root.position.y + d.root.position.z)).map(d => d.markId || S.mphName(d.K)).join('/') || 0}`); if (ring.length > 8) ring.shift();
        if (!Number.isFinite(+S.cam.az) && !out.err) { out.err = 'NaN in the camera: ' + ring.join('\n      '); break; }
        if (!Number.isFinite(P.x + P.y + P.z) || !Number.isFinite(p.vel.x + p.vel.y + p.vel.z)) { out.err = 'NaN in the player: ' + ring.join('\n      '); break; }
      }
      const q = S.quest.cur, s = q && q.steps[S.quest.step], P = S.player.pos;
      return Object.assign(out, { big: !!(s && s.type === 'unskin' && q.steps.some(x => x.type === 'skin' && x.tag === s.tag && x.big)), key: stepKey(), type: s ? s.type : '', text: s ? s.text : '', t: st.t, walked: st.walked, tele: st.tele, sides: st.sides, walls: st.walls, log: st.log.slice(-10), pos: [P.x, P.y, P.z].map(v => +v.toFixed(1)),
        form: S.player.mphK ? S.mphName(S.player.mphK) : 'zap', gate: st.gate || '', juice: Math.round(S.SAVE.juice), forms: S.SAVE.forms.slice(), ch: S.SAVE.ch, done: Object.keys(S.SAVE.flags).filter(f => f.startsWith('qdone:')), crashes: window.__crashes || [], sampT: st.holdT });
    };
  }, { STUCK });

  for (const CH of CHAPTERS) {
    const N = +CH.replace(/^ch/, ''); if (!Number.isFinite(N)) { console.log('BAD  ' + CH + ': a chapter is ch0, ch1, ...'); code = 1; continue; }
    // A CHAPTER IS ITS QUESTS IN FILE ORDER (`ch` on each); the shipped picker (`questAvail`: `from`, `needQ`, the chapter)
    // chooses the next one as the save allows, the tool only waits for it. A chapter asked for on its own (not reached
    // through the one before) has the save moved to it the way GOD's chapter buttons do, and him put at the city spawn.
    const Q = await page.evaluate(n => { const S = window.__play; return S.QUESTS.filter(q => q.ch === n && !q.dormant).map(q => q.id); }, N);
    if (!Q.length) { console.log('BAD  ' + CH + ': no quests carry ch ' + N); code = 1; continue; }
    const st0 = await page.evaluate(() => { const S = window.__play; return { ch: S.SAVE.ch }; });
    if (st0.ch !== N) {
      await page.evaluate(n => { const S = window.__play; S.quest.cur = null; S.SAVE.ch = n; S.progFlag('inTown', n >= 1 ? 1 : 0);
        // m466: AND WHAT THE CHAPTERS BEFORE IT GAVE HIM -- the forms their samples put on the wheel (a Chapter 2 start as
        // nobody but himself is an alien everybody runs from, which no player arriving there is), and their quests marked
        // done, so the kit found on the way (`GEAR`) is in his hands
        const FORMS_BY = [[1, 'HICK SKINNY'], [2, 'CONTRUCTION WORKER'], [3, 'FAT HIPSTER'], [4, 'FAT BIKER'], [5, 'ENGINEER'], [6, 'JACK']];
        for (const [c, nm] of FORMS_BY) if (n >= c) S.progForm(nm);
        for (const q of S.QUESTS) if (q.ch !== undefined && q.ch < n && !q.dormant) S.progFlag('qdone:' + q.id); if (n >= 1) mel.go('oldtown'); S.stick.L.x = S.stick.L.y = 0; }, N);
      console.log(`     ${CH}: the save moved to chapter ${N}` + (N >= 1 ? ' and him to the city spawn' : ''));
    }
    let bad = 0, steps = 0, cur = null, lastR = null, idle = 0;
    const row = (ok, R, extra) => console.log((ok ? 'ok   ' : 'BAD  ') + R.key.padEnd(8) + R.type.padEnd(7) + `'${R.text}'`.padEnd(58) + ` ${R.t.toFixed(1)} s, walked ${R.walked.toFixed(0)} m` + (R.sides ? `, ${R.sides} side-steps` : '') + (R.walls ? `, off a wall x${R.walls}f` : '') + (R.tele ? `, TELEPORTED x${R.tele}` : '') + (extra ? '  ' + extra : ''));
    // THE SHIPPED PICKER DRIVES THE ORDER. Whatever quest it follows is driven -- the chapter's own in turn, and anything
    // that takes over on the way (the incursion's `qinc` tracks itself when its ship comes) -- until every quest of the
    // chapter is done. A row per step as the key changes; a step over the budget is BAD and ends the chapter.
    for (;;) {
      const R = await page.evaluate(n => window.__drive(n), Math.round(FPS / 2));
      if (R.err || R.crashes.length) { row(false, R, 'FRAME ERROR ' + (R.err || R.crashes[0]).split('\n')[0]);
        // m451: the whole trace to a file -- an intermittent NaN is only worth catching if its frames survive the print
        try { fs.writeFileSync('play_fail.txt', (R.err || R.crashes.join('\n')) + '\n'); console.log('     trace -> play_fail.txt'); } catch (e) {}
        bad++; code = 1; break; }
      if (R.key !== cur) {
        if (cur && cur !== '-' && lastR) { row(true, Object.assign({}, R, { key: cur, type: lastR.type, text: lastR.text, t: lastR.t, walked: lastR.walked, tele: lastR.tele, sides: lastR.sides, walls: lastR.walls }), lastR.log.filter(l => /TELEPORT|blow|talk|form|NaN/.test(l)).join(' ') || ''); steps++; }
        cur = R.key;
      }
      if (Q.every(id => R.done.includes('qdone:' + id))) break;
      if (R.key === '-') { idle += R.frames / FPS; if (idle > 20) { console.log(`BAD  ${CH} the shipped picker offers nothing for 20 s (chapter ${R.ch}, done [${R.done.map(d => d.slice(6)).join(' ')}])`); bad++; code = 1; break; } } else idle = 0;
      // m484: a BIG boss (`big`, five downs, flung off its arena by every blow) gets 200 s; everything else the budget
      const lim = R.type === 'unskin' && R.big ? Math.max(BUDGET, 200) : BUDGET;
      if (R.t > lim) { row(false, R, `NOT PASSED in ${lim} s` + (R.why ? ' -- ' + R.why : '') + (R.log.length ? ' | ' + R.log.join(' ') : '') + ` | at ${R.pos} as ${R.form}, juice ${R.juice}` + (R.gate ? ' | ' + R.gate : '')); bad++; code = 1; break; }
      lastR = R;
    }
    const fin = await page.evaluate(() => { const S = window.__play; return { done: Object.keys(S.SAVE.flags).filter(f => f.startsWith('qdone:')), ch: S.SAVE.ch, forms: S.SAVE.forms.slice(), inTown: !!S.SAVE.flags.inTown, juice: S.SAVE.juice }; });
    const done = Q.filter(id => fin.done.includes('qdone:' + id)).length, ended = done === Q.length && !bad && fin.ch > N;
    console.log((ended ? 'ok   ' : 'BAD  ') + `${CH} ${ended ? 'COMPLETE' : 'NOT COMPLETE'}: ${done}/${Q.length} quests, ${steps} steps passed` + (bad ? `, ${bad} failed` : '') + ` | chapter ${fin.ch}, forms [${fin.forms.join(' ')}], inTown ${fin.inTown ? 1 : 0}, done [${fin.done.map(d => d.slice(6)).join(' ')}]  ${el()}`);
    if (!ended) code = 1;
  }
} catch (e) { console.log('BAD  play: ' + String(e && e.message || e).split('\n')[0]); code = 1; }
if (errs.length) console.log('page: ' + errs.slice(0, 6).join(' | '));
await browser.close(); server.close();
process.exit(code);
