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
- [ ] **A2 Talk.** NPCs can carry a `talk` script: walk up, the right pad lights (the existing
  interact pattern), tap → speech bubble with name + lines, tap to advance. A `!` marker over the
  head of anyone with something to say.
- [ ] **A3 Quests & objectives.** Data-driven quests: steps of type talk / go-to / sample / defeat /
  reach / gate. Current objective as one line on the HUD, a waypoint beam in the world, and a
  "quest complete" moment.
- [ ] **A4 Fear & witnesses.** Humans who SEE you undisguised react: scream, flee, phone it in.
  Disguised you are ignored. A witness who phones it in raises heat.
- [ ] **A5 Heat & police.** Wanted stars. 1 = cops come look, 2 = cops chase and arrest-attempt,
  3 = cops shoot, 4 = more cops (military later). Lose heat by breaking line of sight and changing
  form. Chip shows the stars.
- [ ] **A6 The sampler.** Stand over a downed human and hold to take a sample → that form is
  unlocked into the form wheel (the existing disguise pipeline). DNA gun becomes debug-only
  (`mel.dna()` or a debug toggle).
- [ ] **A7 Form wheel.** Pick any unlocked form from a wheel (or cycle). Your own form is always
  there. The current form's abilities are what the gates check.
- [ ] **A7b Juice.** The DNA tool's juice meter on the HUD. Transforming costs juice, wearing a form
  drains it, and at zero you snap back to the alien. Juice comes from small tasks, helping people and
  beating Skinsuits. All rates are tunables on the settings panel, so he can feel them out.
- [ ] **A8 Gates.** Data-driven obstacles that check the current form: police cordon (cop),
  fire wall (firefighter), broken bridge (worker repairs it), barricade (activist inside a protest
  crowd), gap (glider). Each says what it needs when you bump into it.
- [ ] **A8b Portals.** Activatable portal points (a glowing pad). Stepping on one activates it for
  good; from any active portal you can travel to any other as yourself. The ship is the hub. Every
  place a form can reach gets one, so a disguise running out never strands you.
- [ ] **A9 Map & fog.** A full-screen map (tap the minimap) showing regions; unvisited regions are
  fogged and reveal when entered; the objective and quest givers are marked.

## Phase B — Chapter 0 and Chapter 1, playable start to finish

- [ ] **B1 The farm.** Farmland on the island ring around the kit city — small, close and layered,
  not a flat field: a sunken lane between hedges, the barn with a hayloft you can climb, a silo, a
  creek with a footbridge, the road climbing to a bridge into town. Cows as placeholders (boxes or an existing body) that moo and
  wander. The crash site: a wreck, smoke, Clancy inside.
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
