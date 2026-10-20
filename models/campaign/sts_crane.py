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




# sts_crane.py -- the Waterfront's ship-to-shore crane as art, at wfCranes' numbers (the code keeps every collider, both ladders,
# the landing, the crate stair and the moving trolley / spreader / box). Blender X = the frame's u, +Y = its v, origin at the
# crane's (u, 0) on the quay top Y. T = 30 (the portal), B = 34 (the boom's top).
#   wf_sts_crane   legs at X +-8, Y 6 and 24, .9 square, Y..T, on sills with wheel bogies; portal beams at T-2..T; X-braced sides;
#                  the boom: two box-truss girders at X +-3.2 from Y -44 to +44, B-2..B; catwalks at X +-4.25 (B-.2..B) from -44 to
#                  30 with rails at +-5.05; the A-frame to the apex (0, B+14, 15) with its stays to -40, -12 and 42; the machine
#                  house at Y 37.5 (8.2 x 13, B..B+4); the landing at T-13 (Y+17) on the +X land leg.
FMET = mat("FF_metal", (.6, .63, .65), .45, .4)



# mill_kit.py -- the Hollow Creek mill's machines as art, at buildMill's numbers (the code keeps the shed, the flume, the belts,
# the log piles, the ladders and every collider). Blender X = the mill frame's u, +Y = its +v; origins on the ground (y).
#   hm_burner      the teepee burner at (B.u 21, B.v -11): r 4 at the foot, .3 r at the top, 9 high, a mesh dome, a door, the
#                  conveyor's inlet on the -X side at 7; the smoke still leaves at y+9.3 (O.fireAt)
#   hm_crane       the log crane at (C.u -18, C.v 3): legs at +-1 to 8, the platform 2.8 sq, the cab at (-.6, -.6), the boom toward
#                  (+8, +5) from 10.4; the ladder stays the code's (on the -Y side at -1.35)
#   hm_logtruck    at (-21, 6): bed 2.4 x 9 at .5..1.3, the cab toward -Y (at -3.6), stakes and bunks; the five logs stay code
#   hm_watertower  at (9, v0-4): legs at +-1.2 to 7, a staved wooden tank r 2 from 7 to 10.4, a cone roof to 11.6
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

