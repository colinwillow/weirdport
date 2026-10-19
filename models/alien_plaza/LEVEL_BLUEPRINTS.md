# Level Blueprint Library

Twelve famous levels taken apart into reusable patterns, for small, hand-made alien islands (~200 m across,
5 cores each, one new tech per level).

**Why this exists.** Generated layouts feel like "random stuff everywhere". In every level below, each object
has a job. It is a **landmark** (shows you where to go), a **beat** (asks you to use a verb), a **gate**
(says "not yet"), a **reward**, or a **return path**. If a ledge, crate or enemy has none of these jobs, cut it.

**How to read each entry.** Facts about the source game come from the sources at the end. Anything labelled
*guidance* is my design advice, not a measured fact about the source. Our numbers come from `LEVELS.md`:

| Verb | Number used in this doc |
|---|---|
| Jump | apex 2.8 m, ~1.06 s airtime |
| Flat gap | 5 m = easy, 6.5 m = needs a sprint, ~7 m = the absolute limit at 7.2 m/s |
| Ledge | 2.0 m = easy, 2.5 m = clean jump. Above that needs a ledge grab, ladder or tech |
| Hover Pack (L1) | +1.0 m lift, 1.0 s of hover (the `HOVER` numbers the route checker uses). Hover gaps are built at 9–15 m and hover ledges at up to 4.4 m; `route_check.py` proves both |

**One beat grammar runs through all of them: Kishōtenketsu.** Game Maker's Toolkit describes Super Mario 3D
World's levels as four stages: **introduce** a mechanic, **develop** it, **twist** it, then **conclude** it and
set it aside. Director Koichi Hayashida tied this to kishōtenketsu. Every core route below should be one of
these four-beat arcs. "Teach / test / twist / payoff" in this doc means the same thing.

---

## 1. Delfino Plaza: the hub where the landmarks are the doors
**Source:** Super Mario Sunshine (2002). **In one line:** a dense town where every big landmark is also the
entrance to something, and each one opens at a set Shine count or with a set nozzle.

**Topology:** hub with spokes, where the spokes come out of the landmarks themselves.
```
            [Lighthouse]->Gelato         [Bell towers]
                  \                        /
   [Cannon]->Pinna --- ( PLAZA CORE ) --- [Rooftop pipe]->Sirena
                  /          |             \
  [Boathouse]->Ricco   [Shine Gate]->Pianta/Corona   [Grand Pianta Statue]->Bianco
```

**Beat grammar:** you come back to the hub after every episode. Each time you return, the plaza has one new
thing in it: a new portal, a new nozzle box, or a new bit of light.

**Gating (facts):**
- Each level entrance is a landmark. Bianco Hills is on the Grand Pianta Statue, Ricco Harbor is at the
  Boathouse, Gelato Beach is at the lighthouse, Pinna Park is through a cannon, and Sirena Beach is a pipe on a
  rooftop.
- They open in stages. Ricco opens at 3 Shines, Gelato at 5, Pinna at 10 and Noki Bay at 20. The Turbo Nozzle
  comes at 25 Shines (after Yoshi) and the Rocket Nozzle at 30, which also opens Pianta Village.
- The plaza has **15 secret Shines of its own**. Some are puzzles (crates, a coin given to a Pianta). Others
  need a later nozzle: the Turbo Nozzle breaks into the west belltower building, and the Rocket Nozzle
  ground-pounds the lighthouse slab.

**How it shows you the goal early:** the slab, the locked tower and the high ledge are all visible on your
first walk around, years before you can use them.

**What to measure (guidance):**
- Every portal or locked secret is a landmark you can see from the central square.
- Every return to the hub should show **one** visible change.
- Give the hub about 3 secrets that later tech opens, and put each one on a landmark.

**Use it in our game:** the Glowtide plaza (Level 1) is our Delfino. Put the doors to the core routes on
the landmarks: the clock tower, the lighthouse and the waterfall gate. Hang 3 later-tech secrets on
landmarks the player passes every trip:
- a cracked slab on the fountain (Gravity Boots)
- a glowing anchor on the bell tower (Grapple Tether)
- a violet field over the harbour-master's door (Phase Shift)

**Fits:** Level 1, and any town level.

---

