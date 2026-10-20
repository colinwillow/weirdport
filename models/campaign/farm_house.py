# farm_house.py -- Gristle Farm's farmhouse shell and porch as art, at buildFarmhouse's exact numbers (FHOUSE: W 9 along u,
# D 7 along v, floors E1 3.0 / eaves E2 5.8 / ridge 8.1 over the floor, walls .25, porch 2.3 deep on -v, roof .55 overhang).
# buildFarmhouse keeps every collider, the porch's walkable roof triangles, the steps, the chairs, the barrel and log pile,
# the shed and the coop. CONTRACT: Blender X = frame u, Blender +Y = frame +v (so the porch and front door face Blender -Y),
# origin = (hu, hv) at the house FLOOR y0 (the plinth runs down to -1.6 to bury itself on a slope). Ridge along X; gables at +-X;
# chimney outside the +X gable at (W2+.55, +.9), its top at RIDGE+1.1+.15 (FHOUSE.chim, where the smoke comes out).
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection; rnd = random.Random(9)
def mat(name, rgb, rough=.85, metal=0., emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = .7
    return m
CREAM = mat("FH_cream", (.86, .82, .72)); CREAM2 = mat("FH_cream_lap", (.76, .72, .62)); TRIM = mat("FH_trim", (.95, .93, .88)); ROOF = mat("FH_roof", (.42, .2, .14))
ROOF2 = mat("FH_roof_faded", (.52, .3, .22)); STONE = mat("FH_stone", (.53, .51, .47), 1); STONE2 = mat("FH_stone_dark", (.38, .37, .34), 1)
SHUT = mat("FH_shutter", (.16, .3, .22)); DARK = mat("FH_dark", (.1, .09, .08)); WOOD = mat("FH_wood", (.45, .31, .19)); DOOR = mat("FH_door", (.55, .18, .14))
GLOW = mat("FH_glow", (.12, .1, .07), .2, 0, (1.0, .77, .42)); BLOOM = [mat("FH_bloom_y", (.97, .75, .2), .7), mat("FH_bloom_r", (.9, .25, .2), .7)]; METAL = mat("FH_metal", (.6, .63, .65), .45, .4)
L = []
def box(name, x0, y0, z0, x1, y1, z1, m, bev=0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co = Vector(((v.co.x + .5)*(x1 - x0) + x0, (v.co.y + .5)*(y1 - y0) + y0, (v.co.z + .5)*(z1 - z0) + z0))
    if bev: bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bev, segments=1, affect='EDGES')
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m); L.append(o); return o
def mesh(name, vs, fs, m):
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m); L.append(o); return o
W, D, E1, E2, RIDGE, T, P = 9., 7., 3., 5.8, 8.1, .25, 2.3; W2, D2 = W/2, D/2
# ---- plinth: stone, a proud top course, buried deep (the floor stands .5 over the highest corner)
box("plinth", -W2 - .15, -D2 - .15, -1.6, W2 + .15, D2 + .15, -.05, STONE2); box("plinth_top", -W2 - .22, -D2 - .22, -.2, W2 + .22, D2 + .22, 0, STONE, bev=.03)
for k in range(18):
    s = k % 4; t = rnd.uniform(-.9, .9); z = rnd.uniform(-.55, -.3); w = rnd.uniform(.3, .6)
    if s < 2: y = (-D2 - .17) if s == 0 else (D2 + .17); x = t*W2; box("st", x - w/2, y - .03, z - .1, x + w/2, y + .03, z + .1, STONE)
    else: x = (-W2 - .17) if s == 2 else (W2 + .17); y = t*D2; box("st", x - .03, y - w/2, z - .1, x + .03, y + w/2, z + .1, STONE)
# ---- walls, then clapboard laps every .3 m (a thin proud strip at each board's foot) on every face, gaps left for openings
box("wf", -W2, -D2 - T/2, 0, W2, -D2 + T/2, E2, CREAM); box("wb", -W2, D2 - T/2, 0, W2, D2 + T/2, E2, CREAM)
box("wl", -W2 - T/2, -D2, 0, -W2 + T/2, D2, E2, CREAM); box("wr", W2 - T/2, -D2, 0, W2 + T/2, D2, E2, CREAM)
# the openings, (face, centre along the face, z0, w, h) -- buildFarmhouse's `win` calls and the door, for the laps to skip
WINS = [("f", -3, .9, 1.0, 1.3), ("f", 3, .9, 1.0, 1.3), ("f", -2.9, E1 + .55, .9, 1.1), ("f", 0, E1 + .55, .9, 1.1), ("f", 2.9, E1 + .55, .9, 1.1),
        ("b", -2.6, .9, 1.0, 1.3), ("b", 2.6, .9, 1.0, 1.3), ("b", -2.9, E1 + .55, .9, 1.1), ("b", 0, E1 + .55, .9, 1.1), ("b", 2.9, E1 + .55, .9, 1.1),
        ("l", 0, .9, 1.0, 1.3), ("l", 0, E1 + .55, .9, 1.1), ("r", -1.6, .9, .8, 1.2)]
