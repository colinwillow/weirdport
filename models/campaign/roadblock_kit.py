# roadblock_kit.py -- the police line, as pieces the gate code tiles across any width (replaces gateMesh's posts + tape for
# `cordon`, and the orange/white blocks for `barricade` / `pbarricade`).
# CONTRACT: ONE GLB, one root node per piece, origin = the piece's centre ON THE GROUND, Blender X = ALONG the line (three x),
# Blender -Y = the side the player approaches from (three +z = the gate's local normal in gateMesh). Pieces:
#   rb_sawhorse   2.2 m  (tile across w)          rb_car      4.6 m police car, parked ACROSS the line (its length along X)
#   rb_cone       0.5 m  (scatter in front)       rb_jersey   2.0 m concrete barrier (the `barricade` look)
#   rb_fence      2.4 m  crowd-control steel fence with a POLICE LINE sign (the protest's `pbarricade`)
#   rb_lightpost  a work light on a tripod (one per line, at an end)
# Colliders: col_bld_<piece> -- one exact box each, same origin, for the loop to place with its piece. Height of the solid line
# is 1.25 m on the sawhorse / jersey / fence and 1.5 m on the car: with GATE.hi above that, a jump over is a deliberate choice.
import bpy, bmesh, math, os
from mathutils import Vector, Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection
exec(open("/home/claude/campaign/farm_vehicles.py").read().split("TYRE = mat")[0].split("bpy.ops.wm.read_factory_settings(use_empty=True)")[1])   # mat, box, cyl, tyre, lathe, fender
TYRE = mat("FV_tyre", (.06, .06, .07), .85); CHROME = mat("FV_chrome", (.82, .82, .8), .25, .8); GLASS = mat("FV_glass", (.3, .4, .48), .05, alpha=.5)
WHITE = mat("RB_white", (.93, .93, .9), .5); BLACK = mat("RB_black", (.07, .07, .08), .45); ORANGE = mat("RB_orange", (1.0, .38, .08), .5)
RED_L = mat("RB_red_lamp", (1, .1, .05), .3, emit=(1, .1, .05)); BLUE_L = mat("RB_blue_lamp", (.1, .3, 1), .3, emit=(.15, .35, 1))
AMBER = mat("RB_amber", (1, .7, .1), .3, emit=(1, .65, .1)); CONC = mat("RB_concrete", (.72, .7, .66), .9); STEEL = mat("RB_steel", (.55, .57, .6), .4, .5)
YELLOW = mat("RB_yellow", (1, .82, .15), .5); LAMP = mat("FV_lamp", (1, .95, .8), .3, emit=(1, .9, .6))
pieces = {}
def root(name):
    e = bpy.data.objects.new(name, None); col.objects.link(e); pieces[name] = e; return e
def grp(name, parts):
    r = root(name)
    for p in parts: p.parent = r
    return r
def cbox(name, sx, sy, sz):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.scale = (sx, sy, sz); o.location = (0, 0, sz/2); o["collider"] = "bld_"; return o
# ---- sawhorse: two A-frame legs, a striped board (diagonal orange/white), a blinking amber lamp
P = []
for x in (-.95, .95):
    for s in (-1, 1):
        l = box("sh_leg", x, s*.22, .55, .07, .07, 1.15, WHITE, .015); l.rotation_euler = (s*.38, 0, 0); P.append(l)
for k in range(9):                                                                        # the striped board: diagonal stripes as slanted slats
    m = ORANGE if k % 2 else WHITE; x = -1.05 + k*.2625
    b = box("sh_stripe%d" % k, x, 0, 1.0, .27, .05, .3, m, .0); P.append(b)
P.append(box("sh_board_lo", 0, 0, .45, 2.0, .05, .16, WHITE, .01))
P.append(lathe("sh_lamp", [(0, 0), (.09, 0), (.09, .08), (0, .1)], AMBER, 12, axis='Z', at=(.85, 0, 1.18)))
grp("rb_sawhorse", P); c = cbox("col_bld_rb_sawhorse", 2.2, .5, 1.25)
# ---- cone
P = [lathe("cone_body", [(.2, 0), (.17, .12), (.05, .72), (0, .74)], ORANGE, 20, axis='Z'), box("cone_base", 0, 0, .02, .42, .42, .04, BLACK, .01),
     lathe("cone_band", [(.125, .4), (.105, .4), (.085, .52), (.105, .52)], WHITE, 20, axis='Z')]
