# (helpers from farm_outbuildings.py) -- the farm's three small buildings as art, at their builders' exact numbers (the code keeps every collider).
# CONTRACT: one root each, Blender X = the frame's u, Blender +Y = the frame's +v, origin on the ground at the centre given.
#   fo_shed     buildFarmhouse's tool shed: origin (su, sv) at g. Slab 4.6 x 3.6 (g-.2..g+.25), walls from g+.25, back (+Y) 2.6 high,
#               front (-Y) 2.1 with the doorway at u -.4..+.8, pent roof 5.0 wide rising to the back
#   fo_coop     the chicken coop: origin (cu, cv) at g. Hut 2.3 x 1.7 from .6 to 1.85 on four legs at (+-1, +-.7), pitched roof,
#               the ramp down the -X end. The run (posts and wire) stays code.
#   fo_haybarn  the lone Dutch hay barn: origin at its centre at g. L 18 along X, posts every 4.5 at Y +-4.5, eaves 5.6, roof the
#               top arc of R 6.5 (+-.9 rad), L+1.4 long. The hay stays code.
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection; rnd = random.Random(21)
def mat(name, rgb, rough=.85, metal=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal; return m
SHED = mat("FO_shed", (.4, .46, .42)); SHED2 = mat("FO_shed_lap", (.33, .38, .35)); TRIM = mat("FO_trim", (.9, .87, .8)); ROOF = mat("FO_tin", (.55, .58, .6), .5, .35)
RUST = mat("FO_rust", (.5, .27, .14), .8); WOOD = mat("FO_wood", (.45, .31, .19)); WOOD2 = mat("FO_wood_old", (.58, .52, .42), .95); DARK = mat("FO_dark", (.1, .09, .08))
COOP = mat("FO_coop", (.78, .68, .45)); RED = mat("FO_red", (.62, .16, .12)); STONE = mat("FO_stone", (.53, .51, .47), 1); STEEL = mat("FO_steel", (.36, .4, .43), .5, .45)
STRAW = mat("FO_straw", (.85, .7, .35), 1)
cur = None; groups = {}
def put(o): groups[cur].append(o); return o
def box(x0, y0, z0, x1, y1, z1, m, bev=0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co = Vector(((v.co.x + .5)*(x1 - x0) + x0, (v.co.y + .5)*(y1 - y0) + y0, (v.co.z + .5)*(z1 - z0) + z0))
    if bev: bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bev, segments=1, affect='EDGES')
    me = bpy.data.meshes.new("b"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("b", me); col.objects.link(o); me.materials.append(m); return put(o)
def quadbox(pts, th, m):
    """a slab from 4 corner points (counter-clockwise from above) pushed `th` along +Z -- roofs built from points, never rotated"""
    vs = [Vector(p) for p in pts] + [Vector(p) + Vector((0, 0, th)) for p in pts]
    f = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new("q"); me.from_pydata([tuple(v) for v in vs], [], f); me.validate(); o = bpy.data.objects.new("q", me); col.objects.link(o); me.materials.append(m); return put(o)
def cylz(x, y, z0, z1, r, m, seg=10):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    me = bpy.data.meshes.new("c"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("c", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation((x, y, (z0 + z1)/2))); return put(o)

# (fair_kit.py header kept for its helpers) -- Hollow Creek's fairground pieces as art, at buildFairground's numbers (the code keeps every collider, the
# painted canvas signs, the bunting, the stage and the grandstand). Blender X = the fair frame's u, Blender +Y = its +v.
#   ff_wheel_frame  origin (W.u, W.v) on y: A-frames at v +-1.3 from feet at u +-3.2 up to the hub at r+1.6 = 9.6; the red
#                   loading booth 1.6 x 3.4 x 2.5. Does NOT turn.
#   ff_wheel_rotor  origin AT THE HUB, built in Blender XZ (the wheel's plane), axle along Blender Y: twin rims r 8 at Y +-.6,
#                   16 spokes, bulbs. In three this is the `wheel` group's own frame (plane XY, axle z) -- it replaces the torus
#                   rings and spokes and spins about z exactly as now.
#   ff_wheel_car    ONE gondola, origin at its CENTRE (where the code's 1.2 x 1.1 x 1.4 box is), its hanger rising to +.7 (the
#                   rim point). Eight copies, kept level by fairStep as now.
#   ff_stall_red / ff_stall_blue  one midway stall each, origin (u -19, St.v) on y; counter, booth, striped canopy, poles
#                   (the SIGN stays the code's canvas plane at u+.55, 3.3)
#   ff_livebarn     origin (bu 16, bv 22) on y: the barn whose box is at u +3 (6 x 8, eaves 4.5), a gambrel roof over it, its
#                   door on the -X face; the pens stay code
#   ff_gate         origin (0, gv 25) on y: posts at u +-5 to 6, the beam, an arch of bulbs behind the code's sign, the
#                   ticket booth at (7.5, -1)
WHITE = mat("FF_white", (.93, .9, .84), .5, .3); REDP = mat("FF_red", (.72, .2, .16), .6); BLUEP = mat("FF_blue", (.18, .29, .54), .6)
RED2 = mat("FF_red2", (.62, .17, .13), .7); YEL = mat("FF_yellow", (.9, .68, .14), .6); BULB = mat("FF_bulb", (.95, .85, .6), .3); _b = BULB.node_tree.nodes["Principled BSDF"]; _b.inputs["Emission Color"].default_value = (1, .85, .5, 1); _b.inputs["Emission Strength"].default_value = 2.0
def bar(p, q, r, m):
    """a square beam from point p to point q, half-width r (built from points, no rotations)"""
    p, q = Vector(p), Vector(q); d = (q - p).normalized(); a = d.cross(Vector((0, 0, 1))) if abs(d.z) < .95 else d.cross(Vector((1, 0, 0))); a.normalize(); b = d.cross(a)
    vs = [p + (a*sx + b*sy)*r for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]; vs += [v + (q - p) for v in vs]
    fs = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new("bar"); me.from_pydata([tuple(v) for v in vs], [], fs); me.validate(); o = bpy.data.objects.new("bar", me); col.objects.link(o); me.materials.append(m); return put(o)
def ball(c, r, m, seg=8):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg//2), radius=r)
    me = bpy.data.meshes.new("ball"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("ball", me); col.objects.link(o); me.materials.append(m); me.transform(Matrix.Translation(c))
    for p in me.polygons: p.use_smooth = True
    return put(o)
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)















# old_car.py -- the broken-down car on the road bridge into Hollow Creek (and a plain one for anywhere), at buildBridge's m511
# numbers (the code keeps the collider: 1.8 x 4.2 from .3 to 1.0). Origin at the car's centre on the road; Blender X across (1.8),
# +Y its FRONT (the code raises the hood at v + 1.85), the body .3..1.0, the cabin 1.6 x 2.0 at Y -.3 up to 1.5, wheels at
# (+-.8, +-1.4), r .33.
#   oc_car_broken   hood up, the engine bay showing, a flat front tyre, steam, a warning triangle 3 m ahead, rust
#   oc_car          the same car, hood shut, all four tyres up -- for parking anywhere
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)














# dock_props.py -- the waterside furniture that repeats along the Pearl's piers (and the Waterfront, the ferry landing, the halt):
# one kit, each piece on its own ground centre, so every call site that draws one of these as a cylinder and a sphere can draw this.
#   dp_bollard   a cast-iron mushroom bollard, .55 high (the Pearl's collider is .36 sq x .55), r ~.2, its cap's lip
#   dp_rope      a rope coil, ~.32 r, flat on the ground, a tail running off it (the Pearl puts it at (+.15, +.2) off a bollard)
#   dp_lamp      a harbour lamp post to 4.55: the pole, a lantern head with its glass at 4.3 (the Pearl's lamp point), a cap
#   dp_ring      a life ring on its own little post, the ring's centre at .62, the ring in the Blender XZ plane (facing +-Y)
#   dp_pot       a lobster pot, .7 x .45 x .4 (the Pearl's open cylinders)
#   dp_crate     a fish crate, .8 x .7 x .45, slatted, stackable
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)













# rue_field.py -- Rue's field on the River Islands as art, at buildIslandThermal's m504 numbers (the code keeps the rings, the stepping
# stones, the flowers, the table's collider and the bench's). Blender X = the islands' frame u, +Y = its v; origins on the ground.
#   rf_canopy   at (-11, 11): legs at (+-1.6, +-1.4) to 2.5, the canvas roof 3.6 x 3.2 peaked over 2.5, a scalloped valance on -Y; the
#               folding table 1.8 x .8 at (0, +.4), .72 high, with a thermos, a cup, a clipboard, a wind sock on a pole
#   rf_rack     at (-14.5, 5): posts at Y +-1.4 to 1.8, the beam along Y at 1.7, three folded wingsuits hanging at Y -.9 / 0 / .9 --
#               orange, cream, sand (the code's three)
#   rf_chalk    at (-8, 15.5): an A-frame chalkboard of the day's landings, the board facing -Y
#   rf_bench    at (-13, 14.5), turned .5: slatted, 1.6 long
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)












