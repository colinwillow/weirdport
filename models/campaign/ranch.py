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
# ================= SHADOWHIDE RANCH: buildRanch (RANCH, m822, Birch Institute's UFO ranch) as art. Blender X = u, +Y = v; origins on the flat's y at
# the code's spots. The canvas gate sign and the night's effects stay code; every collider stays.
# rn_gate (0, -15): two log gateposts at +-2.4 to 3.6 and the crossbar at 3.3..3.55, iron brackets.
# rn_house (-6, 5): 9 x 6 weathered-board house to 3 with batten strips, two boarded windows on -Y, the door, side windows, the pitched tin roof
# (ridge along X, slopes .52), the stone chimney at (+3.3, +1.5), the porch deck 1.6 deep on -Y with three log posts and its tin roof, a bench,
# a crate and the porch lamp.
# rn_trailer (7.5, 5): the white research trailer 2.6 x 8 on blocks, its windows on -X, the door, the dish on the roof at +2, the whip aerial at
# (+.9, -3.4), the generator at (-2.6, -2) and its cable.
# rn_tower (9, -8): four log poles at +-1.2 to 6.1, cross braces at 1.6 / 3.3, the deck at 5, the log rail (open at -Y for the ladder), the
# spotlight and the camera.
# rn_corral (-8, -8): fourteen posts round r 4.6 (missing k 3: the gate gap) with two log rails (missing the run from k 2), and the scorched ring
# r 1.6..2.5 inside.
LOG = mat("RN_log", (.35, .28, .21), .9); BOARD = mat("RN_board", (.48, .42, .35), .95); BOARD2 = mat("RN_board_dark", (.37, .32, .27), .95)
DECK = mat("RN_deck", (.54, .45, .35), .9); TIN = mat("RN_tin", (.54, .54, .52), .55, .5); RUST = mat("RN_rust", (.54, .29, .16), .9)
DARK = mat("RN_dark", (.12, .11, .1), .8); STONE = mat("RN_stone", (.48, .46, .44), .95); WHITE = mat("RN_white", (.9, .9, .88), .6)
STEEL = mat("RN_steel", (.54, .59, .63), .4, .6); GLOW = mat("RN_glow", (1, .82, .54), .3); SCORCH = mat("RN_scorch", (.16, .15, .13), 1)
IRON = mat("RN_iron", (.2, .21, .22), .5, .5)
GLOW.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1, .82, .54, 1); GLOW.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.5
TIN.use_backface_culling = False
import bmesh
def logbox(x, y, z0, z1, r=.16, M=LOG): return cylz(x, y, z0, z1, r, M, 8)
cur = "rn_gate"; groups[cur] = []
for s in (-1, 1): logbox(s * 2.4, 0, -.3, 3.6, .17)
o = cylz(0, 0, -2.7, 2.7, .14, LOG, 8); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y')); o.data.transform(Matrix.Translation((0, 0, 3.43)))
for s in (-1, 1): box(s * 2.4 - .2, -.18, 3.2, s * 2.4 + .2, -.16, 3.6, IRON, 0)
cur = "rn_house"; groups[cur] = []
W2, D2, H = 4.5, 3, 3
box(-W2, -D2, -.4, W2, D2, H, BOARD, 0)
for k in range(9): box(-W2 + .5 + k - .03, -D2 - .04, .1, -W2 + .5 + k + .03, -D2, H - .1, BOARD2, 0)
for k in range(7): box(-W2 + .5 + k - .03, D2, .1, -W2 + .5 + k + .03, D2 + .04, H - .1, BOARD2, 0)
for x in (-2.8, 2.8):
    box(x - .55, -D2 - .06, 1, x + .55, -D2 - .01, 2.2, DARK, 0)
    for k in range(3): box(x - .7, -D2 - .1, 1.2 + k * .4, x + .7, -D2 - .05, 1.35 + k * .4, BOARD2, 0)
