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
# ================= CAMP HOLLIS YARD: buildMilBase's trucks, camo net, comms mast and supply cage (MILB, m745) as art. Blender X = u, +Y = v;
# origins on the base's ground (y).
# mt_truck: one cargo truck, built for psi 0 with its cab toward +Y (the code's forward (sin psi, cos psi)): origin at the code's (u, v); the
# canvas-tilt body centred at Y -.8 (2.3 x 4.2, .9..2.9), the cab at +2.2 (2.3 x 1.8 to 2.5) with its windscreen at +2.85, wheels at Y -2.2 /
# 0 / 2.4 and X +-1.05 (r .48), bumper, lamps. The code's `olive` colliders stay; the plate is separate on the code's side (one truck has one).
# mt_net: the camo net, origin at its centre (-8.25, 6) on y + 3.58: a 9.8 m square drape, sagging between its four poles (whose own boxes are
# the code's thin `wood` posts -- leave them, or use the `mt_pole` here at each [-13 1.5] [-3.5 1.5] [-13 10.5] [-3.5 11]).
# mt_mast: the comms mast at (-2, -14): a 15 m triangular lattice (legs at the code's three points), its rungs every 1.2, three guys to 6 m out at
# 0 / 2.09 / 4.18 rad, the beacon housing at the top (the code's red sphere stays: it blinks), the generator at (+1.4, +1.2).
# mt_cage: the supply cage at (4, -13.5), 5 x 3.6 x 2.6 chain-link with its door at +Y, the crate stacks and the prize box (olive, yellow lid) at
# the code's spots. The `wire` / `crate` / `olive` colliders stay.
OLIVE = mat("MY_olive", (.37, .43, .2), .7); OLIVE2 = mat("MY_olive_dark", (.28, .33, .15), .7); CAN = mat("MY_canvas", (.48, .48, .32), .9)
TYRE = mat("MY_tyre", (.08, .08, .09), .9); DARK = mat("MY_dark", (.12, .13, .14), .6, .5); GLASS = mat("MY_glass", (.15, .2, .22), .1, .3)
STEEL = mat("MY_steel", (.5, .55, .58), .45, .7); NET = mat("MY_net", (.29, .35, .18), .9); NET2 = mat("MY_net2", (.4, .38, .25), .9)
WOOD = mat("MY_wood", (.54, .41, .27), .9); LINK = mat("MY_link", (.6, .63, .65), .4, .8); CRATE = mat("MY_crate", (.42, .42, .23), .8)
YEL = mat("MY_yellow", (.9, .7, .1), .5); RED = mat("MY_red", (.8, .1, .08), .4); WHITE = mat("MY_white", (.9, .88, .82), .6)
LINK.use_backface_culling = False; NET.use_backface_culling = False; NET2.use_backface_culling = False
cur = "mt_truck"; groups[cur] = []
box(-1.15, -2.9, .9, 1.15, 1.3, 1.05, OLIVE2, .01)                                            # the bed floor
box(-1.15, -2.9, 1.05, 1.15, 1.3, 1.6, OLIVE, .01)                                            # the bed sides
vs = []; fs = []
import bmesh
for k, y in enumerate([-2.9 + i * .7 for i in range(7)]):
    bar((-1.15, y, 1.6), (-1.15, y, 2.75), .02, DARK); bar((1.15, y, 1.6), (1.15, y, 2.75), .02, DARK); bar((-1.15, y, 2.75), (1.15, y, 2.75), .02, DARK)
box(-1.2, -2.95, 1.6, 1.2, 1.35, 2.9, CAN, .04); box(-1.2, -2.95, 2.9, 1.2, 1.35, 3.0, CAN, .04)
box(-1.15, 1.3, .9, 1.15, 3.1, 2.5, OLIVE, .03); box(-1.1, 3.1, .9, 1.1, 3.25, 1.55, OLIVE2, .02)   # cab, bonnet front
box(-1.0, 3.09, 1.7, 1.0, 3.12, 2.3, GLASS, 0)
for s in (-1, 1): box(s * 1.15 - .01 * (s < 0), 1.6, 1.7, s * 1.15 + .01 * (s > 0), 2.8, 2.3, GLASS, 0)
box(-1.2, 3.25, .65, 1.2, 3.4, .85, DARK, .01)
box(-1.15, -.2, .55, 1.15, .9, .9, DARK, 0)
for a in (-2.2, 0, 2.4):
    for s in (-1, 1):
        o = cylz(0, 0, -.18, .18, .48, TYRE, 14); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y')); o.data.transform(Matrix.Translation((s * 1.05, a, .48)))
        o = cylz(0, 0, -.19, .19, .24, OLIVE2, 10); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y')); o.data.transform(Matrix.Translation((s * 1.05, a, .48)))
for s in (-1, 1): box(s * 1.05 - .2, -2.65, .9, s * 1.05 + .2, -1.75, 1.0, OLIVE2, 0); box(s * 1.05 - .2, 1.95, .9, s * 1.05 + .2, 2.85, 1.0, OLIVE2, 0)
cur = "mt_net"; groups[cur] = []
N = 14; vs = []; fs = []
P = [(-4.75, -4.5), (4.75, -4.5), (-4.75, 4.5), (4.75, 5)]
for i in range(N + 1):
    for j in range(N + 1):
        x = -4.9 + 9.8 * i / N; yv = -4.9 + 9.8 * j / N
        d = min(math.hypot(x - px, yv - py) for px, py in P)
        z = -min(.6, .12 * d) + .06 * math.sin(i * 1.7 + j * 2.3)
        vs.append((x, yv, z))