# skate_hangout.py -- the island skate park's hangout as art, at buildIslandSkate's m505 numbers (the code keeps the deck, the
# ramps, the poles and lights, the paint and every collider). Blender X = the islands' frame u, +Y = its v; origins on the deck y.
#   sk_sofa          at (66, 18.6): 2.0 x .9, seat .45, the back on Blender -Y (sv - .5), arms at X +-1.05, tagged in paint
#   sk_cooler        at (68.5, 17.2): .7 x .5 x .5 with its lid, handles, a can on top
#   sk_speaker       at (63.8, 19.4): the crate .6 sq x .6, the speaker .5 x .3 x .4 on it, its cone facing -Y
#   sk_board_paint / sk_board_trim  one skateboard: the deck .8 (X) x .22, kicked both ends, flat on Z = 0; paint the deck's
#                    underside graphic one white material (pink / paint / yel per board), the trim is grip, trucks, wheels.
#                    The code leans three on the rail at (70 + k*.9, S.v1 - .45) tilted -1.1 about X: do the same.
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)











# camp_kit.py -- Old Town's camp as art, at buildCamp's numbers (the code keeps every collider, the patchwork roof, the junk fence,
# the washing line, the lights, the smart spots and the fire). Blender X = the camp frame's u, +Y = its v; origins on the ground.
#   oc_tent_paint / oc_tent_trim  an A-frame tent, ridge along X: 2.8 long, 2.3 wide, 1.5 high (scale to the code's L, W, H per
#                  tent and turn it `rot`); the tarp is ONE white material -- tint it tarp / tarpo / tarp2 -- the trim is its ridge
#                  pole, uprights, pegs and guy lines, a flap tied back
#   oc_barrel      the burn barrel at (0, 0): r .33 -> .3, .9 high, holes punched round it, embers glowing inside (the fire is code)
#   oc_sofa        2.0 x .9, seat .45, the back on Blender -Y, arms at X +-.95 -- turn it r = -1.9 as now
#   oc_cart        a shopping cart, .55 x .85, the basket .35..95 -- turn it r
#   oc_shack       the shack at (u0, v0): 2.6 (X) x 2.2 (Y), 2.1 high, open on +Y, the back (-Y) rusted sheet, +X an old door,
#                  -X planks, a tin roof sloping to +Y, the stovepipe at (-.7, -.5)
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)










