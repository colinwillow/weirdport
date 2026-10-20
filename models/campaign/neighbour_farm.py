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

# neighbour_farm.py -- the neighbour's farm on the ridge as art, at buildNeighbours' exact numbers (the code keeps every collider,
# the picket fence and the shop's painted sign). CONTRACT: one root each, Blender X = the frame's u, Blender +Y = the frame's +v,
#   nf_house   origin (hu, hv) at the house floor y0 (plinth to -1.6). 6 x 5.5, eaves 8.6, ridge 12.8 along X, walls .22, roof
#              .45 overhang; windows at floors .9 / 3.7 / 6.5 and u +-1.5, front (-Y) and back; door front; stoop; chimney at
#              (W2-.8, +.6) through the +Y slope to RID+1.2
#   nf_shed    the cattle shed: origin (su, sv) at y0 = lo. L 22 x D 7, open on -Y with 7 posts, front 2.9 / back 3.4, pent roof
#   nf_tower   the water tower: origin (tu, tv) at g. Legs at +-1.3 to 12, tank r 2.0 x 3.4 on top, cone cap, ladder at (+1.3, -1.55)
#   nf_shop    the farm shop: origin (pu, pv) at g. Shack 4 x 2 (back wall at +.9), roof at 2.55 over g+.15, counter at -.9,
#              the awning and three produce crates; the SIGN stays the code's canvas plane (FARM SHOP / EGGS HONEY APPLES)
BLUE = mat("NF_blue", (.5, .6, .7)); BLUE2 = mat("NF_blue_lap", (.42, .51, .6)); SLATE = mat("NF_slate", (.22, .24, .28)); SLATE2 = mat("NF_slate2", (.3, .32, .36))
GLOW = mat("NF_glow", (.12, .1, .07), .2); _b = GLOW.node_tree.nodes["Principled BSDF"]; _b.inputs["Emission Color"].default_value = (1, .77, .42, 1); _b.inputs["Emission Strength"].default_value = .7
WHITE = mat("NF_white", (.93, .92, .88)); TANK = mat("NF_tank", (.6, .25, .18), .6, .3); APPLE = mat("NF_apple", (.72, .1, .1), .5); PUMP = mat("NF_pumpkin", (.9, .45, .12), .6)
GREENS = mat("NF_greens", (.3, .52, .16)); BARN = mat("NF_barnwood", (.46, .38, .29))
def slabXY(p0, p1, p2, p3, th, m): return quadbox([p0, p1, p2, p3], th, m)
# ======== the tall house
cur = "nf_house"; groups[cur] = []
W2, D2, E, RID, T = 3., 2.75, 8.6, 12.8, .22
box(-W2 - .15, -D2 - .15, -1.6, W2 + .15, D2 + .15, -.05, STONE); box(-W2 - .2, -D2 - .2, -.2, W2 + .2, D2 + .2, 0, WHITE)
box(-W2, -D2 - T/2, 0, W2, -D2 + T/2, E, BLUE); box(-W2, D2 - T/2, 0, W2, D2 + T/2, E, BLUE)
box(-W2 - T/2, -D2, 0, -W2 + T/2, D2, E, BLUE); box(W2 - T/2, -D2, 0, W2 + T/2, D2, E, BLUE)
WN = [(s, du, fl) for s in (-1, 1) for du in (-1.5, 1.5) for fl in (.9, 3.7, 6.5)]
for s in (-1, 1):                                              # laps every .28 on the long faces, cut round the windows and the door
    for k in range(int(E/.28)):
        z = .15 + k*.28; x = -W2
        cuts = sorted([(du - .65, du + .65) for (ss, du, fl) in WN if ss == s and fl - .15 < z < fl + 1.45] + ([(-.75, .75)] if s < 0 and z < 2.3 else []))
        for (c0, c1) in cuts + [(W2, W2)]:
            if c0 > x + .05: box(x, s*(D2 + T/2), z, c0, s*(D2 + T/2) + s*.03, z + .05, BLUE2)
            x = max(x, c1)
    for k in range(int(E/.28)):
        z = .15 + k*.28; box(s*(W2 + T/2), -D2, z, s*(W2 + T/2) + s*.03, D2, z + .05, BLUE2)
