# crash_wreck.py -- the saucer wreck for Chapter 0, as a GLB the game places at CRASH.origin.
# CONTRACT: Blender Z-up, metres. Origin = the wreck's centre ON THE GROUND. +X = the way it was travelling (the nose, ploughed in);
# the furrow runs out along -X. Scale is final (S 1.6: hull radius 5.3 m). Colliders: col_* boxes, same prefixes as every world.
# Markers: fire_0, fire_1, smoke, hatch, clancy, you (empties) -- the same names CRASH.at uses.
import bpy, bmesh, math, random, os
from mathutils import Vector, Matrix, Euler
bpy.ops.wm.read_factory_settings(use_empty=True)
KIT = "/home/claude/weirdport/models/toon_city_kit/toon_city_kit_buildings.glb"
bpy.ops.import_scene.gltf(filepath=KIT)
KM = {m.name: m for m in bpy.data.materials}
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
S = 1.6; R = 3.3*S; rnd = random.Random(7)
col = bpy.context.scene.collection
def mat(name, base, emit=None, rough=.6, metal=.0, src=None, alpha=None):
    if src and src in KM:
        m = KM[src].copy(); m.name = name
    else:
        m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    if not src: b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = 3.0
    if alpha is not None:
        b.inputs["Alpha"].default_value = alpha; m.blend_method = 'BLEND'
    m.use_backface_culling = alpha is None
    return m
M_HULL = mat("CW_hull", (.74, .78, .86), rough=.3, metal=.0)
M_DARK = mat("CW_dark", (.11, .12, .15), rough=.55)
M_RIB = mat("CW_rib", (.42, .3, .24), rough=.5)
M_GLOW = mat("CW_glow", (.25, .05, .35), emit=(.72, .43, 1.0))
M_GLASS = mat("CW_glass", (.5, .88, 1.0), rough=.05, alpha=.35)
M_SCORCH = mat("CW_scorch", (.09, .05, .12), rough=1.0)
M_DIRT = mat("CW_dirt", (.36, .26, .19), rough=1.0)
def obj(name, me, m, smooth=True):
    o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    return o
def lathe(name, prof, m, n=48, smooth=True):
    """profile [(r, z)] revolved about Z; caps where r == 0"""
    bm = bmesh.new(); rings = []
    for r, z in prof:
        rings.append([bm.verts.new((r*math.cos(2*math.pi*k/n), r*math.sin(2*math.pi*k/n), z)) for k in range(n)])
    for a, b in zip(rings, rings[1:]):
        for k in range(n): bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return obj(name, me, m, smooth)
def box(name, x0, y0, z0, x1, y1, z1, m):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = obj(name, me, m, False); o.scale = (x1 - x0, y1 - y0, z1 - z0); o.location = ((x0 + x1)/2, (y0 + y1)/2, (z0 + z1)/2); return o
# ---- the saucer, built level, then tipped nose-down and sunk
parts = []
hull = lathe("hull", [(0, -.55*S), (R*.55, -.62*S), (R*.92, -.38*S), (R, -.05*S), (R*1.02, .02*S), (R*.94, .2*S), (R*.6, .55*S), (R*.42, .7*S), (0, .74*S)], M_HULL, 64); parts.append(hull)
rim = lathe("rim", [(R*.99, -.1*S), (R*1.06, -.06*S), (R*1.07, .04*S), (R*1.0, .08*S)], M_DARK, 64); parts.append(rim)
for k in range(16):                                                                     # rim lights: half dead, the rest still pulsing
    a = 2*math.pi*k/16; m = M_GLOW if k % 3 else M_DARK
    l = lathe("rimlight_%d" % k, [(0, -.08), (.26*S, -.04), (.26*S, .06), (0, .1)], m, 12)
    l.location = (R*1.065*math.cos(a), R*1.065*math.sin(a), 0); parts.append(l)
dome = lathe("dome", [(R*.42, .7*S), (R*.4, .9*S), (R*.3, 1.15*S), (R*.15, 1.28*S), (0, 1.32*S)], M_GLASS, 40); dome.location.x = -.25*S; parts.append(dome)
core = lathe("core", [(0, .65*S), (.55*S, .72*S), (.6*S, .95*S), (0, 1.05*S)], M_GLOW, 24); core.location.x = -.25*S; parts.append(core)
# a torn gash on the nose side: dark interior + exposed ribs + three panels peeled back
gash = lathe("gash", [(R*.5, .0), (R*.95, .02*S), (R*.95, .15*S), (R*.5, .45*S)], M_DARK, 24); gash.scale = (1, .45, 1); gash.location = (.35*S, 0, .02); parts.append(gash)
for k in range(5):
    y = (-1 + k*.5)*S; a = math.atan2(y, R*.8)
    rb = box("rib_%d" % k, R*.55, y - .05, .0, R*.98, y + .05, .45*S, M_RIB); rb.rotation_euler = (0, -.35, 0); parts.append(rb)
for k, (y, rz, rx) in enumerate([(-.9, .6, .9), (.3, -.3, 1.2), (1.1, -.8, .7)]):
    pn = box("panel_%d" % k, 0, -.6*S, 0, 1.4*S, .6*S, .06*S, M_HULL); pn.location = (R*.75, y*S, .35*S); pn.rotation_euler = (rx, -.5, rz); parts.append(pn)
