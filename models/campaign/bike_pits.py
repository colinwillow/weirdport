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
TYRE = mat("BK_tyre", (.07, .07, .08), .9); CHROME = mat("BK_chrome", (.75, .77, .8), .25, .8); SEAT = mat("BK_seat", (.1, .1, .12), .7)
NUMW = mat("BK_plate", (.95, .95, .92), .6); CANV = mat("BK_canvas", (.93, .92, .88), .9)
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
def bike(name, C):
    global cur; cur = name; groups[cur] = []
    for y in (-.62, .62):
        ring((0, y, .42), .33, .09, TYRE, 18, 6)
        for k in range(22): a = k/22*2*math.pi; box(-.08, y + .42*math.cos(a) - .025, .42 + .42*math.sin(a) - .025, .08, y + .42*math.cos(a) + .025, .42 + .42*math.sin(a) + .025, TYRE)   # knobs
        cylz(0, y, .38, .46, .07, CHROME, 8); bar((-.05, y, .42), (.05, y, .42), .06, CHROME)
        for k in range(8): a = k/8*2*math.pi; bar((0, y, .42), (0, y + .3*math.cos(a), .42 + .3*math.sin(a)), .008, CHROME)
    bar((.07, .62, .42), (.07, .45, 1.08), .03, CHROME); bar((-.07, .62, .42), (-.07, .45, 1.08), .03, CHROME)   # fork
    bar((0, .45, 1.08), (0, .5, 1.15), .04, CHROME); bar((-.35, .52, 1.18), (.35, .52, 1.18), .02, CHROME)       # stem, bars
    for s in (-1, 1): bar((s*.3, .52, 1.18), (s*.36, .52, 1.18), .03, SEAT)
    bar((0, .4, 1.0), (0, -.25, .7), .035, CHROME); bar((0, -.25, .7), (0, -.62, .42), .03, CHROME); bar((0, .35, .9), (0, .0, .45), .03, CHROME)   # frame, swingarm
    box(-.13, -.15, .35, .13, .2, .62, DARK)                                     # engine
    box(-.17, .05, .82, .17, .48, 1.02, C, bev=.03)                              # tank and shrouds
    for s in (-1, 1): quadbox([(s*.17, .45, .68), (s*.17, .1, .68), (s*.17, .1, .98), (s*.17, .48, 1.0)] if s > 0 else [(s*.17, .1, .68), (s*.17, .45, .68), (s*.17, .48, 1.0), (s*.17, .1, .98)], .02, C)
    box(-.12, -.6, .93, .12, .1, 1.0, SEAT)                                      # seat
    quadbox([(-.13, -.9, 1.02), (.13, -.9, 1.02), (.13, -.25, .95), (-.13, -.25, .95)], .03, C)   # rear fender
    quadbox([(-.1, .55, .9), (.1, .55, .9), (.1, .95, .82), (-.1, .95, .82)], .03, C)     # front fender
    box(-.14, .58, .95, .14, .62, 1.2, NUMW); box(-.05, .565, 1.0, .05, .58, 1.15, DARK)   # number plate
    bar((.12, -.1, .5), (.17, -.75, .78), .045, CHROME)                          # exhaust
    box(-.04, -.05, 0, .04, .05, .38, CHROME)                                    # the stand it is on
for nm, C in (("bk_bike_red", REDP), ("bk_bike_blue", BLUEP), ("bk_bike_yellow", YEL)): bike(nm, C)
def canopy(name, C):
    global cur; cur = name; groups[cur] = []
    for (a, b) in ((-1.6, -1.6), (1.6, -1.6), (-1.6, 1.6), (1.6, 1.6)):
        bar((a, b, 0), (a, b, 2.6), .03, FMET); box(a - .15, b - .15, 0, a + .15, b + .15, .03, FMET)
        bar((a, b, 2.0), (a*.55, b*.55, 2.6), .02, FMET)
    for s in (-1, 1): bar((-1.6, s*1.6, 2.6), (1.6, s*1.6, 2.6), .02, FMET); bar((s*1.6, -1.6, 2.6), (s*1.6, 1.6, 2.6), .02, FMET)
    apex = (0, 0, 3.1)
    for (p, q) in (((-1.65, -1.65, 2.6), (1.65, -1.65, 2.6)), ((1.65, -1.65, 2.6), (1.65, 1.65, 2.6)), ((1.65, 1.65, 2.6), (-1.65, 1.65, 2.6)), ((-1.65, 1.65, 2.6), (-1.65, -1.65, 2.6))):
        me = bpy.data.meshes.new("cr"); me.from_pydata([p, q, apex], [], [(0, 1, 2)]); me.validate(); me.flip_normals() if False else None
        o = bpy.data.objects.new("cr", me); col.objects.link(o); me.materials.append(C); put(o)
        me.polygons[0].flip() if me.polygons[0].normal.z < 0 else None
    for (p, q) in (((-1.65, -1.65), (1.65, -1.65)), ((1.65, -1.65), (1.65, 1.65)), ((1.65, 1.65), (-1.65, 1.65)), ((-1.65, 1.65), (-1.65, -1.65))):
        for k in range(6):
            t0, t1 = k/6, (k + 1)/6; a = (p[0] + (q[0] - p[0])*t0, p[1] + (q[1] - p[1])*t0); b = (p[0] + (q[0] - p[0])*t1, p[1] + (q[1] - p[1])*t1)
            m = C if k % 2 == 0 else CANV
            me = bpy.data.meshes.new("val"); me.from_pydata([(a[0], a[1], 2.6), (b[0], b[1], 2.6), (b[0], b[1], 2.38), ((a[0] + b[0])/2, (a[1] + b[1])/2, 2.3), (a[0], a[1], 2.38)], [], [(0, 1, 2, 3, 4), (4, 3, 2, 1, 0)]); me.validate()
            o = bpy.data.objects.new("val", me); col.objects.link(o); me.materials.append(m); put(o)
    box(-.6, 1.55, 2.0, .6, 1.62, 2.35, CANV)                                  # a blank team board on the back valance