# market_stall.py -- the Pearl's plaza market stall as art, at buildPearl's numbers (the code keeps the counter's collider and
# places the stalls round the plaza as now). Origin at the stall's centre on the deck; Blender X = along the counter (the code's
# local x, 2.2), turned `f` exactly as the counter box. The counter is .95 high and 1 deep, the canopy 2.6 x 1.6 at 2.2..2.3, the
# poles at X +-1.2. Symmetric front to back, so it reads from the plaza and from the street.
#   pm_stall_paint  the canopy's coloured stripes and the counter's skirt in ONE white material: tint per stall with cc[i % 5]
#   pm_stall_trim   poles, counter top, the white stripes, the valance, crates of produce, a scale, a chalk board, bulbs, a basket
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)









# food_cart.py -- Old Town's food carts as art, at buildCarts' numbers (the code keeps the colliders, the canvas roof SIGNS, the
# deck, tables, umbrellas and the rest of the pod). Origin at the cart's centre on the ground; Blender X = along the cart (2.8),
# Blender +Y = its FRONT, toward the tables (the code's "+v when yaw 0"), so place each at (u, v, g) turned `yaw` as now.
#   fc_cart_paint   the painted parts -- the body (2.8 x 1.7 from .35 to 2.3) and the flip-up awning over the window -- in ONE white
#                   material, tinted per cart with K.col (an InstancedMesh with setColorAt, or a material colour per cart)
#   fc_cart_trim    everything else, never tinted: the steel roof (2.3..2.42), the serving window (1.15..1.95, 1.9 wide) and its
#                   frame, the counter at +1.05 (1.08..1.14), the sign BOARD behind the code's sign plane (+.2, 2.42..3.36), wheels
#                   at X +-1.1 (r .3), the hitch at -Y, a gas bottle, a vent stack, a menu board, a napkin box, string lights
#   fc_cart_shutter the roller shutter that closes the window, for the shut cart (WAFFLE WAGON)
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)








