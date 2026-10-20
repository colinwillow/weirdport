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


HULL = mat("CS_hull", (.16, .18, .21), .6, .4); ANTI = mat("CS_anti", (.55, .17, .13), .8); WHITE2 = mat("CS_white", (.9, .9, .87), .5)
DECK = mat("CS_deck", (.42, .36, .3), .8); HOUSE = mat("CS_house", (.86, .85, .8), .6); FUN = mat("CS_funnel", (.25, .54, .35), .5); PRIMER = mat("CS_primer", (.72, .38, .2), .9)
WIN = mat("CS_window", (.1, .14, .18), .15); HATCH = mat("CS_hatch", (.23, .42, .29), .6, .3)
cur = "wf_coaster"; groups[cur] = []
D = 9.0
# half-beams and deck heights by station, from the code's SECT (b/2), rounded into a ship's lines
ST = [(14.0, 4.6, 3.0, D), (15.0, 5.2, 2.2, D), (16.0, 5.6, 1.4, D), (17.5, 6.1, .7, D), (19.0, 6.4, .3, D), (22.0, 6.95, 0, D), (40, 7.0, 0, D), (66, 7.0, 0, D), (72, 6.9, 0, D + .5),
      (76, 6.3, .2, D + 1.4), (79, 5.4, .6, D + 1.4), (81.5, 4.2, 1.2, D + 1.4), (82.6, 3.5, 1.6, D + 1.42), (83.5, 2.6, 2.2, D + 1.45), (84.3, 1.8, 2.9, D + 1.47), (85.0, 1.0, 3.6, D + 1.5), (85.6, .15, 5.0, D + 1.5)]
def section(hw, zb, zt, v):
    """one half-section from the keel up to the deck edge: a flat bottom, a round bilge, near-vertical sides that FLARE at the bow"""
    fl = max(0, (v - 74)/12)                                  # forward of 74 the bottom pulls in and the top flares out
    hb = hw*(1 - .55*fl); P = [(0, zb), (hb*.55, zb)]
    for k in range(1, 6):
        a = k/6*math.pi/2; P.append((hb*.55 + (hb*.45)*math.sin(a), zb + (min(2.4, zt - zb)*.5)*(1 - math.cos(a))))
    P += [(hb + (hw - hb)*.5, zb + (zt - zb)*.5), (hw, zt)]
    for zc in (3.3, 3.5):                                     # a vertex row AT the waterline and the boot-top, so the paint splits clean
        if zb < zc < zt and not any(abs(p[1] - zc) < 1e-3 for p in P):
            for i in range(len(P) - 1):
                (x0, z0), (x1, z1) = P[i], P[i + 1]
                if z0 < zc <= z1: P.insert(i + 1, (x0 + (x1 - x0)*(zc - z0)/(z1 - z0), zc)); break
    while len(P) < 12: P.insert(-1, ((P[-2][0] + P[-1][0])/2, (P[-2][1] + P[-1][1])/2))
    return P[:12]
secs = [section(hw, zb, zt, v) for (v, hw, zb, zt) in ST]
n = len(secs[0])
vs, fs = [], []
for (v, hw, zb, zt), S in zip(ST, secs):
    for (x, z) in S: vs.append((x, v, z))
    for (x, z) in reversed(S[1:]): vs.append((-x, v, z))
m = 2*n - 1
for i in range(len(ST) - 1):
    for j in range(m - 1): fs.append((i*m + j, i*m + j + 1, (i + 1)*m + j + 1, (i + 1)*m + j))
fs.append(tuple(range(m))[::-1] if False else tuple(range(m)))                     # the transom
me = bpy.data.meshes.new("hull"); me.from_pydata(vs, [], fs); me.validate(); me.materials.append(HULL); me.materials.append(ANTI); me.materials.append(WHITE2)
for p in me.polygons:
    zc = p.center.z; p.material_index = 1 if zc < 3.3 else (2 if zc < 3.5 else 0); p.use_smooth = True
