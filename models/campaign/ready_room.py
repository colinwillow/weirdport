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

# ======== ready_room: Hollow Creek's pilots' bar (buildReadyRoom), at the code's numbers. Blender X = the frame's u, +Y = v (away
# from the road); origin at (0, 0) on the flat's y unless said. The room is u -5.5..5.5, v -2..6, walls 3.2, door 2 m in the -v wall.
#   rr_shell   walls (board and batten), the door frame, two windows with their beer neons, the gable roof, the porch deck with its
#              posts and tin roof, the dark bar under the roof neon (the sign itself stays the code's canvas)
#   rr_inside  the bar along the back with its brass rail, two shelves of bottles, the propeller on the back wall, five stools,
#              the pool table, two round tables, the jukebox, three pendant lamps
#   rr_tank    the drop-tank sign by the road: origin (-6, -11) on its own ground, legs, the olive tank and its nose to +X
#   rr_picnic  a picnic table, origin (7.5, -4.5) on its ground, unturned (the code turns it .3)
#   rr_sock    the windsock, origin (8.5, 8) on its ground: a 5 m pole, the sock flying +X at 4.8
#   rr_pickup  the red pickup, origin (5, -7.5) on its ground, nose -Y (the cab end), unturned (the code turns it .15)
WALL = mat("RR_wall", (.42, .31, .22)); WALL2 = mat("RR_batten", (.33, .25, .18)); TIN = mat("RR_tin", (.35, .37, .39), .5, .45); FLOOR = mat("RR_floor", (.23, .18, .14))
DECK = mat("RR_deck", (.48, .39, .28)); BAR = mat("RR_bar", (.29, .18, .12), .6); TOP = mat("RR_bartop", (.16, .1, .07), .35); WOODL = mat("RR_wood", (.54, .42, .27))
GLS = mat("RR_glass", (.1, .16, .19), .15, .3); STEEL = mat("RR_steel", (.54, .59, .63), .4, .55); BRASS = mat("RR_brass", (.78, .6, .25), .3, .85)
FELT = mat("RR_felt", (.12, .35, .23), 1); REDV = mat("RR_red", (.72, .23, .18), .5); DARKR = mat("RR_dark", (.12, .11, .1), .6); OLIVE = mat("RR_olive", (.35, .42, .29), .6, .2)
BOT = mat("RR_bottle", (.16, .42, .23), .15); AMB = mat("RR_amber", (.54, .29, .1), .15); CREAM = mat("RR_cream", (.9, .88, .84), .6)
def emis(name, rgb, k):
    m = mat(name, rgb, .4); b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = k; return m
GLOW = emis("RR_glow", (1, .82, .54), 2.0); BEER = emis("RR_beer", (1, .23, .35), 2.5); JUKE = emis("RR_juke", (1, .48, .23), 1.6)
W2, V0, V1, HH, T = 5.5, -2., 6., 3.2, .2
cur = "rr_shell"; groups[cur] = []
box(-W2 - .1, V0 - .1, -.3, W2 + .1, V1 + .1, .02, FLOOR)                                 # floor slab
box(-W2, V1 - T/2, 0, W2, V1 + T/2, HH, WALL)
for s in (-1, 1): box(s*W2 - T/2, V0, 0, s*W2 + T/2, V1, HH, WALL)
for s in (-1, 1): box(min(s*1, s*W2), V0 - T/2, 0, max(s*1, s*W2), V0 + T/2, HH, WALL)
box(-1, V0 - T/2, 2.3, 1, V0 + T/2, HH, WALL)
# battens on every outside face (a board-and-batten skin, not a pattern in a tile)
for k in range(23):
    x = -W2 + .25 + k*.5
    box(x - .03, V1 + T/2, .05, x + .03, V1 + T/2 + .04, HH, WALL2)
    if abs(x) > 1.1 and not any(abs(x - s*3.3) < 1.15 for s in (-1, 1)): box(x - .03, V0 - T/2 - .04, .05, x + .03, V0 - T/2, HH, WALL2)
    elif abs(x) > 1.1: box(x - .03, V0 - T/2 - .04, .05, x + .03, V0 - T/2, 1.05, WALL2); box(x - .03, V0 - T/2 - .04, 2.25, x + .03, V0 - T/2, HH, WALL2)
for k in range(16):
    y = V0 + .25 + k*.5
    for s in (-1, 1): box(s*(W2 + T/2) - .02*(s < 0) - (0 if s > 0 else .02), y - .03, .05, s*(W2 + T/2) + (.04 if s > 0 else 0), y + .03, HH, WALL2) if s > 0 else box(-W2 - T/2 - .04, y - .03, .05, -W2 - T/2, y + .03, HH, WALL2)
