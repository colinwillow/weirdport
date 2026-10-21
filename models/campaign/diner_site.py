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
# ================= SAUCER JOE'S SITE: buildDiner's sign tower and the UFO museum as art. Blender X = u, +Y = v, origins on the flat's y.
# ds_tower: origin at (-12, 7): three legs from r .8 at the foot to r .25 at 16 (angles 0 / 2.09 / 4.18), the tapering ring braces every 1.6,
# the saucer on top (r 2.4 over r 1.2, .5 thick, at 16.05..16.55) with its glass dome r .9, twelve bulbs round the rim at r 2.3, and the EAT
# arrow board (3 x 1.2 at 7..8.2, u +.1..+3.1) with its point at u +3.5. The code's `steel` collider and the canvas EAT sign stay.
# ds_museum: origin at (12.5, -6), the quonset's centre: r 3.4, 10 long along Y (v -11..-1 => Y -5..+5), corrugated, ribs every 1.25, the back
# arch closed, the front arch (+Y) with its 2.2 x 2.6 door; inside, four display cases on plinths at (+-1.6, v -3 / -6), the grey in his tube at
# v -9.8, and the six clippings on the walls. The quonset's slab colliders stay; the museum sign (canvas) stays code.
STEEL = mat("DS_steel", (.55, .6, .65), .45, .6); HULL = mat("DS_hull", (.72, .75, .78), .3, .75); GLASS = mat("DS_glass", (.75, .9, 1), .1)
BULB = mat("DS_bulb", (1, .9, .6), .3); RED = mat("DS_red", (.78, .2, .17), .5); CREAM = mat("DS_cream", (1, .94, .78), .6)
QUON = mat("DS_quonset", (.6, .63, .65), .4, .55); RIB = mat("DS_rib", (.45, .48, .5), .4, .6); WOOD = mat("DS_wood", (.54, .41, .27), .7)
CASE = mat("DS_case", (.8, .92, 1), .05); PAPER = mat("DS_paper", (.9, .87, .78), .9); DARK = mat("DS_dark", (.1, .1, .12), .6)
GREY = mat("DS_grey", (.6, .66, .6), .5); CHROME = mat("DS_chrome", (.85, .87, .89), .15, .9); BLACK = mat("DS_black", (.02, .02, .03), .3)
for M, c, e in ((GLASS, (.75, .9, 1, 1), .9), (BULB, (1, .9, .6, 1), 3)):
    M.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = c; M.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = e
CASE.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = .35; QUON.use_backface_culling = False
import bmesh
def cone(r1, r2, z0, z1, M, seg=24, x=0, y=0):
    o = bpy.data.objects.new("c", bpy.data.meshes.new("c")); bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=z1 - z0)
    bmesh.ops.translate(bm, vec=(x, y, (z0 + z1) / 2), verts=bm.verts); bm.to_mesh(o.data); bm.free(); col.objects.link(o); o.data.materials.append(M)
    for p in o.data.polygons: p.use_smooth = True
    put(o); return o
cur = "ds_tower"; groups[cur] = []
for k in range(3):
    a = k * 2.09; bar((math.cos(a) * .8, math.sin(a) * .8, 0), (math.cos(a) * .25, math.sin(a) * .25, 16), .07, STEEL)
    box(math.cos(a) * .8 - .2, math.sin(a) * .8 - .2, 0, math.cos(a) * .8 + .2, math.sin(a) * .8 + .2, .15, DARK, 0)
yy = 1.5
while yy < 16:
    rr = .8 - (.55 * yy / 16)
    for k in range(3):
        a = k * 2.09; b = a + 2.09; bar((math.cos(a) * rr, math.sin(a) * rr, yy), (math.cos(b) * rr, math.sin(b) * rr, yy), .025, STEEL)
    yy += 1.6
cone(1.2, 2.4, 16.05, 16.3, HULL); cone(2.4, 1.9, 16.3, 16.55, HULL)
o = bpy.data.objects.new("d", bpy.data.meshes.new("d")); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=.9)
for v in list(bm.verts):
    if v.co.z < 0: v.co.z = 0
