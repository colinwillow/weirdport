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
| `farm_bushes.glb` | the farm hedges' bank + ico0 clumps (`FBOUND`), plus new free-standing bushes | one root per piece, origin on the ground at its centre, Blender X = along a hedge run (three x). `fb_hedge` 2.7 m (= `FBOUND.piece`), `fb_round` 1.6 m, `fb_cypress` 2.6 m tall, `fb_flower` 0.9 m with blooms | none (the hedge keeps its code box) | 41-960 per piece; hedge 740 |
| `crash_site_kit.glb` + `_collision.glb` | `buildCrash`'s furrow berms + ico0 clods, plus new debris | one root per piece, origin on the ground at its centre, Blender X = along the furrow (three x), -Y = the berm's wet face (turn it to the furrow). `cs_berm` (3.0 m tile, 4.3 m lump), `cs_clod_a/b/c`, `cs_plate`, `cs_strut`, `cs_pod`, `cs_fence` 2.4 m, `cs_grass` | `col_bld_cs_<piece>` for berm, clod_a, plate, pod, fence | 120-520 per piece |
| `farm_barn.glb` | `buildFarm`'s barn shell and silo drum | `fb_barn`: Blender X = frame u, +Y = frame +v (loft door; big doors face -Y), origin (bu, bv) at floor y0, buildFarm's exact dimensions; `fb_silo`: origin at its foot centre | none: buildFarm keeps its boxes as colliders and stops drawing them | barn 1,392, silo 414 |
| `farm_house.glb` | `buildFarmhouse`'s house shell and porch | `fh_house`: Blender X = frame u, +Y = frame +v (porch faces -Y), origin (hu, hv) at floor y0, FHOUSE's exact dimensions, chimney where `FHOUSE.chim` is | none: buildFarmhouse keeps its boxes | 4,622 |
| `farm_outbuildings.glb` | the tool shed, the chicken coop (buildFarmhouse), the lone Dutch hay barn (buildNeighbours) | three roots, Blender X = frame u, +Y = frame +v, origin on the ground at each centre, the builders' exact numbers | none: the code keeps its boxes | 448 / 322 / 3,814 |
| `neighbour_farm.glb` | buildNeighbours' tall house, cattle shed, water tower and farm shop | four roots, Blender X = the neighbour frame's u, +Y = +v, origins at the builders' centres (house on its floor y0), exact numbers | none: the code keeps its boxes and the shop's sign | 2,354 / 508 / 487 / 1,248 |
| `fair_kit.glb` | Hollow Creek's fairground: the ferris wheel (frame, spinning rotor, one car), two midway stalls, the livestock barn, the gate | Blender X = fair frame u, +Y = +v; the rotor is built in Blender XZ (axle Y) so it drops straight into the `wheel` group; the car's origin is its centre | none: the code keeps its boxes and canvas signs | 104-3,426 per piece |
| `fair_stage.glb` | the fairground's stage (deck, steps, backdrop, speakers, podium, truss, catwalk, lamps) and grandstand | Blender X = fair frame u, +Y = +v; `ff_stage` at (0, S.v), `ff_grandstand` at (20, -2), both on y, exact numbers | none: the code keeps its boxes, signs and ladder | 7,872 / 1,385 |
| `bike_pits.glb` | the dirt-bike track's pits (bikes, canopies, trailer, chest, drum, generator) and the announcer's tower | Blender X = track frame u, +Y = +v, origins on the ground at the code's centres; a bike's length is Blender Y (front +Y) | none: the code keeps its boxes and the ladder | 70-700 per piece |
| `trailer_park.glb` | Hollow Creek's trailer homes in four paints, a dish, a lawn chair, a flamingo | Blender X = across the gorge (u), +Y = along it (v); a trailer's door side is -X (turn pi for side -1), origin at its centre on the floor yp, 10 m long (scale Y by len/10) | none | 1,222 per trailer; props 68-106 |
| `mill_kit.glb` | the Hollow Creek mill's teepee burner, log crane, log truck and water tower | Blender X = mill frame u, +Y = +v, origins on the ground at the code's centres, exact numbers | none | 500-1,530 per piece |
| `container.glb` | the Waterfront's shipping containers (and the strays) | two roots (`wf_container_body` white, tinted per instance; `wf_container_trim` dark steel), origin bottom centre, X = 2.44, Y = 12.2 (doors +Y), Z = 2.6 | none: the code keeps its column boxes | 320 + 278 |
| `crash_wreck.glb` + `_collision.glb` | `buildCrash`'s hull, rim, dome, glow, panels, bow wave, wreck colliders (the furrow mounds and scorch discs stay code) | origin = the wreck's centre on the ground (`CRASH.origin`); +X = the way it was travelling, nose ploughed in (the code's `fpsi`); the furrow runs along -X | `fire_0` `fire_1` `smoke` `hatch` `clancy` `you` | 3,140 |

Next: the farm bushes (three kinds), then place by place.
