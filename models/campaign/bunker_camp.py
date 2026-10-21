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



# trailer_park.py -- Hollow Creek's trailer park homes as art, at buildTrailerPark's numbers (the code keeps every platform,
# post, the walk, porches, ramps, ladder, laundry and colliders). Blender X = across the gorge (the frame's u), +Y = along it (v).
#   tp_trailer_cream / _tin / _rust / _red   a single-wide, 2.6 wide (X) x 10 long (Y) x 2.7 to the roof, origin at its centre on
#              its FLOOR (yp). Door, windows and the porch side face -X: for a trailer with side +1 the walk is at -u, so place it as
#              is; for side -1 turn it by pi. Lengths 8..11 in HCTRAIL: scale Y by len/10 (the ends are short, it holds up).
#              Door at Y -1.0 (= -len*.1), windows at Y 0 and +-3 (= k*len*.3) -- the code's own spots.
#   tp_dish, tp_chair, tp_flamingo   yard props on their own centres
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)


# bike_pits.py -- the dirt-bike track's PITS and ANNOUNCER'S TOWER as art, at buildBikeTrack's numbers (the code keeps every
# collider, the ladder, the tracks, tabletops and berms). Blender X = the track frame's u, +Y = its +v. Each root's origin is
# on the ground at the centre the code uses.
#   bk_bike_red / _blue / _yellow  one MX bike, length along Y (front wheel +Y at .62, rear -Y at -.62; tyre .42 outer), bars
#                  at +.55, 1.15 high -- the code's `bike(u, v, g, r, col)` turns it by r exactly as it turns its own boxes
#   bk_canopy_red / _blue / _yellow  a pop-up canopy, legs at +-1.6, roof at 2.6, a valance; origin at its centre
#   bk_trailer     2.4 x 7 x 2.8, long along Y, origin at its centre (the code turns it .1)
#   bk_tower       origin (tu, tv) on g: legs at +-1.2 to 6.0, the deck 3 x 3 at 6, parapets on +Y and +-X (the -Y side open for
#                  the ladder at -1.65), corner posts at +-1.4 up to the roof at 8.3..8.4
#   bk_chest (.7 x .5 x .9), bk_drum (r .28 x .85), bk_generator (1.2 x .8 x .9) -- the pit clutter, each on its centre
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)

# fair_stage.py -- the fairground's STAGE and GRANDSTAND as art, at buildFairground's numbers (the code keeps every collider, the
# stage steps' and rows' boxes, the canvas signs, the ladder up the truss). Blender X = the fair frame's u, +Y = its +v.
#   ff_stage       origin (0, S.v -24) on y. Deck 14 x 8, top 1.4; the field is +Y (the steps at the front corners, u +-6, five
#                  .28 risers); backdrop on the back edge (v -3.8), 6 m over the deck; speaker stacks on the deck at (+-5.8, -1.5)
#                  and on the ground at (+-8.4, 0); podium at (0, +1.5); truss posts at (+-7.3, +-4.3) to 8.0, beams along u at
#                  v +-4.3, catwalk on the back beam (v -4.3, 8.0..8.15, 1.1 deep, railed), five lamp cans along the front beam
#   ff_grandstand  origin (gu 20, -2) on y. Eight rows .9 deep and .34 a riser, rising to +X (the field is -X), 24 long in Y;
#                  back wall at u +4.85 to 6.12; front posts at u -2.6; the roof at 5.92, high at the back
FMET = mat("FF_metal", (.6, .63, .65), .45, .4); PLANK = mat("FF_plank", (.48, .35, .22)); PLANK2 = mat("FF_plank_dark", (.36, .26, .16))
CLOTH = mat("FF_cloth", (.08, .08, .1), .95); CONE = mat("FF_cone", (.2, .2, .22), .6); GOLD = mat("FF_gold", (.85, .62, .2), .4, .5)
def bar(p, q, r, m):
    p, q = Vector(p), Vector(q); d = (q - p).normalized(); a = d.cross(Vector((0, 0, 1))) if abs(d.z) < .95 else d.cross(Vector((1, 0, 0))); a.normalize(); b = d.cross(a)
    vs = [p + (a*sx + b*sy)*r for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]; vs += [v + (q - p) for v in vs]
    fs = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new("bar"); me.from_pydata([tuple(v) for v in vs], [], fs); me.validate(); o = bpy.data.objects.new("bar", me); col.objects.link(o); me.materials.append(m); return put(o)
