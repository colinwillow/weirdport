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
# ================= THE GORGE'S STILT VILLAGE (buildGorgeVillage): the house on its platform, its boat =================
# LOCAL FRAME: origin on the platform's top at the house's centre (the code's dC, Wy); +X = +d (out from the river, toward the walk
# and the door), +Y = +b (along the river). Platform 5 (X) x 5.4 (Y), -.25..0.
import random; rq = random.Random(558)
PAINTW = mat("SV_paint_white", (1, 1, 1), .85); ROOFW = mat("SV_roof_white", (1, 1, 1), .8)
PLANKV = mat("SV_plank", (.54, .42, .28)); PLANKV2 = mat("SV_plank_dark", (.42, .32, .21)); POSTV = mat("SV_post", (.29, .23, .17)); ROPEV = mat("SV_rope", (.79, .71, .54), .9)
DOORV = mat("SV_door", (.2, .17, .14)); LAMPV = mat("SV_lamp", (1, .78, .44), .4); _l = LAMPV.node_tree.nodes["Principled BSDF"]; _l.inputs["Emission Color"].default_value = (1, .78, .44, 1); _l.inputs["Emission Strength"].default_value = 3
FISHV = mat("SV_fish", (.85, .63, .38), .5, .2); NETV = mat("SV_net", (.48, .54, .42), .9); BOATV = mat("SV_boat", (.23, .42, .54), .6); BOATI = mat("SV_boat_in", (.6, .5, .36))
cur = "sv_platform"; groups[cur] = []
for k in range(14): y = -2.7 + k * (5.4/14); box(-2.5, y + .01, -.12, 2.5, y + 5.4/14 - .01, 0, (PLANKV, PLANKV2)[k % 3 == 1])
for x in (-2.3, 0, 2.3): box(x - .1, -2.7, -.25, x + .1, 2.7, -.12, POSTV)
for (x, y) in ((-2.3, -2.5), (2.3, -2.5), (-2.3, 2.5), (2.3, 2.5)): box(x - .11, y - .11, -.6, x + .11, y + .11, .1, POSTV)
# ---- the walls: 3.2 (X) x 3.6 (Y), 2.6 tall, centred at x -.4; weatherboard; ONE white material (tint wall_a / b / c)
cur = "sv_house_wall"; groups[cur] = []
x0, x1, y0, y1 = -2.0, 1.2, -1.8, 1.8
for k in range(10):
    z = k * .26; o = .012 * (k % 2)
    box(x0 - o, y0 - o, z, x1 + o, y0 + .06 - o, z + .27, PAINTW); box(x0 - o, y1 - .06 + o, z, x1 + o, y1 + o, z + .27, PAINTW)
    box(x0 - o, y0, z, x0 + .06 - o, y1, z + .27, PAINTW); box(x1 - .06 + o, y0, z, x1 + o, y1, z + .27, PAINTW)
# ---- the roof: a hip roof (the code's 4-sided cone r 2.85 = a 4.03 m square), eaves at 2.6, ridge point at 4.1; tint roof_a / b / c
cur = "sv_house_roof"; groups[cur] = []
h = 2.85 / math.sqrt(2); cx = -.4
vs = [(cx - h, -h, 2.6), (cx + h, -h, 2.6), (cx + h, h, 2.6), (cx - h, h, 2.6), (cx, 0, 4.1)]
me = bpy.data.meshes.new("roof"); me.from_pydata(vs, [], [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (3, 2, 1, 0)]); o = bpy.data.objects.new("roof", me); col.objects.link(o); me.materials.append(ROOFW)
o.modifiers.new("s", 'SOLIDIFY').thickness = .08; put(o)
for (a, b) in ((0, 4), (1, 4), (2, 4), (3, 4)): bar(vs[a], vs[b], .05, POSTV)
# ---- the rest: door (+X, at y +.6), window (-X, over the water), lamp, the fish rack and its fish, the net, a crate and a coil
cur = "sv_house_trim"; groups[cur] = []
for (x, y) in ((-2.0, -1.8), (1.2, -1.8), (-2.0, 1.8), (1.2, 1.8)): box(x - .07, y - .07, 0, x + .07, y + .07, 2.62, PLANKV2)
box(1.2, .15, 0, 1.25, 1.05, 2.05, DOORV); box(1.2, .1, 2.05, 1.27, 1.1, 2.12, PLANKV2); ball((1.27, .25, 1.0), .03, FMET, 5)
box(-2.05, -.6, 1.1, -2.0, .6, 1.8, mat("SV_glass", (.14, .2, .24), .15)); box(-2.08, -.66, 1.06, -2.0, .66, 1.1, PLANKV2); box(-2.08, -.66, 1.8, -2.0, .66, 1.84, PLANKV2)
for s in (-1, 1): box(-2.1, s*.62 - .32 if s > 0 else s*.62 - .0, 1.1, -2.07, s*.62 + .0 if s > 0 else s*.62 + .32, 1.8, PLANKV2)
bar((1.22, -.3, 2.45), (1.35, -.3, 2.45), .02, POSTV); ball((1.35, -.3, 2.25), .14, LAMPV, 8); box(1.3, -.35, 2.38, 1.4, -.25, 2.42, DARK)
for y in (-2.1, -1.1): box(1.86, y - .04, 0, 1.94, y + .04, 1.6, POSTV)
bar((1.9, -2.2, 1.57), (1.9, -1.0, 1.57), .025, POSTV)
for f in range(4): yy = -2.0 + f * .26; bar((1.9, yy, 1.5), (1.9, yy, 1.12), .045, FISHV); bar((1.9, yy, 1.12), (1.9, yy + .04, 1.06), .03, FISHV)
vs, fs = [], []
for i in range(5):
    for j in range(4): vs.append((-2.55 + .03 * math.sin(i + j), .4 + .4 * i, .0 + .4 * j - .05 * math.sin(i * 1.3)))
