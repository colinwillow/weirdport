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

# ======== town_trailer: the town edge's trailer park (buildTownEdge's TRAILERS), at the code's numbers. Blender X = the town
# frame's u ALONG the trailer, +Y = its +v SIDE (windows, door, deck). Origin on the ground g at the trailer's centre.
#   tv_trailer  footing skirt 11 x 2.8 up to .55, the body 12 x 3.4 from .55 to 3.15, the stripe 1.55-1.85, three lit windows on +Y
#               at x -3.5, 0, 3.5 (1.95-2.65), the door at x 2, the deck 3 x 1.8 at (2, 2.6) top .6 with its steps and awning,
#               the dish on its pole at (-4.5, 0) centre 3.55, the hitch and two propane bottles at -X
#   tv_chair    one lawn chair, origin on the ground, facing +Y (the code puts two at side 3.9, x 1.2 and 2.4, turned r + .4)
TRL = mat("TV_trailer", (.91, .89, .85), .55, .1); TRL2 = mat("TV_trailer_rib", (.84, .82, .78), .55, .1); STR = mat("TV_stripe", (.29, .48, .69), .55)
GLOW = mat("TV_glow", (.25, .18, .1), .5); _g = GLOW.node_tree.nodes["Principled BSDF"]; _g.inputs["Emission Color"].default_value = (1, .77, .42, 1); _g.inputs["Emission Strength"].default_value = 1.6
SKIRT = mat("TV_skirt", (.62, .6, .55), .95); BLOCK = mat("TV_block", (.55, .54, .5), 1); DOOR = mat("TV_door", (.75, .73, .68), .6)
DECK = mat("TV_deck", (.5, .37, .24)); DECK2 = mat("TV_deck_dark", (.4, .29, .19)); AL = mat("TV_alu", (.78, .8, .82), .35, .7)
TANK = mat("TV_propane", (.92, .92, .9), .4, .2); DISH = mat("TV_dish", (.86, .86, .84), .5, .2); BLK = mat("TV_black", (.08, .08, .09), .7)
WEB1 = mat("TV_web_blue", (.29, .48, .69), .8); WEB2 = mat("TV_web_white", (.93, .92, .88), .8); GL = mat("TV_glass", (.12, .16, .2), .15)

cur = "tv_trailer"; groups[cur] = []
Y0, Y1 = .55, 3.15
# the skirt: lattice panels between block piers, set in from the body like the code's 11 x 2.8 footing
box(-5.5, -1.4, 0, 5.5, 1.4, Y0, SKIRT)
for x in [-5.2, -2.6, 0, 2.6, 5.2]:
    for s in (-1, 1): box(x - .2, s*1.4 - .2, 0, x + .2, s*1.4 + .2, Y0 - .02, BLOCK)
for k in range(22):
    x = -5.3 + k*.505
    for s in (-1, 1): box(x - .03, s*1.41 - .015, .05, x + .03, s*1.41 + .015, Y0 - .06, TRL)
# the body, ends rounded by the bevel, then ribs on both long faces
box(-6, -1.7, Y0, 6, 1.7, Y1, TRL, bev=.12)
for k in range(46):
    x = -5.75 + k*.25
    if any(abs(x - w) < .68 for w in (-3.5, 0, 3.5)) and k % 1 == 0: rib_skip_win = True
    for s in (-1, 1):
        if s > 0 and abs(x - 2) < .5: continue          # the door
        box(x - .035, s*1.7 - .02*(s < 0) - 0.0, Y0 + .1, x + .035, s*1.7 + .02*(s > 0), Y0 + .95, TRL2) if s > 0 else box(x - .035, -1.72, Y0 + .1, x + .035, -1.7, Y0 + .95, TRL2)
        if not (s > 0 and any(abs(x - w) < .68 for w in (-3.5, 0, 3.5))):
            box(x - .035, (1.7 if s > 0 else -1.72), Y0 + 1.35, x + .035, (1.72 if s > 0 else -1.7), Y1 - .18, TRL2)
# the stripe, a hair proud of the ribs, round the whole body
box(-6.03, -1.74, Y0 + 1.0, 6.03, 1.74, Y0 + 1.3, STR)
# a crowned roof cap
quadbox([(-5.9, -1.5, Y1), (5.9, -1.5, Y1), (5.9, 1.5, Y1), (-5.9, 1.5, Y1)], .06, TRL2)
# three lit windows on +Y at the code's spots, alu frames; two dark ones on -Y and one each end
for x in (-3.5, 0, 3.5):
    box(x - .66, 1.7, Y0 + 1.33, x + .66, 1.76, Y0 + 2.17, AL)
    box(x - .6, 1.755, Y0 + 1.4, x + .6, 1.775, Y0 + 2.1, GLOW)
    box(x - .02, 1.76, Y0 + 1.4, x + .02, 1.79, Y0 + 2.1, AL)
for x in (-2.5, 2.5):
    box(x - .56, -1.76, Y0 + 1.4, x + .56, -1.7, Y0 + 2.1, AL); box(x - .5, -1.775, Y0 + 1.46, x + .5, -1.755, Y0 + 2.04, GL)