def ball(c, r, m, seg=8):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg//2), radius=r)
    me = bpy.data.meshes.new("ball"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("ball", me); col.objects.link(o); me.materials.append(m); me.transform(Matrix.Translation(c))
    for p in me.polygons: p.use_smooth = True
    return put(o)
def ring(c, R, r, m, seg=16, side=6, axis='X'):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, segments=seg, radius=R)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); bm.free()
    bm = bmesh.new()
    for i in range(seg):
        for j in range(side):
            pass
    bm.free()
    # a torus built by hand: R about the axle, r the tube
    vs, fs = [], []
    for i in range(seg):
        a = i/seg*2*math.pi
        for j in range(side):
            b = j/side*2*math.pi; rr = R + r*math.cos(b)
            p = Vector((0, rr*math.cos(a), rr*math.sin(a))); p.x = r*math.sin(b)
            vs.append(tuple(p))
    for i in range(seg):
        for j in range(side): fs.append((i*side + j, ((i + 1) % seg)*side + j, ((i + 1) % seg)*side + (j + 1) % side, i*side + (j + 1) % side))
    me = bpy.data.meshes.new("tor"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("tor", me); col.objects.link(o); me.materials.append(m)
    me.transform(Matrix.Translation(c));
    for p in me.polygons: p.use_smooth = True
    return put(o)

CHROME = mat("TP_chrome", (.75, .77, .8), .25, .8); CREAMT = mat("TP_cream", (.88, .84, .72)); TINT = mat("TP_tin", (.68, .71, .73), .4, .55); RUSTT = mat("TP_rust", (.52, .29, .17), .8); REDT = mat("TP_red", (.68, .2, .16), .7)
GLASS = mat("TP_glass", (.12, .16, .2), .15); LAT = mat("TP_lattice", (.86, .83, .76)); PINK = mat("TP_pink", (.95, .45, .62), .5)
# ================= MERLE'S CAMP: the rest of buildBunker as art. Blender X = u, +Y = v, each piece's origin on y at the spot given.
# bk_lookout (-6, -1.5): four poles at +-1.1 to 5.1, X-bracing at 1.4 and 2.8 on the +-Y faces, the deck 2.5 square at 3.85..4, the plank rail
# to 5 (open at +Y where the ladder lands, the code's two .7 runs at +-.8), the telescope on its tripod at (+.3, -.3) aimed up.
# bk_mast (2.8, -6.2): the 9 m pole wrapped in foil, six crumpled foil cones up it from 2 every 1.2, the foil dish at the top turned toward +X,
# three guys to 3.5 m at .3 / 2.39 / 4.48 rad.
# bk_solar (6.15, -1.5): three panels 1.05 x 1.6 at u -1.15 / 0 / +1.15, tilted up toward +Y (front legs 1.0, back 1.6), cells and frames.
# bk_barrels (2.25, -5.7): two blue rain barrels at u -.45 / +.45 with lids and taps, the downpipe from the left one up to (1.1, 2.6, -5.1).
# bk_garden (-5, 5): the 4 x 3 chicken-wire run on stakes (a gate gap at +X's front), three raised beds with their greens.
# bk_firepit (4, 4.5): the stone ring with ash and charred logs, four stump seats at r 1.4. The code's colliders stay for all of them.
WOOD = mat("BC_wood", (.54, .41, .27), .85); WOOD2 = mat("BC_wood_dark", (.4, .3, .19), .9); STEEL = mat("BC_steel", (.54, .59, .63), .4, .6)
FOIL = mat("BC_foil", (.85, .87, .89), .25, .9); DARK = mat("BC_dark", (.12, .13, .15), .6); PANEL = mat("BC_panel", (.12, .16, .29), .25, .4)
CELL = mat("BC_cell", (.85, .87, .9), .3, .5); BLUE = mat("BC_barrel", (.16, .29, .42), .6); WIRE = mat("BC_wire", (.6, .63, .65), .4, .8)
DIRT = mat("BC_dirt", (.4, .32, .21), 1); GREEN = mat("BC_green", (.29, .48, .23), .9); STONE = mat("BC_stone", (.5, .49, .46), .95)
ASH = mat("BC_ash", (.25, .24, .23), 1); CHAR = mat("BC_char", (.08, .07, .06), .9)
WIRE.use_backface_culling = False
import random; rq = random.Random(765)
cur = "bk_lookout"; groups[cur] = []
hw = 1.1
for a in (-1, 1):
    for b in (-1, 1): box(a * hw - .08, b * hw - .08, 0, a * hw + .08, b * hw + .08, 5.1, WOOD, .01)
for z0, z1 in ((.2, 1.4), (1.4, 2.8), (2.8, 3.85)):
    for b in (-1, 1): bar((-hw, b * hw, z0), (hw, b * hw, z1), .04, WOOD2)
    for a in (-1, 1): bar((a * hw, -hw, z0), (a * hw, hw, z1), .04, WOOD2)
box(-1.25, -1.25, 3.85, 1.25, 1.25, 3.99, WOOD, .01)
for k in range(9): box(-1.25 + k * .278 + .005, -1.25, 3.99, -1.25 + k * .278 + .27, 1.25, 4.0, WOOD2 if k % 2 else WOOD, 0)
def rail(x0, y0, x1, y1):
    for z in (4.5, 4.95): box(min(x0, x1) - .04, min(y0, y1) - .04, z, max(x0, x1) + .04, max(y0, y1) + .04, z + .1, WOOD, 0)
rail(-1.2, -1.2, 1.2, -1.2); rail(-1.2, -1.2, -1.2, 1.2); rail(1.2, -1.2, 1.2, 1.2); rail(-1.2, 1.2, -.45, 1.2); rail(.45, 1.2, 1.2, 1.2)
for k in range(3): a = k * 2.09; bar((.3, -.3, 4.9), (.3 + .35 * math.cos(a), -.3 + .35 * math.sin(a), 4.0), .02, DARK)
o = cylz(0, 0, -.55, .55, .11, STEEL, 10); o.data.transform(Matrix.Rotation(.9, 4, 'X')); o.data.transform(Matrix.Rotation(.3, 4, 'Z')); o.data.transform(Matrix.Translation((.3, -.3, 5.15)))
cur = "bk_mast"; groups[cur] = []
cylz(0, 0, 0, 9, .07, FOIL, 8)
for k in range(6):
    r = .22 + rq.random() * .12; z = 2 + k * 1.2
    import bmesh
    o = bpy.data.objects.new("cn", bpy.data.meshes.new("cn")); bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=5, radius1=0, radius2=r, depth=.5)
    for v in bm.verts: v.co += Vector(((rq.random() - .5) * .04, (rq.random() - .5) * .04, (rq.random() - .5) * .04))
    bmesh.ops.translate(bm, vec=(0, 0, z), verts=bm.verts); bm.to_mesh(o.data); bm.free(); col.objects.link(o); o.data.materials.append(FOIL); put(o)
