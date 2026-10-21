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

- [x] m797 **STEER, FROM COLIN (Oct 20, 20:35) -- DO THIS NEXT: A THIRD HERO ON THE CHARACTER SELECT, THE ALIEN GREY.**
  *"I have another new hero character. We should add it to the character selection screen... I think it might be called alien gray,
  medium."* **THE FILE:** `models/characters/alien_grey_medium.glb` (in `characters/` this time). The select is `HERO` (index.html ~917:
  `files` / `names`), so this should be one entry: `grey: 'models/characters/alien_grey_medium.glb'`, name **ALIEN GREY**, a third card,
  and `?hero=grey` working the same way as `?hero=lizard`. Run `npm run bump` so its hash is in `ASSETS`.
  **MEASURED FROM THIS SIDE (JSON only):** the same pipeline as the lizard. **61 clips, every one of zap's names present** (only
  `CINEMA_4D_Main` missing, which is dropped anyway); **all four weapon mounts**; **51 joints**; **no draco/webp** (4.6 MB raw);
  `doubleSided: true`; root `grey_export_rig` with **no scale: a METRE rig like the lizard.** His `weapon_tip_2` is (-0.157, 0, 0), so
  the mount-to-tip length is **0.157** against zap's 14.31, and the axis is pure -X like zap's (no -Z part, unlike the lizard). m794's
  measured weapon fit should therefore give him **WSC ~.011** with no rotation. Check that the chip says so; if the guns come out huge,
  the m794 fit is not reaching this rig. Same `HERO <name> n/n` clip chip as the lizard.
  **Then tick this and go back to the items below.**

- [x] m794 m796 **STEER, FROM COLIN (Oct 20, 20:22) -- TWO BUGS, AHEAD OF THE CAMPAIGN ITEMS: (1) GUNS ~100x TOO BIG ON THE ALIEN LIZARD, (2) THE DOUBLE-JUMP FLIP STUTTERS.**
  *"Due to me using a different workflow... this new workflow has made the guy have a different scale, so now he's actually fine for the
  game. He looks fine, he works fine, however when you load a rocket launcher or a blaster, the guns are about 100 times too big -- they
  take up the whole screen. And we recently implemented a double jump, and double jump is supposed to be a flip, and when you double
  jump it looks like it starts to do a flip but the animation never really fully goes, so it's like a stutter."*
  **(1) THE GUNS -- MEASURED HERE, READ STRAIGHT OUT OF BOTH FILES' JSON:**
  - **zap's armature carries `scale 0.01`** (`Armature` -> root -> hips -> ... -> `mixamorig_RightHand` -> `weapon_root_right`), so his
    mount's local units are CENTIMETRES: `weapon_root_right` t = (3.86, 7.97, -1.55), `weapon_tip_2` t = (-14.31, 0, 0). Every weapon
    file is built around exactly that pair (CLAUDE.md: "byte-identical to the character's own pair"), which is why weapons parent with
    IDENTITY on zap.
  - **the lizard's root (`lizard_export_rig`) has NO scale: his rig is in METRES.** His `weapon_root_right` t = (0.042, 0.088, -0.017)
    and `weapon_tip_2` t = **(-0.140, 0, -0.072)**: the mount-to-tip length is **0.157** against zap's **14.31**, which is 1/91. A weapon
    parented with identity is therefore ~91x too big, which is his "100 times".
  - **AND THE AXIS DIFFERS TOO**: zap's tip is pure -X off the mount; the lizard's has a -Z part (-0.072), so even at the right size
    the barrel would point ~27 degrees off. Identity is wrong on both counts for this rig.
  - **THE FIX IS A MEASUREMENT, NOT A TYPED NUMBER:** at mount time, read the WEARER's own mount -> tip vector (from his GLB, in the
    mount's local frame) and the WEAPON's own root -> tip vector (from the weapon file), and give the weapon the scale |wearer| / |weapon|
    and the rotation that turns the weapon's axis onto the wearer's. On zap that comes out scale 1.0000 and identity rotation (check
    it, and keep the chip honest), so nothing changes for him. Do NOT reintroduce a `weapFit`-style hand-typed nudge (CLAUDE.md forbids
    it); this is the same fact measured instead of assumed. Do it in ONE place that every weapon (blaster, rapid, rocket launcher,
    hammer, mace if worn) goes through, and do the left mount the same way.
  - Put the measured weapon scale in the chip (e.g. `WSC 1.00` on zap, `WSC .011` on the lizard) so a phone can tell "fixed" from
    "not loaded".
  **(2) THE DOUBLE-JUMP FLIP STUTTERS** (he saw it on the lizard; check whether zap does it too, and say which). Not diagnosed here;
  what is known from this side:
  - both rigs' `front_flip` clips are **0.875 s** long in the file, while the m97/m100 notes at `AIR.fill` in index.html reason from a
    `front_flip` of **0.667 s**. That number is stale, or it is measuring something else. Re-measure the clip and fit the air rate
    from the measured length.
  - "starts to flip and never fully goes" is the CLAUDE.md landmine shape: **a ONCE clip re-entered without rewinding, or a clip
    asked about with `isRunning()` instead of its weight, or the double-jump state re-triggering the clip every frame, or `in_air`
    taking the weight back before the flip is over.** Check where the double jump sets the flip (grep `flipAir`, `p.jumps`,
    `front_flip`), confirm the action is reset ONCE on the jump and then left to play, and that the clip's weight holds until its end
    or landing. Also confirm `front_flip` is in the clamp-when-finished list (line ~5171) for whichever rig is worn.
  - Put the flip's state in the chip while it plays (clip time / clip length, weight) so he can see it run on the phone.
  **Ship each as its own build, tick this, then go back to the items below.** Shipped unverified, as always.

- [x] m785 **STEER, FROM COLIN (Oct 20, 19:55) -- DO THIS NEXT, AHEAD OF EVERYTHING ELSE: A CHARACTER SELECT, ZAP OR THE ALIEN LIZARD.**
  *"I just created a new hero character... a bit of an automated process using Claude through the Blender MCP and scripting... I want
  to see if this workflow worked... I want to now have a character selection screen where you could choose the original character zap
  or the new hero character."* **It is a test of his pipeline: what he wants to see is whether every animation came across.**
  **THE FILE:** `models/alien_lizard.glb` (commit `0cb941e`, "added alien lizard"). It is at `models/`, NOT `models/characters/`.
  Leave it where he put it or move it into `models/characters/`, and fix the `ASSETS` hash either way (it is already in `ASSETS`).
  **MEASURED FROM THIS SIDE (read the JSON chunk; nothing decoded):**
  - **61 clips, and every name zap has is there.** Zap has 62, and the only one missing is `CINEMA_4D_Main` (residue that is dropped
    anyway). So every clip `RIG` / `MOVE` / the weapons / the board / the ledge / cover ask for by name should resolve with no
    remapping. That is the claim the test is meant to check, so do not paper over a miss: if one fails to bind, the chip says so.
  - **All four weapon mounts are present** (`weapon_root_left` / `weapon_tip` / `weapon_root_right` / `weapon_tip_2`), so the
    blaster and the rest should parent by name with IDENTITY, as on zap. Verify with `npm run rig` if a mount looks off. Do not nudge.
  - **51 joints against zap's 62.** Different rig. Anything typed against zap's bone list (a bone looked up by name for the spine,
    the head, the hips (`rig.hipY`), the ragdoll, the weapon hand) must be looked up rather than assumed. Grep for bone names.
  - **NOT compressed:** no `KHR_draco_mesh_compression`, no `EXT_texture_webp`, 4.6 MB raw (zap is 4.1 MB draco). Fine for a test.
    Bake it with `npm run ktx` (and draco) only if he keeps it.
  - **`doubleSided: true`, alphaMode default (OPAQUE).** It is the generated-asset habit. Force FrontSide the way the builders do, or
    leave it for the test and say so.
  - **Height and facing are MEASURED at load** (toes and shoulders, `RIG.height`), so a different authored size or axis lands
    right with no edit. Do not type a scale for him.
  **THE BUILD:** a **character select** before play (or on the boot card / a chip he can tap on the phone): two cards, **ZAP** and
  **ALIEN LIZARD**. The choice is saved (`SAVE` or localStorage) and switches `RIG.file` (and its `_ktx2` twin where zap has one)
  before the rig loads. A `?hero=lizard` / `?hero=zap` URL switch also works, so he can A/B with a link. Put the hero's name and a
  **clip count bound / clips asked for** in the chip (e.g. `HERO lizard 58/58`), plus the names of any clip that did not bind.
  That number is the answer to his test, so it has to be visible on the phone.
  **Then tick this and go back to the campaign items below.** No other change to the hero, the controls or the camera.

**FROM COLIN (Oct 20), OVER EVERYTHING BELOW: THE LOOP WORKS ON THE CAMPAIGN (STORY MODE, THE KIT CITY), NOT THE ALIEN LEVELS.**
*"The campaign mode was quite a bit more promising... spending the rest of my next day and a half of tokens on the loop
refining the main game is a good use of them."* He has played some of it: it needs a lot of development in how its dynamics
work. So the loop takes **Phase F** in order (F0b-2b onward, then F1 polish, F2...), and favours anything that makes the story
PLAY better (quests that hold together, fights, the feel of the systems) over new content. **The two alien STEER items below
(Glowtide's events, the big alien map) are PAUSED for the loop**: another window is building the alien levels in parallel and
owns them. Do not touch `models/alien_plaza/` or `models/alien_world/`. The levels will come together with the campaign later.

**FROM COLIN (Oct 20, 2 am), relayed by the level window because the loop was mid-pass -- take these next, in the campaign:**
*"The character text when they talk to you does this weird wrap feature: based on how you're looking at them it's always
adjusting the line wrap. Which is weird. And it would be nice if we could stylize it to look more like toon writing, comic style."*
- [x] m471 **T1. Speech text: wrap ONCE, then never re-wrap.** Lay the line out when the bubble opens (fixed width in screen px or a
  fixed character count) and keep that layout while it is on screen, whatever the camera does; only the bubble's POSITION follows
  the speaker. Then style it as a comic balloon: a white rounded balloon with a dark outline and a tail to the speaker, a
  hand-lettered comic font (a Google Font such as Bangers / Comic Neue / Patrick Hand -- pick one, put it on a switch he can
  reach), words appearing a few at a time.

*"We should add to the task list to develop the game land: stylize the scenes, a details pass, actual better geometry. When the cops
block the bridge you can just physically jump over the barricade. The truck could have better detail. Those bushes on the
farmland. The crash. All of that could be developed further -- keep doing detail passes, and if you want to hand that off to a
different context window, let me know."*
- [x] m474 **T2a. Swap in the crash wreck** (`models/campaign/crash_wreck.glb`, `crash_wreck_collision.glb`; read `models/campaign/README_CAMPAIGN_ART.md`).
  In `buildCrash`: load the GLB, put its origin at `(wx(cu,cv), g0, wz(cu,cv))` with yaw `fpsi` (its +X is the travel direction,
  nose ploughed in), drop the code-built hull / rim / dome / glow / torn panels / bow wave and the two wreck colliders, take
  colliders from the collision file, and read `CRASH.at` (fire, fire2, smoke, hatch, you) off its empties. Keep the furrow mounds,
  clods and scorch discs. The scenery window owns the art in `models/campaign/`; this is code only.
- [x] m476 **T2b. Swap in the farm pickup and tractor** (`models/campaign/farm_pickup.glb`, `farm_tractor.glb`). In `buildVehicles`
  (and wherever `vehTractor()` / `vehPickup()` are called, the parked barnyard tractor included): load each GLB once, clone it per
  use, and use the clone where the merged box mesh was -- same model space (forward +z, origin on the ground at the footprint
  centre), so `vehPlace`, `vehStep` and the hw/hl push-out keep working unchanged. Fall back to the boxes if the file fails.
- [x] m477 **T2c. Swap in the roadblock kit** (`models/campaign/roadblock_kit.glb` + `_collision.glb`). In `gateMesh`: a `cordon` is
  sawhorses tiled across `w` (2.2 m each), a police car at one end when `w` > 5 m, three or four cones scattered on the approach
  side, a work light at the other end; `barricade` is jersey barriers; `pbarricade` is the crowd fence. Their collider boxes make
  the line SOLID to 1.25 m (car 1.5), so with `GATE.hi` above that a jump over it is a deliberate act -- pair it with the cops'
  reaction (Colin: "when the cops block the bridge you can just physically jump over the barricade"). Keep the gate's own logic.
- [x] m478 **T2d. Swap in the farm bushes** (`models/campaign/farm_bushes.glb`, no collision file). Four roots, origin on the ground at
  the centre: `fb_hedge` (one 2.7 m hedge piece on its earth bank, Blender X = along the run = three x, 740 tris -- the same length
  as `FBOUND.piece`, so it replaces the bank ellipsoid + three ico0 clumps one for one; keep the hedge's own box collider and
  instance it), `fb_round` (1.6 m round bush), `fb_cypress` (2.6 m tall cone, 41 tris) and `fb_flower` (0.9 m mound with orange/red
  blooms). Scatter round/cypress/flower along the hedge lines, by the farmhouse and at field corners (Colin: "bushes on the farm
  land"); a random yaw and 0.85-1.15 scale per copy. Opaque, vertex-free plain materials (FB_*), smooth normals.
- [x] m497 **T2e. Swap in the crash-site kit** (`models/campaign/crash_site_kit.glb` + `_collision.glb`). In `buildCrash`: the furrow's
  berm ellipsoids + plank boxes become `cs_berm` tiled every 3.0 m along each side (Blender X = along the furrow = three x, its
  darker face -Y turned TO the furrow; the lump is 4.3 m long so neighbours overlap into one ridge; scale it up toward the wreck the
  way `h` grows now, `a*a`), each with its `col_bld_cs_berm` box; the ico0 clods become `cs_clod_a/b/c` (random yaw); and new
  dressing the style guide's Chapter 0 asks for: 3-4 `cs_plate` (torn hull plates) and 2 `cs_strut` along the last third of the
  furrow, ONE `cs_pod` (cracked cargo pod, purple glow -- a natural pickup spot) off to one side, 3 `cs_fence` on the crater rim
  where the furrow crossed the field's fence line, and `cs_grass` tufts round the edges. Colliders: berm, clod_a, plate, pod, fence.
- [x] m516 **T2f. (m514) Swap in the barn and silo** (`models/campaign/farm_barn.glb`, no collision file -- `buildFarm` keeps every collider).
  `fb_barn`: Blender X = the frame's u, Blender +Y = +v (the loft door), so the big doors face -v as now; origin at (bu, bv) on the
  FLOOR y0 (its plinth runs down to -1.2, so it buries itself on a slope). It is drawn at buildFarm's exact numbers (10 x 14, eaves
  5.0, ridge 7.4, walls .3, roof .6 overhang, front door 4 x 3.6 with the leaves open at +-4.0, loft door 3 wide 2.9..4.6, hook beam
  over it for the rope at v D2+.75). So: in `buildFarm` keep every `bx` of the SHELL as a collider but stop DRAWING it (the plinth,
  the walls, the door leaves and frames, the corner trims, the gables, the two roof planks and their `quad`s) and put the model there
  instead. Keep drawn: the loft floor, the bale stair, the loft bales, the outside hay stack, the rope, the lean-to, the paddock.
  `fb_silo`: origin at its foot centre (u bu+W2+3.4, v bv+D2+1.5), r 2.4/2.3, 11 m drum + red dome; replaces the drum, dome and
  rings; its ladder, landing and rails stay code. 1,392 + 414 faces, one mesh each (11 and 5 materials).
- [x] m519 **T2g. Swap in the farmhouse** (`models/campaign/farm_house.glb`, no collision file -- `buildFarmhouse` keeps every collider).
  `fh_house`: Blender X = frame u, Blender +Y = frame +v, so the porch and door face -v as now; origin (hu, hv) at the house FLOOR
  y0 (plinth down to -1.6). Drawn at FHOUSE's exact numbers: W 9, D 7, E1 3.0, E2 5.8, ridge 8.1 along u, walls .25, roof .55
  overhang, chimney at (W2+.55, +.9) topping at RIDGE+1.25 (so `FHOUSE.chim` and the smoke stay put), the windows at the `win`
  calls' places, the door and fanlight, and the PORCH (2.3 deep: board floor, four posts, rails and balusters, its roof from 2.75 at
  the wall to 2.4 at the posts). So in `buildFarmhouse` keep the shell's and porch's boxes as colliders but stop drawing them (plinth,
  walls, bands, corner boards, gables, roof slabs and cap, chimney, every `win`, the door, the porch floor/posts/rails and its roof
  slab) and keep its walkable `quad`, the steps, chairs, table, barrel, log pile, shed and coop. 4,622 faces, one mesh, 15 materials.
