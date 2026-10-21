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

# ======== mill_shed: Hollow Creek Lumber's shed (buildMill), at the code's numbers. Blender X = the frame's u, +Y = v; the shed
# pieces' origin is the FRAME's origin on the flat's y (place at (0, 0, y)). SHED w 24 d 14 at v -8 (v -15..-1), walls 9, ridge 3,
# upper floor 4.5. Openings as the code's walls leave them: the front (v -1) has the conveyor slot u -9.4..-6.6 z 2.8..6.4, the big
# door u -4..4 to 5.4, the flume slot u 5.2..6.8 z 4.2..6.9; the right wall (u 12) has the slot v -12.5..-10.5 z 4.3..7.1.
#   hm_shed    the corrugated walls round those openings, the plinth, rust streaks off the eaves, the roof with its seams and
#              overhang, the gables, the door's track, the sign's board (the sign itself stays the code's canvas)
#   hm_loft    the upper floor (v -15..-7, top 4.5), its rail with the code's gaps, the 14-riser stair at u 10
#   hm_lumber5 / hm_lumber4  a sawn-lumber stack on three bearers, 5 or 4 layers with stickers; origin on the ground at (13, 5) / (17.5, 9.5)
#   hm_stump   the chopping stump with the axe in it, origin on the ground at (10.5, 12)
TIN = mat("HM_tin", (.6, .63, .64), .4, .55); RIB = mat("HM_rib", (.52, .55, .57), .45, .55); ROOFT = mat("HM_roof", (.5, .52, .54), .5, .5)
CONC = mat("HM_conc", (.54, .53, .49), 1); STREAK = mat("HM_streak", (.48, .29, .16), .9); BOARD = mat("HM_board", (.16, .23, .16)); STL = mat("HM_steel", (.42, .46, .5), .45, .5)
PLK = mat("HM_plank", (.48, .35, .23)); POST = mat("HM_post", (.29, .21, .15)); CUT = mat("HM_cut", (.78, .63, .44), .9); CUT2 = mat("HM_cut_end", (.85, .72, .52), .9)
LOGM = mat("HM_log", (.42, .29, .18), 1); RED = mat("HM_red", (.62, .16, .12), .6)
W, D, SV, H, RG, MZ = 24., 14., -8., 9., 3., 4.5
UW, V0, V1 = W/2, SV - D/2, SV + D/2
cur = "hm_shed"; groups[cur] = []
def wallU(a, b, v, z0, z1, ribs=True, out=1):      # a wall along u at v, from u a..b, z0..z1; ribs on its outside (out = +1 for +v)
    box(a, v - .1, z0, b, v + .1, z1, TIN)
    if ribs:
        u = a + .3
        while u < b - .1: box(u - .035, v + out*.1 - (.04 if out < 0 else 0), max(z0, .4), u + .035, v + out*.1 + (.04 if out > 0 else 0), z1, RIB); u += .6
def wallV(a, b, u, z0, z1, out=1):
    box(u - .1, a, z0, u + .1, b, z1, TIN)
    v = a + .3
    while v < b - .1: box(u + out*.1 - (.04 if out < 0 else 0), v - .035, max(z0, .4), u + out*.1 + (.04 if out > 0 else 0), v + .035, z1, RIB); v += .6
wallU(-UW, UW, V0, 0, H, out=-1)
wallV(V0, V1, -UW, 0, H, out=-1)
for (a, b, z0, z1) in ((V0, V0 + 2.5, 0, H), (V0 + 2.5, V0 + 4.5, 0, MZ - .2), (V0 + 2.5, V0 + 4.5, MZ + 2.6, H), (V0 + 4.5, V1, 0, H)): wallV(a, b, UW, z0, z1, out=1)
for (a, b, z0, z1) in ((-UW, -9.4, 0, H), (-9.4, -6.6, 0, 2.8), (-9.4, -6.6, 6.4, H), (-6.6, -4, 0, H), (-4, 4, 5.4, H), (4, 5.2, 0, H), (5.2, 6.8, 0, MZ - .3), (5.2, 6.8, MZ + 2.4, H), (6.8, UW, 0, H)):
    wallU(a, b, V1, z0, z1, out=1)
