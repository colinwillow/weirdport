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




# container.py -- the Waterfront's shipping container as art, at buildWaterfront's numbers: CW 2.44 (Blender X = the block's u),
# CL 12.2 (Blender Y = its v), CH 2.6 (Z). Origin at the BOTTOM CENTRE. Doors on the +Y end (the code picks an end per box: turn
# by pi for e = -1). TWO roots, so the whole yard stays two InstancedMeshes:
#   wf_container_body  the painted shell -- corrugated sides, the roof, the far end, the door leaves -- in ONE white material,
#                      tinted per instance with `setColorAt` from c0..c8 (white x paint = the paint)
#   wf_container_trim  the steel that is NOT painted: corner posts, eight corner castings, top and bottom rails, the four locking
#                      bars and their handles, the hinges -- one dark material, never tinted
PAINT = mat("WF_paint", (1, 1, 1), .7, .3); TRIMM = mat("WF_trim", (.16, .17, .19), .6, .5)
CW, CL, CH = 2.44, 12.2, 2.6; P = .32                       # a corrugation every .32 m
def body_mesh():
    vs, fs = [], []
    def quad(a, b, c, d):
        i = len(vs); vs.extend([a, b, c, d]); fs.append((i, i + 1, i + 2, i + 3))
    z0, z1 = .12, CH - .12
    for s in (-1, 1):                                         # the long sides: a trapezoid corrugation, in and out by .05
        x0 = s*CW/2; n = int((CL - .5)/P); y0 = -(n*P)/2
        for k in range(n):
            ya, yb, yc, yd = y0 + k*P, y0 + k*P + P*.25, y0 + k*P + P*.5, y0 + k*P + P*.75
            ye = y0 + (k + 1)*P
            xo, xi = x0, x0 - s*.05
            for (p0, p1, xx0, xx1) in ((ya, yb, xo, xi), (yb, yc, xi, xi), (yc, yd, xi, xo), (yd, ye, xo, xo)):
                if s > 0: quad((xx0, p0, z0), (xx1, p1, z0), (xx1, p1, z1), (xx0, p0, z1))
                else: quad((xx1, p1, z0), (xx0, p0, z0), (xx0, p0, z1), (xx1, p1, z1))
        for (ya, yb) in ((-CL/2 + .12, y0), (y0 + n*P, CL/2 - .12)):
            if s > 0: quad((x0, ya, z0), (x0, yb, z0), (x0, yb, z1), (x0, ya, z1))
            else: quad((x0, yb, z0), (x0, ya, z0), (x0, ya, z1), (x0, yb, z1))
    quad((-CW/2, -CL/2, CH - .05), (CW/2, -CL/2, CH - .05), (CW/2, CL/2, CH - .05), (-CW/2, CL/2, CH - .05))[::-1] if False else None
    i = len(vs); vs.extend([(-CW/2, -CL/2, CH - .04), (CW/2, -CL/2, CH - .04), (CW/2, CL/2, CH - .04), (-CW/2, CL/2, CH - .04)]); fs.append((i, i + 1, i + 2, i + 3))
    i = len(vs); vs.extend([(-CW/2, -CL/2, .05), (-CW/2, CL/2, .05), (CW/2, CL/2, .05), (CW/2, -CL/2, .05)]); fs.append((i, i + 1, i + 2, i + 3))
    for k in range(6):                                        # the blind end (-Y): vertical corrugation too
        x0 = -CW/2 + .12 + k*(CW - .24)/6; x1 = x0 + (CW - .24)/6; xm = (x0 + x1)/2
        quad((x1, -CL/2, z0), (xm, -CL/2 + .05, z0), (xm, -CL/2 + .05, z1), (x1, -CL/2, z1)); quad((xm, -CL/2 + .05, z0), (x0, -CL/2, z0), (x0, -CL/2, z1), (xm, -CL/2 + .05, z1))
    for s in (-1, 1):                                         # the doors (+Y): two leaves, each with three horizontal swages
        xa, xb = (0, CW/2 - .12) if s > 0 else (-CW/2 + .12, 0)
        zs = [z0, .7, .78, 1.3, 1.38, 1.9, 1.98, z1]
        for k in range(len(zs) - 1):
            yy = CL/2 - (.02 if k % 2 else 0)
            quad((xa, yy, zs[k]), (xb, yy, zs[k]), (xb, yy, zs[k + 1]), (xa, yy, zs[k + 1]))
    me = bpy.data.meshes.new("cb"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("cb", me); col.objects.link(o); me.materials.append(PAINT); return put(o)
cur = "wf_container_body"; groups[cur] = []; body_mesh()
cur = "wf_container_trim"; groups[cur] = []
for a in (-1, 1):
    for b in (-1, 1):
        box(a*CW/2 - (.12 if a > 0 else 0), b*CL/2 - (.12 if b > 0 else 0), 0, a*CW/2 + (0 if a > 0 else .12), b*CL/2 + (0 if b > 0 else .12), CH, TRIMM)   # corner posts
        for z in (0, CH - .12): box(a*CW/2 - (.14 if a > 0 else -.0) - (0 if a > 0 else .02), b*CL/2 - (.18 if b > 0 else 0) - (0 if b > 0 else .02), z, a*CW/2 + (.02 if a > 0 else .14), b*CL/2 + (.02 if b > 0 else .18), z + .12, TRIMM)   # castings
for z in (0, CH - .12):
    for s in (-1, 1): box(s*CW/2 - .06, -CL/2, z, s*CW/2 + .06, CL/2, z + .12, TRIMM)
    for b in (-1, 1): box(-CW/2, b*CL/2 - .06, z, CW/2, b*CL/2 + .06, z + .12, TRIMM)
for x in (-.85, -.35, .35, .85):                              # the locking bars, cams, handles
    cylz(x, CL/2 + .06, .1, CH - .1, .025, TRIMM, 6)
    for z in (.18, CH - .18): box(x - .05, CL/2 + .03, z - .05, x + .05, CL/2 + .1, z + .05, TRIMM)
    box(x - .02, CL/2 + .06, 1.05, x + .18 if x > 0 else x + .02, CL/2 + .12, 1.15, TRIMM) if True else None
for s in (-1, 1):
    for z in (.35, 1.0, 1.65, 2.25): box(s*(CW/2 - .14) - .04, CL/2, z, s*(CW/2 - .14) + .04, CL/2 + .06, z + .14, TRIMM)   # hinges
box(-.3, CL/2 + .01, 1.95, .3, CL/2 + .02, 2.25, mat("WF_plate", (.85, .85, .8), .5))      # the data plate (unpainted)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/container.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
# preview: a small stack, instanced by hand with the yard's own paints
cols = [(.6, .29, .16), (.16, .35, .54), (.23, .42, .29), (.78, .63, .16), (.85, .85, .82), (.66, .2, .2), (.16, .48, .48), (.48, .48, .5), (.78, .39, .16)]
bodyM = roots["wf_container_body"].children[0]; trimM = roots["wf_container_trim"].children[0]
import random as _r; rr = _r.Random(4); k = 0
for (cx, h) in ((-5, 3), (-2.5, 4), (0, 2), (2.5, 3), (5, 1)):
    for l in range(h):
        mb = bpy.data.materials.new("p%d" % k); mb.use_nodes = True; mb.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*cols[rr.randrange(9)], 1); mb.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = .7
        b = bodyM.copy(); b.data = bodyM.data.copy(); b.data.materials[0] = mb; col.objects.link(b); b.parent = None; b.location = (cx, rr.uniform(-.15, .15), l*2.6); b.rotation_euler = (0, 0, 0 if rr.random() < .5 else math.pi)
        t = trimM.copy(); col.objects.link(t); t.parent = None; t.location = b.location; t.rotation_euler = b.rotation_euler; k += 1
roots["wf_container_body"].location = (999, 0, 0); roots["wf_container_trim"].location = (999, 0, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.56, .55, .52), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-40))
cd = bpy.data.cameras.new("C"); cd.lens = 26; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-12, 16, 6); cam.rotation_euler = (Vector((0, 2, 4)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/container.png"; bpy.ops.render.render(write_still=True)
