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











# site_kit.py -- Old Town's building site pieces as art, at buildSite's numbers (the code keeps the frame, the scaffold, every
# ladder and collider, the hook line and its load, the stacks and cones). Blender X = the site frame's u, +Y = its v; origins on
# the ground at the code's centres.
#   os_crane     the tower crane at (mu, mv) on gm: a 2.6 sq pad to .6, a 1.4 sq lattice mast to 26, the slewing unit and cab at
#                26.4, the A-frame over it, the JIB along Blender +X (17 m) and the counter-jib along -X (6 m) with its
#                counterweights. Turn it so +X points along the code's (cos ja, sin ja) -- back over the frame.
#   os_office    the site office at (ou, ov): 2.4 (X) x 5.0 (Y) x 2.6, its window on -X at Y +1.0, a door, steps
#   os_mixer     at (3.0, sv+1.4), turned .5: the drum on its stand, wheels, a tow bar
#   os_skip      at (-su-2.2, sv+.6), turned .1: 2.0 x 3.2 x 1.3, rubble in it
#   os_hoarding  ONE 2.4 m hoarding panel, centred, X along it, -Y the street side, from -.1 to 2.2 -- the code's `bx` per panel
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)










# lighthouse.py -- the River Islands' lighthouse and the keeper's cottage as art, at buildIslands' numbers (the code keeps the
# tower's box collider, the cottage's, the ladder, the oil store, drums, flag, washing line, pots, rope, and IKEEP's beam).
#   li_lighthouse  origin (K.u, K.v) on the rock top. Tower r 1.8 -> 1.4 over 11 m, red bands at 2.5 and 6.5, a stone apron r 2.5,
#                  the gallery deck r 2.4 at 11.1 with its rail (r 2.3, to 12.1), the lantern r 1.1 from 11.2 to 12.8 with the lens
#                  at 12 (the code's lamp point), the red cap to 14 and a vent ball. Its DOOR faces Blender +Y: turn the root so +Y
#                  points along the code's door direction (cos dA, sin dA) in the islands' frame. Windows climb from the door.
#   li_cottage     origin (cu0, cv0) on the rock top: 3.2 (X) x 2.6 (Y), walls to 2.5, a pitched roof (ridge along X) to ~3.3, the
#                  chimney at X +1.0; its door and two windows on Blender +Y. Turn it `cps` exactly as the code's cottage box.
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

