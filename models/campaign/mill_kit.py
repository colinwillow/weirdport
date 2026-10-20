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



# mill_kit.py -- the Hollow Creek mill's machines as art, at buildMill's numbers (the code keeps the shed, the flume, the belts,
# the log piles, the ladders and every collider). Blender X = the mill frame's u, +Y = its +v; origins on the ground (y).
#   hm_burner      the teepee burner at (B.u 21, B.v -11): r 4 at the foot, .3 r at the top, 9 high, a mesh dome, a door, the
#                  conveyor's inlet on the -X side at 7; the smoke still leaves at y+9.3 (O.fireAt)
#   hm_crane       the log crane at (C.u -18, C.v 3): legs at +-1 to 8, the platform 2.8 sq, the cab at (-.6, -.6), the boom toward
#                  (+8, +5) from 10.4; the ladder stays the code's (on the -Y side at -1.35)
#   hm_logtruck    at (-21, 6): bed 2.4 x 9 at .5..1.3, the cab toward -Y (at -3.6), stakes and bunks; the five logs stay code
#   hm_watertower  at (9, v0-4): legs at +-1.2 to 7, a staved wooden tank r 2 from 7 to 10.4, a cone roof to 11.6
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

TYRE = mat("HM_tyre", (.07, .07, .08), .9); CHROME = mat("HM_chrome", (.75, .77, .8), .25, .8)
RUSTM = mat("HM_rust", (.48, .25, .14), .75, .3); RUST2 = mat("HM_rust_dark", (.3, .16, .1), .8, .3); YELM = mat("HM_yellow", (.88, .66, .12), .55); STAVE = mat("HM_stave", (.55, .4, .26)); STAVE2 = mat("HM_stave2", (.45, .32, .2))
GLASSM = mat("HM_glass", (.12, .16, .2), .15)
# ======== the teepee burner
cur = "hm_burner"; groups[cur] = []
R0, R1, Hb = 4., 1.2, 9.
N = 24; vs = []; fs = []
for i in range(N):
    a = i/N*2*math.pi; vs += [(R0*math.cos(a), R0*math.sin(a), 0), (R1*math.cos(a), R1*math.sin(a), Hb)]