# the door frame and a sill
for s in (-1, 1): box(s*1 - .07, V0 - .14, 0, s*1 + .07, V0 + .14, 2.36, WOODL)
box(-1.07, V0 - .14, 2.3, 1.07, V0 + .14, 2.42, WOODL)
# the windows, framed, with a beer neon in each
for s in (-1, 1):
    box(s*3.3 - 1.15, V0 - .16, 1.05, s*3.3 + 1.15, V0 - .1, 2.25, WOODL)
    box(s*3.3 - 1.08, V0 - .17, 1.1, s*3.3 + 1.08, V0 - .15, 2.2, GLS)
    box(s*3.3 - .45, V0 - .2, 1.6, s*3.3 + .45, V0 - .18, 1.9, BEER)
    box(s*3.3 - 1.2, V0 - .3, 1.0, s*3.3 + 1.2, V0 - .1, 1.06, WOODL)                       # the sill
# the gable roof over the code's flat .4 cap: eaves at HH + .1, ridge at HH + .65 along u at v 2, overhangs
mid = (V0 + V1)/2
for s in (-1, 1):
    a, b = (V0 - .45, mid) if s < 0 else (mid, V1 + .45)
    ze = HH + .07
    pts = [(-W2 - .4, a, ze if s < 0 else HH + .62), (W2 + .4, a, ze if s < 0 else HH + .62), (W2 + .4, b, HH + .62 if s < 0 else ze), (-W2 - .4, b, HH + .62 if s < 0 else ze)]
    quadbox(pts, .08, TIN)
    for k in range(12):          # standing seams
        x = -W2 - .1 + k*1.0
        p0 = (x, a, (ze if s < 0 else HH + .62) + .08); p1 = (x, b, (HH + .62 if s < 0 else ze) + .08); bar(p0, p1, .02, TIN)
for s in (-1, 1):                # the gable ends
    vs = [(s*(W2 + .02), V0, HH), (s*(W2 + .02), V1, HH), (s*(W2 + .02), mid, HH + .6)]
    me = bpy.data.meshes.new("g"); me.from_pydata(vs, [], [(0, 1, 2) if s > 0 else (2, 1, 0)]); o = bpy.data.objects.new("g", me); col.objects.link(o); me.materials.append(WALL); put(o)
# the porch: deck 11 x 1.6 at v -2.9, two posts at u +-5.3 v -3.6, a tin lean-to falling to -v
box(-W2, V0 - 1.7, -.3, W2, V0 - .1, .02, DECK)
for k in range(8): x = -W2 + .7 + k*1.4; box(x - .02, V0 - 1.72, -.01, x + .02, V0 - .1, .025, DARKR)
for s in (-1, 1): box(s*(W2 - .2) - .06, V0 - 1.66, 0, s*(W2 - .2) + .06, V0 - 1.54, 2.55, WOODL)
box(-W2, V0 - 1.66, 2.45, W2, V0 - 1.54, 2.55, WOODL)
quadbox([(-W2 - .15, V0 - 1.85, 2.5), (W2 + .15, V0 - 1.85, 2.5), (W2 + .15, V0 + .05, 2.78), (-W2 - .15, V0 + .05, 2.78)], .05, TIN)
box(-2.2, V0 + .24, HH + .3, 2.2, V0 + .36, HH + .7, DARKR)                                 # the neon's backer (the sign stays code)
for x in (-1.8, 1.8): box(x - .04, V0 + .26, HH + .1, x + .04, V0 + .34, HH + .7, STEEL)

cur = "rr_inside"; groups[cur] = []
vb = V1 - 1.6
box(-3.5, vb - .3, 0, 3.5, vb + .3, 1.05, BAR)
for k in range(15): x = -3.4 + k*.486; box(x - .02, vb - .32, .1, x + .02, vb - .3, 1.0, TOP)
box(-3.6, vb - .38, 1.05, 3.6, vb + .38, 1.12, TOP)
bar((-3.4, vb - .5, .2), (3.4, vb - .5, .2), .025, BRASS)                                   # the foot rail
for x in (-3, 0, 3): bar((x, vb - .3, .2), (x, vb - .5, .2), .02, BRASS)
for z in (1.3, 1.9): box(-3.5, V1 - .4, z, 3.5, V1 - .1, z + .06, WOODL)
for x in (-3.45, 3.45): box(x - .03, V1 - .4, 1.0, x + .03, V1 - .1, 2.4, WOODL)
rr = random.Random(837)
for k in range(22):
    x = -3.3 + k*.31; sh = 1.36 if k % 2 else 1.96; h = .3 + rr.random()*.12; m = BOT if rr.random() < .5 else AMB
    cylz(x, V1 - .25, sh, sh + h*.7, .05, m, 8); cylz(x, V1 - .25, sh + h*.7, sh + h, .018, m, 6)
