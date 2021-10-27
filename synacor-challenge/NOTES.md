# NOTES

2317 Foothills (tablet)

- south 2322
- doorway 2327

2322 Foothills

- north 2317

2327 Dark cave

- north 2332
- south 2317

2332 Dark cave

- south 2327?
- bridge

2342 Rope bridge

- continue 2347
- back 2332

2347 Falling through air

- down 2352

2352 Moss cavern

- west 2362
- east 2357

2357 Moss cavern (empty lantern)

- west 2352

2362 Moss cavern

- east 2352
- passage 2367

2367 Passage

- cavern 2362
- ladder 2377
- darkness 2372

2372 Passage (with lantern)

- continue 2427
- back

2377 Twisty passages

- ladder 2367
- north 2382
- south 2387
- east 2392
- west 2397

2382 Twisty passages

- north 2387
- south 2377
- west 2382

2387 Twisty passages

- north 2377
- south 2382
- east 2387

2382 Twisty passages

- north 2387
- south 2377
- west 2382

2392 Twisty passages

- north 2407
- south 2392
- west 2377
- east (grue?)

2397 Twisty passages

- north 2397
- south 2402
- east 2377

2402 Twisty passages

- north 2417
- south 2382
- west 2387
- east (grue?) 2468

2407 Twisty passages

- north 2387
- east
- south

2417 Twisty passages YcahtzqKsHvp (can)

- west 2377

2427 Dark passage

- west 2432
- east 2372

2432 Dark Passage

- east
- west 2437

2432 Dark Passage

- east
- west 2442

2442 Dark Passage

- east
- west 2447

2447 Ruins

- east
- north 2452

2452 Ruins (red coin)

- north
- south

2457 ruins (sum)
_ + _ * _^2 + _^3 - _ = 399

- north 2463 (locked door - use blue, red, shiny, concave, corroded in order)
- south
- east 2468
- west 2478

2463 ruins (teleporter)

- south
  (use teleporter -- 2488 -- ILaryZuJANwv)

2468 Ruins (concave coin)

- down 2473
- west 2457

2473 ruins (corroded coin)

- up 2468

2478 ruins (blue coin)

- up 2483
- east 2457

2483 - ruins (shiny coin)

- down 2478

2488 synacor headquarters(business card and strage book)

- outside 2493

2493 synacor headquarters

- inside 2488

2468 Fumbling around in the darkness

- forward
- back 2653

2653 Fumbling around in the darkness

- run
- investigate

2658 Panicked and lost

- run -> EATEN BY GRUE
- wait
- hide

The cover of this book subtly swirls with colors. It is titled "A Brief Introduction to Interdimensional Physics". It
reads:

Recent advances in interdimensional physics have produced fascinating predictions about the fundamentals of our
universe!  For example, interdimensional physics seems to predict that the universe is, at its root, a purely
mathematical construct, and that all events are caused by the interactions between eight pockets of energy called "
registers". Furthermore, it seems that while the lower registers primarily control mundane things like sound and light,
the highest register (the so-called "eighth register") is used to control interdimensional events such as teleportation.

A hypothetical such teleportation device would need to have have exactly two destinations. One destination would be used
when the eighth register is at its minimum energy level - this would be the default operation assuming the user has no
way to control the eighth register. In this situation, the teleporter should send the user to a preconfigured safe
location as a default.

The second destination, however, is predicted to require a very specific energy level in the eighth register. The
teleporter must take great care to confirm that this energy level is exactly correct before teleporting its user!
If it is even slightly off, the user would (probably) arrive at the correct location, but would briefly experience
anomalies in the fabric of reality itself - this is, of course, not recommended. Any teleporter would need to test the
energy level in the eighth register and abort teleportation if it is not exactly correct.

This required precision implies that the confirmation mechanism would be very computationally expensive. While this
would likely not be an issue for large- scale teleporters, a hypothetical hand-held teleporter would take billions of
years to compute the result and confirm that the eighth register is correct.

If you find yourself trapped in an alternate dimension with nothing but a hand-held teleporter, you will need to extract
the confirmation algorithm, reimplement it on more powerful hardware, and optimize it. This should, at the very least,
allow you to determine the value of the eighth register which would have been accepted by the teleporter's confirmation
mechanism.

Then, set the eighth register to this value, activate the teleporter, and bypass the confirmation mechanism. If the
eighth register is set correctly, no anomalies should be experienced, but beware - if it is set incorrectly, the
now-bypassed confirmation mechanism will not protect you!

Of course, since teleportation is impossible, this is all totally ridiculous.

The relevant bit of code:

# the condition

5483 set ['r0', 4]
5486 set ['r1', 1]
5489 call [6027]
5491 eq ['r1', 'r0', 6]
5495 jf ['r1', 5579]

6027 jt ['r0', 6035]        if r0 != 0 goto 6035 6030 add ['r0', 'r1', 1]    r0 = r1 + 1 6034 ret []            return

6035 jt ['r1', 6048]        if r1 != 0 goto 6048 6038 add ['r0', 'r0', 32767]    r0 = r0 - 1 6042 set ['r1', 'r7']
r1 = r7 6045 call [6027]        jsr 6027 # recursive 6047 ret []            return

6048 push ['r0']        push r0 6050 add ['r1', 'r1', 32767]    r1-- 6054 call [6027]        jsr 6027 # recursive 6056
set ['r1', 'r0']           r1 = r0 6059 pop ['r0']            pop r0 6061 add ['r0', 'r0', 32767]    r0-- 6065
call [6027]        jsr 6027 # recursive 6067 ret []            return

Optimize this by memoizing the subroutine @6027 (r0 and r1 are parameters and output values)
Then brute force values of r7 to find the output 6. (r7 = 25734 for me)

2498 Beach

- west 2503
- east 2508
- north 2513

2503 Beach

- east 2498
- north 2513

2508 Beach

- west 2498
- north 2518

2513 Tropical island

- north 2523
- east 2518
- south 2498

2518 Tropical island

- north 2523
- south 2508
- west 2513

2523 Tropical island

- north 2528
- south 2513

2528 Tropical island

- north 2533
- south 2523

2533 Tropical Island

- north 2538
- south

2538 Tropical Cave

- north 2543
- south

2543 Tropical Cave

- north 2548
- south

2548 Tropical Cave

- north
- south
- east 2553

2553 Tropical Cave Alcove (journal)

- west 2548

2558 Tropical Cave

- north 2623
- south

2623 Vault Antechamber (orb) #22

- north 2603
- east 2628
- south 2558 (leave grid)

See maze.py to solve route through the grid

2603 Vault Lock +

- north 2583
- east
- south

2583 Vault Lock 4

- north 2563
- east 2583
- south

2563 Vault Lock *

- east 2568
- south

2568 Vault Lock 8

- east 2573
- south
- west

2573 Vault Lock -

- east 2578
- south
- west

2578 Vault Door #30 (hourglass) 1

- south 2598
- west
- vault

2598 Vault Lock *

- north
- south 2618
- west 2593

2593 Vault Lock 11

- north
- east 2598
- south
- west 2588

2588 Vault Lock *

- north
- east
- south 2608
- west 2583

2608 Vault Lock 4

- north
- east 2613
- south 2628
- west

2613 Vault Lock -

- north
- east 2618
- south
- west

2618 Vault Lock 18

- north 2598
- south 2638
- west 2613

2638 Vault Lock *

- north 2618
- west 2633

2633 Vault Lock 9

- north 2613
- east 2638
- west 2628

2628 Vault Lock -

- north 2608
- east 2633
- west 2623

In the mirror, reverse the writing including the characters.