for s in (-1, 1):                                              # gables at +-X, laps up them, a round attic window in each
    x0, x1 = s*W2 - T/2, s*W2 + T/2
    vs = [(x0, -D2 - .1, E), (x0, D2 + .1, E), (x0, 0, RID), (x1, -D2 - .1, E), (x1, D2 + .1, E), (x1, 0, RID)]
    me = bpy.data.meshes.new("g"); me.from_pydata(vs, [], [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]); me.validate()
    o = bpy.data.objects.new("g", me); col.objects.link(o); me.materials.append(BLUE); put(o)
    for k in range(int((RID - E)/.28)):
        z = E + .1 + k*.28; hw = (D2 + .1)*(1 - (z - E)/(RID - E)) - .05
        if hw > .2: box(s*(W2 + T/2), -hw, z, s*(W2 + T/2) + s*.03, hw, z + .05, BLUE2)
    box(s*(W2 + T/2) - .05, -.4, E + 1.4, s*(W2 + T/2) + .05, .4, E + 2.2, GLOW); box(s*(W2 + T/2 + .04) - .04, -.5, E + 1.3, s*(W2 + T/2 + .04) + .04, .5, E + 1.4, WHITE)
for a in (-1, 1):
    for b in (-1, 1): box(a*(W2 + .02) - .12, b*(D2 + .02) - .12, 0, a*(W2 + .02) + .12, b*(D2 + .02) + .12, E + .05, WHITE)
for s in (-1, 1):
    for fl in (2.95, 5.75): box(-W2 - .05, s*(D2 + .02) - T/2 - .03, fl, W2 + .05, s*(D2 + .02) + T/2 + .03, fl + .14, WHITE)
    box(-W2 - .05, s*(D2 + .02) - T/2 - .04, E - .35, W2 + .05, s*(D2 + .02) + T/2 + .04, E - .05, WHITE)
