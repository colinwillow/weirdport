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

# fair_kit.py -- Hollow Creek's fairground pieces as art, at buildFairground's numbers (the code keeps every collider, the
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
R, HUB = 8., 9.6
# ======== the wheel's frame
cur = "ff_wheel_frame"; groups[cur] = []
for s in (-1, 1):
    for a in (-1, 1): bar((a*3.2, s*1.3, 0), (a*.15, s*1.3, HUB), .13, WHITE)
    for z in (3.0, 6.0): bar((-3.2*(1 - z/HUB) - .05, s*1.3, z), (3.2*(1 - z/HUB) + .05, s*1.3, z), .07, WHITE)
    bar((-2.2, s*1.3, 3.0), (2.0, s*1.3, 6.0), .05, WHITE); bar((2.2, s*1.3, 3.0), (-2.0, s*1.3, 6.0), .05, WHITE)
    for a in (-1, 1): box(a*3.2 - .3, s*1.3 - .3, -.3, a*3.2 + .3, s*1.3 + .3, .2, STONE)
    cylz(0, s*1.3, HUB - .25, HUB + .25, .28, DARK, 12)
bar((0, -1.5, HUB), (0, 1.5, HUB), .12, DARK)
box(-.8, -1.7, 0, .8, 1.7, 2.5, REDP); box(-.9, -1.8, 2.5, .9, 1.8, 2.65, WHITE)
for k in range(5): box(.8, -1.5 + k*.75, .5, .84, -1.5 + k*.75 + .35, 2.2, YEL)
box(.8, -1.2, 1.0, .9, 1.2, 1.1, WHITE)                                         # a ledge to lean on
for k in range(3): box(1.0 + k*.45, -.8, 0, 1.45 + k*.45, .8, .15*(k + 1), WOOD)  # three steps up to the cars at the bottom
# ======== the rotor (Blender XZ plane, axle Y)
cur = "ff_wheel_rotor"; groups[cur] = []
NS = 16
for s in (-1, 1):
    for k in range(48):                                                         # the rims as 48 bars
        a0, a1 = k/48*2*math.pi, (k + 1)/48*2*math.pi
        bar((R*math.cos(a0), s*.6, R*math.sin(a0)), (R*math.cos(a1), s*.6, R*math.sin(a1)), .1, WHITE)
        b0, b1 = (R - .7)*math.cos(a0), (R - .7)*math.sin(a0); c0, c1 = (R - .7)*math.cos(a1), (R - .7)*math.sin(a1)
        bar((b0, s*.6, b1), (c0, s*.6, c1), .05, REDP)                          # an inner rim, red
    for k in range(NS):
        a = k/NS*2*math.pi; bar((.3*math.cos(a), s*.6, .3*math.sin(a)), (R*math.cos(a), s*.6, R*math.sin(a)), .05, WHITE)
    for k in range(32): a = (k + .5)/32*2*math.pi; ball(((R + .14)*math.cos(a), s*.6, (R + .14)*math.sin(a)), .09, BULB, 6)
