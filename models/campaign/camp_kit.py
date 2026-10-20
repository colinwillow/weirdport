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

TARP = mat("OC_tarp", (1, 1, 1), .85); WOODC = mat("OC_wood", (.48, .35, .23), .9); ROPE = mat("OC_rope", (.79, .7, .54), .9)
RUSTC = mat("OC_rust", (.42, .23, .15), .75, .3); RUST2C = mat("OC_rust2", (.55, .32, .2), .8, .25); EMBER = mat("OC_ember", (.3, .08, .02), .9)
_b = EMBER.node_tree.nodes["Principled BSDF"]; _b.inputs["Emission Color"].default_value = (1, .45, .1, 1); _b.inputs["Emission Strength"].default_value = 4
SOFA = mat("OC_sofa", (.54, .23, .23), .9); SOFA2 = mat("OC_sofa2", (.44, .18, .18), .9); STEELO = mat("OC_steel", (.62, .65, .68), .4, .6)
TINO = mat("OC_tin", (.55, .58, .6), .5, .45); DOORO = mat("OC_door", (.31, .42, .35), .8); RED2 = mat("OC_redcart", (.75, .18, .15), .5)
# ======== the tent
cur = "oc_tent_paint"; groups[cur] = []
L2, W2, H = 1.4, 1.15, 1.5
for s in (-1, 1):                                                                         # the two slopes, sagging a little mid-span
    vs = []; n = 6
    for i in range(n + 1):
        x = -L2 + 2*L2*i/n; sag = .08*math.sin(i/n*math.pi)
        vs += [(x, 0, H - sag), (x, s*W2, 0)]
    fs = [(2*i, 2*i + 2, 2*i + 3, 2*i + 1) if s > 0 else (2*i, 2*i + 1, 2*i + 3, 2*i + 2) for i in range(n)]
    me = bpy.data.meshes.new("t"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("t", me); col.objects.link(o); me.materials.append(TARP); put(o)
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=.02); bm.to_mesh(me); bm.free()
vs = [(L2, -W2, 0), (L2, W2, 0), (L2, 0, H)]; me = bpy.data.meshes.new("e"); me.from_pydata(vs, [], [(0, 1, 2)]); me.validate(); o = bpy.data.objects.new("e", me); col.objects.link(o); me.materials.append(TARP); put(o)   # the back end, closed
for s in (-1, 1):                                                                          # the front flaps, tied back
    vs = [(-L2, 0, H), (-L2, s*W2, 0), (-L2 - .35, s*W2*.55, .2)]; me = bpy.data.meshes.new("f"); me.from_pydata(vs, [], [(0, 1, 2), (2, 1, 0)]); me.validate(); o = bpy.data.objects.new("f", me); col.objects.link(o); me.materials.append(TARP); put(o)
cur = "oc_tent_trim"; groups[cur] = []
bar((-L2 - .15, 0, H + .02), (L2 + .15, 0, H + .02), .03, WOODC)
for x in (-L2, L2): bar((x, 0, 0), (x, 0, H + .05), .025, WOODC)
for x in (-L2 - .1, L2 + .1):
    for s in (-1, 1): bar((x, 0, H), (x + (-.9 if x < 0 else .9), s*.9, 0), .008, ROPE); box(x + (-.9 if x < 0 else .9) - .02, s*.9 - .02, 0, x + (-.9 if x < 0 else .9) + .02, s*.9 + .02, .15, WOODC)
for i in range(4):
    for s in (-1, 1): x = -L2 + .2 + i*(2*L2 - .4)/3; box(x - .02, s*(W2 + .05) - .02, 0, x + .02, s*(W2 + .05) + .02, .12, WOODC)
box(-L2 + .2, -.7, 0, L2 - .2, .7, .06, mat("OC_mat", (.42, .44, .48), .9))                    # a bedroll inside
# ======== the burn barrel
cur = "oc_barrel"; groups[cur] = []
n = 14; vs, fs = [], []
for i in range(n):
    a = i/n*2*math.pi
    for (r, z) in ((.3, 0), (.315, .45), (.33, .9)): vs.append((r*math.cos(a), r*math.sin(a), z))
for i in range(n):
    j = (i + 1) % n
    for t in range(2): fs.append((i*3 + t, j*3 + t, j*3 + t + 1, i*3 + t + 1))