grp("rb_cone", P); cbox("col_bld_rb_cone", .42, .42, .74)
# ---- jersey barrier
bm = bmesh.new(); prof = [(-.3, 0), (-.3, .08), (-.2, .25), (-.08, .8), (.08, .8), (.2, .25), (.3, .08), (.3, 0)]
F = [[bm.verts.new((x, y, z)) for (y, z) in prof] for x in (-1, 1)]
for i in range(len(prof) - 1): bm.faces.new((F[0][i], F[1][i], F[1][i + 1], F[0][i + 1]))
bm.faces.new(F[0][::-1]); bm.faces.new(F[1])
me = bpy.data.meshes.new("jersey"); bm.to_mesh(me); bm.free(); jo = bpy.data.objects.new("jersey", me); col.objects.link(jo); finish(jo, CONC, smooth=False)
grp("rb_jersey", [jo, box("jersey_stripe", 0, -.12, .55, 1.8, .02, .08, YELLOW, .0)]); cbox("col_bld_rb_jersey", 2.0, .6, 1.25)
# ---- crowd fence with a sign
P = [box("fence_top", 0, 0, 1.1, 2.4, .05, .05, STEEL, .01), box("fence_bot", 0, 0, .25, 2.4, .05, .05, STEEL, .01)]
for x in (-1.2, 1.2): P += [box("fence_post", x, 0, .58, .05, .05, 1.1, STEEL, .01), box("fence_foot", x, 0, .03, .08, .7, .05, STEEL, .01)]
for k in range(13): P.append(box("fence_bar%d" % k, -1.08 + k*.18, 0, .67, .022, .022, .84, STEEL, .0))
P += [box("fence_sign", 0, -.04, .7, 1.1, .02, .34, WHITE, .01), box("fence_sign_band", 0, -.055, .7, 1.0, .01, .1, mat("RB_blue", (.12, .2, .55), .5), .0)]
grp("rb_fence", P); cbox("col_bld_rb_fence", 2.4, .7, 1.25)
# ---- the work light
P = [box("lp_leg%d" % k, .35*math.cos(2*math.pi*k/3), .35*math.sin(2*math.pi*k/3), .75, .04, .04, 1.6, BLACK, .01) for k in range(3)]
for p_, k in zip(P, range(3)): p_.rotation_euler = (-.22*math.sin(2*math.pi*k/3), .22*math.cos(2*math.pi*k/3), 0)
P += [cyl("lp_mast", 0, 0, 1.8, .03, 1.2, BLACK, 'Z'), box("lp_head", 0, -.05, 2.45, .5, .18, .32, BLACK, .03), box("lp_lens", 0, -.15, 2.45, .44, .02, .26, LAMP, .0)]
grp("rb_lightpost", P)
# ---- the police car: retro toon cruiser, black and white, light bar, push bar
B = BLACK; W_ = WHITE; P = []
P.append(box("car_body_lo", 0, 0, .62, 4.4, 1.85, .5, B, .12))                              # length along X (the line)
P.append(box("car_doors", 0, 0, .66, 2.1, 1.87, .44, W_, .06))                              # the white door panels
P.append(box("car_cabin", -.1, 0, 1.2, 2.2, 1.65, .6, W_, .18))
P.append(box("car_roof", -.1, 0, 1.52, 1.9, 1.5, .08, W_, .05))
for s in (-1, 1):
    P.append(box("car_side_win%d" % s, -.1, s*.83, 1.24, 1.9, .03, .42, GLASS, .02))
    for x in (-1.35, 1.35): P += tyre("car_wheel%d%d" % (s, int(x)), x, s*.86, .38, .38, .26, TYRE, CHROME) if False else []
for x in (-1.35, 1.35):
    for s in (-1, 1):
        t = cyl("car_tyre%d%d" % (s, int(x*10)), x, s*.86, .38, .38, .26, TYRE, 'Y', 24, bevel=.04); P.append(t)
        h = cyl("car_hub%d%d" % (s, int(x*10)), x, s*(.86 + .135), .38, .2, .02, CHROME, 'Y', 16); P.append(h)