# freight_train.py -- Hollow Creek's freight train as art, at buildFreight's numbers (the code keeps every BDYN box and moves the
# groups as now). Three roots, one per car, each in its car GROUP's own frame: origin at rail level on the car's centre, Blender X =
# across (three x), Blender Z = up (three y), and Blender -Y = the group's +z (glTF's Y-up export turns Blender Y into three -z).
#   ft_loco     len 11: frame .5..1.0, the hood toward three -z (z -5.25..2.25, 2.5 wide, to 3.6), the cab at three +z (z 2.1..5.3,
#               2.7 wide, to 3.9, roof 3.95), the stack at z -3.5; the body collider tops out at 3.7
#   ft_flat     len 10: the deck at 1.2; the code's five logs on its -z half stay; stakes; its +z half is the open deck you ride
#   ft_caboose  len 8: deck 1.2, porches 1.4 each end, the body 2.5 wide x 5.2 long from 1.2 to 3.5, the cupola 1.2 x 1.6 on top
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)







# ferry.py -- the Old Town <-> Waterfront ferry as art, at buildFerry's numbers (the code keeps the moving BDYN boxes: the deck to
# 1.25, the side rails to +1.05, the cabin 4 x 5 to +2.6, the wheelhouse 2.4 sq to +4, two benches at +-6). One root, the
# `O.grp` group's own frame: origin AT THE WATERLINE on the centre, Blender X = across the beam (7), Blender Y = along the length
# (18; three's z), the deck at Z 1.25. It is double-ended, so which way Y points does not matter.
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)






# wf_shed_tug.py -- the Waterfront's TRANSIT SHED and the TUG at pier 2 as art, at buildWaterfront's numbers (the code keeps every
# collider, the shed's roof floor and its ladder, the tug's ladder, the pallets and drums). Blender X = the frame's u, +Y = its v.
#   wf_shed  origin (Sh.u -88, Sh.v 22) on Y: 52 (X) x 24 (Y) x 9.5; the quay face is -Y (v0 = -12) with four roll-up doors at
#            X -19.5 / -6.5 / 6.5 / 19.5, 6.4 wide, 5.6 tall; roof vents at (-14, 3), (6, -4), (18, 5); the ladder (code) at +X, Y +8
#   wf_tug   origin at the hull's centre ON ITS DECK (pier-local (w/2+2.9, -2), at sea+.9), the pier-local frame (turned P.psi):
#            hull 5 (X) x 15 (Y) down to -2.1, bow toward +Y; the wheelhouse at Y -1 (the code's -3 less the -2), 3.4 x 4.2 x 3
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)





# coaster.py -- the coaster in the Waterfront's dry dock as art, at buildWaterfront's numbers (the code keeps the hull's boxes as
# colliders, the bulwarks', the forecastle's, the steps, the hatch covers', the wheelhouse's, both ladders, the scaffold, the
# stair tower and the gangway). Blender X = the frame's u, +Y = its v, origin at (D.u, 0) on the keel blocks' top (hb): stern
# at Y 14 (S.v0), bow at 85.5 (S.v1), deck at Z 9 (S.depth), the forecastle deck 1.4 higher from 70 to the bow.
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)




# sts_crane.py -- the Waterfront's ship-to-shore crane as art, at wfCranes' numbers (the code keeps every collider, both ladders,
# the landing, the crate stair and the moving trolley / spreader / box). Blender X = the frame's u, +Y = its v, origin at the
# crane's (u, 0) on the quay top Y. T = 30 (the portal), B = 34 (the boom's top).
#   wf_sts_crane   legs at X +-8, Y 6 and 24, .9 square, Y..T, on sills with wheel bogies; portal beams at T-2..T; X-braced sides;
#                  the boom: two box-truss girders at X +-3.2 from Y -44 to +44, B-2..B; catwalks at X +-4.25 (B-.2..B) from -44 to
#                  30 with rails at +-5.05; the A-frame to the apex (0, B+14, 15) with its stays to -40, -12 and 42; the machine
#                  house at Y 37.5 (8.2 x 13, B..B+4); the landing at T-13 (Y+17) on the +X land leg.
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)