# the propeller on the back wall: hub and two blades, crossed at .4
cylz(0, V1 - .14, 2.6, 2.7, .14, STEEL, 12)
import mathutils
for ang in (.4, .4 + math.pi):
    c, s_ = math.cos(ang), math.sin(ang)
    quadbox([(c*.12 - s_*.07, V1 - .16, 2.65 + s_*.12 + c*.07), (c*1.1 - s_*.05, V1 - .16, 2.65 + s_*1.1 + c*.05), (c*1.1 + s_*.05, V1 - .16, 2.65 + s_*1.1 - c*.05), (c*.12 + s_*.07, V1 - .16, 2.65 + s_*.12 - c*.07)], .03, WOODL)
for k in range(5):
    x = -2.8 + k*1.4
    cylz(x, V1 - 2.5, .72, .78, .2, REDV, 12); cylz(x, V1 - 2.5, 0, .72, .03, STEEL, 6); cylz(x, V1 - 2.5, 0, .03, .18, STEEL, 10)
    bar((x - .14, V1 - 2.5, .3), (x + .14, V1 - 2.5, .3), .012, STEEL)
# the pool table at (-3, 1.2): 2.3 x 1.3, felt at .82, rails, six legs, two cues and a rack
box(-3 - 1.05, 1.2 - .55, .55, -3 + 1.05, 1.2 + .55, .82, BAR)
box(-3 - 1.05, 1.2 - .55, .82, -3 + 1.05, 1.2 + .55, .84, FELT)
for (x0, y0, x1, y1) in ((-4.15, .55, -1.85, .65), (-4.15, 1.75, -1.85, 1.85), (-4.15, .55, -4.05, 1.85), (-1.95, .55, -1.85, 1.85)): box(x0, y0, .78, x1, y1, .9, BAR)
for x in (-4, -3, -2):
    for y in (.68, 1.72): box(x - .07, y - .07, 0, x + .07, y + .07, .56, BAR)
bar((-3.6, 1.0, .85), (-2.2, 1.35, .86), .012, WOODL); bar((-3.3, 1.5, .85), (-2.0, 1.2, .86), .012, WOODL)
for k in range(6): ball((-3.6 + k*.12, 1.3 + (k % 2)*.08, .875), .03, REDV if k % 2 else CREAM, 6)
for (u, v) in ((2.4, .4), (3.9, 2.2)):
    cylz(u, v, .72, .77, .45, TOP, 14); cylz(u, v, 0, .72, .06, DARKR, 6); cylz(u, v, 0, .04, .3, DARKR, 10)
    for a in range(3):
        aa = a*2.1 + u; cylz(u + math.cos(aa)*.7, v + math.sin(aa)*.7, .44, .48, .2, REDV, 10); cylz(u + math.cos(aa)*.7, v + math.sin(aa)*.7, 0, .44, .025, STEEL, 6)
    cylz(u + .1, v, .77, .92, .035, AMB, 8)
# the jukebox at (5, 5.4): a body, a lit arch, a dark cap
ju, jv = W2 - .5, V1 - .6
box(ju - .35, jv - .27, 0, ju + .35, jv + .27, 1.2, BAR)
box(ju - .3, jv - .29, .25, ju + .3, jv - .27, 1.1, JUKE)
cylz(ju, jv, 1.2, 1.6, .35, JUKE, 14); box(ju - .36, jv - .28, 1.6, ju + .36, jv + .28, 1.75, DARKR)
for u in (-3, 0, 3):
    cylz(u, 2.5, HH - .3, HH, .008, DARKR, 4); cylz(u, 2.5, HH - .38, HH - .28, .18, DARKR, 10); ball((u, 2.5, HH - .38), .09, GLOW, 8)

