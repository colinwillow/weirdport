# farm_vehicles.py -- the farm's PICKUP and TRACTOR as GLBs (replacing vehPickup / vehTractor's boxes).
# CONTRACT: Blender Z-up, metres. Origin = centre of the footprint ON THE GROUND. Forward = -Y in Blender (= three's +z, which is
# what vehParts' model space uses: forward +z, right +x, up +y). Same footprint as the code (pickup 1.95 x 4.9, tractor 2.1 x 4.4)
# so FVEH's hw / hl push-out boxes still fit. Bevelled, smooth-shaded, 5-7 materials each, all opaque except the glass.
import bpy, bmesh, math, os
from mathutils import Vector, Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection
def mat(name, rgb, rough=.55, metal=0.0, emit=None, alpha=None):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = 2.0
    if alpha is not None: b.inputs["Alpha"].default_value = alpha; m.blend_method = 'BLEND'
    return m
def finish(o, m, bevel=0.0, smooth=True, segs=2):
    o.data.materials.append(m)
    if bevel > 0:
        md = o.modifiers.new("b", 'BEVEL'); md.width = bevel; md.segments = segs; md.limit_method = 'ANGLE'
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
        try: o.data.set_sharp_from_angle(angle=math.radians(40))
        except Exception: pass
    return o
def box(name, cx, cy, cz, sx, sy, sz, m, bevel=.04, parent=None):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.scale = (sx, sy, sz); o.location = (cx, cy, cz)
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.transform_apply(scale=True); o.select_set(False)
    finish(o, m, bevel); o.parent = parent; return o
def cyl(name, cx, cy, cz, r, w, m, axis='X', n=24, parent=None, bevel=.02):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=n, radius1=r, radius2=r, depth=w)
    if axis == 'X': bmesh.ops.rotate(bm, verts=bm.verts, matrix=Matrix.Rotation(math.pi/2, 3, 'Y'))
    if axis == 'Y': bmesh.ops.rotate(bm, verts=bm.verts, matrix=Matrix.Rotation(math.pi/2, 3, 'X'))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = (cx, cy, cz)
    finish(o, m, bevel); o.parent = parent; return o
def tyre(name, cx, cy, cz, r, w, m_t, m_h, hub=.5, lugs=0, parent=None):
    out = [cyl(name, cx, cy, cz, r, w, m_t, n=28, bevel=r*.12), cyl(name + "_hub", cx + (w/2 + .005)*(1 if cx > 0 else -1), cy, cz, r*hub, .04, m_h, n=20)]
    for k in range(lugs):                                                                     # tractor tread lugs, chevrons round the tyre
        a = 2*math.pi*k/lugs
        for side in (-1, 1):
            l = box(name + "_lug%d%d" % (k, side), cx + side*w*.24, cy + math.cos(a)*r, cz + math.sin(a)*r, w*.42, .12, .07, m_t, bevel=.01)
            l.rotation_euler = (a + math.pi/2, 0, side*.45); out.append(l)
    return out
def tread(name, cx, cy, cz, r, w, m, n=20):
    bm = bmesh.new()
    for k in range(n):
        a0 = 2*math.pi*k/n; a1 = a0 + 2*math.pi/n*.55
        for side in (-1, 1):
            x0, x1 = (0, side*w*.5) if side > 0 else (side*w*.5, 0); off = side*.06
            vs = []
            for a, rr in ((a0, r), (a1, r), (a1, r + .07), (a0, r + .07)):
                for x in (x0, x1): vs.append(bm.verts.new((x, math.cos(a + off)*rr, math.sin(a + off)*rr)))
            q = vs; bmesh.ops.contextual_create(bm, geom=[q[0], q[2], q[4], q[6]]); bmesh.ops.contextual_create(bm, geom=[q[1], q[3], q[5], q[7]])
            bmesh.ops.contextual_create(bm, geom=[q[4], q[5], q[7], q[6]]); bmesh.ops.contextual_create(bm, geom=[q[0], q[1], q[3], q[2]])
            bmesh.ops.contextual_create(bm, geom=[q[2], q[3], q[5], q[4]]); bmesh.ops.contextual_create(bm, geom=[q[6], q[7], q[1], q[0]])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = (cx, cy, cz)
    return finish(o, m, smooth=False)
def lathe(name, prof, m, n=24, axis='Y', at=(0, 0, 0)):
    bm = bmesh.new(); rings = []
    for r, z in prof: rings.append([bm.verts.new((r*math.cos(2*math.pi*k/n), r*math.sin(2*math.pi*k/n), z)) for k in range(n)])
    for a, b in zip(rings, rings[1:]):
        for k in range(n): bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    if axis == 'Y': bmesh.ops.rotate(bm, verts=bm.verts, matrix=Matrix.Rotation(-math.pi/2, 3, 'X'))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = at
    return finish(o, m)