for (s, du, fl) in WN:                                          # tall windows: pane, mullions, sill, head with a little pediment
    y = s*(D2 + T/2)
    box(du - .4, y - .02, fl, du + .4, y + .02, fl + 1.3, GLOW)
    box(du - .03, y + s*.02 - .02, fl, du + .03, y + s*.02 + .02, fl + 1.3, WHITE); box(du - .4, y + s*.02 - .02, fl + .62, du + .4, y + s*.02 + .02, fl + .68, WHITE)
    for x in (du - .48, du + .4): box(x, y, fl, x + .08, y + s*.06, fl + 1.3, WHITE)
    box(du - .55, y, fl - .12, du + .55, y + s*.12, fl, WHITE); box(du - .52, y, fl + 1.3, du + .52, y + s*.1, fl + 1.44, WHITE)
    vs = [(du - .55, y, fl + 1.44), (du + .55, y, fl + 1.44), (du, y, fl + 1.7), (du - .55, y + s*.1, fl + 1.44), (du + .55, y + s*.1, fl + 1.44), (du, y + s*.1, fl + 1.7)]
    me = bpy.data.meshes.new("ped"); me.from_pydata(vs, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate()
    o = bpy.data.objects.new("ped", me); col.objects.link(o); me.materials.append(WHITE); put(o)
y = -D2 - T/2
box(-.5, y - .06, 0, .5, y - .02, 2.1, mat("NF_door", (.85, .7, .2), .6)); box(-.65, y - .1, 0, -.5, y, 2.4, WHITE); box(.5, y - .1, 0, .65, y, 2.4, WHITE); box(-.7, y - .12, 2.1, .7, y, 2.4, WHITE)
box(-.8, -D2 - 1.6, -1.2, .8, -D2 - .2, 0, STONE, bev=.03)       # the stoop the code collides as 1.6 x 1.4 at v -D2-.9
quadbox([(-.85, -D2 - .1, 2.65), (.85, -D2 - .1, 2.65), (.85, -D2 - 1.3, 2.4), (-.85, -D2 - 1.3, 2.4)], .06, SLATE)   # a little hood over it
for x in (-.75, .75): box(x - .025, -D2 - 1.27, 2.15, x + .025, -D2 - 1.23, 2.4, WHITE)
run = D2 + .45; ang = math.atan2(RID - E, D2); ca, sa = math.cos(ang), math.sin(ang); sl = run/ca
for s in (-1, 1):                                               # steep slate roof, courses from points; scalloped look by alternating thickness
    n = int(sl/.35)
    for k in range(n + 1):
        d0 = k*sl/(n + 1); d1 = (k + 1)*sl/(n + 1) + .05
        p0 = (s*d0*ca, RID + .06 - d0*sa); p1 = (s*d1*ca, RID + .06 - d1*sa); m = SLATE2 if k % 4 == 1 else SLATE
        pts = [(-W2 - .45, p0[0], p0[1]), (W2 + .45, p0[0], p0[1]), (W2 + .45, p1[0], p1[1]), (-W2 - .45, p1[0], p1[1])]
        if s < 0: pts = [pts[1], pts[0], pts[3], pts[2]]
        quadbox(pts, .1 + .04*(k % 2), m)
    ey = s*run; ez = RID + .06 - sl*sa
    box(-W2 - .45, ey - .08 if s > 0 else ey - .02, ez - .3, W2 + .45, ey + .02 if s > 0 else ey + .08, ez, WHITE)
box(-W2 - .5, -.15, RID + .05, W2 + .5, .15, RID + .3, SLATE2)
for s in (-1, 1):
    for sd in (-1, 1):
        vs = []
        for x in (s*(W2 + .4) - .07, s*(W2 + .4) + .07): vs += [(x, 0, RID + .3), (x, sd*run, RID + .06 - sl*sa + .16), (x, sd*run, RID + .06 - sl*sa - .12), (x, 0, RID)]
        fs = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        if sd < 0: fs = [tuple(reversed(q)) for q in fs]
        me = bpy.data.meshes.new("rk"); me.from_pydata(vs, [], fs); me.validate(); o = bpy.data.objects.new("rk", me); col.objects.link(o); me.materials.append(WHITE); put(o)
box(W2 - .8 - .4, .6 - .4, RID - 1.6, W2 - .8 + .4, .6 + .4, RID + 1.2, STONE); box(W2 - .8 - .5, .6 - .5, RID + 1.2, W2 - .8 + .5, .6 + .5, RID + 1.35, STONE, bev=.03)
cylz(W2 - .8, .6, RID + 1.35, RID + 1.75, .14, mat("NF_pot", (.55, .3, .22)))
box(W2 + .25, D2 - .3, 0, W2 + .35, D2 - .2, E - .2, METAL := mat("NF_metal", (.6, .63, .65), .45, .4))
# ======== the cattle shed: plank walls with battens, round-pole posts on the open front, a tin pent roof, troughs, straw
cur = "nf_shed"; groups[cur] = []
L, D, hf, hb = 22., 7., 2.9, 3.4
box(-L/2, D/2 - .15, -.3, L/2, D/2 + .15, hb, BARN)
for s in (-1, 1):
    x0, x1 = s*L/2 - .15, s*L/2 + .15
    vs = [(x0, -D/2, -.3), (x0, D/2, -.3), (x0, D/2, hb), (x0, -D/2, hf), (x1, -D/2, -.3), (x1, D/2, -.3), (x1, D/2, hb), (x1, -D/2, hf)]
    me = bpy.data.meshes.new("sw"); me.from_pydata(vs, [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
    o = bpy.data.objects.new("sw", me); col.objects.link(o); me.materials.append(BARN); put(o)
for x in [-L/2 + .5 + i*.7 for i in range(31)]: box(x - .04, D/2 + .15, 0, x + .04, D/2 + .19, hb - .1, WOOD)
for k in range(7): cylz(-L/2 + k*L/6, -D/2, -.3, hf, .13, WOOD, 8)
box(-L/2 - .2, -D/2 - .12, hf - .25, L/2 + .2, -D/2 + .12, hf, WOOD)
pt = math.atan2(hb - hf, D)
for k in range(14):
    x0 = -L/2 - .4 + k*(L + .8)/14; x1 = x0 + (L + .8)/14 + .02
    quadbox([(x0, -D/2 - .4, hf - .03), (x1, -D/2 - .4, hf - .03), (x1, D/2 + .35, hb + .06), (x0, D/2 + .35, hb + .06)], .05 + .025*(k % 2), RUST if k == 10 else ROOF)
for k in range(5): box(-8 + k*4 - .8, 2.4 - .25, 0, -8 + k*4 + .8, 2.4 + .25, .9, WOOD); box(-8 + k*4 - .7, 2.4 - .17, .6, -8 + k*4 + .7, 2.4 + .17, .85, STRAW)
for k in range(14): a = rnd.uniform(-10, 10); b = rnd.uniform(-3, 2); box(a - .3, b - .15, 0, a + .3, b + .15, .03, STRAW)
# ======== the water tower: braced legs, a banded tank, a cone cap with a finial, the ladder and a walkway ring
cur = "nf_tower"; groups[cur] = []
H = 12.
for (dx, dy) in ((-1.3, -1.3), (1.3, -1.3), (-1.3, 1.3), (1.3, 1.3)): box(dx - .11, dy - .11, -.3, dx + .11, dy + .11, H, METAL); box(dx - .25, dy - .25, -.3, dx + .25, dy + .25, .15, STONE)
for zz in (3.5, 7.5, 11.0):
    for s in (-1, 1): box(-1.4, s*1.3 - .05, zz, 1.4, s*1.3 + .05, zz + .1, METAL); box(s*1.3 - .05, -1.4, zz, s*1.3 + .05, 1.4, zz + .1, METAL)
for (y0_, y1_) in ((0, 3.5), (3.5, 7.5), (7.5, 11.0)):          # X braces on two faces
    for s in (-1, 1):
        for (za, zb) in ((y0_, y1_), (y1_, y0_)):
            vs = [(-1.3, s*1.3 - .03, za - .03), (1.3, s*1.3 - .03, zb - .03), (1.3, s*1.3 - .03, zb + .03), (-1.3, s*1.3 - .03, za + .03)]
            vs += [(v[0], v[1] + .06, v[2]) for v in vs]
            me = bpy.data.meshes.new("x"); me.from_pydata(vs, [], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]); me.validate()
            o = bpy.data.objects.new("x", me); col.objects.link(o); me.materials.append(METAL); put(o)
box(-1.6, -1.6, H - .1, 1.6, 1.6, H, WOOD)
cylz(0, 0, H, H + 3.4, 2.0, TANK, 20)
for zz in (H + .4, H + 1.7, H + 3.0): cylz(0, 0, zz, zz + .07, 2.04, DARK, 20)
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=2.2, radius2=0, depth=1.3)
me = bpy.data.meshes.new("cap"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("cap", me); col.objects.link(o); me.materials.append(SLATE); me.transform(Matrix.Translation((0, 0, H + 3.4 + .65))); put(o)
box(-.04, -.04, H + 4.05, .04, .04, H + 4.8, DARK); box(-.3, -.02, H + 4.55, .3, .02, H + 4.62, DARK)
for k in range(21): box(1.3 - .22, -1.55 - .02, .4 + k*.6, 1.3 + .22, -1.55 + .02, .46 + k*.6, METAL)
for s in (-1, 1): box(1.3 + s*.24 - .03, -1.58, -.1, 1.3 + s*.24 + .03, -1.52, H + .9, METAL)
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=24, radius1=2.25, radius2=2.25, depth=.05)
me = bpy.data.meshes.new("rail"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("rail", me); col.objects.link(o); me.materials.append(METAL); me.transform(Matrix.Translation((0, 0, H + .9))); put(o)
box(-.9, -2.06, H + 1.5, .9, -2.0, H + 2.2, WHITE)                # a painted board on the tank (blank: the town name goes on it later)
# ======== the farm shop: plank shack, a tin roof, the striped awning built from points, the counter, crates of produce
cur = "nf_shop"; groups[cur] = []
y0 = .15
box(-2, .82, -.2, 2, .98, y0 + 2.4, BARN); box(-2.08, -1, -.2, -1.92, 1, y0 + 2.4, BARN); box(1.92, -1, -.2, 2.08, 1, y0 + 2.4, BARN)
for x in [-1.8 + i*.45 for i in range(9)]: box(x - .03, .98, -.1, x + .03, 1.02, y0 + 2.3, WOOD)
quadbox([(-2.2, -1.2, y0 + 2.4), (2.2, -1.2, y0 + 2.4), (2.2, 1.2, y0 + 2.5), (-2.2, 1.2, y0 + 2.5)], .08, ROOF)
box(-1.8, -1.15, -.2, 1.8, -.65, y0 + .95, BARN); box(-1.9, -1.2, y0 + .95, 1.9, -.6, y0 + 1.02, WOOD)
for k in range(6):
    x0 = -2 + .02 + k*.66; x1 = x0 + .64
    quadbox([(x0, -2.2, y0 + 1.86), (x1, -2.2, y0 + 1.86), (x1, -1.0, y0 + 2.18), (x0, -1.0, y0 + 2.18)], .04, WHITE if k % 2 else mat("NF_awn_red", (.78, .2, .17), .7))
    vs = [(x0, -2.2, y0 + 1.86), (x1, -2.2, y0 + 1.86), ((x0 + x1)/2, -2.22, y0 + 1.66)]   # the scalloped valance, a point per stripe
    vs += [(v[0], v[1] - .02, v[2]) for v in vs]
    me = bpy.data.meshes.new("val"); me.from_pydata(vs, [], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]); me.validate()
    o = bpy.data.objects.new("val", me); col.objects.link(o); me.materials.append(WHITE if k % 2 else bpy.data.materials["NF_awn_red"]); put(o)
for x in (-2, 2): box(x - .04, -2.24, y0 + 1.6, x + .04, -2.16, y0 + 1.9, DARK)
for (du, m, r) in ((-1.2, APPLE, .08), (0, PUMP, .14), (1.2, GREENS, .09)):
    box(du - .5, -1.17, y0 + .95, du + .5, -.72, y0 + 1.15, WOOD)
    for k in range(7):
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=r)
        me = bpy.data.meshes.new("f"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("f", me); col.objects.link(o); me.materials.append(m)
        me.transform(Matrix.Translation((du - .38 + (k % 4)*.25 + (k // 4)*.12, -.95 + (.1 if k % 2 else -.1), y0 + 1.15 + r*.8 + (k // 4)*r*.9)))
        for p in me.polygons: p.use_smooth = True
        put(o)
for (x, y) in ((-2.6, -1.6), (2.7, -1.3), (2.6, -.4)): box(x - .3, y - .25, 0, x + .3, y + .25, .45, WOOD); box(x - .26, y - .21, .4, x + .26, y + .21, .5, (APPLE, PUMP, GREENS)[int(x > 0) + int(y > -1)])
box(-.6, -.6, y0 + 1.02, -.2, -.3, y0 + 1.3, mat("NF_jar", (.9, .65, .15), .3))
for x in (-1.4, 1.4): box(x - .04, -1.04, y0 + 2.5, x + .04, -.96, y0 + 3.4, WOOD)
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
bpy.ops.export_scene.gltf(filepath="/home/claude/weirdport/models/campaign/neighbour_farm.glb", export_format='GLB', use_selection=True, export_yup=True, export_apply=True, export_draco_mesh_compression_enable=True)
roots["nf_house"].location = (8, 6, .4); roots["nf_shed"].location = (-12, 14, 0); roots["nf_tower"].location = (17, 17, 0); roots["nf_shop"].location = (-6, -14, 0)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (.55, .72, .95, 1); bg.inputs[1].default_value = .5
g = bpy.data.meshes.new("g"); g.from_pydata([(-80, -80, -.01), (80, -80, -.01), (80, 80, -.01), (-80, 80, -.01)], [], [(0, 1, 2, 3)]); go = bpy.data.objects.new("g", g); col.objects.link(go); g.materials.append(mat("G", (.35, .45, .2), 1))
sun = bpy.data.lights.new("sun", 'SUN'); sun.energy = 3.4; sun.color = (1, .92, .78); so = bpy.data.objects.new("sun", sun); col.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(-30))
cd = bpy.data.cameras.new("C"); cd.lens = 24; cam = bpy.data.objects.new("C", cd); col.objects.link(cam); sc.camera = cam
cam.location = (-14, -34, 9); cam.rotation_euler = (Vector((2, 4, 5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = "/home/claude/campaign/neighbour_farm.png"; bpy.ops.render.render(write_still=True)
