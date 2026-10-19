# Alien world: game import notes

Everything here is metres, Y-up (glTF). Each building's origin is the centre of its footprint at ground level, front facing -Z.

## Files
- `<building>.glb` x13: spore_pharmacy, slime_cafe, junk_repair, watch_tower_gate, residential_hut, power_shack, market_kiosk, comms_tower, fermentation_lab, landing_kiosk, noodle_bar, mushroom_inn (about 2-3.5 MB each, Draco-compressed, WebP textures)
- `alien_town.glb`: the level (ground, plaza, paths, rim spires, goo pond, crashed saucer, fence) plus about 660 scatter instances (plants, rocks, mushrooms, crystals, lamp posts, crates, flags)
- `alien_town_placements.json`: where each building goes in the level: `{building, pos:[x,y,z], rotY}`. Load `<building>.glb`, put it at `pos` and rotate `rotY` radians about +Y. (There are two residential huts.)
- `<building>_atlas_a.png` / `_atlas_b.png`: the two baked 2048 colour atlases (also embedded in the GLB)

## Inside each building GLB
Root node `<building>_root` carries `userData` (glTF extras):
- `chunks`: JSON string, a list of `{id, src, hp, nb, anchored, box}`
  - `box` = [minX,minY,minZ,maxX,maxY,maxZ] in the building's local Y-up space
  - `nb` = ids of touching chunks (the support graph)
  - `anchored` = touches the ground (chunks that lose every path to an anchored chunk should fall)
  - `hp` = 40 by default (`chunk_hp` is also on the root)
- `lights`: JSON string, a list of `{pos:[x,y,z], color:[r,g,b], intensity, range}`, meant to become PointLights (interiors, goo vats and so on)

Render meshes (each has a per-vertex float attribute `_CHUNK`; three.js GLTFLoader exposes it as `geometry.attributes._chunk`):
- `<b>_body_a` / `<b>_body_b`: everything painted, split into left and right halves, each baked into its own 2048 atlas (`<b>_atlas_a/_b.png`) for double the texel density
- `<b>_plain`: small bits and emissives (neon, lamps, rivets) with flat colours
- `<b>_glass`: transparent glass and tank liquid
- `<b>_decal`: alpha decals (rust streaks, drips, icons)

`_CHUNK` values:
- `>= 0`: the chunk id. When that chunk is destroyed, hide or collapse those vertices (or split the geometry per chunk on load).
- `-1`: core, never breaks (dark inner cores of tanks)
- `-2`: cosmetic (ivy, ferns, plants). Drop it when the nearest chunk goes.

Edges between different chunks are pre-split, so every vertex belongs to exactly one chunk.

## Colliders (in the GLB as separate meshes, don't render them)
- `col_bld_*`: solid (boxes, 12-sided cylinders for tanks, decimated meshes for big organic shapes)
- `col_deck_*`: walkable ground (level only: `col_deck_ground`, `col_deck_plaza`)
- `ramp_*`: stair ramps (a single quad from the bottom step to the landing)
- `climb_*`: ladder volumes (watch_tower_gate has one on the back of each tower, up to the bridge)
- the watch tower bridge top is `col_deck_watch_tower_gate_arch` (walkable)
- Doorways are left open in the colliders. Enterable: spore_pharmacy (right side of the storefront), slime_cafe (right side of the counter), junk_repair (garage), residential_hut (left arch), fermentation_lab (front arch), power_shack (front blast door), noodle_bar (left arch), mushroom_inn (front arch; balcony is a col_deck_ and the back ladder is climb_), bot_workshop (round hatch). The market and landing kiosks are open stalls.

## Notes / known gaps
- Textures are baked from a procedural Blender shader, and the small parts use flat colours, so the tint/detile shader setup from the Weirdport pipeline isn't used here.
- No LODs yet.
- The chunk `box` values are axis-aligned bounds of each chunk's geometry, so they're loose on curved tanks.
- Everything is unverified in-engine.