## 2. Bianco Hills: one map, ten states
**Source:** Super Mario Sunshine. **In one line:** one map that stays the same, and each episode changes a few
conditions to give a new mission.

**Topology:** a ring around a lake with a tower on an island in the middle.
```
   [Start cliff, view of the bay] -> [Windmill Village W] -> [Wall + gate + water wheel]
                                                              |
                         ( LAKE w/ leaf boats )  --spiral-->  [Big Windmill, centre isle]
                          |                 \
                     [Hillside Cave]      [Cliff Spring Cave behind the windmill]
```

**Beat grammar:** episode 1 is a path to the landmark (*Road to the Big Windmill*). Episode 2 is a boss on top
of it. Later episodes reuse the same ground with a new condition: the boss in the village, a secret course
that opens off the lake, red coins, or a chase.

**Gating (facts):**
- Brambles cover the windmill for the first two episodes.
- The Hillside Cave opens from episode 3 and the Cliff Spring Cave from episode 6.
- Ep 8 adds extra lake platforms and ropes.
- Nozzle boxes start to appear from episode 4.
- Petey Piranha stands on the windmill in episode 2 and in the village in episode 5.

**How it shows you the goal early:** the windmill is the tallest thing on the map and you see it from the
very first cliff.

**What to measure (guidance):**
- 10 missions on one map means the *map* stays the same and only the *props* change. Count how much each
  mission changes. A good mission changes 1–3 things: an enemy placement, a blocker, or a platform set.
- Each mission keeps the same landmark in view.

**Use it in our game:** this is how to get 5 cores out of a single 200 m island without building 5 maps. For
each core, change one thing:
- a gate opens
- the tide drops and shows a walkway
- guards move to the docks, so it is a disguise core
- rails light up, so it is a board core
- one area changes after the Hover Pack

**Fits:** every level. It is the cheapest way to fill a small island.

---

## 3. Bob-omb Battlefield: the summit you can see from the start
**Source:** Super Mario 64 (1996). **In one line:** the goal sits on a mountain that is always in view, and the
route to it climbs round the mountain into the danger.

**Topology:** a critical path, then a spiral up the mountain, with one sky island off to the side.
```
 [Start S: cannon, buddies] -> bridge -> [Field: Chain Chomp, water bombs] -> teeter bridge
        -> [Mountain base] -> spiral path (iron balls roll DOWN at you) -> [SUMMIT: King / flag]
        (side) cannon ------------------------------------------> [Floating island: Wing Cap]
```

**Beat grammar:** you cross three bands, then climb. The spiral sends the danger (rolling iron balls) down the
same path you are climbing. Star 1 is the boss on the summit. Star 2 is a race up the same route (Koopa the
Quick). Stars 3–6 use the cannon, the red coins, the Wing Cap and the Chain Chomp's gate.

**Gating (facts):**
- 6 stars plus a 100-coin star.
- The cannon that reaches the floating island is shut until you talk to a Bob-omb Buddy.
- Behind Chain Chomp's Gate needs you to ground-pound a post that holds the Chomp.

**How it shows you the goal early:** a Game Developer comparison notes that Bob-omb Battlefield and Cascade
Kingdom both put the first goal in plain view early, at the peak.

**What to measure (guidance):**
- The summit should be visible from the spawn and from at least 80% of the route.
- The danger on the spiral comes *toward* you. A climb with nothing coming down it is just stairs.
- Use the same route twice, once as a fight and once as a race. That gives you a second core for free.

**Use it in our game:** a Volcano Core. Spiral a ramp 3 times around a 20–25 m cone.
- Roll goo boulders down the ramp, and let a dodge roll go through them.
- Break the ramp at 2 points with 5 m gaps (the teach level), then 1 point with a 6.5 m sprint gap (the test).
- Put a race version on the same ramp for a second core. A local skater races you, so board it.
- Add a later-tech sky island off the summit. It needs the Hover Pack, or a Grapple anchor in Level 2+.

**Fits:** Level 1, as the volcano behind Glowtide.

---

## 4. Whomp's Fortress: the climb that changes after you win
**Source:** Super Mario 64. **In one line:** a fortress climbed by switchbacks, where beating the boss on top
replaces him with a new tower that the next stars use.