# mill_kit.py -- the Hollow Creek mill's machines as art, at buildMill's numbers (the code keeps the shed, the flume, the belts,
# the log piles, the ladders and every collider). Blender X = the mill frame's u, +Y = its +v; origins on the ground (y).
#   hm_burner      the teepee burner at (B.u 21, B.v -11): r 4 at the foot, .3 r at the top, 9 high, a mesh dome, a door, the
#                  conveyor's inlet on the -X side at 7; the smoke still leaves at y+9.3 (O.fireAt)
#   hm_crane       the log crane at (C.u -18, C.v 3): legs at +-1 to 8, the platform 2.8 sq, the cab at (-.6, -.6), the boom toward
#                  (+8, +5) from 10.4; the ladder stays the code's (on the -Y side at -1.35)
#   hm_logtruck    at (-21, 6): bed 2.4 x 9 at .5..1.3, the cab toward -Y (at -3.6), stakes and bunks; the five logs stay code
#   hm_watertower  at (9, v0-4): legs at +-1.2 to 7, a staved wooden tank r 2 from 7 to 10.4, a cone roof to 11.6
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)


# bike_pits.py -- the dirt-bike track's PITS and ANNOUNCER'S TOWER as art, at buildBikeTrack's numbers (the code keeps every
# collider, the ladder, the tracks, tabletops and berms). Blender X = the track frame's u, +Y = its +v. Each root's origin is
# on the ground at the centre the code uses.
#   bk_bike_red / _blue / _yellow  one MX bike, length along Y (front wheel +Y at .62, rear -Y at -.62; tyre .42 outer), bars
#                  at +.55, 1.15 high -- the code's `bike(u, v, g, r, col)` turns it by r exactly as it turns its own boxes
#   bk_canopy_red / _blue / _yellow  a pop-up canopy, legs at +-1.6, roof at 2.6, a valance; origin at its centre
#   bk_trailer     2.4 x 7 x 2.8, long along Y, origin at its centre (the code turns it .1)
#   bk_tower       origin (tu, tv) on g: legs at +-1.2 to 6.0, the deck 3 x 3 at 6, parapets on +Y and +-X (the -Y side open for
#                  the ladder at -1.65), corner posts at +-1.4 up to the roof at 8.3..8.4
#   bk_chest (.7 x .5 x .9), bk_drum (r .28 x .85), bk_generator (1.2 x .8 x .9) -- the pit clutter, each on its centre
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)

# fair_stage.py -- the fairground's STAGE and GRANDSTAND as art, at buildFairground's numbers (the code keeps every collider, the
# stage steps' and rows' boxes, the canvas signs, the ladder up the truss). Blender X = the fair frame's u, +Y = its +v.
#   ff_stage       origin (0, S.v -24) on y. Deck 14 x 8, top 1.4; the field is +Y (the steps at the front corners, u +-6, five
#                  .28 risers); backdrop on the back edge (v -3.8), 6 m over the deck; speaker stacks on the deck at (+-5.8, -1.5)
#                  and on the ground at (+-8.4, 0); podium at (0, +1.5); truss posts at (+-7.3, +-4.3) to 8.0, beams along u at
#                  v +-4.3, catwalk on the back beam (v -4.3, 8.0..8.15, 1.1 deep, railed), five lamp cans along the front beam
#   ff_grandstand  origin (gu 20, -2) on y. Eight rows .9 deep and .34 a riser, rising to +X (the field is -X), 24 long in Y;
#                  back wall at u +4.85 to 6.12; front posts at u -2.6; the roof at 5.92, high at the back
FMET = mat("FF_metal", (.6, .63, .65), .45, .4); PLANK = mat("FF_plank", (.48, .35, .22)); PLANK2 = mat("FF_plank_dark", (.36, .26, .16))
CLOTH = mat("FF_cloth", (.08, .08, .1), .95); CONE = mat("FF_cone", (.2, .2, .22), .6); GOLD = mat("FF_gold", (.85, .62, .2), .4, .5)
def bar(p, q, r, m):
    p, q = Vector(p), Vector(q); d = (q - p).normalized(); a = d.cross(Vector((0, 0, 1))) if abs(d.z) < .95 else d.cross(Vector((1, 0, 0))); a.normalize(); b = d.cross(a)
    vs = [p + (a*sx + b*sy)*r for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]; vs += [v + (q - p) for v in vs]
    fs = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new("bar"); me.from_pydata([tuple(v) for v in vs], [], fs); me.validate(); o = bpy.data.objects.new("bar", me); col.objects.link(o); me.materials.append(m); return put(o)
