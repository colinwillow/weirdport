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
BOARD = mat("WS_board", (.95, .95, .92), .6); LAMPW = mat("WS_lamp", (1, .9, .6), .3); TIN = mat("WS_tin", (.55, .6, .62), .5, .45); TIN2 = mat("WS_tin_dark", (.42, .46, .48), .55, .45); ROOFS = mat("WS_roof", (.4, .43, .45), .55, .5)
DOOR = mat("WS_door", (.3, .33, .36), .5, .5); YELW = mat("WS_yellow", (.9, .68, .14), .55); SKY = mat("WS_sky", (.75, .85, .9), .2, .1); WIN = mat("WS_win", (.12, .16, .2), .15)
TUGR = mat("WT_red", (.68, .16, .12), .6); TUGB = mat("WT_black", (.1, .1, .11), .6); TUGW = mat("WT_white", (.92, .91, .88), .55); RUB = mat("WT_rubber", (.06, .06, .07), .9)
def corr(x0, y0, x1, y1, z0, z1, m, out, pitch=.6, depth=.06):
    """a corrugated wall from (x0,y0) to (x1,y1), ribs vertical, the ribs standing OUT along `out` (a unit (dx, dy))"""
    vs, fs = [], []; L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L/pitch)); dx, dy = (x1 - x0)/L, (y1 - y0)/L
    for k in range(n):
        for (a, b, o0, o1) in ((0, .3, 0, 1), (.3, .5, 1, 1), (.5, .8, 1, 0), (.8, 1, 0, 0)):
            t0, t1 = (k + a)*L/n, (k + b)*L/n
            p0 = (x0 + dx*t0 + out[0]*depth*o0, y0 + dy*t0 + out[1]*depth*o0); p1 = (x0 + dx*t1 + out[0]*depth*o1, y0 + dy*t1 + out[1]*depth*o1)
            i = len(vs); vs.extend([(p0[0], p0[1], z0), (p1[0], p1[1], z0), (p1[0], p1[1], z1), (p0[0], p0[1], z1)]); fs.append((i, i + 1, i + 2, i + 3))
    me = bpy.data.meshes.new("cw"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("cw", me); col.objects.link(o); me.materials.append(m)
    bm = bmesh.new(); bm.from_mesh(me)
    c = Vector(((x0 + x1)/2 + out[0]*5, (y0 + y1)/2 + out[1]*5, (z0 + z1)/2))
    for f in bm.faces:
        if (f.calc_center_median() - c).length > (f.calc_center_median() + f.normal - c).length: pass
        elif True: f.normal_flip()
    bm.to_mesh(me); bm.free(); return put(o)
# ======== the transit shed
cur = "wf_shed"; groups[cur] = []
W2, D2, H = 26., 12., 9.5
box(-W2, -D2, -.3, W2, D2, .3, mat("WS_plinth", (.55, .53, .5), .9))                                 # a concrete upstand
DOORS = (-19.5, -6.5, 6.5, 19.5)
# the quay face: corrugated between the doors, and over them up to the eaves
xs = [-W2] + sum([[c - 3.5, c + 3.5] for c in DOORS], []) + [W2]
for i in range(0, len(xs), 2): corr(xs[i], -D2, xs[i + 1], -D2, .3, H, TIN, (0, -1))
for c in DOORS: corr(c - 3.5, -D2, c + 3.5, -D2, 6.4, H, TIN, (0, -1))
corr(W2, D2, -W2, D2, .3, H, TIN, (0, 1)); corr(-W2, -D2, -W2, D2, .3, H, TIN2, (-1, 0)); corr(W2, D2, W2, -D2, .3, H, TIN2, (1, 0))
box(-W2 + .1, -D2 + .1, .3, W2 - .1, D2 - .1, H, mat("WS_inside", (.18, .19, .2), .9))                # the dark inside, a skin behind the doors
for c in DOORS:                                                                   # roll-up doors: slats, a drum housing, yellow jambs and bumpers
    box(c - 3.2, -D2 - .06, .3, c + 3.2, -D2 - .02, 5.6, DOOR)
    for k in range(int(5.3/.25)): box(c - 3.2, -D2 - .09, .35 + k*.25, c + 3.2, -D2 - .06, .38 + k*.25, TIN2)
    box(c - 3.4, -D2 - .55, 5.6, c + 3.4, -D2, 6.3, TIN2)
    for s in (-1, 1): box(c + s*3.35 - .15, -D2 - .16, 0, c + s*3.35 + .15, -D2, 5.8, YELW); box(c + s*3.35 - .2, -D2 - .4, 0, c + s*3.35 + .2, -D2, 1.0, YELW)
    for k in range(4): box(c + s*3.35 - .16, -D2 - .17, .3 + k*.5, c + s*3.35 + .16, -D2 - .16, .55 + k*.5, TUGB) if False else None
    box(c - .8, -D2 - .1, 7.2, c + .8, -D2 - .08, 8.2, BOARD)           # a door number board (blank)
box(W2 - 5, -D2 - .06, .3, W2 - 4, -D2 - .02, 2.4, mat("WS_pdoor", (.2, .4, .3), .6))             # a personnel door
box(W2 - 5.15, -D2 - .1, 2.4, W2 - 3.85, -D2 - .02, 2.55, TUGW)
for s in (-1, 1):                                                                 # a band of clerestory windows high on the long sides
    for k in range(12):
        x = -W2 + 2 + k*4.3
        if s < 0 and (any(abs(x + 1 - c) < 4 for c in DOORS) or abs(x + 1) < 9.5): continue
        box(x, s*(D2 + .08) - .03, 7.4, x + 2.2, s*(D2 + .08) + .03, 8.4, WIN)
box(-W2 - .3, -D2 - 2.6, 6.4, W2 + .3, -D2, 6.55, ROOFS)                          # a canopy along the quay face over the doors
for k in range(9): x = -W2 + k*W2*2/8; bar((x, -D2, 4.8), (x, -D2 - 2.5, 6.4), .06, FMET)
for s in (-1, 1): box(s*(W2 + .1) - .1, -D2 - .5, H - .3, s*(W2 + .1) + .1, D2 + .5, H, FMET)
for s in (-1, 1): box(-W2 - .5, s*(D2 + .2) - .15, H - .35, W2 + .5, s*(D2 + .2) + .15, H - .1, FMET)   # gutters
for (x, y) in ((-W2 + 1, -D2 - .3), (W2 - 1, -D2 - .3), (-W2 + 1, D2 + .3), (W2 - 1, D2 + .3)): cylz(x, y, 0, H - .2, .08, FMET, 8)
quadbox([(-W2 - .3, -D2 - .3, H), (W2 + .3, -D2 - .3, H), (W2 + .3, D2 + .3, H), (-W2 - .3, D2 + .3, H)], .2, ROOFS)
for k in range(1, 26): box(-W2 - .3 + k*2.1 - .03, -D2 - .3, H + .2, -W2 - .3 + k*2.1 + .03, D2 + .3, H + .26, TIN2)   # roof sheet laps
for k in range(5): box(-20 + k*10 - 1, -6, H + .2, -20 + k*10 + 1, 6, H + .28, SKY)                  # skylights
for (a, b) in ((-14, 3), (6, -4), (18, 5)):                                       # the roof vents (the code's boxes): louvred
    box(a - 1.1, b - 1.1, H + .2, a + 1.1, b + 1.1, H + 1.4, TIN2); box(a - 1.25, b - 1.25, H + 1.4, a + 1.25, b + 1.25, H + 1.55, ROOFS)
    for k in range(4):
        for s in (-1, 1): box(a - 1.12, b + s*1.12 - .02, H + .4 + k*.25, a + 1.12, b + s*1.12 + .02, H + .5 + k*.25, DARK)
box(-8, -D2 - .1, 7.0, 8, -D2 - .07, 8.8, mat("WS_name", (.92, .92, .88), .6))     # the shed's name board (blank: TRANSIT SHED 1 goes on it)
for s in (-1, 1): box(s*W2 - (2 if s > 0 else -1), -D2 - .3, 8.6, s*W2 - (1 if s > 0 else -2), -D2 - .1, 8.9, LAMPW)
# ======== the tug
cur = "wf_tug"; groups[cur] = []
L2, B2 = 7.5, 2.5
ST = [(-7.5, 2.1, -1.2), (-6.5, 2.45, -1.7), (-4, 2.5, -2.1), (2, 2.5, -2.1), (4.5, 2.2, -1.8), (6.2, 1.5, -1.3), (7.3, .4, -.6), (7.6, .05, -.1)]
vs, fs = [], []
for (y, hw, zb) in ST:
    prof = [(0, zb), (hw*.6, zb + .05), (hw*.92, zb + .4), (hw, zb*.4), (hw*1.02, .0), (hw*1.04, .45)]
    for (x, z) in prof: vs.append((x, y, z))
    for (x, z) in reversed(prof[1:]): vs.append((-x, y, z))
m = 11
for i in range(len(ST) - 1):
    for j in range(m - 1): fs.append((i*m + j, i*m + j + 1, (i + 1)*m + j + 1, (i + 1)*m + j))
fs.append(tuple(range(m)))
me = bpy.data.meshes.new("tug"); me.from_pydata(vs, [], fs); me.validate(); me.materials.append(TUGB); me.materials.append(TUGR)
bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); bm.to_mesh(me); bm.free()
for p in me.polygons: p.material_index = 1 if p.center.z < -.9 else 0; p.use_smooth = True
o = bpy.data.objects.new("tug", me); col.objects.link(o); put(o)
quadbox([(-2.4, -7.3, -.05), (2.4, -7.3, -.05), (2.4, 6.0, -.05), (-2.4, 6.0, -.05)], .05, mat("WT_deck", (.45, .35, .25), .8))
box(-1.8, 4, 0, 1.8, 7.8, .6, TUGR)                                                # the raised foredeck (the code's box at +4.. )
box(-1.7, -3.1, 0, 1.7, 1.1, 3.0, TUGW)                                            # the wheelhouse (the code's at -3 less -2 = -1)
for s in (-1, 1): box(s*1.72 - .02, -2.8, 1.9, s*1.72 + .02, .8, 2.7, WIN)
box(-1.5, 1.1, 1.9, 1.5, 1.14, 2.7, WIN); box(-1.8, -3.2, 3.0, 1.8, 1.2, 3.15, TUGB)
cylz(0, -2.0, 3.15, 4.6, .45, TUGR, 12); cylz(0, -2.0, 4.6, 4.9, .47, TUGB, 12)   # the stack
bar((0, -.2, 3.15), (0, -.2, 5.8), .05, TUGW); box(-.6, -.25, 5.2, .6, -.15, 5.26, TUGW); ball((0, -.2, 5.9), .08, mat("WT_lamp", (1, .9, .6), .3))
for s in (-1, 1): bar((s*2.4, -7.2, .9), (s*2.4, 4, .9), .04, TUGW)                 # a rail along each side, the stern rail
bar((-2.2, -7.3, .9), (2.2, -7.3, .9), .04, TUGW)
for y in (-6.5, -4.5): cylz(0, y, 0, .7, .2, TUGB, 10)                               # the towing bitts and the hook
box(-.2, -5.6, .3, .2, -5.2, 1.1, TUGB)
for k in range(10):                                                                 # tyre fenders all round the sheer
    a = k/9; y = -7 + a*13.5; x = 2.55 if k % 2 else -2.55
    ring((x, y, -.25), .32, .14, RUB, 12, 6)
for k in range(5): ring((0, 7.5 + .02*k, -.2 + k*.0), .0 + .3, .18, RUB, 12, 6) if k == 0 else None   # the bow pudding
box(-.6, 7.55, -.6, .6, 7.9, .3, RUB)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/wf_shed_tug.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["wf_tug"].location = (26, -22, -2.3)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-60, -16, -.01), (60, -16, -.01), (60, 40, -.01), (-60, 40, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.56, .55, .52), 1))
wa = bpy.data.meshes.new("wa"); wa.from_pydata([(-60, -60, -3.2), (60, -60, -3.2), (60, -16, -3.2), (-60, -16, -3.2)], [], [(0, 1, 2, 3)]); wo = bpy.data.objects.new("wa", wa); col.objects.link(wo); wa.materials.append(mat("Wt", (.2, .35, .45), .2))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 24; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-30, -48, 14); cam.rotation_euler = (Vector((4, -6, 3)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/wf_shed_tug.png"; bpy.ops.render.render(write_still=True)