cur = "rr_tank"; groups[cur] = []
for s in (-1, 1): box(s*.9 - .06, -.06, 0, s*.9 + .06, .06, 1.6, STEEL); bar((s*.9, 0, 1.6), (s*.9, 0, 1.9), .05, STEEL)
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=.42, radius2=.42, depth=2.8)
me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("t", me); col.objects.link(o); me.materials.append(OLIVE)
me.transform(Matrix.Translation((0, 0, 1.9)) @ Matrix.Rotation(math.pi/2, 4, 'Y')); [setattr(p, 'use_smooth', True) for p in me.polygons]; put(o)
for s in (-1, 1):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=.42, radius2=.04, depth=.6)
    me = bpy.data.meshes.new("n"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("n", me); col.objects.link(o); me.materials.append(OLIVE)
    me.transform(Matrix.Translation((s*1.7, 0, 1.9)) @ Matrix.Rotation(s*math.pi/2, 4, 'Y')); put(o)
for fy in (-1, 1): quadbox([(-1.9, fy*.0 - .02, 1.9), (-1.4, -.02, 1.9), (-1.6, -.02, 1.9 + fy*.55), (-1.95, -.02, 1.9 + fy*.55)], .04, OLIVE) if fy > 0 else quadbox([(-1.95, -.02, 1.35), (-1.6, -.02, 1.35), (-1.4, -.02, 1.9), (-1.9, -.02, 1.9)], .04, OLIVE)
box(-.3, -.43, 1.75, .3, -.41, 2.05, CREAM)                                                 # a stencil panel
cur = "rr_picnic"; groups[cur] = []
for k in range(4): box(-.9, -.4 + k*.2 + .01, .72, .9, -.4 + k*.2 + .19, .78, WOODL)
for s in (-1, 1):
    for k in range(2): box(-.9, s*.6 - .125 + k*.13, .4, .9, s*.6 - .125 + k*.13 + .11, .46, WOODL)
    bar((s*.65, -.7, 0), (s*.65, .25, .72), .04, WOODL); bar((s*.65, .7, 0), (s*.65, -.25, .72), .04, WOODL)
    bar((s*.65, -.75, .4), (s*.65, .75, .4), .035, WOODL)
cur = "rr_sock"; groups[cur] = []
cylz(0, 0, -.2, 5.0, .05, STEEL, 8); ball((0, 0, 5.02), .06, REDV, 6)
bar((0, 0, 4.8), (.12, 0, 4.8), .03, STEEL)
for k in range(5):
    x0, x1 = .12 + k*.24, .12 + (k + 1)*.24; r0, r1 = .25 - k*.03, .25 - (k + 1)*.03; z0, z1 = 4.8 - k*.06, 4.8 - (k + 1)*.06
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=10, radius1=r0, radius2=r1, depth=.24)
    me = bpy.data.meshes.new("s"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("s", me); col.objects.link(o); me.materials.append(REDV if k % 2 == 0 else CREAM)
    me.transform(Matrix.Translation(((x0 + x1)/2, 0, (z0 + z1)/2)) @ Matrix.Rotation(math.pi/2 + .25, 4, 'Y')); put(o)
cur = "rr_pickup"; groups[cur] = []
box(-1, -2.4, .4, 1, 2.4, 1.2, REDV, bev=.05)
box(-.9, -1.55, 1.2, .9, .35, 1.75, REDV, bev=.04)                                           # the cab
box(-.91, -1.0, 1.25, .91, .2, 1.7, GLS); box(-.86, -1.57, 1.25, .86, -1.5, 1.7, GLS); box(-.86, .3, 1.3, .86, .37, 1.68, GLS)
box(-.85, .5, 1.12, .85, 2.3, 1.22, DARKR)                                                   # the bed floor seen from above
box(-1.03, -2.45, .45, 1.03, -2.38, .7, STEEL); box(-1.03, 2.38, .45, 1.03, 2.45, .65, STEEL)  # bumpers
for s in (-1, 1): box(s*.7 - .15, -2.42, .85, s*.7 + .15, -2.4, 1.0, GLOW)
for a in (-.9, .9):
    for b in (-1.6, 1.6):
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=.38, radius2=.38, depth=.3)
        me = bpy.data.meshes.new("w"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("w", me); col.objects.link(o); me.materials.append(DARKR)
        me.transform(Matrix.Translation((a*1.02, b, .38)) @ Matrix.Rotation(math.pi/2, 4, 'Y')); put(o)
        cylz(a*1.18, b, .26, .5, .0001, STEEL, 4) if False else None
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=.2, radius2=.2, depth=.02)
        me = bpy.data.meshes.new("h"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("h", me); col.objects.link(o); me.materials.append(STEEL)
        me.transform(Matrix.Translation((a*1.18, b, .38)) @ Matrix.Rotation(math.pi/2, 4, 'Y')); put(o)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/ready_room.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"rr_shell": (0, 0, 0), "rr_inside": (0, 0, 0), "rr_tank": (-6, -11, 0), "rr_picnic": (7.5, -4.5, 0), "rr_sock": (8.5, 8, 0), "rr_pickup": (5, -7.5, 0)}
for k, v in lay.items(): roots[k].location = v
roots["rr_picnic"].rotation_euler = (0, 0, .3); roots["rr_pickup"].rotation_euler = (0, 0, .15)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (14, -20, 9); cam.rotation_euler = (Vector((0, -2, 1.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/ready_room.png"; bpy.ops.render.render(write_still=True)