for nm, C in (("bk_canopy_red", REDP), ("bk_canopy_blue", BLUEP), ("bk_canopy_yellow", YEL)): canopy(nm, C)
# ======== the trailer
cur = "bk_trailer"; groups[cur] = []
box(-1.2, -3.5, .45, 1.2, 3.5, 2.8, WHITE, bev=.04); box(-1.25, -3.55, .35, 1.25, 3.55, .5, DARK)
for s in (-1, 1):
    for y in (-.9, .9): ring((s*1.15, y, .35), .25, .1, TYRE, 14, 6)
    quadbox([(s*1.22, -1.35, .5), (s*1.22, 1.35, .5), (s*1.22, 1.35, .72), (s*1.22, -1.35, .72)] if s > 0 else [(s*1.22, 1.35, .5), (s*1.22, -1.35, .5), (s*1.22, -1.35, .72), (s*1.22, 1.35, .72)], .02, FMET)
    box(s*1.2 - .02*s - .01, -3.0, 1.6, s*1.2 + .02*s + .01, 3.0, 1.9, REDP)        # a stripe down each side
box(-1.25, -3.6, 2.8, 1.25, 3.6, 2.9, FMET)
bar((0, 3.5, .5), (0, 4.6, .45), .06, FMET); cylz(0, 4.3, 0, .4, .04, FMET, 8)
box(-.9, -3.53, .6, .9, -3.5, 2.6, mat("BK_ramp", (.5, .52, .55), .5, .4))           # the rear ramp door, closed
box(1.21, 1.4, .8, 1.24, 2.4, 2.4, DARK); box(1.21, 1.3, 2.4, 1.26, 2.5, 2.45, FMET)  # side door
for y in (-2.6, 2.6): box(-.15, y - .15, 2.9, .15, y + .15, 3.05, FMET)
# ======== the announcer's tower
cur = "bk_tower"; groups[cur] = []
H = 6.0
for (a, b) in ((-1.2, -1.2), (1.2, -1.2), (-1.2, 1.2), (1.2, 1.2)):
    box(a - .09, b - .09, -.3, a + .09, b + .09, H, PLANK2); box(a - .2, b - .2, -.3, a + .2, b + .2, .1, STONE)
for z0, z1 in ((.3, 2.9), (2.9, 5.6)):
    for s in (-1, 1):
        bar((-1.2, s*1.2, z0), (1.2, s*1.2, z1), .04, PLANK); bar((s*1.2, -1.2, z0), (s*1.2, 1.2, z1), .04, PLANK)
for z in (2.9, 5.6): bar((-1.2, 1.2, z), (1.2, 1.2, z), .05, PLANK); bar((-1.2, -1.2, z), (-1.2, 1.2, z), .05, PLANK); bar((1.2, -1.2, z), (1.2, 1.2, z), .05, PLANK)
box(-1.5, -1.5, H - .2, 1.5, 1.5, H, PLANK2)
for k in range(12): box(-1.5 + k*.25 + .01, -1.5, H - .01, -1.5 + (k + 1)*.25 - .01, 1.5, H + .01, PLANK)
for (a0, b0, a1, b1) in ((-1.5, 1.4, 1.5, 1.5), (-1.5, -1.5, -1.4, 1.5), (1.4, -1.5, 1.5, 1.5)):
    box(a0, b0, H, a1, b1, H + 1.1, PLANK)
for k in range(13):
    x = -1.45 + k*.24; box(x, 1.5, H + .05, x + .04, 1.54, H + 1.05, PLANK2)
