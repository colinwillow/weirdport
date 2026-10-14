# ROADMAP — the loop's work list

**This file steers the autonomous loop.** It is re-read at the start of every pass. Edit it from
the GitHub app on your phone and the next pass follows the edit:

- **reorder** items to change what comes next;
- write a line under **STEER** to interrupt (e.g. "stop the map, the cops shooting feels wrong");
- delete an item to cancel it.

The loop takes the **first unchecked item**, ships it as one build (bump, check, push to main),
then ticks it with the build number. One item per pass, so passes are short and your messages land
between them. Design context lives in `GAME_DESIGN.md`.

## STEER

<!-- write here; the loop reads this first and obeys it over everything below -->

**NEXT, BEFORE ANY OTHER FARM PASS — THE FARM IS THE WRONG SIZE AND IN THE WRONG PLACE. REBUILD IT AS
OPEN COUNTRYSIDE ACROSS THE RIVER.** Colin finally walked it (m302-m304) and said: *"it's like 12 feet
away from the border of the city... a very small city block tacked onto the edge of the city... the
border between the city and the farm is just a line, it's not organic at all. I want it to be farmland:
fields, meadows, cows, tractors, farmers, trees, buildings, ridges... exactly not what I meant."* This is
our fault, not the loop's: the docs said "intimate, empty ground is a failure" and "SMALL and DENSE: a few
blocks". Both are rewritten now. **Read the new "Scale follows the place" and "No borders that are lines"
rules in `GAME_DESIGN.md` and the new Gristle Farm entry in `REGIONS.md` before starting.**

What to build (several builds; ship each step, never wait):
1. **A separate farm landmass across a river from the city island**, not a lobe on the city's coast.
   Roughly 400 x 300 m or more, at an authored bearing, far enough that the city is a SKYLINE on the
   horizon from the crash site. One river/channel between them, crossed by the checkpoint bridge (move
   `BRIDGE` there). Fog `far` and the sky must let the skyline read from the farm. **— done m306** (the land,
   its water, the channel bridge, the long view; the old pieces came along as one cluster round the yard).
2. **Rolling terrain**: a heightfield with low ridges and hills, a creek valley with a footbridge, a pond.
   Walkable through the real collider (`groundAt`), chunked so the camera culls what is behind it.
3. **Fields that follow the land**: irregular patches of wheat, corn, ploughed earth, hay meadow and
   pasture, divided by hedgerows, fences, tree lines and dirt tracks. Nothing square to the world grid.
4. **Spread the existing pieces out into clusters** (reuse m288-m304, do not throw them away): the
   farmhouse and yard, the barn and silo, sheds and coop, a neighbour's farm on another ridge, a lone hay
   barn. **The crash site far out in a field**, a long gouge through the wheat, the crop circle near it.
5. **Life**: herds of cows in the pastures, a tractor working a field and one parked, farmhands in the
   fields, a pickup on the track.
6. **The transition into town, never a line**: dirt track -> country road -> past the neighbour's farm
   -> an edge-of-town strip on the farm's side of the river (gas station, trailer park, a few houses with
   yards, billboards, power poles, a fruit stand) -> the bridge checkpoint -> across it the city starts
   thin (low houses, lots, a warehouse) and thickens. Also soften the city island's own edge the same way
   (scattered houses, yards, fences, trees on the ring) so the kit city doesn't end at a ruler line.
7. **Phone cost**: instance everything repeated (trees, fence posts, bales, cows, crop stalks), merge
   per material, chunk the terrain, and keep draw calls in the tens. Distance fades the small stuff.
7b. **More than one way from the farm to town** (the new "connective tissue" rules in `REGIONS.md`): the
   bridge checkpoint is the main route the tutorial teaches, but also build a creek culvert under the
   road, an old rail trestle over the river, a shallow ford downstream with cows drinking, and a way
   through backyards and fence gaps on the town edge. Early on, block or hide the extras (a grate,
   broken planks, a dog in the yard) so the checkpoint still teaches; they open later with forms or
   Clancy. Each route bends, crosses over or under another one, and has something on it.
8. **Prove it**: `npm run places` passes with every GOD farm place moving him onto the new land, and the
   crash spawn landing at the wreck. **Screenshots allowed and wanted** for this work: a wide shot from a
   ridge showing fields, buildings and the distant skyline, and one of the road through the transition.
   Paste the `places` output in NOTES.