for s in (-1, 1):
    box(s*6 - .03, -.5, Y0 + 1.45, s*6 + .03, .5, Y0 + 2.05, AL); box(s*6.01 - .015 if s > 0 else -6.025, -.44, Y0 + 1.51, s*6.025 if s > 0 else -6.01, .44, Y0 + 1.99, GL)
# the door at x 2, with its little window and a handle
box(1.6, 1.7, Y0 + .05, 2.4, 1.75, Y0 + 2.05, DOOR); box(1.85, 1.745, Y0 + 1.3, 2.15, 1.765, Y0 + 1.8, GL); box(2.27, 1.75, Y0 + .95, 2.33, 1.8, Y0 + 1.05, AL)
# the deck: 3 x 1.8 at (2, 2.6), top .6 -- planks on joists on posts, two steps off its -X end
for k in range(8):
    y = 1.75 + k*.225
    box(.5, y + .01, .52, 3.5, y + .215, .6, DECK if k % 2 else DECK2)
for x in (.55, 2, 3.45):
    for y in (1.8, 3.45): box(x - .06, y - .06, 0, x + .06, y + .06, .52, DECK2)
box(.5, 1.75, .38, 3.5, 1.85, .52, DECK2); box(.5, 3.4, .38, 3.5, 3.5, .52, DECK2)
box(-.1, 2.1, .32, .5, 3.2, .4, DECK); box(-.4, 2.1, .14, -.1, 3.2, .22, DECK)
for y in (2.15, 3.15): box(-.4, y - .05, 0, .5, y + .05, .32, DECK2)
# the rail on the deck's +X end and +Y edge (open where the chairs look out)
for (x, y) in ((3.45, 1.8), (3.45, 3.45), (2.5, 3.45)): box(x - .04, y - .04, .6, x + .04, y + .04, 1.5, DECK2)
box(3.41, 1.8, 1.42, 3.49, 3.45, 1.5, DECK); box(2.5, 3.41, 1.42, 3.49, 3.49, 1.5, DECK)
# the alu awning over the door, out over the deck on two poles
quadbox([(.7, 1.72, Y1 - .3), (3.3, 1.72, Y1 - .3), (3.3, 3.3, Y1 - .55), (.7, 3.3, Y1 - .55)], .04, AL)
for x in (.75, 3.25): cylz(x, 3.25, .6, Y1 - .55, .03, AL, 8)
# the dish on its pole at (-4.5, 0): pole from the roof to 3.55, the dish tilted .9 about Y, its feed arm
cylz(-4.5, 0, Y1, Y1 + .42, .03, AL, 8)
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=.45, radius2=.36, depth=.06)
me = bpy.data.meshes.new("dish"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("dish", me); col.objects.link(o); me.materials.append(DISH)
me.transform(Matrix.Translation((-4.5, 0, Y0 + 3.0)) @ Matrix.Rotation(.9, 4, 'Y')); put(o)
nrm = Matrix.Rotation(.9, 4, 'Y') @ Vector((0, 0, 1)); c = Vector((-4.5, 0, Y0 + 3.0))
bar(c + nrm*.04, c + nrm*.5, .012, AL); ball(c + nrm*.52, .05, BLK, 8)
# the hitch: an A-frame to a coupler, a jack, two propane bottles on the tongue
bar((-6, -.8, .45), (-7.3, 0, .45), .05, BLK); bar((-6, .8, .45), (-7.3, 0, .45), .05, BLK); box(-7.5, -.08, .38, -7.25, .08, .52, BLK)
cylz(-6.9, 0, 0, .45, .04, AL, 8); box(-7.0, -.1, 0, -6.8, .1, .03, BLK)
for y in (-.35, .35): cylz(-6.45, y, .5, 1.15, .17, TANK, 12); cylz(-6.45, y, 1.15, 1.25, .06, AL, 8)
# porch light by the door
box(1.38, 1.72, Y0 + 2.0, 1.5, 1.82, Y0 + 2.2, GLOW)

cur = "tv_chair"; groups[cur] = []
for x in (-.25, .25):
    bar((x, -.3, 0), (x, .25, .42), .015, AL); bar((x, .25, 0), (x, -.2, .42), .015, AL)
    bar((x, -.2, .42), (x, -.32, .92), .015, AL); bar((x, -.25, .62), (x, .2, .62), .015, AL)
bar((-.25, .2, .42), (.25, .2, .42), .015, AL); bar((-.25, -.32, .92), (.25, -.32, .92), .015, AL)
for k in range(5):
    y = -.18 + k*.09; box(-.24, y, .41, .24, y + .06, .43, WEB1 if k % 2 == 0 else WEB2)
for k in range(5):
    t = (k + .5)/5.5; z = .44 + t*.46; y = -.2 - t*.12; box(-.24, y - .012, z - .035, .24, y + .012, z + .035, WEB2 if k % 2 == 0 else WEB1)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/town_trailer.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["tv_trailer"].location = (0, 0, 0); roots["tv_chair"].location = (1.6, 4.2, 0); roots["tv_chair"].rotation_euler = (0, 0, .4)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.32, .32, .33), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-60))
cd = bpy.data.cameras.new("C"); cd.lens = 28; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (9, 14, 5); cam.rotation_euler = (Vector((0, 1, 1.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/town_trailer.png"; bpy.ops.render.render(write_still=True)
