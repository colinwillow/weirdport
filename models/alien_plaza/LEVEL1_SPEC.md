# Level 1: Glowtide (the spec, in the blueprint template)

```
LEVEL 1   name: Glowtide   island: about 230 x 200 m (town about 160 x 135)   tech: Hover Pack (vault, after core 3)
TOPOLOGY: hub with spokes (Delfino Plaza). The spokes are hung on landmarks, plus a spiral finale (Bob-omb).
          ASCII diagram: see LEVELS.md and storyboards/board_00_levelmap.jpg
FANTASY:  a sunny alien harbour town whose beacon went dark. Bring its five cores home and climb the volcano out.
```

## Landmarks (all visible from the spawn)
| Id | Landmark | Height | Its job |
|---|---|---|---|
| L1 | Clock tower | 22 m | **Door** to core 2. The clock hands are the bell clue. |
| L2 | Gate and waterfall | 23 m | **Goal.** The beacon sockets are here, and so is the way into the vault. |
| L3 | Volcano | 81 m | **Goal.** The finale, seen from every outdoor spot. |
| L4 | Lighthouse | 23 m | **Door** to core 4. |
| L5 | The keep | 23 m | **Door** to core 5 and the hover teaser. |
| L6 | Boathouse dome | 11 m | **Door** to the fuel cell, and the start of glyph 2. |

**Vista points**
- The stage, where you spawn. In view: L1, L2, L3 and L5, with L4 and L6 at the edges.
- The bell room. It overlooks the whole plaza and the west quarter.
- The east tower before the hover gap. You see the lighthouse, the pylon and the beach.
- The summit. You see the open sea.

## Core routes
Every beat below is measured and proven by `route_check.py`, and `ROUTES.txt` has the full printout.

| Core | Verb family | Starts at | Arc (teach / develop / twist / payoff) | Shortcut home |
|---|---|---|---|---|
| 1 Market | fight | the stage (spawn) | three waves in the fenced plaza; the warrior last; the core rises from the fountain | (you're already in the hub) |
| 2 Bell | acrobatics + clue | west wing | ladder, 3 m jump, ladder, zipline, ladder; a roof patrol at the 9 m step; bells rung in the clock-hand order | zipline from the bell room to the plaza |
| 3 Canal | disguise + mechanism | goo nest | DNA from a nest guard, then the nest, the handle, the checkpoint, the sluice; the canal drains, the ledges lead to the vault, and the **Hover Pack** | the shrine's one-way door onto the gate terrace |
| 4 Lighthouse | tech (hover) | dome roof | ladder, then an 11.7 m hover, ladder, then a 10.4 m hover to the pylon, then a jump to the gallery; the generators get shot along the way | zipline from the lighthouse to the beach |
| 5 Keep | tech + favour | boathouse | crane cab, a 3.8 m hover lift, the dome steps, the fuel cell; carried to the launcher, who launches you | zipline from the keep to the promenade |
| Finale | climb + dodge | gate terrace | 5 sockets, the lift, a 238 m spiral at 21%, rolling goo boulders | the portal itself |

Each route brings in at most **one new idea**:
- core 2: the zipline
- core 3: the disguise, then carrying an item
- core 4: hover gaps
- core 5: the hover lift
- finale: boulders

## Gating table
| Gate | Blocks | Opened by | Seen before it opens? |
|---|---|---|---|
| Bell-room shutter | core 2 | the bells, in clock order | yes, from the spawn |
| Nest guards | the handle | the goo disguise | yes: the handle glows through the doorway |
| Harbour checkpoints | the sluice | the goo disguise | yes, from the canal quay |
| Canal water at -2.0 | the ledges and the vault | the sluice (handle, then 3 hammer hits) | yes: the ledges are visible under the water |
| 11.7 m and 10.4 m gaps | core 4 | Hover Pack | yes, from the dome roof |
| 3.8 m dome rim | the fuel cell | Hover Pack | yes, from the pier |
| Launcher | core 5 | the fuel cell | yes, from the plaza |
| Waterfall and vault door | the lift and the finale | the beacon (5 cores) | yes, the whole game |

## Secrets for later tech
| Secret | Where | Needs | Visible hint | Reward |
|---|---|---|---|---|
| Hover teaser | ledge on the keep's west face, 4.2 m | Hover Pack (this level) | the spore cache glows over the promenade | 20 spores |
| Glyph 1 | balcony on the twin tower, 3.8 m above its roof | Hover Pack, then hammer | the cracked wall, visible from the alley | a glyph |
| Glyph 2 | the north-west islet | Hover Pack across the boats | the islet's palm, seen from the boathouse | a glyph |
| Glyph 3 | under the beach hatch | Clancy (and a Grapple anchor in the sewer, level 2) | a dog digging by the amber umbrella | a glyph |

## Enemies (each has a reason)
| Enemy | Where | Reason | Count |
|---|---|---|---|
| Goo grunts, then a goo warrior | sunken plaza | teaches combat (core 1) | 6, then 8, then 4 + 1 |
| Roof patrol | west wing, 9 m roof | pressures the bell route's middle beat | 2 |
| Nest guards | goo nest door | the disguise source, and they gate the nest | 2 |
| Checkpoint guards | both harbour bridges | gate the sluice | 3 |
| Goo boulders | summit path | the finale's danger comes down the climb | 3 spawners |

## Pickups
66 breadcrumb spores laid by the checker along the intended routes: arcs over jumps, columns up
ladders, and a line up the summit path. A crate by the stage pays out in the first 30 s.

## Budget (measured at m450)
- **Draw calls:** about 26: 15 static materials plus 11 separate movers.
- **Triangles:** about 117,000.
- **Texture memory:** about 9 MB once the game bakes the textures to KTX2.
- **Download:** about 2 MB for the visual file.

## Checks
- Route checker: **0 problems**. Every target is reachable only with its intended tech, every
  intended leg is proven, every surface has headroom, and line of sight is tested against every wall.
- Storyboards: `storyboards/board_*.jpg`.
- Map: `board_00_levelmap.jpg`.