# the hatch on the tail side (open, the ramp down to the dirt)
hatch = box("hatch_ramp", -R*.95, -.7*S, -.1, -R*.95 + 1.9*S, .7*S, .05, M_DARK); hatch.rotation_euler = (0, .38, 0); hatch.location.x = -R*.85; parts.append(hatch)
# parent all hull parts under a pivot, then tip + sink
piv = bpy.data.objects.new("wreck_pivot", None); col.objects.link(piv)
for p in parts: p.parent = piv
piv.rotation_euler = (math.radians(-9), math.radians(20), 0); piv.location = (0, 0, .25*S)
# ---- the ground around it: a scorch disc and the bow wave of earth in front of the nose, debris strewn behind
bm = bmesh.new(); n = 40
c = bm.verts.new((0, 0, .03)); ring = [bm.verts.new(((R*1.9 + rnd.uniform(-1, 1))*math.cos(2*math.pi*k/n)*1.25 - 2.5, (R*1.6 + rnd.uniform(-1, 1))*math.sin(2*math.pi*k/n), .03)) for k in range(n)]
for k in range(n): bm.faces.new((c, ring[k], ring[(k + 1) % n]))
me = bpy.data.meshes.new("scorch"); bm.to_mesh(me); bm.free(); obj("scorch", me, M_SCORCH, False)
bow = lathe("bow_wave", [(0, -.3), (2.2*S, -.3), (2.0*S, .6*S), (1.0*S, 1.0*S), (0, 1.1*S)], M_DIRT, 24); bow.scale = (.7, 1.6, 1); bow.location = (R*1.05, 0, -.15)
for k in range(14):                                                                     # debris: hull shards + dirt clods behind the wreck
    x = -R - rnd.uniform(0, 14); y = rnd.uniform(-5, 5); s = rnd.uniform(.25, .7)
    if k % 2: d = box("shard_%d" % k, -s, -s*.6, 0, s, s*.6, .05, M_HULL)
    else: d = lathe("clod_%d" % k, [(0, 0), (s, .05), (s*.8, s*.6), (0, s*.7)], M_DIRT, 7)
    d.location = (x, y, .02); d.rotation_euler = (rnd.uniform(-.4, .4), rnd.uniform(-.4, .4), rnd.uniform(0, 6.28))
# ---- markers (the names CRASH.at already uses) + colliders (tail high, nose buried: standable, like the code's two boxes)
for name, p in (("fire_0", (R*.8, .2*S, .6*S)), ("fire_1", (.0, -2.2*S, .05)), ("smoke", (0, 0, 1.6*S + .55*S)), ("hatch", (-R*1.0, 0, .1)), ("clancy", (-R*1.4, 1.2, 0)), ("you", (-9*S, 3*S, 0))):
    e = bpy.data.objects.new(name, None); col.objects.link(e); e.location = p
c1 = box("col_bld_wreck_tail", -R, -R*.9, -.3, .0, R*.9, .55*S + .95*S, M_DARK); c1.hide_render = True
c2 = box("col_bld_wreck_nose", .0, -R*.9, -.3, R*1.05, R*.9, .55*S + .1*S, M_DARK); c2.hide_render = True
c3 = box("col_bld_bow_wave", R*1.05 - 1.4*S, -2.6*S, -.3, R*1.05 + 1.4*S, 2.6*S, 1.0*S, M_DARK); c3.hide_render = True
bpy.context.view_layer.update()
out = "/home/claude/weirdport/models/campaign"; os.makedirs(out, exist_ok=True)
vis = [o for o in col.objects if not o.name.startswith("col_")]; cols = [o for o in col.objects if o.name.startswith("col_")]
def export(path, objs, draco):
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_extras=True, export_yup=True, export_apply=True,
                              export_draco_mesh_compression_enable=draco, export_image_format='WEBP')
export(os.path.join(out, "crash_wreck.glb"), vis, True)
export(os.path.join(out, "crash_wreck_collision.glb"), cols, False)
tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in vis if o.type == 'MESH')
print("WRECK tris", tris, "objs", len(vis))
# preview render
for c_ in cols: c_.hide_render = True
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.render.resolution_x = 1280; sc.render.resolution_y = 720
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (.25, .3, .45, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
g = bpy.data.meshes.new("ground"); g.from_pydata([(-60, -60, 0), (60, -60, 0), (60, 60, 0), (-60, 60, 0)], [], [(0, 1, 2, 3)]); go = obj("ground_preview", g, mat("G", (.25, .32, .15), rough=1), False)
sun = bpy.data.lights.new("moon", 'SUN'); sun.energy = 4.0; sun.color = (.85, .9, 1.0); so = bpy.data.objects.new("moon", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(140))
fl = bpy.data.lights.new("fire", 'POINT'); fl.energy = 900; fl.color = (1, .5, .2); fo = bpy.data.objects.new("firel", fl); col.objects.link(fo); fo.location = (R*.8, .2*S, 1.6)
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-13, -10, 4.5); cam.rotation_euler = (Vector((1, 0, 1.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/crash_wreck.png"; bpy.ops.render.render(write_still=True)