o = bpy.data.objects.new("hull", me); col.objects.link(o); put(o)
# make sure the normals face out (a hand-built loft can come out inside-out)
bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); bm.to_mesh(me); bm.free()
for p in me.polygons: zc = p.center.z; p.material_index = 1 if zc < 3.3 else (2 if zc < 3.5 else 0); p.use_smooth = True
# the boot-top line (white) as a thin proud band at 3.3..3.5 along the parallel middle body
for s in (-1, 1): box(s*7.0 - .02, 22, 3.3, s*7.0 + .02, 72, 3.5, WHITE2)
# the deck: planks of steel plate, and the forecastle deck over it from 70
quadbox([(-6.9, 22, D - .1), (6.9, 22, D - .1), (6.9, 70, D - .1), (-6.9, 70, D - .1)], .1, DECK)
quadbox([(-5.9, 14.3, D - .1), (5.9, 14.3, D - .1), (6.9, 22, D - .1), (-6.9, 22, D - .1)], .1, DECK)
box(-6.95, 70, D, 6.95, 76, D + 1.4, HULL)
quadbox([(-6.3, 76, D + 1.3), (6.3, 76, D + 1.3), (2.6, 83.5, D + 1.35), (-2.6, 83.5, D + 1.35)], .1, DECK)
for k in range(5): box(3 - 1.2, 70 - (4 - k)*.55 - .55, D, 3 + 1.2, 70 - (4 - k)*.55, D + (k + 1)*.28, FMET)
# bulwarks with their gaps, a rail along the top, stanchion ribs
def bul(x, v0, v1):
    if v1 - v0 < .2: return
    box(x - .1, v0, D, x + .1, v1, D + 1, HULL); box(x - .14, v0, D + 1, x + .14, v1, D + 1.08, WHITE2)
    for k in range(int((v1 - v0)/1.5)): box(x - .18*(1 if x < 0 else -1) - .04, v0 + .7 + k*1.5, D, x - .18*(1 if x < 0 else -1) + .04, v0 + .74 + k*1.5, D + 1, HULL)
bul(6.9, 22, 49.2); bul(6.9, 50.8, 70); bul(-6.9, 22, 40); bul(-6.9, 44, 70)
for s in (-1, 1): bul(s*5.9, 14.2, 22)
box(-6, 14.0, D, 6, 14.2, D + 1, HULL)
for s in (-1, 1):                                                                # the forecastle's rail up to the bow
    for (a, b) in (((s*6.3, 76), (s*2.6, 83.5)),): bar((a[0], a[1], D + 2.4), (b[0], b[1], D + 2.45), .04, WHITE2); bar((a[0], a[1], D + 1.9), (b[0], b[1], D + 1.95), .03, WHITE2)
# the hatch covers (the code's c2 boxes): ribbed, with cleats
for (v0, v1) in ((30, 38), (40, 48), (54, 62)):
    box(-4.5, v0, D, 4.5, v1, D + .9, HATCH)
    for k in range(int((v1 - v0)/.8)): box(-4.52, v0 + .2 + k*.8, D + .9, 4.52, v0 + .3 + k*.8, D + .98, HATCH)
    box(-4.6, v0 - .1, D, 4.6, v0, D + .5, FMET); box(-4.6, v1, D, 4.6, v1 + .1, D + .5, FMET)
    for s in (-1, 1): box(s*4.5 - .05, (v0 + v1)/2 - 1, D + .2, s*4.5 + .05, (v0 + v1)/2 + 1, D + .6, DARK)
# deck gear: two cargo masts with derricks, bollards, the windlass on the forecastle, anchors in their hawse pipes
for vm in (39, 63):
    cylz(0, vm, D, D + 11, .3, WHITE2, 12); box(-1.5, vm - .2, D + 8, 1.5, vm + .2, D + 8.3, WHITE2)
    bar((0, vm, D + 1.5), (0, vm + (-6 if vm == 39 else 5), D + 6), .12, WHITE2); bar((0, vm, D + 11), (0, vm + (-6 if vm == 39 else 5), D + 6), .02, DARK)
    ball((0, vm, D + 11.1), .15, mat("CS_lamp", (1, .9, .6), .3) if "CS_lamp" not in bpy.data.materials else bpy.data.materials["CS_lamp"])
for s in (-1, 1):
    for v in (24, 46, 68): cylz(s*5.8, v, D, D + .6, .2, DARK, 10); cylz(s*5.8, v + .7, D, D + .6, .2, DARK, 10)
    cylz(s*1.6, 79, D + 1.4, D + 2.1, .4, DARK, 12)
    box(s*5.4 - .3, 81.5, 7.2, s*5.4 + .3, 82.2, 8.0, DARK)                         # hawse pipe
    box(s*5.6 - .05, 81.0, 5.6, s*5.6 + .05, 82.6, 7.3, DARK)                      # the anchor's shank and crown
