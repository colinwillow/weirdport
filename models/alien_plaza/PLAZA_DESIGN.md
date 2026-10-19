# Alien Plaza: a standalone hub level (Delfino Plaza study)

A separate level with its own scene, its own export and its own budget. It is not a district of the big
alien map, and it can be stitched in later if we want that.

The exercise: rebuild Delfino Plaza's LAYOUT faithfully as a greybox, prove that the routes work, and only
then reskin it in our alien kit. Every object in the greybox has a job, and that job is written down here.

## Player metrics (read from the game, index.html)
- Rig height is 1.25 m. A step he can walk up is 0.357 m, so stairs are built at 0.30.
- A jump is 10.6 m/s at gravity 20 m/s², which peaks at **2.8 m**. Design numbers:
  - EASY ledge: 2.0 m.
  - CLEAN-JUMP ledge: 2.5 m.
  - Anything over 2.8 m needs a ladder, a rope line, a stepping object or a ledge grab.
- One storey is 3 m. Rooftop tiers are R1 at 6 m, R2 at 9 m and R3 at 12 m. Towers run 15–24 m.

## Delfino's rules, and how this level keeps them
1. **Every landmark is visible from the spawn and is a goal.** From the stage at the plaza's south edge
   you see:
   - centre: the bell hall's clock tower;
   - straight behind it: the gate and its waterfall;
   - far left: the boathouse dome;
   - far right: the SE keep, with the lighthouse peeking over the east rooftops.
2. **The plaza is a sunken courtyard that the town wraps around.** Its floor is 0.9 m down, with a fence
   and three ways in. Buildings close it on the north, west and east; the sea promenade is in front.
3. **A canal cross organises the town.** The main canal runs on axis from the waterfall to the back of the
   bell hall, with a west branch to the sea and an east branch to a harbour basin. Bridges are the
   crossings, and ledges just above the water are a secret route.
4. **A second map runs on the rooftops.** The roofs step up in tiers that you can travel along, joined by
   jumps, rope lines and ladders. Towers are the punctuation and the vantage points.
5. **The edges are never straight.** The sea wall has a central bastion with grand stairs down to the
   water, the beach is a crescent, the keep stands half in the sea, and the boathouse sits out on a pier.
6. **It is small and dense.** About 230 × 200 m including the beach, the mountain face and the islets.
   Nothing is filler: every block either makes a route, hides one or frames a view.

## Map (metres; origin at the plaza fountain; +Y is north toward the mountain; +X is east)
| # | Zone | Where | Height | Job |
|---|---|---|---|---|
| 1 | Sunken plaza | x -45..40, y -12..14 | floor -0.9 | Hub. Fountain at (0,0). Stage at (0,-13) is the spawn. |
| 2 | Bell hall + clock tower | x -22..22, y 14..26; tower x -13..-7 (off the canal axis so it never hides the gate) | 6 m hall, 18 m tower | Centrepiece. Shops face the plaza. The open bell room on top is an objective. |
| 3 | Main canal | x -5..5, y 26..88 | water -2 | Axis to the gate. Arched bridge at y 40, flat bridge at y 65. Ledges at -0.8. |
| 4 | West canal | y 30..36, x -75..-5 | water -2 | To the sea. Bridge at x -30. |
| 5 | East harbour | basin x 32..62, y 50..78; channel y 50..56 | water -2 | U-basin with a quay finger and two bridges. |
| 6 | West quarter | x -70..-8, y 38..85 | 6–12 m, twin tower 24 m | Alleys up to the mountain. The twin tower is the "prison tower" (endgame vantage). |
| 7 | East quarter | x 8..30 and 62..78, y 30..85 | 6–9 m, dome 14 m | Rooftop chain to the lighthouse. |
| 8 | West wing | x -70..-45, y -15..35 | towers 9 / 12 / 15 | Stepped climbing showcase that overlooks the plaza. |
| 9 | Boathouse | dome at (-88,-20), pier x -102..-74 | 10 m dome | Boat exit and a dock with boats. |
| 10 | East wing | x 40..55, y -15..30 | 6 m, roof garden | Roof NPC who throws you up the keep. |
| 11 | Promenade | y -36..-14 | 0 | Organic palm beds. Bastion at x -18..18, y -50..-36, with grand stairs to the sea. |
| 12 | SE keep | x 56..78, y -46..-16 | 12 m + 18 m tower | Half in the sea, with a dock on its east side. High vantage. |
| 13 | Statue circle | (88,10), r 7 | 0 | The grand statue and its portal. East road loops from here to the lighthouse. |
| 14 | Beach | crescent x 82..125, y -25..80 | slopes into the sea | Umbrellas, and a hidden sewer hatch. |
| 15 | Lighthouse | promontory at (86,90) | base +4, tower 22 m | The slab on top is an objective. |
| 16 | Mountain and gate | y 92+ ; gate at (0,95) | pillars 20 m, mountain to 60 m | Waterfall gate, a locked cave at (-14,104), and a back terrace street at +3. |
| 17 | Offshore | NW islet (-125,55), east rock (140,30), south mini tower (10,-115) | — | Boat-hop secrets. |

## Objectives (first pass, built from our verbs)
1. **Bell top.** From the west wing towers, take the rope line onto the bell hall roof, then the ladder up
   the clock tower.
2. **Crate hop.** Climb the fruit crates (1.4 m) to the shop awnings (a 2.3 m jump), then up onto the bell hall roof.
3. **Canal run.** Drop onto the canal ledges and follow them to the waterfall grotto.
4. **Keep summit.** The east wing's roof NPC launches you to the keep's upper tower.
5. **Lighthouse slab.** Climb the east-quarter rooftop chain, then hammer the slab on top.
6. **Statue portal.** Clear the slime off the statue (blaster) and the portal opens.
7. **Boathouse dome.** Hop the moored boats to reach the dome roof.
8. **Twin tower** (late game). Break the walls into the west quarter's tower.
9. **Beach hatch.** Find it under the umbrella; it leads into the sewer maze under the plaza.
10. **NW islet.** Boat-hop out to it.
11. **Gate.** Unlocked last; it opens the mountain cave.
12. **Harbour.** Grind the basin railings on the skateboard in one run.

## Budget (standalone)
- 250k triangles and 150 draw calls for the whole level.
- The greybox is grey on purpose: we judge routes and silhouettes first, paint after.
