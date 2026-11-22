# 2751. Robot Collisions

There are `n` **1-indexed** robots, each having a position on a line,
health, and movement direction.

You are given **0-indexed** integer arrays `positions`, `healths`, and a
string `directions` (`directions[i]` is either **'L'** for **left** or
**'R'** for **right**). All integers in `positions` are **unique**.

All robots start moving on the line **simultaneously** at the **same
speed** in their given directions. If two robots ever share the same
position while moving, they will **collide**.

If two robots collide, the robot with **lower health** is **removed**
from the line, and the health of the other robot **decreases** **by
one**. The surviving robot continues in the **same** direction it was
going. If both robots have the **same** health, they are **both**
removed from the line.

Your task is to determine the **health** of the robots that survive the
collisions, in the same **order** that the robots were given, i.e. final
health of robot 1 (if survived), final health of robot 2 (if survived),
and so on. If there are no survivors, return an empty array.

Return *an array containing the health of the remaining robots (in the
order they were given in the input), after no further collisions can
occur.*

**Note:** The positions may be unsorted.

```
positions = [5, 4, 3, 2, 1], healths = [2, 17, 9, 15, 10], directions = "RRRRR"  ->  [2, 17, 9, 15, 10]
positions = [3, 5, 2, 6],    healths = [10, 10, 15, 12],   directions = "RLRL"   ->  [14]
positions = [1, 2, 5, 6],    healths = [10, 10, 11, 11],   directions = "RLRL"   ->  []
```

**Constraints:** `1 <= positions.length == healths.length ==
directions.length == n <= 10^5`, `1 <= positions[i], healths[i] <=
10^9`, `directions[i] == 'L'` or `directions[i] == 'R'`, all values in
`positions` are distinct.

## Approaches

Robots moving the same way never meet, so every fight is between a
robot moving right and the nearest one moving left after it that is
still standing.

| file | mechanism |
|---|---|
| `robots.kara` ★ | the robots in order of position through a sorted index; those moving right wait on a stack, and each robot moving left meets the stack's top in turn, by `let Some(top) = .. else { break }`; the survivors read back in input order by `filter`. O(n log n) |
| `robots_mirror.kara` | the same fights seen from the right: the robots in falling order of position by `sort_by` and `cmp`, those moving left on a stack, the two healths compared by `cmp` and the three `Ordering`s matched. O(n log n) |
| `robots_linked.kara` | the robots in order of position joined in a doubly linked list of `prev` and `next` slots; a cursor walks right, two neighbours facing each other fight, the loser is unlinked by a closure taking both slot lists as `mut ref`, and the cursor steps back. O(n log n) |
| `robots_structs.kara` | each robot a `struct Robot`, sorted by position; those moving right moved onto a stack as owned values and popped by `while let Some(top) = stack.pop()`, the survivors gathered as `Robot`s and sorted back by their place in the input. O(n log n) |
| `robots_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut healths` changed in place, a `Vec<usize>` of indices sorted by `sort_unstable_by_key`, and `while let Some(&j) = stack.last()` with `break`s, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one
robot; two facing apart; one strong robot through a line of weak ones;
3000 random cases of 1 to 12 robots at positions up to 30 with healths
up to 5; and 10 of `10^5` robots, LeetCode's most, the last two with the
sum of the survivors' healths and a checksum over every survivor.
`robots.py` mirrors the ★ arm and its output is byte-identical.

```
[2, 17, 9, 15, 10]
[14]
[]
[3]
[5, 6]
[6]
3000 small cases: healths sum to 33152, checksum 493751350
10 cases of 100000 robots: healths sum to 124537351, checksum 220856242
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: time run in half steps, every position doubled and each
robot moving one place a tick, two robots on one place fighting there,
until no robot moving right has one moving left anywhere after it; no
stack. It draws 2000 random cases of 1 to 10 robots at positions up to
30 with healths up to 5, then 100 of up to 2000 robots with positions and
healths up to `10^9`, all before any arm answers; the literal reading is
asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 robots, the survivors are the literal reading's |
| P2 | every position mirrored and every direction turned: the same survivors |
| P3 | every position doubled, less 1: the same survivors |
| P4 | the robots listed in reverse order: the survivors reversed |
| P5 | no more survivors than robots and no health above the total; and every robot facing right: every health as it was |
| P6 | each arm agrees with at least three of the other four |

P3 first multiplied by 3 and added 7, which takes a position of `10^9`
past `i32`: the solution arm's wrapper narrows it with `as i32`, which
wraps as Rust's does, and the robots changed order, failing P3 in every
one of the 100 large cases. P3 now stays within `i32` by doubling.

The differential prints `2100 cases: checksum 651555085, 63000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same ticks gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M4 fail the same checks, both letting a
robot moving left win with its health whole; so do M3 and M9, both
reading the fights from the wrong side. M6 first left a back link
unmended, which the interpreter could not finish within ten minutes, and
was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a robot moving left loses nothing for a win | P1 857, P2 1353, P6 955 |
| M2 | ★: of two equals only the one moving left goes | P1 600, P2 557, P6 603 |
| M3 | mirror: the robots taken in rising order | P1 1581, P6 1681 |
| M4 | mirror: the stronger loses nothing | P1 857, P2 1353, P6 955 |
| M5 | linked: the cursor never steps back | P1 535, P2 810, P6 635 |
| M6 | linked: of two equals only the one moving right goes | P1 598, P2 557, P6 601 |
| M7 | structs: the robots left on the stack lost | P1 1417, P2 2040, P5 2100, P6 1513 |
| M8 | structs: the survivors sorted by position | P1 1189, P2 1516, P4 1516, P5 1667, P6 1289 |
| M9 | solution: every direction read the other way | P1 1581, P6 1681 |
| M10 | solution: the indices left in input order | P1 1413, P2 1685, P4 1685, P6 1513 |

## Benchmarks

The bench draws 10 cases of `10^5` robots, LeetCode's most, robot i
somewhere in the i-th stretch of `10^4` places and the list then
shuffled, healths up to `10^9`, all of them first, then answers each 3
times by the ★ arm in all five languages. C sorts with `qsort`, Go with
`slices.SortFunc`, and Rust and Kāra with `sort_by_key`; positions are
distinct, so every sort gives one order. Every implementation prints
`10 cases of 100000 robots, 3 rounds: healths sum to 13980962835099,
checksum 787389373`.

BENCHTAB

## Verification

All five arms print the same output as `robots.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, mirror and linked arms checked clean as first written. The
structs arm wrote Rust's `while let Some(mut top) = stack.pop()`, and
`karac fix` made it `Some(top)` with `let mut top = top;` inside. The
bench first passed `directions.clone()` to the arm, and `karac check`
warned that the parameter only borrows it; `karac fix` dropped the
`.clone()`.

LeetCode's Rust template took 37 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `mut healths: Vec<i32>` became
`healths: own Vec[i32]` with a `let mut healths = healths;`;
`Vec<usize>` became `Vec[i64]` and `sort_unstable_by_key` became
`sort_by_key`; `as_bytes()` became `bytes()`; `for &i in &idx` became
`for i in ref idx`; `while let Some(&j) = stack.last()` became `while
let Some(j) = stack.last().cloned()`; the `&h`, `&p` and `&i` patterns
dropped their `&`; and `Solution::` became `Solution.`.
