# Alien Levels: one level at a time

## Why
The scope keeps growing from a level into a world, and then the level logic never gets the attention.
So the alien side is built as **a series of small, hand-made levels**, one at a time, each finished
before the next is started.

- **Each level is an island.** It is small and confined, with a fixed map, and every object is placed
  for a reason.
- **Each level is a puzzle box.** Five core pieces unlock its tech. The way to each core mixes
  acrobatics, a clue, technology, fighting and, sometimes, the board.
- **Each level gives you one alien tech** (the way Sunshine gives you a FLUDD nozzle). You get it
  halfway through and spend the rest of the level using it.
- **Later tech opens secrets in earlier levels**, the Zelda / Metroid way. Every level keeps three
  glyph secrets that you cannot reach the first time through.
- **The finale of each level opens the way to the next one.**

Inspirations: Mario Sunshine (the hub town, the tight dense layout, nozzle tech), Prince of Persia
(acrobatic routes), Zelda (tools that are keys, and clues read off the world).

## Player verbs (as they exist in the game now)
- Walk and run.
- **Jump**, apex 2.8 m with 1.06 s of air. At a 7.2 m/s sprint that covers about 7 m of flat gap, so
  gaps are built at 5 m (easy) or 6.5 m (needs a sprint). Ledges are built at 2.0 m (easy) or 2.5 m
  (needs a clean jump).
- Ledge grab, dodge roll, ladders and ropes.
- **Blaster** (charge or auto). **Hammer.**
- **DNA disguise**: become someone else, so guards and locals stop reacting to you.
- **Skateboard**: ollie, grinds, tricks.
- **Breakable walls.**

## Tech, one per level (draft)
| Level | Tech | What it does | What it opens |
|---|---|---|---|
| 1 Glowtide | **Hover Pack** | Hold jump in the air to hover 1.0 s with +1.0 m of lift, with a meter that refills on the ground | Gaps of 9–15 m, and ledges up to 4.4 m, overshooting a ledge, slowing a fall |
| 2 | Grapple Tether | Fire at a glowing anchor to swing or reel to it | Anchor routes, pulling down walls and doors |
| 3 | Phase Shift | Dash through violet force fields and thin walls | Sealed rooms, guard lasers |
| 4 | Gravity Boots | Walk on magnetic plates on walls and ceilings | Upside-down routes, rotating towers |
| 5 | Tractor Beam | Lift, carry and throw crates, boats and enemies | Building stairs, weighing down switches |
| 6 | Shrink Ray | Shrink yourself to Clancy size | Vents, pipes, the inside of machines |

---

# Level 1: Glowtide (the harbour plaza)

A seaside alien town on an island, with a volcano behind it. Its **beacon** (the eye on the gate
under the waterfall) has gone dark, the Goo Gang has taken the plaza, and the five beacon cores are
scattered around the town. Bring all five back to relight the beacon, open the gate, and take the
mountain path to Level 2.

## The cores (any order, except where a core needs the Hover Pack)
**1. The Market Core: fight (this is the opener).**
- You spawn on the stage, and the sunken plaza in front of you is full of goo grunts.
- The fence and the three entrances make it an arena. Clear three waves; the last one is the goo
  warrior.
- The core rises out of the fountain. The market reopens, townsfolk flood back, and the shops talk.
- *Teaches:* combat, and the plaza as the centre of everything.

**2. The Bell Core: acrobatics and a clue.**
- The bell room at the top of the clock tower is shuttered.
- **The clue:** the clock face has three coloured hands: violet, teal and amber. Each one points at a
  rooftop tower that has a small bell in the same colour:
  - the west wing tower;
  - the east quarter's spire;
  - the keep's lower roof.
- Ring the bells in that order (hit them with the blaster or the hammer). A wrong bell resets the
  sequence.
- **The route to the bell room:**
  1. Ladder from the plaza onto the west wing's 6 m roof.
  2. Ladder to the 9 m roof, then up the 15 m tower.
  3. Rope line down to the bell hall roof.
  4. Ladder up the clock tower.