**Topology:** a layered climb with a split near the top.
```
 [Base field] -> ramp w/ moving bars -> receding-platform gaps -> Thwomp stairs
     -> fork:  down-ramp -> [pool, Bob-omb Buddy, cannon]
               up-path   -> Piranhas -> falling bridge -> turning bridge -> Whomps -> [TOP: Whomp King]
 After star 1: [TOP] now holds a tall tower with receding steps.
```

**Beat grammar:** each floor brings in one obstacle type: moving bars, receding platforms, Thwomps, then a
falling bridge and a turning bridge. Each one is a short four-beat arc. The fork near the top gives a quieter
side branch (the pool and cannon) that pays off in later stars. Hoot the owl, in the starting tree in some
missions, carries you up to platforms above the course. That is an alternate way in, offered in some missions
only.

**Gating (facts):** the Whomp King is on top only for mission 1. After that a tower stands there instead.
6 stars, including *Blast Away the Wall* and *Fall onto the Caged Island*.

**What to measure (guidance):**
- About 4–5 floors, each with one new obstacle. Never bring in two new ones on the same floor.
- After the main goal is done, change the top of the map in a way you can see from below.

**Use it in our game:** the Bell Core in Glowtide's clock tower. Teach one new verb on each floor:
- Floor 1: a ladder.
- Floor 2: a 2.5 m ledge.
- Floor 3: a 5 m gap with a swinging bar.
- Floor 4: a cracked wall you hammer through.
- Top: guards. Fight them, or use the DNA disguise to walk past.

When the core is taken, a new spire grows out of the roof. Its first step is a 4.0 m hover ledge for the
mid-level Hover Pack core.

**Fits:** Level 1. The idea of "the map changes after the boss" fits every level.

---

## 5. Good Egg Galaxy: a string of beads
**Source:** Super Mario Galaxy (2007). **In one line:** a chain of tiny planets, each of which is one complete
idea, linked by launch stars.

**Topology:** a linear chain. Each bead is self-contained.
```
 [Tower] *-> [Peanut: 5 Star Chips] *-> [Bean: beat Piranha -> vine] -> [Bitten apple: shrinking platform, pipe]
   -> [Flipswitch planet: flip all panels] *-> [Block climb] *-> [Dino Piranha egg]
```

**Beat grammar:** each planet has one rule and one action that ends it:
- Collect chips, and a launch star forms.
- Beat the Piranha Plant, and a vine grows.
- Flip every panel, and a launch star appears.
- Climb the blocks, and you reach the launch star on top.

The pattern is: finish the bead, and the link to the next bead *appears*.

**Gating (facts):** every launch star after the first is earned on the planet before it (the chips, the
panels, the top of the climb).

**What to measure (guidance):**
- One rule per bead.
- A bead should take 30–90 s.
- The reward for finishing a bead is the way to the next bead. No keys, and nothing to backtrack for.

**Use it in our game:** use this for any core route that runs offshore or up through the sky. For example, a
**Reef Core** across 5 rock stacks in the harbour, one idea per stack:
1. Grind a rail.
2. Hammer a pillar into a bridge.
3. Shoot 4 targets to raise steps.
4. Make a 6.5 m sprint gap.
5. Make the first 9 m hover gap.

Finishing each stack raises the bridge or lights the zipline to the next.

**Fits:** good for the second half of any level, after the tech is in hand.

---

## 6. Cascade Kingdom: the key is a creature
**Source:** Super Mario Odyssey (2017). **In one line:** a short guided route that a capture opens up. The early
reward comes almost at once, and the whole map opens after the boss.

**Topology:** a short critical path, then open loops.
```
 [Waterfall Basin: landing] -> (Chain Chomp breaks wall: early moon ~50 ft from start)
    -> [Stone Bridge: rubble -> T-Rex / Big Chomp] -> [Big Stump: Chomp breaks blocks over a pipe]
    -> [Fossil Falls Heights: fling Chomp at rubble] -> [Broode arena: Multi Moon]
 After the boss: the whole kingdom is open for the remaining moons.
```

**Beat grammar:** you capture something, and its power is the key. The Chain Chomp breaks rubble near the start,
again at the Big Stump and again at the summit, so you meet one key three times. The T-Rex is a **power
fantasy** you get early: it smashes the rubble on the bridge, and a trampoline at the base of its nest throws
you toward the summit.