for i in range(N): j = (i + 1) % N; fs.append((2*i, 2*j, 2*j + 1, 2*i + 1))
me = bpy.data.meshes.new("cone"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("cone", me); col.objects.link(o); me.materials.append(RUSTM); me.materials.append(RUST2)
for p in me.polygons: p.use_smooth = True; p.material_index = 1 if p.index % 5 == 2 else 0
put(o)
bm = bmesh.new(); bmesh.ops.solidify(bm, geom=[], thickness=0); bm.free()
for k in range(1, 6):                                                         # hoops up the cone
    z = k*Hb/6; r = R0 + (R1 - R0)*z/Hb + .04
    for i in range(N): a0, a1 = i/N*2*math.pi, (i + 1)/N*2*math.pi; bar((r*math.cos(a0), r*math.sin(a0), z), (r*math.cos(a1), r*math.sin(a1), z), .05, RUST2)
for i in range(0, N, 3):                                                      # seams down it
    a = i/N*2*math.pi; bar(((R0 + .05)*math.cos(a), (R0 + .05)*math.sin(a), 0), ((R1 + .05)*math.cos(a), (R1 + .05)*math.sin(a), Hb), .035, RUST2)
for i in range(12):                                                           # the spark-arrestor dome: mesh ribs over the top
    a = i/12*2*math.pi
    P = [((R1 + .1)*math.cos(a)*math.cos(t), (R1 + .1)*math.sin(a)*math.cos(t), Hb + 1.2*math.sin(t)) for t in [k*math.pi/2/5 for k in range(6)]]
    for k in range(5): bar(P[k], P[k + 1], .03, DARK)
for t in (.3, .8, 1.2):
    r = (R1 + .1)*math.cos(t); z = Hb + 1.2*math.sin(t)
    for i in range(16): a0, a1 = i/16*2*math.pi, (i + 1)/16*2*math.pi; bar((r*math.cos(a0), r*math.sin(a0), z), (r*math.cos(a1), r*math.sin(a1), z), .02, DARK)
box(-R0 - .05, -.8, 0, -R0 + .5, .8, 1.9, RUST2)                              # the stoking door on -X, and its frame
box(-R0 - .08, -.9, 1.9, -R0 + .5, .9, 2.05, DARK); box(-R0 - .08, -.9, 0, -R0 + .5, -.8, 1.9, DARK); box(-R0 - .08, .8, 0, -R0 + .5, .9, 1.9, DARK)
r7 = R0 + (R1 - R0)*7/Hb
box(-r7 - .3, -.9, 6.6, -r7 + .4, .9, 7.6, RUST2)                             # the conveyor's inlet hood at 7
box(-R0 - .4, -R0 - .4, -.3, R0 + .4, R0 + .4, .15, STONE)                     # its concrete pad
for k in range(9): a = rnd.uniform(0, 6.28); r = rnd.uniform(R0 + .4, R0 + 2.2); box(r*math.cos(a) - .3, r*math.sin(a) - .3, 0, r*math.cos(a) + .3, r*math.sin(a) + .3, .05, DARK)   # ash
# ======== the crane
cur = "hm_crane"; groups[cur] = []
Hc = 8.
for (a, b) in ((-1, -1), (1, -1), (-1, 1), (1, 1)): bar((a, b, 0), (a, b, Hc), .09, YELM); box(a - .25, b - .25, -.2, a + .25, b + .25, .1, STONE)
for z0 in [h for h in (0.4, 2.4, 4.4, 6.4)]:
    z1 = z0 + 2.0 if z0 < 6 else Hc - .05
    for s in (-1, 1):
        bar((-1, s, z0), (1, s, z1), .035, YELM); bar((s, -1, z0), (s, 1, z1), .035, YELM)
        bar((-1, s, z1), (1, s, z1), .04, YELM); bar((s, -1, z1), (s, 1, z1), .04, YELM)
box(-1.4, -1.4, Hc, 1.4, 1.4, Hc + .2, FMET)
for (a, b, c, d) in ((-1.4, -1.4, 1.4, -1.36), (-1.4, 1.36, 1.4, 1.4), (1.36, -1.4, 1.4, 1.4)): box(a, b, Hc + .2, c, d, Hc + 1.2, YELM)   # the platform rail
cylz(.3, .3, Hc + .2, Hc + .6, .9, DARK, 16)                                   # the slew ring
box(-1.3, -1.3, Hc + .2, .1, .1, Hc + 2.2, YELM, bev=.05)                       # the cab
box(-1.32, -1.0, Hc + 1.1, -1.28, -.2, Hc + 1.9, GLASSM); box(-1.0, -1.32, Hc + 1.1, -.2, -1.28, Hc + 1.9, GLASSM); box(-1.0, .08, Hc + 1.1, -.2, .12, Hc + 1.9, GLASSM)
quadbox([(-1.45, -1.45, Hc + 2.2), (.25, -1.45, Hc + 2.2), (.25, .25, Hc + 2.25), (-1.45, .25, Hc + 2.25)], .08, DARK)
base = Vector((.3, .3, Hc + 2.4)); tip = Vector((8, 5, Hc + 4.5)); d = tip - base; side = Vector((-d.y, d.x, 0)).normalized()*.3
for s in (-1, 1): bar(base + side*s, tip, .06, YELM); bar(base + side*s + Vector((0, 0, .5)), tip + Vector((0, 0, .1)), .05, YELM)
for k in range(1, 9):
    t = k/9; p = base + d*t
    bar(p + side*s*(1 - t), p - side*(1 - t), .025, YELM)
    bar(p + side*(1 - t), p + Vector((0, 0, .5*(1 - t))), .025, YELM)
bar((.3, .3, Hc + 2.4), (-1.5, -1.0, Hc + 2.6), .07, YELM); box(-2.1, -1.6, Hc + 2.2, -1.1, -.6, Hc + 3.0, DARK)   # the counterweight arm
bar(tip, tip - Vector((0, 0, 4.5)), .015, DARK)                                # the cable, and the log grapple on it
g0 = tip - Vector((0, 0, 4.6)); box(g0.x - .3, g0.y - .15, g0.z - .25, g0.x + .3, g0.y + .15, g0.z, YELM)
for s in (-1, 1):
    bar((g0.x + s*.3, g0.y, g0.z - .2), (g0.x + s*.6, g0.y, g0.z - .8), .05, DARK); bar((g0.x + s*.6, g0.y, g0.z - .8), (g0.x + s*.3, g0.y, g0.z - 1.2), .05, DARK)
# ======== the log truck
cur = "hm_logtruck"; groups[cur] = []
for y_ in (-3.4, 1.0, 2.4, 3.8):
    for s in (-1, 1): ring((s*1.05, y_, .5), .38, .14, TYRE, 16, 6); cylz(s*1.05 + (.0 if s < 0 else 0), y_, .44, .56, .1, CHROME, 8)
for y_ in (1.0, 2.4, 3.8):
    for s in (-1, 1): ring((s*.7, y_, .5), .38, .14, TYRE, 16, 6) if False else None
box(-.5, -4.6, .4, .5, 4.6, .65, DARK)                                          # the chassis rails
box(-1.2, -4.6, .5, 1.2, -2.6, 2.0, REDP, bev=.06)                               # the cab, the bonnet ahead of it
box(-1.15, -4.65, .7, 1.15, -4.55, 1.5, CHROME)
box(-1.15, -2.65, 2.0, 1.15, -1.7, 3.0, REDP, bev=.06); box(-1.17, -2.5, 2.2, 1.17, -1.9, 2.8, GLASSM); box(-1.1, -2.67, 2.2, 1.1, -2.63, 2.8, GLASSM)
for s in (-1, 1): bar((s*1.0, -1.65, .7), (s*1.0, -1.65, 3.6), .07, CHROME); box(s*1.25 - .05, -2.5, 2.2, s*1.25 + .05, -2.2, 2.55, CHROME)   # stacks, mirrors
box(-1.0, -2.6, .55, 1.0, -1.7, 1.2, DARK)
quadbox([(-1.25, -4.4, 1.0), (1.25, -4.4, 1.0), (1.25, -3.0, 1.0), (-1.25, -3.0, 1.0)], .05, DARK)       # the fenders over the front
for y_ in (-.8, 1.7, 4.2):                                                       # bunks and stakes for the logs
    box(-1.25, y_ - .15, .65, 1.25, y_ + .15, 1.3, DARK)
    for s in (-1, 1): box(s*1.15 - .07, y_ - .07, 1.3, s*1.15 + .07, y_ + .07, 2.9, YELM)
box(-.15, -1.6, 1.3, .15, 4.6, 1.4, DARK)                                        # the reach
box(-1.0, 4.4, .7, 1.0, 4.55, 1.1, REDP); box(-.9, 4.55, .8, -.6, 4.58, .95, mat("HM_lamp", (.9, .15, .1), .3)); box(.6, 4.55, .8, .9, 4.58, .95, bpy.data.materials["HM_lamp"])
# ======== the mill's water tower
cur = "hm_watertower"; groups[cur] = []
for (a, b) in ((-1.2, -1.2), (1.2, -1.2), (-1.2, 1.2), (1.2, 1.2)): box(a - .11, b - .11, -.3, a + .11, b + .11, 7, PLANK2); box(a - .25, b - .25, -.3, a + .25, b + .25, .1, STONE)
for z0 in (.4, 3.7):
    for s in (-1, 1): bar((-1.2, s*1.2, z0), (1.2, s*1.2, z0 + 3.2), .04, PLANK); bar((s*1.2, -1.2, z0), (s*1.2, 1.2, z0 + 3.2), .04, PLANK)
box(-1.6, -1.6, 6.85, 1.6, 1.6, 7.0, PLANK2)
NS = 28
for i in range(NS):                                                             # the staves, each its own board
    a0, a1 = i/NS*2*math.pi, (i + .92)/NS*2*math.pi
    pts = [(2*math.cos(a0), 2*math.sin(a0), 7.0), (2*math.cos(a1), 2*math.sin(a1), 7.0), (2*math.cos(a1), 2*math.sin(a1), 10.4), (2*math.cos(a0), 2*math.sin(a0), 10.4)]
    vs = pts + [(p[0]*.94, p[1]*.94, p[2]) for p in pts]
    me = bpy.data.meshes.new("st"); me.from_pydata(vs, [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
    o = bpy.data.objects.new("st", me); col.objects.link(o); me.materials.append(STAVE if i % 3 else STAVE2); put(o)
for z in (7.4, 8.4, 9.4, 10.1):
    for i in range(20): a0, a1 = i/20*2*math.pi, (i + 1)/20*2*math.pi; bar((2.05*math.cos(a0), 2.05*math.sin(a0), z), (2.05*math.cos(a1), 2.05*math.sin(a1), z), .03, DARK)
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=2.3, radius2=0, depth=1.2)
me = bpy.data.meshes.new("cap"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("cap", me); col.objects.link(o); me.materials.append(ROOF); me.transform(Matrix.Translation((0, 0, 11.0))); put(o)
box(-.3, -.3, 11.55, .3, .3, 11.8, PLANK2)
for k in range(12): box(1.2 - .2, -1.35, .5 + k*.55, 1.2 + .2, -1.32, .55 + k*.55, FMET)                       # a ladder up a leg to the tank
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/mill_kit.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"hm_burner": (21, -11, 0), "hm_crane": (-18, 3, 0), "hm_logtruck": (-21, 6, 0), "hm_watertower": (9, -19, 0)}
for k, (x, y, r) in lay.items(): roots[k].location = (x, y, 0); roots[k].rotation_euler = (0, 0, r)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.45, .38, .26), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-40))
cd = bpy.data.cameras.new("C"); cd.lens = 22; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (12, 34, 11); cam.rotation_euler = (Vector((-3, -2, 3)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/mill_kit.png"; bpy.ops.render.render(write_still=True)