OPEN = WINS + [("f", 0, 0, 1.4, 2.6)]
def laps(face, span, z0, z1, gable=False):
    o = -1 if face in "fl" else 1
    for k in range(int((z1 - z0)/.3)):
        z = z0 + k*.3; a, b = -span, span
        if gable: h = (z - E2)/(RIDGE - E2); a, b = -span*(1 - h), span*(1 - h)
        if b - a < .3: break
        cuts = sorted([(c - w/2 - .35, c + w/2 + .35) for (f, c, zz, w, hh) in OPEN if f == face and zz - .1 < z + .06 < zz + hh + .12])
        x = a
        for (c0, c1) in cuts + [(b, b)]:
            if c0 > x + .05:
                if face in "fb": box("lap", x, o*(D2 + T/2), z, c0, o*(D2 + T/2) + o*.03, z + .06, CREAM2)
                else: box("lap", o*(W2 + T/2), x, z, o*(W2 + T/2) + o*.03, c0, z + .06, CREAM2)
            x = max(x, c1)
for f in "fb": laps(f, W2, .2, E2)
for f in "lr": laps(f, D2, .2, E2)
# gables at +-X (the shape spans Y), clapboarded, with a small attic window
for s in (-1, 1):
    x0, x1 = s*W2 - T/2, s*W2 + T/2
    mesh("gab", [(x0, -D2 - .12, E2), (x0, D2 + .12, E2), (x0, 0, RIDGE), (x1, -D2 - .12, E2), (x1, D2 + .12, E2), (x1, 0, RIDGE)],
         [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)], CREAM)
    laps("l" if s < 0 else "r", D2, E2 + .1, RIDGE - .3, gable=True)
    box("attic", s*(W2 + T/2) - .04, -.35, 6.55, s*(W2 + T/2) + .04, .35, 7.15, GLOW)
    box("attic_fr", s*(W2 + T/2 + .02) - .04, -.45, 6.45, s*(W2 + T/2 + .02) + .04, .45, 6.55, TRIM)
# trim: corner boards, the floor band (E1), a frieze under the eaves, the rakes
for a in (-1, 1):
    for b in (-1, 1): box("cn", a*(W2 + .02) - .13, b*(D2 + .02) - .13, 0, a*(W2 + .02) + .13, b*(D2 + .02) + .13, E2 + .05, TRIM)
for s in (-1, 1):
    box("band", -W2 - .05, s*(D2 + .02) - T/2 - .03, E1 - .08, W2 + .05, s*(D2 + .02) + T/2 + .03, E1 + .08, TRIM)
    box("frieze", -W2 - .05, s*(D2 + .02) - T/2 - .04, E2 - .35, W2 + .05, s*(D2 + .02) + T/2 + .04, E2 - .05, TRIM)
    box("bandE", s*(W2 + .02) - T/2 - .03, -D2, E1 - .08, s*(W2 + .02) + T/2 + .03, D2, E1 + .08, TRIM)
# ---- windows: a lit pane with a cross mullion, a sill and a head (the formula's sill and lintel), louvred green shutters
for (f, c, z, w, h) in WINS:
    o = -1 if f in "fl" else 1; d = (D2 if f in "fb" else W2) + T/2
    def B(n, a0, a1, z0, z1, t0, t1, m):
        if f in "fb": box(n, a0, o*(d + t0), z0, a1, o*(d + t1), z1, m)
        else: box(n, o*(d + t0), a0, z0, o*(d + t1), a1, z1, m)
    B("pane", c - w/2, c + w/2, z, z + h, -.02, .02, GLOW)
    B("mv", c - .03, c + .03, z, z + h, .02, .05, TRIM); B("mh", c - w/2, c + w/2, z + h*.55 - .03, z + h*.55 + .03, .02, .05, TRIM)
    for (a0, a1, z0, z1) in ((c - w/2 - .08, c - w/2, z, z + h), (c + w/2, c + w/2 + .08, z, z + h)): B("jamb", a0, a1, z0, z1, .0, .07, TRIM)
    B("sill", c - w/2 - .18, c + w/2 + .18, z - .12, z, .0, .14, TRIM); B("head", c - w/2 - .14, c + w/2 + .14, z + h, z + h + .14, .0, .1, TRIM)
    B("headcap", c - w/2 - .2, c + w/2 + .2, z + h + .14, z + h + .19, .0, .14, TRIM)
    for sd in (-1, 1):
        a0 = c + sd*(w/2 + .08) + (0 if sd > 0 else -.45); B("shut", a0, a0 + .45, z, z + h, .02, .06, SHUT)
        for k in range(int(h/.12)): B("louv", a0 + .05, a0 + .4, z + .06 + k*.12, z + .1 + k*.12, .06, .08, SHUT)
    if f in "fb" and z < 2: B("box", c - w/2 - .1, c + w/2 + .1, z - .45, z - .12, .02, .3, WOOD)          # a window box under the ground-floor fronts
    if f in "fb" and z < 2:
        for k in range(5):
            a = c - w/2 + k*w/4; B("bloom", a - .07, a + .07, z - .14, z, .1, .24, BLOOM[k % 2])
