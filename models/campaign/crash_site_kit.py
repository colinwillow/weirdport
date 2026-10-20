# crash_site_kit.py -- the ground the wreck tore up: replaces the crash builder's faceted berm ellipsoids, ico0 clods and plank
# colliders with soft pieces, and adds the debris the style guide's Chapter 0 row asks for (hull plates, a cargo pod, a broken
# fence on the crater rim, tall grass). CONTRACT as the rest of models/campaign: one root per piece, origin on the ground at its
# centre, Blender X = ALONG the furrow (three x), Blender -Y = one side. Colliders `col_bld_cs_<piece>`, one box each.
#   cs_berm      3.0 m segment of thrown earth with torn turf flaps on its crest (tiles along the furrow, both sides)
#   cs_clod_a/b/c three clods, dirt with a grass cap, 0.4-0.9 m
#   cs_plate     a torn hull plate, bent, stuck in the dirt at an angle (rivets, a hazard stripe)
#   cs_strut     a snapped rib/strut with a glowing broken end
#   cs_pod       a cargo pod, cracked open, purple glow inside (the thing worth walking to)
#   cs_fence     a broken farm fence: two posts (one leaning), a split rail down, 2.4 m
#   cs_grass     a tall grass tuft (opaque tapered blades)
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix, noise
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection; rnd = random.Random(11)
def mat(name, rgb, rough=.85, metal=0., emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = 3.0
    return m
DIRT = mat("CS_dirt", (.36, .26, .19), 1); DIRT2 = mat("CS_dirt_dark", (.24, .17, .13), 1); TURF = mat("CS_turf", (.3, .42, .17), 1)
GRASS = mat("CS_grass", (.45, .56, .22), .9); GRASS2 = mat("CS_grass_dry", (.66, .6, .3), .9)
HULL = mat("CS_hull", (.74, .78, .86), .3, .0); DARK = mat("CS_dark", (.11, .12, .15), .55); STRIPE = mat("CS_stripe", (.95, .62, .08), .5)
GLOW = mat("CS_glow", (.25, .05, .35), .5, 0, (.72, .43, 1.0)); WOOD = mat("CS_wood", (.46, .34, .22), .9); WOOD2 = mat("CS_wood_old", (.56, .5, .42), .95)
SCORCH = mat("CS_scorch", (.09, .05, .12), 1)
def link(name, me, m, smooth=True):
    o = bpy.data.objects.new(name, me); col.objects.link(o)
    if isinstance(m, list):
        for mm in m: me.materials.append(mm)
    else: me.materials.append(m)
    for p in me.polygons: p.use_smooth = smooth
    return o
def blob(name, c, r, m, sub=2, wob=.15, seed=0, floor=True):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0); off = Vector((seed*3.1, seed*1.7, seed*2.3))
    for v in bm.verts:
        n = v.co.normalized(); d = 1 + wob*noise.noise(n*1.7 + off); z = n.z*r[2]*d
        v.co = Vector((n.x*r[0]*d, n.y*r[1]*d, max(z, -c[2]) if floor else z))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = link(name, me, m); o.location = c; return o
def box(name, c, s, m, rot=(0, 0, 0), bevel=0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co = Vector((v.co.x*s[0], v.co.y*s[1], v.co.z*s[2]))
    if bevel: bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel, segments=1, affect='EDGES')
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = link(name, me, m, smooth=False); o.location = c; o.rotation_euler = rot; return o
def cyl(name, c, r, h, m, rot=(0, 0, 0), seg=10, r2=None):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = link(name, me, m); o.location = c; o.rotation_euler = rot; return o
pieces = {}; cols = []
def grp(name, parts, colbox=None):
    r = bpy.data.objects.new(name, None); col.objects.link(r); pieces[name] = r
    for p in parts: p.parent = r
    if colbox:                                       # (centre, size) in the piece's own frame -> col_bld_cs_<name>, an exact 8-corner box
        (cx, cy, cz), (sx, sy, sz) = colbox; me = bpy.data.meshes.new("c"); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
        for v in bm.verts: v.co = Vector((cx + v.co.x*sx, cy + v.co.y*sy, cz + v.co.z*sz))
        bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("col_bld_" + name, me); col.objects.link(o); cols.append(o)
    return r