YELS = mat("OS_yellow", (.95, .74, .14), .5); CONC = mat("OS_conc", (.65, .63, .6), .9); WHS = mat("OS_white", (.92, .92, .9), .55)
DARKS = mat("OS_dark", (.12, .12, .13), .5); WINS = mat("OS_win", (.12, .16, .2), .15); ORNS = mat("OS_orange", (.95, .42, .1), .5)
BLUES = mat("OS_hoard", (.18, .35, .54), .7); PLY = mat("OS_ply", (.72, .58, .38), .8); RUBB = mat("OS_rubble", (.55, .5, .45), .95)
BRICKS = mat("OS_brick", (.6, .29, .21), .85); STEELS = mat("OS_steel", (.55, .58, .6), .45, .55); TYRES = mat("OS_tyre", (.07, .07, .08), .9)
POST = [mat("OS_poster%d" % i, c, .7) for i, c in enumerate(((.92, .9, .82), (.85, .3, .25), (.25, .45, .3)))]
# ======== the tower crane
cur = "os_crane"; groups[cur] = []
H = 26.
box(-1.3, -1.3, -.3, 1.3, 1.3, .6, CONC)
for (a, b) in ((-.6, -.6), (.6, -.6), (-.6, .6), (.6, .6)): box(a - .1, b - .1, .5, a + .1, b + .1, .62, STEELS)   # anchor plates
truss((0, 0, .6), (0, 0, H), 1.4, YELS)
box(-.9, -.9, H, .9, .9, H + .4, YELS)                                                        # the slewing ring
cylz(0, 0, H + .05, H + .35, .8, DARKS, 16)
box(-.8, .7, H + .4, .9, 2.1, H + 1.9, WHS); box(-.82, 1.0, H + .9, .92, 2.12, H + 1.75, WINS)   # the cab off one side
box(-.5, -.5, H + .4, .5, .5, H + 1.3, YELS)
for s in (-1, 1): bar((s*.45, 0, H + 1.3), (0, 0, H + 4.8), .09, YELS)                         # the A-frame / tower head
truss((-6, 0, H + .85), (17, 0, H + .85), .9, YELS)                                           # jib (+X) and counter-jib (-X) as one box truss
box(-6.2, -.5, H + .35, -2.2, .5, H + .45, STEELS)                                            # counter-jib walkway
for k in range(4): box(-5.8 + k*.9, -.55, H - .9, -5.0 + k*.9, .55, H + .4, CONC)              # the counterweight blocks
for x in (17, 8): bar((0, 0, H + 4.8), (x, 0, H + 1.3), .025, STEELS)                          # the pendant ties
bar((0, 0, H + 4.8), (-6, 0, H + 1.3), .025, STEELS)
box(10.7, -.35, H + .15, 12.0, .35, H + .4, YELS)                                             # the trolley at the code's 0.7 jib
for s in (-1, 1): ring((10.8 + (0 if s < 0 else 1.1), 0, H + .3), .12, .04, DARKS, 10, 5)
ball((0, 0, H + 4.95), .12, mat("OS_red", (1, .15, .1), .3), 8); ball((17, 0, H + 1.4), .1, bpy.data.materials["OS_red"], 8)
box(-.5, -.45, H + 2.0, .5, .45, H + 2.06, STEELS)                                            # a sign board on the head (blank)
for k in range(int(H/2.4)): box(.69, -.2, 1 + k*2.4, .71, .2, 1.04 + k*2.4, STEELS)          # ladder rungs inside the mast face
# ======== the site office (a portacabin)
cur = "os_office"; groups[cur] = []
box(-1.2, -2.5, .25, 1.2, 2.5, 2.6, WHS, bev=.04)
for k in range(9): box(-1.22, -2.45 + k*.6, .3, -1.21, -2.4 + k*.6, 2.55, mat("OS_white2", (.82, .82, .8), .6) if k == 0 else bpy.data.materials["OS_white2"])
box(-1.25, -2.55, 2.6, 1.25, 2.55, 2.75, DARKS)
box(-1.23, .4, 1.0, -1.21, 1.6, 2.0, WINS); for_ = [box(-1.26, .35, .95, -1.2, 1.65, 1.0, DARKS), box(-1.26, .35, 2.0, -1.2, 1.65, 2.05, DARKS)]
for k in range(4): box(-1.27, .45 + k*.37, 1.0, -1.25, .48 + k*.37, 2.0, STEELS)               # bars over the window
box(-1.23, -1.6, .25, -1.21, -.7, 2.2, mat("OS_door", (.3, .4, .5), .6))
for k in range(3): box(-1.9 + k*.22, -1.65, 0, -1.25, -.65, .1 + k*.08, STEELS) if False else box(-1.25 - (3 - k)*.25, -1.65, 0, -1.25, -.65, .1 + k*.08, STEELS)   # steps
for (a, b) in ((-1, -2.2), (1, -2.2), (-1, 2.2), (1, 2.2)): box(a - .15, b - .15, 0, a + .15, b + .15, .26, CONC)        # blocks it sits on
box(1.2, -.4, 1.6, 1.45, .4, 2.1, STEELS)                                                      # an AC unit on the back
box(-1.24, -.3, 2.2, -1.21, .3, 2.45, mat("OS_sign", (.95, .74, .14), .5))                    # a yellow SITE OFFICE plate
# ======== the mixer
cur = "os_mixer"; groups[cur] = []
box(-.7, -.45, .3, .7, .45, .55, STEELS)
for s in (-1, 1): ring((0, s*.5, .3), .22, .08, TYRES, 12, 5)
bar((-.7, 0, .4), (-1.4, 0, .35), .04, STEELS)
for s in (-1, 1): bar((s*.5, -.35, .55), (s*.3, -.2, 1.1), .04, ORNS); bar((s*.5, .35, .55), (s*.3, .2, 1.1), .04, ORNS)
bm = bmesh.new()
prof = [(.0, -.65), (.42, -.55), (.6, -.1), (.55, .25), (.3, .6), (.25, .65)]
n = 16; vs = []; fs = []
for i in range(n):
    a = i/n*2*math.pi
    for (r, z) in prof: vs.append((r*math.cos(a), r*math.sin(a), z))
for i in range(n):
    j = (i + 1) % n
    for t in range(len(prof) - 1): fs.append((i*len(prof) + t, j*len(prof) + t, j*len(prof) + t + 1, i*len(prof) + t + 1))
