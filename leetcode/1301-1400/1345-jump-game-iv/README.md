# 1345. Jump Game IV

Given an array of integers `arr`, you are initially positioned at the
first index of the array. In one step you can jump from index `i` to
index:

- `i + 1` where `i + 1 < arr.length`;
- `i - 1` where `i - 1 >= 0`;
- `j` where `arr[i] == arr[j]` and `i != j`.

Return the minimum number of steps to reach the last index of the array.
Notice that you can not jump outside of the array at any time.

```
arr = [100,-23,-23,404,100,23,23,23,3,404]  ->  3
arr = [7]                                    ->  0
arr = [7,6,9,6,9,6,9,7]                      ->  1
```

**Constraints:** `1 <= arr.length <= 5 * 10^4`, `-10^8 <= arr[i] <=
10^8`.

The arms are `fn min_jumps(arr: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_jumps.kara` ★ | a breadth-first search from index 0, the neighbours of i being i - 1, i + 1 and every index holding the same value; the indices of each value gathered in a `Map` first, and a value's list taken out by `remove` the first time it is used, since every index on it is then queued. O(n) |
| `min_jumps_seen.kara` | the same search with the value lists left whole; a `Set` of the values already expanded, whose `insert` says whether a value is new, walks each list once. O(n) |
| `min_jumps_zeroone.kara` | one more node for each distinct value, so a jump between equal values is two edges: from an index to its value's node, costing the step, and from the node to each index holding it, costing nothing. A breadth-first search with a deque, free edges pushed at the front and paid ones at the back. O(n) |
| `min_jumps_levels.kara` | no queue: the indices reached in d steps held as one `Vec`, the next built from it, each value's list used once and emptied by `insert` of an empty `Vec`, whose old value is the list. O(n) |
| `min_jumps_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, Vec<usize>>` filled by `.entry(x).or_insert_with(Vec::new).push(i)`, a `VecDeque` taken a level at a time, `vec![false; n]`, and a value's list taken out by `if let Some(nexts) = graph.remove(&arr[i])`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, and 5 *
10^4 values, the constraints' longest, all equal, all different and
rising, at random from 1 to 1000, and with unique first and last values
and the rest drawn from 300 values between -10^8 and 10^8 (`3 0 1 1
49999 5 6`); and 1000 random arrays of 1 to 500 values, most of them
short, from 1 to 3, to 20 or to 10^4 (`1000 random arrays: checksum
679931738`). `min_jumps.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`. Only lookups touch a `Map` or a
`Set`, never a walk, so their order cannot reach the output.

The Mend loop: the four Kāra arms check clean. The Rust solution takes
one round of 26 fixes by `karac fix`'s count, from 17 errors: the `use
std::collections::{HashMap, VecDeque};` line deleted, `struct
Solution;` to `struct Solution {}`, `HashMap<i32, Vec<usize>>` to
`Map[i32, Vec[i64]]` and `HashMap::new()`, `Vec::new` and
`VecDeque::new()` to `Map.new()`, `Vec.new` and `VecDeque.new()`,
`vec![false; n]` to `Vec.filled(n, false)`, `0usize` to `0`, `(i, &x)`
to `(i, x)`, `&arr[i]` to `arr[i]`, each `!` and `&&` to `not` and
`and`, and `Solution::` to `Solution.`. Its output matches on the first
run.

A second Rust solution, which empties a list in place with `if let
Some(list) = map.get_mut(&arr[i]) { .. list.clear(); }` and steps to
both sides with `for j in [i.wrapping_sub(1), i + 1] { if j < n && .. }`,
is held back. `karac fix` makes its `usize` index an `i64` and leaves
`i.wrapping_sub(1)` as it was; on a `usize` that wrapped past every
length at 0 and `j < n` dropped it, but on an `i64` it is -1, passes `j <
n`, and the fixed program stops with index out of bounds. The same pass
gives `checked_sub` and `saturating_sub` an edit that keeps the `usize`
floor, and `wrapping_sub` none. That is ledger row B-2026-11-24-49; the
arm joins the kata once the fix lands.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every index's distance from the first relaxed over every
allowed step, every pair of indices tried each round, until a round
changes nothing. 2000 arrays of 1 to 12 values in four kinds, 500 each:
from 1 to 2; from 1 to 4; from 1 to 12, mostly different; and a walk,
each value one more, one less or the same as the one before. Every array
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the same answer |
| P3 | every value x made 3x + 7, which keeps equal values equal and different ones different: the same answer |
| P4 | the first value put again at the end: one jump |
| P5 | a value held nowhere else put in front: one step more |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 603861800,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, with a breadth-first search
over every pair, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no step forward | P1 1302, P5 2000, P6 5208 |
| M2 | ★: the last index left out of the value lists | P1 800, P2 827, P4 1864, P6 3200 |
| M3 | seen: the step back taken as a step of two | P1 14, P6 14 |
| M4 | seen: a value's indices marked but never queued | P1 1439, P4 1864, P5 1439, P6 1439 |
| M5 | zeroone: the step onto a value's node made free | P1 1634, P4 2000, P6 1634 |
| M6 | zeroone: a jump between equal values costing two steps | P1 1439, P4 1864, P6 1439 |
| M7 | levels: no step back | P1 11, P6 11 |
| M8 | levels: the steps counted from 1 | P1 2000, P4 2000, P6 2000 |
| M9 | solution: no step forward onto the last index | P1 716, P2 690, P5 704, P6 716 |
| M10 | solution: the steps counted per index taken, not per level | P1 1308, P2 580, P4 1263, P6 1308 |

P1 and P6 kill all ten, P4 six, P2 three, P5 three and P3 none. The
first value put again at the end (P4) asks for exactly one jump, which
catches every edit that prices a jump between equal values wrong (M5,
M6), cannot jump onto the last index (M2) or not at all (M4), or counts
wrong (M8, M10). The fresh value in front (P5) can only be left by a
step forward, which catches the arms that lose that step (M1, M9) and
the one that marks a jump's landing places without visiting them (M4).
Reading backwards (P2) catches the edits that treat the two ends
differently (M2, M9) and the per-index count (M10), whose total depends
on how many indices a level holds before the last. Relabelling (P3)
keeps every jump, and no arm here looks at a value except to compare it,
so it catches nothing. The two edits to the step back (M3, M7) are the
weakest: a step back is on a shortest path only when the way forward is
blocked and a jump lands beyond the target, which 14 and 11 of the 2000
short arrays need.

## Benchmarks

The bench builds 10 arrays of 5 * 10^4 values, the constraints' longest,
once: half at random from 1 to 1000, where a few jumps reach the end,
and half with every value twice in a row, where the path walks most of
the array. It then makes 30 passes, each setting one value of every
array from the checksum so far, so no answer carries over, answering
every array with the ★ arm's search and folding the answer plus the pass
into the checksum. Rust uses a `HashMap` and Go a `map`; C, which has no
map, numbers each value's group from an open-addressing table, lays the
groups' indices out one after another, and marks a group used instead
of removing it. Every implementation prints `30 passes over 10 arrays of
5 * 10^4: checksum 161757040`.

BENCHTAB
