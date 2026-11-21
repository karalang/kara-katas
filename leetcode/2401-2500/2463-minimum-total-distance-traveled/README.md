# 2463. Minimum Total Distance Traveled

There are some robots and factories on the X-axis. You are given an
integer array `robot` where `robot[i]` is the position of the `i`th
robot. You are also given a 2D integer array `factory` where
`factory[j] = [position_j, limit_j]` indicates that `position_j` is the
position of the `j`th factory and that the `j`th factory can repair at
most `limit_j` robots.

The positions of each robot are **unique**. The positions of each
factory are also **unique**. Note that a robot can be **in the same
position** as a factory initially.

All the robots are initially broken; they keep moving in one direction.
The direction could be the negative or the positive direction of the
X-axis. When a robot reaches a factory that did not reach its limit, the
factory repairs the robot, and it stops moving.

**At any moment**, you can set the initial direction of moving for
**some** robot. Your target is to minimize the total distance traveled
by all the robots.

Return *the minimum total distance traveled by all the robots*. The test
cases are generated such that all the robots can be repaired.

**Note that**

- All robots move at the same speed.
- If two robots move in the same direction, they will never collide.
- If two robots move in opposite directions and they meet at some
  point, they do not collide. They cross each other.
- If a robot passes by a factory that reached its limits, it crosses it
  as if it does not exist.
- If the robot moved from a position `x` to a position `y`, the distance
  it moved is `|y - x|`.

```
robot = [0,4,6], factory = [[2,2],[6,2]]  ->  4
robot = [1,-1], factory = [[-2,1],[2,1]]  ->  2
```

**Constraints:** `1 <= robot.length, factory.length <= 100`;
`factory[j].length == 2`; `-10^9 <= robot[i], position_j <= 10^9`;
`0 <= limit_j <= robot.length`; the input is generated such that it is
always possible to repair every robot.

Since a robot may be pointed either way and passes full factories, the
question is only which factory repairs which robot: the cheapest
assignment of robots to factories within their limits, each robot
paying its distance. Two robots never need to cross: if the left one
goes right of where the right one goes, swapping their factories costs
no more. So with both lists sorted, each factory takes a run of
consecutive robots, and a table over "robots from `i`, factories from
`j`" settles it.

## Approaches

| file | mechanism |
|---|---|
| `distance.kara` ★ | a table over the sorted robots and factories: `best[i][j]`, the least distance for robots `i..` with factories `j..`, either skips factory `j` or gives it the next `t` robots, `t` up to its limit, the run's distance added as it grows. O(n m L) |
| `distance_memo.kara` | the same choice top down: a recursion over the next robot, the next factory and the room it has left, remembered in a `Map` keyed by the three, each call passing the factory by or sending it one more robot. O(n m L) |
| `distance_slots.kara` | every factory spread into its `limit` slots along the line; the sorted robots are matched in order to an increasing choice of slots, one row of the table kept per robot. O(n S), S the slots |
| `distance_flow.kara` | a minimum-cost flow: source to robots, robots to factories at their distance, factories to sink with their limits, one robot's flow pushed at a time along the cheapest residual path, found by Bellman-Ford. No sorting. O(n^2 m (n + m)) |
| `distance_iter.kara` | iterators over the slots: the slots by `flat_map` and `repeat` with `take`, then the robots folded by `fold` into the row of least distances, each row built right to left by `scan` and reversed. O(n S) |
| `distance_solution.kara` | LeetCode's Rust template: `mut robot: Vec<i32>` and `mut factory: Vec<Vec<i32>>` sorted by `sort_unstable` and `sort_unstable_by_key`, a `vec![vec![i64::MAX; m + 1]; n + 1]` table over `usize` indices and inclusive ranges, the distances added in `i64` through `as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; then four
more, one robot on a factory, a factory with no room, robots sent past
the nearer factory, and the constraints' widest line, two robots and
two factories at its two ends; 100 robots and 100 factories over the
whole line from `-10^9` to `10^9`, the constraints' most, with limits up
to 3; 100 robots and 3 factories whose limits only just hold them; 100
robots and 100 factories packed into 201 places; and 1000 random cases
of 1 to 6 robots and 1 to 4 factories over 21 places, as a checksum.
`distance.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 2356 random cases of up to 6 robots and 4
factories against every assignment within the limits.

The flow arm's Bellman-Ford reads each edge through `let edge = ref
edges[e];`. Written `let edge = edges[e];`, `check` refused it, since
`Edge` is not `Copy` and the index cannot be moved out of, and `karac
fix` wrote the `ref`.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 17 edits: each `mut robot: Vec<i32>`
parameter written `robot: own Vec[i32]` with `let mut robot = robot;`
at the body's start; the brackets of each `Vec<..>`; `sort_unstable`
and `sort_unstable_by_key` written `sort` and `sort_by_key`, Kāra's
sorts being stable; `vec![vec![x; a]; b]` written `Vec.filled(b,
Vec.filled(a, x))`; each `i64::MAX` written `i64.MAX`; `factory[j][1] as
usize` written `as i64`, and `robot[..] as i64` written plain; and
`struct Solution;` given its braces. The tuple `let (n, m) = (..)`,
`0..=m` and `1..=limit.min(n - i)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to send each robot, in the order given, to a
factory that still has room, tried by a recursion with nothing sorted
or remembered, and the least total distance kept. It checks 300 random
cases of 1 to 6 robots and 1 to 4 factories over the 21 places from
-10 to 10, limits up to 3; then 30 of up to 6 robots and 3 factories
over the whole line from `-10^9` to `10^9`; then 30 of up to 6 robots
whose factories have exactly room for them. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every position negated: the same answer |
| P3 | a robot added on a factory no robot stands on, its limit raised by one: the same answer |
| P4 | every limit raised by one: an answer no larger |
| P5 | every limit the number of robots: each robot's distance to its nearest factory, added |
| P6 | each arm agrees with at least three of the other five |

