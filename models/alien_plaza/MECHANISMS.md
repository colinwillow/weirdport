# Mechanisms: the parts a level is built from

A level is an escape room the size of a town. Every place you want to reach is locked by something, and the key is somewhere you can already get to. Chain enough of those and you have a level. Design is picking parts from this catalogue and wiring them so each one unlocks the next, with the goal always in view.

## The rule for every part

Every mechanism has four things, or it is not finished:
- **What it gates.** The place or thing you cannot reach until it runs.
- **What starts it.** A lever, a button, a carried item, a fuel cell, a fight, a skill move.
- **What it tests.** One skill: a jump, a timing, a climb, a fight, a disguise, an item carry.
- **The tell.** You can SEE it before you solve it: the dead conveyor, the unlit portal, the rail pointing the wrong way.

## The catalogue

**Power and motion**
- **Lever on a motor.** Up high, hard to reach. Throw it and the motor runs. Gates: anything the motor drives. Tell: a still belt, a dark lamp.
- **Conveyor belt.** Dead until powered, then runs back and forth. You ride it across a gap. Tell: the belt and the gap, visible from below.
- **Elevator button.** A button at the bottom calls a lift that was parked at the top. Gates: the upper floor, for everyone after you. Tell: the lift, up there, with its shaft.
- **Crane.** A hook you ride, or a load you swing onto a roof. Starts with a cab button or a fuel cell. Tell: the hook hanging over the spot you want.
- **Pulley that turns a grind rail.** The rail is there but aims at the wrong ledge. Crank the pulley and it swings 90 or 180 degrees. Tell: a rail that visibly ends in nothing.
- **Gondola.** A cable car between two towers. Starts when both stations have power. Tell: the cable, and the car parked at the far end.

**Water and air**
- **Geyser.** Shoots you to a spot you could not jump to. Starts on a timer, or when you plug a leak elsewhere. Tell: the vent, steaming.
- **Sluice.** Drains or fills a canal, revealing ledges or floating a boat. Starts with a handle you carry. Tell: ledges visible under the water. (Glowtide has this one.)
- **Fan or updraft.** Lifts a hover across a gap it could not make alone. Starts with power.

**Doors and gates**
- **Locked tower door.** Opens with a key, a code (the clock hands), or an item. Tell: the door, with its symbol.
- **Shutter.** Rolls up when a sequence is completed (the bells in order). Tell: the shutter, half-lit.
- **Checkpoint guard.** Lets you through only in disguise. Tell: the guard, and someone else walking through.
- **One-way door.** Opens from inside, then stays open: a shortcut home. Tell: the door from outside, with no handle.

**Portals and checkpoints**
- **Dead portal.** Two posts, dark. Reach it once and it lights; from then on you can jump back to it from any lit portal. Tell: the posts, seen from far away. This is the game's checkpoint and its fast travel, and it fits the alien story.

**Skill challenges (no mechanism, the body is the key)**
- **Chimney wall-jump.** Two close parallel walls, bounce up between them. A button at the top opens the easy way for next time.
- **Balance beam.** Narrow, over a drop. Slow is the trick.
- **Monkey bars.** Hang and swing. Tests the grab.
- **Crouch hole.** A gap in a wall down a nothing alley. The side-quest entrance.
- **Timed platforms.** Appear and vanish on a beat.

**Rewards**
- **The main prize** of a route: a core, a ship piece, a moon. Whatever the world counts.
- **The side prize** at the end of a crouch hole, a beam, and monkey bars: a power, a life, a shell piece, spores.

## How the pieces chain

Write a route as a sentence of parts: "To get the core you need the lift; the lift needs the button; the button is at the top of the chimney; the chimney is behind the checkpoint; the checkpoint needs the disguise; the disguise comes from the nest guards." Six parts, one core. Then draw it as a graph. If a part gates nothing, cut it. If a part is gated by nothing, it is the start.

Glowtide's routes in this language:
- **Core 2:** ladders and a jump → rooftop → grind rail → lift → bells in clock order → shutter → core.
- **Core 3:** disguise from the nest guards → nest → sluice handle → checkpoint guards → sluice wheel → canal drains → ledges → vault → Hover Pack → core.
- **Core 4:** ladder → hover gap → ladder → hover gap → pylon → gallery; generators shot on the way → lamp → core.
- **Core 5:** crane cab → hover lift → dome → fuel cell → carried to the launcher → launched to the keep → core.
- **Finale:** five cores → beacon → waterfall opens → lift → spiral path with boulders → portal.

