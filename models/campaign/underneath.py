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
# ================= THE UNDERNEATH: buildUnderneath's tunnels and rooms (UNDER, m512) as tiles. The plan is procedural (run() and room() take
# any length), so the art is TILES at the code's sections, not a baked map. Blender +Y = along a run (the code's dir 'v'; turn by pi/2 for 'u'),
# X = across it; origins on the tunnel FLOOR (the code's y) at the run's centre line.
# un_tunnel: ONE METRE of a run, Y -.5..+.5, the code's T 3.0 wide and H 3.2 high: the stone floor (with the drain channel the code's seam
# boxes stand for), brick walls .5 thick at x +-(1.5 + .25) with mortar courses and staggered joints, a shallow brick vault under the ceiling
# slab, the pipe on its hangers along -X at 2.9, damp streaks and teal growth low on the walls. TILE it along each run (n = round(L), each
# scaled L / n along Y). The code's stone / ceil / brick boxes stay the colliders; drop their drawing. Door gaps stay gaps: skip the wall
# half of a tile there with `un_tunnel_open` (floor, vault, pipe; no walls).
# un_wall: ONE METRE of a room wall, X -.5..+.5, .5 thick, 4 high (scale Z by the room's h / 4), brick both faces, a plinth course.
# un_lamp: a wall lantern on its bracket (the code's `lamp` box at 2.1..2.5 and its `iron` cap), origin on the wall face at y, lamp out to +Y.
# un_growth: a cluster of the teal growth (a dozen glowing nubs and tendrils, 1.2 m spread, low): SCATTER it on wall feet with a seeded
# random -- never one per tile, which reads as a row of lit windows. Origin on the floor at the wall face, growth along Y and up.
# un_prop: one pit-prop set for the old dig: two posts at x +-(T / 2 - .15) to H and the cap across, origin on the floor.
BR = mat("UN_brick", (.23, .14, .12), .9); BR2 = mat("UN_brick_dark", (.18, .11, .09), .9); MORT = mat("UN_mortar", (.1, .08, .07), 1)
STONE = mat("UN_stone", (.17, .16, .15), .6); CEIL = mat("UN_ceil", (.11, .08, .07), .95); IRON = mat("UN_iron", (.23, .24, .25), .5, .5)
RUST = mat("UN_rust", (.35, .19, .12), .9); LAMP = mat("UN_lamp", (1, .63, .25), .4); GROW = mat("UN_grow", (.04, .17, .16), .6)
WOOD = mat("UN_plank", (.29, .21, .15), .9); GLASS = mat("UN_glass", (1, .7, .35), .2)
LAMP.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1, .63, .25, 1); LAMP.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 3
GROW.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (.16, 1, .82, 1); GROW.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.1
T, H = 3.0, 3.2
def brickface(x, y0, y1, z0, z1, side):
    # mortar courses every .25 and staggered joints every .5, a few mm proud of the wall face at x, facing `side`
    eps = .004 * side; z = z0 + .25
    while z < z1 - .01: box(min(x, x + eps), y0, z - .008, max(x, x + eps), y1, z + .008, MORT, 0); z += .25
    k = 0; z = z0
    while z < z1 - .01:
        yy = y0 + (.25 if k % 2 else 0)
        while yy < y1 - .01:
            if yy > y0 + .01: box(min(x, x + eps), yy - .008, z, max(x, x + eps), yy + .008, min(z + .25, z1), MORT, 0)
            yy += .5
        z += .25; k += 1
