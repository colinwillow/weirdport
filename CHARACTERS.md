# Weirdport — characters, the shared rig, and the animation library

## Where this is going: one body, many people

Eventually every human-shaped character is **one skeleton** with:
- **blend shapes** for body shape (thin, fat, tall, short, the alien, the ballerina, the worker…);
- **texture sets** for skin, clothes and faces;
- **one shared animation library** that every character draws from, plus a few custom clips per
  character for what makes them them.

That makes transformation natural: turning a ballerina into an alien, an alien into a worker or a
homeless man into a worker is a blend between two sets of shape weights and two texture sets on the
same skeleton, not a swap between two models. It also ends retargeting: every clip already fits
every body.

**How the game will use it (for the loop, when the rig lands):**
- A character is a **recipe**: shape weights + texture set + which clips from the library it uses
  + its custom clips. Adding a character is a line, not a model.
- The DNA morph (`MORPH`, `npm run morph`) is already heading this way: it moves shapes onto zap's
  topology. The shared rig replaces that with authored blend shapes.
- **Phone cost to watch:** many blend shapes on one mesh means per-vertex morph work for every body
  on screen. Bake a character's fixed shape once at spawn and only keep live morphing for the one
  that is transforming.
- **Until the rig exists, the current per-character files keep working.** Nothing waits on it.

## The animation library — what we have, what we need

Today's clips are mostly locomotion, combat, hit reactions and a few idles. An everyday city needs
everyday actions. **Colin authors these**; until each lands, the game stands in an idle and names
the missing clip in the chip, so the moment it exists it plays.

| Group | Clips needed | Have now |
|---|---|---|
| **Sitting** | sit down / sit idle / stand up — chair, bench, kerb, stool; sit and eat; sit and drink coffee; sit and read a paper; sit on the ground | none |
| **Waiting** | wait at a bus stop, check watch, check phone, lean on a wall, smoke (the hick has a cigarette joint) | phone/lean: none |
| **Social** | wave, talk with gestures, laugh, argue, point, shrug, handshake, hug, high five, nod / shake head | wave (Colin only) |
| **Work** | hammer, sweep, carry a box, push a cart, cook at a grill / food cart, serve, type at a desk, mop, dig, paint a wall | worker's repair swings |
| **Shop & door** | open a door and walk through, browse a shelf, pay at a counter, knock | none |
| **Climbing** | climb a ladder (have for zap), climb a fence, vault a low wall, step up onto a ledge | ladder (zap) |
| **Protest & rally** | hold a sign up, chant with a fist pump, march, cheer, clap, boo, throw something | none |
| **Fear** | cower, hands up / surrender, scream and point, hide behind something | flee run (some) |
| **Police** | arrest / cuff, frisk, radio in, wave traffic on, aim and hold | aim/shoot (officer) |
| **Trance (orbs)** | stand dazed, slow trance walk, wake up confused | none |
| **Farm** | feed animals, pitchfork hay, drive a tractor (seated), chase a cow | none |
| **Animals** | cow idle / graze / walk / stampede / lifted in a beam | none (cows are stand-ins) |

**Smart objects make these clips useful.** Benches, café tables, bus stops, food carts, counters and
doors should carry **use spots**: where to stand or sit, which way to face, which clip to play. NPCs
pick a spot near them, walk to it, use it for a while and leave. That is most of what makes a
street look alive, and it works with stand-in idles before the clips exist.

## The roster — who the game needs, and what stands in

Placeholders let the game be built against **roles**, not models. A placeholder is an existing body
with a tint, a prop and a name tag, tagged with the role it stands in for. When the real model
lands, it's one line in the roster.

| Role | Where | Stand-in now | Status |
|---|---|---|---|
| Zap (you) | everywhere | zap.glb | have |
| Clancy | everywhere | clancy.glb | have |
| Farmer + family | Gristle Farm | hick_skinny | stand-in |
| Farmhands | Gristle Farm | hobo_01 tinted | stand-in |
| Homeless | Old Town, Underneath | hobo_01 | have |
| Construction worker | Old Town | contruction_worker.glb | have |
| Firefighter | Old Town | firefighter.glb | have |
| Cop | everywhere | dummy_officer.glb | have |
| Food-cart chef (hidden good alien) | Old Town | hipster tinted | needs model |
| Mail carrier | Old Town | biker tinted | needs model |
| Mechanic | Old Town, Hollow Creek | worker tinted | needs model |
| Activists, artists, baristas | The Pearl | fat_activist, fat_hippie, fat_hipster | have |
| Protest organiser (boss) | The Pearl | fat_activist | needs model |
| Rednecks, bikers | Hollow Creek | hick_skinny, fat_biker_01/02 | have |
| Rally leader (boss) | Hollow Creek | fat_trump | have |
| Dock workers, cyborgs | Waterfront | worker tinted | needs model |
| Security robots | Waterfront | none | needs model |
| Executives, assistants, security | Dump Tower | secret_service, beautiful_blonde/asian | partly |
| CEO (boss) | Dump Tower | fat_trump | needs model |
| Scuba diver | The Gorge | none | needs model |
| Fishers, river guides | The Gorge | hick tinted | needs model |
| Hang-glider guy | River Islands | jack | needs model |
| Skaters, kite surfers | River Islands | moussa, colin | have |
| Rollergirl (Easter egg) | River Islands | alien_rollerskate_blue | have |
| Cave miner | The Underneath | worker tinted | needs model |
| Engineer / hacker | Waterfront | hipster tinted | needs model |
| Military | high heat | officer tinted | needs model |
| Skinsuit versions of civilians | everywhere | alien_warrior | needs models |
| Cyborg versions of workers | Waterfront | worker tinted | needs models |
| Evil alien grunts | everywhere | alien_warrior | have |
| Cows | Gristle Farm | box stand-ins | needs model |