def ball(c, r, m, seg=8):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg//2), radius=r)
    me = bpy.data.meshes.new("ball"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("ball", me); col.objects.link(o); me.materials.append(m); me.transform(Matrix.Translation(c))
    for p in me.polygons: p.use_smooth = True
    return put(o)
def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

def truss(p, q, w=.35, m=None):
    """a box truss from p to q: four chords and zigzag lacing on its four faces (built from points)"""
    p, q = Vector(p), Vector(q); d = (q - p); L = d.length; n = d.normalized()
    a = n.cross(Vector((0, 0, 1))) if abs(n.z) < .95 else n.cross(Vector((1, 0, 0))); a.normalize(); b = n.cross(a)
    C = [(a*sx + b*sy)*w/2 for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for c in C: bar(p + c, q + c, .035, m)
    k = max(2, int(L/w))
    for i in range(k):
        t0, t1 = i/k, (i + 1)/k
        for j in range(4):
            c0, c1 = C[j], C[(j + 1) % 4]
            bar(p + d*t0 + (c0 if i % 2 else c1), p + d*t1 + (c1 if i % 2 else c0), .018, m)



def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)
def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)


def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)


def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

PAINTC = mat("CR_paint", (.42, .6, .58), .55, .1); PAINT2 = mat("CR_paint_faded", (.52, .68, .65), .7); RUSTC = mat("CR_rust", (.5, .27, .14), .85)
CHR = mat("CR_chrome", (.78, .8, .82), .25, .8); GLS = mat("CR_glass", (.15, .2, .25), .1); TYR = mat("CR_tyre", (.07, .07, .08), .9)
LAMPC = mat("CR_lamp", (1, .95, .8), .2); TAIL = mat("CR_tail", (.7, .08, .06), .3); ENG = mat("CR_engine", (.25, .26, .28), .5, .5)
ORNC = mat("CR_orange", (.95, .4, .1), .5); STEAM = mat("CR_steam", (.9, .9, .9), .9)
def car(name, broken):
    global cur; cur = name; groups[cur] = []
    # the lower body, rounded at the corners (a profile in X swept along Y)
    prof = [(-.9, .35), (-.9, .9), (-.85, 1.0), (.85, 1.0), (.9, .9), (.9, .35), (.85, .3), (-.85, .3)]
    for (y0, y1) in ((-2.1, -1.8), (-1.8, 1.8), (1.8, 2.1)):
        sh = .06 if abs(y0) > 1.9 or abs(y1) > 1.9 else 0
        vs = [(x, y0, z - (sh if z > .8 else 0)) for (x, z) in prof] + [(x, y1, z - (sh if z > .8 else 0)) for (x, z) in prof]
        n = len(prof); fs = [tuple(range(n))[::-1], tuple(range(n, 2*n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        me = bpy.data.meshes.new("b"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("b", me); col.objects.link(o); me.materials.append(PAINTC); put(o)
    for s in (-1, 1):
        for y in (-1.4, 1.4): box(s*.9 - .005, y - .42, .3, s*.9 + .005, y + .42, .68, DARK if False else mat("CR_arch", (.1, .1, .11), .8) if "CR_arch" not in bpy.data.materials else bpy.data.materials["CR_arch"])   # wheel arches' dark
        box(s*.91 - .01, -1.0, .55, s*.91 + .01, 1.0, .6, CHR)                                    # a chrome strip
    for (y0, y1, a) in ((-2.12, -2.05, 0), (2.05, 2.12, 0)): box(-.9, y0, .32, .9, y1, .45, CHR)  # bumpers
    for s in (-1, 1):
        box(s*.65 - .17, 2.08, .62, s*.65 + .17, 2.11, .8, LAMPC); box(s*.65 - .15, -2.11, .62, s*.65 + .15, -2.08, .78, TAIL)
    box(-.4, 2.09, .5, .4, 2.12, .62, CHR)                                                     # the grille
    # the cabin: a trapezoid sweep, glass all round, a pillar each corner
    top = [(-.72, 1.5), (.72, 1.5)]; base = [(-.82, 1.0), (.82, 1.0)]
    vs = [(-.82, -1.3, 1.0), (.82, -1.3, 1.0), (.82, .7, 1.0), (-.82, .7, 1.0), (-.72, -1.0, 1.5), (.72, -1.0, 1.5), (.72, .25, 1.5), (-.72, .25, 1.5)]
    fs = [(4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new("cab"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("cab", me); col.objects.link(o); me.materials.append(GLS); me.materials.append(PAINT2)
    me.polygons[0].material_index = 1; put(o)
    quadbox([(-.74, -1.02, 1.5), (.74, -1.02, 1.5), (.74, .27, 1.5), (-.74, .27, 1.5)], .04, PAINT2)
    for (a, b) in ((-.82, .7), (.82, .7), (-.82, -1.3), (.82, -1.3)): bar((a, b, 1.0), (a*.88, b + (-.45 if b > 0 else .3), 1.5), .04, PAINT2)
    for s in (-1, 1): bar((s*.86, -.3, 1.0), (s*.74, -.35, 1.5), .03, PAINT2)
    for s in (-1, 1): box(s*.9 - .02, .5, 1.05, s*.9 + .1*s, .65, 1.15, CHR)                   # mirrors
    for (s, y) in ((-1, -1.4), (1, -1.4), (-1, 1.4), (1, 1.4)):
        flat = broken and s < 0 and y > 0
        R = .33 if not flat else .3
        ring((s*.8, y, R), .22, .11 if not flat else .13, TYR, 14, 6)
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=.16, radius2=.16, depth=.04)
        me = bpy.data.meshes.new("hub"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("hub", me); col.objects.link(o); me.materials.append(CHR)
        me.transform(Matrix.Translation((s*.86, y, R)) @ Matrix.Rotation(math.pi/2, 4, 'Y')); put(o)
    for (x, y, sx, sy) in ((-.9, -1.9, .02, .5), (.6, 1.95, .3, .02), (.88, -.6, .02, .3)): box(x - sx, y - sy, .35, x + sx, y + sy, .5, RUSTC)   # rust
    if broken:
        box(-.85, 1.0, .9, .85, 2.05, .93, ENG)                                                    # the engine bay's floor/top
        box(-.45, 1.2, .9, .45, 1.9, 1.12, ENG); cylz(-.3, 1.55, 1.12, 1.2, .14, CHR, 12)          # the block, the air cleaner
        box(.4, 1.3, .9, .7, 1.6, 1.08, mat("CR_battery", (.12, .12, .13), .6))
        bar((-.6, 1.95, .95), (.6, 1.95, .95), .05, CHR)                                            # the radiator top
        hp = [(-.85, 1.0, 1.0), (.85, 1.0, 1.0), (.85, 1.5, 1.95), (-.85, 1.5, 1.95)]               # the hood, propped up off its hinge
        quadbox(hp, .04, PAINTC); bar((.7, 1.9, .95), (.7, 1.45, 1.85), .012, CHR)
        for k in range(4): ball((-.2 + k*.12, 1.6 + k*.08, 1.25 + k*.3), .07 + k*.035, STEAM, 8)       # steam off the radiator
        for s in (-1, 1): bar((s*.2, 5.0 - .2, 0), (0, 5.0, .45), .02, ORNC)                       # a warning triangle 3 m ahead
        bar((-.2, 4.8, .02), (.2, 4.8, .02), .02, ORNC)
    else:
        quadbox([(-.85, 1.0, .99), (.85, 1.0, .99), (.85, 2.05, .94), (-.85, 2.05, .94)], .03, PAINTC)
car("oc_car_broken", True); car("oc_car", False)
# ======== join each group under its root, export, preview
roots = {}
for name, Lg in groups.items():
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in Lg: o.select_set(True)
    bpy.context.view_layer.objects.active = Lg[0]; bpy.ops.object.join(); j = bpy.context.view_layer.objects.active; j.name = name + "_mesh"
    r = bpy.data.objects.new(name, None); col.objects.link(r); j.parent = r; roots[name] = r
    print(name, len(j.data.polygons), "faces", len(j.data.materials), "materials")
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in roots.values(): r.select_set(True); [c.select_set(True) for c in r.children]
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/old_car.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["oc_car"].location = (3.2, -1.5, 0); roots["oc_car"].rotation_euler = (0, 0, .4)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.3, .3, .32), .9))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-150))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-4.5, 7, 3.2); cam.rotation_euler = (Vector((.8, 0, .8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/old_car.png"; bpy.ops.render.render(write_still=True)