box(-1.2, 78.3, D + 1.4, 1.2, 79.7, D + 2.0, FMET)
# the wheelhouse aft: two decks of accommodation, the bridge with its window band and wings, the funnel, a mast with lights
box(-5, 15, D, 5, 23, D + 3.5, HOUSE); box(-4.6, 15.2, D + 3.5, 4.6, 22.8, D + 7, HOUSE)
for s in (-1, 1):
    for k in range(3): box(s*5 - .03, 16 + k*2.4, D + 1.3, s*5 + .03, 17.2 + k*2.4, D + 2.4, WIN)
    box(s*4.6 - .03, 15.6, D + 4.8, s*4.6 + .03, 22.4, D + 6.2, WIN)
    box(s*4.6, 21.6, D + 4.6, s*6.6, 23.2, D + 4.75, HOUSE); bar((s*6.6, 21.6, D + 5.7), (s*6.6, 23.2, D + 5.7), .03, WHITE2)   # bridge wings
box(-4.4, 22.8, D + 4.8, 4.4, 23.03, D + 6.2, WIN)
for k in range(9): box(-4.3 + k*.96, 23.02, D + 4.8, -4.24 + k*.96, 23.06, D + 6.2, HOUSE)
box(-4.8, 14.9, D + 7, 4.8, 23.1, D + 7.15, DARK)
for k in range(4): box(-4.8 + k*3.2 - .02, 23.0, D + 7.15, -4.8 + k*3.2 + .02, 23.1, D + 8.1, WHITE2)
box(-4.8, 23.0, D + 7.6, 4.8, 23.1, D + 7.66, WHITE2); box(-4.8, 23.0, D + 8.05, 4.8, 23.1, D + 8.11, WHITE2)
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=1.5, radius2=1.3, depth=6)
me = bpy.data.meshes.new("fun"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("fun", me); col.objects.link(o); me.materials.append(FUN); me.transform(Matrix.Translation((0, 17.5, D + 10))); put(o)
for p in me.polygons: p.use_smooth = True
cylz(0, 17.5, D + 12.2, D + 13.0, 1.33, DARK, 16); cylz(0, 17.5, D + 10.6, D + 11.0, 1.42, WHITE2, 16)
for s in (-1, 1): bar((s*.8, 21, D + 7), (s*.8, 21, D + 13), .06, FMET)
box(-1.2, 20.9, D + 12.4, 1.2, 21.1, D + 12.5, FMET); ball((0, 21, D + 13.2), .12, bpy.data.materials["CS_lamp"])
for s in (-1, 1): box(s*7.0 - .02, 15, D - 1.5, s*7.0 + .02, 22, D - .3, HULL)     # lifeboat davits' plates
for s in (-1, 1):                                                                # a lifeboat each side of the house
    cylz(s*5.9, 19, D + 3.6, D + 4.4, .5, mat("CS_boat", (.95, .45, .1), .6) if "CS_boat" not in bpy.data.materials else bpy.data.materials["CS_boat"], 10)
# the repair: plates off the west side shown as bare primer patches, and a few staging brackets
for (v, h) in ((34, 2.4), (46, 3), (58, 2)): box(-7.03, v - 2.5, 2.2 + 2.2, -6.99, v + 2.5, 2.2 + 2.2 + h, PRIMER)
for v in range(26, 70, 6): box(-7.05, v, 4.0, -6.95, v + .4, 4.1, PRIMER)
box(-.8, 14.0, 4.5, .8, 14.05, 5.5, WHITE2)                                       # a blank name board on the transom
for s in (-1, 1): box(s*2.6 - .3, 83.0, D - .2, s*2.6 + .3, 83.05, D + .6, WHITE2) if False else None
cylz(0, 14.6, -.3, 3.0, .08, DARK, 8); box(-.05, 13.4, .6, .05, 14.4, 2.8, DARK)   # rudder stock and rudder
for k in range(4): a = k*math.pi/2; bar((0, 14.6, 1.6), (.9*math.cos(a), 14.6, 1.6 + .9*math.sin(a)), .14, mat("CS_brass", (.75, .55, .25), .3, .8) if k == 0 else bpy.data.materials["CS_brass"])   # the propeller
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/coaster.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-40, -20, -.01), (40, -20, -.01), (40, 120, -.01), (-40, 120, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.42, .36, .3), 1))
for v in range(16, 82, 4): bpy.data.objects.new  # (keel blocks are the code's)
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-50))
cd = bpy.data.cameras.new("C"); cd.lens = 24; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-32, 100, 16); cam.rotation_euler = (Vector((0, 50, 6)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/coaster.png"; bpy.ops.render.render(write_still=True)