def tuft(name, c, h, n, m, seed):
    """tall grass: tapered three-sided blades leaning out, one mesh"""
    rr = random.Random(seed); bm = bmesh.new()
    for k in range(n):
        a = rr.uniform(0, 6.28); lean = rr.uniform(.15, .45); hh = h*rr.uniform(.6, 1.0); w = .035
        bx, by = math.cos(a)*rr.uniform(0, .12), math.sin(a)*rr.uniform(0, .12)
        tip = Vector((bx + math.cos(a)*lean*hh, by + math.sin(a)*lean*hh, hh))
        base = [bm.verts.new((bx + math.cos(a + t)*w, by + math.sin(a + t)*w, 0)) for t in (0, 2.1, 4.2)]
        mid = [bm.verts.new((bx*.5 + tip.x*.5 + math.cos(a + t)*w*.6, by*.5 + tip.y*.5 + math.sin(a + t)*w*.6, hh*.55)) for t in (0, 2.1, 4.2)]
        tv = bm.verts.new(tip)
        for i in range(3):
            j = (i + 1) % 3; bm.faces.new((base[i], base[j], mid[j], mid[i])); bm.faces.new((mid[i], mid[j], tv))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = link(name, me, m); o.location = c; return o
# ---- berm (4.3 m of lump for a 3.0 m tile: neighbours OVERLAP into one ridge, never a row of potatoes): a long low lump of thrown earth, a darker wet face toward the furrow (-Y), torn turf flaps tipped over its crest
P = [blob("bm_body", (0, 0, 0), (2.15, .95, .62), DIRT, sub=3, wob=.12, seed=1), blob("bm_face", (0, -.35, 0), (1.95, .6, .45), DIRT2, sub=2, seed=2)]
for k, x in enumerate((-1.0, .1, 1.05)):
    f = box("bm_flap%d" % k, (x, .05 + rnd.uniform(-.08, .08), .55), (.7, .45, .07), TURF, rot=(rnd.uniform(-.25, -.1), rnd.uniform(-.1, .1), rnd.uniform(-.3, .3)), bevel=.03)
    P.append(f)
P.append(tuft("bm_grass", (.6, .45, .55), .45, 7, GRASS, 3))
grp("cs_berm", P, ((0, 0, .3), (3.0, 1.5, .6)))
# ---- clods: three sizes, each a dirt lump with a grass cap and a root of the field still on it
for k, (s, nm) in enumerate(((.9, "a"), (.6, "b"), (.4, "c"))):
    P = [blob("cl%s_dirt" % nm, (0, 0, s*.38), (s*.55, s*.45, s*.4), DIRT, sub=2, seed=5 + k),
         blob("cl%s_cap" % nm, (s*.06, 0, s*.68), (s*.42, s*.36, s*.12), TURF, sub=2, wob=.08, seed=8 + k)]
    if k == 0: P.append(tuft("cla_grass", (0, 0, s*.72), .3, 5, GRASS, 4))
    grp("cs_clod_" + nm, P, ((0, 0, s*.4), (s*1.0, s*.8, s*.8)) if k == 0 else None)
# ---- hull plate: a curved, torn panel driven into the dirt, rivets along one edge, a hazard stripe
bm = bmesh.new(); W, H = 1.8, 1.3
grid = [[bm.verts.new((x, .25*math.sin(x/W*math.pi) + .12*(z/H)**2, z)) for z in [H*j/6 for j in range(7)]] for x in [-W/2 + W*i/8 for i in range(9)]]
for i in range(8):
    for j in range(6): bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