me = bpy.data.meshes.new("bar"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("bar", me); col.objects.link(o); me.materials.append(RUSTC); put(o)
bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=.02); bm.to_mesh(me); bm.free()
for z in (.15, .5, .85):
    for i in range(n): a0, a1 = i/n*2*math.pi, (i + 1)/n*2*math.pi; r = .3 + .03*z; bar((r*math.cos(a0), r*math.sin(a0), z), (r*math.cos(a1), r*math.sin(a1), z), .015, RUST2C)
for k in range(10):                                                                        # the punched holes, glowing
    a = k/10*2*math.pi + (.3 if k % 2 else 0); z = .3 if k % 2 else .55; r = .325
    ball((r*math.cos(a), r*math.sin(a), z), .045, EMBER, 6)
cylz(0, 0, .5, .75, .27, EMBER, 12)                                                        # embers inside
for k in range(4): a = k*1.6; bar((.1*math.cos(a), .1*math.sin(a), .7), (.25*math.cos(a + .5), .25*math.sin(a + .5), .95), .03, WOODC)   # sticks
# ======== the sofa
cur = "oc_sofa"; groups[cur] = []
box(-1.0, -.45, .08, 1.0, .45, .3, SOFA2); box(-1.0, -.45, 0, 1.0, .45, .08, WOODC)
for k in range(3): box(-.95 + k*.64, -.35, .3, -.35 + k*.64, .42, .48, SOFA, bev=.04)          # three cushions, one sunk
box(-1.0, -.45, .3, 1.0, -.22, .95, SOFA, bev=.05)
for s in (-1, 1): box(s*.95 - .11, -.45, .3, s*.95 + .11, .45, .7, SOFA, bev=.05)
box(.1, -.2, .48, .6, .2, .5, mat("OC_patch", (.35, .45, .6), .9))                           # a patch
for (x, y) in ((-.9, -.4), (.9, -.4), (-.9, .4), (.9, .4)): box(x - .04, y - .04, -.0, x + .04, y + .04, .08, WOODC)
# ======== the shopping cart
cur = "oc_cart"; groups[cur] = []
for (x, y) in ((-.22, -.36), (.22, -.36), (-.22, .36), (.22, .36)): bar((x, y, .08), (x*1.1, y*1.05, .35), .015, STEELO); ring((x, y, .06), .05, .02, DARKO := mat("OC_dark", (.1, .1, .11), .6), 8, 4)
for z in (.35, .95):
    for (a, b) in (((-.28, -.43), (.28, -.43)), ((.28, -.43), (.28, .43)), ((.28, .43), (-.28, .43)), ((-.28, .43), (-.28, -.43))): bar((a[0], a[1], z), (b[0], b[1], z), .012, STEELO)
for k in range(8):
    y = -.4 + k*.11
    for s in (-1, 1): bar((s*.28, y, .35), (s*.28, y, .95), .006, STEELO)
for k in range(5): x = -.24 + k*.12; bar((x, -.43, .35), (x, -.43, .95), .006, STEELO); bar((x, .43, .35), (x, .43, .95), .006, STEELO)
bar((-.3, .5, 1.0), (.3, .5, 1.0), .02, RED2); bar((-.28, .43, .95), (-.3, .5, 1.0), .012, STEELO); bar((.28, .43, .95), (.3, .5, 1.0), .012, STEELO)
box(-.2, -.3, .4, .15, .1, .7, mat("OC_bag", (.3, .3, .32), .9)); box(.0, .0, .4, .25, .35, .62, mat("OC_box", (.69, .54, .35), .9))   # what's in it
# ======== the shack
cur = "oc_shack"; groups[cur] = []
W, D, H = 2.6, 2.2, 2.1
def corrX(x0, x1, y, z0, z1, m):
    n = int((x1 - x0)/.15)
    for k in range(n): box(x0 + k*.15, y - .03 - (.02 if k % 2 else 0), z0, x0 + (k + 1)*.15, y + .03, z1, m)