- [x] m520 **T2h. Swap in the shed, the coop and the lone hay barn** (`models/campaign/farm_outbuildings.glb`, no collision file -- the
  code keeps every collider). Three roots, Blender X = the frame's u, Blender +Y = +v, origin on the ground at each one's centre:
  `fo_shed` at buildFarmhouse's (su, sv) -- replaces the slab, walls, pent roof, the doorway's dark, the tools and the drum;
  `fo_coop` at (cu, cv) -- replaces the legs, hut, roof planks and ramp (the run's posts and wire stay code); `fo_haybarn` at the
  lone hay barn's frame origin (FL.FLATS[1], turned thN - .45) -- replaces the posts, eave beams and the DoubleSide roof cylinder
  (the hay steps and the round bales stay code; its roof is solid both ways, so `droof`'s DoubleSide goes). Each built at its
  builder's exact numbers. 448 / 322 / 3,814 faces, one mesh each.
- [x] m521 **T2i. Swap in the neighbour's farm** (`models/campaign/neighbour_farm.glb`, no collision file -- `buildNeighbours` keeps every
  collider, the picket fence and the shop's canvas SIGN plane). Four roots, Blender X = the neighbour frame's u, +Y = its +v:
  `nf_house` at (hu 8, hv 6) on the house floor y0 -- replaces the plinth, walls, gables, roof slabs, windows, door, stoop and
  chimney (6 x 5.5, eaves 8.6, ridge 12.8, all as built); `nf_shed` at (su -12, sv 14) on y0 = lo -- replaces the walls, posts, roof
  and troughs; `nf_tower` at (tu 17, tv 17) on g -- replaces the legs, braces, tank, cap and ladder (it has a blank painted board on
  the tank: a town name later); `nf_shop` at (pu -6, pv -14) on g -- replaces the shack, roof, counter, awning slats, crates and
  produce spheres and the two sign posts. 2,354 / 508 / 487 / 1,248 faces, one mesh each.
- [x] m525 **T2j. Swap in the fairground kit** (`models/campaign/fair_kit.glb`, no collision file -- `buildFairground` keeps every
  collider, every canvas sign, the bunting, the stage and the grandstand). Blender X = the fair frame's u, +Y = its +v. Roots:
  `ff_wheel_frame` at (W.u, W.v) on y -- replaces the four A-frame legs, their foot boxes' drawing and the red booth;
  `ff_wheel_rotor` -- built in Blender XZ with the axle along Blender Y, so in three it is ALREADY the `wheel` group's frame (plane
  XY, axle z): add it to `wheel` at (0,0,0) in place of the two torus rings and the spokes, and it spins as now; `ff_wheel_car` --
  origin at the car's centre, hanger up to +.7: one per `O.cars` entry in place of the BoxGeometry (fairStep keeps them level);
  `ff_stall_red` / `ff_stall_blue` at (-19, St.v) by `St.col` -- replace the counter, booth, canopy slats and poles (the sign plane
  stays at u+.55, 3.3); `ff_livebarn` at (bu 16, bv 22) -- replaces the barn box, its flat roof and door (gambrel roof, cupola, a
  blank name board; the pens stay); `ff_gate` at (0, gv 25) -- replaces the posts, beam and the ticket booth (the arch of bulbs sits
  BEHIND the canvas sign at +.35 v). 196 / 3,426 / 104 / 392 / 392 / 278 / 983 faces.
- [x] m529 **T2k. Swap in the stage and grandstand** (`models/campaign/fair_stage.glb`, no collision file -- `buildFairground` keeps every
  collider, the steps' and rows' boxes, both canvas signs and the truss ladder). Blender X = the fair frame's u, +Y = its +v.
  `ff_stage` at (0, S.v) on y: replaces the deck, the five steps a side, the backdrop, both pairs of speaker stacks, the podium,
  the four truss posts, both spans, the catwalk and its rails and the five lamp cans (box trusses with lacing, bunting on the deck's
  skirt, handrails on the steps, bulbs over the backdrop and down two festoons to the ground). `ff_grandstand` at (gu 20, (v0+v1)/2
  = -2) on y: replaces the rows (seat plank + footboard each, same .9 x .34), the back wall, the side walls (stepped to the rows),
  the posts and the roof -- the roof slopes LOW AT THE FRONT (-u) and high at the back. 7,872 / 1,385 faces.
- [x] m533 **T2l. Swap in the bike pits and the announcer's tower** (`models/campaign/bike_pits.glb`, no collision file --
  `buildBikeTrack` keeps every collider and the tower's ladder). Blender X = the track frame's u, +Y = its +v, origins on the ground.
  In `bike(u, v, g, r, col)`: draw `bk_bike_<red|blue|yellow>` at (u, v, g) turned r (its length is Blender Y, front wheel +Y,
  exactly the code's q(0, b) axis) in place of the two tori, the segment, the tank, engine and bars. Each pit canopy:
  `bk_canopy_<red|blue|yellow>` at (u, v) in place of the four legs and the roof slab; its chest `bk_chest` at (u+1.1, v-1), drum
  `bk_drum` at (u+1.2, v+1.1); `bk_trailer` at (pu+14, pv+1) turned .1; `bk_generator` at (pu-15, pv); `bk_tower` at (tu, tv) --
  replaces the legs, the deck, the three parapets, the corner posts and the roof (it adds X braces, a desk with the PA and mic, a
  stool and two loudspeaker horns on the roof). Faces: bike 700, canopy 130, trailer 444, tower 398, chest 214, drum 70, generator 106.
- [x] m539 **T2m. Swap in the trailer-park homes** (`models/campaign/trailer_park.glb`, no collision file -- `buildTrailerPark` keeps every
  platform, post, the walk, porch, awning, ramps, ladder, laundry and every collider). In the TRAILERS loop: draw
  `tp_trailer_<cream|tin|rust|red>` (by `R.col`) at (u + R.side*.4, v) on yp, in place of the body box, the roof, the stripe, the
  three windows and the door. It is 2.6 x 10 x 2.7 with its door and windows on Blender -X: for `R.side` +1 the walk is at -u, so
  place it unturned; for -1 turn it by pi. Scale its Y by R.len / 10. Door at Y -1.0 and windows at 0, +-3 -- the code's own
  -len*.1 and k*len*.3 at len 10. Its lattice skirt runs to -.8 under the floor. Props: `tp_dish` on the dish-and-flag trailer
  (v 1), `tp_chair` replacing the porch chair box, a `tp_flamingo` or two on the platforms. 1,222 per trailer; props 68-106.
- [x] m541 **T2n. Swap in the mill's machines** (`models/campaign/mill_kit.glb`, no collision file -- `buildMill` keeps the shed, the
  flume, both belts, the log piles, the crane's ladder and every collider). Blender X = the mill frame's u, +Y = its +v, origins on
  the ground at y: `hm_burner` at (B.u, B.v) -- replaces the open cylinder (a hooped, seamed cone with a mesh spark-arrestor dome,
  a stoking door on -X, the belt's inlet hood at 7; the smoke point stays y+9.3); `hm_crane` at (C.u, C.v) -- replaces the legs,
  the bracing bars, the platform, the cab and the boom (it adds a slew ring, a railed platform, a counterweight and a grapple on its
  cable); `hm_logtruck` at (-21, 6) -- replaces the bed, cab and chassis boxes (the five logs stay); `hm_watertower` at (9, v0-4) --
  replaces the legs, the tank cylinder and the cone (staves, hoops, a ladder). 1,530 / 500 / 1,038 / 849 faces.
- [x] m542 **T2o. Swap in the shipping container** (`models/campaign/container.glb`, no collision file -- `buildWaterfront` keeps the
  column colliders, crate stairs and ladders). Two roots, origin at the BOTTOM CENTRE, Blender X = the block's u (CW 2.44), Y = its v
  (CL 12.2), height CH 2.6; the doors are on +Y, so a box whose doors face `e` = -1 turns by pi. In the yard loop, instead of the
  painted `bx` per container and its two door lines and two bars: ONE InstancedMesh of `wf_container_body` (a single white material:
  `setColorAt` each instance with its c0..c8 paint) and ONE of `wf_container_trim` (corner posts, castings, rails, locking bars,
  hinges -- dark steel, not tinted), each instance at (cu, cv, Y + l*CH) turned Bk.yaw + yj (+pi for e = -1). The three STRAYS use
  it too. ~330 boxes x 598 faces in two draw calls.
- [x] m545 **T2p. Swap in the ship-to-shore crane** (`models/campaign/sts_crane.glb`, no collision file -- `wfCranes` keeps every collider,
  both ladders, the crate stair, the box pad, and `wfCraneParts` keeps the moving trolley, cab, spreader and box). One root,
  `wf_sts_crane`, Blender X = the frame's u, +Y = its v, origin at each crane's (K.u, 0) on Y, built at WCRANE's top 30 / boom 34.
  Place one per `C.CRANES` entry and stop DRAWING what it replaces: the legs and their sills, the portal beams, the X braces, the
  boom girders, their struts and ties, the catwalks and rails, the nose, the under-trolley beams, the A-frame and its stays, the
  machine house and its roof, both red lights, the landing and its rails. 10,378 faces, one mesh (two cranes: ~20k).
- [x] m547 **T2q. Swap in the dry-dock coaster** (`models/campaign/coaster.glb`, no collision file -- `buildWaterfront` keeps every hull
  section box, the bulwarks', forecastle's and wheelhouse's colliders, the steps, both ladders, the scaffold, the stair tower and the
  gangway). One root, `wf_coaster`, Blender X = the frame's u, +Y = its v, origin at (D.u, 0) on hb (the keel blocks' top): stern at
  Y 14, bow at 85.5, deck at 9, forecastle 1.4 higher from 70. Stop DRAWING the five hull sections and their anti-fouling and boot
  bands, the forecastle, its steps, the three hatch covers, every bulwark, the wheelhouse, its window bands, the funnel and its mast,
  and the three repair plates. 1,813 faces, one mesh.
- [x] m549 **T2r. Swap in the transit shed and the tug** (`models/campaign/wf_shed_tug.glb`, no collision file -- `buildWaterfront` keeps
  every collider, the shed's roof floor, both ladders, the pallets and drums). Blender X = the frame's u, +Y = its v. `wf_shed` at
  (Sh.u, Sh.v) on Y -- replaces the body box, the roof slab, the four doors with their jambs and slats, and the three roof vents'
  drawing (corrugated walls, a canopy over the doors, clerestory windows, gutters and downpipes, skylights, a blank name board over
  the middle doors). `wf_tug` in pier 2's own frame (turned P.psi) at pier-local (w/2+2.9, -2), on its DECK at sea+.9, bow toward
  +Y -- replaces the hull box, the foredeck, the wheelhouse and its windows and the tyre tori (a lofted hull, red below, a stack,
  rails, bitts, a mast). 2,300 / 1,031 faces.
- [x] m553 **T2s. Swap in the ferry** (`models/campaign/ferry.glb`, no collision file -- `buildFerry` keeps its moving BDYN boxes and
  `ferryPlace` moves the group as now). One root, `fy_ferry`, in the `O.grp` group's own frame: origin at the WATERLINE on the
  centre, Blender X = across the beam (7), Blender Y = along the length (18) -- double-ended, so either way round. Add it to `grp`
  at (0, 0, 0) in place of the hull, the blue band, the deck, the rails and stanchions, the cabin and its window band, the
  wheelhouse and its glass, and the two bench boxes (it has all of those at the same sizes: deck 1.25, cabin 4 x 5 to +2.6,
  wheelhouse 2.4 sq to +4, benches at +-6), plus raised end ramps, fenders, life rings, a mast with lamps. 1,904 faces.
- [x] m555 **T2t. Swap in the freight train** (`models/campaign/freight_train.glb`, no collision file -- `buildFreight` keeps every BDYN
  box, `trainPlace` / `trainStep` move the groups as now). Three roots, one per car, each in its car group's OWN frame: origin at
  rail level on the car's centre, X across, up = three y, and the export already turns Blender Y into three -z, so add each root to
  its `car.g` at (0, 0, 0) unturned: `ft_loco` in place of the frame, hood, cab, roof, stack, yellow bar and the four wheels (cab at
  three +z exactly as the code's); `ft_flat` in place of the frame, deck, two stakes and wheels (KEEP the five logs); `ft_caboose`
  in place of the frame, deck, body, cupola, roof and the two yellow bars. Each has two-axle trucks, couplers and striped end sills.
  658 / 438 / 656 faces.
- [x] m556 **T2u. Swap in the food carts** (`models/campaign/food_cart.glb`, no collision file -- `buildCarts` keeps the colliders, the
  canvas roof SIGNS and everything else in the pod). Origin at each cart's centre on the ground, Blender X along the cart, +Y its
  FRONT toward the tables, so place at (u, v, g) turned `yaw` exactly as the body box. Per cart: `fc_cart_paint` tinted with K.col
  (it is ONE white material -- clone it per cart or instance it with setColorAt) in place of the body box and the awning;
  `fc_cart_trim` in place of the roof, window, counter, wheels, hitch and sign board (the code's sign plane sits on its board's front
  at +.27, unchanged); and for `K.shut` add `fc_cart_shutter` (and skip the awning: the paint root's awning is part of it, so for
  the shut cart hide or scale it -- or say so and a separate awning root can be split out). 62 / 648 / 60 faces.
- [x] m559 **T2v. Swap in the lighthouse and the keeper's cottage** (`models/campaign/lighthouse.glb`, no collision file -- `buildIslands`
  keeps the tower's box, the cottage's, the ladder, the oil store, drums, flag, washing line, pots and rope, and IKEEP keeps its beam).
  `li_lighthouse` at (K.u, K.v) on the rock top, turned so its Blender +Y (the door) points along (cos dA, sin dA) in the islands'
  frame -- replaces the tower cylinder, both bands, the gallery deck and its torus and posts, the lantern glass and mullions, the
  lamp sphere (its lens glows at the same 12 m), the cap, the vent ball, the door, the apron and the four windows.
  `li_cottage` at (cu0, cv0) on the top, turned `cps` like its body box -- replaces the body, both roof planks, the chimney, the door
  and the two windows. 1,362 / 272 faces.
- [x] m562 **T2w. Swap in the building-site kit** (`models/campaign/site_kit.glb`, no collision file -- `buildSite` keeps the frame, the
  scaffold, every ladder and collider, the hook line and load, the stacks and cones). Blender X = the site frame's u, +Y = its v.
  `os_crane` at (mu, mv) on gm, turned so its +X (the jib) points along (cos ja, sin ja) -- replaces the pad, the mast's four
  legs and its bars, the jib box, cab, counterweights and A-frame (a lattice mast and jib, a slewing ring, pendant ties, a trolley at
  the code's 0.7 jib where the hook line already hangs); `os_office` at (ou, ov) -- replaces the office box, its roof and window;
  `os_mixer` at (3.0, sv+1.4) turned .5 -- replaces the drum cylinder and its box; `os_skip` at (-su-2.2, sv+.6) turned .1 --
  replaces the skip box; `os_hoarding` once per hoarding `bx` (2.4 wide, X along it, its street face -Y: turn the side runs and the
  far run so -Y faces OUT). 1,448 / 188 / 242 / 140 / 60 faces.
- [x] m564 **T2x. Swap in the Pearl's market stall** (`models/campaign/market_stall.glb`, no collision file -- `buildPearl` keeps the
  counter's collider and the stall positions). Origin at the stall's centre on the deck, Blender X along the counter, turned `f`
  exactly as the counter box. Per stall: `pm_stall_paint` tinted with `cc[i % 5]` (one white material: clone or instance with
  setColorAt) and `pm_stall_trim`, in place of the counter's drawing, the canopy slab, the two poles and the plant icosahedron.
  100 / 1,340 faces.
- [x] m565 **T2y. Swap in the camp kit** (`models/campaign/camp_kit.glb`, no collision file -- `buildCamp` keeps every collider, the
  patchwork roof, the junk fence, the lean-to, the washing line, the lights, the smart spots and the fire). Blender X = the camp
  frame's u, +Y = its v, origins on the ground. In `tent(u, v, rot, L, W, H, mat)`: `oc_tent_paint` (one white material, tinted with
  `mat`'s colour) and `oc_tent_trim`, scaled (L/2.8, W/2.3, H/1.5) and turned `rot`, in place of the prism and its ridge pole;
  `oc_barrel` at (0, 0) in place of the barrel cylinder (the fire point stays); `oc_sofa` at (3.6, -1.4) turned r in place of its
  four boxes (its back is on Blender -Y: if it ends up facing away from the barrel, add pi); `oc_cart` at each cart in place of its
  basket and legs; `oc_shack` at (u0, v0) in place of its three walls, roof, stovepipe. 55+120 / 614 / 198 / 386 / 304 faces.
- [x] m567 **T2z. Swap in the sentry turret** (`models/campaign/turret.glb`, no collision file -- `wfTurrets` keeps the posts and the
  panel's collider; `wfTurretParts` keeps the lens and its glow, the laser, tracer, flash and all the aiming). Each root is built in
  its THREE.Group's own frame (three y up, the muzzle along +z), so add it at (0, 0, 0) in that group unturned: `tu_base` in `grp`
  in place of the base cylinder; `tu_yoke` in `yoke` in place of the yellow box; `tu_gun` in `gun` (its origin is the trunnion,
  where `gun` already sits at .45) in place of the gun box and both barrel cylinders -- its sensor hood sits over the code's lens at
  (0, .12, .62); `tu_panel` at each `T.panel` (pu, pv, Y + ph) in place of the panel box and its yellow top (its screen faces -Y:
  turn it to face the walkway). 136 / 166 / 170 / 100 faces.
- [x] m569 **T3a. Swap in the floodlight mast** (`models/campaign/flood_mast.glb`, no collision file -- `buildWaterfront` keeps the pole's
  collider and the light cones). One root, `fl_mast`, origin at each mast's foot on Y, Blender X = the frame's u, +Y = its v, at
  every `W.MASTS` entry, in place of the pole box, the base pad, the head frame, the four lamp boxes and the ladder rungs. A tapered
  octagonal pole on a bolted flange with section joints and a hatch, a caged ladder up its -Y face, a railed grated platform on
  brackets under the head, the head frame, four floodlights tilted down and out with glowing glass at the code's lamp spots
  (the cones still come from (u, v) at top - .7), an aircraft light. 1,582 faces (eight masts: ~12.7k).
- [x] m571 **T3b. Swap in the halt's shelter and water tank** (`models/campaign/halt_kit.glb`, no collision file -- `buildFreight` keeps the
  platforms, posts, rails, stairs, bench, timetable, churns, sacks, lamps, signs and every collider). Blender X = the line frame's u,
  +Y = its v. `fh_shelter` at (pu, vm) on `deck`, at BOTH platforms -- replaces the red roof slab and its two posts (the outer edge is
  -X, as side = -1; it adds a back screen, brackets, a fretted valance, a gutter and a clock). `fh_tank` at (tu, tv) on g --
  replaces the four legs, the tank cylinder, the cone, the three tori and the spout bar (a staved tank with hoops, braced timber legs
  on pads, the spout swung out along +X with its chain and valve, a ladder). 313 / 809 faces.
- [x] m573 **T3c. Swap in the skate park hangout** (`models/campaign/skate_hangout.glb`, no collision file -- `buildIslandSkate` keeps
  every collider). Blender X = the islands' frame u, +Y = its v, origins on the deck y: `sk_sofa` at (66, 18.6) in place of its four
  boxes (back on -Y, as the code's); `sk_cooler` at (68.5, 17.2) in place of its two; `sk_speaker` at (63.8, 19.4) in place of the
  crate, the speaker box and its cone circle; and the three leaning boards -- `sk_board_paint` (one white material, tinted pink /
  paint / yel) + `sk_board_trim` at (70 + k*.9, S.v1 - .45, y + .1), tilted -1.1 about X as the code tilts its boxes. 192 / 94 /
  118 / 5+77 faces.
- [x] m575 **T3d. Swap in Rue's field** (`models/campaign/rue_field.glb`, no collision file -- the islands' m504 block keeps the rings, the
  stones, the flowers, the table's and bench's colliders). Blender X = the islands' frame u, +Y = its v, origins on the ground gT:
  `rf_canopy` at (-11, 11) in place of the four legs, the roof slab, the five valance flaps, the table, its legs, the thermos and cup
  (it adds a peaked two-tone roof, cross braces, a clipboard and a wind sock); `rf_rack` at (-14.5, 5) in place of the posts, beam
  and the three wing triangles; `rf_chalk` at (-8, 15.5) in place of its legs, board and lines; `rf_bench` at (-13, 14.5) turned
  r2 = .5 as the code's (its slats along X). 267 / 141 / 66 / 48 faces.
- [x] m580 **T3e. Swap in the dock props kit** (`models/campaign/dock_props.glb`, no collision file -- every call site keeps its colliders).
  Six roots, each on its own ground centre: `dp_bollard` (.55 high: the Pearl's two geos per bollard, and the Waterfront's quay and
  pier bollards), `dp_rope` (the torus coils), `dp_lamp` (the Pearl's rail lamps: pole + sphere + cone, its glass at 4.3), `dp_ring`
  (the life-ring tori: its own post, the ring facing +-Y, turned as the code turns the torus), `dp_pot` (the lobster-pot cylinders),
  `dp_crate` (the crate stacks at dock 1's corners and the Waterfront's pallets where they are crates). Instance them -- they repeat
  hundreds of times. 192 / 372 / 230 / 132 / 238 / 222 faces.
  - [x] m578 **T3e-1** the bollards: the Pearl's rail and dock-1 bollards and the Waterfront's quay bollards, instanced (`DPK`, `dpPut`, `dpBuild`).
  - [x] m579 **T3e-2** the rope coils and the life rings (`dp_rope`, `dp_ring`).
  - [x] m580 **T3e-3** the Pearl's rail lamps, the lobster pots and the crate stacks (`dp_lamp`, `dp_pot`, `dp_crate`).
- [x] m582 **T3f. Swap in the old car** (`models/campaign/old_car.glb`, no collision file -- the road bridge's m511 block keeps the car's
  collider). Origin at the car's centre on the road, Blender X across, +Y its front, the code's own numbers (1.8 x 4.2, body .3..1.0,
  cabin 1.6 x 2.0 at -.3 to 1.5, wheels at (+-.8, +-1.4) r .33): `oc_car_broken` at (u, v) = (-(O.w/2 - .2), L*.3) in place of the
  body, cabin, glass, four wheels, the hood and the drum (it carries a raised hood, the engine bay, a flat front tyre, steam and a
  warning triangle 3 m ahead). `oc_car` is the same car with the hood shut -- for any other place a parked car is wanted.
  765 / 575 faces.
- [x] m587 **T3g. Swap in the trestle kit** (`models/campaign/trestle_kit.glb`, no collision file -- `buildFreight`'s m509 block keeps the
  refuge's deck and rail colliders). Blender X = the line frame's u, +Y = its v. `tr_signal` at each (1.9, v) on yr -- replaces the
  mast, its board, the two lamp spheres and the bracket beam (lamps face -Y at the code's heights); `tr_milepost` at each (-1.55, v)
  on yr -- replaces the post and its board; `tr_refuge` at (ru, vm) on ry -- replaces the deck, the three braces, the rails, the tool
  chest, the cable torus, the churn and the rod (it adds a stool, a cable drum, a line in the water and two gulls on the rail).
  148 / 36 / 616 faces.
- [x] m588 **T3h. Swap in the swing bridge kit** (`models/campaign/swing_kit.glb`, no collision file -- the m510 block keeps the cool box's
  collider, the lane paint and the canvas WAIT AT RED boards). Blender X = the frame's u, +Y = its v, on Y. `sw_pitch` at (fu, v) =
  (U + hw - .35, vW + 6) in place of the two rod segments, the bucket, the stool and its legs, the cool box and its lid (it adds
  reels, rod rests, lines to the water, a tackle box, a thermos, a paper); `sw_signpost` at each board's (su, v) in place of its post,
  turned pi where the board is (its frame sits just behind the board's plane at 2.1; a red lamp on top). 246 / 66 faces.
- [x] m589 **T3i. Swap in the Mothership's pods and machine** (`models/campaign/ship_pods.glb`, no collision file -- `buildShipDecks` keeps
  every collider, the pod GLASS (`D.podMat`, so it can still pulse) and its sleeper capsule, the cable to the ceiling, the turning
  crown, the floor and walls). Origins on the chamber floor yC. `ms_pod` at each pod's (u, v) in place of the base box and the cap
  box only (its claws hold the code's glass, its cap's socket is where the code's cable starts at 2.95); `ms_machine` at (C.u, C.v)
  in place of the column cylinder -- it cradles the code's glow sphere at 3.2 in an open cage (keep the sphere). 564 / 1,188 faces.
- [x] m591 **T3j. Swap in the Mothership bridge's console, chair and holo pedestal** (`models/campaign/ship_bridge.glb`, no collision file
  -- `buildShipDecks` keeps every collider, the floor ring, the glow dots, and `D.holo`'s turning globe and band). `mb_console` at
  each of the five desk segments' (u, v) on yB, turned -a + pi/2 like the desk box (its operator side and screen face its local +Y:
  if the screens end up facing out over Old Town instead of at the chair, add pi), in place of the desk box and the screen box;
  `mb_chair` at (B.u, B.v + .6) in place of the two shade boxes (it faces -Y, out over the console); `mb_holo` added to `D.holo`
  at (0, 0, 0) in place of its base cylinder (the pedestal runs -1.3 to -.4 under the code's globe). 72 / 228 / 342 faces.
- [x] m596 **T3k. Swap in the Mothership belly's eggs, glyphs and tendrils** (`models/campaign/ship_belly.glb`, no collision file -- the m507
  block keeps the seams, the glow ring and the veins; nothing here is solid). `mb_eggs` once per clutch at (cos a, sin a) * (R - 1.1)
  on y, X along the wall (turned -a + pi/2), in place of its five spheres; `mb_glyph` once per panel at (cos a, sin a) * (R - .3) on
  y, turned so its -X face looks into the room, in place of its three thin glow bars; `mb_tendril` per tendril at its ceiling root
  (y + S.H), Z scaled by L / 1.6, in place of the cylinder and its tip sphere. 1,408 / 254 / 134 faces.
- [x] m597 **T3l. Swap in the farm props** (`models/campaign/farm_props.glb`, no collision file -- `buildFarmProps` keeps every collider,
  the windpump's head group and tail, the tractor). Blender X = the farm frame's u, +Y = its v, on the ground. `fp_windpump` at
  (wu, wv) in place of the four legs, the girts and the platform (it adds bracing, a ladder, the pump rod, a pump and a trough);
  `fp_wheel` added to `wheel` at (0, 0, 0) in place of the 14 blade boxes and the torus -- it is built in Blender XZ with the axle
  along -Y, which is three's XY with the axle on z, the wheel group's own frame; `fp_scarecrow` at (su, sv) in place of its post,
  bar, shirt, sleeves, head, hat brim and crown; `fp_barrel` at each barrel (u, v); `fp_barrow` at the wheelbarrow, turned .4 (its
  tray, straw and tyre). 486 / 410 / 466 / 224 / 134 faces.
- [x] m599 **T3m. Swap in the MX track kit** (`models/campaign/mx_track.glb`, no collision file -- the m498 block has no colliders and keeps
  its ruts and tape). `mx_arch` at the midpoint of L and R on the ground, its span (Blender X) along L -> R, in place of the two posts,
  their tyre cylinders and the top bar (the code's canvas banner hangs in front of its yellow backing at 4.3); `mx_flag` at every flag
  in place of the pole and the cone pennant -- its pennant is ONE white material, tint it with the flag's `cols[k % 4]`, turned so
  it flies the way the code's cone does (+X); `mx_tyres` for the turns' tyre walls and the pits (where a stack of tyre cylinders is
  drawn). 2,579 / 35 / 468 faces.
- [x] m601 **T3n. Swap in the farm trees** (`models/campaign/farm_trees.glb`, no collision file -- keep `farmTree`'s trunk box collider as
  it is). In `farmTree(F, rr, ico1, u, v, s, k)` draw `ft_oak` (or `ft_willow` where the code draws its willow) at (u, v, ground),
  origin on the ground, scaled uniformly by `s` and turned by the same random yaw, in place of the trunk cylinder, the two limbs and
  the ico crown blobs. Both are built at s = 1 to the code's numbers: trunk to 3.4 m (willow 2.6), crown centred 1.9 m above it.
  Instance them (one InstancedMesh per piece) -- every farm and roadside tree shares this one builder.
- [x] m603 **T3o. Swap in the trailer park's rim props** (`models/campaign/rim_props.glb`, no collision file -- keep the three code boxes as
  colliders, just hide them). In `buildTrailerPark`'s THE RIMS block: `rp_barrel` at the drum's (u, v, g) in place of the 'drum' box
  (the tame fire still starts at g + 1.0, which is just above its embers); `rp_pickup` at (pu, pv, pg), its nose along +v, in place
  of the two 'red' boxes and the 'post' box (it sits on four cinder blocks, no wheels -- they are in its bed); `rp_pole` + `rp_flag`
  at (fu, 1, fg) in place of the steel box and the plane -- the flag flies along +v off the pole at 4.9..5.9 like the plane did;
  it is ONE white material, tint it with the 'flag' colour. The barrel also fits any other burn barrel (gate, camp, gang bridge).
- [x] m605 **T3p. Swap in the Pearl's roof gardens** (`models/campaign/roof_garden.glb`, no collision file -- keep `pearlGarden`'s boxes as
  colliders, hidden). All in the warehouse's frame: X = the code's a, Blender +Y = its b, turned by `W.yaw`. `rg_bed_veg` /
  `rg_bed_flower` (alternate by the seed) at each bed's (ja, jb, y), scaled X by w2 / 2 (built 2.0 x 0.9 x 0.5, soil at .5), in
  place of the 'bed' and 'soil' boxes AND the ico plants -- the plants are in the model. `rg_tank` at the tank's corner (the 2.2 m
  stand, legs to 1.2, the drum to 3.0, lid to 3.1) in place of the four legs, the steel box and the 'tank' cylinder. `rg_pergola`
  at the pergola's (a, b, y) in place of its four posts, seven slats AND the bench box -- the bench is in it at +.4 in b.
- [x] m607 **T3q. Swap in the kit town's roof extras** (`models/campaign/roof_extras.glb`, no collision -- these were never colliders). In
  `kgenMake`'s `S.extra` block, through the same `add` (so they ride `Bm` and merge per material): Blender (x, y, z) is the block's
  (u, -v, h). `garden`: `rx_bed` at (u, roofH, v) in place of the wood box, the soil box and the three ico leaves (the plants are in
  it); `rx_solar` at (cu - .9 + k * 1.8, roofH, -D + 1.1) in place of the tilted 'solar' box and its post -- built tilted the same
  way, the post .3 toward +v. `tank`: `rx_tank` at (W - 1.6, H, -D + 1.6) in place of the drum, the cone and the four legs.
  `vents`: `rx_vent` at each vent's (u, roofH, cv) in place of the 'vent' box and its 'glow' lid. `scrap`: `rx_tyres` at
  (W - 1.2, roofH, -1.2) in place of the four tori.
- [x] m608 **T3r. Swap in the Pearl's dock props** (`models/campaign/pearl_dock.glb`, no collision -- keep every collider box as it is). In
  `buildFootbridge`'s dock, Blender X = u, +Y = v, origins on the dock (yP): `pd_pot_paint` (ONE white material, tint it with that
  pot's pot1/2/3 colour) + `pd_pot_plants` at each of the five pots, in place of the cylinder, the torus rim, the three icos and the
  four bloom spheres; `pd_planter_paint` (tint pot2 / pot1; built 1.8 square, scale X .89 for the 1.6 one) + `pd_planter_plants`
  at (cu - 1.8, cv) and (cu + 1.6, cv) on the container's roof (yP + 2.6), in place of the two 'pot' boxes and the leaf clumps;
  `pd_crates` at (-dW + 2.6, vL0 + 1.6) in place of the three crate boxes and the sack sphere; `pd_chalkboard` at
  (dW - 2.4, vL0 + 1.4) turned by r = -.3 in place of its legs, board and chalk lines (its face is -Y).
- [x] m611 **T3s. Swap in the gang's road bridge** (`models/campaign/gang_road.glb` plus pieces already shipped; no collision -- keep the
  boxes). In `buildHighway`, Blender X = u, +Y = v, origins on the deck at yv(v): `gr_distsign` at each distance sign's (su, v)
  turned like its canvas plane (face +Y = the plane's front), in place of the two 'rail' posts -- keep the canvas plane, nudged
  .01 in front of the green board; `gr_gangsign` at (hw - .2, gv - .5) in place of the 'dark' post, the LOCALS ONLY plane sitting
  on its ply sheet (sheet 1.3..2.3 up, face +Y); `gr_cooler` at (5.0, gv + 3.4) in place of the 'line' box and the five can
  cylinders; `gr_pennant_paint` (tint it truck / line / dark by k % 3) + `gr_pennant_string` at each of the 20 cones, in place of
  the cone. Already in the repo: `rp_barrel` (rim_props) for the 'drum', `rp_pickup` turned across the lane for the two 'truck'
  boxes, `tp_chair` (trailer_park) for the two chairs, `bk_bike` (bike_pits) for the two bikes, `rx_tyres` (roof_extras) for the
  tyre stack.
- [x] m613 **T3t. Swap in the rest of the camp** (`models/campaign/camp_extras.glb`; no collision -- keep the boxes that collide). In
  `buildCamp`, Blender X = u, +Y = v, origins on `gnd(u, v)`, each turned like the box it replaces: `ce_pallet` (1.2 x .14 x
  1.35 from -.1) at each of the six pallet-wall boxes; `ce_sheet_rust` / `ce_sheet_tarp` (1.2 x 2.4 from -.1, scale Z by
  (h + .1) / 2.4) at the seven back sheets ('rust' / 'tarp2'); `ce_leanto` at (-4.6, -7.7) in place of both tarps, the two poles
  and the 'mat' box; `ce_crate` (.6 cube from -.05, scale Z by (h + .05) / .65) at the four crates and the three seat crates (scale
  X .55/.6, Y .45/.6 for those); `ce_cardboard` (1 x 1, scale X by w, Y by d) at the three cardboard boxes; `ce_bottle` at the six
  bottle cylinders (lying ones turned on their side); `ce_laundry` (ONE white material, tinted with cols[i]) hanging from the line
  at each of the five laundry boxes -- its origin is ON the line.
- [x] m617 **T3u. Swap in the camp's roof and fence** (`models/campaign/camp_roof.glb`; no collision -- keep the boxes that collide). In
  `buildCamp`'s m489 block, Blender X = u, +Y = v: `cr_roof` ONCE at (0, gnd(0, 0), 0) in place of the four posts and the four
  patch sheets (its posts stand at the code's P4, the +u side .3 higher); the junk fence's panels by kind -- 'door' -> `cr_door`,
  'wood' -> `cr_planks` (both 1.0 wide from -.1: scale X by L / n * .95 and Z by (h + .1) / 2.0 for the door, / 1.8 for the
  planks), 'rust' / 'tarp2' -> `ce_sheet_rust` / `ce_sheet_tarp` (camp_extras), each turned like its box; `rx_tyres` (roof_extras)
  for the three tori; `cr_herbs` at the four herb tins in place of the tin and its ico; `cr_bucket` in place of the bucket.
- [x] m619 **T3v. Swap in the Pearl's plaza** (`models/campaign/pearl_plaza.glb`; no collision -- keep every box that collides). In
  `buildPearlPlaza`, Blender X = u, +Y = v, origins on y: `pp_stage` at (T.u, T.v) in place of the 'plat' box and the two
  'steel' poles (its poles stand at +-2.3, +Y 1.65; the banner stays the code's; its steps are at -Y, the plaza side). The
  barricade junk by kind, each turned by j like its box: 0 -> `pp_pallets` (1.3 x 1.1, scale Z by h / 1.2); 1 ->
  `pp_dresser_paint` (ONE white material, tint pink / mint / cream) + `pp_dresser_trim`; 2 -> `pp_drums` in place of the two
  cylinders; 3 -> `oc_sofa` (camp_kit) or `sk_sofa`; 4 -> `pp_crates` (its top crate already turned .4). `pp_bed` at each of the
  twelve corner beds in place of the wood and soil boxes, the stems, the discs and the leaves. Bunting: `gr_pennant_paint` +
  `gr_pennant_string` (gang_road) at the pennants.
- [x] m622 **T3w. Swap in the food-cart pod's dressing** (`models/campaign/cart_pod.glb`; no collision -- keep the boxes that collide). In
  `buildCarts`' m488 block, Blender X = u, +Y = v: `cp_table` + `cp_umbrella_paint` (ONE white material, tint umb / umb2 / umb3) +
  `cp_umbrella_ribs` at each table's (u, v, deckTop) turned by r, in place of the top, the leg, the benches, the pole, the cone and
  the napkin box; `cp_sail` ONCE at (0, deckTop, 0) in place of the two posts and the sail box (its posts stand at the code's
  (-3.4, 5.6) and (3.6, .6); the sail clears the umbrellas); `cp_planter` at the three potted plants on the deck in place of pot +
  ico; `cp_gas` at each gas bottle; `cp_bin` at each cart's bin; `cp_generator` at (0, -9.4) in place of the 'dark' box; the
  crates behind the carts -> `ce_crate` (camp_extras) scaled to .6 x .5 x .48.
- [x] m623 **T3x. Swap in Dump Tower's floors** (`models/campaign/tower_floors.glb`; no collision -- keep every box that collides). In
  `buildDumpTower`'s "what the floor is for", Blender X = u, +Y = v, origins on the floor f. LOBBY: `dt_lobbydesk` at (3, 3) in
  place of the gold desk and the dark name wall (the wall is in it at +.7); `dt_lobbysofa` at (+-6, -6); `dt_urn` at (+-8.5, -8.5)
  in place of the gold cylinder and the plant sphere. OFFICES: `dt_desk` at each (u, v) in place of top, base and screen (its
  chair is in it at -.75). GYM: `dt_treadmill` at (-1 + c * 3, -7.5) (its console at -Y) in place of both boxes; `dt_weights` at
  (1 + c * 3, 5) in place of the 'carpet' box. GARDEN: `dt_tree` at each of the six in place of soil, trunk and ico; `dt_bench` at
  the six benches. BOARDROOM: `dt_boardtable` at (2, 0) in place of top and base; `dt_execchair` at each chair, turned to face
  the table (s2 = -1 -> +pi/2, +1 -> -pi/2). PENTHOUSE: `dt_whitesofa` at each sofa turned by r; `dt_coffeetable` at (4, -1);
  `dt_coins` at the three gold cylinders.
- [x] m624 **T3y. Swap in Dump Tower's roof and lift** (`models/campaign/tower_top.glb`; no collision -- keep the boxes that collide). In
  `buildDumpTower`, Blender X = u, +Y = v: `dt_helipad` at (2, ry, 1) in place of the pad cylinder, the four white strips and the
  sixteen lamp spheres (it adds a windsock off the +u edge); `dt_rail` (1 m long, scale X by w or d) along each of the four
  roof-edge rails, turned along its run, in place of the two gold boxes each; `dt_lift` at (LU, LV, f) on every floor in place of
  the three glass walls, the four posts, the crown, the carpet and the call panel (its open side is -X, the panel outside it at
  (-1.25, -1.6)). Keep the glass walls' colliders.
- [x] m626 **T3z. Swap in the kit town's other roof extras** (`models/campaign/roof_extras2.glb`; no collision). In `kgenMake`'s
  `S.extra` block through `add`, Blender (x, y, z) = (u, -v, h): `pods` -> `rx_pod` at each pod's (u, roofH, v), scaled uniformly
  by s and turned by its random yaw, in place of the sphere (its origin is the roof; the code's sphere centre is .5 s up);
  `squat` -> `rx_tarp` at each tarp in place of the tilted box, and `rx_ply` at each boarded window in place of the 'ply' box
  (face -Y, so turned to face out of the wall; keep its small z tilt); `crown` -> `rx_crownsign` at (cu, H + 2, -D + .4), scaled
  X by W * .7, in place of the dark board and its gold panel (the four gold edge strips stay); `rx_mast` at (W - 1, H, -1) in
  place of the mast cylinder and its lamp sphere (`crown` and `vents` both have one).
- [x] m628 **T4a. Swap in the gorge's stilt houses** (`models/campaign/stilt_village.glb`; no collision -- keep the platform and wall boxes).
  In `buildGorgeVillage`, each house in a LOCAL frame: origin at (AU(b, s, dC), Wy, b) -- the platform's top at the house centre;
  local +X = +d (away from the river, toward the walk and the door), local +Y = +b. Because AU flips u with s, a house on s = 1
  needs scale.x = -1 (so +X runs to -u) and one on s = -1 needs none; then turn by ps. `sv_platform` in place of the platform box
  (its four corner posts stop at -.6; the code's stilts to the bed stay); `sv_house_wall` (ONE white material, tint wall_k) +
  `sv_house_roof` (ONE white material, tint roof_k) + `sv_house_trim` in place of the walls box, the cone roof, the door, the
  window, the lamp, the rack posts and bar, the fish and the net. `sv_boat` at (AU(b + 2.6, s, 1.6), sea, b + 2.6) turned by ps
  (its mooring line runs up 3.2 m) in place of the 'boat' box.
- [x] m630 **T4b. Swap in the gorge dam's works** (`models/campaign/gorge_dam.glb`; no collision -- keep the boxes that collide; the
  concrete wall itself stays the code's). In `buildGorgeDam`, Blender X = u, +Y = +b (the downstream face is -Y): `gd_winch` at
  (U(hu), top, b0) in place of the tin box and the rust roof (its door faces downstream); `gd_wheel` at (U(wa), top, b0) in place
  of the yellow torus, its post and the dark grate (the wheel is at -.3 Y, as the code has it); `gd_sluice` at each mouth's
  (U(ra +- 2.4), bed + .3, b0 - 1.12) in place of the dark mouth and the rust lintel; `gd_rail` (1 m, scale X by 2 hw) along both
  crest rails at b0 +- 1.05 in place of the two steel boxes each, plus `gd_post` every 2 m along each (never scaled).
- [x] m632 **T4c. Swap in the fjord's grotto and wreck** (`models/campaign/gorge_deep.glb`; no collision -- keep the bulk box and the
  cache/strongbox boxes; the grotto's rock roof and pillar stay the code's). In `buildGorgeDeep`, Blender X = u, +Y = +b:
  `gw_wreck` at (U(ra), fy, b) in place of the keel, both hull sides, the five ribs, the wheelhouse and the stern -- she is
  already rolled (.9 about her keel, which runs along Y) and holed, kelp standing up off her; the mast cylinder stays. `gw_crystals`
  at a few of the sixteen crystal points (each clump is ~7 of the code's cones) in place of the cones, turned by the code's yaw;
  `gw_cache` at (U(ca), cy, cb) in place of the wood box, the steel lid and the gold box (the gold spill is in it at +X);
  `gw_strongbox` at (U(sa), sy, sb) in place of the steel box and its gold band. Keep the PointLight.
- [x] m635 **T4d. Swap in the fjord lookout** (`models/campaign/gorge_look.glb`; no collision -- keep the legs', deck's and rails'
  boxes as colliders). In `buildGorgeLook`, Blender X = u, +Y = +b: `gl_tower` at (u, g, b) in place of the eight leg boxes, the
  girts, the deck, the three rails, the four roof posts and the roof (its legs run from -.6 to the deck at 14, splayed 1.9 -> 1.45
  like the code's; X-braces; the rail is open at +Y for the ladder, which stays the code's); `gl_foot` at (u, fg, fb) in place of
  the bench, the tin chest, the rack posts and bar and the sail cone (bench at -1.6, chest at +1.4, rack and folded sail at +2.6).
- [x] m637 **T4e. Swap in the long flume** (`models/campaign/gorge_flume.glb`; no collision -- keep the `quad` floor and the wall boxes).
  In `buildGorgeFlume`, per segment P -> R: `fl_trough` + `fl_water` at the segment's midpoint, (P.y + R.y) / 2, turned by psi
  and pitched by atan2(R.y - P.y, L), scaled Y by L / 2 (built 2 m along +Y, the floor's top at -.05 like the code's plank, inner
  width 1.5 = 2 hw, walls .6, a yoke every metre), in place of the two plank `pearlSeg`s, the water `pearlSeg` and the two wall
  `pearlSeg`s; the trestle posts and cross beams stay the code's. `fl_head` at (bu, y0, bv) with +Y down the flume (psi =
  atan2(ux, uz)), in place of the deck box, the side rails and the tank cylinder (the legs stay the code's).
- [x] m640 **T4f. Swap in the pirate radio** (`models/campaign/radio_kit.glb`; no collision -- keep the booth's wall boxes and the three
  leg-foot boxes; the booth's plywood walls, its window and the ON AIR sign stay the code's). In `buildRadio`, Blender X = x,
  +Y = +z, origins on y: `rd_mast` at (mx, y, mz) in place of the three leg rods and the brace boxes (its legs are the code's
  `leg(k, h)`; the two red lights stay the code's spheres -- it has brackets for them at 7 and 14.15 -- plus a whip and a dish);
  `rd_desk` at ((bx0 + bx1) / 2 + .6, y, bz0 + .5) in place of the desk box, the mixing desk, the six knobs and the mic (its
  monitors and mic arm are on its +Y side, which is the booth's wall at bz0: turn it pi if it ends up facing out); `rd_chair` in front of it; `rd_foam` at each of the nine
  foam tiles in place of the box (wedges toward the room).
- [x] m641 **T4g. Swap in the BASE jumpers' shack** (`models/campaign/island_base.glb`; no collision -- keep the hut box and the bench
  box). In `buildIslandBase`, `ib_shack` at (hu, g, hv) turned by psi like the hut box, in a local frame where +Y = e (along the
  exit deck) and +X = -n (toward the deck: the door, the awning and the rigs), in place of the hut box, its roof, the door, the
  awning `pearlSeg`, the two awning posts, the rail, the five rigs and the bench (it adds a drum and a crate round the back).
  Every number is the code's: hut 2.6 x 3.4 x 2.3, awning from x 1.3 at 2.4 to x 3.1 at 2.0, rigs on the rail at x 2.0,
  (k - 2) * .62 along Y, bench at x 2.75.
- [x] m644 **T4h. Swap in Dump Tower's plaza and doors** (`models/campaign/tower_plaza.glb`; no collision -- keep every box that
  collides). In `buildDumpTower`, Blender X = u, +Y = v, through `dtPut`: `dt_bollard` at each of the six gold bollards
  (k * 2.6, y0, -D2 - 8); `dt_planter` at (+-9, y0, -D2 - 4) in place of the gold box, the plant sphere and the trunk; `dt_doors`
  at (0, y0, -D2) in the lobby's 5 m gap (k = 0, side 's'), its outside -Y toward the city, adding a revolving door, glass swing
  doors, a canopy and a red mat (the gap stays walkable: the drum is not a collider); `dt_reader` beside each security
  vestibule's door on floors 8 and 9, on the side away from the stair.
- [x] m646 **T4i. Give the alien orbs a body** (`models/campaign/alien_orb.glb`; no collision -- the orbs are air targets, `O.T`). In
  `orbBody` (the amp and the watcher) and `buildOrbs` (the trance orb): add `ao_shell` to the orb's group at its centre, round the
  code's core sphere (r .7), which keeps its own colour and emissive and shows through the six gaps; or swap the core for `ao_core`
  (ONE white material -- give it the orb's colour and emissive). The ring, the halo sprite, the cones and the beams stay the
  code's. The shell spins with the group if the group spins; its fins point down and out.
- [x] m649 **T4j. Swap in the rope-bridge crossing's decks** (`models/campaign/island_xing.glb`; no collision -- keep the deck box). In
  `buildIslandXing`, Blender X = u, +Y = v, turned by ps like the deck box: `ix_deck` at each stack's (P.u, P.y, P.v) -- its top
  at the origin, 4.4 square (X.deck), +Y along the chain where the bridges land, rope rails on its two sides -- in place of the
  plank box and the four corner posts; `ix_cone` (ONE white material, tint orange / white by k % 2) at the field's fourteen cones;
  `ix_signframe` at Old Town's end (u, y, v - 1.2) in place of the two sign posts, the code's canvas planes on its board at 2.15.
- [x] m653 **T4k. Swap in the skate park's wall and planters, and the strike's placards** (`models/campaign/street_bits.glb`; no
  collision -- keep the wall and planter boxes). In `buildIslandSkate`, Blender X = u, +Y = v: `sb_graffiti` at (65, y, 31.6) in
  place of the 'conc' wall box and its three paint boxes (its painted face is -Y, toward the park, as the code's paint at 31.43);
  `sb_planter` at (64.5, 16.5) and (66, 16.2) in place of the plank box and the ico. In `buildStrike`: `sb_placard` at each sign's
  (l, f) with the code's lean, in place of the stick box -- the code's canvas plane stays, on its board's +Y face at 1.55.
- [x] m655 **T4l. Swap in Skye's lookout** (`models/campaign/old_lookout.glb`; no collision -- keep every deck, rail and post box, and the
  `farmClimb`s). In `buildLookout`, Blender X = u, +Y = v (+v out to sea): `ol_tower` at (0, g0, 0) in place of the four posts, the
  cross braces, the three decks (cut round each hatch at the code's lu, hv -hw .. -hw + 1.05), every rail, the three ladders, the
  canopy posts, the canopy and the windsock mast (its posts run to -1.0 under g0, so a post on lower ground still meets it; the
  windsock cone stays the code's). The ramp stays the code's.
- [x] m657 **T4m. Swap in the good aliens' kiosks** (`models/campaign/good_kiosk.glb`; no collision -- keep the hut and counter boxes).
  In `buildGoodKiosks`, per kiosk, Blender X = u, +Y = v (+v the street), origin at (0, g, 0): `gk_hut_paint` (ONE white
  material, tint it K.col) + `gk_hut_trim` in place of the hut box, the roof, the window, the counter and the awning (the code's
  canvas sign sits on the trim's board at 2.78); then the goods by `K.goods` -- `gk_papers` for 'papers', `gk_keys` for 'keys',
  `gk_clothes` for 'clothes' -- in place of that branch's boxes.
- [x] m659 **T4n. Swap in the town edge's gas station** (`models/campaign/gas_station.glb`; no collision -- keep every box that collides).
  In `buildTownEdge`'s gas station, Blender X = u, +Y = v (the town frame, after `UV`), origins on the ground: `gs_canopy` at
  (u, g, v) in place of the four posts, the canopy box and its red band; `gs_pumps` at (u +- 2.2, g, v) in place of each island
  and its two pumps; `gs_shop` at (su, gs, sv) in place of its plinth, walls, window, door and roof (its front, the window and the
  door, faces -Y as the code's at sv - 3); `gs_pole` at (pu, gp, pv) in place of the pole and the dark sign box -- the code's two
  'sgas' planes stay, on its board's faces at 11.6.
- [x] m661 **T4o. Swap in the town edge's houses, fences and fruit stand** (`models/campaign/town_edge.glb`; no collision -- keep the
  boxes that collide). In `buildTownEdge`, Blender X = u, +Y = v (after `UV`): `te_house_wall` (ONE white material, tint Hs.col) +
  `te_house_trim` at (u, y0, v), its front facing -Y -- turn it pi when Hs.front is -1 -- in place of the four walls, the two
  gables, the roof slabs, the windows, the door, the porch, its posts and its roof (its stone footing runs to -1.0 under y0, so it
  meets lower ground). The picket fence: `te_picket` (a 1 m section, four pickets and two rails) laid along each run every metre,
  turned by psi, in place of the pickets and the rail (keep the run's collider). `te_mailbox` at (mu, g, mv). `te_stand` at the
  fruit stand's (u, g, v) in place of the counter, the posts, the awning and the produce spheres.
- [x] m663 **T4p. Swap in the town edge's billboards and power poles** (`models/campaign/roadside2.glb`; no collision -- keep the leg
  and pole boxes). In `buildTownEdge`, Blender X = u, +Y = v: `rb_billboard` at each board's (u, g, v), its face -Y -- turn it pi
  when Bd.face is -1 -- in place of the two legs, the catwalk and the dark board (the code's 'sb0' / 'sb1' plane stays on its face
  at 9.55; it adds braces, a catwalk rail, a ladder and three lamps). `rb_pole` at each power pole's top's (u, g, v) in place of
  the pole and its crossbar (insulators at +-.7 on the crossbar at 8.45, where the code's wires start; the wires stay the code's).
- [x] m666 **T4q. Swap in the city ring's warehouse and parked cars** (`models/campaign/city_ring.glb`; no collision -- keep every box
  that collides, the walk-on roof and the stair steps above all). In `buildCityRing`, the 'warehouse' row: `cr_warehouse` at
  L(0, 0) on y0, turned psi, in the row's (lu, lv) frame (Blender X = lu, +Y = lv; the front with the roll-up door, the open
  doorway at lu -2..0 and the dock is -Y), in place of the plinth, the walls, the door and its slats, the roof and parapet, the dock,
  the twelve stair steps and the crates; `cr_forklift` at L(-12, -D2 - 4) in place of its two boxes. The 'lot' row:
  `cr_car_paint` (ONE white material, tint car1 / car2 / car3) + `cr_car_trim` at each car's (u, g, v) turned p0, nose +X, in place
  of the body, the glass box and the four tyres.
- [x] m667 **T4r. Swap in the city ring's houses** (`models/campaign/ring_house.glb`; no collision -- keep the boxes that collide). In
  `ringHouse`, Blender X = lu, +Y = lv (its front, -D2, is -Y), turned psi: `rh_house_wall` (ONE white material, tint `col`) +
  `rh_house_trim` at L(0, 0) on y0 in place of the four walls, the gables, the roof slabs, the windows, the door and the 'wood'
  stoop (it is the town edge house at the ring's own 6.8 x 5.8 x 2.7 / 4.5, with a stoop, rails and a door hood instead of a porch;
  its footing runs to -1.0). The yard fence: `rh_fence` (a 1 m section with a post at its middle: lay one per metre, turned along the run)
  along the back and both sides, in place of the two white rails each (keep each run's collider).
- [x] m670 **T4s. Swap in the fields' post-and-rail fence** (`models/campaign/farm_fence.glb`; no collision -- keep the post box and the
  run's thin collider). In `buildFieldBounds`' 'fence' branch, at each piece (u, g, v) turned psi (Blender X = along the run):
  `ff_post` (never scaled) in place of the post box, and `ff_rails` scaled X by F.piece + .25 (2.95) in place of the two rail
  boxes -- the rails sag and are weathered in two tones. Instance both (one InstancedMesh each); they run the whole farm.
  `ff_gate` (a 3 m five-bar gate on its hanging post, closed along +X from 0) is there for any gap the farm wants to close.
- [x] m672 **T4t. Swap in the channel bridge's checkpoint and lamps, and the ford's stones** (`models/campaign/bridge_bits.glb`; no
  collision -- keep the booth box and every stone's box). In `buildChannelBridge`, Blender X = u (city -> farm), +Y = v: `cb_booth`
  at (uc, yD, W / 2 - 1.1) in place of the booth box, its roof, its window and the six arm boxes (the arm is in it, pivoting at
  (-1.2, -.77) and running 3.96 to -Y, on a rest post at its end; `BRIDGE.gate` stays where the code puts it); `cb_lamp` at each
  parapet lamp's (u, yD + .95, sd * (W / 2 - .2)), its head toward the road (turn it pi on the -v side), in place of the post and
  the lamp box. In `buildFord`, `fd_stone` at each stone's (x, top, z), scaled by r / .65 and turned like the code's ico, in place of
  the ico, the cylinder and the weed (its stem runs to -2 below its top).
- [x] m673 **T4u. Swap in the creek footbridge, the reeds and the lily pads** (`models/campaign/farm_waters.glb`; no collision -- keep the
  deck and the two handrail boxes). In `buildFarmWaters`: `fw_footbridge` at (cu, top, cv) turned psi, its X across the creek (the
  code's (du, dv), the deck's length), in place of the deck, the handrails, the fourteen posts and the two trestles (they run to
  -2.5 under the deck; on deeper ground the code's own trestle can stay under them). The pond: `fw_lily` at each pad (scale by s2 /
  .7, turned by the code's angle) in place of the circle; `fw_reeds` at each reed spot (the code's four cones round it) in place of
  the cones.
- [x] m674 **T4v. Swap in the lot's chain-link fence and the channel bridge's piers** (`models/campaign/chainlink.glb`; no collision --
  keep the run colliders and the pier boxes). In `buildCityRing`'s 'lot': `cl_post` (never scaled) at each of the code's posts, and
  `cl_mesh` (1 m along X: scale X by the span between two posts, ~2.5) between each pair, turned along the run, in place of the posts,
  the top rail and the thin wall. In `buildChannelBridge`: `cb_pier` at each pier's (u, yD - .6, 0) in place of the pier box and its
  two cutwater cylinders -- built for W 6 (5.6 across, the noses at +-Y = across the bridge, upstream and down), from its cap at 0
  down to -12; it sinks into the bed below that.
- [x] m676 **T4w. Swap in the Mothership gauntlet's organics** (`models/campaign/ship_gauntlet.glb`; no collision -- the sac is drawn
  only, the room is its trigger). In `buildShipGauntlet`, the ship frame (Blender X = u, +Y = v): `sg_sac` at (hall[0] + 2.5, yC,
  hall[1] + G.hallR - 1.6) in place of the glow sphere -- its origin is the floor under the code's sphere (r 1.1 at 1.4), its
  feeding tubes up into the north wall (+Y); `sg_rib` at each of the lock room's six glow boxes, turned -a like them (its X points
  out of the wall), in place of the box; `sg_strand` at each tear strand's root (the edge of the tear, yC - .1), turned toward the
  hole (s * .6), in place of the cone.
- [x] m678 **T4x. Swap in the rally trucks** (`models/campaign/rally_truck.glb`; no collision -- each truck's `BDYN` box stays). In
  `buildRally`, inside each truck's group `g` at its origin, with no turn: `rt_paint` (ONE white material -- give it mats[k]'s
  colour) + `rt_trim`, in place of the three boxes and the four wheel cylinders. It is built in the group's own frame (the nose at
  the group's +z, where the code's cab sits forward of the bed), 2.0 x 5.0 like the box, wheels where the code's are, a light bar
  and two flags.
- [x] m681 **T4y. Swap in the orchard terrace's dry-stone walls and steps** (`models/campaign/orchard_terrace.glb`; no collision -- keep
  every wall and step box). In `buildOrchardTerrace`: `ot_wall` at each wall segment's (u, y0, v) turned like its box (X along the
  outline), scaled Z by y1 - y0 (built 2.1 x .7 x 1.0 from 0, the coping on top), in place of the stone box and the moss box (it has
  its own moss); `ot_step` at each step's (u, base, v) turned like its box (X along the stair's run), scaled Z by its height (built
  .55 x 2.0 x 1.0 from 0, a worn tread on top), in place of the stone box. Instance both: there are a lot of them.
- [x] m683 **T4z. Swap in the dry dock's blocks, the quay's fenders and the ship's stair tower** (`models/campaign/dry_dock.glb`; no
  collision -- keep every box that collides). In `buildWaterfront`, Blender X = u, +Y = v: `wd_keelblock` at each keel and bilge
  block's (u, floor, v), scaled Z by hb - floor, in place of the 'block' box; `wd_fender` at each fender's (u, Y, v + .18) on the
  river's edge (its face -Y toward the water; turn it for the piers' sides and ends like their boxes) in place of the 'rubber' box;
  `wd_stairs` at (lu, Y, 50) in place of the landing, its four posts, the twenty steps and the two rails (built for deck - Y = 6.25,
  the code's 20 risers of .3125; scale Z by (deck - Y) / 6.25 if that ever moves).
- [x] m686 **T5a. Swap in the scaffold up the coaster's side** (`models/campaign/ship_scaffold.glb`; no collision -- keep the working
  deck's box and the rail's collider; the ladder stays the code's `pearlLadder`). In `buildWaterfront`, Blender X = u, +Y = v:
  `ss_scaffold` at (su, floor, 45) in place of the 22 standards, the two lifts' boards, the top deck and the guard rail -- every
  standard where the code's are (v 30..60 every 3, u su +- 1.4, to top + 1.1), the lifts at 3.8 and 7.6, the deck at top
  (floor + 10.95), toe boards, X-braces on the outer face. Built for D.rise 2.2 and S.depth 9.
- [x] m690 **T5b. Swap in the counter-protest camp** (`models/campaign/rally_camp.glb`; no collision -- keep the cooler's and the chair's
  boxes). In `buildRally`'s camp, Blender X = u, +Y = v in its frame (turned th like its boxes): `rc_camp` at (0, g0, 0) in place of
  the four posts, the tarp, the cooler and the chair -- all at the code's places, plus guy ropes and pegs, a string of bunting in
  the Pearl's pastels along the front and two placards on sticks (blank card for a canvas if the code wants to write on them).
- [x] m691 **T5c. Swap in the trailer park's boardwalk** (`models/campaign/trailer_walk.glb`; no collision -- keep the walk, platform,
  rail and post boxes). In `buildTrailerPark`, Blender X across, +Y along, turned psi like the boxes: `tw_walk` at each segment's
  (um, Y, vm), scaled Y by (len + .3) / 4.3, in place of the plank box (bearers under it); `tw_rail` at each rail's (ru, Y, rv),
  scaled Y by len / 4, in place of its two boxes and its post (posts every metre, a mid rail); `tw_platform` at each trailer's
  platform (u, yp, v), scaled Y by R.len + 1.6, in place of its plank box; `tw_pile` at each of `posts`' piles (pu, top - .2, pv),
  scaled Z by (top - .2) - (g - .4), in place of the post box and its brace.
- [x] m693 **T5d. Swap in the mill's saw line, log piles and sawdust** (`models/campaign/mill_floor.glb`; no collision -- keep the saw
  bed's box and each pile's collider, whose top is a floor). In `buildMill`, Blender X = u, +Y = v: `ml_sawline` at (0, y, S.v + 3.5)
  in place of the rollers, the bed and the blade (its blade where the code's is, under a yellow hood on four posts, a motor and a
  control box); `ml_pile4` / `ml_pile3` at each pile's (P.u, y, P.v) by P.n, in place of every log cylinder and cut-end circle (logs
  6 m along X, .72 apart, .62 up a layer, cut ends with rings, two bearers under); `ml_dust` at each heap's (u, y, v) scaled by r, in
  place of the cone.
- [x] m697 **T5e. Swap in the trailer park's porches and awnings** (`models/campaign/trailer_porch.glb`; no collision -- keep the porch
  box). In `buildTrailerPark`, Blender X = u, +Y = v, per trailer: `tpc_awning` at (u - R.side * .9, yp, v - R.len * .1), its +X
  away from the trailer toward the walk (so mirror X when R.side is +1, which puts the walk at -u), in place of the tin box and the
  two steel posts (it adds rust patches, a rail and a string of bulbs); `tpc_porch` at (pu, py, v - R.len * .1), its step on the +X
  side (mirror like the awning), in place of the plank box (posts to -1.2 under it).
- [x] m699 **T5f. Swap in the MX track's start gate and hay bales** (`models/campaign/mx_extras.glb`; no collision -- keep the hay boxes).
  In `buildBikeTrack`: `mx_gate` at at(-2.3, 0) on g0 + h, turned so its X runs across the lanes (the code's at(-2.3, w) line) and
  its plates face down the track, in place of the seven steel posts and the yellow bar (six drop-plates with number boards between
  them, and the release lever off its end); `mx_hay` at each hay bale's (u, g, v) turned like its box, in place of the 'hay' box.
- [x] m703 **T5g. Swap in the fair field's poles, bunting, hay, trucks and flag** (`models/campaign/fair_field.glb` plus pieces already in
  the repo; no collision -- keep the hay and truck boxes). In `buildFairground`, Blender X = u, +Y = v: `fg_pole` at each of the six
  bunting poles (u, y, v) in place of the wood box; `fg_pennant` (ONE white material, tint bunt1/2/3) at each of the code's pennant
  points (its top edge on the line), turned like the code's triangle, in place of the triangle geometry; `mx_hay` (mx_extras),
  scaled (1.07, 1.11, 1.06), at each of the five hay bales; `rt_paint` + `rt_trim` (rally_truck, paint tinted 'truck') at each of
  the four trucks outside the gate, nose toward -v, in place of the three boxes; `rp_pole` + `rp_flag` (rim_props) scaled Z by 2 at
  the stage's flag, in place of the 12 m steel box and the plane.
- [x] m706 **T5h. Swap in the halts' bench, churns and lamp posts** (`models/campaign/halt_extras.glb`; no collision -- keep the bench's
  box). In `buildFreight`'s m494 block, per platform, Blender X = u, +Y = v, built for side = +1 (mirror X for side -1):
  `hx_bench` at (pu + side * 1.25, deck, vm) in place of the seat, the back, the two iron ends, the timetable board and its four
  lines (the board is in it at +2.0 along v); `hx_churns` at (pu + side * 1.1, deck, cv) for each end (k = +-1; mirror Y for
  k = -1) in place of the four churn cylinders and the two sacks; `hx_lamp` at each lamp post's (lu, deck, vv) in place of the post,
  the lamp sphere, its cone, the bracket, the basket and its flowers (its bracket runs toward -X, the platform's inside).
- [x] m709 **T5i. Swap in the freight trestle's deck and bents** (`models/campaign/trestle_deck.glb`; no collision -- keep each bent's
  post boxes and whatever the deck walks on). In `buildFreight`, the line's frame (Blender X = u across, +Y = v along): `td_deck` at
  (0, yr, v + 3) for each 6 m, in place of the beam box, the 7-8 ties in it and the two rails' share of it (the rails at the code's
  gauge 1.5, tie plates, outer guard timbers); `td_bent` at each bent's (0, yr - .55, v), scaled Z by (yr - .55) - (g - .5), in place
  of the two post boxes and the two brace segments (posts at +-1.1, a cap, a sill, X-braces both faces). Instance both.
- [x] m713 **T5j. Swap in the MX tape, the road litter and the patched potholes** (`models/campaign/trackside.glb`; no collision -- the
  litter boxes the code makes solid stay). In `buildBikeTrack`'s m498 block: `ts_stake` at each tape stake (A) in place of the plank
  box, and `ts_tape` (ONE white material, tint red / white) from A to B -- at their midpoint, turned along A -> B, scaled X by |AB| --
  in place of the tape `pearlSeg`. In `buildHighway`'s m511 block: `ts_patch` at each pothole in place of the circle (scale by its r /
  .55, turned by its angle); `ts_litter` at a few of the gutter litter spots in place of their boxes (one clump stands for three or
  four of the code's).
- [x] m715 **T5k -- `pearlLadder`'s rails and rungs as art (`models/campaign/pearl_ladder.glb`).** Three roots, X = the code's lateral (cos psi, -sin psi), +Y = out along psi, yawed by psi like the code's `bx`: **`pl_rail`** both rails at +-.25, a 1 m section STRETCHED in height from `y0` to `top + 1.0`; **`pl_rung`** one rung, one instance per code rung at `y0 + .3 + r * .32` (never stretched); **`pl_cap`** the rails bent over to two wall plates, origin at `top + 1.0`. Every caller of `pearlLadder` (21) gets it; the climb volume and colliders stay code. Then drop the code's rail and rung `bx`.
- [x] m716 **T5l -- `pearlSpan`'s links as art (`models/campaign/pearl_span.glb`).** One segment per piece: +Y along the span, X across, origin at the segment centre on the walk line, 1 m long -- STRETCH along Y by `L / n` and pitch to P->Q (the rope's sag comes free). Decks 1 m wide (stretch X by `2 * hw`); rails are ONE side at x 0, placed at +-hw. **Steel:** `ps_deck`, `ps_rail` (top 1.0, mid .5), `ps_post` (1.02, every 2nd k), `ps_endpost` (1.3). **Rope:** `ps_planks` (the code's .1..9 plank, Y-scale .8 of the segment), `ps_rope` (hand 1.0, foot .1), `ps_rpost` (every 3rd k), `ps_rendpost`. Landings use `ps_deck`/`ps_planks` too. The walk TRIs and the side colliders stay code; then drop the `pearlSeg`/`bx` visuals (11 callers).
- [x] m719 **T5m -- the dry dock's CAISSON as art (`models/campaign/caisson.glb`, buildWaterfront).** Blender X = u, +Y = v. **`cg_deck`** at (D.u, D.v0 / 2) on Y: plate seams, yellow edges, two hatches, two valve wheels, a bollard each end, .03 proud (the steel box stays the collider). **`cg_rail`** one side's 30 m handrail with its posts every 3 m from -dIn + .5, at v = D.v0 / 2 +- 1.85: replaces the `yel` bar and posts. **`cg_pile`** 1 m, STRETCH from sea - 1 to Y - .4 at each `iron` fender. **`cg_face`** the river face's plating and stiffeners, 30 x 1 m, STRETCH from B0 to Y on v = 0.
- [x] m723 **T5n -- the stair down into the dry dock as art (`models/campaign/dock_stair.glb`, buildWaterfront, `the stair down into the dock at its head`).** Blender X = u, +Y = v. **`dk_stair`** at (su, v0 = 70) on `floor`: the 16 concrete risers (.309, for Y - floor = 4.95; scale Z by (Y - floor) / 4.95 if that ever moves), yellow nosings, drain grates, a sloped handrail on the dock side at x +1.15 -- the `quay` blocks and the `yel` wall stay colliders, drop their drawing. **`dk_landing`** at (D.u - dIn - .3 + lw / 2, top + 1.2) on Y: grated steel 6.8 x 2.4 with its rail on +Y -- replaces the `steel` slab and the `yel` rail.
- [x] m728 **T5o -- the freight halts' platform stairs and the halt yard's fence as art (`models/campaign/halt_stairs.glb`, buildFreight).** Blender X = u, +Y = v. **`hs_step`** one per step at (pu, v - dn * .225) on its tread top y: plank tread 2.8 x .45, yellow nosing on +Y (= dn; turn by pi for dn -1), riser and cheeks -- the `plank` block stays the collider, its drawing goes. **`hs_leg`** one per step, 1 m, STRETCH from min(g, y) - .5 to y - .3. **`hs_fence`** one per side per even k at (u +- 1.6, v) on fg: the post and both rails (v - .9 .. v + 2.7) -- replaces the `post` and the two `plank` rails.
- [x] m729 **T5p -- the outfeed tower's stair and platform as art (`models/campaign/outfeed_tower.glb`, wfFactory `THE OUTFEED TOWER`).** Blender X = u, +Y = v, L3 - Y = 10. **`ot_stair`** at (-45, 108) on Y: 32 open grated treads at the code's j positions (x (31 - j) * .4 + .2, top (j + 1) * .3125), stringers, three bents, the yellow rails at y +-1.05 -- the 32 `grate` blocks stay colliders (drop their drawing), and the two `yel` pearlSegs go. **`ot_platform`** at (-48, 109.5) on Y: the 6 x 7 grated deck at 9.6..10, four legs at (+-2.8, +-3.3), X-bracing -- replaces the `grate` slab's drawing and the four `steel` legs. The `rail()` runs stay.
- [x] m732 **T5q -- the factory gate's hut and barrier as art (`models/campaign/gatehouse.glb`, wfFactory).** Blender X = u, +Y = v. **`gh_hut`** at (gm + 6, lv0 - 4) on Y: the 2.4 hut with its roof, window on -Y, door on +X, a lit lamp, a camera and a company band. The `white` box stays the collider; its drawing, the `dark` roof and the `glass` go. **`gh_barrier`** at (gm, lv0 - 4) on Y: the striped boom at 1.0..1.12 from x -3.5 to +3.5, its post at x +3.7 (the `dark` collider stays), a counterweight and a rest fork. It replaces the `red` arm and the four `white` stripes.
- [x] m736 **T5r -- the factory lot's security fence as art (`models/campaign/security_fence.glb`, wfFactory `run`).** +Y along the run (the code's `ps`), X across. **`sf_post`** at each of the code's posts on Y: a 3.5 m post with its outrigger on -X (the OUTSIDE -- turn by pi where the outside is +X). **`sf_mesh`** is one metre: the weave .1..2.5, the top rail at 2.6, and the three barbed strands. TILE it ceil(l) times per segment, scaled l / ceil(l) along Y; never stretch one copy. It replaces the `mesh`, top-rail `steel`, `dark` strands and post boxes; the `iron` slab stays the collider. INSTANCE both (~270 m of run, 166 faces a metre).
- [x] m739 **T5s -- the factory's roof units and stacks as art (`models/campaign/factory_roof.glb`, wfFactory).** Blender X = u, +Y = v, origins ON THE ROOF (Y + Fc.h). **`fr_unit`** goes at each of the four units' centres: the 6 x 4 x 2.4 air handler with louvres, two fan wells and a duct elbow on -Y. The `steel` box stays the collider; drop its drawing. **`fr_stack`** goes at (Fc.u +- 13, Fc.v + 16): the 22 m stack (r 1.6 to 1.4), the red band at 20..21, the bands, a railed ring platform at 14, a caged ladder on +X and soot at the lip. It replaces the two CylinderGeometry `panel`/`red` draws; the `panel` box stays the collider.
- [x] m742 **T5t -- the factory front's intake door as art (`models/campaign/factory_portal.glb`, wfFactory).** Blender X = u, +Y = v; it faces -Y. **`ff_portal`** goes on the ground at (Fc.u, v0): steel jambs at +-5.25 with 45-degree hazard chevrons, the lintel band at 8..8.5, the shutter hood (the shutter is up), the guides, dock bumpers, two bollards and a beacon. It replaces the 9 + 12 alternating `yel`/`dark` blocks at v0 - .09 (all drawing-only), so no collider changes.
- [x] m747 **T5u -- the transit shed's dunnage as art (`models/campaign/shed_yard.glb`, buildWaterfront, Sh).** Blender X = u, +Y = v. **`ws_pallet`** is one flat 1.2 x 1.0 x .15 pallet. Stack k % 3 + 1 of them at each of the six `wood` spots (Sh.u - 20 + k * 7, v0 - 3.5 - (k % 2)), each .15 up, with a few degrees' turn so the stack is not a block. **`ws_drum_paint` + `ws_drum_trim`** are one drum (r .3, .9) at each of the five drum spots; tint the paint with the code's c1 / c5. They replace the `wood` boxes and the five CylinderGeometry drums, all drawing-only.
- [x] m748 **T5v -- the factory's gallery over the fence as art (`models/campaign/factory_gallery.glb`, wfFactory `THE GALLERY`).** Blender X = u, +Y = v. **`gl_bay`** is one metre, origin at v 109.5 on the floor at L3: grated floor, corrugated walls at +-2.05 with a lit window ribbon, roof and portal frame. TILE it from the wall to -51, scaled len / n along X; never stretch one copy. It replaces the drawing of the `grate`, both `tin` walls and the `roof` (the colliders stay). **`gl_leg`** is 1 m, STRETCHED from Y to L3 - .4, at the code's four legs (u -60 / -54, v gv0 + .3 / gv1 - .3).
- [x] m752 **T5w -- the factory's parapet and screen bands as art (`models/campaign/factory_skin.glb`, buildWaterfront FACTORY block).** +Y = OUT from the wall, X along it; both are 1 m tiles, TILED along each run (scale len / n), never stretched. **`fp_parapet`** goes on the roof (Y + Fc.h) on each of the four `panel` runs' centre lines: the .3 wall, metal coping and an outside scupper. The `panel` boxes stay the colliders; drop their drawing. **`fp_screen`** goes at each `screen` band's foot (Y + 10) on its wall face, facing out: a framed green LED band with scanlines and running "text". It replaces the three drawing-only `screen` boxes (front Fc.w - 4, west Fc.d - 6, east 39).
- [x] m753 **T5x -- the transit shed's roof vents as art (`models/campaign/shed_vents.glb`, buildWaterfront THE TRANSIT SHED).** Blender X = u, +Y = v. **`sv_vent`** goes on the roof (Y + Sh.h) at each of the three `steel` boxes ((-14, 3), (6, -4), (18, 5) off Sh): a curb, a louvred housing, a hipped cap to 1.4 and a turbine ventilator above it (spin it about its Z if you like). The `steel` box stays the collider; drop its drawing. It applies whether or not his `wf_shed` is placed, since the vents are drawn outside that branch.
- [x] m757 **T5y -- wfFactory's scanner arches, strip-down cage, hard hats and boots as art (`models/campaign/factory_stations.glb`).** Blender X = u, +Y = v (ps 0). For `arch()`: **`fa_post`** is 1 m, STRETCHED to h, at (u +- 1.7, v) on y. **`fa_head`** goes at (u, v, y + h): the beam, the screen strip, two red emitter pods and hazard ends. Together they replace the arch's four `bx`. **`fa_cage`** goes on the floor at (-87, 86): posts, the mesh sides, the roof, a bench and hooks; the `steel` posts stay colliders. **`fa_hat_paint` + `fa_hat_trim`** go at each of the 7 hard-hat spots (on Y + Math.floor(k / 3) * .5), with the paint tinted yel / white. **`fa_boots`** is a pair at each of the six `wood` boxes. Everything replaced except the cage posts is drawing-only.
- [x] m758 **T5z -- wfFactory's control room consoles and the red lever as art (`models/campaign/control_room.glb`).** Blender X = u, +Y = v, on L2. **`fc_console`** goes at each of the three consoles, turned by the code's ry: the desk, a raked top with the line's mimic panel lit, three monitors at +Y and a key ledge at -Y. The `dark` box stays the collider; drop its drawing and the `screen` slab. **`fc_lever`** goes at (-104.6, 112.5): the pedestal with a hazard collar and the lever thrown to -Y, with its red knob where the code's sphere is. The `dark` collider stays; the cylinder and sphere go. `L.leverAt` is unchanged.
- [x] m762 **T6a -- wfFactory's crates of arms along the east wall as art (`models/campaign/parts_stock.glb`).** Blender X = u, +Y = v, origins on the floor at each of the 8 crates (-66.5 - (k % 2) * 1.3, 80 + floor(k / 2) * 3.2). Pick the piece by k % 3: **`fs_case`** for 0 (the `c7` 1.1: a ribbed steel parts case with an arm's wrist on the lid), **`fs_crate15`** for 1 (1.5: a crate with a small crate on it) and **`fs_crate19`** for 2 (1.9: two crates with Uplift bands). The boxes stay the colliders; drop their drawing.
- [x] m763 **T6b -- wfFactory's arm pedestals, chrome booth and lift shaft as art (`models/campaign/factory_line.glb`).** Blender X = u, +Y = v. At each `L.ARMS` spot: **`fl_column`** is 1 m, STRETCHED from Y to L2 - .1 (it replaces the `steel` column), and **`fl_pedestal`** goes at L2 - .1 (the yellow base, bolts and turntable; the `yel` collider stays). **`fl_booth`** goes at (-101, 92) on L2: chrome posts and sides, the roof with its glow panel, and the strip curtains at both ends. It replaces all of the booth's drawing-only boxes. **`fl_shaft`** is one metre, origin at (-101, 76): TILE it from Y to L3 + 3 (z += 1) in place of the four `steel` posts. Its -Y face is left open for the platform.
- [x] m766 **T6c -- wfFactory's walkway rails, legs and the west-wall stair as art (`models/campaign/factory_walks.glb`).** +Y along a run, X across. For each `rail()`: **`fw_rail`** is a 2 m tile (a post at its -Y end, the top and knee bars, a toe board), TILED ceil(l / 2) times scaled l / n along Y, plus **`fw_post`** at the run's far end. The `yel` collider stays; drop the drawn bars and posts. **`fw_leg`** is 1 m, STRETCHED from Y to y - .3, at the code's 12 legs. **`fw_step`** goes at each of the 33 stair blocks' top centre (u -108.6): an open grated tread with a yellow nosing on +Y (the downhill side) and cheeks. The `grate` blocks stay colliders and their drawing goes, so the stair reads open.
- [x] m771 **T6d -- Camp Hollis's HESCO ring as art (`models/campaign/hollis_wall.glb`, buildMilBase `run`, first half of the base).** +Y along a run (psi), X across, origins on the ground. **`mb_hesco`** is one basket 1.1 x 1.2 x 1.21. TILE each tier at the code's 1.1 cage pitch, z = i * 1.25, and scale X by 1.0 / 1.2 for upper tiers. It replaces the drawn `hesco` tiers and the `mesh` cage posts. **`mb_sandbag`** goes at each top `sand` box, yawed as the code does. **`mb_wire`** is one .9 m concertina coil at top + .4, tiled in place of the torus run. **`mb_bastion`** goes at each gate bastion (three courses to 4.2, a sandbag crown). The `hesco` colliders all stay. Still to do on the base: the watchtower, tents, motor pool, mast and supply cage.
- [x] m773 **T6e -- Camp Hollis's watchtower and tents as art (`models/campaign/hollis_camp.glb`, buildMilBase).** Blender X = u, +Y = v, on the base's y. **`mt_tower`** goes at (-10, -10): timber legs and bracing, the deck at 6, a sandbag parapet open at +Y (the ladder), the tin roof and the searchlight. It replaces the drawn boxes, the cylinder and the circle; the leg, deck and parapet colliders stay. **`mt_tent_cmd`** goes at (10.5, -7): walls, the pitched roof and ridge, guy ropes, and the door, fly, poles and map table at +Y, toward the gate. It replaces the tent's drawn boxes plus the fly and table. **`mt_tent_bar`** goes at (13.5, 4), turned by .25. The `canvas` wall colliders stay. Still to do: the trucks, the camo net, the comms mast, the supply cage and the firing positions.
- [x] m774 **T6f -- Camp Hollis's trucks, camo net, comms mast and supply cage as art (`models/campaign/hollis_yard.glb`, buildMilBase).** Blender X = u, +Y = v, on y. **`mt_truck`** goes at each `truck(u, v, psi)`, built with its cab toward +Y (turn by psi). It replaces the drawn bed, canvas, cab, windscreen and the six tyre cylinders; the `olive` colliders stay, and the plate stays code. **`mt_net`** goes at (-8.25, 6) on y + 3.58, sagging between its poles, with **`mt_pole`** at each of the four. **`mt_mast`** goes at (-2, -14): a 15 m lattice, the guys, two panel antennas and the generator. The code's blinking beacon sphere stays. **`mt_cage`** goes at (4, -13.5): chain-link with the door gap at +Y, the crate stacks, and the prize box (olive with a yellow lid). The `wire`, `crate` and `olive` colliders stay. Still to do: the firing positions, the drums, the picnic table, the porta-john, the flag and the hoop.
- [x] m775 **T6g -- the last of Camp Hollis as art (`models/campaign/hollis_props.glb`, buildMilBase).** Blender X = u, +Y = v, on y. **`mp_bags`** goes at each firing-position segment, turned a + pi / 2 (three bag courses to 1.08; the `sand` collider stays). **`mp_drum`** goes at each of the five drum cylinders. **`mp_table`** goes at (4, 6.5), yaw .2, and **`mp_john`** at (15, -2.5). **`mp_flag`** goes at (3.2, 14): a 9 m pole with the flag to +X. **`mp_stack`** goes at (-1, 12): four courses and a shovel. **`mp_hoop`** goes at (-4, -6): post, backboard to +Y, rim and net. Each replaces its drawn boxes; the colliders the code keeps (bags, drum block, table, john, stack) stay.
- [x] m779 **T6h -- Saucer Joe's diner as art (`models/campaign/diner.glb`, buildDiner: THE DINER, its inside, steps, awning, roof units).** Blender X = u, +Y = v (+v to the highway). Both pieces go at the code's frame origin (0, 0) on y; every number is the code's. **`dn_shell`** is the body between the round ends (r 3.5 at u +-5.5): the red and chrome bands, the window ribbons (front and the end arcs), the door gap, the red roof with round ends, the steps and awning, the AC unit and vent. It replaces every drawn wall, band, cylinder shell, glass, roof, step, awning and roof-unit box/geo; the `cream` and `red` colliders stay. **`dn_inside`** is the checker floor, the teal counter and back bar, the seven stools, the two booths and the menu board frame. The neon frame, the canvas signs and the sign tower stay code.
- [x] m780 **T6i -- Saucer Joe's sign tower and UFO museum as art (`models/campaign/diner_site.glb`, buildDiner).** Blender X = u, +Y = v, on y. **`ds_tower`** goes at (-12, 7): three tapering legs, the ring braces, the saucer with its glass dome and twelve bulbs at 16, and the EAT arrow with its bulbs (the canvas EAT stays). It replaces the pearlSegs, the braces, the cylinder, dome and sphere geos, and the arrow box and cone; the `steel` collider stays. **`ds_museum`** goes at (12.5, -6): the quonset's corrugated shell and ribs, the closed back arch and the front arch with its door (+Y, to the lot), and inside the four cases, the grey in his tube and the six clippings. It replaces every museum geo and drawn box; the slab colliders and the canvas sign stay.
- [x] m786 **T6j -- Saucer Joe's replica saucer and its yard as art (`models/campaign/diner_saucer.glb`, buildDiner THE YARD AND THE SAUCER).** **`ds_saucer`** is built in the saucer GROUP's own frame. Add it under `O.saucer` unturned, so it rides with the group: the two hulls, seams, the 16 rim bulbs, the missing panel and the three splayed legs. It replaces those meshes; **the dome and the green dome light stay code** (`O.dome` / `O.domeLight` are animated), and so does the `BDYN` box. **`ds_yard`** goes at (-2, -10) on y: the plinth and the chain-link ring (nine faces, the gap at +Y, a post at every corner). The `conc` and fence colliders stay.
- [x] m787 **T6k -- Merle's bunker container and what's in it as art (`models/campaign/bunker.glb`, buildBunker: THE CONTAINER and inside).** Blender X = u, +Y = v (+v away from the hill). Both pieces go at the frame origin (0, 0) on y, at the code's numbers. **`bk_box`** is the corrugated container (v -5..1) with its ribs, door gap and two rusted leaves swung open, roof, corner castings, the pallet step, the twelve sandbags and the periscope. It replaces every drawn box and geo of the container; the `box` colliders stay, and the dirt mounds stay code. **`bk_inside`** is the cork wall (16 clippings and the red string), the cot, the radio desk with four lit dials facing -X, the four shelves of cans and the bulb on its flex. `O.dialAt` is unchanged. Next pass: the lookout and the rest of the camp.
- [x] m788 **T6l -- the rest of Merle's camp as art (`models/campaign/bunker_camp.glb`, buildBunker).** Blender X = u, +Y = v, each piece on y at its spot. **`bk_lookout`** goes at (-6, -1.5): poles, bracing, the deck at 4, the plank rail open at +Y for the ladder, and the telescope. **`bk_mast`** goes at (2.8, -6.2): the foil pole, cones, dish and guys. **`bk_solar`** goes at (6.15, -1.5): three panels tilted to +Y. **`bk_barrels`** goes at (2.25, -5.7): two rain barrels and the downpipe. **`bk_garden`** goes at (-5, 5): the chicken-wire run and three beds. **`bk_firepit`** goes at (4, 4.5): the stone ring and four stumps. Each replaces its drawn boxes and geos; the colliders stay. The tin-can line and the path sign stay code.
- [x] m790 **T6m -- the Underneath's tunnels and rooms as TILES (`models/campaign/underneath.glb`, buildUnderneath `run()` / `room()`).** The plan is procedural, so the art is tiles at the code's sections: +Y along a run (turn by pi/2 for dir 'u'), X across, origin on the floor at y. **`un_tunnel`** is one metre of a run (T 3.0, H 3.2): stone floor and drain, brick walls with mortar and joints, the vault and the pipe. TILE it per run, n = round(L), each scaled L / n. Use **`un_tunnel_open`** (floor, vault and pipe only) where a wall has a gap. **`un_wall`** is one metre of room wall, scaled Z by h / 4. **`un_lamp`** goes at each `lamp` + `iron` pair. **`un_prop`** goes at each pit-prop set in the old dig. **`un_growth`** is a teal growth cluster: SCATTER it with a seeded random on wall feet, never one per tile. All the code's boxes stay colliders; drop their drawing. The cistern, the market and the dig's cart, rails and strongbox are the next pass.
- [x] m799 **T6n -- the Underneath's cistern catwalks, the dig's cart, rails and strongbox, the vault's crates as art (`models/campaign/under_cistern.glb`).** Blender X = u, +Y = v. **`uc_catwalk`** goes at (cu, cv +- 2.6) on y: the 19.4 plank deck on stringers, both rails, and the iron legs down to y - 2.4 every 3 m, braced. It replaces the drawn plank, rails and legs; the colliders stay. **`uc_rail`** is a 1 m track tile (gauge 1.0), tiled along the dig in place of the two `iron` strips. **`uc_cart`** goes at (dc - 1.5, vS2 + .9) on y: the tub, wheels, couplings and ore. **`uc_strongbox`** goes at (dc + 2.6, vS2 - 2.2). **`uc_crate`** goes at each of the vault's five `plank` stacks, scaled Z by the code's h. Colliders stay; `U.dig.box` is unchanged.
- [x] m800 **T6o -- the Underneath's pump room, hidden market and camp props as art (`models/campaign/under_market.glb`).** Blender X = u, +Y = v, on y. **`up_pumps`** goes at (pu, cv): the two pump drums, the mains to the door, the control cabinet, the red WHEEL at the code's `wheelAt` (spin it about X while the pumps run) and the floor grate at the pad. It replaces the cylinders, pearlSegs, the cabinet box and the circle; the colliders stay. **`um_stall_frame` + `um_stall_tarp`** go at each of the six stalls, built for the south row (turn by pi for the north); tint the tarp with the code's `tarp` / `tarp2`. **`um_counter`** goes at (cu + 6.2, cv). **`uc_camp`** (the fire barrel), **`uc_bedroll`** (at the four bedroll spots with their yaw) and **`uc_trolley`** (at (tu, tv), yaw .3) go in the camp. The bulb strings stay code.
- [x] m801 **T6p -- the Underneath's crossways ladders and the good aliens' safe house as art (`models/campaign/under_safe.glb`).** Blender X = u, +Y = v, on y. **`us_ladder`** goes at each shaft's ladder foot (cu, cv + b * 17.6), brackets to +Y (turn by pi for b = -1). It includes the growth puddle, and replaces the `iron` stiles and rungs and the `grow` circle. **`us_cot`** goes at the four cots (the `plank` colliders stay). **`us_table`** goes at (su + 1.5, sv + 2), laid with bowls, cups, a teapot and a candle; it replaces the five rust cylinders. **`us_garden`** goes at the first pot (su - 4.2, sv + 3.9): five pots of glowing plants and the grow lamp on its chains. The six warm wall lamps stay code. That finishes buildUnderneath.
- [ ] **T6q -- the metro core's tower kit as art (`models/campaign/metro_core.glb`, buildMetroCore).** The towers are procedural, so this is the kit each tower uses. Blender X = u, +Y = v. **`mc_lobby`** goes on the ground (g.hi) at (u, v - d / 2), its face at Y 0, the street at -Y: glazed doors, the canopy with its lit soffit and hangers. It replaces the `door` and awning boxes. **`mc_tank`** goes on the roof at (tu, tv): legs and bracing, the hooped tank, the cone roof and a ladder. It replaces the four leg boxes and the cylinder and cone; the `tank` collider stays. **`mc_unit`** goes at a set-back tower's roof unit (the `steel` collider stays). **`mc_bridge`** is one metre of sky-bridge (the deck, glass balustrades, gold handrails), TILED L + .6 along each bridge in place of the `deck` and `rail` drawing. The colliders stay. The window bands stay code: they are per-tower materials the grip dims (m700).
- [ ] **T6r -- the islands' BASE-jump exit point as art (`models/campaign/island_exit.glb`, buildIslandBase THE EXIT POINT).** +Y = the exit direction e (turn by psi), X = n. **`ib_deck`** goes at the deck's centre (cu, cv) on its top y: planks and joists, both rails open at the back and the end, the hazard stripes on the last .6, the braces and back struts into the rock below the edge (dE is local Y -.5), and the sign frame (the canvas sign stays code). It replaces the deck's drawn planks, joists, rail bars and posts, stripes, braces and sign posts; the `deck` and rail colliders stay. **`ib_step`** goes at each ground-fitted step of the way on (the `plank` colliders stay). The windsock stays code, because the wind turns it.
- [ ] **T2. The campaign detail pass** -- a standing item after T1, one place per build: (a) the bridge roadblock must actually
  block -- barricade + cars tall/solid enough that a jump does not clear it, or make clearing it the intended trick with a reaction;
  (b) the truck's model; (c) the farm's bushes; (d) the crash site; then onward place by place. Rules from the level window's
  STYLE_GUIDES.md (`models/alien_plaza/`) apply: no box meets the ground in a straight line (a foot / dirt / rubble), curves are
  smooth-shaded, every building has a plinth / floor bands / cornice, three of each prop kind, imperfections where the eye lands.
  **Tell Colin in the NOTES entry whether you want this handed to a separate scenery window** (the level window can take it: it
  builds in headless Blender and pushes GLBs, so a scenery window owning the campaign's art files while the loop owns the code
  would not collide).

