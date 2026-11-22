# 2766. Relocate Marbles

You are given a **0-indexed** integer array `nums` representing the
initial positions of some marbles. You are also given two **0-indexed**
integer arrays `moveFrom` and `moveTo` of **equal** length.

Throughout `moveFrom.length` steps, you will change the positions of the
marbles. On the `i`th step, you will move **all** marbles at position
`moveFrom[i]` to position `moveTo[i]`.

After completing all the steps, return *the sorted list of **occupied**
positions*.

**Notes:**

- We call a position **occupied** if there is at least one marble in
  that position.
- There may be multiple marbles in a single position.

```
nums = [1, 6, 7, 8], moveFrom = [1, 7, 2], moveTo = [2, 9, 5]  ->  [5, 6, 8, 9]
nums = [1, 1, 3, 3], moveFrom = [1, 3],    moveTo = [2, 2]     ->  [2]
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= moveFrom.length <=
10^5`, `moveFrom.length == moveTo.length`, `1 <= nums[i], moveFrom[i],
moveTo[i] <= 10^9`, the test cases are generated such that there is at
least a marble in `moveFrom[i]` at the moment we want to apply the `i`th
move.

## Approaches

Every marble at a place moves together, so only which places hold
marbles matters, not how many.

| file | mechanism |
|---|---|
| `marbles.kara` ★ | the occupied positions in a `Set` built by `collect`: each move, over a `zip` of the two lists, takes its from position out and puts its to position in; the set collected into a `Vec` and sorted at the end. O(n + m + k log k), k the places left |
| `marbles_sorted.kara` | the occupied positions in a `SortedSet` built by `SortedSet.from`, so the moves leave them in order and the answer is the set read out by `into_iter`. O((n + m) log k) |
| `marbles_counts.kara` | how many marbles stand at each position, in a `Map`: a move takes the whole count off its from position by `remove` and adds it at its to position through `entry`; the keys still there, sorted. O(n + m + k log k) |
| `marbles_compress.kara` | no hashing: every position that can ever hold a marble, the starting ones and the moves' targets, sorted and deduplicated, each looked up by `binary_search` in a closure, and a `Vec[bool]` over that list marks the occupied ones. O((n + m) log (n + m)) |
| `marbles_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashSet<i32>` from `nums.into_iter().collect()`, each move a `remove(&from)` and an `insert(to)`, and the set drained into a `Vec<i32>` sorted by `sort_unstable`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a move to
the place itself; marbles at both ends of LeetCode's range moved on top
of each other and away; 3000 random cases of 1 to 10 marbles and moves
over places up to 15; and 5 of `10^5` marbles and moves, LeetCode's
most, over places up to `10^9`, the last two with the count of places
and a checksum. Each move is drawn from a place that holds marbles at
the time. `marbles.py` mirrors the ★ arm and its output is
byte-identical.

```
[5, 6, 8, 9]
[2]
[9]
[5]
3000 small cases: 7019 places, checksum 456741589
5 cases of 100000 marbles and moves: 499966 places, checksum 224025439
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every marble kept on its own, each move carrying every marble
standing on its from position, and at the end the positions with a
marble on them, gathered by picking the least one left each time; no
set. It draws 2000 random cases of 1 to 10 marbles and moves over places
up to 15, then 50 of up to 2000 over places up to `10^9`, all before any
arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 marbles, the places are the literal reading's |
| P2 | every place 1000 more: every answer 1000 more |
| P3 | a last move from the last move's target to itself: the same places |
| P4 | the marbles listed in reverse: the same places |
| P5 | strictly rising, each a starting place or a target, no more than the marbles; and the last move's target among them |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 204329569, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same marble-by-marble moves gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M3 and M5 fail the same checks: both leave the
from position holding its marbles, one in the sorted arm and one in the
counts. The compress arm's first M7, the place list left with repeats,
changed nothing, every lookup still finding a copy, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the marbles put back where they were | P1 1827, P3 672, P5 1069, P6 1877 |
| M2 | ★: the places answered falling | P1 1176, P5 1226, P6 1226 |
| M3 | sorted: the target taken out, not the source | P1 1827, P5 930, P6 1877 |
| M4 | sorted: the first move skipped | P1 913, P3 93, P5 259, P6 963 |
| M5 | counts: the source keeps its marbles | P1 1827, P5 930, P6 1877 |
| M6 | counts: the first marble never placed | P1 563, P4 605, P5 326, P6 613 |
| M7 | compress: the last move left undone | P1 1563, P3 1613, P5 1275, P6 1613 |
| M8 | compress: the empty places answered | P1 2000, P5 2050, P6 2050 |
| M9 | solution: the target put in before the source taken out | P1 566, P3 1613, P5 437, P6 566 |
| M10 | solution: the starting marbles never placed | P1 635, P6 683 |

## Benchmarks

The bench draws 20 cases of `10^5` marbles and moves, LeetCode's most,
over places up to `10^6`, all of them first, then answers each 5 times
by the ★ arm in all five languages: the set is Kāra's `Set`, Rust's
`HashSet`, a Go map, a Python set, and in C an open-addressing table with
linear probing and tombstones; C sorts with `qsort`. Every
implementation prints `20 cases of 100000 marbles and moves, 5 rounds:
8611790 places, checksum 534461405`.

BENCHTAB

## Verification

All five arms print the same output as `marbles.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential first
raised every place by a closure ending in Rust's
`.collect::<Vec<i64>>()` turbofish, written in brackets; `karac check`
refused it, Kāra having no call-site type arguments, and said to
annotate a binding instead. The closure became a function `shifted` with
its return type.

LeetCode's Rust template took 38 `karac fix` edits, the wrapper
included: `use std::collections::HashSet` became `struct Solution {}`;
`nums: Vec<i32>` became `nums: own Vec[i32]`, since `into_iter` takes
it; the other `Vec<..>`s became `Vec[..]`; `HashSet<i32>` became
`Set[i32]`; `remove(&move_from[i])` dropped its `&`; `sort_unstable`
became `sort`; the wrapper's closure `|v: &Vec<i64>| -> Vec<i32>` became
`let narrow: Fn(ref Vec[i64]) -> Vec[i32] = |v: ref Vec[i64]| ..`, the
return type moved onto the binding; its `&nums` arguments and `&x`
pattern dropped their `&`; and `Solution::` became `Solution.`.
