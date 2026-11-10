# 2079. Watering Plants

You want to water `n` plants in your garden with a watering can. The
plants are arranged in a row and are labeled from `0` to `n - 1` from
left to right where the `i`-th plant is located at `x = i`. There is a
river at `x = -1` that you can refill your watering can at.

Each plant needs a specific amount of water. You will water the plants
in the following way:

- Water the plants in order from left to right.
- After watering the current plant, if you do not have enough water to
  completely water the next plant, return to the river to fully refill
  the watering can.
- You cannot refill the watering can early.

You are initially at the river (i.e., `x = -1`). It takes one step to
move one unit on the x-axis.

Given a 0-indexed integer array `plants` of `n` integers, where
`plants[i]` is the amount of water the `i`-th plant needs, and an
integer `capacity` representing the watering can capacity, return the
number of steps needed to water all the plants.

```
plants = [2,2,3,3], capacity = 5        ->  14
plants = [1,1,1,4,2,3], capacity = 4    ->  30
plants = [7,7,7,7,7,7,7], capacity = 8  ->  49
```

**Constraints:** `n == plants.length`; `1 <= n <= 1000`; `1 <=
plants[i] <= 10^6`; `max(plants[i]) <= capacity <= 10^9`.

One step reaches each plant from the one before, `n` in all. A plant `i`
the can no longer covers sends the gardener from plant `i - 1` back to
the river and out again, `i` steps each way, and the can is full when
they arrive: `2 · i` more. One walk down the row adds them up, O(n). The
approaches differ in how they keep the walk's state and count it.

## Approaches

| file | mechanism |
|---|---|
| `water.kara` ★ | a `for` over `iter().enumerate()`, the water left and the steps in two `let mut`s: one step a plant, `2 · i` for a refill. O(n) |
| `water_walk.kara` | the walk itself: the gardener's place moved one unit at a time with `while` loops back to the river and out, every unit a step. O(steps), up to about n² |
| `water_fold.kara` | one `fold` over the plants with their places, carrying `(steps, water left)` as a tuple. O(n) |
| `water_trips.kara` | by trips: the row cut into the runs one can covers, the walks back `2 · start` for every run but the first, plus `n`. O(n) |
| `water_struct.kara` | a `struct Gardener` of place, can and steps, with `walk_to(place)` adding the distance and `water(place, need)` going to the river first when the can falls short. O(n) |
| `water_solution.kara` | LeetCode's Rust template (`Vec<i32>`, `for (i, &need) in plants.iter().enumerate()`, `(2 * i + 1) as i32`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each garden and its steps; then the sum and a checksum of the
steps for 2000 random gardens of 1 to 100 plants, the can holding 1 to
50; then the steps for the constraints' largest, 1000 plants of up to
`10^6` and a can of `10^6`. `water.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the places the gardener stands, in order, the river first,
then each plant, with a visit to the river put before any plant the can
cannot cover, and the steps the sum of the distances from each place to
the next. It checks 300 random gardens of 1 to 12 plants, the can
holding 1 to 10; then 20 whose every plant wants the full can, and 20
whose can holds the whole row. All 340 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the steps are the statement read literally |
| P2 | every plant's want and the can three times as big give the same steps |
| P3 | the steps are at least `n`, at most `n²`, and the steps less `n` an even number |
| P4 | a can that holds the whole row walks `n` steps, and plants each wanting the full can walk `n²` |
| P5 | one more plant, wanting what the middle plant wants, adds one step or `2n + 1` |
| P6 | each arm agrees with at least three of the other five |

A bigger can is not a property: it can cost steps. With `plants =
[7,4,2,8,1,7,7,1]` a can of 8 takes 36 steps and a can of 9 takes 38,
as the larger can puts off a refill to a plant further from the river.

The differential prints `340 gardens: checksum 941388594, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal steps was checked against a Python reading of the same
gardens. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the refill added to what was left | P1 159, P6 159 |
| M2 | ★: the first step not counted | P1 340, P3 340, P4 340, P6 340 |
| M3 | ★: the can holding one less after a refill | P1 109, P6 109 |
| M4 | walk: the walk back stopping at the first plant | P1 274, P4 311, P5 243, P6 274 |
| M5 | walk: the walk out stopping a plant short | P1 274, P3 274, P4 311, P5 266, P6 274 |
| M6 | walk: the can filled for this plant alone | P1 151, P6 151 |
| M7 | fold: the trip back a step short | P1 274, P3 144, P4 311, P5 266, P6 274 |
| M8 | fold: a can short by one at the start | P1 59, P4 311, P6 59 |
| M9 | fold: the step to a plant within reach not counted | P1 340, P3 226, P4 340, P5 74, P6 340 |
| M10 | trips: a run ending when the can would be emptied | P1 152, P4 311, P6 152 |
| M11 | trips: a new run's first plant not in it | P1 232, P4 272, P6 232 |
| M12 | trips: the row's own walk left out | P1 340, P3 205, P4 340, P5 340, P6 340 |
| M13 | struct: the walk counted only outward | P1 274, P3 149, P4 311, P5 266, P6 274 |
| M14 | struct: the gardener left at the river | P1 302, P3 187, P4 311, P5 340, P6 302 |
| M15 | struct: the river one place further | P1 274, P3 141, P4 311, P5 266, P6 274 |
| M16 | solution: the adapter's can one bigger | P1 178, P2 178, P4 26, P6 178 |
| M17 | solution: the adapter's plants halved | P1 272, P2 170, P4 311, P6 272 |