**GLOWTIDE MECHANICS BLOCK -- RUN ONLY WHEN COLIN SAYS "do the Glowtide block", then go back to Phase F.** (Written by the level
window, Oct 20.) The level file already carries every one of these as markers with their numbers; nothing in the game reads them
yet, which is why none of them do anything. One build each, in this order. Read `models/alien_plaza/README_ALIEN_PLAZA.md` and
`MECHANISMS.md` (same folder) for the design. The level window keeps owning the GEOMETRY in `models/alien_plaza/`; these items
are code only. Where a system already exists (portals, grind, hover, the marker loader), reuse it -- do not fork it.
- [ ] **G1. Portals.** `portal_0..5` (kind `portal`, `lit`, `where`) through the existing PORTAL/marker system (MARKERS.md says
  `portal_*` is live). `portal_0` lit at start; the others light when he walks between their posts; jump between lit ones.
  *He sees:* the posts glow on arrival and the GOD/portal list offers them.
- [ ] **G2. Grind rails.** `rails` in `alien_plaza_level.json` (`a`, `b`; ride a -> b downhill). Catch with the air tap like the
  board's rail catch, ON FOOT as well as on the board; slide along the segment at a speed from the drop; hop off at b or with a
  tap. Reuse the board's grind code. *He sees:* the bell-room rail drops him into the plaza's west corner.