# ---- the front door: panelled, a fanlight over it (lit), its frame and a little hood
y = -D2 - T/2
box("door", -.55, y - .06, 0, .55, y - .02, 2.2, DOOR)
for (x0, x1, z0, z1) in ((-.42, -.06, .2, 1.0), (.06, .42, .2, 1.0), (-.42, -.06, 1.15, 2.0), (.06, .42, 1.15, 2.0)): box("panel", x0, y - .09, z0, x1, y - .06, z1, DOOR)
box("knob", .32, y - .13, 1.0, .4, y - .07, 1.08, METAL); box("fan", -.55, y - .05, 2.25, .55, y - .01, 2.55, GLOW)
for (x0, x1, z0, z1) in ((-.7, -.55, 0, 2.6), (.55, .7, 0, 2.6), (-.7, .7, 2.2, 2.28), (-.75, .75, 2.55, 2.68)): box("dfr", x0, y - .1, z0, x1, y, z1, TRIM)
# ---- the roof: ridge along X; courses laid from points on each slope (no rotations: the barn's lesson)
run = D2 + .55; ang = math.atan2(RIDGE - E2, D2); sl = run/math.cos(ang); ca, sa = math.cos(ang), math.sin(ang)
def slab(sd, d0, d1, t0, t1, x0, x1, m):
    Pt = lambda d, t: (sd*(d*ca + t*sa), RIDGE + .08 - d*sa + t*ca)
    vs = [(x0, *Pt(d, t)) for (d, t) in ((d0, t0), (d1, t0), (d1, t1), (d0, t1))] + [(x1, *Pt(d, t)) for (d, t) in ((d0, t0), (d1, t0), (d1, t1), (d0, t1))]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    if sd > 0: f = [tuple(reversed(q)) for q in f]
    return mesh("roof", vs, f, m)
for sd in (-1, 1):
    slab(sd, 0, sl, -.12, 0, -W2 - .55, W2 + .55, ROOF); n = int(sl/.42)
    for k in range(n):
        slab(sd, k*sl/n, (k + 1)*sl/n + .06, 0, .06 + .03*(k % 2), -W2 - .55, W2 + .55, ROOF2 if rnd.random() < .2 else ROOF)
    slab(sd, sl - .02, sl + .02, -.25, .08, -W2 - .55, W2 + .55, TRIM)                    # the fascia at the eave
    box("gutter", -W2 - .55, sd*(run + .03) - .1, RIDGE + .08 - sl*sa - .32, W2 + .55, sd*(run + .03) + .1, RIDGE + .08 - sl*sa - .14, METAL)
box("ridgecap", -W2 - .6, -.18, RIDGE + .04, W2 + .6, .18, RIDGE + .26, DARK)
for s in (-1, 1):                                            # rake boards up each gable edge, built from points too
    for sd in (-1, 1):
        a = (s*(W2 + .5) - .08, s*(W2 + .5) + .08)
        vs = []
        for x in a:
            vs += [(x, 0, RIDGE + .2), (x, sd*run, RIDGE + .08 - sl*sa + .12), (x, sd*run, RIDGE + .08 - sl*sa - .14), (x, 0, RIDGE - .06)]
        fs = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        if sd < 0: fs = [tuple(reversed(q)) for q in fs]
        mesh("rake", vs, fs, TRIM)
