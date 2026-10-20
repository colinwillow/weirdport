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
# ================= UNDER THE FJORD (buildGorgeDeep): the wreck, a crystal clump, the cache chest, the strongbox =================
import random; rq = random.Random(594)
ROT = mat("GW_rot", (.24, .2, .16), .95); ROT2 = mat("GW_rot2", (.3, .25, .19), .95); PAINTR = mat("GW_paint", (.3, .18, .14), .95); PAINTW = mat("GW_paint_w", (.55, .56, .5), .9)
MOSS = mat("GW_moss", (.18, .35, .29), 1); KELP = mat("GW_kelp", (.18, .42, .23), .8); WOODW = mat("GW_wood", (.35, .27, .19), .9)
CRA = mat("GW_crys_a", (.1, .29, .31), .2); _a = CRA.node_tree.nodes["Principled BSDF"]; _a.inputs["Emission Color"].default_value = (.35, 1, .88, 1); _a.inputs["Emission Strength"].default_value = 1.2
CRB = mat("GW_crys_b", (.19, .09, .29), .2); _b = CRB.node_tree.nodes["Principled BSDF"]; _b.inputs["Emission Color"].default_value = (.7, .42, 1, 1); _b.inputs["Emission Strength"].default_value = 1.2
ROCKG = mat("GW_rock", (.23, .25, .28), 1); GOLDG = mat("GW_gold", (.83, .66, .23), .3, .8); STEELG = mat("GW_steel", (.35, .38, .41), .5, .5)
# ---- the wreck: a 7 m fishing boat along Y, on her side (rolled .9 about her keel toward +X), origin at the hollow's floor under her keel
cur = "gw_wreck"; groups[cur] = []
L = 7.0; N = 10; ring = []
for i in range(N + 1):
    y = -L/2 + L * i / N; t = (i / N)
    w = .95 * math.sin(math.pi * min(1, (t * 1.15 + .05))) ** .5 if t < .87 else .95 * (1 - (t - .87) * 2.5)
    w = max(.12, w); hgt = 1.6 + .35 * (1 - t)
    ring.append([(-w, y, hgt), (-w * .85, y, .6), (0, y, 0), (w * .85, y, .6), (w, y, hgt)])
vs = [p for r in ring for p in r]; fs = []
for i in range(N):
    for j in range(4):
        a = i * 5 + j
        if j == 3 and 3 <= i <= 5: continue                       # the hole, stove in her +X side
        fs.append((a, a + 5, a + 6, a + 1))
me = bpy.data.meshes.new("hull"); me.from_pydata(vs, [], fs); o = bpy.data.objects.new("hull", me); col.objects.link(o); me.materials.append(PAINTR); o.modifiers.new("s", 'SOLIDIFY').thickness = .08; put(o)
for i in (1, 3, 5, 7, 9):                                         # ribs, through the hole too
    r = ring[i]
    for a, b in zip(r, r[1:]): bar(a, b, .06, ROT)
for i in range(N):                                                # the gunwales, half gone
    if i in (6, 7): continue
    bar(ring[i][0], ring[i + 1][0], .06, ROT2)
    if i < 6: bar(ring[i][4], ring[i + 1][4], .06, ROT2)
box(-.75, 1.4, .8, .75, 2.9, 1.7, WOODW); box(-.8, 1.35, 1.7, .8, 2.95, 1.8, ROT); box(-.6, 1.38, 1.1, .6, 1.4, 1.5, mat("GW_glass", (.1, .15, .14), .3))
box(-.3, -2.5, .6, .3, -1.9, .9, ROT2); box(-.1, -.4, .5, .1, -.2, 1.9, ROT)
for k in range(9):                                                # moss patches and kelp up off her
    x, y = rq.uniform(-.8, .8), rq.uniform(-3, 3); ball((x, y, rq.uniform(.6, 1.6)), .2, MOSS, 5)
for ob in groups[cur]: ob.data.transform(Matrix.Rotation(.9, 4, 'Y'))
for k in range(5):
    x, y = rq.uniform(-1.4, 1.6), rq.uniform(-3.5, 3.5); z0 = 0
    pts = [(x, y, z0 + t * .5) for t in range(5)]
    for t, (p, q) in enumerate(zip(pts, pts[1:])): bar((p[0] + .1 * math.sin(t + k), p[1], p[2]), (q[0] + .1 * math.sin(t + k + 1), q[1], q[2]), .05, KELP)
# ---- a crystal clump: seven glowing prisms from a rock knuckle, ~1.4 tall
cur = "gw_crystals"; groups[cur] = []
ball((0, 0, 0), .35, ROCKG, 7)
for k in range(7):
    a = k / 7 * 2 * math.pi + rq.uniform(0, .5); tilt = rq.uniform(.15, .5); h = rq.uniform(.6, 1.4); r = rq.uniform(.08, .16)
    d = Vector((math.sin(tilt) * math.cos(a), math.sin(tilt) * math.sin(a), math.cos(tilt)))
    base = Vector((.15 * math.cos(a), .15 * math.sin(a), .1))
    o = lathe([(0, 0), (r, .05), (r, h * .8), (0, h)], (CRA, CRB)[k % 3 == 0], 5, False)
    q = Vector((0, 0, 1)).rotation_difference(d); o.data.transform(q.to_matrix().to_4x4()); o.data.transform(Matrix.Translation(base))
# ---- the cache chest: 1.1 x .8 x .6 iron-banded, its lid .12, a gold spill beside (the code's gold box)
cur = "gw_cache"; groups[cur] = []
box(-.55, -.4, 0, .55, .4, .6, WOODW, .02)
for x in (-.4, 0, .4): box(x - .04, -.42, 0, x + .04, .42, .62, STEELG)
quadbox([(-.57, -.42, .6), (.57, -.42, .6), (.57, .42, .6), (-.57, .42, .6)], .12, STEELG)
box(-.08, -.44, .4, .08, -.4, .55, GOLDG)
for k in range(9): cylz(1.0 + rq.uniform(-.2, .2), -.2 + rq.uniform(-.15, .15), k * .03, k * .03 + .028, .07, GOLDG, 10) if k < 5 else cylz(.8 + rq.uniform(-.3, .3), rq.uniform(-.3, .1), 0, .028, .07, GOLDG, 10)
box(.85, .05, 0, 1.2, .3, .15, GOLDG)
# ---- the strongbox: .6 x .45 x .45 steel, a gold lid band, a dial
cur = "gw_strongbox"; groups[cur] = []
box(-.3, -.225, 0, .3, .225, .45, STEELG, .02); box(-.31, -.235, .45, .31, .235, .5, GOLDG)
o = cylz(0, 0, -.02, .02, .07, GOLDG, 12); o.data.transform(Matrix.Rotation(math.pi/2, 4, 'X')); o.data.transform(Matrix.Translation((0, -.23, .23)))
for x in (-.22, .22): box(x - .03, -.24, .08, x + .03, -.22, .38, STEELG)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/gorge_deep.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"gw_wreck": (0, 1, 0, 0), "gw_crystals": (-3.6, -1.2, 0, .2), "gw_cache": (3.2, -1.5, -.3, 0), "gw_strongbox": (-2.0, -2.8, .4, 0)}
for k, (x, y, r, z) in lay.items(): roots[k].location = (x, y, z); roots[k].rotation_euler = (0, 0, r)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.15, .3, .35, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.26, .3, .3), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-5, -10, 5); cam.rotation_euler = (Vector((0, 0, .8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/gorge_deep.png"; bpy.ops.render.render(write_still=True)