**Gating (facts):**
- 42 moons in all.
- 16 plus the Multi Moon can be collected on the first visit.
- Only 5 are needed to move on.
- The Island in the Sky is reached through a painting in a different, later kingdom. That is a
  cross-level secret.

**How it shows you the goal early:** the main task sits at the top of the area, on a platform high above the
island. You see it early and only reach it at the end. The first moon is about 50 ft from the start, which
tells you that moons are stops along the way.

**What to measure (guidance):**
- The first reward comes in **under 30 s**.
- One capture or key is used **3 times** on the main path, in 3 different settings.
- The number needed to move on (5 of 42) is far below the number available. For us that would mean "5 cores
  open the exit, and there are side glyphs as well".

**Use it in our game:** this is the **DNA disguise** core. Become a goo warrior, a big heavy body, to:
- shoulder through rubble (1)
- get waved past a guard post (2)
- be thrown by a launcher only warriors may use (3)

Put a cracked crate with a small reward 15 m from the spawn, so the first minute pays out.

**Fits:** Level 1 for the disguise. Later levels, with the tech as the "capture".

---

## 7. Forest Temple: the hub that keeps score
**Source:** The Legend of Zelda: Ocarina of Time (1998). **In one line:** a central hub where four torches go
out at the start, with each wing returning one flame, and one tool sending you back through rooms you have
already seen.

**Topology:** hub with spokes, plus a loop the tool opens.
```
                 [W wing: courtyard]      [E wing: courtyard / well]
                          \                  /
   [Entry] -> ( HUB: 4 torches, elevator DOWN-blocked ) -> [N: block puzzle -> Poe 3]
                          /                  \
          [Twisted corridor <eye switch>] -- [Bow room] -> back: shoot eye, corridor untwists
                                    -> [basement: rotating roulette room] -> Boss Door
```

**Beat grammar:**
1. Show the problem at the start. Four Poes steal the flames and the elevator drops.
2. Each wing ends with a Poe and **a flame you can see relit in the hub**, so your progress is part of the
   room you keep crossing.
3. Twist: an eye switch above a door that the Slingshot cannot reach as an adult. You pass under it on the way
   to the Fairy Bow, and a Poe painting on a staircase hints that you will want the bow later.
4. You come back with the bow and shoot the eye. The corridor untwists and there is a new route through a
   room you already know.

**Gating (facts):**
- The goal is "find the four Poes and relight the torches".
- Poes 1–2 are beaten by shooting their paintings.
- Poe 3 needs a timed block puzzle.
- Poe 4 makes clones, and you must spot the real one.
- The Boss Door is in the last section, past the roulette room.

**What to measure (guidance):**
- The hub shows your progress **in the room itself**, not only in the HUD.
- Each tool-gated switch is passed at least once *before* you have the tool, close to the path, at eye height
  or above.
- Each wing gives back one torch, then returns to the hub.

**Use it in our game:** Glowtide's beacon is our four torches. Put 5 glyph sockets around the beacon gate, and
light each one as its core comes home, so the player sees progress every time they cross the plaza. Put the
Hover Pack vault midway, and on the way *to* it make the player walk under a lip 4.0 m up that they cannot yet
reach (the route checker should mark that ledge NEED: hover). After the vault, that lip is a shortcut back to
the plaza.

**Fits:** Level 1. The structure works for any level whose tech arrives midway.

---

## 8. A Breath of the Wild shrine: the one-idea room
**Source:** BotW (2017), the Oman Au shrine (the Magnesis Trial), plus the GDC 2017 talk "Change and
Constant — Breaking Conventions". **In one line:** one room, one rule, taught and then tested in under five
minutes.

**Topology:** a short line of rooms, with one side pocket.
```
 [Pedestal: get rune] -> [lift plate -> ladder down] -> [block wall: pull blocks] -> [Guardian]
     -> [slab: ride / bridge it] -> (side: pull chest off ledge -> Bow) -> [pull doors] -> [Spirit Orb]
```

