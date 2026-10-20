# farm_trees.py -- the farm's OAK and WILLOW as art, for `farmTree` (every hedgerow, roadside, orchard and line tree uses it).
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
# CONTRACT: one root each, origin on the ground at the trunk, built at farmTree's s = 1 (scale uniformly by the caller's `s`, turn by
# its random yaw); smooth, soft crowns in the Sites-painting greens, low-poly enough to stand in their hundreds.
#   ft_oak     trunk r .4 -> .24 to 3.4 with a root flare, two limbs out of the fork, the crown centred ~5.3: a big lump r 2.3 and
#              five round it at 1.5 out (r 1.45-1.95) -- the code's own layout
#   ft_willow  a trunk leaning to +X to 2.6, a crown at ~3.6 drooping in long hanging lobes, as the code's willow
LEAF = mat("FT_leaf", (.24, .42, .17)); LEAF2 = mat("FT_leaf2", (.43, .58, .25)); LEAF3 = mat("FT_leaf_dark", (.15, .3, .12)); BARK = mat("FT_bark", (.31, .24, .17), 1)
WLEAF = mat("FT_willow", (.38, .54, .24)); WLEAF2 = mat("FT_willow2", (.28, .44, .19))
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
def blob(name, c, r, m, sub=2, wob=.12, seed=0, floor=True):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0); off = Vector((seed*3.1, seed*1.7, seed*2.3))
    for v in bm.verts:
        n = v.co.normalized(); dd = 1 + wob*noise.noise(n*1.8 + off); z = n.z*r[2]*dd
        v.co = Vector((n.x*r[0]*dd, n.y*r[1]*dd, max(z, -c[2]) if floor else z))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = c; me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return o
def link(name, me, m):
    o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return o
def trunk(name, base_r, top_r, h, lean=(0, 0)):
    bm = bmesh.new(); n = 9; rings = 5; verts = []
    for j in range(rings + 1):
        t = j/rings; z = -.3 + (h + .3)*t; r = base_r + (top_r - base_r)*t + (.18 if j == 0 else 0)
        verts.append([bm.verts.new((r*math.cos(i/n*2*math.pi) + lean[0]*t*t, r*math.sin(i/n*2*math.pi) + lean[1]*t*t, z)) for i in range(n)])
    for j in range(rings):
        for i in range(n): bm.faces.new((verts[j][i], verts[j][(i + 1) % n], verts[j + 1][(i + 1) % n], verts[j + 1][i]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = link(name, me, BARK); return o
def limb(name, p, q, r):
    v = Vector(q) - Vector(p); bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r, radius2=r*.5, depth=v.length)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = link(name, me, BARK)
    o.location = (Vector(p) + Vector(q))/2; o.rotation_euler = v.to_track_quat('Z', 'Y').to_euler(); return o
import random as _r; rt = _r.Random(303)
P = [trunk("oak_trunk", .4, .24, 3.4)]
for k in range(4): a = k/4*2*math.pi + .4; P.append(blob("oak_root%d" % k, (math.cos(a)*.35, math.sin(a)*.35, 0), (.35, .14, .14), BARK, sub=1, wob=0, seed=40 + k))
for k, a in enumerate((.6, 3.4)):
    P.append(limb("oak_limb%d" % k, (0, 0, 3.0), (math.cos(a)*1.25, math.sin(a)*1.25, 4.4), .17))
cy = 3.4 + 1.9
P.append(blob("oak_c0", (0, 0, cy + .4), (2.3, 2.3, 1.85), LEAF, sub=2, wob=.14, seed=50, floor=False))
for c in range(1, 6):
    a = c/5*2*math.pi + rt.uniform(0, .6); d = 1.5; r = 1.45 + rt.uniform(0, .5); y = cy + rt.uniform(-.2, .7)
    P.append(blob("oak_c%d" % c, (math.cos(a)*d, math.sin(a)*d, y), (r, r, r*.8), (LEAF, LEAF2, LEAF3)[c % 3], sub=2, wob=.16, seed=50 + c, floor=False))
grp("ft_oak", P)
P = [trunk("wil_trunk", .36, .2, 2.6, lean=(.9, 0))]
cy = 2.6 + 1.0
P.append(blob("wil_c0", (.9, 0, cy + .4), (2.0, 2.0, 1.3), WLEAF, sub=2, wob=.12, seed=70, floor=False))
for c in range(1, 13):
    a = c/12*2*math.pi + rt.uniform(0, .3); d = 1.85; r = .9 + rt.uniform(0, .3)
    P.append(blob("wil_c%d" % c, (.9 + math.cos(a)*d, math.sin(a)*d, cy - .7 - rt.uniform(0, .5)), (r*.42, r*.42, r*1.55), (WLEAF, WLEAF2)[c % 2], sub=1, wob=.1, seed=70 + c, floor=False))
grp("ft_willow", P)
out = "/home/claude/weirdport/models/campaign"
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in pieces.values():
    r.select_set(True)
    for c_ in r.children_recursive: c_.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(out, "farm_trees.glb"), export_format='GLB', use_selection=True, export_extras=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
for k, r in pieces.items(): print(k, sum(len(c_.data.polygons) for c_ in r.children_recursive if c_.type == 'MESH'))
# preview: an oak, a smaller oak, a willow by a hedge line
pieces["ft_oak"].location = (-4, 2, 0); pieces["ft_willow"].location = (5, 3, 0)
d = bpy.data.objects.new("oak2", None); col.objects.link(d)
for c_ in pieces["ft_oak"].children: cc = c_.copy(); col.objects.link(cc); cc.parent = d
d.location = (1, 8, 0); d.scale = (.7, .7, .7); d.rotation_euler = (0, 0, 2.1)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.render.resolution_x = 1280; sc.render.resolution_y = 720
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (.55, .72, .95, 1); w.node_tree.nodes["Background"].inputs[1].default_value = .45; sc.view_settings.view_transform = "Standard"
g = bpy.data.meshes.new("g"); g.from_pydata([(-30, -30, 0), (30, -30, 0), (30, 30, 0), (-30, 30, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.85, .7, .38), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .95, .85); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-40))
cd = bpy.data.cameras.new("C"); cd.lens = 30; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (0, -18, 4.5); cam.rotation_euler = (Vector((0, 3, 4)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/farm_trees.png"; bpy.ops.render.render(write_still=True)
