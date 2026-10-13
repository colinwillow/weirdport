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

**The glider is one example of a whole family.** Every region has a technology its people own,
and the form that carries it is the key. The list is open-ended — these are the shape of it:

| Tech | Form | Opens |
|---|---|---|
| flight | hang-glider guy, a pilot | islands, rooftops, canyons |
| underwater | scuba diver | flooded areas, behind the waterfall |
| underground | cave miner (sees in the dark, digs) | caves, mines, the sewers |
| the farm | farmer | rural areas, machinery, animals |
| business | a CEO | the corporate tower — "Dump Tower" — boardrooms, executive lifts |
| machines | an engineer / hacker | controls robots and AI, turrets, doors |
| the law | cop, then military | cordons, the precinct, the base |
| the trades | construction worker, firefighter | rebuilding the way on, clearing fires |
| the street | hobo, activist, biker | stealth, crowds, gang turf |

**Juice: a disguise is a resource, not a costume.** Your DNA tool runs on juice. Transforming costs
it and holding a form drains it (roughly minutes, not seconds — tunable). When it runs out you
snap back to the alien wherever you are. Juice is earned by doing things in the world (small tasks,
helping people, beating Skinsuits) and the tank's size grows as you progress. Taking a sample
unlocks a form permanently; *wearing* it costs juice.

**The rule that comes with juice: no one-way trips.** If you can glide to an island, the juice can
run out on the island. So every place a form can take you must have a way back for the alien.
**Portals** are the general answer: reaching certain spots (a checkpoint, a hidden-alien safe house,
the top of a climb) activates a portal there, and from then on you can travel between any activated
portals as yourself — back to the mainland, or back to your ship. A place a form opened once is a
place the alien can return to. Some portals are one-way out (an escape hatch); the important ones
are two-way. The ship is the hub portal.

Each region's lock is a kind of obstacle (a fire wall, a police cordon, a broken bridge, a
barricade, a gap) and each needs a particular form. Forms stack: once you have one, it is in your
form wheel for good.

## Who's out there

**UFO lore, our spin:** `LORE.md` turns real UFO and paranormal folklore into systems: the orbs as the
aliens' control grid (shoot one down and people fall out of the trance), electromagnetic effects as
the tell, crop circles, tractor beams, missing time, Men in Black, implants and more.


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

**The map is a central metropolis hub with the regions around it** (see the top of `REGIONS.md`):
you cure the outer regions one by one, each opens more of the metropolis, and its core is the last
stop before the Mothership.

**The full region bible is `REGIONS.md`**: each region's shape, light, people, problem, tech, signature
system and the journey into it, plus the checklist that keeps any two regions from feeling alike.
It supersedes the short list above where they differ.

## The world: dense, vertical, organic, alive

**The visual identity is the selling point**: beautifully painted scenes, weirdness, an organic
mess that is compelling to look at. What it must NOT be is what the skate game's auto-built worlds
turned into: flat, spaced out, rectangular areas sat next to each other on a grid, with no height
and nothing between them.

**Rules for every place built, by the loop or in Blender:**
- **Intimate, not spaced out.** Streets are narrow, things are close to the camera, you are always
  within a few metres of something to look at or touch. Empty ground between "areas" is a failure.
- **Vertical, always.** Every place has layers: street, stoops and kerbs, balconies, fire escapes,
  rooftops, bridges and walkways over the street, stairs down to cellars, canals, sewers below.
  Places stack and overlap; you can go over and under the same spot.
- **Organic, not a grid.** Streets bend, buildings lean and crowd each other, nothing is
  axis-aligned for its own sake, and districts bleed into each other rather than sitting side by side
  with a border between them.
- **Everything is interactive.** Things break, get used, get fixed. If it is on screen, ask what
  happens when you hit it, climb it, or burn it.
- **One place at a time, finished.** Build one block, one plaza, one alley properly — the look, the
  height, the people, the systems in it — before starting the next. A small finished corner beats a
  big empty scaffold every time.

**The city is a living system, and disturbing one part ripples into others.** The people each do a
job, and the jobs depend on each other:
- buildings break (fights, fires, aliens, you); **construction crews** walk out and rebuild them;
- **firefighters** put out fires before they spread to the next building;
- **cops** respond to violence; protests and brawls pull them off their beats;
- a **strike or a protest** takes the workers off the job, so damage stops getting fixed and the
  district slides toward broken and abandoned: boarded windows, rubble, the homeless move in, the
  Skinsuits move in after them;
- end the strike (persuade the organiser, expose the infiltrator) and the crews pour back out and
  the district rebuilds in front of you.

Each district has a **health** that these systems push up and down, and the look follows it —
healthy, worn, broken, abandoned. Unforeseen outcomes are the point: the player pulls one thread
and watches what else moves.

## Turf: the city is up for grabs (idea, Colin, not yet scheduled first)

A self-sustaining city whose LOOK and LIFE follow whoever holds each block. Every block carries an
**influence share** for each faction:
- the activists / hippies;
- the rednecks / bikers;
- big business (Dump Tower money);
- small business (food carts, corner shops);
- the homeless;
- Uplift's robots;
- the Skinsuit aliens.

**What influence changes, cheapest first:**
1. **Who walks there.** The crowd mix follows the shares.
2. **Dressing on the buildings that are already there.** Flags, banners and graffiti; boarded
   windows; neon, gold trim and corporate signs; solar panels and gardens; scrap and chain-link;
   alien growth crawling up the walls.
3. **The buildings themselves.** Procedurally generated from the kit pieces in each faction's
   style: rundown walk-ups, a glass tower, a trailer lot, a co-op with a roof garden, a factory,
   alien pods. Swapped in as a block changes hands.

**What moves influence:** protests and rallies (the crowd system), Skinsuit conversions and Uplift
conversions, crews rebuilding or not (district health), and you — who you help, who you knock down,
whose strike you end, whose leader you expose.

**Choose your destiny.** You are always the alien, but which way you tilt the city is yours: back the
activists, the business owners, the rednecks, or let it go to the robots or the aliens. The city's
end state, and maybe the ending, reflects who holds it. Factions push against each other at their
borders (turf flashpoints: a rally marching into protest territory, a developer bulldozing a camp),
so the map keeps moving even when you don't. Think GTA San Andreas turf wars or SimCity, with the
main plot running through it: the aliens are trying to win the map too.

**It sits on systems the roadmap already builds**: district health (C0), protests (C1), Skinsuit
incursions (C2), Uplift (C3), the kit buildings and their generator.

## World building split

**Blender is for the real worlds** (textures, breakable buildings). The loop builds **greybox
regions** — but a greybox is still dense, layered and vertical by the rules above, never a flat
plane with boxes on it — out of the kit pieces and procedural geometry so every mechanic can be played now, and
each greybox is meant to be swapped for a Blender region later. A greybox region has: its bounds
(for the fog), its gates, its quest NPCs, and its spawn points — all data, so the swap is a file
change.

**`CHARACTERS.md` is the character plan**: the shared skeleton with blend shapes and texture sets,
the everyday animation library he needs to author, smart objects (benches, café tables, bus stops)
that NPCs use, and the full roster with what stands in for each role until its model exists.

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
- Juice: how long a form lasts, and does each form drain at its own rate (flight costs more)?
- Do sampling methods differ per character (some need a stun, some a task, some a disguise first)?