def truss(p, q, w=.35, m=None):
    """a box truss from p to q: four chords and zigzag lacing on its four faces (built from points)"""
    p, q = Vector(p), Vector(q); d = (q - p); L = d.length; n = d.normalized()
    a = n.cross(Vector((0, 0, 1))) if abs(n.z) < .95 else n.cross(Vector((1, 0, 0))); a.normalize(); b = n.cross(a)
    C = [(a*sx + b*sy)*w/2 for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for c in C: bar(p + c, q + c, .035, m)
    k = max(2, int(L/w))
    for i in range(k):
        t0, t1 = i/k, (i + 1)/k
        for j in range(4):
            c0, c1 = C[j], C[(j + 1) % 4]
            bar(p + d*t0 + (c0 if i % 2 else c1), p + d*t1 + (c1 if i % 2 else c0), .018, m)

YEL2 = mat("WF_crane", (.92, .66, .12), .5, .2); WHT = mat("WF_white", (.9, .9, .87), .6); GRATE = mat("WF_grate", (.32, .35, .38), .55, .5)
STRIPE = mat("WF_stripe", (.08, .08, .09), .6); RED = mat("WF_redglow", (.6, .05, .05), .4); _b = RED.node_tree.nodes["Principled BSDF"]; _b.inputs["Emission Color"].default_value = (1, .15, .1, 1); _b.inputs["Emission Strength"].default_value = 3
WIN = mat("WF_window", (.1, .14, .18), .15)
T, B = 30., 34.
cur = "wf_sts_crane"; groups[cur] = []
# ---- legs, sills and bogies
for s in (-1, 1):
    for v in (6, 24):
        box(s*8 - .45, v - .45, 1.2, s*8 + .45, v + .45, T - 2, YEL2)
        box(s*8 - .8, v - 1.6, 0, s*8 + .8, v + 1.6, 1.2, YEL2)
        for k in range(6): box(s*8 - .82, v - 1.6 + k*.55, .2, s*8 + .82, v - 1.6 + k*.55 + .27, 1.0, STRIPE)   # hazard stripes on the sill
        for w in (-1.1, -.4, .4, 1.1): ring((s*8, v + w, .0 + .28), .22, .07, DARK, 12, 5)
        box(s*8 - .5, v - .5, T - 2.6, s*8 + .5, v + .5, T - 2, YEL2)                     # a knee at the top
# ---- the portal: beams along Y on each side, along X at both legs, and the sill beam low across the land legs
for s in (-1, 1): box(s*8 - .45, 6 - .45, T - 2, s*8 + .45, 24 + .45, T, YEL2)
for v in (6, 24): box(-8.45, v - .45, T - 2, 8.45, v + .45, T, YEL2)
box(-8, 23.6, 6.0, 8, 24.4, 6.8, YEL2)                                                  # a low tie across the land side, over head height
for s in (-1, 1):                                                                       # the side X-braces, as box members
    bar((s*8, 6.4, 4), (s*8, 23.6, T - 2), .14, YEL2); bar((s*8, 23.6, 4), (s*8, 6.4, T - 2), .14, YEL2)
# ---- the boom: two box-truss girders, then a deck of grating between them under the trolley's way
for s in (-1, 1):
    x = s*3.2
    box(x - .25, -44, B - .45, x + .25, 44, B, YEL2)                                     # top chord
    box(x - .25, -44, B - 2, x + .25, 44, B - 1.55, YEL2)                                # bottom chord
    for k in range(44):
        y0, y1 = -44 + k*2, -44 + (k + 1)*2
        bar((x, y0, B - 1.6), (x, y1, B - .45), .07, YEL2) if k % 2 == 0 else bar((x, y0, B - .45), (x, y1, B - 1.6), .07, YEL2)
        box(x - .06, y0 - .06, B - 1.55, x + .06, y0 + .06, B - .45, YEL2)
    for (y0, y1) in ((-44, 30),):
        box(s*4.25 - .8, y0, B - .2, s*4.25 + .8, y1, B, GRATE)                          # catwalk
        for k in range(int((y1 - y0)/.25)): box(s*4.25 - .8, y0 + k*.25, B, s*4.25 + .8, y0 + k*.25 + .03, B + .005, DARK)
    rails = [(-44, 22.8), (25.2, 30)] if s > 0 else [(-44, 30)]
    for (y0, y1) in rails:
        for z in (B + .5, B + 1.0): box(s*5.05 - .03, y0, z, s*5.05 + .03, y1, z + .06, YEL2)
        for k in range(int((y1 - y0)/2) + 1): yy = min(y1, y0 + k*2); box(s*5.05 - .03, yy - .03, B, s*5.05 + .03, yy + .03, B + 1.06, YEL2)
    for k in range(9): yy = -40 + k*10; box(s*4.4 - .1, yy - .1, B - .45 - .5, s*4.4 + .1, yy + .1, B - .45, YEL2)   # catwalk hangers
for k in range(23): yy = -44 + k*4; box(-3.2, yy - .1, B - 2, 3.2, yy + .1, B - 1.8, YEL2)    # cross ties between the girders, under
box(-3.45, -44.1, B - 2, 3.45, -43.7, B, YEL2)                                          # the nose
for z in (B + .5, B + 1.0): box(-4.25 - .8, -44.03, z, 4.25 + .8, -43.97, z + .06, YEL2)
for v in (6, 24): box(-3.45, v - .25, T, 3.45, v + .25, T + 1, YEL2)                   # under the trolley's way
for s in (-1, 1):
    for v in (6, 24): box(s*3.2 - .25, v - .25, T, s*3.2 + .25, v + .25, B - 2, YEL2)
# ---- the A-frame and its stays
apex = Vector((0, 15, B + 14))
for s in (-1, 1):
    for v in (13, 17): truss((s*3.2, v, B), apex, .45, YEL2)
    for vv in (-40, -12, 42): bar(apex + Vector((s*.2, 0, 0)), (s*3.2, vv, B), .06, FMET)
box(-.6, 14.4, B + 13.6, .6, 15.6, B + 14.4, YEL2)
ball((0, 15, B + 14.7), .3, RED, 8)
# ---- the machine house (its roof is the code's floor), windows, a door, vents, the red light; a blank board for the logo
box(-4.1, 31, B, 4.1, 44, B + 4, WHT)
box(-4.3, 30.8, B + 4, 4.3, 44.2, B + 4.2, DARK)
for s in (-1, 1):
    for k in range(5): box(s*4.1 - .02*s - (.03 if s < 0 else 0), 32.2 + k*2.4, B + 2, s*4.1 + (.03 if s > 0 else 0), 33.6 + k*2.4, B + 3.1, WIN)
    for k in range(4): box(s*4.1 - .05, 33 + k*2.4, B + .4, s*4.1 + .05, 34 + k*2.4, B + 1.2, GRATE)   # vents
box(-.6, 30.95, B + .5, .6, 31.0, B + 2.8, DARK)
box(-3.5, 30.9, B + 3.1, 3.5, 30.95, B + 3.8, mat("WF_board", (.95, .95, .92), .6))
ball((0, 43.5, B + 4.5), .25, RED, 8)
for s in (-1, 1): box(s*3 - .15, 42, B + 4.2, s*3 + .15, 43, B + 4.8, GRATE)            # roof plant
# ---- the cab under the boom (the driver's, fixed at the landward end of the trolley's run) and floodlights
box(-1.2, 26, B - 3.6, 1.2, 28.4, B - 2, WHT); box(-1.22, 26.2, B - 3.3, 1.22, 28.2, B - 2.4, WIN)
for vv in (-30, -10, 10):
    for s in (-1, 1): box(s*3.5 - .2, vv - .2, B - 2.4, s*3.5 + .2, vv + .2, B - 2.1, DARK); ball((s*3.5, vv, B - 2.5), .12, mat("WF_flood", (1, .95, .8), .3) if "WF_flood" not in bpy.data.materials else bpy.data.materials["WF_flood"])
# ---- the landing at Y+17 on the +X land leg (the code's floor and rails; ladders are the code's)
L1 = 17.
box(7.9 - 2.3, 24 - 1.2, L1 - .25, 7.9 + 2.3, 24 + 1.2, L1, GRATE)
for (a0, a1, b0, b1) in ((10.17, 10.23, 22.8, 25.2), (5.6, 10.2, 22.77, 22.83), (5.6, 10.2, 25.17, 25.23)):
    for z in (L1 + .5, L1 + .98): box(a0, b0, z, a1, b1, z + .06, YEL2)
for k in range(3): box(10.17, 22.8 + k*1.2 - .03, L1, 10.23, 22.8 + k*1.2 + .03, L1 + 1.05, YEL2)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/sts_crane.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-120, -80, -.01), (120, -80, -.01), (120, 160, -.01), (-120, 160, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.56, .55, .52), 1))
wa = bpy.data.meshes.new("wa"); wa.from_pydata([(-120, -80, -.5), (120, -80, -.5), (120, 0, -.5), (-120, 0, -.5)], [], [(0, 1, 2, 3)]); wo = bpy.data.objects.new("wa", wa); col.objects.link(wo); wa.materials.append(mat("Wt", (.2, .35, .45), .2)); go.location.y = 0
g.vertices[0].co.y = 0; g.vertices[1].co.y = 0
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.2; sun.color = (1, .92, .8); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-40))
cd = bpy.data.cameras.new("C"); cd.lens = 20; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-45, 55, 12); cam.rotation_euler = (Vector((0, 5, 24)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/sts_crane.png"; bpy.ops.render.render(write_still=True)