def fender(name, cx, cy, cz, r, w, m, arc=(0.0, math.pi), thick=.06, n=16):
    """a curved mudguard over a wheel: an arc of quads extruded across the wheel's width"""
    bm = bmesh.new(); A = []; B = []
    for k in range(n + 1):
        a = arc[0] + (arc[1] - arc[0])*k/n; y = math.cos(a)*r; z = math.sin(a)*r
        A.append((bm.verts.new((-w/2, y, z)), bm.verts.new((-w/2, y*(1 + thick/r), z*(1 + thick/r)))))
        B.append((bm.verts.new((w/2, y, z)), bm.verts.new((w/2, y*(1 + thick/r), z*(1 + thick/r)))))
    for k in range(n):
        bm.faces.new((A[k][1], A[k + 1][1], B[k + 1][1], B[k][1])); bm.faces.new((B[k][0], B[k + 1][0], A[k + 1][0], A[k][0]))
        bm.faces.new((A[k][0], A[k + 1][0], A[k + 1][1], A[k][1])); bm.faces.new((B[k][1], B[k + 1][1], B[k + 1][0], B[k][0]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = (cx, cy, cz)
    return finish(o, m)

TYRE = mat("FV_tyre", (.06, .06, .07), .85); CHROME = mat("FV_chrome", (.82, .82, .8), .25, .8); GLASS = mat("FV_glass", (.45, .6, .68), .05, alpha=.45)
LAMP = mat("FV_lamp", (1, .95, .8), .3, emit=(1, .9, .6)); WOOD = mat("FV_wood", (.55, .38, .22), .8); DARK = mat("FV_dark", (.12, .12, .13), .6)

def pickup():
    B = mat("FV_pickup_blue", (.27, .43, .55), .45); HUB = mat("FV_hub_cream", (.9, .86, .74), .4); HAY = mat("FV_hay", (.85, .7, .35), .9)
    P = []
    P.append(box("pk_chassis", 0, 0, .55, 1.7, 4.7, .28, DARK, .03))
    P.append(box("pk_hood", 0, -1.55, 1.0, 1.55, 1.5, .55, B, .14))                          # long rounded hood
    P.append(box("pk_cab", 0, -.15, 1.35, 1.75, 1.35, 1.15, B, .16))                         # the cab
    P.append(box("pk_roof", 0, -.15, 1.95, 1.62, 1.2, .12, B, .08))
    P.append(box("pk_windshield", 0, -.82, 1.55, 1.52, .06, .55, GLASS, .02)); P[-1].rotation_euler = (math.radians(-18), 0, 0)
    for s in (-1, 1): P.append(box("pk_side_win%d" % s, s*.88, -.1, 1.58, .04, .95, .5, GLASS, .02))
    P.append(box("pk_backwin", 0, .53, 1.58, 1.3, .04, .45, GLASS, .02))
    P.append(box("pk_grille", 0, -2.33, .95, 1.2, .08, .45, CHROME, .03))
    for k in range(6): P.append(box("pk_grille_bar%d" % k, 0, -2.38, .78 + k*.07, 1.1, .03, .02, DARK, .0))
    P.append(box("pk_bumper_f", 0, -2.45, .62, 1.9, .14, .16, CHROME, .05)); P.append(box("pk_bumper_r", 0, 2.38, .62, 1.9, .14, .16, CHROME, .05))
    for s in (-1, 1):
        P.append(lathe("pk_headlamp%d" % s, [(0, 0), (.16, 0), (.16, .08), (.1, .12), (0, .13)], LAMP, 16, at=(s*.6, -2.32, 1.12)))
        P.append(box("pk_runboard%d" % s, s*.92, -.2, .55, .22, 1.6, .05, DARK, .02))
        P.append(box("pk_mirror%d" % s, s*.98, -.72, 1.7, .05, .14, .1, CHROME, .02))
        for y in (-1.5, 1.5): P.append(fender("pk_fender%d%d" % (s, int(y)), s*.86, y, .42, .5, .34, B))
    # the bed: low sides, wooden floor slats, a tailgate, a hay bale and a spare tyre (the farm's errand)
    P.append(box("pk_bed_floor", 0, 1.5, .72, 1.6, 1.7, .06, WOOD, .01))
    for s in (-1, 1): P.append(box("pk_bed_side%d" % s, s*.82, 1.5, .98, .06, 1.75, .48, B, .03))
    P.append(box("pk_tailgate", 0, 2.36, .98, 1.64, .06, .48, B, .03))
    P.append(box("pk_hay", -.3, 1.35, 1.12, .9, .55, .7, HAY, .08))
    P += tyre("pk_spare", .35, 1.85, 1.0, .36, .22, TYRE, HUB)
    for s in (-1, 1):
        for y in (-1.5, 1.5): P += tyre("pk_wheel%d%d" % (s, int(y)), s*.85, y, .4, .4, .3, TYRE, HUB)
    P.append(box("pk_taillight_l", -.7, 2.4, 1.0, .12, .04, .12, mat("FV_red_lamp", (.9, .15, .1), .4, emit=(.8, .1, .05)), .01)); P.append(box("pk_taillight_r", .7, 2.4, 1.0, .12, .04, .12, mat("FV_red_lamp", (.9, .15, .1)), .01))
    return P

def tractor():
    R = mat("FV_tractor_red", (.72, .17, .13), .45); HUB = mat("FV_hub_yellow", (.88, .74, .3), .4); ST = mat("FV_steel", (.5, .52, .55), .4, .5)
    P = []
    P.append(box("tr_hood", 0, -.75, 1.05, .82, 1.8, .7, R, .12))                            # the long hood
    P.append(box("tr_grille", 0, -1.66, 1.0, .7, .06, .58, DARK, .03))
    for k in range(7): P.append(box("tr_grille_bar%d" % k, 0, -1.69, .76 + k*.08, .62, .02, .025, CHROME, .0))
    P.append(box("tr_belly", 0, -.4, .62, .5, 2.2, .3, DARK, .04))
    P.append(box("tr_seat_base", 0, .75, 1.25, .6, .6, .35, R, .06))
    P.append(box("tr_seat", 0, .82, 1.5, .5, .42, .1, DARK, .04)); P.append(box("tr_seat_back", 0, 1.05, 1.72, .5, .08, .4, DARK, .04))
    P.append(cyl("tr_steer_col", 0, .2, 1.55, .03, .6, DARK, 'Y')); P[-1].rotation_euler = (math.radians(-35), 0, 0)
    P.append(lathe("tr_steer_wheel", [(.2, 0), (.22, .02), (.2, .04), (.18, .02), (.2, 0)], DARK, 20, axis='Z', at=(0, .35, 1.85)))
    P.append(cyl("tr_exhaust", .25, -1.1, 1.75, .05, 1.1, DARK, 'Z')); P.append(cyl("tr_exhaust_cap", .25, -1.1, 2.33, .07, .08, DARK, 'Z'))
    P.append(lathe("tr_headlamp", [(0, 0), (.1, 0), (.1, .06), (0, .08)], LAMP, 14, at=(0, -1.7, 1.42)))
    # big rear wheels with tread lugs and fenders, small fronts
    for s in (-1, 1):
        P += tyre("tr_rear%d" % s, s*.82, .65, .82, .82, .45, TYRE, HUB, hub=.55, lugs=0)
        P.append(tread("tr_tread%d" % s, s*.82, .65, .82, .82, .45, TYRE))
        P.append(fender("tr_fender%d" % s, s*.82, .65, .82, .95, .52, R, arc=(math.radians(15), math.radians(165))))
        P += tyre("tr_front%d" % s, s*.55, -1.25, .42, .42, .26, TYRE, HUB, hub=.5)
    P.append(box("tr_front_axle", 0, -1.25, .42, 1.1, .1, .1, DARK, .02))
    # the plough behind: a frame, a hitch bar and three discs
    P.append(box("tr_hitch", 0, 1.55, .6, .14, .7, .1, ST, .02)); P.append(box("tr_plough_frame", 0, 1.95, .55, 1.8, .24, .2, ST, .03))
    for x in (-.6, 0, .6):
        d = lathe("tr_disc%d" % int(x*10), [(0, 0), (.3, .04), (.32, .07), (0, .1)], ST, 20, axis='Z', at=(x, 2.05, .32)); d.rotation_euler = (math.radians(70), math.radians(20), 0); P.append(d)
    return P

out = "/home/claude/weirdport/models/campaign"; os.makedirs(out, exist_ok=True)
def export(name, parts):
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in parts: o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + ".glb"), export_format='GLB', use_selection=True, export_extras=True, export_yup=True,
                              export_apply=True, export_draco_mesh_compression_enable=True)
    dg = bpy.context.evaluated_depsgraph_get()
    t = sum(len(o.evaluated_get(dg).data.polygons) for o in parts if o.type == 'MESH')
    print(name.upper(), "faces", t, "parts", len(parts))
pk = pickup(); export("farm_pickup", pk)
for o in pk: o.location.x -= 3.2
tr = tractor(); export("farm_tractor", tr)
for o in tr: o.location.x += 2.6
# preview
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.render.resolution_x = 1280; sc.render.resolution_y = 720
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (.6, .7, .85, 1)
g = bpy.data.meshes.new("g"); g.from_pydata([(-30, -30, 0), (30, -30, 0), (30, 30, 0), (-30, 30, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.42, .5, .25), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 4; so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(45), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 32; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-6.5, -8.5, 3.6); cam.rotation_euler = (Vector((0, 0, .9)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/farm_vehicles.png"; bpy.ops.render.render(write_still=True)