for i in range(4):
    for j in range(3): a = i*4 + j; fs.append((a, a + 4, a + 5, a + 1))
me = bpy.data.meshes.new("net"); me.from_pydata(vs, [], fs); o = bpy.data.objects.new("net", me); col.objects.link(o); me.materials.append(NETV); o.modifiers.new("s", 'SOLIDIFY').thickness = .02; put(o)
bar((-2.55, .4, 1.25), (-2.55, 2.0, 1.25), .02, POSTV)
box(.3, -2.3, 0, .9, -1.8, .45, PLANKV2)
o = None
for t in range(3): cylz(1.7, 1.9, t * .05, t * .05 + .05, .3 - t * .03, ROPEV, 12)
# ---- the boat tied under: 1.3 x 3.6, origin on the water at its centre, a painted hull, thwarts, oars
cur = "sv_boat"; groups[cur] = []
prof = []
vs, fs = [], []; N = 8
for i in range(N + 1):
    y = -1.8 + 3.6 * i / N; w = .65 * math.sin(math.pi * (i + .3) / (N + .6)) ** .6
    vs += [(-w, y, .3), (-w * .55, y, -.15), (w * .55, y, -.15), (w, y, .3)]
for i in range(N):
    a = i * 4; fs += [(a, a + 4, a + 5, a + 1), (a + 1, a + 5, a + 6, a + 2), (a + 2, a + 6, a + 7, a + 3)]
fs += [(0, 1, 2, 3)[::-1], (N*4, N*4 + 1, N*4 + 2, N*4 + 3)]
me = bpy.data.meshes.new("hull"); me.from_pydata(vs, [], fs); o = bpy.data.objects.new("hull", me); col.objects.link(o); me.materials.append(BOATV); o.modifiers.new("s", 'SOLIDIFY').thickness = .04; put(o)
for y in (-.7, .5): box(-.5, y - .1, .12, .5, y + .1, .17, BOATI)
for s in (-1, 1): bar((s*.35, -.3, .2), (s*.2, 1.4, .25), .025, BOATI)
bar((0, 1.75, .3), (0, 2.6, 3.2), .012, ROPEV)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/stilt_village.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"sv_platform": (0, 0, 0, 1), "sv_house_wall": (0, 0, 0, 1), "sv_house_roof": (0, 0, 0, 1), "sv_house_trim": (0, 0, 0, 1), "sv_boat": (-4.5, -3.5, 0, .15)}
for k, (x, y, r, z) in lay.items(): roots[k].location = (x, y, z); roots[k].rotation_euler = (0, 0, r)
for c in roots["sv_house_wall"].children: c.data.materials[0] = mat("pw", (.72, .66, .53), .85)
for c in roots["sv_house_roof"].children: c.data.materials[0] = mat("pr", (.35, .48, .54), .8)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.2, .35, .4), .3))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-9, -8, 5.5); cam.rotation_euler = (Vector((-.5, 0, 1.8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/stilt_village.png"; bpy.ops.render.render(write_still=True)
