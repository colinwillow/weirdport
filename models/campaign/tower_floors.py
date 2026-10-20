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
# ================= DUMP TOWER'S FLOORS (buildDumpTower): lobby, offices, gym, sky garden, boardroom, penthouse =================
import random; rq = random.Random(528)
GOLDT = mat("DT_gold", (.85, .64, .22), .3, .9); MARB = mat("DT_marble", (.9, .88, .84), .25); DARKT = mat("DT_dark", (.11, .11, .13), .5); WHITET = mat("DT_white", (.93, .92, .9), .5)
LEATH = mat("DT_leather", (.32, .14, .1), .5); CARP = mat("DT_carpet", (.42, .1, .12), .95); SCREEN = mat("DT_screen", (.15, .35, .55), .2); WOODT = mat("DT_wood", (.33, .2, .12), .4)
STEELT = mat("DT_steel", (.6, .63, .66), .35, .7); RUBB = mat("DT_rubber", (.08, .08, .09), .9); PLANT = mat("DT_plant", (.26, .52, .24)); PLANT2 = mat("DT_plant2", (.2, .42, .2)); SOILT = mat("DT_soil", (.22, .15, .1), 1)
BARK = mat("DT_bark", (.36, .26, .18), .9)
def leafy(c, r, m, sub=1):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    for v in bm.verts: v.co += Vector((rq.uniform(-.05, .05), rq.uniform(-.05, .05), rq.uniform(-.04, .04)))
    me = bpy.data.meshes.new("lf"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("lf", me); col.objects.link(o); me.materials.append(m); o.location = c; put(o)
def chair(x, y, rot, m=LEATH, hi=1.1):
    c, s = math.cos(rot), math.sin(rot)
    def P(a, b): return (x + a*c - b*s, y + a*s + b*c)
    cylz(*P(0, 0), 0, .42, .03, STEELT, 6)
    for k in range(5): a = k / 5 * 2 * math.pi; bar((*P(0, 0), .05), (*P(.28*math.cos(a), .28*math.sin(a)), .03), .02, STEELT)
    p = [P(-.27, -.27), P(.27, -.27), P(.27, .25), P(-.27, .25)]; quadbox([(*q, .42) for q in p], .1, m)
    p = [P(-.25, .22), P(.25, .22), P(.25, .3), P(-.25, .3)]; quadbox([(*q, .5) for q in p], hi - .5, m)
# ---- the lobby desk: 5 x 1.2 x 1.1 gold-fronted marble counter, the 6 x 3.6 name wall behind it at +.7
cur = "dt_lobbydesk"; groups[cur] = []
box(-2.5, -.6, 0, 2.5, .6, 1.0, GOLDT, .03); box(-2.55, -.65, 1.0, 2.55, .65, 1.1, MARB)
for x in (-1.6, -.5, .6, 1.7): box(x - .02, -.62, .1, x + .02, -.6, .9, DARKT)
box(-3, .6, 0, 3, .8, 3.6, DARKT); box(-2.4, .58, 2.4, 2.4, .6, 3.1, GOLDT)
for x in (-1.2, 1.2): box(x - .25, .2, 1.1, x + .25, .25, 1.4, SCREEN)
# ---- a lobby urn with a clipped ball tree: gold urn r .5 -> .4, .8 tall, ball r .8 at 1.4
cur = "dt_urn"; groups[cur] = []
lathe([(0, 0), (.38, 0), (.4, .1), (.5, .72), (.54, .8), (0, .76)], GOLDT, 16)
cylz(0, 0, .76, 1.0, .05, BARK, 6); leafy((0, 0, 1.4), .75, PLANT, 2)
# ---- a lobby sofa (also the waiting bench): 2.2 x .9 x .45 seat, carpet-red leather, back at +Y
cur = "dt_lobbysofa"; groups[cur] = []
box(-1.1, -.45, .1, 1.1, .45, .45, LEATH, .05); box(-1.1, .25, .45, 1.1, .45, .85, LEATH, .05)
for s in (-1, 1): box(s*1.1 - .12, -.45, .1, s*1.1 + .0 if s > 0 else s*1.1 + .12, .45, .65, LEATH, .04) if False else box(min(s*1.1, s*1.1 - s*.12), -.45, .1, max(s*1.1, s*1.1 - s*.12), .45, .65, LEATH, .04)
for (x, y) in ((-1, -.4), (1, -.4), (-1, .4), (1, .4)): box(x - .03, y - .03, 0, x + .03, y + .03, .1, GOLDT)
# ---- an office desk: top 1.8 x .9 at .72..78, a modesty panel, monitor at +.3 Y, keyboard, the chair at -.7
cur = "dt_desk"; groups[cur] = []
box(-.9, -.45, .72, .9, .45, .78, WHITET); box(-.85, .38, .05, .85, .42, .72, DARKT)
for x in (-.85, .85): box(x - .03, -.42, 0, x + .03, .42, .72, DARKT)
box(-.25, .26, .78, .25, .3, 1.2, DARKT); box(-.23, .255, .82, .23, .26, 1.18, SCREEN); box(-.04, .27, .78, .04, .35, .9, DARKT)
box(-.22, -.05, .78, .22, .1, .8, DARKT); chair(0, -.75, 0, DARKT, 1.0)
# ---- a treadmill: .9 x 2 deck to .3, the upright and console at -Y to 1.4
cur = "dt_treadmill"; groups[cur] = []
box(-.45, -1, 0, .45, 1, .22, DARKT, .04); box(-.35, -.9, .22, .35, .95, .26, RUBB)
for s in (-1, 1): bar((s*.38, -.85, .22), (s*.35, -.82, 1.25), .03, STEELT); bar((s*.35, -.82, 1.0), (s*.35, -.35, 1.0), .02, STEELT)
box(-.38, -.92, 1.15, .38, -.72, 1.42, DARKT); box(-.25, -.73, 1.2, .25, -.72, 1.36, SCREEN)
# ---- a weight bench: 1.2 x 2.2, a padded bench, the rack and a bar with plates
cur = "dt_weights"; groups[cur] = []
box(-.15, -.9, .38, .15, .5, .5, CARP, .04)
for y in (-.7, .3): box(-.05, y - .03, 0, .05, y + .03, .38, STEELT); box(-.25, y - .03, 0, .25, y + .03, .04, STEELT)
for s in (-1, 1): box(s*.5 - .03, -.85, 0, s*.5 + .03, -.79, 1.2, STEELT); box(s*.5 - .1, -.85, 1.05, s*.5 + .03, -.82, 1.08, STEELT)
bar((-.6, -.82, 1.12), (.6, -.82, 1.12), .015, STEELT)
for s in (-1, 1):
    o = cylz(0, 0, -.02, .02, .2, RUBB, 14); o.data.transform(Matrix.Rotation(math.pi/2, 4, 'Y')); o.data.transform(Matrix.Translation((s*.52, -.82, 1.12)))
# ---- a sky-garden tree: a 1.6 m planter .6 tall, a trunk to 2.4, a crown r 1.1 at 2.9
cur = "dt_tree"; groups[cur] = []
box(-.8, -.8, 0, .8, .8, .6, MARB, .03); box(-.72, -.72, .55, .72, .72, .6, SOILT)
bar((0, 0, .6), (.05, .03, 2.4), .1, BARK); bar((.03, .02, 1.9), (.45, .2, 2.5), .05, BARK)
for (c, r, m) in (((0, 0, 2.9), .85, PLANT), ((.5, .2, 2.7), .55, PLANT2), ((-.45, -.2, 2.75), .6, PLANT2), ((.1, -.4, 3.2), .55, PLANT)): leafy(c, r, m, 2)
# ---- a garden bench: 1.4 x .5 x .45 slatted teak on gold legs
cur = "dt_bench"; groups[cur] = []
for k in range(4): box(-.7, -.25 + k*.125 + .01, .4, .7, -.25 + (k + 1)*.125 - .01, .45, WOODT)
for x in (-.6, .6): box(x - .04, -.22, 0, x + .04, .22, .4, GOLDT)
# ---- the boardroom table: 3 x 10, .8 high, wood top on a dark pedestal; and its chair
cur = "dt_boardtable"; groups[cur] = []
box(-1.5, -5, .72, 1.5, 5, .8, WOODT, .03)
box(-1.3, -4.7, 0, 1.3, 4.7, .72, DARKT)
for y in (-3, 0, 3): box(-.12, y - .12, .8, .12, y + .12, .84, GOLDT)
cur = "dt_execchair"; groups[cur] = []; chair(0, 0, 0, LEATH, 1.15)
# ---- the penthouse sofa: 3 x 1 x .45 white, back toward +Y .4
cur = "dt_whitesofa"; groups[cur] = []
box(-1.5, -.5, .1, 1.5, .5, .45, WHITET, .06); box(-1.5, .3, .45, 1.5, .5, .95, WHITET, .06)
for k in range(3): box(-1.4 + k*.95, -.45, .45, -.5 + k*.95, .3, .55, WHITET, .06)
for (x, y) in ((-1.4, -.4), (1.4, -.4), (-1.4, .4), (1.4, .4)): box(x - .03, y - .03, 0, x + .03, y + .03, .1, GOLDT)
# ---- the penthouse coffee table (1.6 square, .4) and a gold coin stack (r .25, .9)
cur = "dt_coffeetable"; groups[cur] = []
box(-.8, -.8, .34, .8, .8, .4, GOLDT); box(-.75, -.75, .4, .75, .75, .41, MARB)
for (x, y) in ((-.7, -.7), (.7, -.7), (-.7, .7), (.7, .7)): box(x - .04, y - .04, 0, x + .04, y + .04, .34, GOLDT)
cur = "dt_coins"; groups[cur] = []
for k in range(18): cylz(rq.uniform(-.015, .015), rq.uniform(-.015, .015), k*.05, k*.05 + .048, .25, GOLDT, 16)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/tower_floors.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"dt_lobbydesk": (-5, 5, 0, 0), "dt_urn": (-8.5, 3, 0, 0), "dt_lobbysofa": (-6, 1, 0, 0), "dt_desk": (-2.5, 1.5, 0, 0), "dt_treadmill": (-.5, 1.5, 0, 0), "dt_weights": (1, 1.5, 0, 0), "dt_tree": (3.2, 4, 0, 0), "dt_bench": (3.2, 1.6, 0, 0), "dt_boardtable": (7, 6, 0, 0), "dt_execchair": (5.3, 4, -1.57, 0), "dt_whitesofa": (-3, -2, 0, 0), "dt_coffeetable": (-3, -3.6, 0, 0), "dt_coins": (-1.3, -3.6, 0, 0)}
for k, (x, y, r, z) in lay.items(): roots[k].location = (x, y, z); roots[k].rotation_euler = (0, 0, r)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.43, .36, .27), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-3, -14, 9); cam.rotation_euler = (Vector((0, 1.5, .5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/tower_floors.png"; bpy.ops.render.render(write_still=True)