box(-.5, -D2 - .06, .35, .5, -D2 - .01, 2.4, DARK, 0); box(.3, -D2 - .1, 1.3, .36, -D2 - .06, 1.4, IRON, 0)
for s in (-1, 1): box(s * W2 - .03, -.6, 1, s * W2 + .03, .6, 2.1, DARK, 0)
for s in (-1, 1):
    vs = [(-W2 - .4, 0, H + 1.6), (W2 + .4, 0, H + 1.6), (W2 + .4, s * (D2 + .5), H - .1), (-W2 - .4, s * (D2 + .5), H - .1)]
    o = bpy.data.objects.new("rf", bpy.data.meshes.new("rf")); o.data.from_pydata(vs, [], [(0, 1, 2, 3)]); col.objects.link(o); o.data.materials.append(TIN); o.modifiers.new("s", 'SOLIDIFY').thickness = .06; put(o)
    for k in range(13): x = -W2 + k * .75; bar((x, 0, H + 1.62), (x, s * (D2 + .5), H - .08), .02, TIN)
for s in (-1, 1):
    vs = [(s * W2, -D2, H), (s * W2, D2, H), (s * W2, 0, H + 1.5)]
    me = bpy.data.meshes.new("gb"); me.from_pydata(vs, [], [(0, 1, 2)]); o = bpy.data.objects.new("gb", me); col.objects.link(o); me.materials.append(BOARD); o.modifiers.new("s", 'SOLIDIFY').thickness = .1; put(o)
box(W2 - 1.55, 1.15, H - .5, W2 - .85, 1.85, H + 2.4, STONE, .03); box(W2 - 1.6, 1.1, H + 2.3, W2 - .8, 1.9, H + 2.4, STONE, .02)
box(-W2, -D2 - 1.6, 0, W2, -D2, .35, DECK, .01)
for k in range(15): x = -W2 + .3 + k * .6; box(x - .01, -D2 - 1.6, .35, x + .01, -D2, .352, BOARD2, 0)
for s in (-1, 0, 1): logbox(s * (W2 - .2), -D2 - 1.5, .35, 2.5, .08)
vs = [(-W2 - .15, -D2, 2.75), (W2 + .15, -D2, 2.75), (W2 + .15, -D2 - 1.75, 2.42), (-W2 - .15, -D2 - 1.75, 2.42)]
o = bpy.data.objects.new("pr", bpy.data.meshes.new("pr")); o.data.from_pydata(vs, [], [(0, 1, 2, 3)]); col.objects.link(o); o.data.materials.append(TIN); o.modifiers.new("s", 'SOLIDIFY').thickness = .05; put(o)
o = cylz(0, 0, -.7, .7, .2, LOG, 8); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y')); o.data.transform(Matrix.Translation((-2.2, -D2 - .5, .6)))
o = box(-.27, -.27, .35, .27, .27, .95, BOARD2, .02); o.data.transform(Matrix.Translation((0, 0, 0))); o.data.transform(Matrix.Translation((2.4, -D2 - .6, 0)))
ball((-.9, -D2 - .15, 2.3), .09, GLOW, 8); box(-.95, -D2 - .05, 2.35, -.85, -D2, 2.5, IRON, 0)
cur = "rn_trailer"; groups[cur] = []
box(-1.3, -4, .45, 1.3, 4, 3.1, WHITE, .05); box(-1.32, -4.02, .45, 1.32, 4.02, .65, STEEL, 0)
for (a, b) in ((-1, -3), (1, -3), (-1, 3), (1, 3)): box(a - .2, b - .2, 0, a + .2, b + .2, .45, STONE, .02)
for b in (-2.4, 0, 2.4): box(-1.33, b - .6, 1.6, -1.3, b + .6, 2.4, DARK, 0)
box(-1.33, -3.75, .5, -1.3, -2.85, 2.6, BOARD2, 0)
o = bpy.data.objects.new("ds", bpy.data.meshes.new("ds")); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=6, radius=.9)
for v in list(bm.verts):
    if v.co.z < .9 * math.cos(math.pi / 2.6): v.co.z = .9 * math.cos(math.pi / 2.6)