o = bpy.data.objects.new("dish", bpy.data.meshes.new("dish")); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=6, radius=.5)
for v in list(bm.verts):
    if v.co.z > 0: v.co.z = 0
bm.to_mesh(o.data); bm.free(); col.objects.link(o); o.data.materials.append(FOIL); put(o)
o.data.transform(Matrix.Rotation(-math.pi / 2 - .4, 4, 'Y')); o.data.transform(Matrix.Translation((.25, 0, 8.8)))
for k in range(3):
    a = k * 2.09 + .3; bar((0, 0, 6.75), (3.5 * math.cos(a), 3.5 * math.sin(a), .05), .01, DARK); box(3.5 * math.cos(a) - .05, 3.5 * math.sin(a) - .05, 0, 3.5 * math.cos(a) + .05, 3.5 * math.sin(a) + .05, .3, WOOD, 0)
cur = "bk_solar"; groups[cur] = []
for k in (-1, 0, 1):
    x = k * 1.15
    vs = [(x - .525, -.8, 1.0), (x + .525, -.8, 1.0), (x + .525, .8, 1.6), (x - .525, .8, 1.6)]
    o = bpy.data.objects.new("pn", bpy.data.meshes.new("pn")); o.data.from_pydata(vs, [], [(0, 1, 2, 3)]); col.objects.link(o); o.data.materials.append(PANEL); o.modifiers.new("s", 'SOLIDIFY').thickness = .04; put(o)
    for i in range(1, 3):
        xi = x - .525 + i * .35; bar((xi, -.8, 1.005), (xi, .8, 1.605), .004, CELL)
    for j in range(1, 5):
        t = j / 5; bar((x - .525, -.8 + 1.6 * t, 1.0 + .6 * t + .005), (x + .525, -.8 + 1.6 * t, 1.0 + .6 * t + .005), .004, CELL)
    box(x - .03, -.83, 0, x + .03, -.77, 1.0, STEEL, 0); box(x - .03, .77, 0, x + .03, .83, 1.6, STEEL, 0)