for i in range(N):
    for j in range(N): fs.append((i * (N + 1) + j, (i + 1) * (N + 1) + j, (i + 1) * (N + 1) + j + 1, i * (N + 1) + j + 1))
me = bpy.data.meshes.new("net"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("net", me); col.objects.link(o); me.materials.append(NET); me.materials.append(NET2)
for k, p in enumerate(me.polygons): p.material_index = 1 if (k * 7) % 5 == 0 else 0
put(o)
cur = "mt_pole"; groups[cur] = []
box(-.05, -.05, 0, .05, .05, 3.6, WOOD, 0); box(-.12, -.12, 3.55, .12, .12, 3.6, WOOD, 0)
cur = "mt_mast"; groups[cur] = []
L = [(-.3, -.3), (.3, -.3), (0, .3)]
for (a, b) in L: box(a - .03, b - .03, 0, a + .03, b + .03, 15, STEEL, 0)
for k in range(13):
    z0 = .2 + k * 1.2; z1 = z0 + 1.2
    for i in range(3):
        p, q = L[i], L[(i + 1) % 3]; bar((p[0], p[1], z0), (q[0], q[1], z1), .012, STEEL); bar((p[0], p[1], z0), (q[0], q[1], z0), .015, STEEL)
for k in range(3):
    a = k * 2.09; bar((0, 0, 12), (math.cos(a) * 6, math.sin(a) * 6, .1), .01, DARK); box(math.cos(a) * 6 - .15, math.sin(a) * 6 - .15, 0, math.cos(a) * 6 + .15, math.sin(a) * 6 + .15, .12, STEEL, 0)
for z in (10.5, 12.5): box(-.12, -.5, z, .12, -.32, z + .9, WHITE, .02)                      # panel antennas
cylz(0, 0, 15, 15.05, .2, DARK, 10); cylz(0, 0, 15.05, 15.15, .08, DARK, 8)
box(.6, .65, 0, 2.2, 1.75, 1.0, OLIVE, .03); box(.62, 1.75, .5, 2.18, 1.78, .9, DARK, 0); box(.7, .75, 1.0, 2.1, 1.65, 1.1, OLIVE2, .02)
cylz(1.9, .9, 1.1, 1.5, .05, DARK, 6)
cur = "mt_cage"; groups[cur] = []
gw, gd = 5, 3.6
def panel(x0, y0, x1, y1):
    L = math.hypot(x1 - x0, y1 - y0); n = max(2, int(L / .25)); m = 10
    bar((x0, y0, 2.6), (x1, y1, 2.6), .025, STEEL); bar((x0, y0, .05), (x1, y1, .05), .015, STEEL)
    vs2, fs2 = [], []
    for i in range(n):
        for j in range(m):
            t0 = i / n; t1 = (i + 1) / n; z0 = j * 2.6 / m; z1 = (j + 1) * 2.6 / m
            pa = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0); pb = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
            for (A, za, B, zb) in ((pa, z0, pb, z1), (pa, z1, pb, z0)):
                q = len(vs2); vs2.extend([(A[0], A[1], za - .008), (B[0], B[1], zb - .008), (B[0], B[1], zb + .008), (A[0], A[1], za + .008)]); fs2.append((q, q + 1, q + 2, q + 3))
    me = bpy.data.meshes.new("lk"); me.from_pydata(vs2, [], fs2); me.validate(); o = bpy.data.objects.new("lk", me); col.objects.link(o); me.materials.append(LINK); put(o)
panel(-gw / 2, -gd / 2, gw / 2, -gd / 2); panel(-gw / 2, -gd / 2, -gw / 2, gd / 2); panel(gw / 2, -gd / 2, gw / 2, gd / 2)
panel(-gw / 2, gd / 2, -.2, gd / 2); panel(1.6, gd / 2, gw / 2, gd / 2)
for (a, b) in ((-gw / 2, -gd / 2), (gw / 2, -gd / 2), (-gw / 2, gd / 2), (gw / 2, gd / 2), (-.2, gd / 2), (1.6, gd / 2)): cylz(a, b, 0, 2.7, .04, STEEL, 8)
bar((-.2, gd / 2, 1.3), (1.6, gd / 2 - .9, 1.3), .02, STEEL)
import random; rq = random.Random(5)
for (a, b, n) in ((-1.6, -1, 3), (-.4, -1.1, 2), (1.8, -1, 2)):
    for l in range(n):
        box(a - .525, b - .4, l * .62, a + .525, b + .4, l * .62 + .6, CRATE, .02); box(a - .3, b - .405, l * .62 + .2, a + .3, b - .4, l * .62 + .4, WHITE, 0)
box(.45, .15, 0, 1.35, .65, .5, OLIVE, .02); box(.44, .14, .5, 1.36, .66, .56, YEL, .01); box(.8, .13, .3, 1.0, .15, .4, RED, 0)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/hollis_yard.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
def inst(k, x, y, z, r=0):
    c = bpy.data.objects.new(k, None); col.objects.link(c); c.location = (x, y, z); c.rotation_euler = (0, 0, r)
    for ch in roots[k].children: cc = ch.copy(); col.objects.link(cc); cc.parent = c
for k in roots: roots[k].location = (0, 0, -40)
inst("mt_truck", -11, 4, 0, -.3); inst("mt_truck", -6.5, 8, 0, .2)
inst("mt_net", -8.25, 6, 3.58)
for (a, b) in ((-13, 1.5), (-3.5, 1.5), (-13, 10.5), (-3.5, 11)): inst("mt_pole", a, b, 0)
inst("mt_mast", -2, -14, 0); inst("mt_cage", 4, -13.5, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (8, 22, 14); cam.rotation_euler = (Vector((-4, -3, 2)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/hollis_yard.png"; bpy.ops.render.render(write_still=True)