me = bpy.data.meshes.new("drum"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("drum", me); col.objects.link(o); me.materials.append(ORNS)
me.transform(Matrix.Translation((.1, 0, 1.1)) @ Matrix.Rotation(.9, 4, 'Y')); put(o)
for p in me.polygons: p.use_smooth = True
box(-.25, -.2, .55, .25, .2, .9, DARKS)                                                       # the engine box
# ======== the skip
cur = "os_skip"; groups[cur] = []
vs = [(-1.0, -1.6, 0), (1.0, -1.6, 0), (1.0, 1.6, 0), (-1.0, 1.6, 0), (-1.0, -1.9, 1.3), (1.0, -1.9, 1.3), (1.0, 1.9, 1.3), (-1.0, 1.9, 1.3)]
for (sx, f) in ((1.0, 0), ):
    pass
me = bpy.data.meshes.new("skip"); me.from_pydata(vs + [(v[0]*.94, v[1]*.96, v[2] + (.08 if v[2] < .1 else 0)) for v in vs], [], [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (3, 2, 1, 0), (12, 13, 9, 8), (13, 14, 10, 9), (14, 15, 11, 10), (15, 12, 8, 11), (8, 9, 10, 11), (4, 5, 13, 12), (5, 6, 14, 13), (6, 7, 15, 14), (7, 4, 12, 15)]); me.validate()
o = bpy.data.objects.new("skip", me); col.objects.link(o); me.materials.append(YELS); put(o)
for s in (-1, 1):
    for y in (-.8, .8): bar((s*1.02, y, .1), (s*1.02, y*1.15, 1.25), .04, YELS)
    box(s*1.0 - .02*s - .03, -.3, .9, s*1.0 + .03, .3, 1.05, DARKS)                               # lifting lugs
import random as _r; rr2 = _r.Random(7)
for k in range(14):
    x, y = rr2.uniform(-.75, .75), rr2.uniform(-1.4, 1.4); sz = rr2.uniform(.15, .35); m = rr2.choice((RUBB, BRICKS, PLY, CONC))
    box(x - sz, y - sz*.7, .85 + rr2.uniform(0, .3), x + sz, y + sz*.7, .85 + rr2.uniform(.3, .55), m)
bar((-.5, -1.2, 1.1), (.6, 1.3, 1.6), .03, STEELS)                                            # a pipe sticking out
# ======== one hoarding panel
cur = "os_hoarding"; groups[cur] = []
box(-1.2, -.04, -.1, 1.2, .04, 2.2, BLUES)
for x in (-1.2, 1.2): box(x - .05, -.08, -.1, x + .05, .08, 2.25, PLY)
box(-1.2, -.06, 1.2, 1.2, -.04, 1.32, WHS)                                                     # a white band
import random as _r2; rp = _r2.Random(3)
for k in range(2):                                                                             # posters, pasted, one torn
    x = rp.uniform(-.9, .3); box(x, -.07, .35 + k*.0, x + .55, -.06, 1.05, POST[k % 3])
box(.4, -.07, 1.45, 1.0, -.06, 1.95, POST[2])
for k in range(3): box(-1.18, .04, .3 + k*.7, 1.18, .12, .4 + k*.7, PLY)                         # the battens behind (the site side)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/site_kit.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
su, sv = 4.0, 3.25
roots["os_crane"].location = (su + 1.8, sv + 1.2, 0); roots["os_crane"].rotation_euler = (0, 0, math.atan2(-(sv + 1.2), -(su + 1.8)))
roots["os_office"].location = (su + 2.0, -sv + .3, 0); roots["os_mixer"].location = (3.0, sv + 1.4, 0); roots["os_mixer"].rotation_euler = (0, 0, .5)
roots["os_skip"].location = (-su - 2.2, sv + .6, 0); roots["os_skip"].rotation_euler = (0, 0, .1)
hp = roots["os_hoarding"].children[0]
for k in range(6):
    o = hp.copy(); col.objects.link(o); o.parent = None; o.location = (-7.2 + 1.2 + k*2.4, -(sv + 2.2), 0)
roots["os_hoarding"].location = (999, 0, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-60, -60, 0), (60, -60, 0), (60, 60, 0), (-60, 60, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.55, .5, .44), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 22; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-34, -30, 12); cam.rotation_euler = (Vector((0, 0, 13)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/site_kit.png"; bpy.ops.render.render(write_still=True)