bar((-1.7, -.8, .5), (1.7, -.8, .5), .02, STEEL); bar((-1.7, .8, .8), (1.7, .8, .8), .02, STEEL)
cur = "bk_barrels"; groups[cur] = []
for x in (-.45, .45):
    cylz(x, 0, 0, 1.1, .4, BLUE, 14); cylz(x, 0, 1.1, 1.13, .41, BLUE, 14)
    for z in (.35, .75): cylz(x, 0, z, z + .03, .405, DARK, 14)
    o = cylz(0, 0, -.05, .05, .03, STEEL, 6); o.data.transform(Matrix.Rotation(math.pi / 2, 4, 'X')); o.data.transform(Matrix.Translation((x, -.42, .2)))
bar((-.45, 0, 1.1), (-1.15, .6, 2.6), .03, DARK)
cur = "bk_garden"; groups[cur] = []
gw, gd = 4, 3
def wire(x0, y0, x1, y1):
    L = math.hypot(x1 - x0, y1 - y0); n = max(2, int(L / .15)); vs, fs = [], []
    for i in range(n):
        for j in range(6):
            t0, t1 = i / n, (i + 1) / n; z0, z1 = j / 6, (j + 1) / 6
            A = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0); B = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
            for (P, za, Q, zb) in ((A, z0, B, z1), (A, z1, B, z0)):
                c = len(vs); vs.extend([(P[0], P[1], za - .004), (Q[0], Q[1], zb - .004), (Q[0], Q[1], zb + .004), (P[0], P[1], za + .004)]); fs.append((c, c + 1, c + 2, c + 3))
    me = bpy.data.meshes.new("w"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("w", me); col.objects.link(o); me.materials.append(WIRE); put(o)
wire(-2, -1.5, 2, -1.5); wire(-2, 1.5, 2, 1.5); wire(-2, -1.5, -2, 1.5); wire(2, -1, 2, 1.5)
for (x, yv) in ((-2, -1.5), (2, -1.5), (-2, 1.5), (2, 1.5), (0, -1.5), (0, 1.5), (2, -1), (-2, 0)): box(x - .03, yv - .03, 0, x + .03, yv + .03, 1.05, WOOD, 0)
for k in range(3):
    yv = -1 + k; box(-1.7, yv - .25, 0, 1.7, yv + .25, .12, WOOD2, 0); box(-1.65, yv - .22, .12, 1.65, yv + .22, .14, DIRT, 0)
    for j in range(6):
        r = .16 + rq.random() * .08; ball((-1.6 + j * .62, yv, .14 + r * .7), r, GREEN, 6)
cur = "bk_firepit"; groups[cur] = []
for k in range(12):
    a = k * math.pi / 6; box(.55 * math.cos(a) - .1, .55 * math.sin(a) - .1, 0, .55 * math.cos(a) + .1, .55 * math.sin(a) + .1, .2, STONE, .04)
cylz(0, 0, 0, .04, .45, ASH, 12)
for a in (0, 1.2, 2.6): bar((.3 * math.cos(a), .3 * math.sin(a), .08), (-.2 * math.cos(a), -.2 * math.sin(a), .12), .05, CHAR)
for k in range(4):
    a = k * 1.57 + .4; cylz(1.4 * math.cos(a), 1.4 * math.sin(a), 0, .45, .23, WOOD, 10); cylz(1.4 * math.cos(a), 1.4 * math.sin(a), .45, .46, .21, WOOD2, 10)
# ======== join each group under its root, export, preview
roots = {}
for name, Lg in groups.items():
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in Lg: o.select_set(True)
    bpy.context.view_layer.objects.active = Lg[0]; bpy.ops.object.join(); j = bpy.context.view_layer.objects.active; j.name = name + "_mesh"
    r = bpy.data.objects.new(name, None); col.objects.link(r); j.parent = r; roots[name] = r
    print(name, len(j.data.polygons), "faces", len(j.data.materials), "materials", tuple(round(d, 2) for d in j.dimensions))
for o in bpy.context.view_layer.objects: o.select_set(False)
for r in roots.values(): r.select_set(True); [c.select_set(True) for c in r.children]
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/bunker_camp.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
lay = {"bk_lookout": (-6, -1.5), "bk_mast": (2.8, -6.2), "bk_solar": (6.15, -1.5), "bk_barrels": (2.25, -5.7), "bk_garden": (-5, 5), "bk_firepit": (4, 4.5)}
for k, (x, yv) in lay.items(): roots[k].location = (x, yv, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (2, 18, 9); cam.rotation_euler = (Vector((0, 0, 2)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/bunker_camp.png"; bpy.ops.render.render(write_still=True)