for i in range(9):                                     # torn top edge: knock the top row down unevenly
    grid[i][6].co.z -= rnd.uniform(0, .35) * (1 if i % 3 else .2)
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=.05)
me = bpy.data.meshes.new("pl_body"); bm.to_mesh(me); bm.free(); plate = link("pl_body", me, HULL, smooth=True)
plate.rotation_euler = (math.radians(-22), 0, math.radians(8)); plate.location = (0, 0, -.15)
P = [plate, box("pl_stripe", (0, .1, .28), (1.7, .07, .16), STRIPE, rot=(math.radians(-22), 0, math.radians(8)))]
for k in range(7): P.append(cyl("pl_rivet%d" % k, (-.78 + k*.26, .04, .12), .035, .06, DARK, rot=(math.radians(68), 0, 0), seg=6))
P.append(blob("pl_heap", (0, .15, 0), (1.1, .55, .28), DIRT, sub=2, seed=12))
grp("cs_plate", P, ((0, .1, .5), (1.9, .6, 1.0)))
# ---- strut: a snapped rib lying in the grass, one end up on a clod, its broken end glowing
P = [cyl("st_rib", (0, 0, .28), .09, 2.6, DARK, rot=(0, math.radians(84), 0), seg=8),
     cyl("st_sleeve", (-.6, 0, .25), .13, .5, HULL, rot=(0, math.radians(84), 0), seg=8),
     blob("st_break", (1.3, 0, .41), (.13, .13, .13), GLOW, sub=1, wob=.35, seed=14, floor=False),
     blob("st_rest", (1.1, 0, .12), (.3, .28, .2), DIRT, sub=2, seed=15)]
grp("cs_strut", P)
# ---- cargo pod: a capsule on its side, split along the top, a purple glow welling out of the split
P = [cyl("pd_body", (0, 0, .55), .55, 1.6, HULL, rot=(0, math.radians(90), 0), seg=20),
     blob("pd_capL", (-.8, 0, .55), (.2, .55, .55), HULL, sub=2, wob=0, floor=False), blob("pd_capR", (.8, 0, .55), (.2, .55, .55), HULL, sub=2, wob=0, floor=False),
     box("pd_band1", (-.45, 0, .55), (.1, 1.16, 1.16), DARK, bevel=.03), box("pd_band2", (.45, 0, .55), (.1, 1.16, 1.16), DARK, bevel=.03),
     box("pd_stripe", (0, -.56, .55), (.6, .02, .14), STRIPE),
     blob("pd_glow", (0, .05, 1.02), (.62, .14, .1), GLOW, sub=2, wob=.25, seed=16, floor=False),
     box("pd_lid", (.1, .42, 1.05), (1.0, .55, .06), HULL, rot=(math.radians(35), 0, math.radians(4)), bevel=.02),
     blob("pd_dirt", (0, 0, 0), (1.1, .75, .22), DIRT2, sub=2, seed=17)]
grp("cs_pod", P, ((0, 0, .55), (2.0, 1.15, 1.1)))
# ---- broken fence: two posts on the crater rim (one leaning), the rail split and down, a wire sagging
P = [box("fn_post0", (-1.2, 0, .6), (.14, .14, 1.25), WOOD, bevel=.02), box("fn_post1", (1.2, 0, .5), (.14, .14, 1.2), WOOD, rot=(math.radians(18), math.radians(-14), 0), bevel=.02),
     box("fn_rail_top", (-.6, 0, 1.0), (1.3, .08, .12), WOOD2, rot=(0, math.radians(8), 0), bevel=.015),
     box("fn_rail_down", (.45, -.15, .25), (1.4, .08, .12), WOOD2, rot=(0, math.radians(-14), math.radians(10)), bevel=.015),
     box("fn_rail_low", (0, 0, .5), (2.4, .08, .12), WOOD2, rot=(0, math.radians(3), 0), bevel=.015),
     blob("fn_foot0", (-1.2, 0, 0), (.25, .25, .1), DIRT, sub=1, seed=18), blob("fn_foot1", (1.25, 0, 0), (.3, .3, .14), DIRT, sub=1, seed=19),
     tuft("fn_grass0", (-1.0, .15, 0), .7, 9, GRASS2, 5), tuft("fn_grass1", (1.4, -.1, 0), .6, 8, GRASS, 6)]