## Level v2 (terrain update)
alien_town.glb now holds a 260 x 260 m landscape around the town:
- alien_town_ground: terrain mesh (1.25 m grid) coloured by vertex colours (COLOR_0). Use a MeshStandardMaterial with vertexColors: true. It is not baked into the atlas.
- alien_town_water: river, lake and canal surfaces, using material K_water. Make it translucent in three.js if you like. It has no collider.
- alien_town_body: plaza, paths, bridges, dock, sky islands, spires and saucer, baked to alien_town_atlas.png.
- Colliders: col_deck_ground (decimated terrain), col_deck_plaza, col_deck_deck_* (walkable decks for 3 river bridges, 3 sky-island rope bridges, the dock and the sky-island tops), col_bld_wall_* (bridge railings), col_bld_* for rocks, mushrooms, lamps and features.
- Water level is y = -2.0 (canal -0.9). Treat anything below it as swimming or kill depth.
- Buildings sit at terrain height. alien_town_placements.json has the new y values and two extra copies: comms tower on the summit (about 41 m up) and power shack on the east hill.

- New building: lookout_tower.glb. Walkable decks are col_deck_*, the two stair runs are ramp_*, and the ladder from the 2nd deck up to the top pod deck is climb_*. It is placed twice in alien_town_placements.json.


## Ground textures (painted splat)
- exports/terrain/grass.png, dirt.png, rock.png, moss.png are seamless 1024 tiles. Tile them every 4 m in world space.
- exports/alien_town_splat.png (209x209) holds the blend weights: R = grass, G = dirt, B = rock, A = moss. It uses the ground mesh's UV (0..1 across the 260 m map).
- alien_town_ground also carries COLOR_0, a tint colour. Use it at about 35% strength.
- three.js sketch (MeshStandardMaterial.onBeforeCompile, fragment):
    vec4 w = texture2D(splatMap, vUv);
    vec2 t = vWorldPos.xz * 0.25;
    vec3 c = texture2D(grassMap,t).rgb*w.r + texture2D(dirtMap,t).rgb*w.g + texture2D(rockMap,t).rgb*w.b + texture2D(mossMap,t).rgb*w.a;
    diffuseColor.rgb = c * mix(vec3(1.0), vColor.rgb, 0.35);

## Faction regions
- Fire Forge (red faction): fire_forge.glb, in the south by the lake. The ground is rust tinted and the area has lava vents, scrap, banners, braziers and fuel tanks.
- Goo Warband (green faction): goo_hangar.glb plus refinery_tower.glb, in the west valley against the peak. The area has toxic pools, spike barricades, skull totems, goo barrels and pipe vents.
- Both are in alien_town_placements.json. Colliders: the forge dome and the hangar shell are box rings with their doorways open. The hangar mouth and the forge apron are col_deck_. The hangar has a climb_ ladder up to a catwalk.
- New flora (5 tree species, crystals, flowers, ribcages, rock arches, ground pipes) is instanced in alien_town.glb. Tree trunks and crystals have box colliders. Arches and ribcages have none yet.

- New buildings: fire_workshop.glb, goo_barracks.glb, border_fort.glb (placed twice). The border fort's road passes through its central tower. Walkways and side tower tops are col_deck_ and the outside stairs are ramp_.

- New building: res_complex.glb (town north terrace). Balconies and walkways are col_deck_, 3 staircases are ramp_, and the ground flat in tower B is enterable.

- Lift: alien_town_placements.json has a 'lifts' list (also alien_town_root extras 'lifts'): x, z, y_up_bottom, y_up_top, cage_size, exit_dir. Animate a 1.8 m cage platform between the two heights. The top walkway is col_deck_deck_lift_top.

- New buildings: goo_refinery.glb and fire_hangar.glb (both in placements). Catwalks and aprons are col_deck_ and the stairs are ramp_.

- Critters: exports/critters.glb holds CRIT_jelly (floating jellyfish) and CRIT_moth (glowing moth, 2 flat wings, flap them). alien_town_placements.json has a 'critters' list: type, pos (Y-up), radius, count. Spawn `count` of them wandering inside `radius`. There are 10 jelly spots over the lake and 30 moth swarms near trees.


## LEVEL SUMMARY (Oct 19)
Map: 260 x 260 m, built by scripts/aw_terrain.py. Water at y = -2.
- Town hub (centre): plaza, a raised north terrace, a walled mesa with the landing pad, 13 original buildings, the res_complex and street lamps.
- North mountains: a 41 m summit with a comms tower, 3 sky islands joined by rope bridges, a stilt village of 7 huts on the mountain trail, a cliff lift, 2 waterfalls and a river gorge with a rope bridge.
- River and lake: an arched bridge, a canal with a footbridge, a pipe bridge, a stone arch bridge, a lake dock and jellyfish over the lake.
- Fire region (south, red): fire_forge, fire_hangar, fire_workshop, a border fort on the road in, ember trees, lava vents and red signs.
- Goo region (west, green): goo_hangar, goo_refinery, refinery_tower, goo_barracks, a border fort, toxic mushrooms and pools, skull totems and green signs.
- East: the crash crater with the mothership wreck, signal_tower and a lookout tower on the east hill.
- Wild areas: 5 tree species in groves, crystal fields, ribcages, rock arches, flowers and moth swarms.
Files: alien_town.glb plus one GLB per building, alien_town_placements.json (buildings, lifts, critters) and critters.glb.

