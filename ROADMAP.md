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

**From Colin: keep going, never wait.** Every earlier STEER block (God mode, the farm rebuild, the
farm's room) is done and has been cleared from here. **The roadmap now has a Phase F; take its items in
order.** The rules that still stand:

- **Never wait for Colin.** No Blender work for about a week; places are built in code. If an item is
  too big for one build, split it in the roadmap and ship the first half. If the roadmap ever runs dry,
  write the next items yourself from `GAME_DESIGN.md`, `REGIONS.md`, `LORE.md` and `CHARACTERS.md` — and
  say so under Decisions — rather than idling.
- **He has seen nothing since the farm (m304).** Everything from m305 to m415 is unverified on a phone, so
  Phase F starts with the phone pass and the whole-game check before anything new is built.
- **Polish is worth as many passes as it takes.** *"If we need to run the same pass over and over for
  like 10 passes until it looks beautiful, so be it."* Use `npm run shot` on every polish pass and fix
  the worst thing in the shot.
- **`npm run places` before pushing any build that adds or moves a place**, output in the NOTES entry.
- **Anything built must be reachable from GOD mode in the same build.**
- **Authored placement only**: nothing dropped in the world without a reason and a place for it.
- **The world rules** (scale follows the place, no borders that are lines, connective tissue,
  exaggerated scale, vertical, organic, interactive) apply to every place, old and new.

## Standing rules for anything built in the world

- **Exaggerated scale and contrast:** vary heights a lot and push them past realistic — tall and thin
  beside short and squat (a tall windmill over a low shed, a skinny tower beside a squat diner). Never a
  row of same-height boxes. Bosses are oversized. See "Exaggerated scale and contrast" in `GAME_DESIGN.md`.

- **Connective tissue:** between any two regions, build several irregular routes of different kinds
  (water, crossings, over and under, open ground), never a single road and never a straight border.
  Read "The connective tissue" in `REGIONS.md`.

Read `GAME_DESIGN.md` → "The world: dense, vertical, organic, alive" before building any place.
**Scale follows the place, vertical, organic, interactive, and one place finished at a time.** Never a
flat plane with spaced-out rectangles on it, never a grid of separate areas, never a straight border.
Build one place at the scale that place really is (dense city, open country) and finish it.
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

- [x] m329 **B1 The farm.** Farmland on the island ring around the kit city — small, close and layered,
  not a flat field: a sunken lane between hedges, the barn with a hayloft you can climb, a silo, a
  creek with a footbridge, the road climbing to a bridge into town. Cows as placeholders (boxes or an existing body) that moo and
  wander. The crash site: a wreck, smoke, Clancy inside.
  - [x] m288 **B1a The farmyard** — barn on a plinth, hay-bale stair to the hayloft, loft door over a hay stack, lean-to whose roof you reach off crates, walkable barn roof, silo, split-rail paddock, round bales, trough.
  - [x] m289 **B1b The crash site** — the wreck, scorched ground, smoke, Clancy inside; where Chapter 0 starts.
  - [x] m290 **B1c The sunken lane and the creek** — a lane cut below the fields between hedges, a creek with a footbridge.
  - [x] m291 **B1d The road and the bridge** — the road climbing from the farm to a bridge into town (split: the cows are B1d2).
  - [x] m294 **B1d2 The cows** — cows that moo and wander the farm.
  - [x] m329 **B1e From REGIONS.md's Gristle Farm entry, not in m288** — a rope down from the hayloft, the silo ladder made climbable, an orchard terrace, and cows that panic and stampede (its signature system).
    - [x] m327 **B1e-1** the rope down from the hayloft and the silo ladder, climbable, with a landing on top.
    - [x] m328 **B1e-2** an orchard terrace.
    - [x] m329 **B1e-3** cows that panic and stampede (the farm's signature system).
- [x] m333 **B1f Direction and discovery** (see the new section in `GAME_DESIGN.md`). Build on m278's quests:
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
  - [x] m330 **B1f-1** the "New task" card, the task list (tap the objective), several tasks with one followed, the waypoint's distance in the world, and the same metres on the map.
  - [x] m331 **B1f-2** rumours: a separate list, no marker (or a rough circle), resolved when you find the thing.
  - [x] m332 **B1f-3** who talks to whom: forms a speaker talks to, forms it brushes off (a short line), the alien makes it flee; a task can need a form to start.
  - [x] m333 **B1f-4** Chapter 0 uses it: the farmer's family brush off the alien; as the farmer, the neighbour at the farm shop gives the bridge task and the hill rumour.
- [x] m334 **B2 Chapter 0 script.** Crash → find Clancy → the farmer sees you and panics → knock him
  down → take his sample → walk to the bridge as him → the cop checkpoint lets the farmer through
  (and stops the alien) → Old Town, fog lifts. Tutorial prompts along the way.
- [x] m338 **B3 Old Town setup.** Region bounds, a homeless camp, a food cart with the hidden good
  alien (the tell under the hat), a building site. Ambient life placed by role.
  - [x] m335 **B3-1** the map's real regions (Old Town, Gristle Farm) and the homeless camp.
  - [x] m336 **B3-2** the food-cart pod in a lot, with the hidden good alien at one cart (the antenna under the hat).
  - [x] m337 **B3-3** a building site wrapped in scaffolding, with its crew.
  - [x] m338 **B3-4** ambient life placed by role (cops on the beat, people on the pavements, the crews' comings and goings).
- [x] m341 **B4 Chapter 1 quests.** The good alien points you at the building site; workers are being
  turned into Skinsuits; get the worker form; repair the broken bridge (gate) to the next district.
  - [x] m339 **B4-1** the good alien points you at the building site; you watch a worker turned into a Skinsuit and beat it back; she tells you about the foreman.
  - [x] m340 **B4-2** get the worker form: knock a worker down and take the sample; as a worker the crew talk to you, and the foreman gives you a job.
  - [x] m341 **B4-3** the collapsed footbridge to The Pearl (REGIONS: over the rail cut), rebuilt as the worker: the bridge gate, the quest step, and the far side as a portal.
- [x] m342 **B5 Chapter 1 boss.** The infiltrated foreman bursts out of his skin; beat him; revert the
  crew; chapter complete → Chapter 2 region unlocks on the map.

## Phase C — systems the later chapters need

- [x] m345 **C0 District health.** Each district has a health the city's systems push up and down:
  damage, fires and Skinsuits lower it; crews and firefighters raise it. A strike stops the crews and
  the district decays (boarded windows, rubble, squatters); ending it sends them back out. The look
  follows the health. Start with Old Town and the existing worker/repair and fire systems.
  - [x] m343 **C0-1** the number: Old Town's health, pushed by chunks, breakables, fires, Skinsuits, repairs and the crews; saved; on the chip, the map and in GOD.
  - [x] m344 **C0-2** the look follows it: boarded windows, rubble, litter, dead streetlights and squatters as Old Town slips; cleaned up as it recovers.
  - [x] m345 **C0-3** the strike: the crews down tools (pickets at the site, no repairs, the district slides); ending it sends them back out.
- [x] m348 **C1 Protest events.** Activists gather with signs and chant; rednecks show up; it turns into
  a brawl if provoked; cops respond. As an activist you can walk inside the crowd through a barricade.
  - [x] m346 **C1-1** the protest: activists with signs gather at the square, march up the street chanting, rally, and go home, on their own clock.
  - [x] m347 **C1-2** the counter-protest: rednecks and bikers show up at the rally, the two sides shout; it turns into a brawl if provoked (a blow, a shot, the alien); cops respond.
  - [x] m348 **C1-3** the barricade: as an activist inside the crowd you march through a barricade nobody else gets past.
- [x] m349 **C2 Skinsuit incursions.** An enemy ship/agent turns civilians on the street; you fight and
  revert them. Ties to the existing virus system.
- [x] m352 **C2b The orbs (`LORE.md`).** Start with the pacifier: an orb floating over a few Old Town
  blocks, a trance on the people under it (they stare and walk in slow loops), the blaster can shoot
  it down, and they come out of it dazed. Lights flicker and cars stall near it (the
  electromagnetic tell). Then the watcher and the amplifier, which feeds the protests and brawls.
  - [x] m350 **C2b-1** the pacifier over the south side: the trance, the crackle, the shot that finds it, the dazed release.
  - [x] m351 **C2b-2** the watcher: a searchlight orb; caught in its beam you raise the alert (heat), and it calls the others; shot down, the alert drops.
  - [x] m352 **C2b-3** the amplifier: over the square, it makes the protest louder and the brawl likelier; shot down, the crowd calms.
- [x] m353 **C2c Placeholder roster (`CHARACTERS.md`).** Build against ROLES, not models: a roster table of
  every role the regions need, each mapped to a stand-in (existing body + tint + prop + name tag).
  When his model for a role lands it is one line. GOD mode lists every role and spawns one.
- [x] m354 **C2d Smart objects.** Benches, café tables, bus stops, food carts and counters carry use spots
  (where to stand or sit, which way to face, which clip). NPCs nearby walk to one, use it for a while,
  and leave. Missing clips fall back to an idle and the chip names the clip, so his animations drop in
  with no code change. Start in Old Town.
- [x] m355 **C3 Uplift cyborgs.** A cyborg variant of a worker (placeholder tint/parts until his models
  land) with its own behaviour.
- [x] m357 **C4 The glider.** The hang-glider guy at a lookout; his form flies (reuse her wingsuit flight).
  - [x] m356 **C4-1** his form flies: her wingsuit flight (double tap the right pad) under a hang glider instead of her wings; the gap gate wants his form.
  - [x] m357 **C4-2** the lookout: a tower on Old Town's ring over the water, the glider guy on top with his glider, and a task to take his form and fly.
- [x] m358 **C5 Hidden good aliens.** A network of disguised shopkeepers who give tips and upgrades.
- [x] m406 **C6 Chapter 2 greybox (The Pearl)** with its quests and boss — then 3, 4…
  - [x] m359 **C6-1** the land: piers past dock 1's door, eight warehouses round a plaza, containers, stalls, string lights, four locals; GOD place.
  - [x] m360 **C6-2** the plaza protest and a barricade on every street into it.
  - [x] m361 **C6-3** up top: rooftop gardens, catwalks and rope bridges between the warehouses.
  - [x] m364 **C6-4** Chapter 2's quests: the strike starts, the organiser's rooftop HQ (W5), expose the infiltrator (the boss), the strike ends and the crews go back.
    - [x] m362 **C6-4a** Chapter 2 opens: the strike is called; to The Pearl, Juno, an activist's look, into the plaza, Marisol.
    - [x] m363 **C6-4b** the organiser's roof: up over the roofs to the HQ shed; the organiser at the transmitter; the receipts for the signs; take them to Marisol.
    - [x] m364 **C6-4c** the exposure: the organiser called down to the stage; knocked down in front of the crowd, it bursts (the boss); after, the strike ends and the crews go back; Chapter 2 complete.
  - [x] m376 **C6-5** Chapter 3 greybox (Hollow Creek, REGIONS 4), split:
    - [x] m365 **C6-5a** the land: its own landmass across the water, the hill, the bike-track ridges, the gorge and its stream, the two flats, the forest; GOD places.
    - [x] m367 **C6-5b** the trailer park on stilts over the creek, and the logging mill with its flume and conveyors.
      - [x] m366 **C6-5b-1** the trailer park on stilts: a boardwalk down the creek, seven trailers off it, ramps from the rims, a ladder to the water, four residents.
      - [x] m367 **C6-5b-2** the logging mill on its flat by the gorge: the shed, the log deck, conveyors, a flume dropping into the creek.
    - [x] m369 **C6-5c** the fairground and the dirt-bike track; the people (rednecks, bikers, rally-goers).
      - [x] m368 **C6-5c-1** the fairground: the stage and its truss, the field, the grandstand, the midway, the Ferris wheel, the barn, the gate; rally-goers.
      - [x] m369 **C6-5c-2** the dirt-bike track over the ridges: jumps, berms, a start gate, the pits; the bikers.
    - [x] m371 **C6-5d** the way in: the freight line out of Old Town over the water, and a second way (the highway shoulder).
      - [x] m370 **C6-5d-1** the freight line: a trestle from Old Town's south-west beach to a halt at the creek's mouth, and a train you ride.
      - [x] m371 **C6-5d-2** the second way: the highway shoulder (a road bridge in, watched by the gang).
    - [x] m372 **C6-5e** the rally, the region's living system: it builds, the leader speaks, it boils over.
    - [x] m376 **C6-5f** Chapter 3's quests: the biker form, the gang's respect, the infiltrated rally leader (the boss).
      - [x] m373 **C6-5f-1** Chapter 3 opens: over the water, Pap, a biker's sample, Spud's challenge.
      - [x] m374 **C6-5f-2** the motorcycle: the biker form rides (the skateboard's riding, a bike under him, faster, no deck tricks).
      - [x] m375 **C6-5f-3** the gang's respect: race Big Rae round the dirt track; win, and the gang knows your name.
      - [x] m376 **C6-5f-4** the rally man: on the stage at the rally, in front of everyone; he bursts (the boss); Chapter 3 complete.
  - [x] m388 **C6-6** Chapter 4 greybox (The Waterfront, REGIONS 5), split:
    - [x] m377 **C6-6a** the land: quays across the river from Old Town, two piers, the dry dock with a ship in it, the container yard as cliffs with a high road over it, the transit shed, the factory shut behind its fence, floodlights; the sodium night; GOD places.
    - [x] m379 **C6-6b** the cyborg factory: the hall opened up, conveyor lines through it at several levels, catwalks; the conversion line (workers go in human, come out cyborg), the signature system.
      - [x] m378 **C6-6b-1** the hall opened up: the line climbing through it on three levels (belts that carry), walkways, the west stair, the control room, the gallery and the outfeed tower.
      - [x] m379 **C6-6b-2** the conversion line: workers ride it in human and come out cyborg; the line's own clock and noise.
    - [x] m380 **C6-6c** the gantry cranes on the quay's rails: climb one, ride the trolley along the boom, swing a container.
    - [x] m382 **C6-6d** the way in: the ferry from Old Town's docks to pier 1; a second way (the swing bridge, or the drainage outfall).
      - [x] m381 **C6-6d-1** the ferry: Old Town's landing on the south-east shore, a double-ended boat on its own clock, pier 1's pontoon.
      - [x] m382 **C6-6d-2** a second way: the swing bridge (or the drainage outfall), its own kind of crossing.
    - [x] m385 **C6-6e** the engineer / hacker form: locked doors, turrets, security robots; as the engineer they open, turn and stand down.
      - [x] m383 **C6-6e-1** the engineer form (a ROLE's form: sample Ivy or Dex) and the doors: Uplift's gate and the swing bridge's control box answer to the engineer.
      - [x] m384 **C6-6e-2** the turrets on Uplift's lot: they fire on strangers; the engineer turns them.
      - [x] m385 **C6-6e-3** the security robots in the yard: they chase strangers off; for the engineer they stand down.
    - [x] m388 **C6-6f** Chapter 4's quests and its boss; shut the line down and the cyborgs turn back; Chapter 4 complete.
      - [x] m386 **C6-6f-1** Chapter 4 opens: over the river, Rosa on pier 1, Dex on the shed roof, an engineer's face, through Uplift's gate.
      - [x] m387 **C6-6f-2** shut the line: the control room's red lever, the line stops for good, the cyborgs start turning back.
      - [x] m388 **C6-6f-3** the boss: the line's supervisor bursts out (Uplift's own, nearly twice your height); after him Chapter 4 is complete.
  - [x] m398 **C6-7** Chapter 5 greybox (the River Islands -- GAME_DESIGN's "Skate Islands", REGIONS 8), split:
    - [x] m389 **C6-7a** the land: six islands at six heights off Old Town's +z shore, water in every gap, ladders up the cliffs, the lighthouse; GOD places.
    - [x] m392 **C6-7b** what is on them, split:
      - [x] m390 **C6-7b-1** the skate park on the old pier and its people (three locals and Rollergirl, the easter egg).
      - [x] m391 **C6-7b-2** the BASE jumpers' exit point on the mesa and the gap ramp on the high hump, with their people.
      - [x] m392 **C6-7b-3** the people who move: a BASE jumper who really jumps (off the exit point, canopy, down to the water) and the kite surfers on the water between the islands.
    - [x] m393 **C6-7c** the wind: gusts that change direction and strength and push every flight (the signature system).
    - [x] m395 **C6-7d** the ways in and out, split:
      - [x] m394 **C6-7d-1** the ways in: the lookout glide's landing field on the landing rock, and a second way over on foot (sea stacks and rope bridges across the strait from Old Town's beach).
      - [x] m395 **C6-7d-2** the way on: the thermal up off the needle to the Mothership's tether.
    - [x] m398 **C6-7e** Chapter 5's quests and its boss, split:
      - [x] m396 **C6-7e-1** Chapter 5 opens: over to the islands, Rue on the landing field, Rollergirl at the pier (the tether, the lighthouse that points up), up the mesa to Teo.
      - [x] m397 **C6-7e-2** the gaps: land on Rue's field, clear the gap ramp's jump, top the needle.
      - [x] m398 **C6-7e-3** the boss: the lighthouse keeper (a Skinsuit guiding the Mothership in), the wind turned on you while he stands; after him Chapter 5 is complete and the tether is the way on.
  - [x] m406 **C6-8** Chapter 6 greybox (the Mothership -- GAME_DESIGN's finale, REGIONS 10), split:
    - [x] m399 **C6-8a** in: the pod up the tether into the ship's belly -- a round chamber in the hull with a glass floor over the cloud's hole, looking down the tether at the islands; the way on shut.
    - [x] m400 **C6-8b** the corridors: organic tubes off the belly up through the ship, the conversion chamber (pods of half-turned people), the bridge with Weirdport under it.
    - [x] m401 **C6-8c** its people: Skinsuit grunts on patrol, the turned in their pods.
    - [x] m403 **C6-8d** every form one last time, split:
      - [x] m402 **C6-8d-1** the way to the core: the torn walkway (the worker mends it), the neural lock (the engineer's mind opens it), the shaft (a flight rides its lift up), the core on the ship's back.
      - [x] m403 **C6-8d-2** the rest: the activist's march, the biker's jump, the farmer -- each one more stretch of the way.
    - [x] m406 **C6-8e** Chapter 6's quests and the final boss; the end, split:
      - [x] m404 **C6-8e-1** Chapter 6 opens: up the tether, the conversion chamber, Benny in his pod (the man in the nice suit, the core behind six locks), the bridge.
      - [x] m405 **C6-8e-2** the six locks as a quest: each gate a step, the form it wants in its tip; up the shaft to the core.
      - [x] m406 **C6-8e-3** the man in the nice suit: the final boss in the core; after him, the turned come back and the end.

## Phase D — turf (after Phase C; see "Turf" in GAME_DESIGN.md)

- [x] m407 **D1 Influence model.** Per-block shares for each faction, saved with progress; a map overlay
  and a chip token showing who holds the block you're in.
- [x] m408 **D2 The crowd follows influence.** The NPC mix in a block comes from its shares.
- [x] m409 **D3 Faction dressing.** Each faction's set of props, signs, paint and decay on existing
  buildings, cross-fading as a block changes hands.
- [x] m411 **D4 Faction buildings.** Kit-generated building styles per faction, swapped in when a block
  changes hands for good. Split:
  - [x] m410 **D4a** the generator: a building assembled from his piece library in each faction's style (co-op, garage, glass tower, shopfronts, walk-up, Uplift's plant, the hive), its colliders from the pieces' own; GOD builds one in front of you.
  - [x] m411 **D4b** the swap: a block held long enough is held "for good", and one of its buildings is replaced by its holder's.
- [x] m413 **D5 Pressure.** Factions push at their borders on their own (flashpoint events), and the
  player's actions move the shares. Split:
  - [x] m412 **D5a** your actions move the shares: who you knock down, bodies turned and cured, workers freed of Uplift, rallies and brawls, the strike.
  - [x] m413 **D5b** flashpoints: factions push at their borders on their own (a rally marching into another's block, a developer at the camp), and you can tip one.

## Phase E — side quests (see "Side quests from UFO pop culture" in LORE.md)

- [x] m414 **E1 Element 115.** The jittery ex-lab tech (stand-in body), hidden somewhere in Old Town; earn his
  trust, learn where the 115 is, fetch it; it upgrades the juice tank. The first side quest, and the
  template for the rest.
- [x] m415 **E2 The late-night radio host.** A voice on car radios that reacts to what you've done and
  points at sightings; a side-quest hub.

## Phase F — what the docs call for that isn't built yet (after E; Colin has not seen m305-m415)

- [ ] **F0 The phone pass and the whole-game check.** Before anything new:
  - [ ] **F0a Measure every world** as it is now: draw calls, triangles, resident texture memory and
    boot time per world, printed in the chip and in NOTES. Set a budget per world for a phone (draw
    calls in the low hundreds, textures KTX2, nothing resident that isn't on screen) and cut the worst
    offenders: instance, merge, fade with distance, cull by chunk, drop what nobody sees. Repeat per
    world until each is inside its budget.
    Split:
    - [x] m416 **F0a-1** the measure: `TX`/`G`/`boot` in the chip's perf line, `mel.mem()`, and `npm run worlds` (every world, every region, against the budget; exits 1 on OVER).
    - [ ] **F0a-2** cut the worst offender in the kit city (the biggest OVER in the `worlds` table), one world or one offender per build, until `npm run worlds` exits 0. Split:
      - [x] m417 **F0a-2a** the far culls: bodies beyond 150 m and the kit's moving parts beyond 220 m are not drawn (7 of 14 places inside the draw budget; every place halved).
      - [x] m418 **F0a-2b** the unnamed `Mesh` draws (150-250 at the Waterfront's cliff, the islands' landing, the trailer park): name them in `--who`, then merge or instance them.
      - [ ] **F0a-2c** Old Town from inside and from the islands: the kit batch is 790 cell meshes; far cells as one merged LOD per material, near cells as now.
      - [ ] **F0a-2d** the textures (270 MB): Moussa's two 2K maps to KTX2 or 1K, the impact atlas and the HDRI; then the other worlds.
  - [ ] **F0b A headless playthrough** (`npm run play`): drive Chapter 0 to the end through the shipped
    quest steps and the shipped `godPlace`, every gate and boss in order, and fail if any step can't
    complete. Run it before every build that touches a quest, a gate or a chapter from now on.
  - [ ] **F0c Every world boots** through the real loader with no red toast, in `places`.
- [ ] **F1 Polish passes, region by region, with `npm run shot`.** The farm had five; each of the others
  gets at least three, one build each, fixing the worst thing in the shots and checked against the
  world rules (exaggerated scale, connective tissue, vertical, no straight borders, nothing bare):
  Old Town, The Pearl, Hollow Creek, the Waterfront, the River Islands, the Mothership. Then the
  routes between them (the trestle, the ferry, the freight line, the bridges) as places in their own
  right, with something on every one.
- [ ] **F2 The regions still missing from `REGIONS.md`**, each as land → places → people → the ways in
  (several, per the connective-tissue rules) → its quests and boss. Read the entry first.
  - [ ] **F2a The Underneath** (3): the tunnels under Old Town, the Pearl and the Waterfront, surfacing in
    cellars and drains; the hobo's and the miner's region; the safe-house portals.
  - [ ] **F2b Dump Tower** (6): the vertical level, the Reptilians' seat. It goes BEFORE the Mothership in
    the chapter order (Dump Tower is the last stop in the metropolis; renumber the chapters and the
    Mothership's six locks become seven).
  - [ ] **F2c The Gorge** (7): falls, the stilt village, the scuba diver; between Hollow Creek and the
    River Islands, down the log flume.
  - [ ] **F2d The Hothouse** (9): the alien takeover, as a region that grows across the map while the
    grid stands and shrinks as you cure districts.
  - [ ] **F2e The metropolis hub**: the tall city in the middle of the map that the other regions ring,
    opened a part at a time as chapters complete; Dump Tower stands in it.
- [ ] **F3 The rest of the grid and the fail states** (`LORE.md`): the projector, poltergeist and relay
  orbs; the EM tell (lights flicker, cars stall, radios hiss near the grid); the Hum; black triangles at
  night and tic-tacs that chase flyers; **missing time** as the capture fail state and something at
  zero health (Colin's open question: propose one, build it switchable).
- [ ] **F4 The forms still missing** from the forms table, each with the door it opens: cop (cordons,
  arrest), firefighter (fires, the truck ladder), hobo as stealth (guards ignore him), CEO (Dump Tower),
  scuba diver (the Gorge), cave miner (the Underneath), military (the base at high heat).
- [ ] **F5 Side quests**, one build each, from the table in `LORE.md`, in this order: the Roswell diner,
  the tinfoil-hat bunker (the grid on the map), the Majestic Dozen, Mothman, the Phoenix Lights, the
  haunted ranch, the tic-tac pilot, Bigfoot, D.B. Cooper, Betty & Barney, Travis Walton, Area 15.
- [ ] **F6 Living-city depth**: more smart objects and the everyday life they make (sitting, waiting,
  queuing, shopping, the bus stop), named in the chip when a clip is missing so Colin knows what to
  author; the turf's building swap in every region, not only Old Town.

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
- **m307 (farm rebuild, step 2):** a creek now runs down a real valley from the long ridge to the
  sea, east of the farmyard, with a wooden footbridge across it. A pond with reeds, lily pads and
  four willows sits in the low ground west of the yard. Both are cut into the land itself, so you
  can walk down into the valley and the pond's banks hold its water.
- **m308 (farm rebuild, step 3):** the land is now 20 named fields in irregular patches (wheat, corn,
  hay, pasture, ploughed earth with furrows, stubble), each tinted on the ground so the patchwork
  reads from the west hill. Hedgerows with oaks in them, post-and-rail fences round the pastures,
  a few tree lines, and four dirt tracks: bridge to farmyard, yard to the neighbour's ridge, across
  the creek ford to the big wheat, and round the pond up the west hill. The crops themselves don't
  stand on the new fields yet; that's next (3b). Each field is one row in `FPLAN.FIELDS` if you want
  a different crop somewhere.
- **m309 (farm rebuild, step 3b):** the crops now stand in the new fields (wheat, corn, hay, stubble,
  pasture grass), about 38,000 clumps. They shrink away past 110 to 160 m and whole patches stop
  drawing beyond that, so only the fields near you cost anything; the coloured ground carries the
  patchwork in the distance. If the fade is too close or too far, it's `mel.FCROP.fade`.
- **m310 (farm rebuild, step 4a):** the crash is now far out in the big wheat on the swell, about
  185 m from the farmyard. It sits at the end of a 68 m gouge torn through the wheat, with a crop
  circle (a ring, a disc and three satellites of flattened wheat) a field away. A new game starts
  there, with the city just a skyline.
- **m311 (farm rebuild, step 4b):** the farmhouse now has its own yard, 70 m north of the barn
  across a home pasture, with a tool shed and a chicken coop beside it and a track between the two
  yards. The ground between is fields: corn with the scarecrow in it, the home pasture, an orchard
  in rows, and a pasture down to the creek. The old headland's hedge-and-crop layout and the little
  brook through the lane are switched off on the new land (not deleted), since the field plan and
  the creek valley do their jobs now.
- **m312 (farm rebuild, step 4c):** the neighbour's farm now stands on the ridge where the ridge track
  ends: a tall, thin blue house beside a long, low cattle shed, a skinny water tower, and a little
  farm shop by the track with an awning and crates of apples and pumpkins (where the neighbour in
  B1f will give you the bridge task). Out in a far hay field stands a lone open-sided hay barn with
  a curved roof; its bales are stacked in steps you can climb. That finishes step 4.
- **m313 (farm rebuild, step 5a):** herds of cows now graze six pastures across the land: the far
  hill, the neighbour's ridge, the slope above the creek mouth, by the pond, the home pasture and
  down by the creek. That's 30 cows with the paddock's three, each keeping to its own field.
- **m314 (farm rebuild, step 5b):** a red tractor now ploughs the field under the far hill, up and down
  its furrows, dust behind it. A blue pickup with a bale in the back drives from the barn door out
  along the sunken lane and the bridge road to the bridge, waits, and comes back. Both stop if you
  stand in front of them. No engine sound yet; I left that for later rather than fake one badly.
- **m315 (farm rebuild, step 5c):** four farmhands now work the land, Dale in the wheat by the bridge
  road, Wendell on the west hill's hay, Mags in the orchard and Earl by the ploughed field, plus
  Farmer Gristle at his barn doors. Each has a name and a few lines. They're stand-in bodies
  (hobo for the hands, the skinny hick for the farmer, as CHARACTERS.md says) until your models
  land. That finishes step 5.
- **m316 (farm rebuild, step 6a):** the edge of town now stands on the farm's side of the bridge: a gas
  station under an 11 m price sign, a trailer park, three little houses with picket-fenced yards, two
  tall billboards ("VISIT WEIRDPORT · IT'S PERFECTLY NORMAL HERE"), a fruit stand, power poles along
  the road, and the bridge road paved for its last stretch. Next is the city side of the bridge.
- **m317 (farm rebuild, step 6b):** across the bridge the city now starts thin. Where the bridge comes in
  there's a big warehouse (climb its outside stair to the roof) and a fenced lot of parked cars. Ten
  low houses with fenced yards sit round the city island's grass ring, and about 40 trees are planted
  right against the city's edge, so it no longer ends at a ruler line. That finishes step 6.
- **m318 (farm rebuild, step 7):** phone cost. Everything static on the farm, the town edge and the
  city ring is now merged by paint type into 200 m patches: 108 separate draws became 71, and the
  ones behind you aren't drawn at all. It should look exactly the same. If anything looks different
  (wrong colour, missing paint), GOD has a FARM BATCHING switch to compare with it off.
- **m319 (farm rebuild, step 7b-1):** a second way over the channel: an old wooden rail trestle west
  of the bridge, on an embankment out of the south wheat. It bends toward town and comes down behind
  a house whose back fence is broken, a way through the backyards past the checkpoint. For now a
  19 m stretch of it has fallen in (too far to jump), so the checkpoint still teaches; it opens later
  with a form or Clancy.

- **m320 (farm rebuild, step 7b-2):** a third way over the channel, the lowest: stepping stones from
  the beach below the east pasture, wandering out to the city's shore between two ring houses, with
  three cows drinking at the foot. Like the trestle, a 26 m stretch in the middle is under the tide
  for now, so the checkpoint still teaches; it opens later. Also a stone culvert where the east
  track crosses the creek, with earth ramps up to it, so the track no longer runs into the water.

- **m321 (farm rebuild, step 8):** a screenshot tool works here now (`npm run shot`). It renders one
  frame from a named spot and saves it, about 100 s for three shots. The three shots (ridge, road to
  town, crash) are in the chat. What they showed decides the next farm polish passes, in this order:
  1. From the ridge every far field is the same green; wheat and ploughed earth should read from a hill.
  2. The city skyline is lost in the haze.
  3. The hedge banks look like boxes.
  These come before B1e, per the STEER's "polish passes on the farm until it is beautiful".

- **m322 (farm polish 1 of the three from m321's shots):** the fields read from the ridge now. Wheat
  is gold, hay meadows are straw, ploughed fields are brown with furrows, and pasture and corn stay
  green (corn darker). The farm's grass overall is a little warmer and less lime. The before and
  after shots are in the chat. `mel.FPLAN.dye.value` makes the dyed fields brighter or darker live (1.05 now).
  Next: the skyline in the haze, then the hedge banks.

- **m323 (farm polish 2):** the skyline. The island city's houses are too low to be seen from the
  farm, so I put the METROPOLIS on the horizon behind it, since REGIONS.md describes it as the farm's
  view: skyscrapers in five districts and Dump Tower in gold, the tallest thing in the world, with a
  green alien beacon pulsing on top. It's scenery: you can't reach it, and from the island city it
  shows across the water on the far side. It's one draw call. GOD → SWITCHES → METROPOLIS ON THE
  HORIZON turns it off if you'd rather not have it. Next: the hedge banks.

- **m324 (farm polish 3):** the hedge banks are no longer boxes. Field hedges sit on long lumpy
  mounds, and the farm lane's tall banks have sloped sides with rounded ends where they stop. Walking
  on them is unchanged (same colliders). That's the three things m321's shots showed. Next pass:
  take new shots and polish whatever looks weakest, or move to B1e if it all reads right.

- **m325 (farm polish 4):** the crash site is the weakest thing in the new shots, so this pass
  makes it the hero:
  - the saucer is 1.6x bigger, nose down in a bow wave of earth it ploughed up;
  - the furrow's sides are mounds of thrown earth, not brown planks;
  - the purple scorch is charred and patchy, not a canal;
  - a new game now starts 15 m back so the whole wreck is in view.
  `mel.CRASH.S` is the scale, which takes a reload.

- **m326 (farm polish 5):** the cows. They were sixteen boxes each, and a herd was five cows
  wandering separately over a whole field. Now every part is a rounded box, so they read as chunky
  toy cows, and a herd grazes together, each cow mostly picking a spot near a herd-mate. The bigger
  pastures have 7 cows. `mel.COW.round` (0 is the old boxes; needs a reload) and `mel.COW.herdP`
  (how herd-bound they are, 0.7 now) are the dials.


- **m327 (B1e-1):** I stopped the farm polish after five passes (fields, skyline, hedge banks, the
  wreck, the cows). The new shots read right, and the STEER says B1e comes next. Say if you want
  more polish passes. B1e is split in three: the rope and the silo ladder now, then the orchard
  terrace, then the stampede. The rope hangs from the hook beam over the loft door; walk into it
  facing the barn and push up to land in the loft. The silo ladder climbs to a railed landing at
  11 m.

- **m328 (B1e-2):** the orchard sat on ground too gentle to cut terraces into (1.6 m of rise), so
  I built them up: four dry-stone tiers, 1.4 m each, about 7.5 m to the top, following the orchard
  field's own outline. A stair comes up each tier on a different side, so the way up winds round.
  There's a row of apple trees on every tier (54 trees), apples in the grass, and crates at the
  stair heads. Next: the stampede.

- **m329 (B1e-3, so B1e is done):** cows stampede:
  - A shot within 34 m, or the alien undisguised within 6 m, panics a cow.
  - The panic ripples through its herd, and they all bolt the same way at 5.6 m/s.
  - While stampeding they ignore their field, so they end up out on tracks and lanes, then wander back.
  - A stampeding cow knocks you down (not in GOD mode, which takes no damage).

  The 6 m alien range means walking up to cows as yourself always sets them off. That's on purpose:
  being a farmhand is how you get close. `mel.COW.alienR` is the dial.


- **m330 (B1f-1):** B1f is split in four: tasks, rumours, who talks to whom, then Chapter 0 using
  them. The tasks part:
  - A "NEW TASK" card when a task arrives.
  - Tap the objective at the top to open the task list; tap a task to follow it.
  - The followed task's waypoint has a gold distance label over it, pinned to the screen edge with
    an arrow when it's off screen. The full map shows the same metres by its gold dot.
  - No real tasks exist until Chapter 0 (B2). To try it: GOD → THE STAND-IN TASKS, then tap the
    objective.

- **m331 (B1f-2):** rumours. Three farmhands now end their chat with one:
  - Dale in the wheat: a ring in the wheat.
  - Wendell on the west hill: the old rail bridge.
  - Earl by the plough: the cows' way over the water.

  A rumour goes in the task list under RUMOURS, with who told you, and shows as a rough dashed circle
  on the full map (never a marker or a waypoint). Getting to the place gives "RUMOUR FOUND". The
  fourth, "the man on the hill", is for the farm-shop neighbour in B1f-4. GOD → HEAR EVERY RUMOUR
  fills the list for a look.

- **m332 (B1f-3), with a bug fix:**
  - **Bug fix:** the farmhands (Dale, Wendell, Mags, Earl) and Farmer Gristle had never actually
    appeared. Their markers never matched a character file (a name-format mismatch since m293), and
    the same bug would have stopped any npc marker you place in Blender. Fixed, and `places` now fails
    if one doesn't resolve.
  - **Who talks to whom:** people now react to your form. The alien makes them run, or gets a
    brush-off from the few who stand their ground. The wrong sort of local gets one short, light
    brush-off line. Their own sort gets the real conversation, rumours included. Farmhands talk to
    country folk and tramps.
  - **Tasks:** a task can now come from a person and only unlock once they've talked to you properly.
  - **Your Blender npc markers** can carry `group`, `talks` and `alien` too.

- **m333 (B1f-4, so B1f is done):** Chapter 0's talkers.
  - **Ma and Grandpa Gristle** are on the farmhouse yard. They don't run from the alien; they get rid
    of you with their own lines.
  - **Nell Haskins** is at her farm shop on the ridge. She runs from the alien but talks to the farmer:
    she gives you THE ROAD TO TOWN (the first real task, with waypoint and distance to the checkpoint)
    and the rumour about the man at the top of the hill.
  - **Names and models:** I picked them from what we have. Ma uses the blonde model, Nell the Asian
    model, and Grandpa the hobo. Say if you want different bodies for them.

- **m334 (B2):** Chapter 0 plays start to finish as one quest with a tip on each step:
  1. Find Clancy.
  2. Find the farmer at his barn.
  3. Knock him down.
  4. Take his sample.
  5. Walk to the bridge as him.
  6. Get through the checkpoint.
  7. Reach Old Town.

  Finishing it moves you to Chapter 1. The bridge now has a police checkpoint with two officers: any
  human form walks through, and the alien is held back and raises heat each time it tries.
  Another bug fix of the m332 kind: the gates (cordon, fire, barricade, broken bridge) never let
  ANY form through since m285. They do now.
  To play it: GOD → NEW GAME AT THE CRASH.

- **m335 (B3-1):** B3 is split in four: regions and the camp, the food-cart pod, the building
  site, then ambient life. This build:
  - The map now has real regions, OLD TOWN and GRISTLE FARM, in place of quadrants. Your own region
    markers will still replace them.
  - The homeless camp is on the biggest open lot in Old Town, at the west edge by the water. No
    overpass exists in your city, so I measured for the lot instead. It has tarp tents round a burn
    barrel that stays lit, a lean-to, sofa, carts, a washing line and string lights.
  - Dusty, Pockets and Mother Agnes live there. They talk to street folk and brush off the alien
    rather than run.

- **m336 (B3-2):** the food-cart pod is on the lot next to the camp. TACO PLANET, THE GOOD GRILL,
  PHO REAL and a shut WAFFLE WAGON sit round tables, umbrellas and lights.
  - **Chef Norrie** at THE GOOD GRILL is the hidden good alien. His hat has an antenna poking through
    it, wobbling, with a glowing tip. To humans he's a cart guy. To you as the alien he never runs,
    he admits it, and he points you at the building site (gives juice the first time).
  - **Bodies:** Norrie, Lupe and Minh use the hipster, activist and hippie stand-ins, per
    CHARACTERS.md.

- **m337 (B3-3):** the building site is on a clear lot in Old Town's south-west quarter. It's a
  three-storey concrete frame in scaffolding, with plank decks at every lift you can walk and
  ladders between them up to 9 m. A tower crane stands over it, and there's hoarding, the site
  office, a mixer and a skip. Sal, Dee and Foreman Briggs work there; Briggs is clearly not right
  (B5's boss).
  My first pick of lot had your COSMIC FUEL gas station on it: its walls aren't in the collision
  boxes, so my lot measurement missed it. I fixed the measurement and moved the site. The
  construction workers there use a new plain-civilian copy of the worker model, so they stay put
  rather than going off to repair walls.

- **m338 (B3-4):** Old Town has eight people moving through it with a purpose: two cops each walk a
  loop round the middle of town (one tight, one wide), four pedestrians walk between the carts, the
  camp, the building site and the town end of the bridge, and two of the site crew go to the carts and
  back. Each stops briefly at every point and moves on, instead of wandering at random. They're all
  ordinary people otherwise: they talk, brush you off by group, and run if you scare them. I left out
  cars in town and any day/night schedule.

- **m339 (B4-1):** Chapter 1 opens at the food carts. Chef Norrie recognises you whatever form you're
  in and sends you to the building site. There, Dee (by the mixer) is turned into a Skinsuit in front
  of you, and you beat it down three times until it lets go of her. Then she tells you about Briggs's
  "safety briefing". I picked Dee rather than Sal because she already says the crew have stopped
  eating. A person turned by the virus now comes back as the same person, with their name and lines,
  and that applies to every turn, not just this one. GOD's Chapter 1 button now takes you to the carts.

- **m340 (B4-2):** after Dee, the task "A HARD HAT": knock down any of the crew except the foreman
  (the two workers walking to the carts are the easy ones), take the sample, talk to Sal as a worker,
  then report to Briggs. As a worker he gives you the footbridge job and invites you to the office
  "alone"; to the alien he says the site is closed. I let you sample any crew member rather than one
  named person, so you can choose who to jump. GOD now has a QUESTS list that starts any quest from
  the top.

- **m341 (B4-3):** your city has no rail cut, so the footbridge to The Pearl crosses the water off Old
  Town's west shore instead, on the bearing where the skyline puts The Pearl. On the far side is The
  Pearl's first loading dock on piles, with a mural wall, which is where Chapter 2's land will grow
  from. The middle span has fallen in, and nobody can cross until you lean on the barrier as the
  worker for two seconds. That also applies to any future "broken bridge" gate: before, the right form
  could walk straight into the gap. There's a portal pad at each end. If you'd rather have the rail
  cut, it can become a trench inside The Pearl's land when Chapter 2 builds it.

- **m342 (B5):** after the footbridge, Briggs's "safety briefing". At the site office he bursts out as
  a Skinsuit about 1.85 times normal size that takes five knock-downs, not three. At the same moment
  the two crew members who walk to the carts all day turn too, so freeing the rest of the crew means
  hunting them down. When everyone's back, Briggs comes round starving and blames "a fella in a nice
  suit" (a lead for later), Chapter 1 completes, and The Pearl is revealed on the map. The boss is
  only bigger to look at: his reach and hits are a normal warrior's, until your model for him exists.
  GOD's Chapter 2 button now takes you to The Pearl's dock.

- **m343 (C0-1):** Old Town's health is one number, 0-100, that's saved and starts at 55 (WORN), because
  "nothing is being rebuilt". It goes down when walls are broken, things are smashed, fires burn and
  Skinsuits walk the streets. It goes up when the crew repairs walls, fires are put out and Skinsuits
  are reverted, plus +15 for beating Briggs. It also creeps up slowly while the crews work and nothing
  is burning. The camp's burn barrel doesn't count as a fire. The numbers are first guesses; they're
  all in `mel.DHEALTH`. GOD has +20 / -20 and a strike switch to try it out.

- **m344 (C0-2):** as Old Town's health falls, litter appears first, then rubble heaps by the walls
  and planks nailed over the real windows of your kit buildings, mostly the lower floors. Below 45 the
  homeless start moving in (up to 5). Every piece has its own point where it shows up, so it gets worse
  gradually and cleans up in reverse as the health recovers. There are no dead streetlights, because
  the city's lamps aren't lights the game controls. Use GOD's OLD TOWN -20 to see it.

- **m345 (C0-3):** the strike is now a real state. The crew walk the picket line outside the site
  gate under an OFFICIAL STRIKE banner, with placards and a burn barrel, and they talk about it. The
  repair worker takes no new jobs, and Old Town's health only slides. Calling it off puts everyone back
  on their routes and the crews go back to fixing things. Nothing in the story starts a strike yet,
  because The Pearl's organiser (Chapter 2) is meant to call it, so until then it's GOD's switch or
  `mel.strike(1)`.

- **m346 (C1-1):** the protest happens in Old Town for now, because The Pearl, its home in the design,
  doesn't have its land yet. Eight activists gather at a square near the middle of town, march about
  43 m up the street to a corner lot, rally there, then go home; it comes round again every few
  minutes. Their signs and chants make fun of everyone ("NO TO THE THING", "TRUST NO HAT", "WHAT DO WE
  WANT? SOMETHING!"), and a man in a suit paid for the placards. The alien still scatters them. When
  The Pearl gets its land, the same event moves to its plaza.

- **m347 (C1-2):** four counter-protesters (hicks and bikers, with their own signs and chant) walk out
  to meet the rally, and a man in a nice suit (who paid for both sides' signs) stands between them. It
  turns into a brawl if you hit anyone in either crowd, or now and then by itself ("somebody threw a
  sandwich"). Everyone goes for the nearest person from the other side, the cops in the area run over,
  and the first cop to arrive breaks it up; it fizzles out after 45 s if they don't get there. The
  brawlers punch with the same knock-back you do but give you no heat. Civilians have no punch
  animation, so it looks like people charging and knocking each other over. I also fixed a bug from
  m338: a cop or walker who got hit lost their route for good, and a protester hit mid-march would
  have been stuck in the hit pose forever.

- **m348 (C1-3):** a police line now stands across the march's street, with two officers at its ends.
  It only opens for someone who looks like part of the march: any activist, hippie or hipster form, not
  only the activist the original gate list named. And only while you're walking in the middle of the
  marching crowd. Sage gives the task MARCH WITH THEM. In Old Town there are other streets round the
  line; in The Pearl's plaza, barricades will close every street.

- **m349 (C2):** the enemy is a ship, not a person on foot. From Chapter 1 on, every 4-7 minutes in
  Old Town, a saucer drops over a street near you. It rays up to four ordinary people into Skinsuits,
  one at a time, then flies off, and a task tracks you beating them back into people. It never takes
  anyone the story needs, and never fires while a quest is turning someone of its own. You can't shoot
  the ship down yet. GOD has "A SKINSUIT INCURSION NOW".

- **m350 (C2b-1):** the first orb is the pacifier, floating over the south side of Old Town. Everyone
  under it walks in small loops saying "Everything is fine." You can hear a faint crackle before you see
  it. When nothing else is targeted, pointing the camera at an orb makes your shots go to it. Three hits
  bring it down; a full charge counts as two. Everyone comes round dazed, Old Town gains 5 health, and
  it stays down. No lights flicker or cars stall: the city's lamps aren't lights the game controls, and
  the kit city has no traffic. GOD can raise it again.

- **m351 (C2b-2):** the watcher hangs over the east side, and its searchlight sweeps the streets. It
  only notices you as the alien, out in the open; any disguise walks right under it. Once it has you, it
  follows you and an alert climbs (`AL` in the chip). At full alert it calls a Skinsuit ship down on
  you, then can't call again for 90 seconds. Shooting it down clears the alert for good. The alert is
  separate from police heat and stays on in GOD mode, so you can watch it work.

- **m352 (C2b-3):** the amplifier is a red orb over the square that rides out above the march. While
  it's up, the protest comes round twice as often, the chants are bigger and red, and the rally is
  four times as likely to turn into a brawl by itself. Shoot it down and a brawl that's already
  happening stops; after that, brawls almost never start unless you start one. That makes three of the
  six orbs in LORE.md; the projector, poltergeist and relay are for later.

- **m353 (C2c):** the roster has 30 roles, each a stand-in built from an existing body plus a tint, a
  simple prop (cap, beanie, chef's hat, helmet, glowing visor) and a name tag. A real model for a role
  will be a one-line change. Two roles had nothing in CHARACTERS.md: I stood in the security robot as
  a silver cop with a cyan visor and the scuba diver as a navy-tinted woman with goggles. Their tags
  say "nothing close yet". Bosses are drawn bigger. In GOD, tap any role to spawn one in front of you.
  None of the people already placed in the world have been switched over to roles yet.

- **m354 (C2d):** the first smart objects are the furniture I'd already built: the food carts (order
  at the counter), their three picnic tables (four places each) and the camp's barrel and sofa (the
  camp's own people only). Nearby people with nothing to do walk over, face the right way, use the spot
  for a while and leave. Your clip names are `order_food`, `sit_eat`, `sit_crate`/`warm_hands` and
  `sit_sofa`. Until a model has those clips it stands in its idle, and the chip shows which clip is
  missing (`SM`). Nobody actually sits on a bench yet: that needs your sit clip and the bench's
  collision letting them through. Bus stops and shop counters come later.

- **m355 (C3):** Uplift sends a two-cyborg survey crew to walk loops of Old Town's streets. They're
  workers with steel tint, a red visor, shoulder plates and a chest light. They never run from you.
  At each stop they sweep a red scan beam; if it catches you as the alien, out in the open, they log
  you. That pushes the watcher's alert up, or brings police heat if the watcher is down. Knock one down
  twice and the implant shorts out, leaving a dazed ordinary worker. The pacifier's trance doesn't work
  on them. Their real home and the conversion line belong to the Waterfront chapter.

- **m356 (C4-1):** the glider's form (Jack stands in for now; swapping in your model is one roster line)
  flies Rollergirl's wingsuit flight with the same double tap of the right pad. Instead of her pink
  panels he hangs under an orange and yellow hang glider. The "gap" gate needed a form called
  "glider" that doesn't exist, so nothing could ever cross a gap; it now needs his form. The lookout
  and the glider guy himself come next.

- **m357 (C4-2):** the lookout is a 16 m timber tower on Old Town's grassy ring, facing the sea. It
  has three platforms with ladders that zigzag up through hatches, a canopy, a windsock and a launch
  ramp. Skye, the hang-glider guy, lives on top. Talk to him and he lies down so you can take his
  sample. The task THE LOOKOUT is: take his form, run off the ramp, double tap, and stay up five
  seconds. REGIONS puts his real lookout in the River Islands; this one is in Old Town so his form can
  be had now.

- **m358 (C5):** the hidden good aliens are a chain of four. Chef Norrie points you to Mags's
  newsstand, Mags to Pruitt's key-cutting kiosk, and Pruitt to Ines the tailor. Each one only drops the
  act for the alien, gives a tip and one upgrade, and tells you where the next one is as a rumour.
  The upgrades: Norrie a bigger juice tank, Mags slower juice drain, Pruitt quicker sampling, Ines
  cheaper transforms. Every kiosk keeper wears the antenna hat. I placed the kiosks on three open
  lots well apart: west, south and south-east.

- **m359 (C6-1) The Pearl.** I put it on piers past the footbridge's dock: you walk through a door
  in the dock warehouse and down onto the decks. Three decks at slight angles, eight pastel
  warehouses with murals around a plaza, container stacks you can climb, market stalls, string
  lights and four locals. The fifth warehouse, the tallest, is held for the organiser's rooftop
  HQ in C6-4. I split C6 into four: the land, the plaza protest and barricades, the rooftops, and
  the quests and boss.

- **m360 (C6-2) The plaza's barricades.** Four junk walls close the four streets between the
  plaza's warehouses. Each has a door with a keeper. Anybody can walk OUT; to get IN you have to
  be an activist (or hipster/hippie) walking inside the march. The sit-in is twelve people round a
  stage with Marisol on a megaphone. Every minute or two they march out and back, alternating
  between the dock (so you can join them at dock 1 and get carried in) and the far pier. I made
  leaving free so the plaza is never a trap, and moved Juno out to the dock street so the first
  person you meet tells you why it is shut.

- **m361 (C6-3) The Pearl's roofs.** Every roof is a garden. Six links join them: a stair, three
  sagging rope bridges and two catwalks, the long one propped on a container. Ladders go up by
  dock 1, inside the plaza, and up the climbing gym. **The roofs are a way into the plaza without
  the march** (climb up outside, cross, drop off an edge; there is no fall damage). I kept that on
  purpose: the march is the way in on foot, the roofs the way in for climbers. If you want the march
  to be the only way in, I can make the drop into the plaza hurt or fence the edges.

- **m362 (C6-4a) Chapter 2 opens.** I split C6-4 into three: Chapter 2's start, the organiser's
  roof, and the exposure. The strike is called eight seconds into Chapter 2, so its card doesn't
  land on top of the chapter card. The first quest takes you across to the Pearl, to Juno, to an
  activist's sample, into the plaza and to Marisol on the stage. Getting into the plaza counts
  whether you came in with the march or over the roofs. GOD's Chapter 2 button now drops you at
  dock 1 instead of the plaza.

- **m363 (C6-4b) The organiser's roof.** Ash, the organiser, stands at a transmitter beside the
  shed and talks like the notes read. **Ash is the one person in the Pearl who doesn't run from the
  alien**, which is the hint. The receipts are on a table by the shed door, and walking up to them
  reads them: the same "friend" paid for both sides' signs. Marisol reads them and calls the
  organiser down to the stage, which is the next build.

- **m364 (C6-4c) Chapter 2's boss.** When Marisol calls Ash down, Ash stands on the stage and the
  march stops going out until it's over. Getting near Ash triggers the boss: it bursts out big and
  takes five knock-downs, and two devoted marchers turn with it. When it's done the strike ends
  and Old Town's crews go back, Old Town gets the boss bonus, and Chapter 3 starts. **I also opened
  the barricade doors for good afterwards**, so the cured Pearl is open to everyone. Ash stays
  down by the stage with new lines. Chapter 3 has no region yet, so nothing new shows on the map.

- **m365 (C6-5a) Hollow Creek's land.** I took "then 3, 4…" as Chapter 3 and split it into six
  steps in the ROADMAP. Hollow Creek is its own landmass across the water to the island's
  south-west, out of line with both the farm and the skyline, so the lookout faces it. It has a
  28 m hill, three ridges for the bike track, a 9-10 m gorge with a stream running to the sea, two
  flat spots for the fairground and the mill, and 900 pines. It's raised higher than the farm so
  the gorge has something to cut into. For now only GOD gets you there. It shows on the map once
  Chapter 2 ends.

- **m366 (C6-5b-1) The trailer park.** I split C6-5b into the trailer park and the mill. The
  boardwalk follows the creek's bends rather than running straight, a little below the rim. Seven
  trailers hang off it on stilts, each a step up or down, with porches, awnings and laundry. Two
  steel ramps come down from the rims and a ladder goes down to the water. Four residents only
  talk to country folk and tell anyone else it's private property.

- **m367 (C6-5b-2) The logging mill.** The tin shed has an upper floor with a stair, and two
  conveyors you can walk: one up from the log deck, one out to the smoking burner. There's a crane
  with a ladder to its cab and a water tower. The flume runs from the upper floor down over the
  gorge, and you can walk it all the way down and drop into the creek. That's my start on the
  "down the log flume" route to the next region. I widened the mill's flat so everything stands
  on level ground.

- **m368 (C6-5c-1) The fairground, plus a step-height fix.** It has a stage with a lighting truss
  you can climb, a grandstand, midway stalls, a turning Ferris wheel, a livestock barn and the gate.
  **While building it I found the player can only step up 0.36 m**, which made two shipped stairs
  into walls: the Pearl warehouses' platform steps (m359) and the mill's stair (m367). I rebuilt
  both with lower steps, and `places` now walks every stair at the real step height.

- **m369 (C6-5c-2) The dirt-bike track.** The loop runs over the three ridges already in Hollow
  Creek's land, so the ridges are the big jumps. On top I built tabletop jumps, banked turns, a
  start hill with a gate, the pits and an announcer's tower. The bikes are only props until the
  biker form arrives in C6-5f. I cleared the pines off the track and out of the pits.

- **m370 (C6-5d-1) The freight line.** A train now shuttles on a trestle from Old Town's south-west
  beach to a halt by Hollow Creek's gorge. There's no deck between the rails, so riding the train is
  the only way across: stand on the flatcar's open deck or the caboose porch and it carries you. The
  train runs in every chapter. Hollow Creek isn't closed to anyone, and the chapter decides what
  you do there. I moved one Old Town ring house a few degrees so the landing stairs fit.

- **m371 (C6-5d-2) The highway and the gang.** A road bridge runs from Old Town's south-west edge
  over the water to Hollow Creek, then a road goes up to the fairground. The gang sits on the far end
  of the bridge with a pickup, a burn barrel and a LOCALS ONLY sign. **Only country folk or bikers
  get past; anyone else is turned round**, but anyone can leave. So there are two ways in: as one of
  them by road, or as anything by freight train. I also let all Hollow Creek's people talk to
  bikers as well as country folk, since bikers count as their own group.

- **m372 (C6-5e) The rally.** It runs on its own clock every two to three minutes. Four trucks drive
  up the highway road and park, ten locals fill the field, and the rally man calls from his stage
  while the crowd answers. Halfway through, the Pearl's four counter-protesters march in from their
  camp by the road. It boils over into a brawl, on its own or when you throw the first punch, and
  then everyone limps home and the trucks drive off. The rally man is the Chapter 3 boss in C6-5f;
  for now he just stands on the stage.


- **m373 (C6-5f-1) Chapter 3 opens.** I split C6-5f into four builds: the opening quests, the
  motorcycle, the race for the gang's respect, and the rally man boss. The opening takes you across
  to Hollow Creek, to Pap at the trailer park (wear the farmer, since locals only talk to their own),
  to a biker's sample, and to Spud in the pits, who challenges you to race Big Rae. GOD's Chapter 3
  button now drops you at the freight pier.

- **m374 (C6-5f-2) The motorcycle.** Wearing the biker in Hollow Creek's world puts you on his
  Fat Boy, the motorcycle you rigged in m107, loaded again for the player. It rides on the
  skateboard's physics with a throttle instead of push strokes. It's faster (27 against 19), with
  no deck tricks, flips or grinds. Like Rollergirl's skates, you don't get off: change form to walk.
  **Untested on a phone:** which way it leans, whether he sits right on the seat, and whether the
  wheels spin the right way.

- **m375 (C6-5f-3) The race.** Stop at the dirt track's start gate on the bike and Big Rae lines
  up on her own bike. After a countdown you race two laps through ten checkpoints, so cutting
  across the middle doesn't count. She eases off in the bends and has a little catch-up built in.
  Win and the gang knows your name; she then points you at the rally man's stage. I tuned her to
  about 15 m/s, which a clean ride on the bike beats. Tell me if she's too easy or too hard.
- **m376 (C6-5f-4) The rally man.** At the next rally, climb the stage steps while he's speaking;
  standing by the podium counts. The thing wearing him bursts out (about twice your height, five
  knock-downs) and two of the front row turn with it. The moment it bursts, the rally breaks up and
  the trucks leave, so the fight isn't happening in the middle of a speech. Once he comes round,
  the rallies stop for good and the gang's road opens to anybody. Then the Chapter 3 complete card
  shows. Next up: Chapter 4 (The Waterfront).
- **m377 (C6-6a) The Waterfront's land.** Chapter 4 is split into six builds (the land, the factory, the cranes, the way in, the engineer form, the quests and boss). I also ticked B1 (the farm) as m329, its last part. All its sub-items were done; only the parent box had been left open. The Waterfront sits across the river south-east of Old Town, on the one side of the island nothing else was using.
  - It's a built port, not hills: concrete quays 5 m above the river, two piers, and an irregular back edge.
  - Its height comes from a dry dock you can go down into and from container stacks one to five high, laid out as cliffs with canyons between them. A "high road" of catwalks and rope bridges runs 13 m up across the stack tops.
  - The ship in the dry dock has room to walk under it. You can board it up a stair tower, or climb the scaffold on its side.
  - The factory stays shut behind its fence until the next build.
  - Walking onto its land turns the light to a sodium-orange night with fog. Tell me if that's too dark on the phone.
  - Nothing gets you there except GOD until the ferry build.
- **m378 (C6-6b-1) Inside Uplift's factory.** I split C6-6b into the hall (this build) and the conversion itself (the next).
  - The conveyor line spirals up through the hall on three levels: the floor, 5.5 m, then 10 m. One level crosses over another.
  - Every belt carries whatever stands on it, including you, at 1.3 m/s.
  - The front door stands open because it's the line's intake. The fence gate stays locked until the engineer build.
  - Without the engineer, you get in the way the finished cyborgs come out: up the outfeed tower behind the dry dock, then along the enclosed gallery over the fence.
  - The control room's red lever does nothing yet. Shutting the line down comes in the boss build.
  - If the belt stripes look like they're running backwards, that's one switch: `WFLINE.scroll`.
- **m379 (C6-6b-2) The conversion line.** Five dock workers ride the line round and round:
  - They walk in, ride all three levels, and at the chrome booth turn into cyborgs (Uplift's tint, cyborg parts, Uplift talk). They pick up the red visor at the arch.
  - They walk down the outfeed tower and stand in a line-up on the quay facing the dry dock.
  - After about 45 s, one goes back to the queue as a worker again. This only happens when you're nowhere near either end, so you never see anyone vanish.
  - The line runs 75 s, then stops 10 s with a horn. The belts stop carrying you while it's stopped.
  - Knock a rider off and they leave the line for good.
  - GOD has a stop/start switch.
  - The line also makes a thunk now and then while it runs.
- **m380 (C6-6c) The gantry cranes.** There are two cranes on the container quay.
  - Two ladders take you to the boom's catwalks, 34 m up, which run out over the river.
  - The trolley carries you if you stand on its roof.
  - Each crane moves one container forever: from a pad on the quay (a crate stair lets you climb onto it) up 20 m, out over the water, and down onto a barge (crane 1) or out along pier 2 (crane 2), then back. It swings on its cables as it moves.
  - They run on their own. Driving one yourself waits for the engineer form.
  - GOD has a stop/run switch.
- **m381 (C6-6d-1) The ferry.** I split C6-6d into the ferry (this build) and a second way over (next). Old Town's ferry landing is on the south-east shore: a ticket kiosk, a shelter, a timetable and three people waiting. A jetty runs out to a pontoon. A double-ended ferry (it never turns round) crosses about 40 m to a pontoon at the foot of a stair down from pier 1's tip, every ~50 s, with a horn. It carries you, and the fog and the night come in as you cross. The Chapter 4 button in GOD now starts at the landing. I put the landing on the Waterfront's own bearing rather than the nearest bit of shore, because the nearest shore made an 11 m crossing.
- **m382 (C6-6d-2) The swing bridge.** The second way over is a swing bridge. It leaves the container quay between the two cranes and lands on Old Town's grass down a ramp.
  - It is only a way across while it's shut. On its own clock it flashes and drops its barriers, swings a quarter turn open, waits about 20 s, then swings back.
  - If you're standing on the swinging part, you go round with it and wait mid-river until it closes.
  - I moved one Old Town ring house (287° to 274°) because it stood where the ramp lands.
  - A cyborg runs it from a control box on the quay. Operating it yourself comes with the engineer form.
- **m383 (C6-6e-1) The engineer form.** I split C6-6e into the engineer and doors (this build), the turrets, then the robots.
  - The engineer is the first form that's a role rather than a body: Uplift's engineers use the same stand-in body as the baristas, so a body alone couldn't tell them apart.
  - Sample Ivy at crane 1, or Dex on the transit shed roof. The form wheel then shows ENGINEER.
  - As the engineer, Uplift's gate slides open for you, and the swing bridge's control box swings the bridge on the spot.
  - The factory fence is now 3.4 m and wired, because at 2.6 m you could just hop it.
  - Not done: the engineer looks exactly like the hipster body (no tint, no visor). Say if that needs fixing before the boss.
- **m384 (C6-6e-2) The turrets.** Uplift's lot has four sentry guns: the two front fence corners, the factory roof's corner, and the outfeed tower.
  - Any stranger in sight gets a red laser, a beep, about a second of lock-on, then a three-round burst. Each hit does 7 damage, and moving makes you harder to hit.
  - Strangers means anyone who isn't the engineer, dock workers included.
  - The engineer turns a turret by standing at its control panel. It goes green and stays that way (saved).
  - In GOD they still shoot so you can see them, but they do no damage.
  - If they're too fierce, the numbers to change are the range (30 m), the lock time, the damage and the hit chance.
- **m385 (C6-6e-3) The security robots.** Three robots patrol the Waterfront: round the factory inside the fence, the container yard's lanes, and the lane beside the dry dock.
  - If one sees you it calls you out, runs at you, and shoves you hard (a little damage, a big push) until you're out of its sight or off its patch.
  - For the engineer they stop, face you and go green.
  - Turned turrets now shoot robots. A robot knocked down gets back up.
  - The robots use the cop's body as a stand-in, with an aerial, shoulder plates and a chest light.
  - GOD has an on/off switch.
- **m386 (C6-6f-1) Chapter 4 opens.** I split C6-6f into three: this opening; the lever that shuts the line so the cyborgs turn back; then the boss.
  - The opening goes: cross the river, talk to Rosa on pier 1, climb to Dex on the transit shed roof, take an engineer's face (sample Ivy), then walk through Uplift's gate.
  - Rosa and Dex talk to workers, so the worker form from Chapter 1 is how you start the conversation.
- **m387 (C6-6f-2) The lever.** Pull the red lever in the control room as the engineer and the line stops for good.
  - The belts stop and the factory's green screens turn red.
  - Every converted worker comes back to himself one at a time, nearest first, with sparks and a dazed line about a man in a nice suit.
  - Then you talk to Benny's cousin in the line-up (third from the left). He points you at the line supervisor: next build's boss.
  - Only the engineer can pull the lever, to match the gate.
- **m388 (C6-6f-3) The line supervisor, Chapter 4's boss.** He's a man in a suit on the factory floor by the line, there from the start.
  - Get close after the cousin's warning and the thing wearing him bursts out: nearly twice your height, five knock-downs.
  - While it stands, the robots come for everyone, even the engineer, and the turrets you turned fight on your side.
  - Afterwards he says the man in the nice suit has an office at the top of Dump Tower.
  - The robots and turrets power down for good, and you get the Chapter 4 complete card.
  - Next comes Chapter 5, the Skate Islands.
- **m389 (C6-7a) The River Islands' land.** Chapter 5 is the "Skate Islands", which REGIONS calls the River Islands. I split it into five builds: the land, what's on the islands, the wind, the ways in and out, then the quests and boss.
  - The chain is six islands due +z off Old Town, in front of the glider guy's lookout: a low landing rock, a sheer mesa, a 34 m sea stack (the needle), a long low pier island, twin hills, and a lighthouse rock.
  - There's water between every pair, because the gaps are the region's problem.
  - Ladders climb the cliffs.
  - For now only flight (the glider form) or GOD gets you there.
- **m390 (C6-7b-1) The skate park on the old pier.** I split C6-7b in two: the pier first, then the mesa, the kites and the humps. The pier is a timber deck on piles, 42 x 18 m, 3.1 m over the water, running east off the pier island. On it: a quarter pipe at the far end (4 m radius, up to 55 degrees, a steel coping, a platform to drop in from), a funbox in the middle, two kickers, a ledge up three steps, a manual pad, a flat rail on posts, railings on three sides (open to the island) and a graffiti wall. Every surface is something the board already rides or grinds. Three locals (Kai, Nova, Ruben, all `skater`) and **Rollergirl** on her own skates: she knows what you are and doesn't mind. Overrule any of it.
- **m391 (C6-7b-2) The exit point and the gap ramp.** I split C6-7b-2 again, putting the places first and the people who move (a jumping BASE jumper, the kite surfers) in C6-7b-3. **The exit point** is a deck on the mesa's cliff edge, running 5 m out over the 18 m drop. It points at the skate park, 85 m away over open water, so a glide off it has somewhere to go. It has a windsock (the wind in C6-7c will turn it) and the jumpers' shack. **The gap ramp** runs down the high hump's flank toward the mesa: a 9.6 m drop into a 25-degree kicker, with **20 m of water** to the mesa's beach. Whether a board clears it is a guess; a miss is the sea, which puts you back on the ramp. The BASE jumpers are a new ROSTER role, `basejumper`, standing in on Colin's body with a blue helmet, because CHARACTERS.md had no row for them. Overrule any of it.
- **m392 (C6-7b-3) The jumper and the kite surfers.** Sasha jumps off the exit point every 10-16 s while you are within 110 m: freefall, then a red-and-yellow canopy. She turns back toward the mesa, splashes down and swims to its beach. Then she walks round to the nearer ladder, climbs it and walks back to the deck. There's no teleport, so you can follow her the whole way (about 80 s a lap). Two kite surfers, Pia and Okon, ride loops on open water: one in the lagoon in the middle of the chain, one out by the lighthouse. Each has a board, a kite on two lines and spray, and the kite lifts them into a jump every 8-14 s. The kites hang downwind on a fixed placeholder wind (`IKITE.wind`) until C6-7c adds real wind. All the poses are clips already in Colin's and Moussa's files (freefall, hanging from the canopy, ladder, skate stance), looped on those bodies only. Overrule any of it.
- **m393 (C6-7c) The islands' wind.** One wind over the whole chain. It blows at 6 m/s toward the skate park and veers slowly, and gusts (every 5-12 s, lasting 2-5 s) swing it up to 43 degrees and add 5-11 m/s. It pushes every flight in the islands, and fades to nothing 30 m outside them. **How hard is a guess:** a jump or a board's air drifts at 16% of the wind (about 1 m per airborne second normally, nearly 3 in a strong gust); a glider or wingsuit at 45%, plus a bump up or down in a gust; Sasha's canopy at 40%. You see it coming because the floating dust streams with it, the windsock on the exit point swings round and stands out, and each gust is a whoosh. The kites hang downwind of it and the riders speed up in gusts. The chip shows `WIND<m/s>`, with a `G` during a gust. GOD has a switch to turn it off and a button for a gust on demand. Overrule any of the numbers (`mel.IWIND`).
- **m394 (C6-7d-1) The ways onto the islands.** Until now the only way onto the islands was to fly. Swimming doesn't work, because the sea puts you back on the shore you left. The second way over is three **sea stacks** in the strait with a timber deck on each and **four rope bridges** (16-22 m) from a sign on Old Town's beach to the landing rock. That's my pick from REGIONS' "a rope bridge between islands"; the other option, swimming with scuba, needs a form that doesn't exist yet. The glide from Skye's lookout now ends at a **landing field** on the landing rock: a ring of cones, a cross in the middle, a windsock and **Rue**, a second hang-glider stand-in. A flight that comes down inside the ring counts as a touchdown, and near the cross as a bullseye. Overrule any of it.
- **m395 (C6-7d-2) The thermal and the tether.** A column of rising air goes up from the needle's top. A flight in it rises at 14 m/s, and a plain jump floats. You can see it from far off: a faint shimmer, gulls circling in it, and dust streaming upward when you're inside. **I added a flight ceiling:** the wings climb by themselves, so without a cap the thermal would just be scenery. Outside a thermal, a climb now levels off at **90 m above the sea**. It applies only in the islands' world; Weirdport and the test site are untouched. The tether hangs out of a cloud bank over the needle and ends in a glowing ring **160 m** up, in the middle of the column. Reaching the ring shows "the way on" and is saved (`isl:tether`). Chapter 6 isn't built, so the card says so. Above the cloud, the **Mothership's underside** shows as a dark disc with a magenta ring. That's my call as a tease of the finale; GOD has a switch to hide it. Overrule the ceiling, the heights, or the ship.
- **m396 (C6-7e-1) Chapter 5 opens.** The chapter's story is my call; REGIONS gives the islands no villain. **The lighthouse keeper is a Skinsuit.** Since a storm in the spring, his lamp points straight up the Mothership's tether at night, guiding something in. Rollergirl is the first to say it: she's one of the hidden good aliens and talks to you as you are, which ties the easter egg in without making it a pillar. Next build: the gaps (Rue's field, the ramp's jump, the needle). After that, the keeper as the boss, with the islands' wind turned against you while he stands. The steps: get over to the islands by glide or rope bridge (first arrival also puts the region on the map), talk to Rue, talk to Rollergirl, climb to the exit point on the mesa, talk to Teo. Overrule the story.
- **m397 (C6-7e-2) The gaps.** Quest `ch5b`, Teo's three: land a flight on Rue's field, clear the gap ramp's jump, climb the needle. From the top you see the lighthouse and the tether, which lead into the boss. **The gap was barely possible as built:** at the game's gravity, a board leaving the 25-degree lip at its top speed of 19 m/s comes down 19.8 m out, right at the water's edge. So I added **a landing ramp across the gap**: a timber ramp on piles starting 13 m past the lip, with a yellow top edge, falling to the mesa's beach. Now 17 m/s or faster lands on it, and 15 m/s hits its front edge and goes in the sea. A clear counts if you leave the lip in the air and come down dry at least 12 m past it; coming down short, or being put back by the sea, doesn't. Lou moved up the beach out of the landing line. Overrule the landing's position (`IBASE.landAt` / `landDrop`) if it's too easy.
- **m398 (C6-7e-3) The lighthouse keeper, Chapter 5's boss, and Chapter 5 complete.** Quest `ch5c`. He stands at his door on lighthouse rock. While he's one of them, the lamp's beam points straight up the tether, so you can see the problem from anywhere on the islands. Get close and the thing wearing him bursts out: nearly twice your height, five knock-downs. **While it stands, the islands' wind is its** (the signature system turned against you): gusts come about every 4 s instead of every 12, blow straight at you from it, shove you on the ground as well as in the air, and the sea breaks over the rock. The shove is gentle (`IWIND.stormK` .1, about 0.65 m/s on average); walking against it beats it, but stand still on that small rock and you go in. Afterwards the keeper remembers the spring storm and what came down the line. The beam drops and sweeps the water, and you get the "Chapter 5 complete" card. GOD's Chapter 6 button now goes to the top of the needle, the thermal's foot, because the tether is where the Mothership starts. There's also a GOD place on lighthouse rock. **That finishes Phase C's chapter greyboxes (C6-7)**; next on the roadmap is Phase D (turf). Overrule the storm's strength.
- **m399 (C6-8a) Into the Mothership.** The first unchecked item was C6 ("Chapter 2 greybox... then 3, 4..."). Chapters 2-5 are done, so what keeps it open is GAME_DESIGN's last chapter, **6, the Mothership**. I added it as C6-8, split into five builds. This first one: a **pod** waits at the tether's end, 160 m up. Land on it (ride the thermal) and stand a moment, and it climbs the tether, about 18 s and 170 m through a hole I opened in the cloud, into the ship's **belly**. It docks flush in the floor of a round chamber: ribbed organic walls, a glowing organ in the ceiling, and a **glass floor** round the shaft, so you look straight down the tether at the islands. A railing round the shaft opens toward a doorway with a shut membrane (the corridors are next build). Step back on the pod to go down; left empty it goes back by itself. The pod never counts as the sea's safe spot, so a fall puts you back on solid ground. First time inside shows a "CHAPTER 6 · THE MOTHERSHIP" card. Overrule any of it, including whether the Mothership belongs on the roadmap now.
- **m400 (C6-8b) The Mothership's decks.** The belly's membrane is open now. A ribbed tube climbs 6.5 m to the **conversion chamber**: a round hall with 17 glass pods glowing green, each holding a dark shape (C6-8c puts the half-turned people in them). In the middle is the machine, a column with a turning crown of arms. The pods are all on one side, so the walk from door to door stays clear. A second tube goes down from the chamber's south door, out through the hull's bottom, to **the bridge**: a glass blister hanging 2.5 m under the ship. Its floor is glass except for the console's island, and the console faces Old Town, so Weirdport is under you and in front of you. The look is mine (purple ribbed organics, magenta glows, green pods). It's still a greybox: nobody aboard yet, and no forms needed yet (C6-8c, C6-8d). Overrule the layout.
- **m401 (C6-8c) The Mothership's people.** **Five grunts**, the evil aliens' own warriors, each on a patrol beat: round the belly's shaft, up and down the climb, the chamber's clear side, between its pods, and the bridge. They use the warrior's own brain, so they come for you. **Twelve of the city's people** stand in the chamber's pods (a hick, a hobo, a hipster, an activist, a cop, a biker and more), tinted green, swaying a little, murmuring if you talk to them. Freeing them belongs to C6-8e. **One change outside the ship:** warriors now only notice you within 8 m of their own height (and drop the chase past 13 m). Before, a grunt in the belly would "notice" you on the needle 330 m below and walk into the shaft. Street warriors on the ground behave the same, though one on a roof will no longer react to you down in the street. Overrule it if that's wrong.
- **m402 (C6-8d-1) Every form one last time, part one.** The conversion chamber has a north door now; I moved three pods out of its way. From there the way to the ship's core asks for three things, one per chapter. **The torn walkway** (Chapter 1): the tube's deck is torn through, and only the construction worker can patch it, by leaning on it the way he fixed Old Town's footbridge. **The neural lock** (Chapter 4): a membrane door that stays red and shut until the engineer walks up, then parts green. **The shaft** (Chapter 5): 11.5 m straight up with no ladder; a column of rising air carries a glider or a wingsuit up it in about 1.4 s. A jump only floats. The core is a dome on the ship's back, empty for now; the boss comes in C6-8e. Next: the activist, the biker and the farmer (C6-8d-2). Overrule the order or the stand-ins.
- **m403 (C6-8d-2) Every form one last time, part two.** The way to the core now has six gates, one for each chapter's form, in order. **The pen** (Chapter 0): a gate with a farmer's latch that swings open for anyone country (the farmer or a farmhand). **The torn walkway** (Chapter 1, the worker). **The file of the turned** (Chapter 2): the turned shuffle in a line through a green curtain, and anyone who looks like the city's own (the activist, a hippie, a hipster) can shuffle through with them. **The rumble door** (Chapter 3): an iris that opens only to an engine, so you have to *ride* up to it as the biker; on foot he's stopped. **The neural lock** (Chapter 4, the engineer). **The shaft** (Chapter 5, flight). The route turns west after the file's hall, because carried on north it put the core off the hull's back. The core is now 44 m from the hull's middle. Overrule which form any gate wants.
- **m404 (C6-8e-1) Chapter 6 opens.** The finale's story is my call. **The man in the nice suit** is the one every earlier boss pointed at: the temp agency, the stationery, the office at the top of Dump Tower. He is the Mothership's master and its final boss, in the core. Quest `ch6`: ride the tether's pod up, find the conversion chamber, and talk to **Benny** in pod 5. He's the docker whose cousin you freed in Chapter 4, and he talks to you as you are. He tells you about the suit and the six locks to the core. Then look down from the bridge. Next: the six locks as quest steps, then the boss and the end. Overrule the story.
- **m405 (C6-8e-2) The six locks as a quest.** Quest `ch6b`, after Benny: one step per gate in the order the way runs (pen, tear, file, rumble door, lock), each tip naming the form it wants and where to get it, then up the shaft to the core. GOD can start it from the quest list. The boss and the end come next.
- **m406 (C6-8e-3) The man in the nice suit, and the end.** Quest `ch6c`. The man every boss pointed at stands in the core, by the shaft's mouth. Get close and the thing wearing him bursts out: the biggest boss yet (2.4x, seven knock-downs). Afterwards he comes round. He sold insurance in Tacoma and signed something with a warm pen in an office at the top of Dump Tower, and there are floors of others still in there. That leaves Dump Tower as the hook for the metropolis core. **The turned come out of their pods** in their own colours, saying their own freed lines. **The ship goes dark**: the hull's ring, the tether's ring, the machine's crown, and the pods' glass. Then two cards: "Chapter 6 complete" and **"THE END · WEIRDPORT IS YOURS"**. The save moves to chapter 7, a free roam after the end. **That closes C6, all six chapters in GAME_DESIGN's list**, and Phase D (turf) is next on the roadmap. Overrule the ending.
- **m407 (D1) Turf: the influence model.** "Blocks" are my call: the city has no street grid recorded anywhere, so Old Town is cut into a **6 x 6 grid** over its own rectangle (about 31 m a side), named like a chess board (A1 to F6). Every block has a share for each of GAME_DESIGN's seven factions. The first shares are seeded from what's really there: the homeless camp, the food carts (small business), the building site (big business), Uplift's office, the protest and the amplifier (activists), the watcher (Skinsuits). Everyone has a little everywhere, and the shares are **saved** with your progress. Six factions hold ground at the start (no rednecks in Old Town; they're in Hollow Creek). The **full map** colours each block by its holder, stronger the clearer the lead, with its name and holder written on it; GOD → SWITCHES has a toggle. The **readout** shows `TURF <block> <holder><%>`. Nothing moves the shares yet: `turfPush` is the hook for D5. The other regions (The Pearl, Hollow Creek, the Waterfront) aren't on the grid. Overrule the grid, the seeds, or the colours.
- **m408 (D2) The crowd follows the turf.** In Old Town, each crowd spot now gets a body chosen by its block's shares: a share-weighted draw picks a faction, then one of that faction's bodies. Who stands in for whom: activists are the activist, the hippie and the hipster; rednecks the hick and the two bikers; big business the suit, the Trump body and the blonde; small business the Asian woman and the hipster; the homeless the hobo; Uplift the officer (no robot body yet); the Skinsuits the warrior. The draw is seeded by the spot, so the same street gets the same people every load. The number of bodies hasn't changed, so the frame rate shouldn't move, and outside Old Town the crowd is dealt as before. The mix is set at load, so when D5 starts moving the shares, the crowd changes on the next load. Overrule the cast list.
- **m409 (D3) Faction dressing.** What each faction hangs on a building is my call, two pieces each: **activists** a banner and a spray tag; **rednecks** a sheet hung in a window and a sign by the door; **big business** gold trim along the roof and a corporate sign; **small business** an awning and a shop sign; **the homeless** plywood over a window and a tarp on the ground; **Uplift** a screen and a camera; **the Skinsuits** a creeping tendril and a pod. Each Old Town building takes its block's holder, on up to **four** of its outside walls (picked per building, found cell by cell so an L-shaped building is dressed on its real outer walls). Every faction's set is built for every building and the ones not shown sit at zero size, so **a block changing hands cross-fades over 2.2 s**: the old faction's pieces shrink away as the new one's grow in. That's 14 draw calls for the whole town. GOD → SWITCHES has **FACTION DRESSING ON/OFF** and **HAND THIS BLOCK TO THE NEXT FACTION** (where you stand) to watch one change. No paint or decay layer yet; the props carry it. Overrule the pieces or the four-wall cap.
- **m410 (D4a) The factions' own buildings: the generator.** Built from his piece library (`toon_city_kit_pieces.glb`): `npm run twins` now also writes the intact pieces of all 16 styles into the twins file the kit city already loads (+0.68 MB), so no new download. What each faction builds is my call: **activists** a 3-storey co-op (sage or mint) with a roof garden and solar panels; **rednecks** a one-storey tin garage with roll-up bays, tyres, oil drums and a dish; **big business** an 8-storey glass tower (sky or bluecrete), all windows, a gold crown, a rooftop sign and a mast with a red light; **small business** 2-storey shopfronts (mustard or coral), wide shop openings, awnings and a water tank; **the homeless** a 4-storey walk-up (old or red brick) with plywood over some windows and tarps on the roof; **Uplift** a 2-storey concrete plant, mostly blank walls, vents and a cyan strip; **the Skinsuits** a 3-storey hive (lilac or teal) with glowing pods on the roof and tendrils up the corners. Each one uses the pieces' own colliders: doorways are open, the ground floor and roof are walkable, and the upper floors have no stairs yet. A building is 9 to 11 draw calls. GOD → SWITCHES has **BUILD A FACTION BUILDING HERE** (it cycles through the seven, one at a time) and **TAKE THAT BUILDING AWAY**. Next, D4b swaps them in on turf. Overrule the styles, sizes or extras.
- **m411 (D4b) A block held for good is rebuilt.** "For good" is my call: one faction leading a block by 12 points for **4 minutes of play** (the clock is saved). If that faction isn't the block's owner already (the one its seeds give it at the start, or the one whose building already stands there), the block **settles**. Its biggest building is marked, never the fire or police station. If it's one of **your** buildings, scaffolding goes up round it with the new owner's coloured sheeting, and it's **rebuilt the next time the city loads**: its colliders, walls, doors, ladders, markers and ivy are left out, and the faction's building goes up on its exact footprint (same cells and turn, the faction's height; a tower on a big plot stops at 6 storeys). If a **generated** building is already there, it's replaced **on the spot**. If the block's own faction takes it back for good, your building returns on the next load. Swapping your buildings only at load is deliberate: taking one apart live would touch every system that knows about it (walls, parts, ladders, the batch, the worker, fires), the same reason D2's crowd changes on the next load. GOD → SWITCHES has **REBUILD THIS BLOCK FOR THE NEXT FACTION** and, once something is pending, **RELOAD TO SEE THE REBUILDS, KEEPING MY PLACE**. The chip shows `RB<built>/<replaced>` and `s<settles>`. Overrule the 4 minutes, the 12-point lead, which building is picked, or the load-time swap.
- **m412 (D5a) What you do moves the turf.** The sizes are my call. In the block where it happens: a body **you** knock down costs its faction 1.2 points (a pal's, a brawler's or a bot's punch moves nothing); a body turned by the virus is +3 for the Skinsuits; a body cured is -3, and a Skinsuit boss exposed is -12; a worker freed of Uplift is -4 for Uplift; a rally that ends in peace is +8 for the activists, and one that ends in a brawl is -4; the crews going on strike is +5 for the activists at the building site, and the strike ending is +10 for big business. What one faction loses is spread over the rest by their shares. When a block changes hands, a toast names the new holder and why. Knock-downs aren't saved one by one; the 15-second save from D4b covers them. The chip's turf token adds `m<moves>`. GOD → SWITCHES → **YOUR ACTIONS MOVE THE TURF ON/OFF**. About ten knock-downs of hobos hands the camp's block to small business. Overrule any of the sizes.
- **m413 (D5b) Flashpoints.** Every 2.5 to 4 minutes while you're in Old Town (the first after 75 s), one faction pushes across a border: from a block it holds into a neighbouring block held by someone else. A stronger hold makes it likelier, and so does being nearer you, so you usually see it. The faction's **own bodies already on the street** near the border do it: up to 5 are recruited, given a placard (**OCCUPY!**, **RIDE FREE**, **NOW LEASING**, **OPEN!**, **WE LIVE HERE**, **UPLIFT YOURSELF**, **JOIN US**) and walk to a spot 4 m into the other block, under a ring and a light column in their colour. A toast names it, and the full map marks it with a pulsing ring and a **!**. For 60 s, every one of them standing there moves the block their way; all five unopposed is about +18 points. **Knock down 3 of the 5 and it breaks**: the holder keeps the block and gains 5 points. Each knock-down also costs them, through D5a. No new bodies are spawned, so the frame rate doesn't move, but a border with no free bodies of the attacker's faction near it never flares. The chip shows `FP <faction>><block> <seconds> <down>/<n>`. GOD → SWITCHES has **FLASHPOINTS ON/OFF** and **A FLASHPOINT NOW (THE NEAREST BORDER)** / **END THE FLASHPOINT**. **That closes Phase D**; Phase E's side quests are next. Overrule the timing, the strength, or the 3-of-5 rule.
- **m414 (E1) Element 115.** The story and place are my calls. **Rob Lazlo** lives on the roof of a four-storey walk-up on Old Town's west edge by the water (his building `kit_030`, up its own ladder on the east face, 12 m). Up there: a pallet shack **lined with tinfoil**, a wall of maps and red string inside, an antenna mast with a dish, a telescope at the sky, crates, a camp stove, and tin cans on a line. **Pockets at the camp** gives you the rumour. Lazlo won't talk to you as an alien ("I've SEEN the schematics. Off my roof."); come up disguised as somebody and the side quest opens. He points at **the man in a suit on the corner below**, who has stood there nine days without blinking: a Skinsuit, three knock-downs. Once he's beaten, Lazlo trusts you: the 115 is in a lead box in the cable drum on the **top lift of the building-site scaffold**. Reaching it makes your **juice tank hold half again as much** (it stacks with the bigger-tank gift) and fills it. The stand-in body is the skinny hick; the agent is the secret-service suit. His building is never rebuilt by turf (D4b). GOD places: `e115` (his roof) and `sitetop` (the stash). As the template for the rest of Phase E: a hidden person, a reason they won't trust you, a fight that earns it, a place to go, and an `UPGRADES` reward. Overrule the name, the building, the stash spot or the reward.
- **m415 (E2) Night Signals.** **Art Knell** does NIGHT SIGNALS on KWRD 1420 from a plywood booth on the roof of a four-storey block in Old Town's north (his `kit_010`, up its north-face ladder). Up there: a 14 m lattice **mast** with two blinking red lights (a landmark you can see across Old Town), guy wires, horn speakers aimed at the street, and an **ON AIR** sign that lights while he's talking. A **payphone** stands on the street below. Old Town has no cars, so his voice comes from **any radio**: his speakers (within about 34 m of the building), Lazlo's shack, the camp's barrel, the food carts, the farm's tractor and pickup, the payphone, and your motorcycle. In range, a line comes every 20-30 s in a bar above the pads, typed out. **Your deeds come first**: each chapter done, Lazlo trusted, a block changing hands, a flashpoint won or broken, a rebuild, the strike, the heat. Then **a sighting every third line**: the next rumour you haven't heard, marked on the map. Otherwise it's his own chatter. **The hub**: talk to Art and he gives you a sighting outright. **Call in tips**: the payphone calls in every sighting you've *found* and not called yet, for juice, and he reads it on air. His building is never rebuilt by turf. GOD has the places `radio` and `radiophone`, plus **THE RADIO EVERYWHERE** and **A RADIO LINE NOW** under SWITCHES. The chip shows `R<lines>c<calls>`. Overrule the name, the station, the building, which radios count, or the pacing.
- **m416 (F0a-1) The measure.** The chip's perf line now carries `TX<textures>/<MB>M G<MB>M boot<s>s` (what the GPU holds, and the boot from the page's start to the card going), `mel.mem()` names the biggest textures and geometries, and **`npm run worlds`** boots every world headless, stands at every region's GOD place, and prints draw calls, triangles, resident texture and geometry MB and boot time against a **budget** that is my call: 300 draw calls, 1,000k triangles, 160 MB of textures, 128 MB of geometry (one 2K RGBA map is 22 MB resident; iOS kills a tab past about a gigabyte). It exits 1 on any OVER. **Every world is OVER today.** The kit city is 370-1,700 draw calls and 1.8-3.1M triangles at every place (worst: the islands' landing, 1,713 DC; the Waterfront's container cliff, 1,463), and it holds 270 MB of textures. The biggest single textures everywhere are Moussa's two 2K maps (21 MB each, resident in every world whether or not he is in it), the HDRI (8 MB), the impact atlas (8 MB) and the fire sprites (6 MB). The fog culling only covers the kit buildings' cells (0 of 692 shown at the farm, the mill and the ship, and the draw count barely moves), so the farm, Hollow Creek, the Waterfront, the islands and the ship are drawn from everywhere. F0a-2 cuts these, worst first. The boot times are SwiftShader's (22 s for the kit city), a ratio between worlds, not a phone number. Overrule the budget.
- **m417 (F0a-2a) The far culls.** Two numbers, both mine: a body (any NPC) is not drawn beyond **150 m** from the lens (`mel.PERF.bodyFar`, 0 = always), and the kit buildings' instanced moving parts (doors, lids, AC units) not beyond **220 m** (`KIT.partFar`). `npm run worlds --who` (new: it names what draws) found 400-odd draw calls of the crowd and all 98 part sets drawn from everywhere in the kit city, the farm and the Mothership's core included, because the fog there is 950 m so the skyline reads from the farm. At 150 m a body is a dozen pixels. Result: every place in the kit city roughly halved (the landing 1,568 → 886, the core 340 → 148, the mill 381 → 77), seven of fourteen places now inside the 300-draw budget, triangles 3M → 0.9-1.6M. A side effect worth having: at the crash site the crowd's textures are never uploaded until you walk into town (GL textures 324 → 84 at boot). Still OVER: Old Town from inside (651: the cell batch and the doors), the trailer park, the container cliff, the islands (unnamed meshes, next). Overrule either distance.
- **m418 (F0a-2b) The small things, and the hand-built groups.** `--who` now says what a nameless mesh is (its geometry, material, map, vertex count) and where it stands, which named the leftovers: the cranes, the ferry, the swing bridge and Uplift's gate were built a draw call a box (128 at the container cliff), and every painted sign, glow sprite, tyre and drum was drawn from across the water. Two fixes, both mine to size: **(1)** one pass after every builder registers every mesh or sprite under **3.5 m** across to stop drawing beyond **220 m** (`mel.PERF.smallFar`, 0 = never) -- culled by render layer, so a builder that shows and hides its own thing keeps that to itself; **(2)** the hand-built groups have their plain leaves merged into one mesh per group (the colours in the vertices), moving parts staying their own groups. Like for like: the container cliff 1,192 → 680 draws, the islands' landing 1,304 → 933, the trailer park 588 → 364. The measure also sets a fixed heading at every place now (due +z where a place has none), so its numbers no longer depend on where you came from. What is left OVER is the two big static families -- the farm's batches (50-90 draws from everywhere) and the kit city's cell batches (300-400 from the islands) -- which is F0a-2c's far LOD. Overrule the 3.5 m / 220 m.