def tunnel(walls):
    box(-T / 2 - .5, -.5, -.5, T / 2 + .5, .5, 0, STONE, 0)
    box(-.15, -.5, -.003, .15, .5, .001, MORT, 0)                                                       # the drain channel
    box(-T / 2 - 1, -.5, H, T / 2 + 1, .5, H + .5, CEIL, 0)
    vs, fs = [], []
    for i in range(9):
        a = math.pi * i / 8; x = -T / 2 * math.cos(a); z = H - .35 + .32 * math.sin(a)
        vs += [(x, -.5, z), (x, .5, z)]
    for i in range(8): fs.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
    me = bpy.data.meshes.new("vault"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("vault", me); col.objects.link(o); me.materials.append(BR2); o.modifiers.new("s", 'SOLIDIFY').thickness = .08; put(o)
    if walls:
        for s in (-1, 1):
            box(s * (T / 2 + .25) - .25, -.5, 0, s * (T / 2 + .25) + .25, .5, H - .35, BR if s > 0 else BR2, 0)
            brickface(s * T / 2, -.5, .5, 0, H - .35, -s)
    o = cylz(0, 0, -.5, .5, .12, IRON, 8); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'X')); o.data.transform(Matrix.Translation((-T / 2 + .35, 0, H - .3)))
    box(-T / 2 + .3, -.02, H - .3, -T / 2 + .4, .02, H - .05, RUST, 0)
cur = "un_tunnel"; groups[cur] = []; tunnel(True)
cur = "un_tunnel_open"; groups[cur] = []; tunnel(False)
cur = "un_wall"; groups[cur] = []
box(-.5, -.25, 0, .5, .25, 4, BR, 0); box(-.5, -.27, 0, .5, .27, .3, BR2, 0)
for s in (-1, 1):
    z = .55
    while z < 4: box(-.5, s * .25 - .004 * (s < 0), z - .008, .5, s * .25 + .004 * (s > 0), z + .008, MORT, 0); z += .25
    for k, z in enumerate([.3 + i * .25 for i in range(15)]):
        for x in ((-.25, .25) if k % 2 else (0,)): box(x - .008, s * .25 - .004 * (s < 0), z, x + .008, s * .25 + .004 * (s > 0), z + .25, MORT, 0)
cur = "un_lamp"; groups[cur] = []
box(-.08, 0, 2.55, .08, .25, 2.62, IRON, 0); box(-.05, 0, 2.2, .05, .03, 2.65, IRON, 0)
box(-.11, .05, 2.1, .11, .27, 2.5, IRON, 0); box(-.09, .03, 2.13, .09, .29, 2.47, GLASS, 0); ball((0, .16, 2.3), .06, LAMP, 8)
box(-.15, .01, 2.5, .15, .31, 2.6, IRON, .01)
cur = "un_growth"; groups[cur] = []
import random; rq = random.Random(512)
for k in range(9):
    yv = (rq.random() - .5) * 1.2; z = rq.random() ** 2 * .7; r = .04 + rq.random() * .09
    o = ball((0, yv, z), r, GROW, 6); o.data.transform(Matrix.Translation((0, 0, 0)))
for k in range(5): bar((0, (rq.random() - .5), 0), (0, (rq.random() - .5) * 1.1, .2 + rq.random() * .5), .012, GROW)
cur = "un_prop"; groups[cur] = []
for s in (-1, 1): box(s * (T / 2 - .15) - .11, -.11, 0, s * (T / 2 - .15) + .11, .11, H - .25, WOOD, .01)
box(-T / 2, -.11, H - .25, T / 2, .11, H, WOOD, .01)
for s in (-1, 1): bar((s * (T / 2 - .26), 0, H - .55), (s * (T / 2 - .6), 0, H - .26), .05, WOOD)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/underneath.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
def inst(k, x, y, z=0, r=0):
    c = bpy.data.objects.new(k, None); col.objects.link(c); c.location = (x, y, z); c.rotation_euler = (0, 0, r)
    for ch in roots[k].children: cc = ch.copy(); col.objects.link(cc); cc.parent = c
for k in roots: roots[k].location = (0, 0, -40)
for j in range(10): inst("un_tunnel" if j != 6 else "un_tunnel_open", 0, j + .5)
for j in (2.5, 8.5): inst("un_lamp", 1.5, j, 0, math.pi / 2)
for (x, j) in ((-1.49, 1.6), (1.49, 4.2), (-1.49, 7.7)): inst("un_growth", x, j)
inst("un_prop", 0, 4)
for j in range(4): inst("un_wall", -2.25 - .5 - j, 10.25)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .15
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = .6; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (.6, -2.5, 1.9); cam.rotation_euler = (Vector((-.2, 6, 1.6)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/underneath.png"; bpy.ops.render.render(write_still=True)