**Beat grammar (facts):**
1. Get the rune.
2. Use it at once to lift a plate, which shows a ladder.
3. Use it to clear a wall of blocks.
4. Pressure: a Guardian.
5. A slab you must move into a bridge.
6. Optional: pull a chest off a ledge, which holds the Traveler's Bow.
7. Pull the doors open, and the reward is there.

**One idea, used about 5 times, from simple to clever.** The GDC talk gave the prototype's rule as "there's a
simple goal, can you reach it?" The team's *triangle rule* (from the same talk, as reported by 80.lv) is that
a triangle shape offers a choice of going over or around, and it hides what is behind it, which makes you
curious. Rectangles are used when something must be hidden completely.

**What to measure (guidance):**
- 4–6 uses of one rule per room. The first use is forced and impossible to fail. The last asks you to use the
  rule on yourself or on a treasure.
- One optional pocket per room.
- Use triangles (berms, hills) to hide a reward so the player chooses to go over or around. Use rectangles
  (walls) to hide completely.

**Use it in our game:** the **Tech Vault** where each level's tech is found is a shrine.
- Hover Pack (L1): hover a 1 m pit, then a 9 m gap, then climb to a 4.0 m ledge, then fall a long way slowly
  past laser rows, then the optional pocket is behind a lip you have to overshoot.
- Each later tech's vault follows the same shape.

**Fits:** every level, once per level, at the tech handoff.

---

## 9. Prince of Persia: The Sands of Time: one woven route up a palace
**Source:** PoP: SoT (2003). **In one line:** one route, hidden inside architecture that is believable, climbing
a palace built around what the player can do.

**Topology:** a vertical tower climb. The route is a single line, but it twists and turns back on itself.
```
   [Tower top] <- column swing <- wall-run <- beam <- ledge shimmy
        ^                                              |
   [mid gallery] <- pole <- wall-run <- (rewind save) <-
        ^
   [Courtyard floor]
```

**Beat grammar:** the room *is* the puzzle. Ubisoft says designers built rooms from plain blocks first and the
art came after. When designers asked for unsupported ceiling columns, the team added side poles to make them
believable, and those poles became swing and navigation challenges: "we made constraints into fun". Azad's
palace was laid out so you climb up through the castle to the top of the tower. The rewind was in from very
early and the whole game was built around it, so that a missed jump does not send you all the way back. One
critique points out that SoT's route was a single straight path "woven into" the architecture, while later
free-running games left players unsure where they needed to go.

**Gating:** nothing to collect. The gate is whether you can execute. The rewind softens a failure.

**What to measure (guidance):**
- **Every grabbable thing has a reason in the architecture**: a pole holding up a beam, a ledge that is a
  cornice, a crack that is damage.
- 1 obvious line per room. An alternate line is fine if it is just as legible.
- A checkpoint before every chain of 3 or more moves where one miss means a fall.
- Each room's exit is in view from where you enter it, ideally framed by the camera.

**Use it in our game:** the clock tower, the lighthouse, and every "climb the building" core.
- Make every ledge a cornice, sign, awning or balcony.
- Make every ladder a maintenance ladder that goes to a door.
- Any gap of 6.5 m or more gets a checkpoint or a safe fall (water, an awning) below it.
- The architecture should explain where the route is.

Our ladders and ledge grab are SoT's shimmy and pole. Our Grapple Tether (L2) plays the part of the column
swing.

**Fits:** all levels. Grapple anchors from Level 2.

---

## 10. St. Francis' Folly: the six-storey atrium
**Source:** Tomb Raider (1996). **In one line:** one huge vertical room with a door to a trap room at each floor,
four keys, and the exit at the bottom.

**Topology:** a layered tower around a central climbable structure, 6 storeys.
```
 L6  Neptune door            |     |
 L5  Thor switch             | C   |
 L4  Damocles switch, Atlas door | E |
 L3  Thor door               | N   |
 L2  Neptune switch, Damocles door | T |
 L1  Atlas switch, secret room, EXIT (4 key locks)
```

**Beat grammar (facts):**
- The room has 6 storeys, a central structure, and four doors named after myths: Neptune, Thor, Atlas and
  Damocles.
- Each door hides a trap and a key:
  - Neptune: a flooded current, with a lever to stop it.
  - Atlas: a rolling boulder you outrun to a safe ledge.
  - Thor: lightning, and a hammer over a pressure pad.
  - Damocles: ceiling swords that fall as you approach.