**URGENT, NEXT BUILD — THE FARM DOES NOT EXIST IN THE REAL GAME.** Colin opened every GOD place and
none of them work. Measured with `npm run places` (new; builds the REAL kit city collider and island,
runs every farm builder, then the shipped `godPlace`): the widest grass on the island ring is
**14.9 m**, `buildFarm` needs 18, so it returns early with `FARM NO ROOM 15` and `FARM.at` stays null.
Crash, lane, bridge, cows, flora and props all hang off `FARM.at`, so NONE of m288 to m300 is in his
game, and every farm place in the GOD menu does nothing. (The CHAPTER buttons only set the chapter
flag; they move nothing, which is also confusing. Make each one take him to where that chapter starts.)
Fix:
1. Give the farm the ground it needs: grow the island out into a farm peninsula at an authored
   bearing (a lobe on the waterline in `buildIsle`, wide and deep enough for the yard, the fields
   down to the shore, the lane, the creek and the road to the bridge), and place the farm on it.
   Do not just lower the 18 m threshold: 15 m of grass cannot hold a farm.
2. Prove it with `npm run places`: `FARM.at` and `CRASH.at` non-null, and every GOD place in `tkit`
   moving the player somewhere sensible. **From now on run `npm run places` before pushing any build
   that adds or moves a place, and paste its result in the build's NOTES entry.** A place that only
   exists in a fabricated test does not exist.
3. A builder that bails out must say so loudly: show a red toast at boot for any `... NO ROOM` /
   `... FAIL` note while GOD mode is on, not only a token in the chip. **— done m302.**

**TOP PRIORITY, BEFORE THE NEXT FARM PASS — GOD MODE (Colin can't see anything you've built).**
He can't find the farm, any new place, or Rollergirl: the world key only cycles the old worlds, the
form wheel only offers sampled forms, and new things are only reachable through play. Build a
**PLAY / GOD** switch: a key in the top-left gutter with the world key, remembered in storage, plus
`?god` in the URL. In GOD mode:
- **Places menu:** every authored place in every world, by name (the farmyard, the crash site, the
  creek, the bridge checkpoint, Old Town, each portal, each quest giver…). Tapping one takes him
  there, switching world if needed. It's a list, so a place added later is one line.
- **Every form unlocked** in the form wheel, including Rollergirl and every character on the
  roster; infinite juice.
- **Every weapon and mode**, including the DNA gun.
- **Fly:** a free-flight toggle (stick moves, a second control rises and sinks, nothing collides)
  to explore and look at things.
- **No heat, no damage.**
- **The whole map revealed**; tap anywhere on the full map to teleport there.
- **Chapter controls:** start a new game at the crash, jump to any chapter, reset the save.
- The chip says **GOD** while it's on.
PLAY mode is the game as it plays now. Ship this as the next build, then carry on with the farm. **— done m298.**

**Standing rule from now on:** anything you build must be reachable from GOD mode in the same build
(a new place goes in the Places menu, a new form in the wheel, a new system gets a toggle). If he
can't get to it, it isn't done.

**From Colin (updated, replaces the earlier STEER): keep going, never wait.**

- **Never stop or wait for Colin.** If something seems to need him, make the call, log it under
  "Decisions for Colin", and carry on. (The earlier STEER said to pause until he had looked at the
  farm; that was wrong and is withdrawn.)
- **There is no Blender work for about a week.** Places are built in code until then. `MARKERS.md`
  can wait; do not build anything that depends on his markers.
- **The placement rule stays:** nothing goes in the world as a "demo", "near the spawn" or
  "somewhere open". Everything placed comes from an authored placement table: a named spot in a
  named place, and a one-line reason it is there. (Done: m292 took the demo gates and portals out.)
- **Now: polish passes on the farm until it is beautiful.** One pass per build, as many passes as it
  takes; ten is fine. Each pass, pick the weakest-looking thing about the farm and make it better:
  the light and atmosphere (golden hour, haze, long shadows), the materials and colours (painted, not
  flat greybox; `REGIONS.md`'s farm palette), detail density (crops, grass tufts, fences, clutter,
  tools, hay), silhouettes and rooflines, layering and foreground, the wreck as a hero moment. Keep
  the draw-call budget in mind (merge what does not move).
