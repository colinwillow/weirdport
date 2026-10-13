# Weirdport — markers

**You place, the game behaves.** Nothing appears in the world unless it has an authored place: a
named marker in your Blender export, or an entry in an authored table in `index.html` with a named
spot and a reason. This file is the vocabulary the game reads.

## How a marker works

- A marker is an **Empty** (Plain Axes is fine; use a **Cube** empty for areas) in any of the kit city
  exports: `toon_city_visual.glb`, `toon_city_collision.glb` or `toon_city_kit_buildings.glb`.
- The game recognises it two ways, and either works:
  1. **by name**: the empty's name starts with the type and an underscore: `portal_bridge`,
     `gate_fire_alley`, `npc_hobo_camp_01`. The rest of the name is its **id**.
  2. **by custom property**: any object with a custom property `marker` set to the type
     (`marker = portal`). Then `id` (a custom property) or the object's name is its id.
- **Custom properties** (Object Properties → Custom Properties) ride along as glTF extras. Turn on
  **Include → Custom Properties** in the glTF exporter.
- **Facing**: the empty's own facing is its **−Y axis in Blender** (toward you in Front view,
  numpad 1). A custom property `yaw_deg` overrides it: 0 faces Blender −Y, 90 faces Blender +X.
- **Size**: a Cube empty's size is its **scale** (Display Size 1 means a half-width of 1 m × scale).
- Re-export, then `npm run bump`, and the markers arrive on the phone. The chip shows `MK<n>`, the
  number of markers read; `mel.marks()` lists them, and any marked `(unused)` did nothing.

## The new markers (m293)

| Type | Name pattern | Custom properties | What the game does | Status |
|---|---|---|---|---|
| **portal** | `portal_<id>` | `name` (shown in the travel picker), `hub` (true = active from the start; also `portal_ship` / `portal_hub`) | a portal pad; step on it to activate it for good, then travel between active pads | **live** |
| **gate** | `gate_<type>_<id>`, e.g. `gate_fire_alley`, `gate_cordon_bridge` | `gate` (cordon, fire, barricade, bridge, gap; defaults to the first word after `gate_`), `width` (m; else the empty's X scale × 2, else 4.5) | an obstacle across the empty's facing that only the right form passes (cop, firefighter, activist, worker mends it, glider). The empty faces the way you walk **through** it | **live** |
| **npc** | `npc_<kind>_<nn>`, e.g. `npc_hobo_01`, `npc_farmer_01` | `kind` (a file stem like `hobo_01`, or a word: farmer, cop, hobo, worker, firefighter, activist, biker, hippie, hipster, warrior), `name` (shown in the speech bubble), `talk` (a script id from `TALKS` in index.html), or `lines` (`First line\|Second line\|Third`) | one more body of that kind, standing and ambling at the marker, facing its way; with `talk` or `lines` it gets a `!` and says them | **live** |
| **spawn** | `spawn_start` (or any `spawn_*` with `start = true`) | — | where a new game begins (before you have walked into town once). Overrides the crash-site start | **live** |
| **region** | `region_<id>`, a **Cube** empty | `name` (shown on the map) | a named area on the map, fogged until you walk in. Any region marker replaces the placeholder quadrants for that world | **live** |
| **goal** | `goal_<id>` | — | a point a quest can send you to (`{ type: 'goto', mark: '<id>' }`) | **live** |
| **crowd** | `crowd_<id>`, Cube empty | `kinds` (comma list), `count` | where a crowd gathers | read and counted, **not acted on yet** (C1) |
| **protest** | `protest_<id>`, Cube empty | `side` (activists / rally), `count` | where a protest forms | read and counted, **not acted on yet** (C1) |
| **ambient** | `ambient_<what>_<nn>` | anything | ambient life: birds, smoke, a busker | read and counted, **not acted on yet** |

## The markers already in your files (read where they always were)

Counts are from `toon_city_kit_buildings.glb` as it is today.

| `marker` value | In your file | What the game does with it |
|---|---|---|
| `room` | 916 | a room a fire can start in (`KROOMS`) |
| `repair` (+ `wall_piece`) | 1,326 | where the construction worker stands to mend that wall (`KREPAIR`) |
| `fire_truck_park`, `fire_hose_stand` | 60 each | where the fire truck parks and the hose stands, per building |
| `ladder_top` | 120 | the top of a ladder, paired with its climb volume |
| any name with `truck` / `depot` (not fire) | — | the construction truck's yard (`KDEPOT`) |
| `fx_<what>_<name>` (by name, in the breakables) | — | an effect spot, e.g. `fx_hydrant_water_spout` |
| `door_in`, `door_out` | 118 each | **in your file, not read yet** |
| `ladder_bottom` | 120 | **in your file, not read yet** |
| `police_stand` | 60 | **in your file, not read yet** (a cop's post per building: the obvious place for patrols) |
| `police_spawn`, `police_car_park` | 1, 2 | **in your file, not read yet** |
| `firemen_spawn`, `fire_truck_home` | 1, 2 | **in your file, not read yet** |

## What is dormant until you place it (STEER 2)

- **Talk speakers**: no more one-random-person-per-kind with a `!`. Use `npc_*` markers with `talk`
  or `lines`.
- **The WEIRDPORT 101 stand-in quest**: off. `mel.questOn('q0')` runs it for testing.
- **Demo gates and portals**: off since m292. `mel.gateDemo()` / `mel.portalDemo()` place them round
  you on purpose.