- The exit at the bottom needs all four keys.
- You move with running and standing jumps to ledges, and come back down by dropping to lower ledges.
- **The switch for a door is often on a different floor from the door itself.** The switch for the Neptune
  door at the top is on L2, for example. That makes you cross the room again and again.

**What to measure (guidance):**
- Storeys of about 4–6 m each. For us, each storey is reached by one ladder or one 2.5 m ledge plus a grab.
- The central structure is visible from every door.
- Switch and door on different floors, so the atrium is crossed many times. Never make those crossings boring:
  each one should be a short climb or drop, not a long walk.

**Use it in our game:** a **Cistern Core** under the plaza. Put a 4-storey well, about 18 m deep, with a
climbable pump tower in the middle. 4 small side rooms each hold one glyph shard: a current room, a boulder
room, a guard room (use the disguise) and a crusher room (dodge roll). The core rises when all 4 are
socketed at the bottom. Later tech: a Phase Shift field (L3) on a fifth door at L4.

**Fits:** Level 1 at 4 storeys, and Levels 3–4 at the full 6.

---

## 11. Ratchet & Clank, Novalis: a spine with tool-gated branches
**Source:** Ratchet & Clank (2002). **In one line:** a planet with a main route and side branches that only a
gadget from later opens.

**Topology:** a critical path with loops and gated branches.
```
 [Landing pad + vendor] -> elevator -> [Crater floor: river, suspension bridge] -> [dry crater]
        |                                      |                 \-- hidden extendable bridge (SHORTCUT back)
        +-> [Cave 1: bolt-crank doors]         +-> swim upstream: [Cave 2] (needs Hydro-Pack, later)
        +-> [Waterworks: stalactite platforms] -> cliff-top room w/ window = quick exit
```

**Beat grammar (facts):** the landing pad leads to a vendor, the waterworks, the sewers, a cave and an elevator
down. The dry crater has a hidden extendable bridge that works as a shortcut. The waterworks end in a cliff-top
room with a quick exit. The second cave is reached only by swimming upstream, which needs the Hydro-Pack.

**Gating:**
- Branches are locked by gadgets: bolt cranks, and the Hydro-Pack.
- Every branch ends near the landing pad, through a shortcut or an exit.

**What to measure (guidance):**
- Every branch's end connects back to the start within about 20 s, using a shortcut you open from the far side.
- At least 1 later-gadget branch per planet, entered from a spot you pass on the main route.

**Use it in our game:** each level has a **landing point** with a shop or save. Every core route ends in a
one-way shortcut back:
- a zipline down to the plaza
- a ladder you kick down
- a gate you open from the far side
- a rail you can grind home

Every level also has one blocked branch next to the main path:
- an anchor in the sky for the Grapple
- a violet field for Phase Shift
- a vent for the Shrink Ray

**Fits:** all levels. The shortcut rule matters more than anything else in this entry.

---

## 12. Mumbo's Mountain: a collectathon around landmarks
**Source:** Banjo-Kazooie (1998). **In one line:** a small first world built around a few memorable landmarks,
each of which has a move, a jiggy and a reason to go there.

**Topology:** a ring of landmarks around a central climb.
```
         [Termite Mound (tall pillar, top)]
        /                                  \
 [Stonehenge: Talon Trot] ---- [centre slope] ---- [Conga's Tree / jungle: Egg Firing]
        \                                  /
         [Mumbo's Skull + huts: Beak Buster nearby]  -- [lake + bridge near start]
```

**Beat grammar (facts):**
- Moves are taught at specific landmarks: the Beak Buster beside Mumbo's Skull, the Talon Trot at the
  Stonehenge, and Egg Firing in Conga's jungle.
- The first move at each place is used there at once, on things just next to it.
- Mumbo turns you into a termite, and only a termite may enter the Termite Mound and climb it. A jiggy, a
  Mumbo token, a note and the Witch Switch all need that form.
- 10 jiggies and 100 notes. The world needs 1 jiggy to enter.

**Why it works:** this is a *transformation gate*. Your shape is the key. It is the closest well-documented
match to our DNA disguise.