for k in range(8): a = k/8*2*math.pi; bar((R*math.cos(a), -.65, R*math.sin(a)), (R*math.cos(a), .65, R*math.sin(a)), .06, DARK)   # the car axles
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=.6, radius2=.6, depth=1.5)
me = bpy.data.meshes.new("hub"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("hub", me); col.objects.link(o); me.materials.append(REDP); me.transform(Matrix.Rotation(math.pi/2, 4, 'X')); put(o)
for k in range(10): a = k/10*2*math.pi; ball((.75*math.cos(a), -.78, .75*math.sin(a)), .07, BULB, 6); ball((.75*math.cos(a), .78, .75*math.sin(a)), .07, BULB, 6)
# ======== one car: a tub with a striped canopy, centre at the origin, hanging from +.7
cur = "ff_wheel_car"; groups[cur] = []
box(-.6, -.7, -.55, .6, .7, .05, REDP, bev=.06); box(-.5, -.6, -.1, .5, .6, .08, DARK)
for s in (-1, 1): box(s*.55 - .03, -.03, .05, s*.55 + .03, .03, .55, WHITE)
for k in range(4):                                                              # the canopy, four stripes, from points
    y0, y1 = -.7 + k*.35, -.7 + (k + 1)*.35; m = WHITE if k % 2 else YEL
    quadbox([(-.66, y0, .5), (0, y0, .62), (0, y1, .62), (-.66, y1, .5)], .03, m); quadbox([(0, y0, .62), (.66, y0, .5), (.66, y1, .5), (0, y1, .62)], .03, m)
bar((0, 0, .62), (0, 0, .7), .04, DARK); box(-.62, -.72, -.3, .62, .72, -.22, WHITE)
# ======== two midway stalls (red / blue stripes)
for name, SC in (("ff_stall_red", REDP), ("ff_stall_blue", BLUEP)):
    cur = name; groups[cur] = []
    box(-.5, -2.1, 0, .5, 2.1, 1.0, WOOD); box(-.55, -2.15, 1.0, .6, 2.15, 1.08, WHITE)
    for k in range(6): box(.5, -2.05 + k*.7, .1, .54, -2.05 + k*.7 + .35, .95, SC)        # a striped skirt on the counter front
    box(-2.7, -2.2, 0, -.5, 2.2, 2.6, WHITE); box(-2.75, -2.25, 2.6, -.45, 2.25, 2.7, SC)
    box(-.52, -1.8, 1.1, -.48, 1.8, 2.3, DARK)                                             # the dark of the booth behind the counter
    for k in range(6):                                                                     # the canopy, sloping down to the front (u+), scalloped
        y0, y1 = -2.1 + k*.7, -2.1 + (k + 1)*.7; m = WHITE if k % 2 else SC
        quadbox([(-1.2, y0, 3.12), (1.4, y0, 2.66), (1.4, y1, 2.66), (-1.2, y1, 3.12)], .05, m)
        vs = [(1.4, y0, 2.66), (1.4, y1, 2.66), (1.42, (y0 + y1)/2, 2.4)]; vs += [(v[0] + .02, v[1], v[2]) for v in vs]
        me = bpy.data.meshes.new("v"); me.from_pydata(vs, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate()
        o = bpy.data.objects.new("v", me); col.objects.link(o); me.materials.append(m); put(o)
    for s in (-1, 1): cylz(1.2, s*2.1, 0, 2.75, .05, FMET, 8)
    for k in range(9): ball((1.45, -2.0 + k*.5, 2.38), .06, BULB, 6)
    for k in range(4): box(-2.3 + k*.45, -1.9, 1.3, -2.0 + k*.45, -1.6, 1.6, (YEL, SC, WHITE, YEL)[k])   # prizes on a shelf
# ======== the livestock barn: red planks, white trim, a gambrel roof, the big door on -X with a hay door over it
cur = "ff_livebarn"; groups[cur] = []
u0, u1, v0, v1, E = 0., 6., -4., 4., 4.5
box(u0, v0, -.3, u1, v1, E, REDP)
for k in range(int((v1 - v0)/.6)): y_ = v0 + .3 + k*.6; box(u0 - .04, y_ - .03, 0, u0, y_ + .03, E, RED2); box(u1, y_ - .03, 0, u1 + .04, y_ + .03, E, RED2)
for (a, b) in ((u0, v0), (u0, v1), (u1, v0), (u1, v1)): box(a - .12, b - .12, 0, a + .12, b + .12, E + .05, WHITE)
box(u0 - .08, -1.2, 0, u0 - .02, 1.2, 3.2, DARK)
for s in (-1, 1):
    box(u0 - .2, s*1.2 - .1 if s > 0 else -1.3, 0, u0 - .1, s*1.2 + .1 if s > 0 else -1.1, 3.3, WHITE)
    bar((u0 - .15, -1.1, .2), (u0 - .15, 1.1, 3.0), .05, WHITE) if s > 0 else bar((u0 - .15, 1.1, .2), (u0 - .15, -1.1, 3.0), .05, WHITE)
box(u0 - .14, -1.3, 3.2, u0 - .1, 1.3, 3.35, WHITE); box(u0 - .08, -.6, 5.1, u0 - .02, .6, 6.0, DARK); box(u0 - .12, -.7, 5.0, u0 - .08, .7, 6.1, WHITE)
uc = (u0 + u1)/2; prof = [(-4.3, E - .05), (-3.2, E + 1.4), (0, E + 2.4), (3.2, E + 1.4), (4.3, E - .05)]   # gambrel profile across v
for i in range(4):
    (va, za), (vb, zb) = prof[i], prof[i + 1]
    pts = [(u0 - .4, va, za), (u1 + .4, va, za), (u1 + .4, vb, zb), (u0 - .4, vb, zb)]
    if vb < va: pts = [pts[1], pts[0], pts[3], pts[2]]
    quadbox(pts if i < 2 else [pts[1], pts[0], pts[3], pts[2]], .1, ROOF if i in (0, 3) else SLATE2 if False else ROOF)
for x in (u0, u1):                                                              # the gambrel gables
    vs = [(x, -4.0, E), (x, 4.0, E), (x, 3.0, E + 1.35), (x, 0, E + 2.35), (x, -3.0, E + 1.35)]
    me = bpy.data.meshes.new("gg"); me.from_pydata(vs, [], [(0, 1, 2, 3, 4)] if x > uc else [(4, 3, 2, 1, 0)]); me.validate(); o = bpy.data.objects.new("gg", me); col.objects.link(o); me.materials.append(REDP); put(o)
box(uc - .2, -.2, E + 2.4, uc + .2, .2, E + 3.0, WHITE); quadbox([(uc - .35, -.35, E + 3.0), (uc + .35, -.35, E + 3.0), (uc + .35, .35, E + 3.0), (uc - .35, .35, E + 3.0)], .2, ROOF)   # a cupola
box(u0 - .5, -2.2, 3.6, u0 - .06, 2.2, 4.1, WHITE)                               # a board for the barn's name (blank)
# ======== the gate: posts, the beam, an arch of bulbs behind the code's sign, the ticket booth
cur = "ff_gate"; groups[cur] = []
for s in (-1, 1):
    box(s*5 - .22, -.22, 0, s*5 + .22, .22, 6.0, WHITE); box(s*5 - .3, -.3, 0, s*5 + .3, .3, .5, REDP); ball((s*5, 0, 6.25), .25, REDP, 10)
    for k in range(3): box(s*5 - .23, -.23, 1.2 + k*1.5, s*5 + .23, .23, 1.35 + k*1.5, REDP)
box(-5.2, -.15, 5.6, 5.2, .15, 6.2, WOOD)
N = 24
for k in range(N):                                                              # the arch: a curve from post top to post top, behind the sign
    a0, a1 = math.pi*k/N, math.pi*(k + 1)/N
    p0 = (5*math.cos(a0), .35, 6.0 + 2.6*math.sin(a0)); p1 = (5*math.cos(a1), .35, 6.0 + 2.6*math.sin(a1)); bar(p0, p1, .1, REDP)
    if k % 2 == 0: ball((5.15*math.cos(a0), .35, 6.0 + 2.75*math.sin(a0)), .09, BULB, 6)
for k in range(5): a = math.pi*(k + 1)/6; bar((0, .35, 6.2), (4.9*math.cos(a), .35, 6.0 + 2.55*math.sin(a)), .05, WHITE)   # sunburst spokes
for k in range(11): ball((-5 + k, -.2, 5.5), .08, BULB, 6)
bx, by = 7.5, -1
box(bx - 1, by - 1, 0, bx + 1, by + 1, 2.6, WHITE)
for k in range(5): box(bx - 1.02, by - 1 + .1 + k*.4, 0, bx - 1, by - 1 + .3 + k*.4, 2.6, REDP)
box(bx - 1.03, by - .6, 1.1, bx - .98, by + .6, 1.9, DARK); box(bx - 1.15, by - .7, 1.05, bx - .95, by + .7, 1.12, WOOD)
for s in (-1, 1): quadbox([(bx - 1.25, by - 1.25, 2.6), (bx + 1.25, by - 1.25, 2.6), (bx + 1.25, by + 1.25, 2.6), (bx - 1.25, by + 1.25, 2.6)], .12, REDP) if s < 0 else None
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=1.6, radius2=0, depth=1.0)
me = bpy.data.meshes.new("pyr"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("pyr", me); col.objects.link(o); me.materials.append(WHITE); me.transform(Matrix.Translation((bx, by, 3.22)) @ Matrix.Rotation(math.pi/4, 4, 'Z')); put(o)
ball((bx, by, 3.85), .12, REDP, 8)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/fair_kit.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
# preview: the wheel assembled (rotor at the hub, cars at the rim), a stall, the barn and the gate, in the fair's own layout
roots["ff_wheel_frame"].location = (-19, 21, 0); roots["ff_wheel_rotor"].location = (-19, 21, 9.6); roots["ff_wheel_rotor"].rotation_euler = (0, 0, 0)
cars = roots["ff_wheel_car"]; mc = cars.children[0]
for k in range(8):
    a = k/8*2*math.pi; c = bpy.data.objects.new("car%d" % k, None); col.objects.link(c); mm = mc.copy(); col.objects.link(mm); mm.parent = c
    c.location = (-19 + 8*math.cos(a), 21, 9.6 + 8*math.sin(a) - .7)
cars.location = (999, 0, 0)
roots["ff_stall_red"].location = (-19 + 4, 4, 0); roots["ff_stall_blue"].location = (-19 + 4, -3, 0); roots["ff_livebarn"].location = (16, 22, 0); roots["ff_gate"].location = (0, 25, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.95, .7, .55, 1); bg.inputs[1].default_value = .45
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.42, .45, .22), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.0; sun.color = (1, .82, .62); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(65), 0, math.radians(150))
cd = bpy.data.cameras.new("C"); cd.lens = 24; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (12, -14, 7); cam.rotation_euler = (Vector((-4, 18, 5.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/fair_kit.png"; bpy.ops.render.render(write_still=True)