P2 holds because negating keeps every distance. P3 holds because the
new robot can take the new place at no cost, and no repair does better:
if it went to another factory while an old robot took the new place,
swapping the two costs no more, by the triangle inequality. P4 holds
because every old assignment still fits. P5 holds because with room
everywhere each robot goes to its nearest factory.

The differential prints `360 cases: checksum 398523258, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every assignment. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each run one robot short of the limit | P1 360, P5 360, P6 360 |
| M2 | ★: a run charged only its last robot | P1 282, P2 276, P3 123, P5 294, P6 282 |
| M3 | ★: a factory never passed by | P1 95, P2 129, P3 42, P5 108, P6 95 |
| M8 | memo: the next factory given this one's room | P1 152, P2 176, P3 100, P6 152 |
| M10 | memo: every state remembered at room 0 | P1 6, P2 10, P3 2, P6 6 |
| M11 | memo: the factories left unsorted | P1 106, P2 176, P3 82, P5 104, P6 106 |
| M13 | slots: no slot left empty | P1 79, P2 116, P3 35, P4 133, P5 216, P6 79 |
| M14 | slots: the robots left unsorted | P1 142, P2 165, P3 99, P5 142, P6 142 |
| M15 | slots: a slot used again | P1 55, P2 114, P3 13, P6 55 |
| M18 | flow: no flow ever undone | P1 38, P6 38 |
| M19 | flow: each robot sent twice | P1 149, P3 89, P5 129, P6 149 |
| M20 | flow: each trip one longer | P1 360, P3 340, P5 360, P6 360 |
| M22 | iter: one slot too many each | P1 159, P6 159 |
| M24 | iter: robots left over for free | P1 257, P2 271, P3 59, P4 23, P5 222, P6 257 |
| M25 | iter: the robots folded from the front | P1 179, P3 156, P5 179, P6 179 |
| M28 | solution: a run of one never tried | P1 347, P2 217, P3 186, P5 344, P6 347 |
| M29 | solution: every robot of a run charged as its first | P1 265, P2 271, P3 294, P5 274, P6 265 |

P1 and P6 kill all seventeen, P3 fourteen, P5 twelve, P2 eleven and P4
two.

Fourteen are not kept. Ten fail exactly as a kept one: the ★ arm's
robots left unsorted (M4) as the slots arm's (M14); the ★ arm's and
iter arm's no robots left costing 1 (M5, M26) as the ★ arm's each run
one robot short of the limit (M1), all three wrong on every case; the ★
arm's factory used again (M6) as the slots arm's slot used again (M15);
the memo arm's one robot over each limit and the slots and flow arms'
one place too many at each factory (M7, M12, M17) as the iter arm's one
slot too many each (M22); the slots arm's slots read from the far end
(M16) as the iter arm's robots folded from the front (M25), both
matching the robots against the slots reversed; the iter arm's no slot
left empty (M23) as the slots arm's (M13); and the template's factory
never passed by (M31) as the ★ arm's (M3). Four fail apart from every
kept one and were left out because those arms keep their share already:
the memo arm's each distance doubled (M9), which fails exactly as the
flow arm's one robot fewer sent (M21); the template's last factory
never finishing (M27); and its factories sorted by limit (M30).

P3 was at first every position moved by one constant, which every arm
reads only through differences, so it killed none of the thirty-one; it
was replaced by the robot added on a factory.

## Verification

Every arm prints the same output as `distance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 to 0.7 s but the flow arm,
6.2 s, and the differential 1.6 s; under `karac __mir-llvm-asan` the
differential takes 1.0 s and under `karac run` 0.9 s.

## Benchmarks

The bench builds 40 cases of 100 robots and 100 factories over the
whole line, the constraints' most, limits up to 2, once from its own
generator, then makes 72 passes; each raises one limit of every case,
chosen by the checksum so far, so no answer carries over and the runs
grow longer, then answers every case, folding the answer plus the pass
into the checksum. The bench uses the ★ arm, the table over runs, in all
five languages. Every implementation prints `72 passes over 40 cases of
100 robots: checksum 978978338`. Each language sorts copies of the two
lists, `qsort` in C; the generator keeps positions distinct with the
language's own set, and in C by scanning the positions drawn so far.

BENCHTAB