corrX(-W/2, W/2, -D/2, -.1, H, RUSTC)
for k in range(3): box(-W/2 + .2 + k*.85, -D/2 - .06, .2 + k*.4, -W/2 + .7 + k*.85, -D/2 - .05, 1.0 + k*.4, RUST2C)   # patches
box(W/2 - .05, -D/2, -.1, W/2 + .05, D/2, H - .2, DOORO)                                     # an old door as the +X wall
for (y0, y1, z0, z1) in ((-.9, .9, .2, .9), (-.9, .9, 1.1, 1.7)): box(W/2 + .05, y0, z0, W/2 + .07, y1, z1, mat("OC_door2", (.25, .35, .29), .8) if "OC_door2" not in bpy.data.materials else bpy.data.materials["OC_door2"])
cylz(W/2 + .1, .8, .95, 1.0, .04, STEELO, 8)
for k in range(9): box(-W/2 - .05, -D/2 + k*.25, -.1, -W/2 + .05, -D/2 + k*.25 + .22, H - rnd.uniform(0, .25) if False else H - (k % 3)*.08, WOODC)   # planks
for (x, y) in ((-W/2, D/2), (W/2, D/2)): box(x - .05, y - .05, -.1, x + .05, y + .05, H - .25, WOODC)                  # front posts
for k in range(5):                                                                          # the tin roof, sloping to the open front, sheets overlapping
    x0 = -W/2 - .25 + k*(W + .5)/5; x1 = x0 + (W + .5)/5 + .05
    quadbox([(x0, -D/2 - .3, H + .12), (x1, -D/2 - .3, H + .12), (x1, D/2 + .3, H - .25), (x0, D/2 + .3, H - .25)], .03, TINO if k != 3 else RUST2C)
for (x, y) in ((-.6, -.4), (.5, .3)): box(x - .12, y - .12, H + .1, x + .12, y + .12, H + .25, mat("OC_brick", (.55, .3, .2), .9) if x < 0 else bpy.data.materials["OC_brick"])   # bricks holding it down
cylz(-.7, -.5, H, H + 1.3, .08, TINO, 8); cylz(-.7, -.5, H + 1.3, H + 1.4, .14, TINO, 8)      # the stovepipe and its cap
box(-.9, -.7, 0, -.4, -.3, .55, STEELO); cylz(-.65, -.5, .55, H, .07, TINO, 8)                # the little stove inside
box(.2, -.9, 0, 1.1, .2, .3, WOODC); box(.25, -.85, .3, 1.05, .15, .4, mat("OC_mat2", (.42, .44, .48), .9))   # a cot
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/camp_kit.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
tcols = [(.18, .44, .69), (.78, .4, .17), (.25, .56, .79)]
tp, tt = roots["oc_tent_paint"].children[0], roots["oc_tent_trim"].children[0]
for i, (u, v, r, L, Wd, Hh) in enumerate(((-5.2, -2.6, .35, 2.8, 2.3, 1.5), (4.6, -4.2, -.5, 2.6, 2.1, 1.35), (-.6, -6.4, .1, 3.0, 2.4, 1.55))):
    mb = bpy.data.materials.new("t%d" % i); mb.use_nodes = True; mb.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*tcols[i], 1)
    for src_o, tint in ((tp, mb), (tt, None)):
        o = src_o.copy(); o.data = src_o.data.copy() if tint else src_o.data; col.objects.link(o); o.parent = None
        if tint: o.data.materials[0] = tint
        o.location = (u, v, 0); o.rotation_euler = (0, 0, r); o.scale = (L/2.8, Wd/2.3, Hh/1.5)
roots["oc_tent_paint"].location = (999, 0, 0); roots["oc_tent_trim"].location = (999, 0, 0)
roots["oc_sofa"].location = (3.6, -1.4, 0); roots["oc_sofa"].rotation_euler = (0, 0, -1.9 + math.pi)
roots["oc_cart"].location = (6.3, 1.8, 0); roots["oc_cart"].rotation_euler = (0, 0, .7)
roots["oc_shack"].location = (6.6, -7.0, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.95, .7, .55, 1); bg.inputs[1].default_value = .4
g = bpy.data.meshes.new("g"); g.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.43, .35, .27), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 2.6; sun.color = (1, .8, .6); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(62), 0, math.radians(200))
cd = bpy.data.cameras.new("C"); cd.lens = 24; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (2, 9, 4.5); cam.rotation_euler = (Vector((0, -3.5, .8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/camp_kit.png"; bpy.ops.render.render(write_still=True)