**What to measure (guidance):**
- About 5–6 named landmarks for about 10 collectibles. That is about 2 rewards per landmark, so nothing is
  "somewhere".
- Notes, or our small pickups, are laid as **breadcrumb lines along the intended route**, never as scatter.
- One shape-gated interior per level.

**Use it in our game:** name 5 landmarks and give each one 1 core and 1–2 glyph secrets. Lay the small pickups
along the routes in lines and arcs that show where to jump: an arc of 5 pickups over a 6.5 m gap means "sprint
here". Disguised as a goo grunt, you are let into the goo nest. That is the Mumbo's Mountain termite mound for
us.

**Fits:** Level 1, and the general method for any level.

---

# Level Spec Template (fill this in before anything is built)

Copy this block for each level. A blank field means the level is not ready to build.

```
LEVEL ____  name: ____________   island size: ___ x ___ m   tech given: __________ (vault at core #__)
TOPOLOGY: (hub+spokes / ring / layered tower / bead chain / spine+branches)  ASCII diagram attached: Y/N
FANTASY in one line: ______________________________________________

LANDMARKS (3-6). Each must be visible from the spawn OR from the hub's centre.
 id | name        | height m | seen from (list points) | sightline distance m | its job (door / goal / guide)
 L1 |             |          |                         |                      |
 ...
VISTA POINTS (>=2): spot, what is framed, which locked things are visible from here.

CORE ROUTES (exactly 5). Each is ONE four-beat arc: teach / develop / twist / payoff.
 Core # | name | verb family (acro/clue/fight/disguise/board/tech) | start landmark | ends at
 Beats  (one row each; every number is a real build number):
   b# | verb       | geometry           | value          | fail result      | checkpoint?
   1  | jump       | flat gap           | 5.0 m          | water, 3 s back  | -
   2  | ledge grab | wall               | 2.5 m          | 1 m drop         | -
   3  | hover      | gap                | 9.0 m          | fall to plaza    | yes
   4  | ...        |                    |                |                  |
 Return path: shortcut type (zipline / kicked ladder / gate / rail) + time back to hub (s): ___
 Max NEW ideas on this route: 1. Max carried-over ideas: 2.

GATING TABLE
 gate | where | blocks what | opened by (core / tech / disguise / switch) | seen BEFORE it opens? where?

SECRETS FOR LATER TECH (>=3, each on or beside a landmark the player passes)
 secret | location | needs (Grapple / Phase / Gravity / Tractor / Shrink) | visible hint | reward

ENEMIES: each placement has a reason (guards a gate / pressures a beat / teaches a verb / is a disguise source)
 enemy | location | reason | count

PICKUPS: breadcrumb lines only. List each line and what it teaches (arc = jump here, line up wall = climb).

BUDGET
 draw calls ___ | tris ___ | texture MB resident ___ | unique props ___ | NPCs ___ | build days ___
CHECKS: route checker green on every beat; every NEED: tech ledge reachable after that tech; no orphans
 (every object appears in a landmark / beat / gate / reward / return path row above, or it is cut).
```

---

# Universal Rules (distilled from all twelve)

1. **Show it before you give it.** The summit (Bob-omb), the slab on the lighthouse (Delfino), the eye switch
   (Forest Temple), the platform high over the island (Cascade). Every goal and every locked secret is seen
   before it can be reached. If it cannot be seen from somewhere the player walks, they will never think
   about it.
2. **One new idea per stretch, then retire it.** Introduce, develop, twist, conclude (Mario 3D World), one
   rule per planet (Good Egg), one rune per shrine (BotW). Two new things at once is how a level reads as
   chaos.
3. **Landmarks are the doors.** Delfino puts its portals on its landmarks, and Mumbo's Mountain gives each
   landmark a move and a reward. Hang every core and secret on a named landmark, so the map is a list of
   places rather than a field of stuff.
4. **Progress is visible in the world.** Torches relit in the Forest Temple hub, a new tower on Whomp's
   Fortress, light returning to Delfino. Our beacon sockets and the plaza's changes must show it without the
   HUD.
5. **Reuse the map and change the state.** Bianco Hills gets 10 episodes out of one map. On a 200 m island,
   five cores come from changing the conditions (tide, guards, rails, a gate), not from five new areas.
