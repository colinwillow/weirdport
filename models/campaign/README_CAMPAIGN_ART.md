# Campaign art (the detail pass) -- files the scenery window owns

The campaign's scenery was typed into `index.html` as boxes and spheres. This folder replaces it piece by piece with real models.
**The scenery window owns these files; the game loop owns the code.** Each piece below has a one-build swap item in ROADMAP.md:
load the GLB at the spot the code already computes, drop the code-built version, keep the colliders from the `_collision` file.

## Contract (every file here)
- Blender Z-up, metres, glTF Y-up on export (three: (x, y, z) -> (x, z, -y)). Draco on the visual, off on the collision.
- **Origin = the piece's anchor ON THE GROUND**, and **+X = the piece's forward** (stated per piece). Scale is final; the game applies none.
- Colliders: `col_bld_*` (solid boxes, one exact box per object -- the loader turns anything else into columns) and `col_deck_*` (walkable).
- Markers are empties with the names the code already uses.
- Materials are opaque unless they are glass or a cut-out (m459: blended kit materials cost 30 fps).

## Pieces
| File | Replaces | Anchor / forward | Markers | Tris |
|---|---|---|---|---|
| `farm_pickup.glb` | `vehPickup`'s boxes (the blue pickup that runs barn -> bridge) | origin = footprint centre on the ground; forward = Blender -Y = three +z, exactly `vehParts`' model space; footprint 1.95 x 4.9 so FVEH's hw/hl still fit | -- | 2,828 |
| `farm_tractor.glb` | `vehTractor`'s boxes (the red tractor ploughing the north field, and the parked one in the barnyard if it uses `vehTractor`) | same as the pickup; plough at the back (+z behind = Blender +Y) | -- | 2,780 |
| `roadblock_kit.glb` + `_collision.glb` | `gateMesh`'s posts + tape (`cordon`) and orange/white blocks (`barricade`, `pbarricade`) | one root per piece, origin on the ground at its centre, Blender X = ALONG the line (three x), Blender -Y = the approach side (three +z, the gate's normal). `rb_sawhorse` 2.2 m, `rb_jersey` 2.0 m, `rb_fence` 2.4 m tile across `w`; `rb_car` 4.6 m parks at an end; `rb_cone` scatters in front; `rb_lightpost` one per line | `col_bld_rb_<piece>` per piece (1.25 m tall; the car 1.5) | 15-1,764 per piece |
| `crash_wreck.glb` + `_collision.glb` | `buildCrash`'s hull, rim, dome, glow, panels, bow wave, wreck colliders (the furrow mounds and scorch discs stay code) | origin = the wreck's centre on the ground (`CRASH.origin`); +X = the way it was travelling, nose ploughed in (the code's `fpsi`); the furrow runs along -X | `fire_0` `fire_1` `smoke` `hatch` `clancy` `you` | 3,140 |

Next: the farm bushes (three kinds), then place by place.
