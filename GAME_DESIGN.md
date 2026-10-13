# Weirdport — game design

Living document. **He owns it**; the loop reads it and builds toward it. Change anything here and
the next build follows the change. `ROADMAP.md` is the ordered work list that comes out of it.

## The pitch

You are a good alien stranded on Earth, in Weirdport — a weird, Portland-ish city full of oddball
characters. Evil aliens are quietly taking it over, and **they are doing it by feeding the culture
war**: they infiltrate both sides, stoke every fight, and every escalation makes people easier to
turn. You keep Weirdport weird and in one piece.

It plays like **Zelda's structure with a little GTA**: an open city, but regions are fogged and
locked until you earn your way in; people tell you where to go next; and the keys that open the
world are **the people you can become**.

## The core mechanic: forms are keys

Anyone who sees you as an alien is scared of you — they scream, run, and call the cops. Disguised
as one of them, nobody looks twice. So taking someone's DNA is both **stealth** (who will let you
pass) and **traversal** (what that body can do).

**Getting a sample (the real way):** knock someone down (blaster, melee, a thrown body), then get to
them while they are down and take the sample. The DNA gun stays as a debug shortcut only.

| Form | Gets you past | Gets you in with |
|---|---|---|
| **You (Zap)** | blaster, roll, ledge grab | nobody — everyone runs |
| **Farmer / hick** | the bridge checkpoint into town (tutorial) | rural folk |
| **Hobo** | nobody looks at him: stealth past guards | homeless camps, the sewers |
| **Construction worker** | rebuilds broken bridges, ladders, scaffolds | building sites |
| **Firefighter** | puts out fires blocking streets; truck ladder | the fire station |
| **Cop** | walks through police cordons; can arrest | the precinct |
| **Activist (blue hair)** | marches through barricades inside a protest | the movement |
| **Biker / redneck** | the motorcycle and trucks; gang turf | the Outskirts |
| **Hang-glider guy** (human) | the glider / wingsuit: gaps, islands, rooftops | BASE jumpers |
| **Clancy** (always with you) | sniffs out hidden things, fits through small gaps | — |

Each region's lock is a kind of obstacle (a fire wall, a police cordon, a broken bridge, a
barricade, a gap) and each needs a particular form. Forms stack: once you have one, it is in your
form wheel for good.

## Who's out there

**The culture war (the sub-plot that fills the streets).** Blue-hair activists, protesters with
signs and performance art on one side; rednecks, hillbillies, bikers and rally-goers on the other.
They argue, march, and brawl. Neither side is the villain — the aliens are, and both sides are
being played. Satire lands on everybody equally.

**The working city.** Construction workers fix what breaks, firefighters put out fires, cops
respond to violence (heat that escalates — cops, then more cops, then the military), plus the
homeless, mail carriers, chefs, mechanics.

**The enemies.**
1. **Skinsuits** — evil aliens wearing people. Hit someone with their ray and they burst out of
   their skin as an alien version of themselves (the virus gun already does this). You can beat
   them down and turn them back.
2. **Uplift Corp** — turns working people into cyborg versions of themselves.
3. **A third race, maybe neutral** — undecided. Could sell things.

**The hidden good aliens.** Men-in-Black style: they live among people in disguise — a food-cart
owner, a shopkeeper — with a tell (an antenna under a hat). They give tips, upgrades, and the next
lead. Rollergirl is an **Easter egg** for now (one of these, maybe), not a story pillar.

## Chapters (draft)

0. **The Crash — farmland.** You crash in a field with cows. Clancy is in the wreck. A farmer sees
   you and panics. Tutorial: move, knock down, **take his sample**, become the farmer, walk through
   the police checkpoint on the bridge into town. (This teaches the whole game in ten minutes.)
1. **Old Town** (the kit city — destructible buildings). Homeless camps, food carts, building
   sites. A crew of construction workers is being turned into Skinsuits. Get the worker form,
   rebuild the way on, beat the infiltrated foreman.
2. **The Pearl** — hipsters, the protest movement. Boss: the infiltrated organizer.
3. **The Outskirts** — rednecks, bikers, the rally. Boss: the infiltrated rally leader.
4. **The Waterfront** — Uplift Corp's cyborg factory.
5. **The Skate Islands** — the hang glider / wingsuit, rooftops and islands.
6. **The Mothership** — the finale.

Regions are fogged on the map until you get there; arriving clears the fog.

## World building split

**Blender is for the real worlds** (textures, breakable buildings). The loop builds **greybox
regions** out of the kit pieces and procedural geometry so every mechanic can be played now, and
each greybox is meant to be swapped for a Blender region later. A greybox region has: its bounds
(for the fog), its gates, its quest NPCs, and its spawn points — all data, so the swap is a file
change.

## Characters still needed (for him to make, eventually — none of this blocks the loop)

- **Skinsuit** and **Cyborg** versions of each base civilian (the warrior exists already).
- **One boss per chapter.**
- **Quest-givers:** food-cart chef, mail carrier, mechanic, farmer (hick stands in), the hidden
  good alien shopkeeper.
- **The hang-glider guy** and a glider/wingsuit prop.
- **Military** (for top-level heat).
- **Cows** (and other farm animals) for Chapter 0.

Existing characters stand in for all of these until they arrive.

## Open questions (his call)

- Is the third alien race neutral, a merchant, or another enemy?
- Does Rollergirl stay an Easter egg, become a hidden good alien, or go?
- Death / failure: what happens at zero health? (Right now nothing.)
- Can you also turn **Skinsuits** back with the sampler, or is that a separate tool?