- **You may build a screenshot tool for these passes** (`tools/shot.mjs`, headless Chromium from
  `/opt/pw-browsers`, the player's camera at a named spot) so you can see the farm before and after
  each pass, instead of polishing blind. If a shot takes more than about two minutes or will not
  render, drop it and carry on without it.
- **After the farm looks right:** B1e, then B2, then on down the list.

## Standing rules for anything built in the world

- **Connective tissue:** between any two regions, build several irregular routes of different kinds
  (water, crossings, over and under, open ground), never a single road and never a straight border.
  Read "The connective tissue" in `REGIONS.md`.

Read `GAME_DESIGN.md` → "The world: dense, vertical, organic, alive" before building any place.
**Intimate, vertical, organic, interactive, and one place finished at a time.** Never a flat plane
with spaced-out rectangles on it, never a grid of separate areas. Build small and finish it.
**Before building in a region, read its entry in `REGIONS.md`** and check it against the "what has to
differ" table there, so no region feels like the last one.

## Phase A — the game skeleton (no new art needed)

- [x] m276 **A1 Progress & save.** A new `localStorage` key `mel.prog`: chapter, forms unlocked, regions
  revealed, quest flags, portals activated, juice. `?fresh` already clears keys — make it clear this one too. Chip shows `CH<n>`.
- [x] m277 **A2 Talk.** NPCs can carry a `talk` script: walk up, the right pad lights (the existing
  interact pattern), tap → speech bubble with name + lines, tap to advance. A `!` marker over the
  head of anyone with something to say.
- [x] m278 **A3 Quests & objectives.** Data-driven quests: steps of type talk / go-to / sample / defeat /
  reach / gate. Current objective as one line on the HUD, a waypoint beam in the world, and a
  "quest complete" moment.
- [x] m279 **A4 Fear & witnesses.** Humans who SEE you undisguised react: scream, flee, phone it in.
  Disguised you are ignored. A witness who phones it in raises heat.
- [x] m281 **A5 Heat & police.** Wanted stars. 1 = cops come look, 2 = cops chase and arrest-attempt,
  3 = cops shoot, 4 = more cops (military later). Lose heat by breaking line of sight and changing
  form. Chip shows the stars.
  - [x] m280 **A5a** stars, heat rules (calls, spotting, blows; cools out of sight, faster in a human form), cops come look (1) and chase + arrest-grab (2).
  - [x] m281 **A5b** cops draw and shoot at 3 stars (`draw_weapon`, `shoot_pistol` are in his file), more cops arrive at 4.
- [x] m282 **A6 The sampler.** Stand over a downed human and hold to take a sample → that form is
  unlocked into the form wheel (the existing disguise pipeline). DNA gun becomes debug-only
  (`mel.dna()` or a debug toggle).
- [x] m283 **A7 Form wheel.** Pick any unlocked form from a wheel (or cycle). Your own form is always
  there. The current form's abilities are what the gates check.
- [x] m284 **A7b Juice.** The DNA tool's juice meter on the HUD. Transforming costs juice, wearing a form
  drains it, and at zero you snap back to the alien. Juice comes from small tasks, helping people and
  beating Skinsuits. All rates are tunables on the settings panel, so he can feel them out.
- [x] m285 **A8 Gates.** Data-driven obstacles that check the current form: police cordon (cop),
  fire wall (firefighter), broken bridge (worker repairs it), barricade (activist inside a protest
  crowd), gap (glider). Each says what it needs when you bump into it.
- [x] m286 **A8b Portals.** Activatable portal points (a glowing pad). Stepping on one activates it for
  good; from any active portal you can travel to any other as yourself. The ship is the hub. Every
  place a form can reach gets one, so a disguise running out never strands you.
- [x] m287 **A9 Map & fog.** A full-screen map (tap the minimap) showing regions; unvisited regions are
  fogged and reveal when entered; the objective and quest givers are marked.

## Phase B — Chapter 0 and Chapter 1, playable start to finish

- [ ] **B1 The farm.** Farmland on the island ring around the kit city — small, close and layered,
  not a flat field: a sunken lane between hedges, the barn with a hayloft you can climb, a silo, a
  creek with a footbridge, the road climbing to a bridge into town. Cows as placeholders (boxes or an existing body) that moo and
  wander. The crash site: a wreck, smoke, Clancy inside.
  - [x] m288 **B1a The farmyard** — barn on a plinth, hay-bale stair to the hayloft, loft door over a hay stack, lean-to whose roof you reach off crates, walkable barn roof, silo, split-rail paddock, round bales, trough.
  - [x] m289 **B1b The crash site** — the wreck, scorched ground, smoke, Clancy inside; where Chapter 0 starts.
  - [x] m290 **B1c The sunken lane and the creek** — a lane cut below the fields between hedges, a creek with a footbridge.
  - [x] m291 **B1d The road and the bridge** — the road climbing from the farm to a bridge into town (split: the cows are B1d2).
  - [x] m294 **B1d2 The cows** — cows that moo and wander the farm.
  - [ ] **B1e From REGIONS.md's Gristle Farm entry, not in m288** — a rope down from the hayloft, the silo ladder made climbable, an orchard terrace, and cows that panic and stampede (its signature system).
- [ ] **B1f Direction and discovery** (see the new section in `GAME_DESIGN.md`). Build on m278's quests:
  - a **"New task" card** when a task unlocks, and a **task list** you can open;
  - the waypoint in the world shows the **distance** in metres, and the map marker matches it;
  - **rumours**: lines that add an entry to a rumour list with no marker (or a rough circle), resolved
    when you find the thing;
  - **who talks to whom**: each speaker has a list of forms it talks to properly, forms it
    cold-shoulders (a short brush-off line), and the alien makes it flee. A task can require a form
    to start ("only talks to farmhands"). Keep the lines light and funny, never mean.
  - Chapter 0 uses it: the farmer's family brush off the alien; as the farmer, a neighbour at the
    farm shop gives you the bridge task (marker + waypoint) and a rumour about the man at the top of
    the hill (no marker).
- [ ] **B2 Chapter 0 script.** Crash → find Clancy → the farmer sees you and panics → knock him
  down → take his sample → walk to the bridge as him → the cop checkpoint lets the farmer through
  (and stops the alien) → Old Town, fog lifts. Tutorial prompts along the way.
- [ ] **B3 Old Town setup.** Region bounds, a homeless camp, a food cart with the hidden good
  alien (the tell under the hat), a building site. Ambient life placed by role.
- [ ] **B4 Chapter 1 quests.** The good alien points you at the building site; workers are being
  turned into Skinsuits; get the worker form; repair the broken bridge (gate) to the next district.
- [ ] **B5 Chapter 1 boss.** The infiltrated foreman bursts out of his skin; beat him; revert the
  crew; chapter complete → Chapter 2 region unlocks on the map.

## Phase C — systems the later chapters need

- [ ] **C0 District health.** Each district has a health the city's systems push up and down:
  damage, fires and Skinsuits lower it; crews and firefighters raise it. A strike stops the crews and
  the district decays (boarded windows, rubble, squatters); ending it sends them back out. The look
  follows the health. Start with Old Town and the existing worker/repair and fire systems.
- [ ] **C1 Protest events.** Activists gather with signs and chant; rednecks show up; it turns into
  a brawl if provoked; cops respond. As an activist you can walk inside the crowd through a barricade.
- [ ] **C2 Skinsuit incursions.** An enemy ship/agent turns civilians on the street; you fight and
  revert them. Ties to the existing virus system.
- [ ] **C2b The orbs (`LORE.md`).** Start with the pacifier: an orb floating over a few Old Town
  blocks, a trance on the people under it (they stare and walk in slow loops), the blaster can shoot
  it down, and they come out of it dazed. Lights flicker and cars stall near it (the
  electromagnetic tell). Then the watcher and the amplifier, which feeds the protests and brawls.
- [ ] **C2c Placeholder roster (`CHARACTERS.md`).** Build against ROLES, not models: a roster table of
  every role the regions need, each mapped to a stand-in (existing body + tint + prop + name tag).
  When his model for a role lands it is one line. GOD mode lists every role and spawns one.
- [ ] **C2d Smart objects.** Benches, café tables, bus stops, food carts and counters carry use spots
  (where to stand or sit, which way to face, which clip). NPCs nearby walk to one, use it for a while,
  and leave. Missing clips fall back to an idle and the chip names the clip, so his animations drop in
  with no code change. Start in Old Town.
- [ ] **C3 Uplift cyborgs.** A cyborg variant of a worker (placeholder tint/parts until his models
  land) with its own behaviour.
- [ ] **C4 The glider.** The hang-glider guy at a lookout; his form flies (reuse her wingsuit flight).
- [ ] **C5 Hidden good aliens.** A network of disguised shopkeepers who give tips and upgrades.
- [ ] **C6 Chapter 2 greybox (The Pearl)** with its quests and boss — then 3, 4…

## Phase D — turf (after Phase C; see "Turf" in GAME_DESIGN.md)

- [ ] **D1 Influence model.** Per-block shares for each faction, saved with progress; a map overlay
  and a chip token showing who holds the block you're in.
- [ ] **D2 The crowd follows influence.** The NPC mix in a block comes from its shares.
- [ ] **D3 Faction dressing.** Each faction's set of props, signs, paint and decay on existing
  buildings, cross-fading as a block changes hands.
- [ ] **D4 Faction buildings.** Kit-generated building styles per faction, swapped in when a block
  changes hands for good.
- [ ] **D5 Pressure.** Factions push at their borders on their own (flashpoint events), and the
  player's actions move the shares.

## Phase E — side quests (see "Side quests from UFO pop culture" in LORE.md)

- [ ] **E1 Element 115.** The jittery ex-lab tech (stand-in body), hidden somewhere in Old Town; earn his
  trust, learn where the 115 is, fetch it; it upgrades the juice tank. The first side quest, and the
  template for the rest.
- [ ] **E2 The late-night radio host.** A voice on car radios that reacts to what you've done and
  points at sightings; a side-quest hub.

## Ongoing (fill gaps between items, never instead of them)

- Bugs he reports always jump the queue.
- Keep `npm run check` green; never ship a blank page.

## Done

<!-- the loop moves ticked items here with their build number -->

## Decisions for Colin

- **m276 (A1):** `?fresh` did not exist yet, so I built it: it wipes **every** `mel.*` key (tuning,
  resolution, chip fold, world pick and the save), not just the save, then removes itself from the
  URL so the world key's reload cannot wipe it again. `mel.progReset()` in the console resets only
  the save. Juice starts at 0; A7b decides the tank. The object in code is `SAVE` (the name `PROG`
  was taken by the boot loader); the storage key is `mel.prog` as asked.
- **m277 (A2):** there was no existing "pad lights" interact pattern, so talk lights the right
  pad's ring **sky blue** (the trigger is amber) and its label says `tap = talk`. The **left** tap
  still jumps while someone is in reach. One speaker per character type for now (Dusty the hobo,
  Earl, Sal the worker, Moonbeam, Sage, Knuckles, Jasper, Capt. Reyes) with placeholder lines I
  wrote — rewrite them in `TALKS`. Speakers don't stop or turn to face you yet.
- **m278 (A3):** a stand-in first quest, **WEIRDPORT 101**: talk to someone with a `!`, knock
  somebody down, get 3 m up. It runs in every world until done, so the objective line, the beam
  and the "quest complete" card can be seen now; B2's Chapter 0 script replaces it. The objective
  sits top-centre (the only empty edge). `sample` and `gate` steps read the save, so they will
  start working when A6/A8 write it. `mel.progReset()` replays it.
- **m279 (A4):** people with an unheard `!` are brave and don't run (otherwise you can't talk to
  them undisguised); once heard they're as scared as anyone. Disguised as an *alien* kind (the
  warrior, her) still counts as alien. Cops and the construction worker don't panic. About 45% of
  witnesses phone it in (`FEAR.callP`). There is no scream sound in the repo, so those with a
  voice grunt high and the rest are silent: a scream recording would slot straight in.