6. **Every branch ends in a shortcut home.** Novalis's hidden bridge, the waterworks window exit, Whomp's
   Fortress's warp. A route you have finished should take seconds to leave, not a walk back.
7. **The architecture explains the route.** A pole holds up a beam (Prince of Persia), a ledge is a cornice, a
   pickup arc is a jump. If a ledge has no reason to be there, either give it one or cut it.
8. **Need far fewer than you offer, and gate the rest on later tech.** Cascade needs 5 of 42 moons, and
   Delfino's 15 secret Shines include nozzle-gated ones. Our 5 cores open the exit, and the 3+ secrets per
   level wait for later tech. That return visit is the reason to go back to earlier levels.

---

# Sources

- Game Maker's Toolkit, *Super Mario 3D World's 4 Step Level Design* (via MCV/Develop): https://www.mcvuk.com/development/video-nintendos-level-design-secrets-in-four-steps
- Gigazine on the same video: https://gigazine.net/gsc_news/en/20160920-super-mario-3d-world-4-step-level-design
- Super Mario Wiki, Delfino Plaza: https://www.mariowiki.com/Delfino_Plaza
- Super Mario Wiki, Bianco Hills: https://www.mariowiki.com/Bianco_Hills
- Super Mario Wiki, Bob-omb Battlefield: https://www.mariowiki.com/Bob-omb_Battlefield
- Super Mario Wiki, Whomp's Fortress: https://www.mariowiki.com/Whomp%27s_Fortress
- Super Mario Wiki, Good Egg Galaxy: https://www.mariowiki.com/Good_Egg_Galaxy
- Super Mario Wiki, Cascade Kingdom: https://mariowiki.com/Cascade_Kingdom
- Game Developer, *Mario 64 v Odyssey*: https://www.gamedeveloper.com/design/mario-64-v-odyssey
- Game Developer, *The Level Design of Super Mario Odyssey's Best Stage*: https://gamedeveloper.com/design/the-level-design-of-super-mario-odyssey-s-best-stage
- University of Tulsa CSG, *Exploration, Linearized: the Level Design of Super Mario Odyssey*: https://sites.utulsa.edu/csg/?p=30
- Zelda Dungeon, *Brilliance in Level Design: Ocarina of Time's Forest Temple*: https://www.zeldadungeon.net/?p=10887
- Zelda Wiki, Forest Temple (Ocarina of Time): https://zeldawiki.wiki/wiki/Forest_Temple_(Ocarina_of_Time)
- Zelda Wiki, Twisted Hallway: https://zeldawiki.wiki/wiki/Twisted_Hallway
- GDC Vault, *Change and Constant — Breaking Conventions with The Legend of Zelda: Breath of the Wild*: https://gdcvault.com/play/1024562/Change-and-Constant-Breaking-Conventions
- Thumbsticks, GDC 17 BotW talk report: https://www.thumbsticks.com/gdc-17-breaking-conventions-breath-of-the-wild
- 80.lv, *The Design Secrets of Breath of the Wild* (triangle rule): https://80.lv/articles/the-design-secrets-of-breath-of-the-wild/
- Thonky, Oman Au Shrine (Magnesis Trial): https://www.thonky.com/zelda-breath-of-the-wild/shrine/oman-au
- Ubisoft News, *Prince of Persia: Creating the Sands of Time Trilogy*: https://news.ubisoft.com/en-us/article/3oAqiLg5k7GazIw5OWYTO2
- A Most Agreeable Pastime, *From Prince of Persia to Assassin's Creed: the curse of overly complex level design traversal*: https://amostagreeablepastime.com/2014/07/12/from-prince-of-persia-to-assassins-creed-the-curse-of-overly-complex-level-design-traversal/
- Stella's Tomb Raider walkthrough, St. Francis' Folly: https://tombraiders.net/stella/walks/TR1walk/05stfrancis.html
- Stella's TR Anniversary developer commentary: https://tombraiders.net/stella/walks/TRAwalk/details/commentary2.html
- Ratchet & Clank Wiki, Novalis: https://ratchetandclank.fandom.com/wiki/Novalis
- StrategyWiki, Banjo-Kazooie / Mumbo's Mountain: https://strategywiki.org/wiki/Banjo-Kazooie/Mumbo%27s_Mountain