grp("cs_fence", P, ((0, 0, .6), (2.6, .3, 1.2)))
# ---- tall grass
grp("cs_grass", [tuft("gr_a", (0, 0, 0), .9, 14, GRASS, 7), tuft("gr_b", (.12, .08, 0), .7, 9, GRASS2, 8)])
# ---- export: the visual (every piece root) and the colliders
out = "/home/claude/weirdport/models/campaign"
def export(path, objs):
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs:
        o.select_set(True)
        for c_ in o.children_recursive: c_.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_extras=True, export_yup=True, export_apply=True,
                              export_draco_mesh_compression_enable=path.endswith("kit.glb"), export_materials='EXPORT' if path.endswith("kit.glb") else 'NONE')
export(os.path.join(out, "crash_site_kit.glb"), list(pieces.values())); export(os.path.join(out, "crash_site_kit_collision.glb"), cols)
for k, r in pieces.items(): print(k, sum(len(c_.data.polygons) for c_ in r.children_recursive if c_.type == 'MESH'))
# ---- preview: a short stretch of furrow at dusk, pieces laid round it
for o in cols: o.hide_render = True
lay = [("cs_berm", (-3, 2.0, 0), 180), ("cs_berm", (0, 2.1, 0), 180), ("cs_berm", (3, 1.9, 0), 180), ("cs_berm", (-3, -2.0, 0), 0), ("cs_berm", (0, -2.1, 0), 0),
       ("cs_berm", (3, -1.9, 0), 0), ("cs_pod", (1.2, -.2, 0), 15), ("cs_plate", (-2.5, .3, 0), -20), ("cs_strut", (5.2, -3.6, 0), 40), ("cs_fence", (-5.5, -4.8, 0), 10),
       ("cs_clod_a", (-.5, -4.0, 0), 0), ("cs_clod_b", (1.6, 3.8, 0), 50), ("cs_clod_c", (4.0, 3.3, 0), 20), ("cs_clod_c", (-1.8, 4.2, 0), 70), ("cs_grass", (-3.2, -4.3, 0), 0),
       ("cs_grass", (6.0, 3.8, 0), 0), ("cs_grass", (-6.3, 3.4, 0), 0)]
used = set()
for name, p, yaw in lay:
    r = pieces[name]
    if name in used:
        d = bpy.data.objects.new(name + "_dup", None); col.objects.link(d)
        for c_ in r.children: cc = c_.copy(); col.objects.link(cc); cc.parent = d
        r = d
    used.add(name); r.location = p; r.rotation_euler = (0, 0, math.radians(yaw))
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.12, .14, .3, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)]); link("g", g, mat("G", (.22, .3, .13), 1))
s = bpy.data.meshes.new("s"); s.from_pydata([(-6, -1.4, .01), (6, -1.4, .01), (6, 1.4, .01), (-6, 1.4, .01)], [], [(0, 1, 2, 3)]); link("s", s, SCORCH)
sun = bpy.data.lights.new("moon", 'SUN'); sun.energy = 1.2; sun.color = (.7, .78, 1); so = bpy.data.objects.new("moon", sun); col.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(-30))
fire = bpy.data.lights.new("fire", 'POINT'); fire.energy = 900; fire.color = (1, .55, .2); fo = bpy.data.objects.new("fire", fire); col.objects.link(fo); fo.location = (-1, 0, 1.6)
cd = bpy.data.cameras.new("C"); cd.lens = 26; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (9, -9, 4.2); cam.rotation_euler = (Vector((0, 0, .4)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/crash_site_kit.png"; bpy.ops.render.render(write_still=True)