- Streets: exports/alien_streets.glb (load it alongside alien_town.glb at the same origin). It's the alien street district west and south-west of town: 5 winding streets, 6 round glyph junctions and a raised skyway on glowing pillars that passes over a junction. Materials use real tiling textures (road.png, sidewalk.png, road_glow.png) through UVMap, so they are not baked. Walkable surfaces are col_deck_deck_street_* and the skyway railings are col_bld_wall_street_* (both in alien_town.glb). Street props (lantern posts, telephone poles with wires, benches, bins, hydrants, bollards, mushroom planters) are instanced in alien_town.glb.

## SKY + LIGHTING (alien_sky.glb)
- `alien_sky.glb`: inward-facing sky dome, radius 420 m, centred on the level origin. Its material is emission-only, so in three.js swap it for `MeshBasicMaterial({ map, side: THREE.BackSide, fog: false, depthWrite: false })` and set `renderOrder=-1`. Keep it centred on the camera every frame (copy camera.position) so it never clips.
- Alternative: load `textures/sky_alien_pano.png` as an equirect `scene.background` (texture.mapping = EquirectangularReflectionMapping) and also as `scene.environment` for soft painted ambient light.
- Sun: DirectionalLight colour #FFD1A8, intensity ~2.2, direction FROM sun = (0.55, 0.35, 0.45) in three.js space (x, y-up, z). It's a low warm sun matching the glow on the pano horizon.
- Fill: HemisphereLight sky #7FD8E0 (teal), ground #6A3F86 (violet), intensity ~0.9.
- Fog: THREE.Fog colour #6B548C, near 60, far 260 (matches the pano's hazy violet horizon).
- Emissive glows (cyan/pink/amber S_glow_*) look best with a light UnrealBloomPass (strength 0.6, radius 0.4, threshold 0.85).

## KIT BUILDINGS IN THE TOWN (alien_town_kit_buildings.glb)
- 15 AlienKit buildings placed by scripts/aw_district.py (west + east street districts, fire region, goo region). Each root node `KB_<district>_<n>` has extras `kit:"alien_kit"`, `style`, `use`, `district`; children follow exports/alien_kit/ALIEN_KIT_NOTES.md (same game contract as the Weirdport building kit: _CHUNK walls, doors/glass/grille/shutter children, room_/nav_ markers).
- `alien_town_kit_buildings_collision.glb`: bld_/deck_/ramp_/climb_/solid_ colliders, root-local like alien_town.glb.
- Run Weirdport's applyDetile() on it (materials carry wk_detile "self").

## ALIEN PLAZA COAST (alien_coast.glb) -- new region south of the town (root-local y -130 .. -310)
- Delfino-style alien waterfront: ridge + tall waterfall with gate arch at the back, central canal + side canal, 9 low-poly town blocks (CB_*), bell tower with eye clock + dome (CB_bell, extras landmark), orb fountain + lawn, market stalls, mushroom umbrellas, lamp posts, palm beds, corner towers, lighthouse (east point), beach, docks + boats + sailboats (extras animate:"bob"), spore balloons (animate:"float"), sea stacks with crystals, island.
- Same LEVEL_root origin as alien_town.glb, so both line up when loaded at the same transform.
- Sea plane LV_coast_water at y=-6 (canals at -3) uses K_water; give it the same water shader as the lake.
- Terrain LV_coast_terrain: same splat shader as the town ground, splat map `alien_coast_splat.png` (R grass, G sand, B rock, A moss), with textures/terrain/p_sand.png in the G slot instead of dirt.
- `alien_coast_collision.glb`: block/bell colliders (bld_/deck_/ramp_/climb_), prop colliders from the props' cols, `bld_LV_coast_walls` (quay + canal walls), `deck_LV_coast_paving` (walkable town ground), `ground_LV_coast_terrain` (terrain).
- Unverified in game.
