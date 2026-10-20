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


LOCO = mat("FT_green", (.18, .29, .23), .55, .3); LOCO2 = mat("FT_cream", (.88, .82, .62), .55); DARKT = mat("FT_dark", (.1, .1, .11), .6, .4)
CABR = mat("FT_red", (.68, .2, .16), .7); DECKT = mat("FT_deck", (.38, .3, .23), .85); YELT = mat("FT_yellow", (.9, .68, .14), .55)
GLT = mat("FT_glass", (.12, .16, .2), .15); LAMPT = mat("FT_lamp", (1, .9, .6), .3); STEELT = mat("FT_steel", (.55, .58, .6), .45, .55)
def Z(z): return -z                      # three's z -> Blender Y
def bx3(x0, x1, y0, y1, z0, z1, m, bev=0): return box(x0, min(Z(z0), Z(z1)), y0, x1, max(Z(z0), Z(z1)), y1, m, bev)
def truck(zc):
    """a two-axle bogie centred at three z = zc: side frames, springs, four wheels on the 1.5 gauge"""
    for s in (-1, 1):
        bx3(s*.75 - .06, s*.75 + .06, .25, .75, zc - 1.2, zc + 1.2, DARKT)
        for dz in (-.7, .7):
            vs = []; n = 14
            for k in range(n): a = k/n*2*math.pi; vs.append((s*.75, Z(zc + dz) + .42*math.cos(a), .42 + .42*math.sin(a)))
            vs += [(v[0] + s*.12, v[1], v[2]) for v in vs]
            fs = [tuple(range(n)), tuple(range(2*n - 1, n - 1, -1))] + [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
            me = bpy.data.meshes.new("w"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("w", me); col.objects.link(o); me.materials.append(STEELT); put(o)
        cylz(s*.75, Z(zc), .55, .7, .12, YELT, 8)
    bx3(-.8, .8, .5, .62, zc - .3, zc + .3, DARKT)
def underframe(hl, top=1.0):
    bx3(-1.2, 1.2, .5, top, -hl + .1, hl - .1, DARKT)
    for e in (-1, 1):
        bx3(-.15, .15, .55, .8, e*(hl - .1), e*(hl + .35), DARKT)                         # couplers
        bx3(-1.25, 1.25, .5, .9, e*(hl - .15), e*(hl - .05), YELT)                         # end sills, striped
    truck(-hl + 1.4); truck(hl - 1.4)
# ======== the locomotive: a hood unit, green and cream, the cab at three +z
cur = "ft_loco"; groups[cur] = []
hl = 5.5; underframe(hl)
bx3(-1.25, 1.25, 1.0, 1.2, -hl + .1, hl - .1, LOCO)                                   # the running board
bx3(-1.15, 1.15, 1.2, 3.6, -5.25, 2.25, LOCO, bev=.06)                                 # the long hood
for k in range(6): bx3(-1.17, 1.17, 2.0, 3.3, -4.8 + k*1.1, -4.4 + k*1.1, mat("FT_louver", (.13, .21, .17), .6) if k == 0 else bpy.data.materials["FT_louver"])   # louvred doors
bx3(-1.16, 1.16, 1.4, 1.7, -5.25, 2.25, LOCO2)                                         # the cream band
bx3(-1.35, 1.35, 1.0, 3.9, 2.1, 5.3, LOCO, bev=.05); bx3(-1.45, 1.45, 3.9, 4.05, 2.0, 5.4, DARKT)
bx3(-1.36, 1.36, 1.4, 1.7, 2.1, 5.3, LOCO2)
for s in (-1, 1): bx3(s*1.35 - .02, s*1.35 + .02, 2.6, 3.5, 2.4, 3.6, GLT); bx3(s*1.35 - .02, s*1.35 + .02, 2.6, 3.5, 3.9, 5.0, GLT)
for x in (-.75, .75): bx3(x - .45, x + .45, 2.7, 3.5, 5.3, 5.32, GLT); bx3(x - .45, x + .45, 2.7, 3.5, 2.08, 2.1, GLT)
cylz(0, Z(-3.5), 3.6, 4.6, .3, DARKT, 10); cylz(0, Z(-3.5), 4.5, 4.7, .36, DARKT, 10)
for zc in (-1.5, .5): bx3(-.45, .45, 3.6, 3.85, zc - .45, zc + .45, STEELT)              # radiator fans / vents
cylz(0, Z(-2.5), 3.6, 4.2, .08, STEELT, 6); bar((-.3, Z(-2.5), 4.2), (.3, Z(-2.5), 4.25), .08, STEELT)   # the horn
for e, z in ((-1, -5.35), (1, 5.4)): cylz(0, Z(z) - (0 if e > 0 else 0), 3.1, 3.3, .18, LAMPT, 10) if False else ball((0, Z(z), 3.2 if e < 0 else 3.75), .16, LAMPT, 8)
for s in (-1, 1):                                                                     # handrails down both running boards, steps at the corners
    bar((s*1.22, Z(-hl + .3), 2.05), (s*1.22, Z(2.0), 2.05), .025, YELT)
    for k in range(4): z = -hl + .3 + k*2.5; bar((s*1.22, Z(z), 1.2), (s*1.22, Z(z), 2.05), .02, YELT)
    for e in (-1, 1): bx3(s*1.0 - .25, s*1.0 + .25, .35, .4, e*(hl - .4) - .2, e*(hl - .4) + .2, YELT); bx3(s*1.0 - .25, s*1.0 + .25, .7, .75, e*(hl - .4) - .2, e*(hl - .4) + .2, YELT)
bx3(-1.3, 1.3, 1.2, 1.45, -hl + .05, -hl + .3, YELT)                                   # the nose's yellow (the code's .4 bar)
for k in range(5): bx3(-1.3 + k*.55, -1.3 + k*.55 + .27, 1.2, 1.45, -hl + .02, -hl + .06, DARKT)
bx3(-.6, .6, 2.3, 2.9, 2.08, 2.1, mat("FT_board", (.93, .9, .82), .6))                # a blank number board
# ======== the flatcar: a planked deck, stake pockets and stakes, the open half for riding
cur = "ft_flat"; groups[cur] = []
hl = 5.0; underframe(hl)
bx3(-1.3, 1.3, 1.0, 1.1, -hl, hl, DARKT)
for k in range(13): bx3(-1.3, 1.3, 1.1, 1.2, -hl + k*.77 + .02, -hl + (k + 1)*.77 - .02, DECKT)   # deck planks across
for s in (-1, 1):
    for k in range(5): z = -hl + .4 + k*2.3; bx3(s*1.3 - .08, s*1.3 + .08, .95, 1.2, z - .1, z + .1, DARKT)
    for z in (-hl + .4, -hl + 2.7, -hl + 5.0 - .2): bx3(s*1.25 - .06, s*1.25 + .06, 1.2, 2.8, z - .06, z + .06, STEELT)   # stakes up the log half
for z in (-hl + .5, -hl + 3, -hl + 5.4): bar((-1.25, Z(z), 2.75), (1.25, Z(z), 2.75), .02, DARKT)   # chains over the logs
bx3(-1.3, 1.3, 1.2, 1.45, hl - .3, hl - .05, YELT)                                      # a kick-board at the open end
# ======== the caboose: red, a cupola, porches with rails and steps at both ends, windows, a stove pipe
cur = "ft_caboose"; groups[cur] = []
hl = 4.0; underframe(hl)
bx3(-1.3, 1.3, 1.0, 1.2, -hl, hl, DECKT)
bl = 8 - 2*1.4
bx3(-1.25, 1.25, 1.2, 3.5, -bl/2, bl/2, CABR, bev=.04)
for k in range(int(bl/.3)): bx3(-1.27, 1.27, 1.2, 3.45, -bl/2 + .15 + k*.3 - .015, -bl/2 + .15 + k*.3 + .015, mat("FT_red2", (.58, .16, .13), .7) if k == 0 else bpy.data.materials["FT_red2"])
for s in (-1, 1):
    for z in (-1.4, 1.4): bx3(s*1.27 - .02, s*1.27 + .02, 2.2, 3.0, z - .4, z + .4, GLT)
    bx3(s*1.27 - .03, s*1.27 + .03, 2.12, 3.08, -1.9, -1.8, LOCO2)
for e in (-1, 1): bx3(-.45, .45, 1.2, 3.1, e*bl/2 - .02, e*bl/2 + .02, mat("FT_door", (.86, .78, .55), .6) if e < 0 else bpy.data.materials["FT_door"])
quadbox([(-1.4, Z(-bl/2 - .3), 3.5), (1.4, Z(-bl/2 - .3), 3.5), (1.4, Z(bl/2 + .3), 3.5), (-1.4, Z(bl/2 + .3), 3.5)][::-1] if False else [(-1.4, Z(bl/2 + .3), 3.5), (1.4, Z(bl/2 + .3), 3.5), (1.4, Z(-bl/2 - .3), 3.5), (-1.4, Z(-bl/2 - .3), 3.5)], .12, DARKT)
bx3(-.6, .6, 3.62, 4.4, -.8, .8, CABR); bx3(-.7, .7, 4.4, 4.52, -.9, .9, DARKT)          # the cupola
for s in (-1, 1): bx3(s*.6 - .02, s*.6 + .02, 3.85, 4.25, -.6, .6, GLT)
for e in (-1, 1): bx3(-.45, .45, 3.85, 4.25, e*.8 - .02, e*.8 + .02, GLT)
cylz(.7, Z(1.6), 3.6, 4.6, .07, DARKT, 8)                                              # stove pipe
for e in (-1, 1):                                                                       # porch rails (the code's yellow bar at +1.0) and steps
    z = e*(hl - .1)
    bar((-1.25, Z(z), 2.2), (1.25, Z(z), 2.2), .03, YELT)
    for s in (-1, 1):
        bar((s*1.25, Z(z), 1.2), (s*1.25, Z(z), 2.2), .03, YELT); bar((s*1.25, Z(z), 2.2), (s*1.25, Z(e*bl/2), 2.2), .03, YELT)
        for k in range(2): bx3(s*1.05 - .25, s*1.05 + .25, .45 + k*.35, .5 + k*.35, z - e*.3 - .15, z - e*.3 + .15, YELT)
    ball((0, Z(e*bl/2), 3.3), .1, CABR, 6)
ball((0, Z(-bl/2 - .02), 3.2), .12, mat("FT_tail", (1, .2, .1), .3), 8)                  # the tail lamp
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/freight_train.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
# the cars laid in train order as buildFreight strings them (front first, along three -z... shown along Blender Y)
roots["ft_loco"].location = (0, -(11/2), 0); roots["ft_flat"].location = (0, -(11 + 1.1 + 5), 0); roots["ft_caboose"].location = (0, -(11 + 1.1 + 10 + 1.1 + 4), 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-40, -60, -.2), (40, -60, -.2), (40, 30, -.2), (-40, 30, -.2)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.45, .38, .26), 1))
for s in (-1, 1): box(s*.75 - .04, -50, -.2, s*.75 + .04, 10, 0, mat("Rail", (.5, .5, .52), .4, .7))
for k in range(100): box(-1.2, -50 + k*.6, -.3, 1.2, -50 + k*.6 + .25, -.15, mat("Tie", (.3, .22, .16), .9))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-12, 6, 6); cam.rotation_euler = (Vector((0, -14, 1.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/freight_train.png"; bpy.ops.render.render(write_still=True)
