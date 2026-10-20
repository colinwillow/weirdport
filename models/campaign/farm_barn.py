# farm_barn.py -- Gristle Farm's barn and silo as art (buildFarm still owns every collider, the loft floor, the bale stair, the
# rope, the lean-to and the silo's ladder and landing: this is the SHELL and its dressing, at buildFarm's exact numbers).
# CONTRACT: Blender X = the frame's u (across, 10 m), Blender +Y = the frame's +v (back, the loft door), so the big doors face
# Blender -Y. Origin = (bu, bv) at the FLOOR (y0): the plinth runs down to -1.2 to bury itself on any slope.
#   fb_barn   W 10 x D 14, eaves 5.0, ridge 7.4, walls .3, roof .6 overhang; front door 4 x 3.6 (open, X-braced leaves at
#             +-4.0 just proud of the wall); back loft door 3 wide, 2.9..4.6, with its hook beam (the rope hangs at u 0, v D2+.75)
#   fb_silo   r 2.3/2.4, 11 m drum + dome, origin at its foot centre (buildFarm: u bu+W2+3.4, v bv+D2+1.5); ladder NOT included
import bpy, bmesh, math, os, random
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection; rnd = random.Random(5)
def mat(name, rgb, rough=.85, metal=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal; return m
RED = mat("FBN_red", (.62, .16, .12)); RED2 = mat("FBN_red_faded", (.7, .3, .22)); TRIM = mat("FBN_trim", (.9, .87, .8)); ROOF = mat("FBN_roof", (.22, .27, .26))
ROOF2 = mat("FBN_roof_moss", (.3, .36, .24)); STONE = mat("FBN_stone", (.52, .5, .46), 1); STONE2 = mat("FBN_stone_dark", (.38, .37, .34), 1)
WOOD = mat("FBN_wood", (.42, .29, .18)); DARK = mat("FBN_dark", (.1, .09, .08)); METAL = mat("FBN_metal", (.66, .7, .72), .45, .4)
RUST = mat("FBN_rust", (.5, .27, .14), .8); INSIDE = mat("FBN_inside", (.2, .13, .09), 1)
objs = {"fb_barn": [], "fb_silo": []}; cur = "fb_barn"
def add(o): objs[cur].append(o); return o
def box(name, x0, y0, z0, x1, y1, z1, m, rot=None, piv=None, bev=0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co = Vector(((v.co.x + .5)*(x1 - x0) + x0, (v.co.y + .5)*(y1 - y0) + y0, (v.co.z + .5)*(z1 - z0) + z0))
    if bev: bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bev, segments=1, affect='EDGES')
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    if rot:
        from mathutils import Matrix, Euler
        p = Vector(piv or ((x0 + x1)/2, (y0 + y1)/2, (z0 + z1)/2)); M = Matrix.Translation(p) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Translation(-p); me.transform(M)
    return add(o)
def mesh(name, verts, faces, m, smooth=False):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.validate(); o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = smooth
    return add(o)
BW, BD, EAVE, RIDGE, T = 10., 14., 5., 7.4, .3; W2, D2 = BW/2, BD/2
# ---- plinth: rough stone courses, a slightly proud top course (the formula's plinth), buried to -1.2
box("plinth", -W2 - .3, -D2 - .3, -1.2, W2 + .3, D2 + .3, -.05, STONE2)
box("plinth_top", -W2 - .38, -D2 - .38, -.25, W2 + .38, D2 + .38, .0, STONE, bev=.04)
for k in range(26):                                      # odd stones proud of the face: it is stone, not a slab
    s = rnd.choice((0, 1, 2, 3)); t = rnd.uniform(-.9, .9); z = rnd.uniform(-.75, -.35); w = rnd.uniform(.35, .7)
    if s < 2: x = t*W2; y = (-D2 - .33) if s == 0 else (D2 + .33); box("st%d" % k, x - w/2, y - .04, z - .12, x + w/2, y + .04, z + .12, STONE)
    else: y = t*D2; x = (-W2 - .33) if s == 2 else (W2 + .33); box("st%d" % k, x - .04, y - w/2, z - .12, x + .04, y + w/2, z + .12, STONE)
# ---- walls (exact openings), dark inside skin so the open door shows a barn interior and not red
def wall(name, x0, y0, x1, y1, z0, z1):
    box(name, x0, y0, z0, x1, y1, z1, RED)
wall("wf_l", -W2, -D2 - T/2, -2, -D2 + T/2, 0, EAVE); wall("wf_r", 2, -D2 - T/2, W2, -D2 + T/2, 0, EAVE); wall("wf_top", -2, -D2 - T/2, 2, -D2 + T/2, 3.6, EAVE)
wall("wb_l", -W2, D2 - T/2, -1.5, D2 + T/2, 0, EAVE); wall("wb_r", 1.5, D2 - T/2, W2, D2 + T/2, 0, EAVE)
wall("wb_lo", -1.5, D2 - T/2, 1.5, D2 + T/2, 0, 2.9); wall("wb_hi", -1.5, D2 - T/2, 1.5, D2 + T/2, 4.6, EAVE)
wall("ws_l", -W2 - T/2, -D2, -W2 + T/2, D2, 0, EAVE); wall("ws_r", W2 - T/2, -D2, W2 + T/2, D2, 0, EAVE)
box("in_l", -W2 + T/2, -D2 + T/2, 0, -W2 + T/2 + .02, D2 - T/2, EAVE, INSIDE); box("in_r", W2 - T/2 - .02, -D2 + T/2, 0, W2 - T/2, D2 - T/2, EAVE, INSIDE)
box("in_b", -W2, D2 - T/2 - .02, 0, W2, D2 - T/2, 2.9, INSIDE); box("in_f", -W2, -D2 + T/2, 3.6, W2, -D2 + T/2 + .02, EAVE, INSIDE)
# battens: a vertical strip every .7 m on all four outside faces (board-and-batten is what makes a barn read at 60 m)
for x in [i*.7 - W2 + .35 for i in range(15)]:
    if abs(x) > 2.15: box("bf%.1f" % x, x - .04, -D2 - T/2 - .05, 0, x + .04, -D2 - T/2, EAVE, RED2)
    if abs(x) > 1.65: box("bb%.1f" % x, x - .04, D2 + T/2, 0, x + .04, D2 + T/2 + .05, EAVE, RED2)
    else: box("bbl%.1f" % x, x - .04, D2 + T/2, 0, x + .04, D2 + T/2 + .05, 2.9, RED2); box("bbh%.1f" % x, x - .04, D2 + T/2, 4.6, x + .04, D2 + T/2 + .05, EAVE, RED2)
for y in [i*.7 - D2 + .35 for i in range(20)]:
    for s in (-1, 1): box("bs%.1f%d" % (y, s), s*(W2 + T/2) - .025 + s*.025, y - .04, 0, s*(W2 + T/2) + .025 + s*.025, y + .04, EAVE, RED2)
# trim: corner boards, an eave band all round, the door and loft frames, a string course at the loft floor (2.9) on the sides
for a in (-1, 1):
    for b in (-1, 1): box("cn%d%d" % (a, b), a*(W2 + .05) - .17, b*(D2 + .05) - .17, 0, a*(W2 + .05) + .17, b*(D2 + .05) + .17, EAVE + .1, TRIM)
for s in (-1, 1):
    box("eave_s%d" % s, s*(W2 + .2) - .1, -D2 - .2, EAVE - .3, s*(W2 + .2) + .1, D2 + .2, EAVE, TRIM)
    box("string_s%d" % s, s*(W2 + .2) - .06, -D2, 2.85, s*(W2 + .2) + .06, D2, 2.98, TRIM)
for (x0, x1, z0, z1, y) in ((-2.25, -2.0, 0, 3.75, -D2 - .2), (2.0, 2.25, 0, 3.75, -D2 - .2), (-2.25, 2.25, 3.6, 3.85, -D2 - .2)):
    box("dfr", x0, y - .1, z0, x1, y + .1, z1, TRIM)
for (x0, x1, z0, z1) in ((-1.7, -1.5, 2.8, 4.75), (1.5, 1.7, 2.8, 4.75), (-1.7, 1.7, 4.6, 4.8), (-1.75, 1.75, 2.75, 2.9)):
    box("lfr", x0, D2 + .1, z0, x1, D2 + .3, z1, TRIM)
# the big doors, swung open flat against the front wall, white X braces and a frame round each leaf
for s in (-1, 1):
    c = s*4.0; y = -D2 - .25
    box("door%d" % s, c - 1, y - .06, .05, c + 1, y + .06, 3.5, RED)
    for (x0, x1, z0, z1) in ((c - 1, c + 1, .05, .25), (c - 1, c + 1, 3.3, 3.5), (c - 1, c - .8, .05, 3.5), (c + .8, c + 1, .05, 3.5), (c - 1, c + 1, 1.7, 1.86)):
        box("dtr", x0, y - .12, z0, x1, y - .06, z1, TRIM)
    for sg in (-1, 1):
        L = math.hypot(1.6, 1.45)
        box("dx", c - L/2, y - .13, .975 - .07, c + L/2, y - .07, .975 + .07, TRIM, rot=(0, sg*math.atan2(1.45, 1.6), 0))
        box("dx", c - L/2, y - .13, 2.6 - .07, c + L/2, y - .07, 2.6 + .07, TRIM, rot=(0, sg*math.atan2(1.45, 1.6), 0))
    box("hinge%d" % s, s*2.0 - .12, y - .14, 2.9, s*2.0 + .12, y - .04, 3.0, DARK)
# the loft door's own leaf, swung out to one side, and the hook beam over it (the rope hangs from its end at v D2+.75)
box("loftleaf", 1.7, D2 + .3, 2.95, 3.2, D2 + .4, 4.55, RED2)
box("hookbeam", -.15, D2 - .5, EAVE + .65, .15, D2 + 1.0, EAVE + .95, WOOD)
box("hook", -.04, D2 + .7, EAVE + .5, .04, D2 + .8, EAVE + .67, DARK)
# gables (red), with their own battens, a trim rake along each edge, and a round vent in each
for s in (-1, 1):
    y = s*D2; mesh("gab%d" % s, [(-W2 - .15, y - T/2, EAVE), (W2 + .15, y - T/2, EAVE), (0, y - T/2, RIDGE), (-W2 - .15, y + T/2, EAVE), (W2 + .15, y + T/2, EAVE), (0, y + T/2, RIDGE)],
                   [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], RED)
    for x in [i*.7 - W2 + .35 for i in range(15)]:
        top = EAVE + (RIDGE - EAVE)*(1 - abs(x)/W2) - .05
        if top > EAVE + .1: box("gb", x - .04, y + s*(T/2), EAVE, x + .04, y + s*(T/2 + .05), top, RED2)
    a = math.atan2(RIDGE - EAVE, W2); L = math.hypot(W2 + .6, (RIDGE - EAVE)*(W2 + .6)/W2)
    for sx in (-1, 1):
        box("rake", -L/2, y + s*(.6 + T/2) - .08, -.1, L/2, y + s*(.6 + T/2) + .08, .1, TRIM, rot=(0, sx*a, 0), piv=(0, 0, 0))
        objs[cur][-1].data.transform(__import__('mathutils').Matrix.Translation((sx*(W2 + .6)/2, 0, RIDGE + .12 - (RIDGE - EAVE)*(W2 + .6)/W2/2)))
    bmv = bmesh.new(); bmesh.ops.create_cone(bmv, cap_ends=True, segments=16, radius1=.42, radius2=.42, depth=.12)
    me = bpy.data.meshes.new("vent"); bmv.to_mesh(me); bmv.free(); o = bpy.data.objects.new("vent", me); col.objects.link(o); me.materials.append(TRIM)
    me.transform(__import__('mathutils').Matrix.Rotation(math.pi/2, 4, 'X')); o.location = (0, y + s*(T/2 + .06), 6.35); add(o)
    box("ventdark", -.28, y + s*(T/2 + .1) - .02, 6.07, .28, y + s*(T/2 + .1) + .02, 6.63, DARK)
# roof: two slabs at buildFarm's slope, .6 overhang at eaves and ends, shingle COURSES stepped down each (a course every .5 m of
# slope, each lapping the one below), a ridge cap, some courses mossy
run = W2 + .6; rise = (RIDGE - EAVE)*run/W2; ang = math.atan2(RIDGE - EAVE, W2); sl = math.hypot(run, rise)
from mathutils import Matrix
def slab(name, sd, d0, d1, t0, t1, y0, y1, m):
    """a box laid ON the roof: d down the slope from the ridge, t out of it, y along the barn -- built from points, no rotations"""
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda d, t: (sd*(d*ca + t*sa), RIDGE + .08 - d*sa + t*ca)
    vs = []
    for (d, t) in ((d0, t0), (d1, t0), (d1, t1), (d0, t1)):
        x, z = P(d, t); vs += [(x, y0, z)]
    for (d, t) in ((d0, t0), (d1, t0), (d1, t1), (d0, t1)):
        x, z = P(d, t); vs += [(x, y1, z)]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    if sd < 0: f = [tuple(reversed(q)) for q in f]
    return mesh(name, vs, f, m)
for sd in (-1, 1):
    slab("deck%d" % sd, sd, 0, sl, -.12, 0, -D2 - .6, D2 + .6, ROOF)
    n = int(sl/.5)
    for k in range(n):                                        # a course every ~.5 m down the slope, each lapping the one below
        d0 = k*sl/n; d1 = (k + 1)*sl/n + .07; th = .07 + .03*(k % 2)
        slab("sh%d%d" % (sd, k), sd, d0, d1, 0, th, -D2 - .6, D2 + .6, ROOF2 if rnd.random() < .18 else ROOF)
box("ridgecap", -.22, -D2 - .65, RIDGE + .05, .22, D2 + .65, RIDGE + .3, DARK)
# weathervane (thin: nothing to stand on) over the front third of the ridge
box("vane_post", -.03, -D2 + 3 - .03, RIDGE + .3, .03, -D2 + 3 + .03, RIDGE + 1.6, DARK)
box("vane_arrow", -.025, -D2 + 3 - .55, RIDGE + 1.35, .025, -D2 + 3 + .55, RIDGE + 1.42, DARK)
box("vane_tail", -.02, -D2 + 3 + .35, RIDGE + 1.25, .02, -D2 + 3 + .6, RIDGE + 1.55, DARK)
# imperfections: a lamp over the doors, a downpipe at one corner, a patched board, a horseshoe over the door
box("lamp_arm", -.05, -D2 - .2, 4.1, .05, -D2 - .75, 4.2, DARK); box("lamp", -.18, -D2 - .85, 3.9, .18, -D2 - .6, 4.15, METAL)
box("pipe", W2 + .25, -D2 + .1, 0, W2 + .37, -D2 + .22, EAVE, METAL); box("gutter", W2 + .2, -D2 - .5, EAVE - .15, W2 + .45, D2 + .5, EAVE, METAL)
box("gutterL", -W2 - .45, -D2 - .5, EAVE - .15, -W2 - .2, D2 + .5, EAVE, METAL)
box("patch", -W2 - T/2 - .09, 2, 1.0, -W2 - T/2 - .05, 3.3, 2.2, WOOD)
box("shoe", -.15, -D2 - .32, 3.9, .15, -D2 - .28, 4.15, DARK)
# ---- the silo
cur = "fb_silo"; H = 11.
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=24, radius1=2.4, radius2=2.3, depth=H)
me = bpy.data.meshes.new("drum"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("drum", me); col.objects.link(o); me.materials.append(METAL); o.location = (0, 0, H/2 - .1)
for p in me.polygons: p.use_smooth = True
add(o)
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=8, radius=2.36)
for v in [v for v in bm.verts if v.co.z < -1e-4]: bm.verts.remove(v)
me = bpy.data.meshes.new("dome"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("dome", me); col.objects.link(o); me.materials.append(RED); o.location = (0, 0, H - .1)
for p in me.polygons: p.use_smooth = True
add(o)
for k in range(1, 11):                                    # hoops every 1.1 m, and a rust streak or two under some of them
    r = 2.4 - .1*k*1.1/H + .04
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=24, radius1=r, radius2=r, depth=.08)
    me = bpy.data.meshes.new("hoop"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("hoop", me); col.objects.link(o); me.materials.append(DARK); o.location = (0, 0, k*1.1 - .1); add(o)
for k in range(5):
    a = rnd.uniform(0, 6.28); z1 = rnd.uniform(4, 10); r = 2.38 - .1*z1/H + .01
    o = box("rust%d" % k, -.08, r - .01, z1 - rnd.uniform(1.5, 3), .08, r + .02, z1, RUST); o.data.transform(Matrix.Rotation(a, 4, 'Z'))
box("silo_foot", -2.7, -2.7, -1.0, 2.7, 2.7, .15, STONE2)
box("chute", -.3, 2.25, 3.0, .3, 2.75, 9.5, METAL); box("chute_hood", -.4, 2.2, 9.5, .4, 2.9, 10.2, METAL)
box("finial", -.08, -.08, H + 2.2, .08, .08, H + 2.7, DARK)
# ---- one mesh per piece (materials kept as slots): a building is a handful of draws, not 300 objects
roots = {}
for name, L in objs.items():
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in L: o.select_set(True)
    bpy.context.view_layer.objects.active = L[0]; bpy.ops.object.join(); j = bpy.context.view_layer.objects.active; j.name = name + "_mesh"
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    r = bpy.data.objects.new(name, None); col.objects.link(r); j.parent = r; roots[name] = r
    print(name, len(j.data.polygons), "faces", len(j.data.materials), "materials")
out = "/home/claude/weirdport/models/campaign"
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in roots.values():
    r.select_set(True); [c.select_set(True) for c in r.children]
bpy.ops.export_scene.gltf(filepath=os.path.join(out, "farm_barn.glb"), export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
# ---- preview: the silo at its buildFarm offset, the barn from the front quarter in afternoon light
roots["fb_silo"].location = (W2 + 3.4, D2 + 1.5, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-60, -60, -.3), (60, -60, -.3), (60, 60, -.3), (-60, 60, -.3)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.35, .45, .2), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.4; sun.color = (1, .92, .78); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(-35))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
for nm, loc, tgt in (("front", (-17, -26, 6), (1, 0, 4.5)), ("back", (16, 30, 7), (1, 3, 4.5))):
    cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = "/home/claude/campaign/farm_barn_%s.png" % nm; bpy.ops.render.render(write_still=True)
