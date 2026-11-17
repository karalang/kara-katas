# 2211. Count Collisions on a Road

There are `n` cars on an infinitely long road. The cars are numbered from
`0` to `n - 1` from left to right and each car is present at a **unique**
point.

You are given a **0-indexed** string `directions` of length `n`.
`directions[i]` can be either `'L'`, `'R'`, or `'S'` denoting whether the
`i`th car is moving towards the **left**, towards the **right**, or
**staying** at its current point respectively. Each moving car has the
**same speed**.

The number of collisions can be calculated as follows:

- When two cars moving in **opposite** directions collide with each
  other, the number of collisions increases by `2`.
- When a moving car collides with a stationary car, the number of
  collisions increases by `1`.

After a collision, the cars involved can no longer move and will stay at
the point where they collided. Other than that, cars cannot change their
state or direction of motion.

Return *the **total number of collisions** that will happen on the
road*.

```
directions = "RLRSLL"  ->  5
directions = "LLRR"    ->  0
```

**Constraints:** `1 <= directions.length <= 10^5`; `directions[i]` is
either `'L'`, `'R'`, or `'S'`.

Every collision stops each moving car in it and adds one for each, so
the answer is the number of moving cars that ever collide. The left-movers
at the front and the right-movers at the back drive away with nothing in
their path; every other moving car meets a car that is still or will be.
So trim both ends and count the cars between that are not `'S'`. O(n).

## Approaches

| file | mechanism |
|---|---|
| `collisions.kara` ★ | the cars as a `Vec[char]`, the leading `'L'`s and trailing `'R'`s skipped by two `while` loops, and the moving cars between counted |
| `collisions_sweep.kara` | one pass left to right with the right-movers still running and whether a wreck stands to the left: a left-mover meets the runners (two for the nearest, one for each behind) or the wreck, and a still car stops the runners |
| `collisions_stack.kara` | a `Vec` as the stack of what is left on the road; a left-mover pops the car it meets, both becoming one still wreck, and a still car pops the right-movers before it |
| `collisions_struct.kara` | a `struct Road` of an `enum Car`, which finds once where the leading left-movers end and the trailing right-movers begin; its `escapes` (`ref self`) says whether a car drives off an end with nothing in its way, and every car that does not escape is counted |
| `collisions_iter.kara` | the leading `'L'`s dropped by `skip_while` on the way into a `Vec`, the trailing `'R'`s by `skip_while` over it reversed, and the rest that are not `'S'` counted by `filter` |
| `collisions_solution.kara` | LeetCode's Rust template: a `String` in, `i32` out, the cars by `as_bytes()`, the two ends by `iter().position` and `rposition` in `match`es with a guard, and a slice `s[lo..=hi]` filtered; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one car, every car still, two cars head on, and a column running into a
still car), each with its answer; then a checksum of 3000 random roads
of 1 to 30 cars; then the constraints' longest, 10^5 random cars and
10^5 cars driving right into one still car. `collisions.py` mirrors the ★
arm and its output is byte-identical.

`karac fix` carries the template in two rounds of 5 and 2 edits: first
the three `&` patterns (`|&c|` twice and `|&&c|`) dropped, `struct
Solution;` to `struct Solution {}` and `Solution::` to `Solution.`; then
`as_bytes()` to Kāra's `bytes()` and the adapter's `as i64` on an `i32`
result dropped.

The struct arm compared `Car`s with `==` and the check asked for
`#[derive(PartialEq)]`; `karac fix` added it as a second attribute line
under the `#[derive(Copy, Clone)]` already there, which is valid but
could have joined the list. A first draft of this arm asked each car
with `all` over the cars on its far side, O(n^2), which the interpreter
could not finish on a column of 10^5 cars; it now finds the two ends
once.

