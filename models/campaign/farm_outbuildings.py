# farm_outbuildings.py -- the farm's three small buildings as art, at their builders' exact numbers (the code keeps every collider).
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
# ======== the tool shed: board-and-batten, a tin pent roof, a door hanging open, a window, tools and a bench
cur = "fo_shed"; groups[cur] = []
sh, sl = 2.6, 2.1; b0 = .25
box(-2.3, -1.8, -.4, 2.3, 1.8, b0, STONE, bev=.03)
def h(y): return sl + (sh - sl)*(y + 1.7)/3.4                      # the wall top at y (front 2.1 -> back 2.6)
box(-2.2, 1.62, b0, 2.2, 1.78, sh, SHED)                              # back
for s in (-1, 1):                                                     # the two sides, cut to the slope (built from points)
    x0, x1 = s*2.15 - .08, s*2.15 + .08
    vs = [(x0, -1.7, b0), (x0, 1.7, b0), (x0, 1.7, sh), (x0, -1.7, sl), (x1, -1.7, b0), (x1, 1.7, b0), (x1, 1.7, sh), (x1, -1.7, sl)]
    me = bpy.data.meshes.new("side"); me.from_pydata(vs, [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
    o = bpy.data.objects.new("side", me); col.objects.link(o); me.materials.append(SHED); put(o)
box(-2.2, -1.78, b0, -.4, -1.62, sl, SHED); box(.8, -1.78, b0, 2.2, -1.62, sl, SHED); box(-.4, -1.78, 2.0, .8, -1.62, sl, SHED)
box(-.4, -1.7, b0, .8, -1.66, 2.0, DARK)                               # the dark inside the doorway
for x in [-2.0 + i*.45 for i in range(10)]:                            # battens front and back, the door gap skipped
    box(x - .03, 1.78, b0, x + .03, 1.82, sh - .05, SHED2)
    if not (-.5 < x < .9): box(x - .03, -1.82, b0, x + .03, -1.78, sl - .05, SHED2)
for s in (-1, 1):
    for y in [-1.4 + i*.45 for i in range(7)]: box(s*2.23 - .02, y - .03, b0, s*2.23 + .02, y + .03, h(y) - .05, SHED2)
for (x0, x1, z0, z1) in ((-.5, -.4, b0, 2.05), (.8, .9, b0, 2.05), (-.5, .9, 2.0, 2.1)): box(x0, -1.86, z0, x1, -1.78, z1, TRIM)
for (a, b, c, d) in ((-2.25, -2.15, -1.86, 1.86), (2.15, 2.25, -1.86, 1.86)): box(a, c, b0, b, c + .1, sl, TRIM); box(a, d - .1, b0, b, d, sh, TRIM)
dv = [(.85, -1.82, b0 + .05), (.85, -1.82, 2.0), (1.85, -2.3, 2.0), (1.85, -2.3, b0 + .05)]   # the door, swung open against the front
me = bpy.data.meshes.new("door"); me.from_pydata(dv + [(v[0] + .05, v[1] + .05, v[2]) for v in dv], [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
o = bpy.data.objects.new("door", me); col.objects.link(o); me.materials.append(RED); put(o)
box(2.15 - .02, -.3, 1.1, 2.29, .5, 1.7, DARK); box(2.27, -.36, 1.03, 2.31, .56, 1.1, TRIM); box(2.27, -.36, 1.7, 2.31, .56, 1.76, TRIM); box(2.27, .07, 1.1, 2.31, .13, 1.7, TRIM)
for k in range(9):                                                     # tin roof: ribbed sheets, front 2.1 -> back 2.6, .4 overhang, 5.0 wide
    x0 = -2.5 + k*5/9; x1 = x0 + 5/9 + .02; m = RUST if k == 6 else ROOF
    quadbox([(x0, -2.1, sl - .06), (x1, -2.1, sl - .06), (x1, 2.05, sh + .07), (x0, 2.05, sh + .07)], .05 + .025*(k % 2), m)
box(-2.55, -2.12, sl - .14, 2.55, -2.04, sl, TRIM)
for k in range(3): box(-1.25 + k*.35 - .03, -2.0, b0, -1.25 + k*.35 + .03, -1.95, 1.7, WOOD)        # tools leaning on the front
box(-1.4, -1.95, 1.55, -1.1, -1.9, 1.75, DARK); box(-.95, -1.95, 1.62, -.7, -1.9, 1.72, DARK)
box(-2.0, 1.85, b0, -.6, 2.3, .7, WOOD)                                # a potting bench on the back, a pot on it
cylz(-1.5, 2.08, .7, .9, .12, RED); cylz(2.6, -1.0, 0, .9, .3, SHED2, 12)   # and the drum buildFarmhouse puts there
# ======== the coop: a painted hut on legs, a tin pitched roof, a nesting box, its little door and ramp, straw
cur = "fo_coop"; groups[cur] = []
for (x, y) in ((-1, -.7), (1, -.7), (-1, .7), (1, .7)): box(x - .06, y - .06, 0, x + .06, y + .06, .7, WOOD)
box(-1.15, -.85, .6, 1.15, .85, 1.85, COOP)
for x in [-1.0 + i*.25 for i in range(9)]:
    for s in (-1, 1): box(x - .02, s*.85 - .02 + s*.02, .62, x + .02, s*.85 + .02 + s*.02, 1.83, WOOD2)
for (a, b) in ((-1.17, -1.13), (1.13, 1.17)):
    for (y0, y1) in ((-.87, -.79), (.79, .87)): box(a, y0, .6, b, y1, 1.85, TRIM)
box(-1.2, -.9, .58, 1.2, .9, .66, TRIM)
for s in (-1, 1):                                                      # gable triangles at the X ends, the ridge along Y
    x = s*1.15; vs = [(x - .02, -.85, 1.85), (x - .02, .85, 1.85), (x - .02, 0, 2.27), (x + .02, -.85, 1.85), (x + .02, .85, 1.85), (x + .02, 0, 2.27)]
    me = bpy.data.meshes.new("g"); me.from_pydata(vs, [], [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]); me.validate()
    o = bpy.data.objects.new("g", me); col.objects.link(o); me.materials.append(COOP); put(o)
for s in (-1, 1):                                                      # the roof planes, from points: ridge at y 0 z 2.3, eaves at y +-1.0
    quadbox([(-1.35, 0, 2.27), (1.35, 0, 2.27), (1.35, s*1.02, 1.73), (-1.35, s*1.02, 1.73)] if s > 0 else [(-1.35, s*1.02, 1.73), (1.35, s*1.02, 1.73), (1.35, 0, 2.27), (-1.35, 0, 2.27)], .05, ROOF)
box(-1.38, -.06, 2.28, 1.38, .06, 2.36, DARK)
box(-1.2, -.35, .9, -1.15, .1, 1.4, DARK); box(-1.22, -.4, 1.4, -1.15, .15, 1.46, TRIM)               # the pop hole on the -X end
vs = [(-1.15, -.42, .72), (-1.15, .03, .72), (-2.2, .03, .05), (-2.2, -.42, .05)]                  # the ramp down to the ground
me = bpy.data.meshes.new("ramp"); me.from_pydata(vs + [(v[0], v[1], v[2] - .05) for v in vs], [], [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]); me.validate()
o = bpy.data.objects.new("ramp", me); col.objects.link(o); me.materials.append(WOOD2); put(o)
for k in range(5):
    t = (k + .5)/5; box(-1.15 - t*1.05 - .02, -.42, .72 - t*.67, -1.15 - t*1.05 + .02, .03, .72 - t*.67 + .03, WOOD)
box(-.6, .85, .8, .6, 1.3, 1.35, COOP); quadbox([(-.66, .82, 1.4), (.66, .82, 1.4), (.66, 1.36, 1.28), (-.66, 1.36, 1.28)], .04, ROOF)   # the nesting box
box(-.5, -.88, 1.05, .2, -.86, 1.55, DARK); box(.25, -.88, 1.05, .3, -.86, 1.55, TRIM)                 # a little window, shutter
for k in range(9): a = rnd.uniform(0, 6.28); r = rnd.uniform(.3, 1.4); box(math.cos(a)*r - .12, math.sin(a)*r*.8 - .06, 0, math.cos(a)*r + .12, math.sin(a)*r*.8 + .06, .02, STRAW)
# ======== the Dutch hay barn: I-section posts, eave beams, purlins, X-braced bays, a ribbed curved tin roof with rust, posts on pads
cur = "fo_haybarn"; groups[cur] = []
L, Wd, PH, R = 18., 9., 5.6, 6.5; zc = PH - R*math.cos(.9)
for k in range(5):
    for s in (-1, 1):
        x, y = -L/2 + k*L/4, s*Wd/2
        box(x - .14, y - .14, -.5, x + .14, y + .14, .15, STONE, bev=.02)                              # a pad
        box(x - .13, y - .03, 0, x + .13, y + .03, PH, STEEL); box(x - .13, y - .13, 0, x - .1, y + .13, PH, STEEL); box(x + .1, y - .13, 0, x + .13, y + .13, PH, STEEL)
for s in (-1, 1): box(-L/2 - .2, s*Wd/2 - .1, PH - .25, L/2 + .2, s*Wd/2 + .1, PH, STEEL)
for k in range(4):                                                    # X braces in the two end bays of each side, and across the ends
    for s in (-1, 1):
        if k in (0, 3):
            x0 = -L/2 + k*L/4; x1 = x0 + L/4
            for (za, zb) in ((.4, PH - .4), (PH - .4, .4)):
                v = Vector((x1 - x0, 0, zb - za)); n = v.normalized(); p = Vector((0, 0, 1)).cross(n) if abs(n.z) < .99 else Vector((1, 0, 0))
                me = bpy.data.meshes.new("br"); t = .04; o_ = Vector((x0, s*Wd/2, za)); q = n.cross(Vector((0, 1, 0))).normalized()*t
                vs = [o_ - q + Vector((0, -t, 0)), o_ + q + Vector((0, -t, 0)), o_ + v + q + Vector((0, -t, 0)), o_ + v - q + Vector((0, -t, 0))]
                vs += [p_ + Vector((0, 2*t, 0)) for p_ in vs]
                me.from_pydata([tuple(p_) for p_ in vs], [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
                ob = bpy.data.objects.new("br", me); col.objects.link(ob); me.materials.append(STEEL); put(ob)
# the arch: rafters over every post pair, purlins along X, then the tin in 9 strips round the arc, ribbed every .9 m along X
N = 24
def arc(t): return Vector((0, R*math.sin(t), zc + R*math.cos(t)))
for k in range(5):
    x = -L/2 + k*L/4
    for i in range(N):
        a0 = -.9 + 1.8*i/N; a1 = -.9 + 1.8*(i + 1)/N; p0, p1 = arc(a0), arc(a1); nn0, nn1 = (p0 - Vector((0, 0, zc))).normalized(), (p1 - Vector((0, 0, zc))).normalized()
        vs = [(x - .07, *(p0 - nn0*.22)[1:]), (x - .07, *(p1 - nn1*.22)[1:]), (x - .07, *p1[1:]), (x - .07, *p0[1:])]
        vs += [(x + .07, v[1], v[2]) for v in vs]
        me = bpy.data.meshes.new("r"); me.from_pydata(vs, [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
        ob = bpy.data.objects.new("r", me); col.objects.link(ob); me.materials.append(STEEL); put(ob)
for i in range(1, 8):
    t = -.9 + 1.8*i/8; p = arc(t) - (arc(t) - Vector((0, 0, zc))).normalized()*.08
    box(-L/2 - .5, p.y - .06, p.z - .06, L/2 + .5, p.y + .06, p.z + .06, STEEL)
bm = bmesh.new(); XS = [-(L + 1.4)/2 + j*(L + 1.4)/40 for j in range(41)]; M_ = 30
verts = [[None]*(M_ + 1) for _ in XS]
for j, x in enumerate(XS):
    rib = .05 if j % 2 == 0 else 0.0                                  # a corrugation every other station
    for i in range(M_ + 1):
        t = -.9 + 1.8*i/M_; p = arc(t); n = (p - Vector((0, 0, zc))).normalized(); q = p + n*(.04 + rib)
        verts[j][i] = bm.verts.new((x, q.y, q.z))
for j in range(len(XS) - 1):
    for i in range(M_): bm.faces.new((verts[j][i], verts[j + 1][i], verts[j + 1][i + 1], verts[j][i + 1]))
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=.03)
me = bpy.data.meshes.new("tin"); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new("tin", me); col.objects.link(ob); me.materials.append(ROOF); me.materials.append(RUST)
for p in me.polygons:                                                # rust: two streaky patches down the lower arc
    c = p.center
    if (abs(c.x - 4) < 1.4 or abs(c.x + 6.5) < 1.0) and c.z < zc + R*math.cos(.55) and c.y > 0: p.material_index = 1
put(ob)
for s in (-1, 1): box(-L/2 - .7, s*R*math.sin(.9) - .1, zc + R*math.cos(.9) - .18, L/2 + .7, s*R*math.sin(.9) + .1, zc + R*math.cos(.9) - .02, STEEL)   # gutters
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/farm_outbuildings.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["fo_shed"].location = (-9, -11, 0); roots["fo_coop"].location = (-4, -14, 0); roots["fo_haybarn"].location = (6, 4, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.35, .45, .2), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.4; sun.color = (1, .92, .78); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-20, -27, 7); cam.rotation_euler = (Vector((0, -3, 2.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/farm_outbuildings.png"; bpy.ops.render.render(write_still=True)
