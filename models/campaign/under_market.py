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
# ================= THE UNDERNEATH, PART THREE: the pump room, the hidden market's stalls and counter, the camp's barrel, bedrolls and cart
# (buildUnderneath) as art. Blender X = u, +Y = v; origins on the floor (y) at the spots given.
# up_pumps: the pump room's machinery, origin at the room's centre (pu, cv): the two pump drums r .6 x 2.6 at (-2.6, +-2.5) with flanges and
# bolts, the two mains from them at 2.4 out to the east door (+X to +3.5), the control cabinet at (-2.9, 0) with the WHEEL on its +X face at
# 1.9 (the code's wheelAt; static here -- spin it about its X when the pumps run), the floor grate r .62 at (-1.7, 0) (U.pump.pad).
# um_stall_frame + um_stall_tarp: one market stall built for the SOUTH row (b < 0, its back to -Y): trestle 2.6 x 1.0 to .9, two iron posts at
# x +-1.2 set .4 toward the back, the tarp 2.9 x 1.8 sloping down to the back, goods on the counter. Turn by pi for the north row. The tarp is
# ONE white material: tint it the code's `tarp` / `tarp2` per stall.
# um_counter: the smuggler's counter at (cu + 6.2, cv): .8 x 3.2 to 1.1, iron top, the scale at -.6, a cash tin, a lamp.
# uc_camp: the camp's fire barrel at (cu, cv + 1.4) with its glow, origin there. uc_bedroll: one bedroll and its pillow, origin at the roll's
# centre, long along X (the code's four at their own yaw). uc_trolley: the shopping cart, origin at (tu, tv), yawed .3 by the code.
IRON = mat("UM_iron", (.23, .24, .25), .5, .5); PIPE = mat("UM_pipe", (.35, .38, .4), .45, .6); RUST = mat("UM_rust", (.35, .19, .12), .9)
RED = mat("UM_red", (.6, .12, .1), .5); PLANK = mat("UM_plank", (.29, .21, .15), .9); WHITE = mat("UM_tarp", (1, 1, 1), .8)
DARK = mat("UM_dark", (.07, .07, .08), .7); LAMP = mat("UM_lamp", (1, .63, .25), .4); BRASS = mat("UM_brass", (.6, .48, .2), .35, .8)
CLOTH = mat("UM_cloth", (.3, .33, .38), .95); CLOTH2 = mat("UM_cloth2", (.42, .3, .22), .95); CAN = mat("UM_can", (.6, .62, .64), .35, .7)
BAT = mat("UM_battery", (.85, .6, .1), .5); GREEN = mat("UM_green", (.2, .4, .25), .6)
LAMP.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1, .63, .25, 1); LAMP.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 3
WHITE.use_backface_culling = False
import random; rq = random.Random(513)
cur = "up_pumps"; groups[cur] = []
for b in (-2.5, 2.5):
    cylz(-2.6, b, 0, 2.6, .6, PIPE, 16); cylz(-2.6, b, 0, .12, .7, IRON, 16); cylz(-2.6, b, 2.48, 2.6, .66, IRON, 16)
    for k in range(10): a = k * math.pi / 5; ball((-2.6 + .66 * math.cos(a), b + .66 * math.sin(a), 2.55), .03, DARK, 4)
    bar((-2.6, b, 2.4), (3.5, b, 2.4), .25, PIPE)
    for x in (-1, 1.5): o = cylz(0, 0, -.06, .06, .31, IRON, 12); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y')); o.data.transform(Matrix.Translation((x, b, 2.4)))
    for x in (0, 2.5): box(x - .04, b - .04, 2.65, x + .04, b + .04, 4.2, IRON, 0)
box(-3.2, -.7, 0, -2.6, .7, 1.3, IRON, .02); box(-2.6, -.5, .7, -2.58, .5, 1.2, DARK, 0)
for k in range(3): ball((-2.58, -.3 + k * .3, 1.1), .04, LAMP if k == 0 else RED, 6)
o = ring((0, 0, 0), .45, .04, RED, 20, 6); o.data.transform(Matrix.Translation((-2.55, 0, 1.9)))
for k in range(4): a = k * math.pi / 4; bar((-2.55, .43 * math.cos(a), 1.9 + .43 * math.sin(a)), (-2.55, -.43 * math.cos(a), 1.9 - .43 * math.sin(a)), .02, RED)
bar((-2.9, 0, 1.3), (-2.55, 0, 1.9), .05, IRON)
cylz(-1.7, 0, 0, .03, .62, IRON, 16)
for k in range(-4, 5): box(-1.7 - .55 * math.sqrt(max(0, 1 - (k / 4.6) ** 2)), k * .12 - .015, .03, -1.7 + .55 * math.sqrt(max(0, 1 - (k / 4.6) ** 2)), k * .12 + .015, .045, DARK, 0)
cur = "um_stall_frame"; groups[cur] = []
box(-1.3, -.5, .84, 1.3, .5, .9, PLANK, .01)
for x in (-1.1, 1.1):
    for yv in (-.35, .35): bar((x, yv, 0), (x + (.15 if x < 0 else -.15) * 0, -yv * .2, .84), .03, PLANK)