P.append(box("car_windshield", 1.02, 0, 1.18, .04, 1.5, .4, GLASS, .02)); P[-1].rotation_euler = (0, math.radians(30), 0)
P.append(box("car_rearwin", -1.22, 0, 1.18, .04, 1.45, .38, GLASS, .02)); P[-1].rotation_euler = (0, math.radians(-30), 0)
P.append(box("car_grille", 2.22, 0, .65, .05, 1.2, .26, CHROME, .02))
P.append(box("car_pushbar", 2.38, 0, .62, .1, 1.1, .45, B, .03))
for s in (-1, 1):
    P.append(lathe("car_headlamp%d" % s, [(0, 0), (.13, 0), (.13, .05), (0, .07)], LAMP, 14, axis='X', at=(2.21, s*.62, .78)))
    P.append(box("car_tail%d" % s, -2.21, s*.65, .78, .04, .22, .12, RED_L, .01))
P.append(box("car_badge", 0, -.94, .72, .4, .01, .4, YELLOW, .01))                           # the star on the door
P.append(box("car_lightbar", -.1, 0, 1.63, .35, 1.3, .14, B, .04))
P.append(box("car_light_red", -.1, -.35, 1.72, .3, .5, .12, RED_L, .03)); P.append(box("car_light_blue", -.1, .35, 1.72, .3, .5, .12, BLUE_L, .03))
grp("rb_car", P); cbox("col_bld_rb_car", 4.6, 1.95, 1.5)
# lay them out for the preview, export with roots at the origin
bpy.context.view_layer.update()
out = "/home/claude/weirdport/models/campaign"
vis_roots = [pieces[k] for k in pieces]; cols = [o for o in col.objects if o.name.startswith("col_")]
def sel(objs):
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs:
        o.select_set(True)
        for c_ in o.children_recursive: c_.select_set(True)
sel(vis_roots); bpy.ops.export_scene.gltf(filepath=os.path.join(out, "roadblock_kit.glb"), export_format='GLB', use_selection=True, export_extras=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
sel(cols); bpy.ops.export_scene.gltf(filepath=os.path.join(out, "roadblock_kit_collision.glb"), export_format='GLB', use_selection=True, export_extras=True, export_yup=True, export_apply=True)
dg = bpy.context.evaluated_depsgraph_get()
for k, r in pieces.items(): print(k, sum(len(c_.evaluated_get(dg).data.polygons) for c_ in r.children_recursive if c_.type == 'MESH'))
# preview: a bridge line -- car, sawhorses, cones, a light
for c_ in cols: c_.hide_render = True
layout = [("rb_car", (-4.5, 0, 0), 0), ("rb_sawhorse", (-1.1, 0, 0), 0), ("rb_sawhorse", (1.1, 0, 0), 0), ("rb_jersey", (3.3, 0, 0), 0), ("rb_fence", (5.8, 0, 0), 0),
          ("rb_lightpost", (7.6, .8, 0), 0)]
for name, p, rz in layout:
    r = pieces[name]
    if r.get("_used"):
        d = bpy.data.objects.new(name + "_dup", None); col.objects.link(d)
        for c_ in r.children:
            cc = c_.copy(); col.objects.link(cc); cc.parent = d
        r = d
    r["_used"] = 1; r.location = p; r.rotation_euler = (0, 0, rz)
for k, (x, y) in enumerate([(-2, -1.4), (.3, -1.6), (2.5, -1.3), (-.8, -2.2)]):
    d = bpy.data.objects.new("cone_dup%d" % k, None); col.objects.link(d)
    for c_ in pieces["rb_cone"].children:
        cc = c_.copy(); col.objects.link(cc); cc.parent = d
    d.location = (x, y, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.render.resolution_x = 1280; sc.render.resolution_y = 720
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (.6, .7, .85, 1)
g = bpy.data.meshes.new("g"); g.from_pydata([(-30, -30, 0), (30, -30, 0), (30, 30, 0), (-30, 30, 0)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.3, .3, .32), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 4; so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(45), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 30; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (1.0, -11.5, 3.2); cam.rotation_euler = (Vector((1.0, 0, .9)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/roadblock_kit.png"; bpy.ops.render.render(write_still=True)
