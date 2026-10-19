# Alien Plaza: Level 1 "Glowtide" (a standalone level)

This is its own level. It is not part of the big alien map and it shares nothing with it, so load it as
its own world.

**Design:** `LEVELS.md` covers the series, the five cores, the events and the marker contract.
`PLAZA_DESIGN.md` covers the zone map and the player metrics. Both are in this folder.

## Files
| File | What |
|---|---|
| `alien_plaza.glb` | The visual. It is draco-compressed with WEBP images embedded. |
| `alien_plaza_collision.glb` | The colliders, plain glTF. |
| `alien_plaza_level.json` | Markers, events, ladders and water levels (the same data as the extras in the visual file). |

## Units and axes
- Metres. One shared origin, at the plaza fountain.
- The files are authored Blender Z-up and exported glTF Y-up, so a Blender (x, y, z) is three
  (x, z, −y). Blender +Y is north, toward the mountain. **`alien_plaza_level.json` positions are in
  BLENDER axes** (`pos: [x, y, z]`); convert them with (x, z, −y).
- Nothing is offset. The colliders are built from the same layout table as the visuals, at the same
  origin.

## What is in the visual file
- **`PL_static`:** every static mesh joined into one object, about 15 materials, so about 15 draw calls.
- **Separate objects, because the game moves, hides or hits them:**

  | Object | Role |
  |---|---|
  | `PL_canal_water` | Water level -2.0 → -3.4 on `sluice_open` |
  | `PL_waterfall` | Hidden on `beacon` |
  | `PL_sea` | -3.0 |
  | `PL_mover_shutter` | Slides up 3.2 m on `bells_rung` |
  | `PL_mover_slab` | Breakable after `lamp_powered` |
  | `PL_mover_vault_door` | Slides 5 m on `beacon` |
  | `PL_bells` | Hit targets |
  | `PL_generators` | `gen_1..3` |
  | `PL_fuel_cell` | Carryable |
  | `PL_sluice` | Spins on each hit |

- **Empties:** every gameplay marker (spawn, cores, glyphs, enemies, NPCs, bells, generators,
  triggers, movers, the launch pad, the portal). Each carries its data as JSON in the extra `aw`. The
  name prefixes are listed in `LEVELS.md`.
- **Materials:**
  - Every material multiplies its texture by the vertex colour `COLOR_0`. That is how one plaster
    sheet becomes every wall colour, so **turn on `vertexColors`**.
  - `PA_flat` is pure vertex colour (no image), and `PA_glowflat` is vertex colour used as emission.
  - `PA_winatlas` is a cut-out window sheet, so give it `alphaTest .5`. Every other material is opaque.

## Colliders (`alien_plaza_collision.glb`), using the prefixes that already work
| Prefix | Meaning |
|---|---|
| `col_deck_` | Walkable: ground, mountain, bridges, stairs, docks, canal ledges, the vault floor and the gate bridge |
| `col_bld_` | Solid boxes: buildings, parapets, towers, landmarks and props |
| `col_bld_mover_*` | Solid until its event, then moves with its visual |
| `climb_NN` | A ladder: a thin box in front of the wall face, with extras `top_z` and `face` |

**The canal ledges (`col_deck_canal_ledges`, top -2.9) sit under the water** until `sluice_open`
lowers it to -3.4.

**The rope** (west wing tower to the bell hall roof) is in `alien_plaza_level.json` under `ropes`.
Treat it as a zipline: catch it at the high end and slide down.

## Places, for GOD and for testing
| Place | Blender (x, y, z) |
|---|---|
| Spawn on the stage | `spawn_player` (0, -12, 0), facing north (+Y) |
| Bell room | (-10, 20, 15.6) |
| Waterfall vault | (0, 103, -2.9) |
| Lighthouse gallery | (100, 86, 18.4) |
| Keep summit | (67, -35, 21) |
| Boathouse dome | (-92, -22, 11.4) |
| North-west islet | (-125, 55, 1) |
| Gate terrace | (0, 88, 3) |

## Not built yet (the game decides these)
- Hover Pack physics: hold jump in the air for about 1.5 s of hover with +1 m of lift, refilled on the
  ground.
- The launcher's arc, the zipline, enemy AI, and the townsfolk models.
- The sewer under the beach hatch (glyph 3) is only a hatch for now.