P1 and P6 kill all seventeen, P4 fourteen, P3 and P5 eight each, and P2
two. P4, whose cans take no refill or one at every plant, sees every
edit to a step's count or a refill's test: a can short at the start
(M8), a refill at a can that would just be emptied (M10). P5 sees the cost of
a trip: one way only (M13), a step short (M7) or long (M15), or the
walk back stopping early (M4, M5); P3 all of those but M4, whose
shortened trips keep the steps less `n` even. P2, which triples every want and
the can, sees only what does not scale: the adapter's can one bigger
(M16) and its wants halved (M17). Three edits change only when a refill
happens and are seen by P1 and P6 alone: the water left kept on a
refill (M1), a can one short after one (M3), filled for one plant (M6).

Of the thirty-two, fifteen were not kept, and none survives. Thirteen
fail as a kept one: the ★ arm's trip back counted one way and the
trips arm's walks back one way as M13; the ★ arm's walk back from the
plant itself and the trips arm's run counted from the next plant as
M15; the struct arm's start at the first plant as M2; the ★ arm's
emptied can sending them back and the Rust arm's reach test strict as
M10; the fold arm's refilled plant's water not taken and the Rust arm's
kept as M11; the walk arm's step to each plant not counted as M12; the
Rust arm's trip back without the step as M7; the fold arm's water
allowed one short as M16, which reads the can as one bigger; the struct
arm's can refilled one short as M3. Two are killed with checks of their
own but were left out because their arm keeps three: the walk arm's
refill tested against the can's size (P1 274, P4 311) and its water
taken twice (P1 185, P4 311).

## Verification

Every arm prints the same output as `water.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.5 s to 0.8 s and the
differential 0.4 s (timed while other work shared the machine).

No arm met a compiler gap. The walk arm was written with a `while` over
`next` and `next += 1` at the end of its body; `karac fix` made it a
`for next in 0..plants.len()`, a style lint `karac check` allows.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 4 and 1 edits: `Vec<i32>` to brackets, the `&` of
`&need` dropped, `struct Solution;` to `struct Solution {}`, and the
adapter's `as i64`, which the `i32` widens to anyway; then `let mut ans
= 0` to `ans: i32`, as the literal kept the default `i64` against the
`i32` the method returns. The fixed arm reads as the template does.

## Benchmarks

The bench builds 2000 gardens of 1000 plants wanting 1 to 1000 each,
then answers every garden for 500 cans, from 1000 up by 97 a can, with
the ★ arm in all five languages: 1000000 walks down 1000 plants. Every
implementation prints `1000000 answers: sum 45596432546, checksum
318372821`.

BENCHTAB