# the gable ends (u = +-12), closed triangles over the walls, ribbed
for s in (-1, 1):
    vs = [(s*(UW + .02), V0, H), (s*(UW + .02), V1, H), (s*(UW + .02), SV, H + RG)]
    vs += [(x - s*.2 if i < 3 else x, y, z) for i, (x, y, z) in enumerate(vs)]
    vs = vs[:3] + [(s*(UW - .18), y, z) for (x, y, z) in vs[:3]]
    me = bpy.data.meshes.new("g"); me.from_pydata(vs, [], [(0, 1, 2) if s > 0 else (2, 1, 0), (5, 4, 3) if s > 0 else (3, 4, 5), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate()
    o = bpy.data.objects.new("g", me); col.objects.link(o); me.materials.append(TIN); put(o)
    v = V0 + .3
    while v < V1 - .1:
        zt = H + RG*(1 - abs(v - SV)/(D/2)); box(s*(UW + .02) - .02 + (.02 if s > 0 else -.02), v - .035, H, s*(UW + .02) + .02 + (.02 if s > 0 else -.02), v + .035, zt - .05, RIB); v += .6
# the roof: two slopes off the ridge along u, overhanging .6 at the eaves and .5 at the gables, standing seams
for s in (-1, 1):
    ve = (V0 - .6) if s < 0 else (V1 + .6); ze = H - .6*RG/(D/2)
    pts = [(-UW - .5, ve, ze), (UW + .5, ve, ze), (UW + .5, SV, H + RG), (-UW - .5, SV, H + RG)]
    if s > 0: pts = [pts[1], pts[0], pts[3], pts[2]]
    quadbox(pts, .12, ROOFT)
    u = -UW
    while u <= UW + .01: bar((u, ve, ze + .12), (u, SV, H + RG + .12), .025, RIB); u += 1.2
box(-UW - .5, SV - .15, H + RG + .05, UW + .5, SV + .15, H + RG + .25, RIB)                   # the ridge cap
# the plinth: concrete where it meets the ground, broken at the big door
box(-UW - .27, V0 - .27, -.2, UW + .27, V0 - .1, .45, CONC); box(-UW - .27, V0 - .27, -.2, -UW - .1, V1 + .27, .45, CONC); box(UW + .1, V0 - .27, -.2, UW + .27, V1 + .27, .45, CONC)
for (a, b) in ((-UW - .27, -9.4), (-6.6, -4), (4, 5.2), (6.8, UW + .27)): box(a, V1 + .1, -.2, b, V1 + .27, .45, CONC)
for (a, b) in ((-9.4, -6.6), (5.2, 6.8)): box(a, V1 + .1, -.2, b, V1 + .27, .45, CONC)
# rust streaks off the eaves, at the code's five places (and the gable ends)
for (u, v, a2) in ((-UW - .15, V0 + 3, 0), (-UW - .15, SV + 2, 0), (-6, V0 - .15, 1), (7, V0 - .15, 1), (UW + .15, V1 - 2, 0), (-1.5, V1 + .15, 1), (9, V1 + .15, 1)):
    for k, (dz, wid) in enumerate(((3.2, .5), (2.2, .25), (1.4, .15))):
        off = (k - 1)*.32
        if a2: box(u + off - wid/2, v - .01, H - dz, u + off + wid/2, v + .01, H - .2, STREAK)
        else: box(u - .01, v + off - wid/2, H - dz, u + .01, v + off + wid/2, H - .2, STREAK)
# the big door's frame and its track; the sign's board
for x in (-4, 4): box(x - .12, V1 - .12, 0, x + .12, V1 + .2, 5.5, STL)
box(-4.12, V1 - .12, 5.4, 4.12, V1 + .2, 5.6, STL); box(-12, V1 + .12, 5.65, 12, V1 + .22, 5.8, STL)
box(-3.8, V1 + .1, 5.7, 3.8, V1 + .18, 7.1, BOARD)
for (a, b, z0, z1) in ((-9.4, -6.6, 2.8, 6.4), (5.2, 6.8, MZ - .3, MZ + 2.4)):                 # slot frames
    for x in (a, b): box(x - .06, V1 - .1, z0, x + .06, V1 + .16, z1, STL)
    for z in (z0, z1): box(a, V1 - .1, z - .06, b, V1 + .16, z + .06, STL)

cur = "hm_loft"; groups[cur] = []
MV = SV + 1
for k in range(int((W - .4)/.3)):
    x0 = -UW + .2 + k*.3; box(x0 + .005, V0 + .1, MZ - .06, x0 + .295, MV, MZ, PLK)
box(-UW + .2, V0 + .1, MZ - .3, UW - .2, MV, MZ - .06, POST)
for x in (-8, -2, 4): box(x - .15, MV - .5, 0, x + .15, MV - .2, MZ - .3, POST)               # posts under its edge
box(-UW + .2, MV - .5, MZ - .55, UW - .2, MV - .2, MZ - .3, POST)                            # the edge beam
for (a, b) in ((-UW + .2, -8.8), (-7.2, 5.3), (6.7, 8.6)):
    n = max(2, int((b - a)/1.2) + 1)
    for k in range(n): x = a + (b - a)*k/(n - 1); box(x - .04, MV - .08, MZ, x + .04, MV, MZ + 1.0, STL)
    box(a, MV - .09, MZ + .92, b, MV + .01, MZ + 1.0, STL); box(a, MV - .07, MZ + .47, b, MV - .01, MZ + .53, STL)
for k in range(14):
    vc = MV + (13 - k)*.4 + .2; z1 = (k + 1)*MZ/14
    box(9.1, vc - .2, z1 - .06, 10.9, vc + .2, z1, PLK)
for s in (-1, 1):
    x = 10 + s*.95
    quadbox([(x - .04, MV + 5.6, 0), (x + .04, MV + 5.6, 0), (x + .04, MV, MZ - .3), (x - .04, MV, MZ - .3)], .3, POST)
    for k in range(4): y = MV + .3 + k*1.6; box(x - .03, y - .03, MZ*(1 - (y - MV)/5.6) + .1, x + .03, y + .03, MZ*(1 - (y - MV)/5.6) + 1.0, STL)
    bar((x, MV + 5.6, .9), (x, MV, MZ + 1.0), .025, STL)

for nm, n in (("hm_lumber5", 5), ("hm_lumber4", 4)):
    cur = nm; groups[cur] = []
    for s2 in (-1.6, 0, 1.6): box(s2 - .1, -1.2, 0, s2 + .1, 1.2, .18, LOGM)
    for l in range(n):
        z0 = .18 + l*.34
        for k in range(10):
            x0 = -2.1 + k*.42; box(x0 + .005, -1.1, z0, x0 + .415, 1.1, z0 + .28, CUT if (k + l) % 3 else CUT2)
        if l < n - 1:
            for s2 in (-1.6, 0, 1.6): box(s2 - .05, -1.15, z0 + .28, s2 + .05, 1.15, z0 + .34, POST)
cur = "hm_stump"; groups[cur] = []
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=.5, radius2=.42, depth=.6)
me = bpy.data.meshes.new("s"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("s", me); col.objects.link(o); me.materials.append(LOGM); me.transform(Matrix.Translation((0, 0, .3))); put(o)
cylz(0, 0, .6, .605, .41, CUT2, 12)
bar((-.1, 0, .62), (.5, .2, 1.3), .025, CUT)
quadbox([(-.12, -.02, .58), (.08, -.02, .58), (.1, -.02, .73), (-.16, -.02, .73)], .04, STL)
for k in range(5):
    a = k*1.3; box(math.cos(a)*.7 - .2, math.sin(a)*.7 - .05, 0, math.cos(a)*.7 + .2, math.sin(a)*.7 + .05, .08, CUT)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/mill_shed.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"hm_shed": (0, 0, 0), "hm_loft": (0, 0, 0), "hm_lumber5": (13, 5, 0), "hm_lumber4": (17.5, 9.5, 0), "hm_stump": (10.5, 12, 0)}
for k, v in lay.items(): roots[k].location = v
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (30, 26, 14); cam.rotation_euler = (Vector((2, -3, 3)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/mill_shed.png"; bpy.ops.render.render(write_still=True)