box("pipe", W2 + .3, -run + .1, 0, W2 + .4, -run + .2, RIDGE + .08 - sl*sa - .2, METAL)
# ---- the chimney outside the +X gable: stone, a corbelled cap, two pots
cx, cy = W2 + .55, .9; ch = RIDGE + 1.1
box("chim", cx - .55, cy - .55, -1.6, cx + .55, cy + .55, ch, STONE)
for k in range(int((ch + 1.6)/.6)): box("chc", cx - .57, cy - .57, -1.6 + k*.6 + .28, cx + .57, cy + .57, -1.6 + k*.6 + .32, STONE2)
box("chcap", cx - .65, cy - .65, ch, cx + .65, cy + .65, ch + .15, STONE, bev=.03)
for dx in (-.22, .22):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=.15, radius2=.12, depth=.4)
    me = bpy.data.meshes.new("pot"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("pot", me); col.objects.link(o); me.materials.append(ROOF2); me.transform(Matrix.Translation((cx + dx, cy, ch + .35))); L.append(o)
# ---- the porch: board floor, turned posts, rails with balusters, its own shingled roof (wall 2.75 -> posts 2.4)
pv0 = -D2 - P; pr0, pr1 = 2.75, 2.4
box("pfloor", -W2 + .1, pv0, -.12, W2 - .1, -D2, 0, WOOD)
for k in range(int(W/.18)): box("pboard", -W2 + .1 + k*.18, pv0, 0, -W2 + .1 + k*.18 + .015, -D2, .005, DARK)
box("pfascia", -W2 + .1, pv0 - .03, -.4, W2 - .1, pv0, 0, TRIM)
for du in (-W2 + .25, -1.3, 1.3, W2 - .25):
    box("post", du - .1, pv0 + .05, 0, du + .1, pv0 + .25, pr1, TRIM)
    box("postb", du - .13, pv0 + .02, 0, du + .13, pv0 + .28, .3, TRIM); box("postc", du - .14, pv0 + .01, pr1 - .2, du + .14, pv0 + .29, pr1, TRIM)
for sd in (-1, 1):
    box("rail", sd*(W2 - .25) - .05, pv0 + .15, .85, sd*(W2 - .25) + .05, -D2 - .1, .95, TRIM)
    box("railf", sd*1.25 - (0 if sd > 0 else 3.0), pv0 + .1, .85, sd*1.25 + (3.0 if sd > 0 else 0), pv0 + .2, .95, TRIM)
    for k in range(6): x = sd*(1.5 + k*.5); box("bal", x - .03, pv0 + .12, 0, x + .03, pv0 + .18, .85, TRIM)
    for k in range(4): y = pv0 + .6 + k*.45; box("bal", sd*(W2 - .25) - .03, y - .03, 0, sd*(W2 - .25) + .03, y + .03, .85, TRIM)
Lr = math.hypot(P + .3, pr0 - pr1); tl = math.atan2(pr0 - pr1, P + .3)
for k in range(7):
    d0, d1 = k*Lr/7, (k + 1)*Lr/7 + .05; th = .05 + .02*(k % 2)
    y0_, z0_ = -D2 - d0*math.cos(tl), pr0 - d0*math.sin(tl); y1_, z1_ = -D2 - d1*math.cos(tl), pr0 - d1*math.sin(tl)
    vs = [(-W2 - .15, y0_, z0_ - .06), (-W2 - .15, y1_, z1_ - .06), (-W2 - .15, y1_, z1_ + th), (-W2 - .15, y0_, z0_ + th)]
    vs += [(W2 + .15, v[1], v[2]) for v in vs]
    mesh("proof", vs, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], ROOF2 if k % 3 == 0 else ROOF)
box("pbeam", -W2 - .15, pv0 + .02, pr1 - .25, W2 + .15, pv0 + .3, pr1, TRIM)
box("plamp", -.12, -D2 - T/2 - .25, 2.5, .12, -D2 - T/2 - .05, 2.7, GLOW)
# ---- join and export
for o in bpy.context.view_layer.objects: o.select_set(False)
for o in L: o.select_set(True)
bpy.context.view_layer.objects.active = L[0]; bpy.ops.object.join(); j = bpy.context.view_layer.objects.active; j.name = "fh_house_mesh"
r = bpy.data.objects.new("fh_house", None); col.objects.link(r); j.parent = r
print("fh_house", len(j.data.polygons), "faces", len(j.data.materials), "materials")
for o in bpy.context.view_layer.objects: o.select_set(False)
r.select_set(True); j.select_set(True)
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/farm_house.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-60, -60, -.5), (60, -60, -.5), (60, 60, -.5), (-60, 60, -.5)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.35, .45, .2), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.4; sun.color = (1, .92, .78); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 30; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-13, -20, 4.5); cam.rotation_euler = (Vector((.5, 0, 3.6)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/farm_house.png"; bpy.ops.render.render(write_still=True)
