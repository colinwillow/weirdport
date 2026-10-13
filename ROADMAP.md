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

## Standing rules for anything built in the world

Read `GAME_DESIGN.md` → "The world: dense, vertical, organic, alive" before building any place.
**Intimate, vertical, organic, interactive, and one place finished at a time.** Never a flat plane
with spaced-out rectangles on it, never a grid of separate areas. Build small and finish it.

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
  - [ ] **B1b The crash site** — the wreck, scorched ground, smoke, Clancy inside; where Chapter 0 starts.
  - [ ] **B1c The sunken lane and the creek** — a lane cut below the fields between hedges, a creek with a footbridge.
  - [ ] **B1d The road and the bridge, and the cows** — the road climbing from the farm to a bridge into town; cows that moo and wander.
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
- [ ] **C3 Uplift cyborgs.** A cyborg variant of a worker (placeholder tint/parts until his models
  land) with its own behaviour.
- [ ] **C4 The glider.** The hang-glider guy at a lookout; his form flies (reuse her wingsuit flight).
- [ ] **C5 Hidden good aliens.** A network of disguised shopkeepers who give tips and upgrades.
- [ ] **C6 Chapter 2 greybox (The Pearl)** with its quests and boss — then 3, 4…

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