The iter arm was first written as Rust would trim a string,
`directions.trim_start_matches('L').trim_end_matches('R')`. Kāra has no
`trim_start_matches`; the check says so and points at `strip_prefix`,
which strips one occurrence and returns an `Option`, to be repeated in a
loop. The arm takes `skip_while` from both ends instead, which says the
same thing over the cars.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the road simulated in half steps, every car at twice its
index and each moving car one place a half step, so two cars meeting
always share a position; the moving cars at a shared position stop
there and count one each, which gives two for a head-on meeting and one
for a car into a still one. It runs 2n + 2 half steps, after which
nothing more can meet; no trimming. It checks 300 random roads of 1 to
12 cars; then 30 with no still car; then 30 with no left-mover. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | it is at most the moving cars |
| P3 | the road reversed and every `'L'` and `'R'` swapped: the same count |
| P4 | an `'L'` added at the front and an `'R'` at the back: the same count |
| P5 | an `'S'` added at the back: more by the `'R'`s it is added after |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 639954930, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python simulation that
groups the cars by position after each half step. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm, five to each of
the other Kāra arms and to the template arm, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: still cars counted too | P1 279, P2 211, P5 360, P6 279 |
| M5 | ★: the last car never counted | P1 113, P3 175, P4 113, P5 255, P6 113 |
| M6 | ★: the trailing trim stopping at an 'S' | P1 70, P3 112, P5 142, P6 70 |
| M7 | sweep: a head-on crash counted as one | P1 178, P6 178 |
| M8 | sweep: the runners behind a head-on crash not counted | P1 66, P3 97, P6 66 |
| M9 | sweep: a left-mover into a wreck not counted | P1 178, P3 220, P6 178 |
| M13 | stack: a left-mover into a wreck counted twice | P1 178, P2 111, P3 220, P6 178 |
| M14 | stack: the crashed right-mover left on the road | P1 178, P2 94, P6 178 |
| M15 | stack: a still car not stopping the right-movers | P1 197, P3 220, P5 142, P6 197 |
| M17 | struct: every left-mover escaping | P1 242, P3 220, P6 242 |
| M18 | struct: a right-mover escaping by the first stop | P1 246, P3 235, P4 10, P5 142, P6 246 |
| M20 | struct: 'S' read as a left-mover | P1 225, P2 139, P3 196, P5 311, P6 225 |
| M22 | iter: the trailing 'R's kept | P1 142, P3 191, P4 360, P5 142, P6 142 |
| M23 | iter: the leading 'L's kept | P1 110, P3 191, P4 360, P6 110 |
| M25 | iter: the trailing 'L's trimmed | P1 231, P3 273, P4 360, P5 231, P6 231 |
| M27 | solution: the first car past the 'L's left out | P1 163, P3 145, P5 27, P6 163 |
| M28 | solution: the last car before the 'R's left out | P1 150, P3 145, P5 150, P6 150 |

P1 and P6 kill all seventeen, P3 fourteen, P5 ten, P4 five and P2 four.
P2 kills only the edits that count more than the moving cars: still
cars counted, a wreck hit counted twice, a crashed car left on the road,
and `'S'` read as a left-mover (M4, M13, M14, M20). P3 swaps the two
directions and reverses the road, so it misses the three edits that
treat both directions alike (M4, M7, M14). P4 pads the road with cars
that escape, and kills the five edits that do not let an end car escape
(M5, M18, M22, M23, M25). P5 adds a still car at the back, which the
trailing right-movers hit.

Of the thirty-one, fourteen were not kept, and every one is killed;
none crashes, none differs between the backends, and none survives. Six
fail as a kept one does: the ★ arm's leading `'L'`s and trailing `'R'`s
kept (M1, M2) as the iter arm's M23 and M22; the stack arm's head-on
crash counted as one (M12) as M7; and still cars counted in the struct,
iter and template arms (M19, M24, M31) as M4. The ★ arm's and the
template's front trimmed of `'R'`s (M3, M30) fail alike and neither is
kept. Six fail their own way and are left out for the count of three
(two for the template): the sweep arm's still car leaving no wreck and
its runners not stopped (M10, M11), the stack arm's crashed left-mover
still moving (M16), the struct arm's leading run one car short
(M21), the iter arm's only left-movers counted (M26) and the
template's guard dropped (M29).

## Verification

Every arm prints the same output as `collisions.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 s to 0.8 s, and the
differential 0.5 s.

## Benchmarks

The bench builds 20 roads of 10^5 cars once, the r-th with r thousand
left-movers at the front and as many right-movers at the back around
random cars, then counts every road 10 times over with the ★ arm in all
five languages, each collecting the cars before it trims. Every
implementation prints `10 passes over 20 roads: checksum 655329470`.

BENCHTAB
