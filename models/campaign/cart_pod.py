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



# trailer_park.py -- Hollow Creek's trailer park homes as art, at buildTrailerPark's numbers (the code keeps every platform,
# post, the walk, porches, ramps, ladder, laundry and colliders). Blender X = across the gorge (the frame's u), +Y = along it (v).
#   tp_trailer_cream / _tin / _rust / _red   a single-wide, 2.6 wide (X) x 10 long (Y) x 2.7 to the roof, origin at its centre on
#              its FLOOR (yp). Door, windows and the porch side face -X: for a trailer with side +1 the walk is at -u, so place it as
#              is; for side -1 turn it by pi. Lengths 8..11 in HCTRAIL: scale Y by len/10 (the ends are short, it holds up).
#              Door at Y -1.0 (= -len*.1), windows at Y 0 and +-3 (= k*len*.3) -- the code's own spots.
#   tp_dish, tp_chair, tp_flamingo   yard props on their own centres
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

CHROME = mat("TP_chrome", (.75, .77, .8), .25, .8); CREAMT = mat("TP_cream", (.88, .84, .72)); TINT = mat("TP_tin", (.68, .71, .73), .4, .55); RUSTT = mat("TP_rust", (.52, .29, .17), .8); REDT = mat("TP_red", (.68, .2, .16), .7)
GLASS = mat("TP_glass", (.12, .16, .2), .15); LAT = mat("TP_lattice", (.86, .83, .76)); PINK = mat("TP_pink", (.95, .45, .62), .5)
def lathe(prof, m, n=24, smooth=True):
    vs, fs = [], []
    for i in range(n):
        a = i/n*2*math.pi
        for (r, z) in prof: vs.append((r*math.cos(a), r*math.sin(a), z))
    k = len(prof)
    for i in range(n):
        j = (i + 1) % n
        for t in range(k - 1): fs.append((i*k + t, j*k + t, j*k + t + 1, i*k + t + 1))
    me = bpy.data.meshes.new("lathe"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("lathe", me); col.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = smooth
    return put(o)
# ================= THE FOOD-CART POD (buildCarts m488): picnic table + umbrella, shade sail, bin, generator, gas, potted plant =================
import random; rq = random.Random(488)
TIMB = mat("CP_timber", (.54, .41, .28)); TIMB2 = mat("CP_timber_dark", (.42, .31, .2)); PAINTW = mat("CP_paint_white", (1, 1, 1), .8); POLE = mat("CP_pole", (.72, .75, .78), .35, .6)
SAIL = mat("CP_sail", (.96, .84, .66), .9); BING = mat("CP_bin", (.18, .35, .23), .6); GEN = mat("CP_gen", (.85, .62, .15), .5, .2); GAS = mat("CP_gas", (.82, .23, .16), .5, .3)
POT = mat("CP_pot", (.69, .35, .23), .8); LEAF = mat("CP_leaf", (.31, .54, .23)); LEAF2 = mat("CP_leaf2", (.24, .44, .2)); NAP = mat("CP_napkin", (.14, .15, .17))
def leafy(c, r, m, sub=1):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    for v in bm.verts: v.co.z *= .9; v.co += Vector((rq.uniform(-.03, .03), rq.uniform(-.03, .03), 0))
    me = bpy.data.meshes.new("lf"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("lf", me); col.objects.link(o); me.materials.append(m); o.location = c; put(o)
# ---- the picnic table: top 1.8 x .8 at .72..78, benches 1.8 x .3 at .42..47, +-.7 in Y, A-frame legs, umbrella pole to 2.3, napkin box
cur = "cp_table"; groups[cur] = []
for k in range(5): box(-.9, -.4 + k*.16 + .005, .72, .9, -.4 + (k + 1)*.16 - .005, .78, (TIMB, TIMB2)[k % 2])
for s in (-1, 1):
    for k in range(2): box(-.9, s*.7 - .15 + k*.15 + .005, .42, .9, s*.7 - .15 + (k + 1)*.15 - .005, .47, TIMB)
for x in (-.65, .65):
    bar((x, -.75, 0), (x, -.05, .72), .04, TIMB2); bar((x, .75, 0), (x, .05, .72), .04, TIMB2); box(x - .04, -.85, .36, x + .04, .85, .42, TIMB2)
cylz(0, 0, 0, 2.3, .025, POLE, 8); box(.22, -.07, .78, .38, .07, .95, NAP)
# ---- its umbrella canopy: r 1.3, .5 deep, ten panels, top at 2.7; ONE white material (tint umb / umb2 / umb3)
cur = "cp_umbrella_paint"; groups[cur] = []
lathe([(0, 2.72), (.12, 2.7), (.7, 2.52), (1.3, 2.2), (1.32, 2.15)], PAINTW, 10, False)
cur = "cp_umbrella_ribs"; groups[cur] = []
for k in range(10): a = k / 10 * 2 * math.pi; bar((0, 0, 2.68), (1.28*math.cos(a), 1.28*math.sin(a), 2.18), .01, POLE)
ball((0, 0, 2.75), .05, POLE, 6)
# ---- the shade sail: origin at the deck's (0, 0); posts at the code's (-3.4, 5.6) and (3.6, .6) to 3.2, the sail between, sagging
cur = "cp_sail"; groups[cur] = []
A = (-3.4, 5.6); B = (3.6, .6)
for (x, y) in (A, B): cylz(x, y, 0, 3.2, .06, TIMB2, 8); box(x - .15, y - .15, 0, x + .15, y + .15, .05, TIMB2)
corners = [(A[0], A[1], 3.15), (-.4, .3, 2.9), (B[0], B[1], 3.15), (.0, 4.9, 2.9)]
vs, fs = [], []; N = 6
for i in range(N + 1):
    for j in range(N + 1):
        s, t = i / N, j / N
        p = [(1-s)*(1-t)*corners[0][q] + s*(1-t)*corners[1][q] + s*t*corners[2][q] + (1-s)*t*corners[3][q] for q in range(3)]
        p[2] -= .1 * math.sin(math.pi*s) * math.sin(math.pi*t); vs.append(tuple(p))
for i in range(N):
    for j in range(N): a = i*(N + 1) + j; fs.append((a, a + N + 1, a + N + 2, a + 1))
me = bpy.data.meshes.new("sail"); me.from_pydata(vs, [], fs); o = bpy.data.objects.new("sail", me); col.objects.link(o); me.materials.append(SAIL); o.modifiers.new("s", 'SOLIDIFY').thickness = .02; put(o)
for c in (corners[1], corners[3]): bar(c, (c[0], c[1], 0), .006, DARK)
for c in (corners[0], corners[2]): ball(c, .05, POLE, 6)
# ---- a bin: r .25 at the top, .22 at the foot, .8 tall, a lid and a slot
cur = "cp_bin"; groups[cur] = []
lathe([(0, 0), (.22, 0), (.25, .78), (0, .78)], BING, 14, False); lathe([(.27, .78), (.27, .84), (.18, .88), (0, .88)], BING, 14, False); box(-.1, -.27, .62, .1, -.24, .7, DARK)
# ---- the generator: 1.2 x .8 x .8 on a frame, panel and exhaust
cur = "cp_generator"; groups[cur] = []
for (x, y) in ((-.6, -.4), (.6, -.4), (-.6, .4), (.6, .4)): box(x - .03, y - .03, 0, x + .03, y + .03, .8, DARK)
for z in (.08, .78): box(-.6, -.4, z - .03, .6, .4, z, DARK)
box(-.5, -.32, .1, .4, .32, .72, GEN, .04); box(.42, -.25, .2, .58, .25, .6, FMET); box(-.45, -.33, .45, -.05, -.32, .65, DARK)
cylz(.5, .3, .78, 1.0, .04, FMET, 8)
# ---- a gas bottle: r .18, .75 tall, a collar and valve
cur = "cp_gas"; groups[cur] = []
lathe([(0, 0), (.17, 0), (.18, .05), (.18, .62), (.12, .72), (0, .74)], GAS, 14); cylz(0, 0, .72, .8, .03, FMET, 8); lathe([(.11, .68), (.12, .85), (.1, .85), (.09, .7)], FMET, 12)
# ---- the potted plant on the deck: r .32 -> .26, .5 tall, a bushy plant to ~1.1
cur = "cp_planter"; groups[cur] = []
lathe([(0, 0), (.26, 0), (.32, .5), (.34, .52), (.3, .52), (0, .46)], POT, 14)
for j in range(7): a = j * 2.2; d = .05 + .17 * (j % 2); leafy((math.cos(a)*d, math.sin(a)*d, .7 + (j % 3) * .12), .2 + rq.uniform(0, .06), (LEAF, LEAF2)[j % 2], 2)
# ======== join each group under its root, export, preview
roots = {}
for name, Lg in groups.items():
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in Lg: o.select_set(True)
    bpy.context.view_layer.objects.active = Lg[0]; bpy.ops.object.join(); j = bpy.context.view_layer.objects.active; j.name = name + "_mesh"
    r = bpy.data.objects.new(name, None); col.objects.link(r); j.parent = r; roots[name] = r
    print(name, len(j.data.polygons), "faces", len(j.data.materials), "materials", tuple(round(d, 2) for d in j.dimensions))
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in roots.values(): r.select_set(True); [c.select_set(True) for c in r.children]
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/cart_pod.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"cp_sail": (0, 0, 0, 0), "cp_table": (-.2, 3, .3, 0), "cp_umbrella_paint": (-.2, 3, .3, 0), "cp_umbrella_ribs": (-.2, 3, .3, 0), "cp_bin": (-3.5, -1.5, 0, 0), "cp_generator": (-1.6, -1.8, .3, 0), "cp_gas": (.2, -1.8, 0, 0), "cp_planter": (1.5, -1.5, 0, 0)}
for k, (x, y, r, z) in lay.items(): roots[k].location = (x, y, z); roots[k].rotation_euler = (0, 0, r)
for c in roots["cp_umbrella_paint"].children: c.data.materials[0] = mat("prev_u", (.91, .31, .29), .8)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.43, .36, .27), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-3, -10, 5.5); cam.rotation_euler = (Vector((0, 1.5, 1.2)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/cart_pod.png"; bpy.ops.render.render(write_still=True)
