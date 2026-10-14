// THE HEADLESS PLAYTHROUGH (m429, ROADMAP F0b-1). `npm run play [ch0 ch1 ...] [--draw] [--fps=30] [--budget=120]`
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
const DRAW = ARGS.includes('--draw'), FPS = +(opt('fps') || 30), BUDGET = +(opt('budget') || 120), STUCK = 4;
const CHAPTERS = ARGS.filter(a => !a.startsWith('--')); if (!CHAPTERS.length) CHAPTERS.push('ch0');

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
    body = s.replace(k, 'window.__play = { frameBody, player, cam, stick, quest, QUESTS, SAVE, DUMMIES, dummyBlow, godTo, GATES, ISLE, mphName, talkTap, renderer, rig, GODPLACES, MISSING, SAMPLE, MOVE, CRASH, progFlag }; ' + k);
  }
  r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(body);
});
await new Promise(ok => server.listen(0, ok));
const port = server.address().port, t0 = Date.now(), el = () => ((Date.now() - t0) / 1000).toFixed(0) + 's';

const browser = await pw.chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 640, height: 360 }, deviceScaleFactor: 1 });
const errs = []; page.on('pageerror', e => errs.push(e.message.split('\n')[0]));
page.on('console', m => { const t = m.text(); if (/\[melee\] (quest|frame|FRAME)/i.test(t)) errs.push(t.slice(0, 160)); });
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
    return { pos: [P.x, P.y, P.z].map(v => +v.toFixed(1)), ch: S.SAVE.ch, crash: c ? [c.x, c.z].map(v => +v.toFixed(1)) : null, bodies: S.DUMMIES.length, notes: (S.MISSING || []).join(', ') };
  }, { draw: DRAW, fps: FPS });
  console.log(`== play  tkit, fresh save (chapter ${head.ch})  spawn ${head.pos}  crash ${head.crash}  ${head.bodies} bodies  ${el()}` + (head.notes ? `  NOTE: ${head.notes}` : ''));

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
    const blow = d => { const P = S.player.pos, R = d.root.position, h = Math.atan2(R.x - P.x, R.z - P.z); S.dummyBlow(d, h, 1, null); st.blowT = st.t; st.log.push('blow ' + (d.markId || S.mphName(d.K)) + ' @' + st.t.toFixed(1)); };
    const downBody = () => S.DUMMIES.find(d => d.st === 'down' && !d.wasK && !d.K.pal && !/alien/i.test(S.mphName(d.K))) || null;
    // the stuck rule: no progress toward the walk target for STUCK s -> the shipped teleport, said so in the row
    const progress = d => { if (d < st.best - .3) { st.best = d; st.bestT = st.t; } return st.t - st.bestT; };
    const teleport = (tx, tz, back) => { const P = S.player.pos, dx = tx - P.x, dz = tz - P.z, d = Math.hypot(dx, dz) || 1, b = Math.min(back, d * .9);
      st.log.push('TELEPORT ' + st.walked.toFixed(0) + 'm from ' + P.x.toFixed(0) + ',' + P.z.toFixed(0) + ' @' + st.t.toFixed(1)); st.tele++;
      S.godTo(tx - dx / d * b, null, tz - dz / d * b); stickOff(); st.best = 1e9; st.bestT = st.t; };
    const goTo = (tx, tz, r, run, mayTele) => { const d = walk(tx, tz, run); if (d < r) { stickOff(); return true; }
      const stall = progress(d);
      if (stall > 1.2 && st.side <= 0 && st.t - st.sideT > 2.2) { st.side = .8; st.sideT = st.t; st.sideSign = -st.sideSign; st.sides++; }
      if (stall > STUCK && mayTele) teleport(tx, tz, r * .6); return false; };
    const policy = () => {
      const q = S.quest.cur; if (!q) return 'no quest';
      const s = q.steps[S.quest.step], T = S.quest.tgt, P = S.player.pos;
      switch (s.type) {
        case 'goto': { if (!T) return 'goto: no target yet'; goTo(T.x, T.z, (s.r || 3) * .6, true, true); return ''; }
        case 'reach': { if (!T) return 'reach: no target'; goTo(T.x, T.z, (s.r || 4) * .6, true, true); return ''; }
        case 'talk': { if (!T) return 'talk: nobody to talk to'; if (goTo(T.x, T.z, 2.0, false, true) && st.t - st.talkT > .6) { st.talkT = st.t; S.talkTap(); st.log.push('talk @' + st.t.toFixed(1)); } return ''; }
        case 'defeat': { if (!T) return 'defeat: nobody left to knock down'; const d = bodyAt(T); if (!d) return 'defeat: target is not a body';
          st.lastNpc = d.markId || null; if (goTo(T.x, T.z, 1.6, true, true) && st.t - st.blowT > .5) blow(d); return ''; }
        case 'skin': case 'unskin': { if (!T) return ''; const d = bodyAt(T); if (!d) { goTo(T.x, T.z, 3, true, true); return ''; }
          if (goTo(T.x, T.z, 1.8, true, true) && d.st !== 'down' && st.t - st.blowT > .6) blow(d); return ''; }
        case 'sample': { let d = downBody();
          if (!d) { const f = S.DUMMIES.find(x => x.markId && x.markId === st.lastNpc && !x.wasK) || null; if (!f) return 'sample: nobody is down and the last target is gone';
            if (goTo(f.root.position.x, f.root.position.z, 1.6, true, true) && st.t - st.blowT > .5) blow(f); return ''; }
          const R = d.root.position; if (goTo(R.x, R.z, S.SAMPLE.reach * .7, false, true)) { const RS = S.stick.R; RS.down = 1; RS.x = RS.y = 0; RS.far = 0; st.holdT += window.__clock.dt / 1000; } return ''; }
        case 'gate': { const G = S.GATES.find(g => g.id === s.id); if (!G) return 'gate: no such gate ' + s.id;
          const sn = Math.sin(G.h), cn = Math.cos(G.h), v = (P.x - G.x) * sn + (P.z - G.z) * cn, side = v >= 0 ? 1 : -1;
          // first the approach point 7 m out on his side, then straight through to 7 m past it; no teleport: a gate is walked
          const ax = G.x + sn * 7 * side, az = G.z + cn * 7 * side, bx = G.x - sn * 7 * side, bz = G.z - cn * 7 * side;
          if (!st.gateIn) { if (goTo(ax, az, 1.2, true, true)) st.gateIn = 1; return ''; }
          goTo(bx, bz, 1.0, false, false); return ''; }
        case 'flag': { if (T) { goTo(T.x, T.z, 2.5, true, true); return ''; }
          if (s.flag === 'inTown' && S.ISLE.rect) { const R = S.ISLE.rect, tx = Math.min(Math.max(P.x, R[0] + 8), R[1] - 8), tz = Math.min(Math.max(P.z, R[2] + 8), R[3] - 8); goTo(tx, tz, 1, true, true); return ''; }
          return 'flag: no driver for ' + s.flag; }
      }
      return 'no driver for step type ' + s.type;
    };
    window.__drive = n => {
      const out = { frames: 0, err: null, why: '' };
      for (let i = 0; i < n; i++) {
        const k = stepKey(); if (k !== st.key) { stickOff(); Object.assign(st, { key: k, t: 0, best: 1e9, bestT: 0, walked: 0, tele: 0, blowT: -9, talkT: -9, holdT: 0, gateIn: 0, log: [], side: 0, sideT: -9, sides: 0, walls: 0 }); st.px = S.player.pos.x; st.pz = S.player.pos.z; }
        const why = policy(); if (why) out.why = why;
        window.__clock.t += window.__clock.dt;
        try { S.frameBody(); } catch (e) { out.err = String(e && e.stack || e).split('\n').slice(0, 2).join(' | '); break; }
        const P = S.player.pos; st.walked += Math.hypot(P.x - st.px, P.z - st.pz); st.px = P.x; st.pz = P.z; st.t += window.__clock.dt / 1000; out.frames++;
      }
      const q = S.quest.cur, s = q && q.steps[S.quest.step], P = S.player.pos;
      return Object.assign(out, { key: stepKey(), type: s ? s.type : '', text: s ? s.text : '', t: st.t, walked: st.walked, tele: st.tele, sides: st.sides, walls: st.walls, log: st.log.slice(-6), pos: [P.x, P.y, P.z].map(v => +v.toFixed(1)),
        form: S.player.mphK ? S.mphName(S.player.mphK) : 'zap', forms: S.SAVE.forms.slice(), ch: S.SAVE.ch, done: Object.keys(S.SAVE.flags).filter(f => f.startsWith('qdone:')), crashes: window.__crashes || [], sampT: st.holdT });
    };
  }, { STUCK });

  for (const CH of CHAPTERS) {
    // the chapter has to be the one the save is in: the shipped `questPick` chooses it, the tool only checks
    let r = await page.evaluate(n => window.__drive(n), 2);
    if (!r.key.startsWith(CH + '.')) {
      // a later chapter asked for: the save is moved to it the way GOD's chapter buttons do (progChapter + inTown), then the
      // shipped picker is let choose again; the chapter's own quest id has to exist
      const ok = await page.evaluate(ch => { const S = window.__play, q = S.QUESTS.find(x => x.id === ch); if (!q) return 'no quest ' + ch; if (q.ch === undefined) return 'quest ' + ch + ' has no chapter';
        S.quest.cur = null; if (S.SAVE.ch !== q.ch) { S.SAVE.ch = q.ch; S.progFlag('inTown', q.ch >= 1 ? 1 : 0); } return ''; }, CH);
      if (ok) { console.log('BAD  ' + CH + ' ' + ok); code = 1; continue; }
      r = await page.evaluate(n => window.__drive(n), 2);
      if (!r.key.startsWith(CH + '.')) { console.log(`BAD  ${CH} the shipped picker chose '${r.key}' instead (chapter ${r.ch}, done: ${r.done.join(' ') || '-'})`); code = 1; continue; }
    }
    let cur = r.key, bad = 0, steps = 0;
    const row = (ok, R, extra) => console.log((ok ? 'ok   ' : 'BAD  ') + R.key.padEnd(8) + R.type.padEnd(7) + `'${R.text}'`.padEnd(58) + ` ${R.t.toFixed(1)} s, walked ${R.walked.toFixed(0)} m` + (R.sides ? `, ${R.sides} side-steps` : '') + (R.walls ? `, off a wall x${R.walls}f` : '') + (R.tele ? `, TELEPORTED x${R.tele}` : '') + (extra ? '  ' + extra : ''));
    for (;;) {
      const R = await page.evaluate(n => window.__drive(n), Math.round(FPS / 2));
      if (R.err || R.crashes.length) { row(false, R, 'FRAME ERROR ' + (R.err || R.crashes[0])); bad++; code = 1; break; }
      if (R.key !== cur) {
        // the previous step passed (the shipped test advanced the quest); its row is the state as it left it
        row(true, Object.assign({}, R, { key: cur, type: lastR.type, text: lastR.text, t: lastR.t, walked: lastR.walked, tele: lastR.tele, sides: lastR.sides, walls: lastR.walls }), lastR.log.filter(l => /TELEPORT|blow|talk/.test(l)).join(' ') || '');
        steps++; cur = R.key;
        if (!R.key.startsWith(CH + '.')) break;      // the chapter ended (or another quest took over)
      }
      if (R.t > BUDGET) { row(false, R, `NOT PASSED in ${BUDGET} s` + (R.why ? ' -- ' + R.why : '') + (R.log.length ? ' | ' + R.log.join(' ') : '') + ` | at ${R.pos} as ${R.form}`); bad++; code = 1; break; }
      var lastR = R;
    }
    const fin = await page.evaluate(() => { const S = window.__play; return { done: Object.keys(S.SAVE.flags).filter(f => f.startsWith('qdone:')), ch: S.SAVE.ch, forms: S.SAVE.forms.slice(), inTown: !!S.SAVE.flags.inTown }; });
    const ended = fin.done.includes('qdone:' + CH);
    console.log((ended && !bad ? 'ok   ' : 'BAD  ') + `${CH} ${ended ? 'COMPLETE' : 'NOT COMPLETE'}: ${steps} steps passed` + (bad ? `, ${bad} failed` : '') + ` | chapter ${fin.ch}, forms [${fin.forms.join(' ')}], inTown ${fin.inTown ? 1 : 0}, done [${fin.done.map(d => d.slice(6)).join(' ')}]  ${el()}`);
    if (!ended) code = 1;
  }
} catch (e) { console.log('BAD  play: ' + String(e && e.message || e).split('\n')[0]); code = 1; }
if (errs.length) console.log('page: ' + errs.slice(0, 6).join(' | '));
await browser.close(); server.close();
process.exit(code);