- **m280 (A5a):** A5 split in two. Heat is one number and the stars are thresholds on it
  (1 / 2.5 / 4.5 / 7). A cop who **sees** the alien jumps it straight to 2 stars (chase). Phone
  calls add 1, hitting a cop 1.2, hitting a civilian 0.3. It cools only after 6 s with no cop
  seeing you, and 4x faster while you're in a human form. "Arrest" is a grab that hurts and
  staggers (there's no arrest animation); there's no jail/busted screen. The officer walk/run
  speeds are guesses. Side effect: the officer now has walk/run clips, so he may become a DNA form.
- **m281 (A5b):** at 3 stars a cop who sees you within 18 m stops, draws and shoots (7 damage,
  ~60% hit point blank down to ~18% at range, halved-ish while you move fast; a dodge roll always
  makes him miss). At 4 stars an extra officer turns up behind you every 6 s, up to 3; they leave
  after 12 s with no stars. Gun sound is the blaster pitched down (there's no pistol recording).
- **m282 (A6):** the sample gesture is **hold the right pad still** over a downed human (it
  replaces the backflip duck only while one is in reach); the pad ring goes green and a ring fills
  over him in 1.1 s. He stays down while you hold. Taking a sample unlocks the form **and puts it
  on at once** (until A7's wheel exists there's no other way to wear it). Officers can be sampled.
  The DNA gun mode is gone from the blaster unless you open the game with `?dna`; `mel.dna('hick')`
  still works in the console.
- **m283 (A7):** a single green **FORMS** button on a third ring above the left stick (appears
  once you have a second form) opens a round picker over the screen; tap a form to become it, tap
  outside to close. The game does not pause while it's open. A form whose character isn't loaded
  in the current world shows greyed out. Desktop: `F`. The old REVERT button is still there too.
- **m284 (A7b):** tank 100, a transform costs 20, wearing a form drains 0.4/s (about 3.5 minutes
  from full), going back to Zap is free. A new game starts **full** so the first sample is
  wearable. Earned: quest step +15, quest done +30, first time hearing someone out +6, knocking
  down a Skinsuit +20. The meter is a thin green bar above the health bar. All six numbers are on
  the tune panel under **JUICE**. "Helping people" means talking for now; real favours come later.
- **m285 (A8):** all five gate types exist as data (cordon=cop, fire=firefighter,
  barricade=activist, gap=glider: walk through in that form; bridge=worker: lean on it for 2 s and
  it's mended for good). No level has one yet, so two **demo gates** (a police cordon ~9 m and a
  fire wall ~14 m from where you spawn) are placed on open ground so you can try them; you can walk
  around them, they're tests, not level design. The gap can't be crossed until the glider form
  exists (C4). Gates only stop **you**; NPCs walk through. `mel.gate('bridge')` drops one in front
  of you.
- **m286 (A8b):** pads are violet rings on the ground; step on one to activate it for good. Standing
  on an active pad, the right pad lights violet (`tap = travel`) and opens a picker of the other
  active pads in this world. You can travel in any form. There's no ship model yet, so "THE SHIP"
  hub is a pad a few metres from the spawn (always active), plus two demo pads ~30 m out; Phase B
  places the real ones. Travel stays within one world (worlds are separate loads).
- **m287 (A9):** there was no minimap, so I built one: round, top-right under the stars, turns
  with the camera. Tap it for the full map (north-up), tap again to close; `M` on desktop. The map
  is drawn from the collision boxes (building footprints shaded by height), not a rendered photo,
  so it's cheap and always matches what you can walk into. **Regions are placeholder quadrants**
  (NORTH-WEST etc.) until Phase B defines real districts (`MAPREG`); the one you spawn in starts
  revealed. Markers: you, the objective (gold), `!` quest givers, portals, gates.
- **m288 (B1a):** the farm goes on the **widest stretch of grass on the island ring** (measured
  from the island's own coastline, so it moves if the coast changes), turned ~12° off square. B1
  was split into four builds (yard, crash site, lane + creek, road + bridge + cows). Greybox
  colours, merged so the whole yard is about 8 draw calls. Head inside the barn, climb the bales
  to the loft, drop out of the loft door; or crates → lean-to roof → barn roof. `mel.farm()` takes
  you there.
- **m288 note:** `REGIONS.md` landed while m288 was building. Its Gristle Farm entry asks for a
  rope down from the loft, a climbable silo ladder and an orchard terrace that m288 does not have
  (the silo ladder is only drawn), so I split them out as **B1e**.
- **m289 (B1b):** **a new game now starts at the crash** — beside the burning wreck in the field
  next to the farmyard, Clancy at the hatch. Once you walk into the city, every later boot starts
  in town as before (`?spawn=city` / `?spawn=crash` overrule it for one load; `mel.progReset()`
  makes you a new game again). The crowd stays in town, so the farm is quiet until B1d's cows and
  B2's farmer. The wreck is a greybox saucer: tipped nose-down, a real fire that never goes out,
  dark smoke, a purple scorch down the furrow, and you can climb onto it off the berm. The demo
  gates and portals from m285/m286 are placed round wherever you spawn, so on a new game they're
  at the farm.
- **m290 (B1c):** the lane is "sunken" by its **banks** (1.9 m earth banks with hedges on top)
  rather than by digging into the island's ground, which would mean rebuilding the coastline. You
  can walk along the bank tops above the lane. The creek runs out of a culvert at the city edge down
  to the beach in a stone-sided gully; it **fords** the lane, and a footbridge carries the bank-top
  path over the ford. Openings in the bank at the barn doors and toward the crash field.
  `mel.lane()` / `mel.lane(1)` (the ford). The water is a plain glossy strip for now, not the
  island's sea shader.
- **m291 (B1d):** the island had no river, so the bridge brings one: an 8 m river between 3 m
  stone levees runs from an outfall under the city edge down to the beach, past the crash field.
  **You can't wade it** — drop into the channel and the current puts you back on the bank. The
  road climbs a two-ramp hairpin to the bridge deck and a ramp brings you down the town side. A
  guard booth and barrier arm sit at the town end (B2 turns it into the real checkpoint gate). If
  the side past the crash field doesn't have 30 m of grass, the whole thing mirrors to the far side
  of the farm. **The farm isn't sealed yet**: you can still walk round the island ring into town the
  long way; B2 decides whether to close that off. `mel.bridge()` puts you on the deck.
- **m292 (STEER 1):** `GATE.demo` and `PORTAL.demo` are 0; nothing is placed by the spawn any more.
  `mel.gateDemo()` / `mel.portalDemo()` place them round you on purpose. **The cows** (B1d2) were
  built just before your STEER landed; per point 4 they are **not on main**. They're parked on the
  branch `paused/cows-m292` (six greybox cows, one draw call, a synthesized moo), ready to merge if
  you want the farm to continue. Still placed without an authored marker, and next in line under
  point 2/3: the `!` talk speakers (one random body per kind), the WEIRDPORT 101 stand-in quest, and
  the crash-site spawn on a new game. The marker loader (point 3) is where those get proper places.
- **m293 (STEER 2/3):** `MARKERS.md` is the vocabulary. **Live now**: `portal_*`, `gate_<type>_*`,
  `npc_<kind>_*` (with `name`, `talk` or `lines`), `spawn_start`, `region_*` (Cube empties, they
  replace the placeholder map quadrants), `goal_*` for quests. **Read but not acted on yet**:
  `crowd_*`, `protest_*`, `ambient_*` (C1). Your buildings file already has markers the game never
  read: `police_stand` ×60, `police_spawn`, `police_car_park`, `firemen_spawn`, `fire_truck_home`,
  `door_in/out`, `ladder_bottom`. They're listed as unread in MARKERS.md. Per STEER 2 the random `!`
  speakers and the WEIRDPORT 101 stand-in quest are now **dormant**: speakers come from `npc_*`
  markers, and `mel.questOn('q0')` runs the stand-in. Your files have none of the new marker types
  yet, so until you place some, nothing new appears: that's the point.
- **m293 vs the new STEER:** m293 (`MARKERS.md` + the marker loader) was built under the earlier
  STEER and landed as the new one arrived. It changes nothing in the world until markers exist, so
  it stays, and it needs no Blender work this week. The dormant `!` speakers and stand-in quest also
  stay dormant under the placement rule; they come back via an authored placement table when a place
  needs them. **The cows** (built m292, parked on `paused/cows-m292` when the farm was paused) come
  back now that the pause is withdrawn: they're the first farm pass.
- **m294 (B1d2, farm pass 1):** six greybox **box cows** (Holstein, Hereford, Angus, Jersey coats) until you
  make real ones: three in the paddock behind the barn, three in the field by the crash. They graze
  head-down, look about, wander, come into the sunken lane through its openings, block you, and
  shy away at a trot if you run past close. **The moo is synthesized** (no cow sound in the repo):
  if it sounds wrong, a recording in `audio/` would replace it in one line. `mel.moo()` makes the
  nearest one moo. They're white dots on the minimap. Panic/stampede is B1e.
- **m295 (farm pass 2: light):** the farm now has its own **golden hour**: warm amber sun, a warm sky
  fill and earth bounce, and a gold haze that pulls in closer, so from the fields the city sinks into
  a far golden distance. It blends in as you approach the farm and fades out over the first 14 m into
  town, never a hard switch. Colours only. The sun's **angle** (long shadows) is unchanged, because
  moving it re-bakes the sky. `mel.GRADE.on = 0` is the A/B; the colours are live on `mel.GRADE`.
  **The screenshot tool didn't work**: software WebGL can't render one kit-city frame inside
  Playwright's 30 s limit, so per the STEER I dropped it and these passes stay unseen until you look.
- **m296 (farm pass 3: paint):** the farm's flat greybox colours are now **painted in the shader**
  (no textures, no extra draw calls): the barn and timber are vertical boards with dark seams, a
  slightly different tone per board and red paint worn through to grey wood in patches; the stone
  is coursed blocks with lighter mortar; the roofs have standing seams with rust bleeding down; hay
  is fibrous, the earth clumpy, the hedges blotchy, the metal streaked. It covers the barn, crash
  site, lane and bridge. The cows are separate and unchanged. `mel.FPAINT.on = 0` then reload is the
  flat A/B.
- **m297 (farm pass 4: growth):** the bare fields now grow things, all from an authored table with
  a reason each: a **corn patch** (2.2 m, cover to slip through) between the yard and the crash
  field, a **golden wheat field** behind the paddock running down to the shore, and **~500 grass
  tufts** that grow only where a mower can't reach (against walls, posts, banks and bales). It all
  sways in the wind and **parts round you** as you walk through. The corn hides you visually but
  doesn't block sight for the fear/cop systems yet. One draw call for all of it; tune with
  `mel.FLORA.wind`, `push`, `pushK`.
- **m298 (GOD mode):** the **PLAY/GOD key** sits top-left under the build number and stays visible
  even when the chip is folded (the world key hides then). Tap it for GOD; `MENU` opens the places
  list (this world first, other worlds reload into the place), the chapter controls (new game at the
  crash, chapters 0–6, wipe the save) and switches (fly, the stand-in quest, the demo gates and
  portals). `FLY`: left stick moves, the two yellow buttons over the right stick rise and sink,
  nothing collides. In GOD: every character in the form wheel (Rollergirl included, if she's loaded
  in this world), infinite juice, the DNA gun back on the blaster, no heat, no damage, the whole map
  revealed, and **tapping the full map teleports you there** (onto the highest surface: a roof if
  it's a building). `?god` / `?god=0` in the URL set it too. The menu scrolls by dragging, and a
  button acts on release so a scroll never fires one. **Every farm place from m288–m297 is in the
  list.**
- **m299 (farm pass 5: silhouette & clutter):** the barn now has a **cupola with a weathervane** on
  its ridge and a **hay hood with a hook beam** over the loft door; a 9 m **windmill pump** stands
  in the paddock by the trough, its wheel spinning and turning into the same wind the crops lean in
  (the vane agrees); a **scarecrow** in the corn; a red **tractor** parked in the yard by the lane
  gate; barrels against the lean-to; a wheelbarrow of hay by the stack. All from an authored table
  with a reason each. GOD's places list gained the windmill, the scarecrow and the tractor.
- **m300 (farm pass 6: the wreck):** the crash is now a hero moment: the saucer's **core pulses
  violet** like a heartbeat, a **pool of violet light** lies on the field round it pulsing in step
  (faked with a ground-hugging glow, not a real light, so the city pays nothing for it), a faint
  **violet beam** climbs into the sky as a landmark you can see from anywhere on the farm, the hull
  **spits arcs of electric sparks** with a crack (now and then a big discharge), **hull fragments**
  (some still glowing) and violet crystals lie down the furrow, and it **hums**, a low electrical
  drone that swells as you get close. The ten scorch marks were merged into one draw call.
  Tune on `mel.CHERO` (pulse, arcEvery, beamA, poolA, humG).
- **m301 (farm pass 7: the ground):** the farm stood on unbroken grass. Now there is **bare dirt**
  where the barn doors open onto the lane, a **turning patch** in front of the lean-to, **wet mud**
  round the trough and windmill, the **paddock trodden pale**, the gate churned, and a **worn track
  with two cart ruts** down the floor of the sunken lane. Noise-edged, one draw call, from an
  authored table with a reason each.
- **m302 (the farm, for real):** the farm had never been in your game: it needed 18 m of grass
  and the island seemed to have 15. **The 15 was a misreading** (the code looked at the wrong
  sample, a fifth of the way across the grass; the real ring is 38–66 m). Fixed. As the STEER asked,
  the farm still got **its own headland**: the coast bulges out 34 m on the **+x side, under the
  low sun**, so the yard's long shadows fall back toward town and the sea behind the wheat glitters.
  It's in `ISLE.head` if you'd rather it sat elsewhere. **Your next kit-city boot starts at the
  crash** (a chapter-0 save that has never been to town), as a new game should. The CHAPTER buttons
  now take you somewhere: 0 to the crash, 1 to Old Town; 2–6 say "not built" on the button. In
  GOD, a builder that gives up shows a **red bar** at the top; tap it away.
- **m303 (farm pass 8: the headland's fields):** with the farm finally on the island, I measured
  it: half the headland was empty lawn. I made the headland a little smaller (so the wheat really
  runs down to the shore) and turned the rest into **small fields walled by hedgerows**, with
  trees standing in them and a five-bar gate in each: a **hay meadow** with bales (three stacked to
  climb), the **crash field** cut to stubble, a **ploughed potato field** with real furrows, a
  **river meadow** with willows, and a **copse of oaks** at the headland's tip. The creek now runs
  all the way to the beach. All in GOD's places (meadow, plough, copse). If the hedges feel like
  too many walls, `mel.HROW` holds them.
- **m304 (farm pass 9: the farmhouse):** the farm had no house, so nowhere the farmer and his family
  could live. Now a two-storey cream farmhouse stands in the empty plot between the corn and the hay
  meadow, with lit windows, green shutters, a red roof, a smoking chimney, a porch with chairs facing
  the corn and the lane, and washing flapping on a line behind it. Climb the rain barrel onto the
  porch roof to see over the corn to the wreck. It's the natural home for the farmer in B2.
- **m305 (farm pass 10: the way to the bridge):** a worn **road** now carries on from the end of the
  sunken lane, round the wreck, to the foot of the bridge ramp. A **fingerpost** at the lane's end
  points to THE BRIDGE · TOWN one way and GRISTLE FARM the other. There's a **milk-churn stand**
  on the verge and a **cattle grid** across the road at the ramp (the stampede in B1e will stop
  there).
- **Farm polish: stopped at ten passes.** Your new STEER (the farm as open countryside across the
  river) landed while m305 was shipping, so it goes next, ahead of B1e. m288-m305's pieces get
  reused on the new land, as it says.
- **m306 (farm rebuild, step 1):** the farm is now its own landmass across a channel, about
  460 x 340 m of rolling ground 400 m from the city's middle, on the sunset side, so from the farm
  the city is a skyline lit gold from behind you. A 166 m stone bridge on piers crosses the channel,
  with the checkpoint at the town end. Everything built so far (barn, house, fields, lane, crash)
  came along as one cluster round the yard for now; steps 2 to 4 spread it out and send the crash
  far into a field. I put it on bearing .5 (north-east-ish, `FARMLAND.bearing`) and 70 m of water
  away (`FARMLAND.gap`); both are one number if you want it elsewhere.