bm.to_mesh(o.data); bm.free(); col.objects.link(o); o.data.materials.append(WHITE); put(o)
o.data.transform(Matrix.Translation((0, 0, -.9))); o.data.transform(Matrix.Rotation(-1.9, 4, 'Y')); o.data.transform(Matrix.Translation((0, 2, 3.7)))
cylz(0, 2, 3.1, 3.65, .06, STEEL, 6); cylz(.9, -3.4, 3.1, 6.5, .02, STEEL, 5)
box(-3.1, -2.35, 0, -2.1, -1.65, .9, RUST, .03); bar((-2.1, -2, .05), (-1.3, -1, .05), .04, DARK)
cur = "rn_tower"; groups[cur] = []
hw = 1.2
for (a, b) in ((-1, -1), (1, -1), (-1, 1), (1, 1)): logbox(a * hw, b * hw, -.3, 6.1, .1)
for z in (1.6, 3.3):
    for s in (-1, 1): bar((-hw, s * hw, z - .5), (hw, s * hw, z + .5), .05, LOG); bar((s * hw, -hw, z - .5), (s * hw, hw, z + .5), .05, LOG)
box(-1.35, -1.35, 4.85, 1.35, 1.35, 5, DECK, .01)
for (a, b, w, d) in ((0, hw + .1, 2.7, .08), (-hw - .1, 0, .08, 2.7), (hw + .1, 0, .08, 2.7), (-.85, -hw - .1, .6, .08), (.85, -hw - .1, .6, .08)):
    box(a - w / 2, b - d / 2, 5.9, a + w / 2, b + d / 2, 6.0, LOG, 0); box(a - w / 2, b - d / 2, 5.45, a + w / 2, b + d / 2, 5.52, LOG, 0)
o = bpy.data.objects.new("sp", bpy.data.meshes.new("sp")); bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=.3, radius2=.22, depth=.45); bm.to_mesh(o.data); bm.free(); col.objects.link(o); o.data.materials.append(STEEL); put(o)
o.data.transform(Matrix.Rotation(-.8, 4, 'X')); o.data.transform(Matrix.Translation((.7, .7, 6.35)))
ball((.7, .95, 6.5), .18, GLOW, 8); cylz(.7, .7, 5, 6.1, .04, STEEL, 6)
cur = "rn_corral"; groups[cur] = []
n, R0 = 14, 4.6
for k in range(n):
    if k == 3: continue
    a = k / n * 2 * math.pi; logbox(R0 * math.cos(a), R0 * math.sin(a), -.2, 1.3, .09)
    if k != 2:
        a1 = (k + 1) / n * 2 * math.pi
        for h in (.55, 1.1): bar((R0 * math.cos(a), R0 * math.sin(a), h), (R0 * math.cos(a1), R0 * math.sin(a1), h), .07, LOG)
vs, fs = [], []
for i in range(33):
    a = i / 32 * 2 * math.pi; vs += [(1.6 * math.cos(a), 1.6 * math.sin(a), .03), (2.5 * math.cos(a), 2.5 * math.sin(a), .03)]
for i in range(32): fs.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
me = bpy.data.meshes.new("sc"); me.from_pydata(vs, [], fs); o = bpy.data.objects.new("sc", me); col.objects.link(o); me.materials.append(SCORCH); put(o)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/ranch.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"rn_gate": (0, -15), "rn_house": (-6, 5), "rn_trailer": (7.5, 5), "rn_tower": (9, -8), "rn_corral": (-8, -8)}
for k, (x, yv) in lay.items(): roots[k].location = (x, yv, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.5, .48, .3), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (14, -30, 16); cam.rotation_euler = (Vector((0, -2, 1)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/ranch.png"; bpy.ops.render.render(write_still=True)