- [ ] **G3. Moving platforms.** `platforms` in the JSON (`name`, `size`, `path`, `speed`, `wait_s`). Move the visual
  `PL_plat_<name>` and its collider `col_deck_mover_<name>` along the path, ping-pong with the wait; anything standing on it
  rides it (add the platform's delta to the player). *He sees:* the bell lift beside the clock tower goes up and down.
- [ ] **G4. Hide bins.** `hide_bin_00..11` (kind `hide_bin`, `color`; each has a box `col_bld_bins_NNN`). Jump into one within
  1 m: he becomes the bin (hide his rig, draw the bin at his position, walk at half speed, cops/guards/cameras ignore him);
  jump again to pop out with a hop. *He sees:* the orange bin on the promenade trundles about with him in it.
- [ ] **G5. Security cameras.** `cam_00..05` (kind `security_cam`: `yaw`, `sweep_deg`, `period_s`, `fov_deg`, `range_m`,
  `tilt_deg`, `shootable`, `hp`). Sweep; draw the fov as a faint cone/decal on the ground; on line of sight to the undisguised
  alien (not in a bin, not disguised) lurch, red light, and send the nearest two `npc_guard_*` to the spot. A bolt kills it
  (sparks, cone off). *He sees:* the nest-door camera sweeps, catches him, two guards come running.
- [ ] **G6. Enemies.** `enemy_walker_NN` (`spore_walker`: walk the `patrol`, turn at the ends, a stomp or one hit pops it) and
  `enemy_drone_NN` (`buzz_drone`: hover the patrol, a slow glowing shot every 2.5 s inside 18 m, two hits). Reuse the existing
  foe/body plumbing; placeholder shapes are fine. *He sees:* walkers on the roofs and the canal ledge, drones over the hover gaps.
- [ ] **G7. The events** (the older plaza list above, unchanged): bells in clock order -> shutter; sluice handle + 3 hits ->
  canal water drops 1.4 m; generators -> slab breakable; five cores -> beacon (waterfall off, vault door, lift, boulders).

**NEXT, AHEAD OF THE REST: LOAD THE ALIEN PLAZA AS ITS OWN LEVEL (`models/alien_plaza/`, pushed m436).** Colin is building
the alien side as SMALL hand-made levels, one at a time; this is Level 1, "Glowtide". Read `models/alien_plaza/README_ALIEN_PLAZA.md`
(the contract), `LEVELS.md` (cores, events, markers) and `ROUTES.txt` (every route, beat by beat). First build: a world key
`plaza` (`?w=plaza`) that loads the visual, the collision (the usual prefixes), spawns at `spawn_player`, draws the water levels
from the README, and puts every marker's `aw` name on the GOD place list. Measure it the F0a way. Then, one build each: the
movers and events in `alien_plaza_level.json` (bells in order -> shutter, sluice -> canal water drops 1.4 m, the generators,
the slab), the Hover Pack (hold jump in the air: 1.0 s of hover, +1.0 m lift, refills on the ground -- the checker's numbers),
the launcher NPC, the zipline, and the plaza fight's three waves. The geometry is final for these numbers: do not move ledges
to fit a different hover -- tell Colin and the Blender side re-runs the checker.

**NEXT BUILD, AHEAD OF PHASE F — THE ALIEN WORLD AS A NEW WORLD YOU CAN EXPLORE.** Colin's Blender session
pushed it in m431: `models/alien_world/`. **Read `models/alien_world/README_ALIEN_WORLD.md` first; it is the
contract** (units, origins, extras, `_CHUNK`, colliders, lights, lifts, critters, sky, splat shader). He
wants to load it, walk round it and find the bugs and the performance problems. Not a story, not a chapter.
1. **A new world key `alien` (`?w=alien`), in the world key and the GOD menu.** Load at one shared origin:
   `alien_town.glb` (260 x 260 m level + ~660 scatter instances), `alien_streets.glb`, `alien_coast.glb` +
   `alien_coast_collision.glb`, `alien_town_kit_buildings.glb` + its collision. The kit buildings follow the
   same contract as his Weirdport kit, so reuse `buildKit` / `kitSwap` / the breakable walls rather than a
   second path. Colliders by prefix as the README says (`col_deck_`/`deck_`/`ground_` walkable,
   `col_bld_`/`bld_` solid, `ramp_`, `climb_` ladders); never draw them.
2. **Look:** the sky dome or the pano as background + environment, the sun/hemi/fog numbers in the README,
   the splat shader for both terrains (town: grass/dirt/rock/moss; coast: sand in the G slot), water at
   y -2 (coast -6, canals -3/-0.9) with the existing water shader, below it = swim / put back. The
   PNG textures go through the repo's KTX2 path (`npm run ktxpng`) like the rest.
3. **Life:** the lift (`lifts` in placements), boats bob and balloons float (`extras.animate`), and some
   bodies walking the plaza and the streets so it isn't empty (existing NPCs; placed by a sweep of the
   real collider, never typed). Critters only if `critters.glb` is in the repo.
4. **Buildings from `alien_town_placements.json` load if their GLB is there and are skipped LOUDLY if not.
   25 building GLBs it names (spore_pharmacy, slime_cafe, ... signal_tower) are NOT in the repo yet**,
   nor `critters.glb` — Colin's Blender session has to push them. Show `NO BLD <n>` in the chip and a GOD
   toast listing the missing names, and build the rest. When they arrive they need no code change.
   Their `_CHUNK` / `chunks` / `lights` extras use the same breakable rules as the kit walls.
5. **Measure it** the F0a way (draw calls, triangles, texture memory, boot time) in the chip and NOTES,
   and cut whatever is far over budget: the scatter instanced, far copies, the fog cull. 45 MB of GLB on
   the wire is a lot for a phone, so say what the boot costs.
6. **Spawn** on the plaza, searched not typed. GOD places: town plaza, streets/skyway, coast plaza, the
   summit, the sky islands, the fire region, the goo region, the crash crater. `npm run places` covers them.
Split it over as many builds as it takes; ship the load-and-walk first. Then go back to Phase F.


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
  - [x] m428 **F0a Measure every world** as it is now: draw calls, triangles, resident texture memory and
    boot time per world, printed in the chip and in NOTES. Set a budget per world for a phone (draw
    calls in the low hundreds, textures KTX2, nothing resident that isn't on screen) and cut the worst
    offenders: instance, merge, fade with distance, cull by chunk, drop what nobody sees. Repeat per
    world until each is inside its budget.
    Split:
    - [x] m416 **F0a-1** the measure: `TX`/`G`/`boot` in the chip's perf line, `mel.mem()`, and `npm run worlds` (every world, every region, against the budget; exits 1 on OVER).
    - [x] m428 **F0a-2** cut the worst offender in the kit city (the biggest OVER in the `worlds` table), one world or one offender per build, until `npm run worlds` exits 0. Split: *(closed at m428 with its overs stated under Decision m428 -- the kit city in town and the toon city's spawn are still over; the kit, Weirdport and the test site are inside)*
      - [x] m417 **F0a-2a** the far culls: bodies beyond 150 m and the kit's moving parts beyond 220 m are not drawn (7 of 14 places inside the draw budget; every place halved).
      - [x] m418 **F0a-2b** the unnamed `Mesh` draws (150-250 at the Waterfront's cliff, the islands' landing, the trailer park): name them in `--who`, then merge or instance them.
      - [x] m419 **F0a-2c** Old Town from inside and from the islands: the kit batch is 790 cell meshes; far cells as one merged LOD per material, near cells as now.
      - [x] m420 **F0a-2e** the same far copy for the toon city's own cell merges (`tcmerge_*`) and its instanced props (`tc_*`, 10-16 draws a type from the islands); the kit's doors (54 sets, one per door geometry) need `BatchedMesh`/multi-draw and wait.
      - [x] m421 **F0a-2f** Old Town from inside: the doors as one `BatchedMesh` per material where `WEBGL_multi_draw` answers (the instanced sets otherwise), a body's small parts not drawn past 45 m; the measure's body cull fixed (it had called the wrong function, so every in-town number since m417 had the crowd hidden). Honest Old Town: 835 → 598.
      - [x] m422 **F0a-2g** the body LOD, done right: m421's parts cull had hidden every body's MAIN mesh past 45 m (a skinned mesh's size is not readable off its spheres at spawn); parts are now judged relative to the body (under a quarter of its biggest mesh). Honest Old Town: 610.
      - [x] m423 **F0a-2h** the second draw per body was its SHADOW (79 depth draws of 618 in town, found by counting draws by material type); a body casts one only within 30 m now. The farm batches in view (45) are Old Town's own places in their paint materials and stay; the dressing (14) stays.
      - [x] m427 **F0a-2d** the textures (270 MB): Moussa's two 2K maps to KTX2 or 1K, the impact atlas and the HDRI; then the other worlds. Split:
        - [x] m424 **F0a-2d-1** the nine biggest character/vehicle GLBs baked to KTX2 (UASTC) and swapped in at load: 270 → 193 MB in the kit city.
        - [x] m425 **F0a-2d-2** the loose sheets and atlases as .ktx2 (`npm run ktxpng`, taken at load by `texLoad`), four more GLBs (zap, her, the base, the tower): the kit city 193 → 176 MB, Weirdport 240 → 128, the test site 202 → 78.
        - [x] m427 **F0a-2d-3** the sky on the GPU as KTX2 (the PNG read once for the fog, never uploaded): 176 → 170 MB; the alien's glow hue read off the GPU now that its map is compressed (the bake had broken it: `HUE READ FAILED`). The paint atlas (a 1K canvas, the farm's look) and one unnamed 1K map are the last 10 MB and stay.
      - [x] m428 **F0a-2i** the fog cull for everything: anything unregistered between the fog's end (320 m) and the lens's far plane (400-470) was drawn in pure fog colour; every plain mesh that trusts its own sphere is culled past the fog now, a fog-off material (the beacons, the Mothership) never is, the turf dressing has a real sphere, and Weirdport's instanced trees and cars are keyed by 48 m cell (1,474 → 992 kT, inside). Old Town 589 DC / 1,565 kT, the islands' landing 318, the rest of the kit city's places inside on draws.
  - [x] m486 **F0b A headless playthrough** (`npm run play`): drive Chapter 0 to the end through the shipped
    quest steps and the shipped `godPlace`, every gate and boss in order, and fail if any step can't
    complete. Run it before every build that touches a quest, a gate or a chapter from now on. Split:
    - [x] m429 **F0b-1** the harness and Chapter 0: the shipped game booted headless on a fresh save, its frame stepped on a fake clock, the pads driven (walk, strike, sample hold, talk tap), a gate walked, a teleport only when a walk is stuck (said in the row). Chapter 0 passes its seven steps in 54 s. **Its first run found that the kit city had thrown on every frame since m336** (the hat's tip wrote `.material.` on a material), so nothing after `cartStep` ran -- the render included. Fixed.
    - [x] m486 **F0b-2** Chapters 1 to 6 (`npm run play ch1 ch2 ...`), one chapter per build: each chapter's own step types get a driver (the Skinsuit turn and its knock-downs, `reach`, the bosses' downs, a bike, the glider, the ferry and the trains as the ways in), until every gate and boss passes in order. A chapter that cannot be driven through the shipped steps is a finding about the chapter, not the tool. Split:
      - [x] m430 **F0b-2a** Chapter 1: the turn watched, the Skinsuit knocked down each time it is up, the fix gate leaned on, the talks as the crew, the boss and the two turned crew; the shipped picker drives the quest order (the incursion's own quest included when its ship comes); a seeded random (`--seed`), a NaN watchdog with the last frames' trace, teleports to the target's level. Three seeds pass all four quests (17 steps) in about three minutes each. **Found and fixed: a `fix` gate's lean counted only while pressed inside the slab's half-thickness (0.49 m); a thumb resting 3 cm off it saw "Fixing... 1%" for ever.**
      - [x] m486 **F0b-2b** Chapters 2 to 6, one per build: `reach` (a climb or a jump), the Pearl's barricades inside the march, the roofs, the ferry and the swing bridge, the freight line, a bike, the glider, the islands' crossings and the Mothership's shaft; the bosses' downs.
        - [x] m468 **F0b-2b-1** Chapter 2: a chapter-N start carries the forms and the quests (so the kit) the chapters before it gave; the flag driver walks inside the game's own radius. 14 steps, 3 quests in 115 s. Ash's after-talk failed once in four runs (18 teleports, never in talk reach) and is unsettled.
        - [x] m470 **F0b-2b-2** Chapter 3 (Hollow Creek): 12 steps, 3 quests in 155 s -- the race WON at Rae's own 15 m/s in 51 s. Found and fixed on the way: **the biker never rode his bike** (since m374), the start hill's back stairs stopped every lap 2, a knocked body over the creek fell to -1000 for good, and `npm run places` had died at boot since m425.
        - [x] m479 **F0b-2b-3a** Chapter 4's first quest (`ch4`): the ferry ridden (board at Old Town, round the cabin to the far half, off over its own end), Rosa and Dex as the worker (the talk driver now picks the form by the speaker's group), an engineer's face (a role form), Uplift's gate. 5 steps.
        - [x] m480 **F0b-2b-3b** the orb side-quest the picker takes next (`qorb`: shoot down the pacifier orb -- the blaster through the pads, the camera at it), then `ch4b` (the control room, the lever, the line freed) and `ch4c` (the supervisor).
        - [x] m481 **F0b-2b-4a** Chapter 5's first quest (`ch5`): the rope bridges walked span by span, Rue, Rollergirl, up the mesa, Teo. 5 steps.
        - [x] m482 **F0b-2b-4b-1** `ch5b.0`: Skye's form (his kind sampled) and a glide from 7 m short of the cross, a dive onto it: down inside the cones.
        - [x] m483 **F0b-2b-4b-2** `ch5b.1` THE GAP -- a finding first: on the board down the in-run (3.6 m of drop, ~12 m/s expected at g 20 and `SKSPEED.slope` 11) he reaches the kick at 1-3 m/s and stalls there, every run. Find why (the grade on the deck's triangles? the kick's first quads?) and fix it in the game; then the needle (`ch5b.2`).
        - [x] m484 **F0b-2b-4c-1** the islands made fair: a body out of the world (under it, or a quest's body in the sea) is put back where it last STOOD on a floor; a body turned or cured out there comes out at that spot; the gap's landing moved to where a real run comes down; the board leaves a curved lip on its angle at speed. Gap cleared in ~14 s (most seeds); the keeper beaten on seed 2.
        - [x] m485 **F0b-2b-4c-2** what is left of `ch5c`: the gap is still wind-dependent on some seeds (a head gust lands it short), and on seed 1 the driver ends up on the lighthouse's top after every teleport down to the boss (the sea's put-back takes him up there) -- look at where `islePutBack` sends him off the lighthouse rock.
        - [x] m486 **F0b-2b-5** Chapter 6 (the Mothership): 15 steps, 3 quests in 125 s -- the pod up the tether, the six locks each in its own form, the shaft, the seven-down boss, the end.
  - [x] m487 **F0c Every world boots** through the real loader with no red toast (`npm run worlds:boot`: the shipped page in headless Chromium, every world, a note in the chip's red list or a page error is BAD). 6 of 7 clean; `alien` keeps `GLB NO IMG 20` on purpose (see Decisions).
- [x] m511 **F1 Polish passes, region by region, with `npm run shot`.** The farm had five; each of the others
  gets at least three, one build each, fixing the worst thing in the shots and checked against the
  world rules (exaggerated scale, connective tissue, vertical, no straight borders, nothing bare):
  Old Town, The Pearl, Hollow Creek, the Waterfront, the River Islands, the Mothership. Then the
  routes between them (the trestle, the ferry, the freight line, the bridges) as places in their own
  right, with something on every one.
  - [x] m488 **F1-OT1** Old Town 1 -- the food-cart pod: the worst shot (four carts in a row on bare lawn, tables on grass). A
    paved pad fraying into the grass, a timber deck in two skewed slabs with steps (the tables on it), a shade sail, crates,
    gas bottles, plants, three umbrella colours.
  - [x] m489 **F1-OT2** Old Town 2 -- the camp at the west edge: a trampled-dirt floor, a patchwork tarp roof on four poles over the fire circle, junk fencing round the open sides with gaps to walk in, a shack with a stovepipe, tins of herbs.
  - [x] m490 **F1-OT3** Old Town 3 -- re-shot; the worst was the footbridge's foot (a stair in bare lawn, no way to it): a flagstone path from the street, a concrete apron, a works hut with its lamp, sandbags, a rope barrier, a CLOSED board, a lifebuoy, driftwood and stones on the tideline, a bench facing the water.
  - [x] m491 **F1-PE1** The Pearl 1 -- the plaza (a bare grey slab between the warehouses): bunting and bulbs criss-crossing it roof to roof, a painted floor (a sun before the stage, swirls, footprints), four corner community beds with sunflowers (.3 m kerbs, under his step).
  - [x] m492 **F1-PE2** The Pearl 2 -- the pier (grey slabs edged by bare rails): plank seams on every deck, a mooring line of bollards with rope coils, lamp posts and life rings along every rail, fisher's clutter (crates, pots, a drying net) at dock 1's corners; pots and three-blob clumps on the loading platforms, crowned trees down the dock street.
  - [x] m493 **F1-PE3** The Pearl 3 -- dock 1, where Chapter 2 lands (painted cube pots, bare boards): round tapered pots with clumps and blooms, round bollards with rope, plank seams, a fish-crate stack and a sack by the bridge, the roastery's chalkboard, hanging baskets off the lamps, clumps and a pennant on the container garden.
  - [x] m494 **F1-HC1** Hollow Creek 1 -- the halt, the region's front door by train (a plank and a red roof): board seams and a yellow edge line, a bench and a timetable under the shelter, churns and mail sacks, lamps with hanging baskets; at the creek end's foot a gravel apron, a fenced dirt track, a water tank for the loco, wildflowers round the posts.
  - [x] m496 **F1-HC2** Hollow Creek 2 -- **the race is winnable again** (`play ch3` COMPLETE, Rae beaten in 48 s): a gate run wide still counts (it voided the lap silently since m483), a spill into the creek puts him back ON THE TRACK where he left it, not 27 m back up the ridge; the bike keeps its pre-m483 grade window.
  - [x] m498 **F1-HC2b** Hollow Creek 2b -- the bike track dressed: two worn ruts down the racing line, flags on poles every 16 m, red-and-white spectator tape on stakes down every straight, a HOLLOW CREEK MX banner arch on tyre-stacked posts over the north straight. Nothing beside the track has a collider.
  - [x] m499 **F1-HC3** Hollow Creek 3 -- the mill (a grey box on the grass): corrugation ribs round all four walls, rust streaks off the eaves, a concrete plinth, a HOLLOW CREEK LUMBER sign over the big door; in the yard two lumber stacks on bearers, an offcut heap, a chopping stump with its axe, sawdust drifts.
  - [x] m500 **F1-WF1** the Waterfront 1 -- the quay floor (300 m of one grey): slab joints every 8 m, white container-bay lines and bay numbers in the yard, yellow-hatched strips, oil stains, puddles, manholes and drain grates. All flat, no colliders.
  - [x] m501 **F1-WF2** the Waterfront 2 -- the ferry pontoons (bare grey rafts): yellow safety edges, deck seams, tyres hung at the waterline, cast bollards and a rope coil; the far one gets a lamp, a lifebuoy, crates and a THE WATERFRONT board at the stair's foot.
  - [x] m502 **F1-WF3** the Waterfront 3 -- Uplift's lot (the public quay's bare concrete behind a fence): a green walkway from the gate with UPLIFT stencilled on it, parking bays and three company vans, topiary planters on .3 kerbs, three green flags, a HAPPY WORKERS ARE PRODUCTIVE WORKERS billboard on the fence.
  - [x] m503 **F1-IS1** the River Islands 1 -- lighthouse rock (a white tube and two bands): the lantern's gallery rail and mullions, a door, a stone apron, windows up the tower; the keeper's cottage with its chimney, an oil store with drums, a flag, a washing line, lobster pots, a rope coil.
  - [x] m504 **F1-IS2** the River Islands 2 -- Rue's field (cones on a lawn): two painted rings round the cross, stepping stones up from the rope bridge, Rue's canopy and table, a rack of folded wings, a chalkboard, a bench, wildflowers -- nothing solid within 9 m of the cross.
  - [x] m505 **F1-IS3** the River Islands 3 -- the skate park (a clean deck with ramps): paint splashed on the planks, dark patched planks, string lights on poles down both rails, paint up the quarter pipe's platform and the funbox, and the hangout at the island end -- a sofa, a cooler, a speaker on a crate, boards on the rail.
  - [x] m506 **F1-MS1** the Mothership 1 -- the decks (one flat purple): in the chamber a glowing ring at the wall's foot, radial seams, a cable from every pod to the machine, conduits up the wall, a light ring round the ceiling; glow strips down both tubes; on the bridge a lit ring round the floor disc, console lights and a turning holo-globe.
  - [x] m507 **F1-MS2** the Mothership 2 -- the belly (a purple drum): floor seams out from the glass, a glow ring at the wall's foot, veins snaking up the wall, clutches of eggs at its foot, glyph panels, tendrils hanging round the organ. Nothing near the doorway; nothing solid.
  - [x] m508 **F1-MS3** the Mothership 3 -- the core (an empty dome): two glow rings and 12 seams across the floor, ribs of light up the dome's inside, eight nerves arcing from the dome's wall down into the shaft's mouth, glow strips climbing the shaft. Nothing solid -- it is the last fight's floor.
  - [x] m509 **F1-RT1** the routes 1 -- the freight trestle (a bare line over the water): signal masts with lit lamps every 45 m, mileposts every 30, and halfway over a railed refuge off the side with a tool chest, cable, a fisherman's bucket and rod, gulls on the rail (GOD place `frrefuge`).
  - [x] m510 **F1-RT2** the routes 2 -- the swing bridge (a grey road): dashed lane lines and painted walking strips on both fixed spans, drain grates, a BRIDGE SWINGS / WAIT AT RED board facing each swing gap, and Walt's fishing pitch at the island end -- rods over the rail, a bucket, a stool, a cool box -- with a lifebuoy.
  - [x] m511 **F1-RT3** the routes 3 -- the road bridge into Hollow Creek (a clean grey deck): potholes, gutter litter, a broken-down car with its hood up, green distance signs each end; at the gang's end two parked bikes, a tyre stack, a cooler and cans, pennants down both rails, spray tags.
- [ ] **F2 The regions still missing from `REGIONS.md`**, each as land → places → people → the ways in
  (several, per the connective-tissue rules) → its quests and boss. Read the entry first.
  - [x] m526 **F2a The Underneath** (3): the tunnels under Old Town, the Pearl and the Waterfront, surfacing in
    cellars and drains; the hobo's and the miner's region; the safe-house portals.
    - [x] m512 **F2a-1** the land: a hatch on the footbridge's apron down to a shaft room 28 m under the sea's level; a brick tunnel to a junction, the CISTERN (black water, two catwalks, teal growth) off it, a second tunnel to a second shaft that surfaces at a manhole in Old Town. Lanterns, pipes, dark brick. GOD place `underneath`.
    - [x] m513 **F2a-2** its people: THE CAMP off the cistern's north ledge (bedrolls round a fire barrel, a tarp, candles in bottles, a cart, washing) and THE HIDDEN MARKET east of the junction (six tarp stalls of found goods under strung bulbs, a smuggler's counter with a scale); Rook, Aunt Mags, Tibbs, Fennick, Cass, June. (The hobo form's way in moves to F2a-5 with the miner's.)
    - [x] m522 **F2a-3** the water level: the PUMP ROOM off the cistern's west wall -- step on the grate by the wheel and the cistern drains (y -.3 to -2.6) or fills. LOW: down a stair off the west ledge, under the south ledge, into the SMUGGLERS' VAULT at the pit's floor; but the second tunnel's SLUICE GATE drops shut. HIGH: the vault is under black water, the way to the second shaft is open.
    - [x] m524 **F2a-4** the other surfacings: THE CROSSWAYS east of the market -- a shaft up a drain into the Pearl (the dock street's side), a shaft up to a cellar door at the Waterfront's transit shed, and the GOOD ALIENS' SAFE HOUSE (cots, a laid table, plants under a grow lamp, Pell and Wren, a portal pad `under_safe`).
    - [x] m526 **F2a-5** the Underneath's quest (THE UNDERNEATH, a side quest from Aunt Mags: drain the cistern, the vault, through the collapse to the safe house, Pell) and THE COLLAPSE between the crossways and the safe house -- a gate cleared by somebody who digs. The cave miner's own form waits for his model (F4); the construction worker digs in his place.
  - [x] m538 **F2b Dump Tower** (6): the vertical level, the Reptilians' seat. It goes BEFORE the Mothership in
    the chapter order (Dump Tower is the last stop in the metropolis; renumber the chapters and the
    Mothership's six locks become seven).
    - [x] m528 **F2b-1** the tower: ten floors on its own plaza west of the city (lobby, offices, a gym, a sky garden, the boardroom, the penthouse) joined by a switchback stair, glass curtain walls with gold mullions, the helipad on the roof. GOD places `dtplaza`, `dtroof`.
    - [x] m530 **F2b-2** the lifts and the badges: a lift car that only answers a badge for its floor band; the badge cards found or lifted from the people who carry them.
    - [x] m532 **F2b-3** its people and the corporate ladder: staff per floor, the Reptilian suits, a promotion that opens the next band.
    - [x] m534 **F2b-4** the ways in and out: the tram stop at the plaza, a glider off the helipad.
    - [x] m535 **F2b-5a** the chapter: CHAPTER 6 · DUMP TOWER (the three badges, then Mr. Dump in the penthouse -- six knock-downs), the Mothership renumbered Chapter 7.
    - [x] m538 **F2b-5b** the Mothership's seventh lock: a suit's lock (the boardroom's own), between the neural lock and the shaft; Benny's "six ways" becomes seven.
  - [x] m615 **F2c The Gorge** (7): falls, the stilt village, the scuba diver; between Hollow Creek and the
    River Islands, down the log flume.
    - [x] m543 **F2c-1** the land: its own landmass past the islands (+z), a plateau ~24 m, the upper river in a canyon at 13 m, THE FALLS (15 m, straight into the sea), the fjord below them out to the coast, pines. GOD `gzfalls`, `gzriver`.
    - [x] m551 **F2c-2** the caves behind the falls (a ledge path behind the sheet, a cave with a way up to the upper river), spray, rainbows in it, the falls' sound.
    - [x] m558 **F2c-3** the stilt village: houses on stilts along the fjord's wall, walkways and rope bridges between them and across, fishers and river guides.
    - [x] m576 **F2c-4** the dam gates upstream: shut them and the falls dry to a trickle and the cave mouth opens; open them and they roar.
    - [x] m584 **F2c-5a** the diver (Nell, on the west walk) and SWIMMING as the diver: sink, hold to rise, a kick out of the water onto a 1.6 m ledge -- so the cave behind the falls is reached from below.
    - [x] m594 **F2c-5b** the underwater caves under the fjord: a sunken wreck and a lit grotto in the fjord floor with a cache; a swimming pose (he plays the fall pose in the water now).
    - [x] m609 **F2c-6a** the lookout at the fjord's mouth and the glider to the islands (Ari, a glider pilot to wear); the Gorge's region on the map.
    - [x] m615 **F2c-6b** down the log flume and the rapids from Hollow Creek: the mill's flume runs on, down a rapids channel, into the Gorge's upper river.
  - [x] m684 **F2d The Hothouse** (9): the alien takeover, as a region that grows across the map while the
    grid stands and shrinks as you cure districts.
    - [x] m633 **F2d-1** the growth: any Old Town block the Skinsuits hold (turf `skin`) is overgrown -- vine arches over the street, glowing fronds, pods, wet moss -- growing in as it falls and dying back as it is taken. GOD `hothouse`.
    - [x] m642 **F2d-2** the twilight and the spread: inside a held block the light goes to bioluminescent twilight; the Skinsuits push into the blocks next to theirs on a clock unless you cut it back (shoot or swing the pods and vines to take the block's share off them).
    - [x] m648 **F2d-3** its heart: one block fully grown -- walkable vine bridges between the roofs, a pod nursery with half-turned civilians in the pods, its own GOD place.
    - [x] m650 **F2d-4a** its people: Skinsuits patrol the heart's block and their own on a beat round the block (the turf crowd adds more where they hold).
    - [x] m680 **F2d-4b** the way on: a spore pod from the nursery's mother pod up to the Mothership's tether (a ride, like the tower's tram).
    - [x] m684 **F2d-5** the chapter's beat: cure the city's held blocks back, a quest that holds it together.
  - [x] m702 **F2e The metropolis hub**: the tall city in the middle of the map that the other regions ring,
    opened a part at a time as chapters complete; Dump Tower stands in it.
    - [x] m689 **F2e-1** the core's towers: a packed cluster of skyscrapers round Dump Tower on the west ring, solid to one shared terrace level (Dump Tower's sky-garden floor), set back above it, sky-bridges between facing terraces, a fire escape up from the street, lit windows, roof tanks. GOD `core`.
    - [x] m694 **F2e-2** the way across: a sky-bridge from the nearest terrace into Dump Tower's sky garden, and street life at the towers' feet (lobbies, kiosks, a crossing, traffic islands) so the streets between them are a place, not gaps.
    - [x] m696 **F2e-3** the workers who keep it running: window cleaners on cradles down the faces, a lift engineer, street sweepers, a doorman per lobby -- people with a beat and lines.
    - [x] m700 **F2e-4** the alien grip: beams from Dump Tower's crown to the towers' roofs, the core dim and its streets fenced while they stand; each region cured (chapter done) cuts one beam and lights a tower back up, the last at Chapter 6.
    - [x] m702 **F2e-5** the horizon agrees: the distant skyline (`SKYLINE`) re-aimed or retired so what you see from the farm is the core you can walk to.
- [x] m726 **F3 The rest of the grid and the fail states** (`LORE.md`): the projector, poltergeist and relay
  orbs; the EM tell (lights flicker, cars stall, radios hiss near the grid); the Hum; black triangles at
  night and tic-tacs that chase flyers; **missing time** as the capture fail state and something at
  zero health (Colin's open question: propose one, build it switchable).
  - [x] m705 **F3-1** the projector orb: a hologram police roadblock across Dump Tower's plaza approach, solid until its orb is shot down (it tears into static and goes). GOD `projector`.
  - [x] m708 **F3-2** the poltergeist orb: one Old Town building haunted -- lights flicker, a door slams, furniture is thrown out of its windows at you; shoot the orb and it stops. Animals react first (a dog barks).
  - [x] m711 **F3-3** the relay orb: links the others into the grid -- while it stands they take half damage and re-light if downed; shoot it and every orb it fed drops a hit.
  - [x] m717 **F3-4** the EM tell: near any live orb or alien activity streetlights flicker, cars stall in the road, radios hiss.
  - [x] m720 **F3-5** the Hum: an ambient drone whose loudness follows how much of the grid stands where you are; a freed district goes quiet.
  - [x] m721 **F3-6a** a black triangle circles Old Town and the core high up and drops seeker orbs that follow you and call the Skinsuits if their light stays on you.
  - [x] m724 **F3-6b** tic-tacs: white capsules that chase you when you are gliding or flying, fast and jinking; shoot one down or land to lose them.
  - [x] m726 **F3-7** missing time (captured: white-out, wake somewhere else minutes later, juice drained) and a zero-health state, switchable.
- [x] m745 **F4 The forms still missing** from the forms table, each with the door it opens: cop (cordons,
  arrest), firefighter (fires, the truck ladder), hobo as stealth (guards ignore him), CEO (Dump Tower),
  scuba diver (the Gorge), cave miner (the Underneath), military (the base at high heat).
  - [x] m731 **F4-1** the hobo as stealth: Uplift's turrets and robots look straight through a man in the hobo's coat.
  - [x] m733 **F4-2** the cop's arrest: as a cop, hold the right pad on a Skinsuit you have knocked down to cuff it (it is taken away and the block's turf moves), and the cop's car at the cordon is yours to drive off.
  - [x] m735 **F4-3** the firefighter's truck ladder: a fire engine parked by a burning building in Old Town whose ladder only a firefighter can raise -- up to a roof that has no other way on.
  - [x] m738 **F4-4** the cave miner (the Underneath): a miner to sample in the Underneath, whose lamp lights the dark tunnels and whose pick breaks the rubble walls that block them.
  - [x] m745 **F4-5** the military (the base at high heat): at four stars soldiers come instead of cops; a soldier's form walks through the military cordon round the base.
    - [x] m740 **F4-5a** at four stars the reinforcements are soldiers (the roster's olive officer in a helmet), and a soldier shoots further, faster and straighter than a cop.
    - [x] m743 **F4-5b** the SOLDIER form (sample a downed soldier) and the `military` gate type only that form walks through; a soldier passes a police cordon too.
    - [x] m745 **F4-5c** the base: a National Guard post at Hollow Creek's far edge (the road out toward Area 15), walled in sandbags and wire, with a watchtower, tents, a motor pool and a supply cage inside, ringed by the `military` cordon. A soldier walks in; anyone else is turned round and noticed.
- [ ] **F5 Side quests**, one build each, from the table in `LORE.md`, in this order: the Roswell diner,
  the tinfoil-hat bunker (the grid on the map), the Majestic Dozen, Mothman, the Phoenix Lights, the
  haunted ranch, the tic-tac pilot, Bigfoot, D.B. Cooper, Betty & Barney, Travis Walton, Area 15.
  - [x] m761 **F5-1** the Roswell diner. Split:
    - [x] m750 **F5-1a** Saucer Joe's: the diner (walk in: counter, stools, booths, Joe), its roof up a ladder, the sign tower with a saucer on top, the quonset museum, the lot, and the fenced "replica" saucer that hums for the alien.
    - [x] m756 **F5-1b** the three parts Joe names (a coil, a lens, a silver gyro), one hidden in each of three places across the map, and the quest (`qsaucer`) that tracks them.
    - [x] m761 **F5-1c** the saucer fixed: bring the parts, it lifts off its plinth, and it is yours (a portal back to the diner, and a short hop you can ride).
  - [x] m770 **F5-2** the tinfoil-hat bunker. Split:
    - [x] m765 **F5-2a** Merle's bunker: a half-buried container in a clearing on Hollow Creek's hill (his wall of string inside, a radio desk, a cot, cans), a lookout on stilts with a telescope, a foil mast, solar panels, a garden, a fire pit, tin cans on strings round it, and Merle in his tinfoil hat.
    - [x] m770 **F5-2b** his evidence: bring him three things the orbs leave behind (a shard off a downed orb, a recording of the HUM, a photo of the triangle), and he maps the grid: every orb and the lines between them on your map.
  - [x] m783 **F5-3** the Majestic Dozen. Split:
    - [x] m778 **F5-3a** their twelve dossiers, one on each of twelve places across the map, each a card of what they have done; the first switches the quest on.
    - [x] m783 **F5-3b** the boardroom at the top of Dump Tower, opened by all twelve (`mj:all`): the eleven chairs, the twelfth that is not a man, and what it says.
  - [ ] **F5-4** Mothman. Split:
    - [x] m793 **F5-4a** the thing on the Hollow Creek bridge: walk up and it flies off to a place in Old Town and hangs over a glowing pod; stand on the pod before the fuse runs out or the place goes up in flames. It is back on the bridge four minutes later for the next one.
    - [ ] **F5-4b** warnings on your map: once you have saved one, every omen shows on the map (a moth over the place) from the moment he leaves the bridge, and the next site is marked while he waits.
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
- **m419 (F0a-2c) The far copies.** A cell-batched set seen from outside is now one mesh per material: the kit city's 790 cell batches have a **far copy** (the same geometry merged once more per material, 10.7 MB) that draws instead of the cells whenever the lens is more than **140 m** outside the buildings' rectangle (`KIT.lodOut`); the farm batches (every region's frames, in 200 m cells) get a **flat** far copy per cell (one flat-shaded vertex-colour material, no normals: paint, metal and glow dropped, which at **180 m** is nothing; `FBATCH.lodOut`). A broken wall is whole in its far copy. The gates' posts and boards are merged too. Like for like: the islands' landing 1,098 → 534 draws, the needle 667 → 395, the container cliff 798 → 399, the trailer park 421 → 273, the farm's west hill 327 → 211. The cost is geometry: 108 → 161 MB resident, over my 128 MB budget; I'd rather carry 33 MB of copies than 500 draw calls, and the textures (270 MB) are the bigger number anyway. GOD → SWITCHES → **THE FAR COPIES ON/OFF** is the A/B; the chip's `L<far>/<groups>` says how many sets are drawing their copy. Overrule the two distances or the memory call.
- **m420 (F0a-2e) The toon city's far copy.** The city's own cell merges and its instanced props (soda cans, cups, weeds, planters, lampposts -- one InstancedMesh per prop per 48 m cell, 10-16 draws a type from the islands) get a far copy too: the merges re-merged per material (8 MB, same tinted materials), the props as one InstancedMesh per prop holding every instance (matrices only). It takes over **90 m** outside the city's merges (`TCITY.lodOut`; they run to the shore, so 140 m would have left the landing rock inside). The islands' landing 534 → 360 draws, the container cliff 399 → 323, the needle 395 → 323. The kit's **doors** stay 54 draws in town: they are 54 instanced sets, one per door geometry, and folding them into one draw per material needs three's `BatchedMesh`, which is one draw only where `WEBGL_multi_draw` exists (iOS 17.4+) and a draw per door where it doesn't -- I won't ship that blind. Old Town from inside (741) is the next sub-item after the textures. Overrule the 90 m.
- **m421 (F0a-2f) Old Town from inside.** First a confession: the measure had been calling the wrong function for the body cull since m417 (`perfStep` instead of `bodyCull`), so every in-town number I reported from m417 to m420 was taken with most of the crowd hidden. The honest Old Town figure before this build was **835** draws, 74 bodies within 150 m. Two cuts, both mine: **(1)** the kit's moving parts (doors, lids, AC units) are one `BatchedMesh` per material -- one draw call -- **only where the GPU reports `WEBGL_multi_draw`** (iOS 17.4+; the chip says `md` when it does), and the 54 instanced sets otherwise; **(2)** a body's small meshes (eyes, teeth, shoes, headphones, a hat: anything under 0.45 m across) stop drawing past **45 m** (`mel.PERF.partFar`, 0 = never). Old Town 835 → **598**, the protest square 401, the camp 205. Only two places are over the draw budget now (Old Town 598, the landing 323); triangles are over at five (1.2-1.35M). What is left in town is the crowd itself: 74 bodies at six to ten draws each. Overrule the 45 m, or tell me your iOS version.
- **m422 (F0a-2g) The body LOD, done right.** A bug of mine to own: m421's "small parts" cull judged a body's meshes by their bounding sphere times their world scale, which for a skinned Mixamo rig reads one centimetre for a whole man (the armature is 0.01 and the bones undo it) -- so every body's **main mesh** was registered as a small part and stopped drawing past 45 m. Bodies vanished past 45 m, and my measure couldn't see it because it counted bodies by `root.visible`, not by render layer. Fixed: a part is now judged **relative to its own body** -- any mesh under a quarter of the body's biggest mesh (eyes, teeth, trainers, headphones; heads stay) -- and the measure's body tool lists what each body is made of and which parts are culled. The honest Old Town figure is **610** draws with all 74 bodies within 150 m drawn. Overrule the quarter.
- **m423 (F0a-2h) A body's second draw was its shadow.** Counting the frame's draws by material type answered the question: in Old Town 79 of 618 draws were bodies drawn a second time into the shadow map (every body casts), plus 16 static casters. A shadow at 30 m is nothing, so a body casts one only within **30 m** of the lens now (`mel.PERF.shadowFar`, 0 = always): 79 depth draws → 14. The frame-to-frame noise in town is about ±30 draws (the crowd walks, talk marks come and go), so the total reads 611 rather than the ~555 the cut implies; the depth count is the honest number. The farm batches in view (45) are Old Town's own places -- the camp, the carts, the site, the square -- in their painted materials, and I'm not flattening those; the dressing's 14 instanced sets stay too. That closes the in-town work for now; the textures are next. Overrule the 30 m.
- **m424 (F0a-2d-1) The characters' textures, GPU-compressed.** `npm run ktx` (your own tool from the city bake; its two npm packages had to be installed here first) baked the nine GLBs with the biggest maps -- Moussa, Colin, Jack, the antenna alien, the warrior, the rollerskater, the officer, the construction worker and the dump truck -- to KTX2 **UASTC** (ASTC on iOS, near-lossless; ETC1S would be an eighth the memory but softer, and these are faces), geometry byte for byte. Resident: 117 MB → 28 for the nine; the kit city's textures **270 → 193 MB**. The swap happens at load in the one place a GLB is fetched, so every table keeps your path and every kind keeps its name; a twin only loads when the bump has hashed it, so a re-export falls back to your file until `npm run ktx` is re-run on it. The cost is the wire: UASTC is not supercompressed, so Moussa is 9.2 MB to download instead of 0.8 (about +22 MB across the nine, cached by the phone after the first load and unchanged between builds). Overrule UASTC for ETC1S on the crowd, or the wire cost.
- **m425 (F0a-2d-2) The loose sheets, and four more GLBs.** A second baker, `npm run ktxpng <png>`, turns a sprite sheet or atlas that `TextureLoader` fetches on its own into a `.ktx2` beside it (y-flipped, so the sheets' frame maths reads the same picture; the fire, water and crack sheets without mips, since they're sampled without), and the game takes the twin at load through the same KTX2 loader the GLBs use when the bump has hashed it. Baked: the impact-mark atlas (8 → 2 MB), the three fire sheets, the water sheet, the crack sheet, Weirdport's 2K trim (21 → 5), and the GLBs of zap, the purple alien, the alien base and the alien tower (21 → 5 each). The sky's image stays a PNG on purpose: the fog samples its pixels. Resident textures: the kit city **193 → 176 MB**, Weirdport **240 → 128**, the test site **202 → 78**; the latter two are inside the budget now, the kit city is 16 MB over, which is the next sub-item. Overrule UASTC on the sheets (ETC1S would halve them again).
- **m427 (F0a-2d-3) The sky, and a regression caught.** (The build is m427, not m426: the bump ran twice in this pass, once before a boot gate failure and again before the push.) The sky's equirect was 8 MB of RGBA drawn every frame as `scene.background`; it's a 2 MB KTX2 now, and the PNG is fetched once as a plain image for the fog's horizon colour (which is sampled off the picture, not typed) and dropped: the kit city 176 → 170 MB. Two things the measure caught on the way: (1) `skyLoad` runs at module scope, before the loader helpers exist -- the boot gate stopped a blank page, and the KTX2 path waits a tick; (2) every world's chip had grown **`HUE READ FAILED alien`** since m425 baked zap's map: the alien's glow hue is measured off his texture at load through a canvas, and a compressed texture has nothing a canvas can draw. It's read off the GPU now (the texture drawn onto a 128-pixel target and read back), so the measure stays a measure. The last 10 MB over my 160 are the farm paint's 1K atlas (the look) and one unnamed 1K map; I'm leaving them. Overrule the 160.
- **m428 (F0a-2i) The fog cull, and F0a closed with its overs stated.** The lens draws to 400 m (470 in the farmland's long view) and the fog ends at 320, so anything no builder had registered for the cull was drawn invisibly in that band -- at Old Town a stilt house's twenty boxes 415 m out, an instanced set at 432. Every plain mesh that opts into three's own frustum culling is on the fog cull now (its sphere is the one three already trusts); things that opt out stay out, and **a material with its fog off is never culled**, because that flag is how the beacons, the Mothership's hull and glow and the clouds say they're meant to be seen across the map (m418's small-thing cull had been taking the beacons' rings; fixed). The turf dressing's thirteen instanced sets had no sphere at all (13 draws from everywhere); they have one off their placements now. And Weirdport's instanced trees and cars (700 of its 1,400 kT, every instance every frame) are keyed by 48 m cell like the toon city's, so the half behind the lens is culled: 1,474 → 992 kT, inside. **The table after this build:** the kit, Weirdport and the test site are inside the budget; the kit city is over in town -- Old Town 589 DC / 1,565 kT, the islands' landing 318 DC, five places over on triangles (1,000-1,500 kT) -- and 170 MB on both textures and geometry; the toon city's spawn is 351 DC. **I'm closing F0a here rather than spending more passes on it before you've seen anything since m304.** What the overs are made of, measured: at Old Town the crowd is 74 bodies drawn, about 100 of the 590 draws and about 800 of the 1,565 kT (there is no low-poly rig, so a body LOD is a Blender job or a decimator); the kit's cell batches and the toon city's per-cell material merges are most of the rest, and the far copies (170 MB of geometry) are full-detail copies, not decimated ones; the toon spawn's 351 is 31 bodies standing within 30 m of it at test-site coordinates (82 draws, 37 of them shadows), the city alone is 264. The budget stays as written (300 / 1,000 / 160 / 128) and `npm run worlds` still exits 1 on it, so the record is honest. The number that decides is the frame time on your phone, which the chip's perf line shows; if Old Town stutters, the next cuts in order are `mel.PERF.bodyFar` (150 m; a body at 150 m is 29 px tall on your screen, at 100 m it's 43), a decimated far copy, and 96 m cells for the toon merges. Say "keep cutting" and F0a-2 reopens.
- **m429 (F0b-1) The headless playthrough, and what its first run found.** `npm run play` boots the real game headless on a fresh save (so it starts at the crash like a new game), steps the shipped frame on its own clock (the browser's animation loop never ticks under the software renderer), and plays Chapter 0 the way a thumb would: the left pad to walk, the shipped blow for a strike from arm's reach, the right pad held still over the farmer for the sample, the checkpoint walked through as the farmer, and Old Town entered. It teleports only when a walk makes no progress for four seconds and says so in the row, and a gate cannot be teleported through (landing outside the span sets no flag). Chapter 0 passes all seven steps in under a minute. **The first run failed on frame one, and that is the real news: the kit city has thrown an error on every single frame since m336** -- the good alien's hat (its antenna tip is a material, and the pulse wrote `.material.emissiveIntensity` on it) -- and because the frame aborts there, nothing after that line ran: no protest, no quests' waypoint, no sun, and no render. On your phone, m336 to m428 of the kit city would have been a black screen under a crash card. The boot gate could not see it (it runs the test site, which has no hats) and nothing else stepped a frame in the real world; `play` does now, so a frame error is a BAD row. Fixed in this build. Two things the rows say that I'm leaving for the polish pass: a new game spawns pressed against the wreck, so the first push forward takes cover on its hull instead of walking (the tool spent two seconds getting off it, and so will a thumb); and the farmer gets up and runs about three seconds after a knock-down, which is a tight window for a first-time sample (the tool needed two more blows). Overrule either if you want them fixed before F1.
- **m430 (F0b-2a) Chapter 1 in the playthrough, and the footbridge's lean fixed.** `npm run play` now plays Chapters 0 and 1 on one save (about four minutes), and `npm run play ch1 --seed=2` plays one chapter on a chosen seed: the random is seeded from before the page boots, so two runs of a seed are the same run and a row that changes between builds is the build's doing. Chapter 1's drivers: walk up and watch the turn, knock the Skinsuit down every time it gets up (a blow on a downed one only punts it; the count is at the get-up), lean on the footbridge as the worker, talk as the crew, the boss and the two turned crew. The shipped picker decides the order, so when the incursion's ship came mid-chapter on one seed the tool fought that quest too and came back. Three seeds pass all four quests. **Two findings.** (1) Fixed: the footbridge's mend counted only while you were pressed INSIDE the barrier's slab (within 0.49 m of its line), and the push-back reset the timer every frame you were not -- seed 1 rested 3 cm outside and saw "Fixing... 1%" for two minutes; a thumb will do the same. Standing anywhere within 1.6 m of the line as the worker counts now (`GATE.lean`, the same number the mend already used). (2) Open: on one unseeded run the player's height became NaN during the fight for Dee and nothing could pass after it; three seeded runs since did not reproduce it, so the tool now fails a step the moment any coordinate stops being a number and prints the eight frames before it. When it recurs, that trace is the bug. Also in the rows, for the polish pass: the boss fight throws you far enough that the tool teleported back four or five times per seed, and the two turned crew are halfway across town when the step to free them begins (130-160 m of walking). Overrule the lean distance if 1.6 m feels like mending from across the street.
- **m433 (STEER: the alien world, part 1 -- load, walk, measure).** `?w=alien` or the world key: his planet loads at one origin, you spawn on the plaza, and nine GOD places (plaza, skyway, coast, summit, sky islands, lift top, fire, goo, crater) are read off his own decks and placements. The sky is his pano, the sun/hemisphere/fog are the README's numbers, and anything under the water puts you back on dry ground (no swimming yet). **Four export problems for your Blender session**, each worked around so the world still loads: (1) 15 town materials and 3 coast ones point at images that were never written into the GLB (the loader used to fail the whole file on them; they draw in flat colour now); (2) the decks for the streets, bridges, stilt village, sky islands and lift top, and their railings, are exported 150 m north of their pictures (measured off the 19 streets and corrected in the game); (3) the coast and kit files have no draco (44 MB of the ~60 MB download); (4) the 24 building GLBs and critters.glb aren't pushed yet. **Performance:** textures 278 → 84 MB by baking all four GLBs and the pano to KTX2; draws at the plaza 3,074 → 1,165 and triangles 2.5M → 1.6M by merging light pieces, a short draw distance for the scatter, and flat far copies of the coast and kit cells. That is still about 4x a phone's budget in town, and the rest is in the export: a flower clump is 7,000 triangles and a fern 6,000 (they want ~500), and there are ~260 materials (they want atlasing). The kit buildings are static here until the next part wires them into the breakable walls.
- **m434 (STEER: the alien world, part 2 -- the buildings).** All 24 building GLBs and the critters arrived mid-build and all 28 placements load (0 missing). Every building and the re-exported coast are baked to KTX2 (about 100 MB of textures each down to about 12). **They are the heaviest thing in the world: 90,000 to 471,000 triangles each** (the spore pharmacy is 471k), several million in all, so from the summit or the sky islands you see about 5 million triangles; a phone wants under 1 million. They want decimating to about 30-50k each in Blender. Until then they have a 150 m draw distance inside the fog (they pop), and the GOD menu has an **ALIEN BUILDINGS ON/OFF** switch (also `?bld=0`) in case they crash the tab: with them it's about 700 MB of textures and geometry, without them about 230 MB. Also fixed for every world: a fast fall could tunnel past the ground and land on a surface underneath (you walked under the plaza's terrain and fell out of the world); falls now look for ground from where they started the frame. Overrule the 150 m.
- **m438 (STEER: Glowtide, Level 1 -- part 1, load and walk).** `?w=plaza`, or tap the world key until it says GLOWTIDE. You spawn on the stage facing north, and every one of the level's 96 markers is in the GOD menu's "here" list (cores, glyphs, bells, generators, triggers, movers, enemies, NPCs, pickups, the portal). It measures well inside a phone's budget: 22-42 draw calls and 106,000 triangles anywhere in the level, 45 MB of textures (the plaza's own images baked to KTX2). **One thing for the Blender side:** `PL_static` and 7 other render meshes carry `collider: "ground_"` in their extras, which made the game drop the whole visible plaza as a hidden collider; the game ignores that tag on the plaza's visual file now, but it shouldn't be written on render meshes. The level's objects (shutter, bells, generators, fuel cell, sluice, slab, vault door, waterfall, canal water) are loaded separately for the next builds: the events, the Hover Pack, the launcher, the ziplines and the waves, one build each.
- **m464 (his chat): wall cover OFF by default** (GOD > WALL COVER brings it back), and **the ledge grab only catches with the
  thumb pushed at the edge** (`LEDGE.want` .35; 0 is the old catch). **Next pass builds his progression ask ahead of F0b-2b**:
  a new game starts UNARMED and with no board, pack or DNA mode; each is FOUND in the story (a `SAVE.kit` list, the weapon wheel
  showing only what he has, GOD > ALL KIT for testing). Clancy rescued in the sequence rather than following from the start.
  Order of discovery is my first guess and is written into the quest table where he can move it.
- **m465: the found kit.** A new campaign game is bare hands. Order (one id each in `GEAR.get`, move freely): HAMMER for freeing
  Dee (ch1), BLASTER at the end of Chapter 1 (Briggs), SKATEBOARD at The Pearl's end (ch2c), HOVER PACK at Hollow Creek's end
  (ch3c), LAUNCHER at the Waterfront's end (ch4c). Clancy stays "found at the wreck" in ch0's first step. GOD > ALL KIT gives
  everything. The new technologies (psychic, mind control, telekinesis, phasers) are not built; each will be a slot plus a
  `GEAR.get` line.
- **m468: the playthrough harness starts a later chapter as a player would arrive there** -- the earlier chapters' forms
  (farmer, worker) and their quests marked done, so the found kit is in his hands. Without it, Chapter 2's barista ran from a
  bare alien for two minutes, which no player would ever see.
- **m470: the rally is called within 15 s when Chapter 3 is waiting on the speech** and you are within 60 m of the stage (it ran
  110-170 s quiet + 34 s build otherwise: up to 3.5 minutes stood at an empty stage). **The start hill's back is a ramp now**,
  not stairs: lap 2 rides up it and jumps off the front (the stairs were a wall to the bike). Rae's speed is unchanged (15).
- **m471: the speech balloon.** Comic Neue for the words (GOD > TALK FONT cycles comic / hand (Patrick Hand) / plain), Bangers for
  the name, a fat outline with an ink drop-shadow and a two-triangle tail that follows the speaker. Lettered in at 14 words a
  second (`TALK.wps`; 0 = all at once); the first tap finishes the line, the next advances.
- **m471: the detail pass (T2) goes to a scenery window, yes.** The level window already started it (m469, the crash wreck as a
  GLB in `models/campaign/`). It owns the ART there (headless Blender, GLBs pushed); this loop owns the CODE that loads and wires
  it (T2a, colliders, behaviour) and takes T2's code-side items itself (the roadblock that actually blocks). Neither edits the
  other's files.
- **m474: his wreck is loaded BEFORE `buildCrash` and the code-built hull is its fallback** (a failed load is the old wreck, not an
  empty field; `?wreck=0` is the A/B). His `scorch` mesh and the code's scorch discs both draw for now (the README keeps the
  code's); if they fight, the code's go. The core's glow pulse is scaled to his own emissive strength rather than overwritten.
- **m476: his pickup and tractor are merged per material at load** (44 / 36 meshes -> 10 / 7 draws) and made single-sided but the
  glass (every material came `doubleSided`). The boxes are the fallback; `?vehglb=0` is the A/B.
- **m477: the bridge checkpoint was never jumped OVER -- it was walked ROUND.** The line was the deck's 5 m and `GATE.hi` (4 m) is
  above his 2.8 m jump; up on the 0.9 m parapet and down onto the levee took him past its end. It now BLOCKS 7 m past each side
  of the deck (`BRIDGE.gateLevee`; drawn the deck's width). So no "jump it on purpose" trick and no cops' reaction to one: the
  line holds, which is the simpler reading of "the roadblock must actually block". Say if you want the hop as a feature.
- **m477: cordons and checkpoints leave a 1.8 m gap in the middle** (`RBK.gap`), where the right body is waved through; a
  sawhorse line right across the road would be walked through by every disguise it lets pass. Barricades are solid jersey
  lines. **Only the police car and the work light are solid colliders** -- a solid line would stop the bodies it must let
  through; the gate logic stops the wrong one. The car parks only on lines wider than 5 m (`RBK.carW`), so not on the bridge.
- **m478: the farm's bushes are scattered beside the hedges (22% of pieces) and the fences (7%)** -- 104 of them; not yet by the
  farmhouse or at field corners (the next pass on the farm can add spots there). Every hedge piece and bush is an INSTANCE
  (`FBK`): 482 copies in 11 draws. `?bush=0` is the code-built mounds.
- **m479: T2's four named pieces are done** (roadblock m477, truck m476, bushes m478, crash m474); its "onward, place by place" waits
  on the scenery window's next files, so the loop is back on Phase F until a new `models/campaign/` piece lands.
- **m483: the SKATEBOARD now follows the surface like her skates** (`bladeSurfPre/Post`, `BLADE.surf`'s numbers): a kicker throws
  him up at its own angle instead of rolling him off level. Every ramp and lip the board meets changes, the farm's and the
  test site's included. The bike is left as it was (the race was tuned without it).
- **m484: the islands' gap landing starts 10 m past the lip, not 13** (`IBASE.landAt`), and "cleared" means landing on it. The
  in-run's real top speed is ~16 m/s; at that the old landing's front edge was 0.6 m above where he came down.
- **m486: the playthrough puts him ONTO the tether's pod** (a teleport, said in the row) rather than flying the thermal up to it --
  the flight is the one piece of Chapter 6 the harness does not do with a thumb's inputs. Everything after is walked, ridden
  and fought. **The whole campaign now plays through headless**, Chapter 0 to the end, a chapter per `npm run play chN`.
- **m487: the alien world's `GLB NO IMG 20` stays RED.** It is a fact about his export (20 texture slots with no image), the alien
  world is the other window's, and the note is how that reaches him -- quieting it would hide the data, not fix it. Every other
  world boots with nothing in the red list. The old toon city's island grass is white by construction (it has no grass
  material); that is said in the console now, not in red.
- **m488: F1's shots are taken because the item says `npm run shot`** (the loop's "no screenshots unless asked" yields to an item
  that names the tool). One worst-thing per build, region by region, as written.
- **m512 (F2a-1) The Underneath is reached by HATCHES, not stairs.** The city's floor (`gFloor0`) is one surface with no hole in
  it, so a stair down would end in solid ground. A hatch is a pad: step on it and you are at the other end (the camera
  moves with you, as a portal's does), with a short toast. If you would rather it were a real stair, the floor needs a
  cut-out first -- say so. **And `groundAt` now ignores the island floor INSIDE the Underneath's box only** (it ignored
  height before, so nothing under the ground could be stood on); nothing above ground sees a change.
- **m526 (F2a-5) The collapse under the city is cleared by the CONSTRUCTION WORKER**, standing in for the cave miner, who has
  no model yet. When a miner GLB exists, `GATE_TYPES.undercollapse.need` is the one line to change. The miner's "sees in the
  dark" is not built either -- the tunnels are lit enough to play.
- **m528 (F2b-1) Dump Tower stands on the WEST edge, off the city's ray at 180 deg, 20 x 20 m, 4.2 m floors, a switchback stair rather than lifts for now.** The stair keeps every floor reachable before F2b-2's badge lifts exist; when they land the stair can be locked above the lobby band. `DTOWER.deg` moves it.
- **m530 (F2b-2) Dump Tower's lift is ONE cab with two stops per ride, not a floor picker.** From the lobby it takes you as high as your badges reach (staff -> floor 7, executive -> the boardroom, CEO -> the penthouse); from any other floor it takes you down to the lobby. The stair stays open up to floor 7; the boardroom and the penthouse are behind glass SECURITY VESTIBULES over the stair's head that open to that band's badge. Until F2b-3 gives the badges to people, they lie where their owners left them: the lobby desk, a gym bench, the boardroom table.
- **m532 (F2b-3) The corporate ladder is a RANK: the best of your badges and the face you wear.** A suit (`fat_secret_service`, sampled off a lobby guard with the DNA gun) passes for staff -- the lift runs and the receptionist, the VP and every suit in the tower talk to you; the receptionist then hands you a staff badge and the VP an executive's. The CEO's assistant hands over the CEO's badge only to Mr. Dump's own face (`fat_trump`), and the CEO's face opens everything by itself. The badges lying on the desk, the bench and the table stay as the thief's way. `fat_secret_service` and `fat_trump` are now the social group 'suit' everywhere (they were 'folk').
- **m534 (F2b-4) The aerial tram runs from a station on the grass BEHIND the tower to the sky garden**, not from the hill REGIONS names: there is no hill in the kit city to stand on (the 'hill' is a skyline backdrop). It is the way in that skips the lobby's guards -- the sky garden is below the executive band, so it gets you to floors 0-7 by the stair without a badge. The glider out is Vee, a courier pilot on the helipad: wear her (the DNA gun) and jump.
- **m535 (F2b-5a) Mr. Dump is fought in the PENTHOUSE, not the boardroom** -- he lives there and the CEO's badge is what opens it, so the last door is the climax. The Mothership's quests keep their ids (`ch6`, `ch6b`, `ch6c`) and only their `ch` moved to 7, so a save that finished the game still reads `qdone:ch6c`; the tower's quests are `tower` / `towerb`.
- **m538 (F2b-5b) The seventh lock (THE BOARD DOOR, a suit's) is between the rumble door and the neural lock, not after the lock**, and the file's hall has a SAC that fills your juice tank as you walk through: seven locks is seven forms at 20 juice each, more than a 100 tank. Chapter 6 now has a step that takes a lobby guard's sample, so every player reaching the ship has the suit's face.
- **m539 (T2m) A side -1 trailer is MIRRORED in x, not turned by pi** as T2m said: turned, its door (Blender Y -1) lands at v + len*.1, away from the porch, awning and steps the code builds at v - len*.1. Mirrored, the door stays where they are.
- **m542 (T2o) Containers whose doors face +v are TURNED by pi, never mirrored** -- a negative scale inside an InstancedMesh's matrix flips that instance's winding and the box draws inside out.
- **m543 (F2c-1) The Gorge is its OWN landmass past the River Islands (+z, centre ~(0, 560))**, not a cut through Hollow Creek's land: Hollow Creek already has its gorge (the trailer park, the mill's flume), and between the creek and the islands there is only ~45 m of water. Its falls drop straight into the sea, so the fjord below them is the sea's own water.
- **m551 (F2c-2) The way into the cave behind the falls is DOWN a chimney from the upper river**, not along a ledge from the fjord: the fjord is sea water 28 m down between sheer walls and there is no swimming yet. The diver's underwater way in is F2c-5. No falls sound: there is no water recording in the repo.
- **m556 (T2u) The shut cart keeps its awning up** for now: the awning is part of `fc_cart_paint`, so it cannot be hidden on its own. A separate `fc_cart_awning` root in `food_cart.glb` would let the shut cart drop it (one line in `buildCarts`).
- **m567 (T2z) Each turret's control panel turns its screen AWAY from its own gun**, since nothing in `WTUR` says where the walkway is: you hack it from the side the gun is not on.
- **m576 (F2c-4) The dam starts SHUT** -- the falls a trickle, as the fishers say ("upriver they've dammed it since spring") -- and opening it is the player's, by the grate beside the wheel on its crest. The cave behind the falls stays reached by its chimney either way; the dam changes the falls, the river below it and the spray, not a door.
- **m584 (F2c-5a) Swimming is the DIVER's alone**, a role form (`ROLEFORM.diver`, sampled off Nell with the DNA gun): anybody else in the sea is still put back on the shore. The controls are the hover's -- hold the right pad (or space) to rise, let go to sink -- and at the surface the hold is one kick out of the water, high enough for a 1.6 m ledge.
- **m594 (F2c-5b): the underwater places are DOWNSTREAM of the stilt village, not under it.** Each village house stands on posts
  2-7 m off the river's line, so a hollow anywhere along the walk would have had posts plunging into it. The grotto is at b -57
  and the wreck at b -69, past the walk's last stilt (-48); `gzdeep` is the walk's end, looking at them. The fjord itself stays
  2.3 m deep. Deepening it would widen the canyon at the walkway and leave the stilts short of the wall.
- **m594: the swim pose is a LEAN, not a clip.** The diver has no swim clip, so the whole body tips forward about the hips, up
  to 1.25 rad (`SWIM.pose`) at speed, and plays its run clip at about half speed as the stroke. Still, it treads water upright
  in its idle. `mel.SWIM.pose = 0` turns the lean off.
- **m609 (F2c-6a): F2c-6 is split in two.** 6a is the lookout, the glider and the map region; 6b is the flume and the rapids
  from Hollow Creek. The lookout stands on the east plateau at the fjord's mouth (b -56), with its deck 14 m over the ground,
  about 19 m above the sea before the tower. The nearest islands (lighthouse rock, the humps) are about 120-145 m off, the same
  glide ratio as Skye's 120 m from 15.8 m. If the glide falls short, raise `H` in `buildGorgeLook`.
- **m615 (F2c-6b): the long flume ends at the stilt village, not on the upper river.** The Gorge's upper river is 13 m up a
  canyon, higher than Hollow Creek's shore, so a flume can't run DOWN into it. The flume runs from a tower on Hollow Creek's
  shore nearest the Gorge (head about 17.5 m up) down across the strait to the fjord's mouth. The "rapids" are the long low run
  up the fjord over the water, past the wreck and the grotto, onto the east walk's downstream end. Its current carries him at
  8 m/s (`GFLUME.speed`). This closes F2c; the mill's own flume is unchanged.
- **m633 (F2d-1): the Hothouse is not its own landmass. It is any Old Town turf block the Skinsuits (`skin`) hold**, overgrown
  in place. REGIONS calls it "familiar streets overgrown", "the city underneath" and "the growth spreads", and the turf system
  already moves blocks between factions. So it grows and shrinks with that, with no second map. A bigger standalone jungle
  district can still come later as part of F2e's hub.
- **m642 (F2d-2): the Hothouse is cut back with the blaster only for now.** A bolt landing in a grown block takes .05 x
  (.5 + charge) of the Skinsuits' share there. Swinging at it is not wired yet, because the melee strike has no
  "where did it land" point to hand over. It spreads every 40 s into one of a held block's four neighbours, by .1 share, and
  stops at 18 of the 36 blocks so it can't eat all of Old Town while nobody plays. Inside a grown block the fog goes teal and
  the sun drops to half. `mel.HOTH` has `every`, `push`, `cap`, `cut`, `twFog` and `twDim` to tune it.
- **m648 (F2d-3): the Hothouse's heart is the block NEAREST the Skinsuits' own that has three roofs or more.** Their native
  block, B3 (the watcher's pool), is open street, so the heart landed on A4. It is grown for good, whoever holds the block:
  the vine bridges, the ladder and the nursery stay put. Only the jungle overlay comes and goes with the turf.
- **m680 (F2d-4b), the spore pod:** it docks BESIDE the tether's own pod, at the same height as its top, rather than carrying you into
  the ship. One step across and the existing tether ride takes over, so there is one way into the ship and not two. The pod is
  rider-triggered (stand on it ~1 s), not on a timer: the ride is long (about a kilometre at up to 26 m/s). Left at the tether and
  walked away from (120 m), it drifts home empty, so the nursery is never missing its pod for good.
- **m683 (T4z), the quay fenders:** each fender's centre is put where the code's rubber box was centred (v - .18, hanging off the
  face), not at v + .18 as the item says. At + .18 the 0.36 m-deep fender would sit inside the quay wall. They are instanced with
  no mirror, so each one's water face is turned outward by its yaw instead.
- **m684 (F2d-5), the cure:** it is a side quest (`qcure`, THE CURE) from Fern, a gardener at the foot of the heart's vine ladder,
  not a numbered chapter. The chapter order already runs the Tower and then the Mothership, so this hangs between them. Bursting
  the mother pod (one bolt into her) takes .45 of the Skinsuits' share off every block that has any, which flips most held blocks
  back, and it stops the spread for good. Blocks they still hold stay held until you cut them back. Melee still doesn't cut the
  growth; only bolts do.
- **m689 (F2e-1): the metropolis's core is built round Dump Tower on the island's west ring, not as a new landmass.** REGIONS
  puts Dump Tower in the hub and has Old Town as its first district. So the hub grows outward from what is already there: Old
  Town's blocks plus a tall cluster round the tower. It is packed, not tabled: towers take the nearest free dry ground with a
  5 m street between them. All of them share one terrace level at Dump Tower's sky-garden floor, which is what the sky-bridges
  join. The distant SKYLINE scenery still stands for now (F2e-5).
- **m700 (F2e-4), the grip on the core:** the "streets fenced" part is a translucent magenta membrane across each crossing, with no
  collider. A blocking fence would close off the cradles, the bridges and the fire escape before Chapter 1 has even sent you here.
  The towers are freed in even steps across chapters 1-6 (SAVE.ch 2..7), the farthest from Dump Tower first. All of them are freed
  once Dump Tower falls.
- **m702 (F2e-5): the skyline stays, re-aimed through the real core.** From the farm, the walkable towers round Dump Tower stand
  in front of the scenery, which now reads as the rest of the metropolis behind them (the Pearl's towers, the hill and mast, the
  waterfront strip). The skyline's own 640 m Dump Tower and its Old Town are no longer drawn, because the real ones are right
  there. It falls back to the old aim if the core did not build.
- **m705 (F3-1), the projector's roadblock:** it stands across Dump Tower's plaza approach (13 m out from the tower's front, about
  26 m wide) and is SOLID. That is the lore's "opening the way", but it is a soft block: you can walk round it on the grass. It is
  not a quest gate: Chapter 6's "To Dump Tower" step still passes at the plaza. It is a dormant task (A ROADBLOCK THAT FLICKERS)
  that wakes when you first see it.
- **m708 (F3-2), the poltergeist:** it haunts the kit building nearest Old Town's north-west (-40, 42). It throws a piece of junk
  every 2-4 s while you are within 28 m: 8 damage and a shove if one reaches you. Nothing is thrown while you are flying. "Animals
  react first" is not built: there is no dog in the game, and the farm's cows are far away. Its tells are the stuttering light at
  the building's foot, the door slams and the throws.
- **m711 (F3-3), the relay:** "they take half damage" became "every other hit on them does nothing" (they spark blue: THE RELAY
  FEEDS IT). "They re-light if downed" is NOT built: a downed orb is saved as down, and bringing it back would undo progress you
  have made. Shooting the relay down takes one hit off every orb still up (never their last hit).
- **m717 (F3-4), the EM tell:** the flicker acts on his own lit materials (any emissive material named lit/lamp/neon/light/glow/bulb),
  across the whole scene at once, while you are near an orb. No point light is added: m158 rules streetlights out as lights. Cars
  stall wherever there are cars: the farm's vehicles, and the Weirdport slice's traffic if it reads `emSlow` later. Old Town itself
  has no moving traffic to stall. The radio hiss is static in the air. The radio show's own voice is not touched.
- **m720 (F3-5), the Hum:** it is synthesised (two detuned low saws and a sine through a low-pass) rather than a recording, because
  the repo has no drone sample. Its "district" is Old Town, which is where every orb is: its level is the share of orbs still up,
  full inside Old Town and fading out over 160 m. The EM tell and the Hothouse add to it. Other districts get their own grid when
  they get orbs.
- **m721 (F3-6a), the triangle has no night:** the game has no day/night cycle (the city is a fixed neon dusk), so the black triangle
  patrols all the time. It circles 80 m up, out of the blaster's reach, and only its seekers can be shot (two hits each). A seeker
  that holds its light on you, as yourself, starts an incursion: the watcher's own call.
- **m724 (F3-6b), the tic-tacs:** they come for anything gliding on the wing (`player.wing`), anywhere on the campaign map, after 3 s in
  the air. GOD's free-fly does not count. A hit is 7 damage and a hard shove; it does not fold your wings. Landing and staying
  down 4 s sends them away. Each one is two hits, and the first one you shoot down sets `tictac:down`: the hook for the tic-tac
  pilot's side quest.
- **m726 (F3-7), what happens at zero health:** zero health IS being taken, so it plays as missing time. The screen whites out and
  you wake at the camp, the trailer park or the farmhouse (the nearest of them more than 60 m from where you fell), health full,
  juice cut to a quarter of the tank, and a card with the minutes you lost. `mel.MTIME.on = 0` restores the old behaviour, where
  nothing happens and it regenerates. There is no separate tractor-beam capture yet: every way of being taken goes through
  health.
- **m731 (F4-1), the hobo's stealth:** "guards" are read as Uplift's machines: the yard turrets and the patrol robots. The police
  already only react to the alien, so any human form passes them. A hobo is not SEEN by the turrets or robots. He cannot stand
  them down or take a turret over (that is still the engineer's), and once the yard's alarm is up, he is seen like anyone else.
  F4 is split into F4-1..5. The CEO and the diver are already built (Dump Tower's badges, the Gorge).
- **m733 (F4-2), the cop's arrest:** it is the cuffing only. The "cop's car to drive off" half is not built: no car in the game is
  drivable yet (CLAUDE.md: "The cars are not drivable"), and that is its own build. An arrest takes .08 of the Skinsuits' share off
  the block the body lay in, and the count is saved as `arrests`, the hook for anything that wants to reward it.
- **m735 (F4-3), the fire engine:** the "burning building" is smoke rolling off the roof, not live fire: the fire system's flames
  belong to the decay/fire chapters, and a permanent blaze in Old Town would spread through them. The ladder raises straight up
  the wall from the street, beside the truck's tail, rather than swinging out at an angle, because a climb in this game is
  vertical. Once raised it stays up (saved).
- **m738 (F4-4), the miner:** his door is a new unlit tunnel east off the Underneath's second shaft to an abandoned dig, half-way
  blocked by a roof fall that only the miner clears (lean on it with the pick, the gate system's `fix`). The dig's strongbox
  refills the tank. The miner's head lamp is one point light that is on only inside that tunnel, and only in his form. Old Seam,
  the miner to sample, sits in the second shaft room.
- **m740 (F4-5a): soldiers are the four-star EXTRAS only**; the cops already on the beat stay cops. A soldier reaches 1.5x as far, hits
  1.35x as often (capped at .95) and fires 1.5x as often. Until F4-5b, sampling a soldier gives you the cop's form. `mel.COPS.sol = 0`
  turns them back into cops.
- **m743 (F4-5b): the SOLDIER's group is `law`**, the same as a cop's, so the police talk to him as one of theirs and a police
  cordon waves him through (`soldierToo`). The base itself is split out as F4-5c, to be built as one finished place at Hollow
  Creek's far edge rather than squeezed into this build.
- **m745 (F4-5c): Camp Hollis sits on a new flat at Hollow Creek (-40, 88)**, the far shoulder between the fairground's hill
  and the saddle, with its gate facing the fairground. Its two gate sentries ARE soldiers, so you get the form from them by
  knocking one down at the gate, which means a fight with heat on the doorstep. Trying the gate in any other form adds .8 heat
  each time it speaks. The prize in the supply cage is a full tank of juice plus the base's radio codes, which wipe your heat,
  and a manifest that points at Area 15. No road reaches it yet; a road sign by the gate points out to "AREA 15 40".
- **m750 (F5-1a): Saucer Joe's sits on a new flat at Hollow Creek (-88, -100), just west of the highway** where it comes off the
  bridge. That puts it inside the gang's turf, so you reach it as a local, a biker, or off the freight. Joe talks to the alien
  (he knows what his saucer is). The saucer only reacts to the alien form, not to a disguise.
- **m756 (F5-1b): each of the saucer's parts sits behind a form**: the coil on Camp Hollis' watchtower needs the SOLDIER to get
  in, the lens by the old dig's strongbox needs the MINER (who clears the roof fall and carries the lamp), and the gyro on Uplift's
  outfeed tower is reachable from the quay by anyone. The parts can be picked up before Joe gives the quest, and a part found early
  counts.
- **m761 (F5-1c): the fixed saucer's hop goes from Joe's yard to the top of Hollow Creek's hill and back.** You stand on her a
  moment and she flies; she stays where she landed. The diner's portal pad (in the lot) is lit the moment she is fixed, with no visit
  needed. Once fixed, she glows whatever form you are in, and the neon stops stuttering.
- **m765 (F5-2a): Merle's bunker sits on a new flat on Hollow Creek's hill shoulder (130, 50)**, about 43 m from the hilltop
  where the saucer lands. Its back is to the hill, and it is ringed by the pines. Merle is a new roster role, `prepper` (the hobo
  stem, a crumpled foil hat), and he talks to the alien. The container is ON the ground with dirt heaped over it rather than sunk
  into it, because the terrain is a floor the player cannot go below.
- **m770 (F5-2b): Merle's evidence only counts after he has asked.** The shard lies where the pacifier orb fell. The hum records
  wherever it is loud, and also under the black triangle, so a city with every orb already down can still finish the quest. The
  photo needs you within 45 m of the triangle for 1.5 s. The grid goes on the FULL map only (the minimap stays clean): orbs are red
  while they stand and grey once down, and lines join every pair within 140 m plus every orb to the relay.
- **m778 (F5-3a): the twelve dossiers sit ON twelve of GOD's places** (the helipad, the control room, the roof garden, the
  lookout, the Underneath junction, the mesa, crane 1's boom, the hilltop, the cave behind the falls, the farmhouse porch, the
  core, Mags's newsstand). Those spots are known to be standable, and between them they cover every region and several climbs.
  The quest has no giver: it switches on with the first file found, and its beam points at the nearest file left.
- **m783 (F5-3b): the Dozen's room is a walled-off corner of the boardroom floor (8)**, its south-east, behind dark panelling,
  not the penthouse. A door with no handle slides aside only once you hold all twelve files. The twelfth chair's occupant is a
  Skinsuit, which talks to any form (it knows what you are), and talking to it finishes the quest. I did not use
  `models/alien_lizard.glb`: it is not wired anywhere yet, and its rig and clips are unmeasured. It is the obvious thing to put in
  that chair once it is.
- **m785 (STEER, hero select): the pick lives on the START SCREEN** (a HERO row at the top: ZAP / ALIEN LIZARD), is saved in
  localStorage, and `?hero=lizard` / `?hero=zap` overrides it for a link. The world key reopens the start screen, so that is how
  you switch on the phone. The lizard file stays where you put it (`models/alien_lizard.glb`) and loads as-is: not draco, no KTX2
  twin, and `doubleSided` left on for the test. The chip reads `HERO <pick> <bound>/<asked>`, then `NO <names>` for any clip the
  game asks for by name that did not bind, then `TRK<n>/<total> unbound` for any of the file's tracks whose bone is not in the
  model. Measured offline before the build: the lizard has every clip zap has except `CINEMA_4D_Main` (dropped anyway). Zap's
  clips animate 17 bones the lizard has not got (finger tips 1-4, toe ends, head top). Those only matter for zap's clips on the
  lizard; the lizard's own tracks should all bind.
- **m793 (F5-4a): the "disaster" is a glowing pod Mothman hangs over, and the cost of being late is a building fire** (`fireStart`)
  plus a dent in that district's health. The game has no way for the player to put a fire OUT yet: `fireDouse` exists but nothing
  wires it to the firefighter. So the save is getting there in time and standing on the pod, not fighting the fire. His
  sites are five of Old Town's GOD places in turn: the square, the Hothouse, Mags's newsstand, the foot of the lookout and the
  radio payphone. The 75 s fuse starts when he takes off.
- **m794 (STEER bug 1, the lizard's guns): the weapon fit is MEASURED in `mountWeapon`.** It takes scale |wearer tip| / |weapon tip|
  and the rotation from the weapon's tip axis onto the wearer's. Read from the files: zap's pair is (-14.3102, 0, 0) and so is
  every weapon's, so zap comes out at exactly 1.00 and identity, with nothing changed for him. The lizard's is (-0.140, 0, -0.072),
  so his guns come out at .011 scale, turned 27 degrees onto his axis. The chip says `WSC1.00` on zap and `WSC.011` on the lizard.
  The muzzle is measured in the file's own frame and then carried through the fit, so shots leave the barrel. Bug 2 (the flip) is
  the next build.
- **m796 (STEER bug 2, the flip stutter): it was the LIZARD's clips, not the code path, and zap does not do it.** His
  retargeted `front_flip` and `backflip` carry no vertical hip motion: 0.00 at every key, where zap's hips arc 29 -> 59 -> 29 cm.
  `flipMarks` was measuring the flip's timing off float noise, so the flip clock ran out partway through the rotation. Flat hips now
  fall back to the clip's own length: airborne for .81 of it, which is zap's own measured ratio, with no wind-up. The whole turn
  plays, but the lizard still has no body lift in the flip (his clips have none). **That is a retarget gap for his pipeline:
  root/hips translation is being dropped.** On zap nothing changes, because his marks measure clean. The chip shows
  `FLIPfwd<left> t<time>/<len> w<weight>`, plus `FLAT` when the fallback is in use.