What Glowtide is missing from the catalogue: a conveyor, a geyser, a gondola, a pulley-turned rail, a chimney wall-jump, a crouch hole with a balance beam and monkey bars, and lit portals as checkpoints. Those are the next refinements, and each is one build.

## The world structure

Every world has about five missions. Each mission pays one piece: a ship piece, a moon, whatever the game counts. The next world opens at a count (ten pieces, say), not on finishing everything, so a hard mission can be skipped and come back to. Side prizes count too, in smaller change. This is how Sunshine and Odyssey do it, and it is why those games never feel stuck: there is always another door you could try.

## The disguise world (the game's spine)

Evil aliens are taking over Earth. You are a good alien who crashed. People run from you; cops and the military shoot you on sight, because you are an alien. So you hide, and you disguise, and slowly you earn trust.

**Disguises are a vocabulary, not one trick:**
- **A person.** The DNA gun. Nobody reacts; guards wave you through.
- **A wheelie bin.** Jump into one of the big plastic bins on the street and you ARE the bin: you trundle along at walking pace, low, and press jump to pop out. Cops ignore a bin. Blue, orange, green, black; graffiti on most of them. Bins are placed where a route needs a quiet way past a watcher. (Glowtide has twelve as of m460: `hide_bin_NN` markers, kind `hide_bin`, with a colour.)
- **Other objects later:** a mailbox, a hydrant, a planter, a crate on the dock. Each one a level's joke.

**The trust meter.** A per-world number. It rises when you do good in front of people (save someone, fix something, beat the evil aliens where they can see). Low trust: everyone runs, cops shoot, you live in bins and borrowed faces. Middle: civilians stare but stay, cops warn first. High: you walk the street as yourself, and the propaganda billboards flip from fear to welcome. The meter is the long arc of the whole game, and each world moves it a notch.

**Propaganda and the retro-future dressing.** Giant screens and billboards with alien faces: FEAR THEM at first, then, as trust rises, the same frames carry WELCOME. Retro TV sets in shop windows playing the news. Roswell posters, UFO diner signs, a flying saucer as the lost ship. Men in black in black sedans, and it is never quite clear which agency is on your side: one of them helps, one of them hunts. Powers that fit the fiction and the catalogue above: telepathy (read a guard's patrol), psychokinesis (move the crate, throw the bin), mind control (a guard opens his own gate), hoverboards and the saucer itself as late tech. Each one is a world's unlock and a mechanism's key.

## Hypnosis (a mechanism AND a disguise, written down for later)

A pendulum, a pair of glasses, a gadget held up to the eyes: do it in front of an NPC and his eyes go swirly. He is yours. A hypnotised NPC:
- **follows you**, at walking pace, and stops when you stop;
- **takes one command** at a time: wait here, go there, press that, attack that alien;
- **is a tool for puzzles**, which is the point: the button is at the bottom and you are at the top and the drop would kill you, so you send him; the beam is too narrow for your run but not for his walk; the plate needs a body on it while you go through the door; two levers must be thrown together.
- **can be thrown**, because he is a ragdoll: launch him onto the button.
- **wears off** on a timer, or when he is hit, with a shake of the head. Swirly eyes are the tell, and so is a little spiral over his head so you can see it from the roof.

It stacks with the trust meter: hypnotising people in front of others LOWERS trust (they saw you do it). Using it on an evil alien's guard does not. So it is a temptation with a price, which is the kind of choice the game wants.

Catalogue entries it unlocks: a button out of reach, a pressure plate, paired levers, a guard who opens his own gate, a door you cannot fit through. Level 3 or 4 tech, after the Hover Pack and before the saucer.

## Security cameras (an alarm with a tell)

A box camera on a bracket under a cornice, like the one on SW 17th. It sweeps slowly left and right. Its field of view is DRAWN: a faint cone of light on the ground (a spotlight at night, a translucent wedge by day), so you always know whether you are about to be seen. When it catches you it LURCHES: a little animated jolt, a red light, a sound, and then the alert: two guards run to the spot. You hide (a bin, a doorway), disguise (a borrowed face walks right past it), fight, or shoot the camera out (it sparks, hangs dead, and the cone goes out). A disguise fools it; a bin fools it; the alien does not.

Data per camera (`cam_NN` markers in the level JSON, kind `security_cam`): position, mount yaw, sweep half-angle and period, field of view, range, what it alerts (the nearest `npc_guard_*` pair), and `shootable: true`. Glowtide has six: the nest door, both harbour checkpoints, the keep gate, the boathouse pier and the lighthouse stair. Each one covers a route beat where the disguise is the intended answer, so the camera is the thing that makes the disguise matter.