for x in (-1.2, 1.2): box(x - .035, -.435, 0, x + .035, -.365, 2.6, IRON, 0)
for k in range(4):
    x = -.9 + k * .6; kind = k % 4
    if kind == 0:
        for j in range(5): cylz(x - .1 + (j % 3) * .1, -.1 + (j // 3) * .12, .9, 1.02, .045, CAN, 8)
    elif kind == 1: box(x - .17, -.17, .9, x + .17, .17, 1.08, RUST, .02)
    elif kind == 2:
        for j in range(6): box(x - .15 + (j % 3) * .1, -.08 + (j // 3) * .1, .9, x - .08 + (j % 3) * .1, -.02 + (j // 3) * .1, 1.0, BAT, 0)
    else: box(x - .17, -.17, .9, x + .17, .17, 1.2, GREEN, .02)
cur = "um_stall_tarp"; groups[cur] = []
vs = [(-1.45, .9 - .1, 2.55 + .22), (1.45, .9 - .1, 2.55 + .22), (1.45, -.9 - .1, 2.55 - .22), (-1.45, -.9 - .1, 2.55 - .22)]
o = bpy.data.objects.new("t", bpy.data.meshes.new("t")); o.data.from_pydata(vs, [], [(0, 1, 2, 3)]); col.objects.link(o); o.data.materials.append(WHITE); o.modifiers.new("s", 'SOLIDIFY').thickness = .02; put(o)
cur = "um_counter"; groups[cur] = []
box(-.4, -1.6, 0, .4, 1.6, 1.1, PLANK, .01); box(-.45, -1.65, 1.1, .45, 1.65, 1.16, IRON, .01)
for yv in (-1.2, 0, 1.2): box(-.41, yv - .02, .1, -.4, yv + .02, 1.05, DARK, 0)
cylz(0, -.6, 1.16, 1.2, .18, BRASS, 14); cylz(0, -.6, 1.2, 1.58, .03, BRASS, 6); bar((-.22, -.6, 1.55), (.22, -.6, 1.55), .015, BRASS)
for s in (-1, 1): cylz(s * .22, -.6, 1.4, 1.42, .09, BRASS, 10)
box(-.15, .4, 1.16, .15, .7, 1.26, RED, .01); cylz(.1, 1.2, 1.16, 1.4, .06, IRON, 8); ball((.1, 1.2, 1.45), .06, LAMP, 8)
cur = "uc_camp"; groups[cur] = []
cylz(0, 0, 0, .9, .4, RUST, 14); cylz(0, 0, .85, .9, .41, DARK, 14)
for k in range(8): a = k * math.pi / 4; box(.36 * math.cos(a) - .05, .36 * math.sin(a) - .05, .15, .36 * math.cos(a) + .05, .36 * math.sin(a) + .05, .3, LAMP, 0)
cylz(0, 0, .8, .86, .36, LAMP, 12)
for k in range(5): a = k * 1.3; bar((.2 * math.cos(a), .2 * math.sin(a), .82), (-.15 * math.cos(a), -.15 * math.sin(a), .95), .05, DARK)
cur = "uc_bedroll"; groups[cur] = []
box(-.95, -.4, 0, .95, .4, .1, CLOTH, .04); box(-.95, -.38, .1, .3, .38, .16, CLOTH2, .04)
o = cylz(0, 0, -.38, .38, .12, CLOTH, 10); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'X')); o.data.transform(Matrix.Translation((.6, 0, .2)))
box(-.92, -.25, .1, -.6, .25, .22, CLOTH2, .05)
cur = "uc_trolley"; groups[cur] = []
vs = [(-.45, -.3, 1.0), (.45, -.3, 1.0), (.45, .3, 1.0), (-.45, .3, 1.0), (-.35, -.25, .35), (.35, -.25, .35), (.35, .25, .35), (-.35, .25, .35)]
for (i, j) in ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)): bar(vs[i], vs[j], .012, IRON)
for k in range(1, 6):
    t = k / 6
    for (i, j, ii, jj) in ((0, 1, 4, 5), (3, 2, 7, 6)):
        a = Vector(vs[i]).lerp(Vector(vs[j]), t); b = Vector(vs[ii]).lerp(Vector(vs[jj]), t); bar(tuple(a), tuple(b), .006, IRON)
for (a, b) in ((-.35, -.25), (.35, -.25), (-.35, .25), (.35, .25)):
    bar((a, b, .35), (a, b, .1), .012, IRON); o = cylz(0, 0, -.02, .02, .08, DARK, 8); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'X')); o.data.transform(Matrix.Translation((a, b, .08)))
bar((-.45, -.3, 1.0), (-.65, -.32, 1.05), .012, IRON); bar((-.45, .3, 1.0), (-.65, .32, 1.05), .012, IRON); bar((-.65, -.32, 1.05), (-.65, .32, 1.05), .02, RED)
box(-.3, -.2, .6, .2, .2, .9, CLOTH2, .04)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/under_market.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
def inst(k, x, y, z=0, r=0, mt=None):
    c = bpy.data.objects.new(k, None); col.objects.link(c); c.location = (x, y, z); c.rotation_euler = (0, 0, r)
    for ch in roots[k].children:
        cc = ch.copy(); col.objects.link(cc); cc.parent = c
        if mt: cc.data = ch.data.copy(); cc.data.materials[0] = mt
for k in roots: roots[k].location = (0, 0, -40)
inst("up_pumps", -8, 0)
T1 = mat("prev_tarp", (.16, .29, .42), .8); T2 = mat("prev_tarp2", (.42, .16, .23), .8)
for (a, c) in ((-4, T1), (0, T2), (4, T1)): inst("um_stall_frame", 6 + a, -3.6); inst("um_stall_tarp", 6 + a, -3.6, 0, 0, c)
for (a, c) in ((-4, T2), (0, T1)): inst("um_stall_frame", 6 + a, 3.6, 0, math.pi); inst("um_stall_tarp", 6 + a, 3.6, 0, math.pi, c)
inst("um_counter", 12.2, 0); inst("uc_camp", 2, 6); inst("uc_bedroll", .5, 7, 0, .2); inst("uc_trolley", 3.5, 4.5, 0, .3)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (4, -15, 9); cam.rotation_euler = (Vector((2.5, 1, 1)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/under_market.png"; bpy.ops.render.render(write_still=True)
