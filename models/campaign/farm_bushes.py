# farm_bushes.py -- three bushes and a hedge piece for the farm (replacing the faceted icosahedron clumps in the boundaries pass).
# CONTRACT: one GLB, one root per piece, origin on the ground at its centre, Blender X = along a hedge run (three x). All smooth,
# soft and rounded (the Sites painting's shapes: sage and deep green, a few loud orange/red accents), vertex-coloured, opaque.
#   fb_round   1.6 m round bush (three overlapping soft lumps)        fb_cypress  2.6 m tall dark cone (the painting's cypress)
#   fb_flower  0.9 m low mound with orange/red blooms                  fb_hedge    one 2.7 m hedge piece on its earth bank (FARMLAND.piece)
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix, noise
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection; rnd = random.Random(3)
def mat(name, rgb, rough=.85):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; return m
SAGE = mat("FB_sage", (.47, .66, .38)); SAGE2 = mat("FB_sage_light", (.62, .78, .45)); DEEP = mat("FB_deep", (.13, .36, .16))
BANK = mat("FB_bank", (.38, .45, .22)); EARTH = mat("FB_earth", (.42, .3, .2)); ORANGE = mat("FB_orange", (.98, .52, .1), .6); RED = mat("FB_red", (.86, .14, .12), .6)
BARK = mat("FB_bark", (.33, .23, .16))
def blob(name, cx, cy, cz, rx, ry, rz, m, sub=3, wob=.12, seed=0):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0)
    off = Vector((seed*3.1, seed*1.7, seed*2.3))
    for v in bm.verts:
        n = v.co.normalized(); d = 1 + wob*noise.noise(n*1.8 + off)
        v.co = Vector((n.x*rx*d, n.y*ry*d, max(n.z*rz*d, -cz)))                            # flattened at the GROUND: it sits, never floats
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = (cx, cy, cz); me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return o
def cone(name, cx, cy, h, r, m):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=r, radius2=0.0, depth=h)
    for v in bm.verts:                                                                     # soften the point, belly the sides
        t = (v.co.z + h/2)/h; v.co.x *= 1 + .18*math.sin(t*math.pi); v.co.y *= 1 + .18*math.sin(t*math.pi)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = (cx, cy, h/2)
    me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return o
pieces = {}
def grp(name, parts):
    r = bpy.data.objects.new(name, None); col.objects.link(r); pieces[name] = r
    for p in parts: p.parent = r
    return r
# round bush: three soft lumps, the top one paler (light from above)
grp("fb_round", [blob("rb_a", -.35, 0, .55, .7, .65, .6, SAGE, seed=1), blob("rb_b", .4, .1, .5, .62, .6, .55, SAGE, seed=2),
                 blob("rb_c", 0, -.05, .95, .55, .5, .5, SAGE2, seed=3)])
# cypress: a tall deep cone on a stub of trunk
grp("fb_cypress", [cone("cy_body", 0, 0, 2.5, .55, DEEP), blob("cy_foot", 0, 0, .05, .3, .3, .12, BARK, sub=1, wob=0)])
# flower mound: a low lump with blooms dotted over its top
P = [blob("fl_mound", 0, 0, .3, .55, .5, .38, SAGE, seed=4)]
for k in range(9):
    a = rnd.uniform(0, 6.28); r = rnd.uniform(.1, .42); z = .3 + .38*math.sqrt(max(0, 1 - (r/.55)**2)) - .02
    P.append(blob("fl_bloom%d" % k, math.cos(a)*r, math.sin(a)*r*.9, z, .09, .09, .07, ORANGE if k % 3 else RED, sub=1, wob=0))
grp("fb_flower", P)
# hedge piece (sub 2 throughout: it repeats every 2.7 m of every field edge, so it is the one piece that has to be cheap): a long lumpy earth bank and a hedge of four soft clumps along it, the top line wandering (2.7 m = FARMLAND.piece)
L = 2.7; P = [blob("hd_bank", 0, 0, 0, L*.6, .95, .32, BANK, sub=2, seed=5, wob=.06)]
for k in range(4):
    x = -L/2 + (k + .5)*L/4 + rnd.uniform(-.15, .15); r = rnd.uniform(.55, .72)
    P.append(blob("hd_clump%d" % k, x, rnd.uniform(-.08, .08), .3 + r*.8, r*1.25, .6, r, DEEP, sub=2, seed=6 + k))
    P.append(blob("hd_cap%d" % k, x + rnd.uniform(-.2, .2), -.08, .45 + r*1.45, r*.7, .4, r*.45, SAGE, sub=2, seed=20 + k))
if True: P.append(blob("hd_bloom", .5, -.45, 1.05, .1, .1, .08, ORANGE, sub=1, wob=0))
grp("fb_hedge", P)
out = "/home/claude/weirdport/models/campaign"
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in pieces.values():
    r.select_set(True)
    for c_ in r.children_recursive: c_.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(out, "farm_bushes.glb"), export_format='GLB', use_selection=True, export_extras=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
for k, r in pieces.items(): print(k, sum(len(c_.data.polygons) for c_ in r.children_recursive if c_.type == 'MESH'))
# preview: a hedge run with the bushes in front of it
lay = [("fb_hedge", (-4.05, 2, 0)), ("fb_round", (-3, -.5, 0)), ("fb_cypress", (-.8, 1.2, 0)), ("fb_flower", (.6, -.6, 0)), ("fb_round", (2.2, .3, 0)), ("fb_cypress", (3.6, 1.6, 0)), ("fb_flower", (3.2, -1.0, 0))]
used = set()
for name, p in lay:
    r = pieces[name]
    if name in used:
        d = bpy.data.objects.new(name + "_dup", None); col.objects.link(d)
        for c_ in r.children: cc = c_.copy(); col.objects.link(cc); cc.parent = d
        r = d
    used.add(name); r.location = p
for k in (1, 2):
    d = bpy.data.objects.new("hedge_dup%d" % k, None); col.objects.link(d)
    for c_ in pieces["fb_hedge"].children: cc = c_.copy(); col.objects.link(cc); cc.parent = d
    d.location = (-4.05 + k*2.7, 2, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.render.resolution_x = 1280; sc.render.resolution_y = 720
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (.55, .72, .95, 1); w.node_tree.nodes["Background"].inputs[1].default_value = .45; sc.view_settings.view_transform = "Standard"
g = bpy.data.meshes.new("g"); g.from_pydata([(-30, -30, 0), (30, -30, 0), (30, 30, 0), (-30, 30, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.85, .7, .38), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .95, .85); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-40))
cd = bpy.data.cameras.new("C"); cd.lens = 30; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (0, -9, 2.6); cam.rotation_euler = (Vector((0, 0, .9)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/farm_bushes.png"; bpy.ops.render.render(write_still=True)