- *Teaches:* reading the world for clues, and the rooftop layer.

**3. The Canal Core: disguise, a mechanism, and then THE TECH.**
- Goo guards hold the harbour bridge checkpoint and will not let the alien pass.
- Take a guard's DNA (knock one down at the harbour) and walk through the checkpoint in disguise.
- Hammer the sluice wheel on the harbour finger three times. The canals drain 1.4 m, which uncovers a
  ledge path along the main canal.
- Follow the ledges to the waterfall. Behind it is the **Tech Vault**: you get the **Hover Pack** and
  the third core.
- *Teaches:* forms as keys, environmental mechanisms, and the payoff of a hidden place.

**4. The Lighthouse Core: Hover Pack traversal.**
- The lighthouse lamp is dead, and three generator nodes along the east quarter rooftops feed it.
- Reach the dome roof and the east-quarter roofs by ladder or by jumping, then climb the east tower. Its last link is an
  11 m gap from the east tower to the pylon, which only the Hover Pack crosses (a sprint jump covers
  about 7.6).
- Blast each generator on the way. Then take the rope line from that tower to the lighthouse gallery
  and hammer the cracked slab: the core is inside the lamp.
- *Teaches:* hover distances, with switches placed along a route.

`ROUTES.txt` is the route checker's printout: every route as numbered beats, with the gap and the
rise of each one.

**5. The Keep Core: hover, and a favour for an NPC.**
- The launcher alien on the east wing's roof garden can throw you to the top of the keep, but his
  launcher needs a fuel cell.
- The fuel cell is on top of the boathouse dome:
  1. The crane cab on the pier is 2.5 m up, an easy jump.
  2. The dome rim is 3.8 m above the cab, which is out of reach without the Hover Pack.
  3. Hover up to the rim, then jump the dome's rings to the top.
- Bring the cell back. He launches you to the keep's summit, where the core is.
- *Teaches:* chaining every verb together.

**Finale.**
- Five cores go into the beacon sockets on the gate. The beacon lights, the gate opens, and the
  waterfall parts.
- The mountain path climbs to the exit portal, which leads to Level 2.

## Glyph secrets (three per level, mostly for later tech)
- **The twin tower** in the west quarter: hover onto its ledge, then hammer through the cracked wall.
- **The north-west islet:** hover across the drifting boats from the boathouse.
- **The beach hatch:** under the amber umbrella, a sewer maze runs under the plaza. Clancy sniffs it
  out, and there is a Grapple anchor in it for later.

## Layout
`PLAZA_DESIGN.md` holds the zone map, the coordinates and the player metrics.

## Marker contract (what the game reads from the export)
Every gameplay object is an **empty** in `alien_plaza.glb`. Its custom property `aw` is JSON with
the fields below. `alien_plaza_level.json` carries the same data plus the core and event logic, so
the game can use either one.

| Name prefix | `aw` fields | Meaning |
|---|---|---|
| `spawn_player` | — | Start position and facing |
| `core_N` | `core`, `name`, `hidden_until` | Core piece N, with the event that reveals it |
| `glyph_N` | `glyph`, `needs` | A secret, and the tech it needs |
| `enemy_N` | `wave`, `kind` | A plaza fight spawn point |
| `npc_N` | `role`, `line` | Townsfolk, the launcher, guards |
| `bell_N` | `order`, `color` | A rooftop bell (part of the clock clue) |
| `gen_N` | `hp` | A lighthouse generator node (shoot it) |
| `trig_*` | `event`, `size` | A trigger box (the vault, the checkpoint, the beacon sockets) |
| `mover_*` | `kind`, `from`, `to`, `on` | Something animated by an event: the bell-room shutter, the canal water level, the gate doors, the waterfall |
| `launch_pad` | `to` | The launcher NPC's target |
| `portal_exit` | `to` | The exit to Level 2 |

Colliders keep the usual prefixes: `ground_` / `deck_` are walkable, `bld_` is solid, `climb_` is a
ladder or rope, `ramp_` is a ramp.
