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
def truss(p, q, w=.35, m=None):
    """a box truss from p to q: four chords and zigzag lacing on its four faces (built from points)"""
    p, q = Vector(p), Vector(q); d = (q - p); L = d.length; n = d.normalized()
    a = n.cross(Vector((0, 0, 1))) if abs(n.z) < .95 else n.cross(Vector((1, 0, 0))); a.normalize(); b = n.cross(a)
    C = [(a*sx + b*sy)*w/2 for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for c in C: bar(p + c, q + c, .035, m)
    k = max(2, int(L/w))
    for i in range(k):
        t0, t1 = i/k, (i + 1)/k
        for j in range(4):
            c0, c1 = C[j], C[(j + 1) % 4]
            bar(p + d*t0 + (c0 if i % 2 else c1), p + d*t1 + (c1 if i % 2 else c0), .018, m)
# ======== the stage
cur = "ff_stage"; groups[cur] = []
W, Dd, Hh, TT = 14., 8., 1.4, 8.
box(-W/2, -Dd/2, 0, W/2, Dd/2, Hh - .06, PLANK2)
for k in range(int(W/.25)): box(-W/2 + k*.25 + .01, -Dd/2, Hh - .06, -W/2 + (k + 1)*.25 - .01, Dd/2, Hh, PLANK)
box(-W/2 - .05, Dd/2, Hh - .12, W/2 + .05, Dd/2 + .06, Hh + .02, GOLD)                     # a nosing along the front edge
for k in range(14):                                                              # a skirt of swagged bunting round the front and sides
    x0, x1 = -W/2 + k*W/14, -W/2 + (k + 1)*W/14; m = (REDP, WHITE, BLUEP)[k % 3]
    vs = [(x0, Dd/2 + .07, Hh - .15), (x1, Dd/2 + .07, Hh - .15), ((x0 + x1)/2, Dd/2 + .1, Hh - .75)]; vs += [(v[0], v[1] + .02, v[2]) for v in vs]
    me = bpy.data.meshes.new("sw"); me.from_pydata(vs, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate(); o = bpy.data.objects.new("sw", me); col.objects.link(o); me.materials.append(m); put(o)
for x in [-W/2 + .3 + i*1.0 for i in range(14)]: box(x - .04, Dd/2, 0, x + .04, Dd/2 + .06, Hh - .15, PLANK)   # skirt boards under the bunting
for s in (-1, 1):                                                                # the steps at the front corners, with handrails
    cx = s*(W/2 - 1)
    for k in range(5):
        z = (k + 1)*Hh/5; y0_ = Dd/2 + (4 - k)*.45; box(cx - .9, y0_, z - .05, cx + .9, y0_ + .45, z, PLANK)
        box(cx - .9, y0_ + .43, 0, cx + .9, y0_ + .45, z, PLANK2)
    for e in (-1, 1):
        xe = cx + e*.95
        bar((xe, Dd/2 + 2.25, .9), (xe, Dd/2 + .1, Hh + .9), .03, FMET); bar((xe, Dd/2 + 2.25, 0), (xe, Dd/2 + 2.25, .9), .03, FMET); bar((xe, Dd/2 + .1, Hh), (xe, Dd/2 + .1, Hh + .9), .03, FMET)
box(-W/2, -Dd/2 + .05, Hh, W/2, -Dd/2 + .35, Hh + 6, BLUEP)                     # the backdrop, framed, with lights over its top edge
for (x0, x1, z0, z1) in ((-W/2 - .12, -W/2 + .12, Hh, Hh + 6.15), (W/2 - .12, W/2 + .12, Hh, Hh + 6.15), (-W/2 - .12, W/2 + .12, Hh + 5.95, Hh + 6.15)): box(x0, -Dd/2, z0, x1, -Dd/2 + .45, z1, GOLD)
for k in range(15): box(-W/2 + .2 + k*.97, -Dd/2 + .35, Hh + .1, -W/2 + .2 + k*.97 + .04, -Dd/2 + .39, Hh + 5.9, mat("FF_blue2", (.15, .24, .46), .6) if k == 0 else bpy.data.materials["FF_blue2"])
for k in range(16): a = k/15; ball((-W/2 + .4 + a*(W - .8), -Dd/2 + .42, Hh + 5.8), .08, BULB, 6)
for k in range(5): box(-W/2 + .5 + k*3.2, -Dd/2 + .36, Hh + .3, -W/2 + 1.9 + k*3.2, -Dd/2 + .4, Hh + 2.1, (REDP, WHITE, REDP, WHITE, REDP)[k])   # banners hung low on it
def speaker(cx, cy, z0, w, d, h, face):
    box(cx - w/2, cy - d/2, z0, cx + w/2, cy + d/2, z0 + h, CLOTH)
    n = int(h/1.05)
    for i in range(n):
        zc = z0 + (i + .5)*h/n
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=min(w, h/n)*.36, radius2=min(w, h/n)*.36, depth=.06)
        me = bpy.data.meshes.new("cone"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("cone", me); col.objects.link(o); me.materials.append(CONE)
        me.transform(Matrix.Translation((cx, cy + face*(d/2 + .02), zc)) @ Matrix.Rotation(math.pi/2, 4, 'X')); put(o)
        ball((cx, cy + face*(d/2 + .04), zc), min(w, h/n)*.1, FMET, 8)
        box(cx - w/2, cy + face*d/2 - .02, zc + h/n/2 - .04, cx + w/2, cy + face*d/2 + .02, zc + h/n/2, FMET)
for s in (-1, 1): speaker(s*(W/2 - 1.2), -1.5, Hh, 1.6, 1.4, 3.2, 1); speaker(s*(W/2 + 1.4), 0, 0, 1.6, 1.6, 4.5, 1)
box(-.45, 1.2, Hh, .45, 1.8, Hh + 1.1, WOOD); quadbox([(-.5, 1.15, Hh + 1.1), (.5, 1.15, Hh + 1.1), (.5, 1.85, Hh + 1.25), (-.5, 1.85, Hh + 1.25)], .05, WOOD)
box(-.3, 1.83, Hh + .35, .3, 1.86, Hh + .85, GOLD); bar((0, 1.6, Hh + 1.2), (0, 1.75, Hh + 1.6), .015, FMET); ball((0, 1.78, Hh + 1.63), .04, CLOTH, 6)   # an emblem; the mic
for a in (-1, 1):                                                                # the truss: four towers, two spans, the catwalk on the back one
    for b in (-1, 1):
        truss((a*(W/2 + .3), b*(Dd/2 + .3), 0), (a*(W/2 + .3), b*(Dd/2 + .3), TT - .35), .35, FMET); box(a*(W/2 + .3) - .35, b*(Dd/2 + .3) - .35, 0, a*(W/2 + .3) + .35, b*(Dd/2 + .3) + .35, .08, FMET)
for b in (-1, 1): truss((-(W/2 + .3) - .2, b*(Dd/2 + .3), TT - .175), ((W/2 + .3) + .2, b*(Dd/2 + .3), TT - .175), .35, FMET)
cy = -(Dd/2 + .3)
box(-(W/2 + .45), cy - .55, TT, W/2 + .45, cy + .55, TT + .15, FMET)
for k in range(int((W + .9)/.12)): box(-(W/2 + .45) + k*.12, cy - .55, TT + .15, -(W/2 + .45) + k*.12 + .03, cy + .55, TT + .155, CLOTH)
for s in (-1, 1):
    bar((-(W/2 + .45), cy + s*.5, TT + 1.08), (W/2 + .45, cy + s*.5, TT + 1.08), .03, FMET); bar((-(W/2 + .45), cy + s*.5, TT + .6), (W/2 + .45, cy + s*.5, TT + .6), .02, FMET)
    for k in range(9): x = -(W/2 + .45) + k*(W + .9)/8; bar((x, cy + s*.5, TT + .15), (x, cy + s*.5, TT + 1.1), .025, FMET)
for k in range(-2, 3):                                                           # the lamp cans hanging off the front span
    x = k*2.6; bar((x, Dd/2 + .3, TT - .35), (x, Dd/2 + .3, TT - .55), .02, CLOTH)
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=.18, radius2=.25, depth=.45)
    me = bpy.data.meshes.new("can"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("can", me); col.objects.link(o); me.materials.append(CLOTH)
    me.transform(Matrix.Translation((x, Dd/2 + .45, TT - .75)) @ Matrix.Rotation(-.9, 4, 'X')); put(o)
    ball((x, Dd/2 + .62, TT - .92), .14, BULB, 8)
for s in (-1, 1):                                                                # a festoon of bulbs from the truss tops to the ground pegs
    P = [(s*(W/2 + .3 + (k/9)*4), Dd/2 + .3 + (k/9)*3, TT - (k/9)*7.2 + math.sin(k/9*math.pi)*-.6) for k in range(10)]
    for k in range(10): ball(P[k], .07, BULB, 6)
    for k in range(9): bar(P[k], P[k + 1], .012, CLOTH)                       # the wire they hang on
# ======== the grandstand
cur = "ff_grandstand"; groups[cur] = []
rows, rd, rh, v0, v1 = 8, .9, .34, -12., 12.
for k in range(rows):
    x0 = -2.5 + k*rd; z = (k + 1)*rh
    box(x0, v0, z - rh, x0 + rd, v1, z - .05, WHITE if k % 2 else PLANK2)                 # the riser, painted
    box(x0 - .03, v0, z - .05, x0 + rd*.55, v1, z, PLANK)                                 # the seat plank (front half)
    box(x0 + rd*.6, v0, z - .08, x0 + rd, v1, z - .03, PLANK2)                            # the footboard behind it
    for j in range(13): y = v0 + .5 + j*(v1 - v0 - 1)/12; box(x0 + .02, y - .02, z - rh + .02, x0 + .05, y + .02, z - .06, FMET)   # brackets
for j in range(1, 6):                                                            # aisle numbers painted on the risers
    y = v0 + j*(v1 - v0)/6
    for k in range(rows): box(-2.5 + k*rd - .01, y - .12, (k + 1)*rh - .26, -2.5 + k*rd, y + .12, (k + 1)*rh - .12, YEL)
back = -2.5 + rows*rd
box(back, v0, 0, back + .3, v1, rows*rh + 3.4, BLUEP)
for j in range(17): y = v0 + j*(v1 - v0)/16; box(back - .04, y - .05, rows*rh, back, y + .05, rows*rh + 3.3, mat("FF_blue2", (.15, .24, .46), .6) if "FF_blue2" not in bpy.data.materials else bpy.data.materials["FF_blue2"])
for s in (-1, 1):                                                                # the side walls, stepped to follow the rows
    yy = v1 if s > 0 else v0
    pts = [(-2.5, 0)] + [(-2.5 + k*rd, (k + 1)*rh + 1) for k in range(rows)] + [(back, rows*rh + 1), (back, 0)]
    vs = [(x, yy - .075, z) for (x, z) in pts] + [(x, yy + .075, z) for (x, z) in pts]; n = len(pts)
    fs = [tuple(range(n))[::-1], tuple(range(n, 2*n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    me = bpy.data.meshes.new("side"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("side", me); col.objects.link(o); me.materials.append(PLANK); put(o)
    bar((-2.4, yy + s*.1, .9), (back - .1, yy + s*.1, rows*rh + 1.9), .04, FMET)
top = rows*rh + 3.2
for y in (v0, (v0 + v1)/2, v1): bar((-2.6, y, 0), (-2.6, y, top), .09, FMET); bar((-2.6, y, top - .1), (back, y, top + 1.0), .06, FMET)
for k in range(12):                                                             # the roof: tin strips, low at the front (-X), high at the back
    y0_ = v0 - .3 + k*(v1 - v0 + .6)/12; y1_ = y0_ + (v1 - v0 + .6)/12 + .02
    quadbox([(-3.8, y0_, top - .1), (back + .4, y0_, top + 1.05), (back + .4, y1_, top + 1.05), (-3.8, y1_, top - .1)], .05 + .025*(k % 2), ROOF)
box(-3.85, v0 - .3, top - .5, -3.75, v1 + .3, top - .05, WHITE)
for k in range(13): x0 = -3.8; y = v0 + k*(v1 - v0)/12; box(x0 - .02, y - .04, top - .48, x0, y + .04, top - .05, REDP)
for y in (v0 + .5, (v0 + v1)/2, v1 - .5):                                        # pennant flags along the roof's front
    bar((-3.7, y, top), (-3.7, y, top + 2.2), .03, FMET)
    vs = [(-3.7, y, top + 2.15), (-3.7, y + .9, top + 1.9), (-3.7, y, top + 1.65)]; vs += [(v[0] + .02, v[1], v[2]) for v in vs]
    me = bpy.data.meshes.new("pf"); me.from_pydata(vs, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate(); o = bpy.data.objects.new("pf", me); col.objects.link(o); me.materials.append(REDP); put(o)
box(-2.55, -2.5, top + .1, -2.5, 2.5, top + .7, WHITE)                           # where the code's GRANDSTAND sign hangs (a backing board)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/fair_stage.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["ff_stage"].location = (0, -24, 0); roots["ff_grandstand"].location = (20, -2, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.95, .7, .55, 1); bg.inputs[1].default_value = .45
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.42, .45, .22), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.0; sun.color = (1, .82, .62); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(200))
cd = bpy.data.cameras.new("C"); cd.lens = 24; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-12, 6, 5); cam.rotation_euler = (Vector((6, -18, 4)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/fair_stage.png"; bpy.ops.render.render(write_still=True)