bmesh.ops.translate(bm, vec=(0, 0, 16.55), verts=bm.verts); bm.to_mesh(o.data); bm.free(); col.objects.link(o); o.data.materials.append(GLASS); put(o)
for k in range(12): a = k * math.pi / 6; ball((math.cos(a) * 2.3, math.sin(a) * 2.3, 16.3), .09, BULB, 6)
box(.1, -.1, 7.0, 3.1, .1, 8.2, RED, .02); box(.2, .1, 7.08, 3.0, .12, 8.12, CREAM, 0)
vs = [(3.1, -.1, 7.0 - .3), (3.1, -.1, 8.2 + .3), (4.0, -.1, 7.6), (3.1, .1, 7.0 - .3), (3.1, .1, 8.2 + .3), (4.0, .1, 7.6)]
me = bpy.data.meshes.new("pt"); me.from_pydata(vs, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate(); o = bpy.data.objects.new("pt", me); col.objects.link(o); me.materials.append(RED); put(o)
for k in range(6): ball((.4 + k * .5, .13, 8.05), .06, BULB, 6); ball((.4 + k * .5, .13, 7.15), .06, BULB, 6)
for x in (.4, 2.8): bar((x, 0, 7.0), (x * .1, 0, 6.2), .03, STEEL)
cur = "ds_museum"; groups[cur] = []
R = 3.4; NS = 18
vs, fs = [], []
for i in range(NS + 1):
    a = math.pi * i / NS
    for yv in (-5, 5): vs.append((R * math.cos(a), yv, R * math.sin(a)))
for i in range(NS): fs.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
me = bpy.data.meshes.new("q"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("q", me); col.objects.link(o); me.materials.append(QUON); put(o)
for p in me.polygons: p.use_smooth = False
for k in range(9):
    v = -5 + .5 + k * 1.25
    if v > 5: break
    for i in range(NS):
        a0 = math.pi * i / NS; a1 = math.pi * (i + 1) / NS
        bar(((R + .03) * math.cos(a0), v, (R + .03) * math.sin(a0)), ((R + .03) * math.cos(a1), v, (R + .03) * math.sin(a1)), .04, RIB)
def arch(yv, door):
    vs = [(0, yv, 0)]; fs = []
    for i in range(NS + 1): a = math.pi * i / NS; vs.append((R * math.cos(a), yv, R * math.sin(a)))
    if not door:
        for i in range(NS): fs.append((0, i + 1, i + 2))
        me = bpy.data.meshes.new("a"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("a", me); col.objects.link(o); me.materials.append(QUON); put(o)
    else:
        for s in (-1, 1):
            vv = [(s * 1.1, yv, 0), (s * R, yv, 0)] + [(R * math.cos(math.pi * i / NS), yv, R * math.sin(math.pi * i / NS)) for i in (range(0, NS // 2 + 1) if s > 0 else range(NS, NS // 2 - 1, -1))] + [(0, yv, 2.6), (s * 1.1, yv, 2.6)]
            ff = [tuple(range(len(vv)))]
            me = bpy.data.meshes.new("a"); me.from_pydata(vv, [], ff); me.validate(); o = bpy.data.objects.new("a", me); col.objects.link(o); me.materials.append(QUON); put(o)
        box(-1.1, yv - .05, 2.6, 1.1, yv + .05, 2.7, RIB, 0); box(-1.2, yv - .02, 0, -1.1, yv + .08, 2.7, RIB, 0); box(1.1, yv - .02, 0, 1.2, yv + .08, 2.7, RIB, 0)
arch(-5, False); arch(5, True)
for (a, b) in ((-1.6, 3), (1.6, 3), (-1.6, 0), (1.6, 0)):
    box(a - .45, b - .6, 0, a + .45, b + .6, .9, WOOD, .02); box(a - .425, b - .575, .9, a + .425, b + .575, 1.5, CASE, 0)
    box(a - .25, b - .2, .92, a + .25, b + .2, 1.0, PAPER if a < 0 else CHROME, 0)
cylz(0, -3.8, 0, .2, .62, DARK, 14); cylz(0, -3.8, 2.2, 2.4, .62, DARK, 14)
o = cylz(0, -3.8, .2, 2.2, .6, CASE, 14)
o2 = bpy.data.objects.new("hd", bpy.data.meshes.new("hd")); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=.25); bm.to_mesh(o2.data); bm.free(); col.objects.link(o2); o2.data.materials.append(GREY); o2.data.transform(Matrix.Scale(1.3, 4, (0, 0, 1))); o2.data.transform(Matrix.Translation((0, -3.8, 1.55))); put(o2)
cone(.15, .12, .7, 1.4, GREY, 8, 0, -3.8)
for s in (-1, 1): ball((s * .1, -3.6, 1.6), .06, BLACK, 6)
for s in (-1, 1):
    for k in range(3): box(s * (R - .95) - .02, -2.5 + k * 2.4 - .8, 1.1, s * (R - .95) + .02, -2.5 + k * 2.4 + .8, 2.0, PAPER, 0)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/diner_site.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["ds_tower"].location = (-12, 7, 0); roots["ds_museum"].location = (12.5, -6, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (6, 34, 14); cam.rotation_euler = (Vector((0, 0, 7.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/diner_site.png"; bpy.ops.render.render(write_still=True)