box(-1.55, 1.5, H + .4, 1.55, 1.56, H + .9, CANV)                              # a sponsor banner on the front (blank)
for (a, b) in ((-1.4, -1.4), (1.4, -1.4), (-1.4, 1.4), (1.4, 1.4)): box(a - .04, b - .04, H, a + .04, b + .04, H + 2.3, PLANK2)
quadbox([(-1.75, -1.75, H + 2.3), (1.75, -1.75, H + 2.3), (1.75, 1.75, H + 2.45), (-1.75, 1.75, H + 2.45)], .1, REDP)
bar((0, 1.6, H + 2.4), (0, 1.6, H + 3.4), .03, FMET)                             # the loudspeaker horns on the roof
for s in (-1, 1):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=12, radius1=.08, radius2=.28, depth=.5)
    me = bpy.data.meshes.new("horn"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("horn", me); col.objects.link(o); me.materials.append(FMET)
    me.transform(Matrix.Translation((s*.25, 1.75, H + 3.2)) @ Matrix.Rotation(-math.pi/2, 4, 'X') @ Matrix.Rotation(s*.5, 4, 'Y')); put(o)
box(-.6, .9, H + 1.1, .6, 1.4, H + 1.2, PLANK); box(-.25, 1.0, H + 1.2, .05, 1.2, H + 1.45, DARK); cylz(.3, 1.1, H + 1.2, H + 1.45, .05, FMET, 6)   # a desk, the PA, a mic
box(-.3, -.7, H, .3, -.1, H + .45, PLANK2)                                      # a stool
# ======== pit clutter
cur = "bk_chest"; groups[cur] = []
box(-.35, -.25, .05, .35, .25, .9, REDP, bev=.02)
for k in range(5): box(-.33, -.27, .2 + k*.15, .33, -.25, .3 + k*.15, DARK); box(-.08, -.29, .23 + k*.15, .08, -.27, .26 + k*.15, CHROME)
for (a, b) in ((-.3, -.2), (.3, -.2), (-.3, .2), (.3, .2)): ring((a, b, .05), .04, .02, DARK, 8, 4)
cur = "bk_drum"; groups[cur] = []
cylz(0, 0, 0, .85, .28, BLUEP, 16)
for z in (.25, .6): cylz(0, 0, z, z + .03, .29, DARK, 16)
cylz(.12, .08, .85, .88, .04, FMET, 8); box(-.18, -.29, .3, .18, -.28, .55, WHITE)
cur = "bk_generator"; groups[cur] = []
for s in (-1, 1): bar((s*.55, -.35, .1), (s*.55, .35, .1), .03, DARK); bar((s*.55, -.35, .1), (s*.55, -.35, .85), .03, DARK); bar((s*.55, .35, .1), (s*.55, .35, .85), .03, DARK)
bar((-.55, -.35, .85), (.55, -.35, .85), .03, DARK); bar((-.55, .35, .85), (.55, .35, .85), .03, DARK)
box(-.45, -.3, .12, .2, .3, .65, YEL, bev=.03); cylz(.32, 0, .12, .6, .2, YEL, 12); box(-.4, -.25, .65, .1, .25, .78, DARK)
box(.5, -.2, .3, .52, .2, .55, DARK); bar((-.5, .2, .4), (-.75, .25, .55), .025, FMET)
# ======== join each group under its root, export, preview
roots = {}
for name, Lg in groups.items():
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in Lg: o.select_set(True)
    bpy.context.view_layer.objects.active = Lg[0]; bpy.ops.object.join(); j = bpy.context.view_layer.objects.active; j.name = name + "_mesh"
    r = bpy.data.objects.new(name, None); col.objects.link(r); j.parent = r; roots[name] = r
    print(name, len(j.data.polygons), "faces", len(j.data.materials), "materials")
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in roots.values(): r.select_set(True); [c.select_set(True) for c in r.children]
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/bike_pits.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"bk_canopy_red": (-9, 0, 0), "bk_canopy_blue": (0, 0, 0), "bk_canopy_yellow": (9, 0, 0), "bk_bike_red": (-9.6, .3, .3), "bk_bike_blue": (-.6, .3, .7),
       "bk_bike_yellow": (8.4, .3, 1.1), "bk_trailer": (14, 1, .1), "bk_tower": (-6, 10, 0), "bk_chest": (-7.9, -1, 0), "bk_drum": (1.2, 1.1, 0), "bk_generator": (-15, 0, 0)}
for k, (x, y, r) in lay.items(): roots[k].location = (x, y, 0); roots[k].rotation_euler = (0, 0, r)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.42, .32, .2), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 26; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-4, -15, 5.5); cam.rotation_euler = (Vector((-1, 3, 2.4)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/bike_pits.png"; bpy.ops.render.render(write_still=True)
