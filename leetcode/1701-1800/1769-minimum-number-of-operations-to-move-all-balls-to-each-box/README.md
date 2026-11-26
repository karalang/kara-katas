# 1769. Minimum Number of Operations to Move All Balls to Each Box

You have `n` boxes. You are given a binary string `boxes` of length `n`,
where `boxes[i]` is `'0'` if the `i`th box is empty, and `'1'` if it
contains one ball. In one operation, you can move one ball from a box to
an adjacent box. Box `i` is adjacent to box `j` if `abs(i - j) == 1`.
Note that after doing so, there may be more than one ball in some boxes.
Return an array `answer` of size `n`, where `answer[i]` is the minimum
number of operations needed to move all the balls to the `i`th box. Each
`answer[i]` is calculated considering the initial state of the boxes.

```
boxes = "110"     ->  [1,1,3]
boxes = "001011"  ->  [11,8,5,4,3,4]
```

**Constraints:** `n == boxes.length`, `1 <= n <= 2000`, and `boxes[i]`
is `'0'` or `'1'`.

The arms are `fn min_operations(boxes: String) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `min_operations.kara` ★ | two sweeps: left to right, the moves to bring every ball seen so far one box further grow by the number of those balls, and the same from the right; each box's answer is the two sums. O(n) |
| `min_operations_brute.kara` | for every box, the distance to each ball summed, the balls' positions collected first with `enumerate`, `filter` and `map`. O(n^2) |
| `min_operations_prefix.kara` | prefix sums of the balls and of their positions: a box's moves are its position times the balls on its left less their positions' sum, and the same mirrored on the right. O(n) |
| `min_operations_delta.kara` | the first box's moves counted outright, then each step right adds one move for every ball now on the left and saves one for every ball from the new box on. O(n) |
| `min_operations_solution.kara` | a Rust solution as LeetCode's Rust users write it (`boxes.as_bytes()`, `(b[i] - b'0') as i32`, two sweeps), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`[1, 1, 3]
[11, 8, 5, 4, 3, 4]`); five edges, one empty box, one full box, every
box empty, every box full, and balls only at the two ends; the
constraints' most, 2000 full boxes, so that each end box needs 1999000
moves, and 2000 boxes half full, as the end boxes' answers and digests
(`the most: 1999000 1999000 448715735, 734334012`); and 3000 random rows
of 1 to 40 boxes (`3000 random rows: checksum 285668090`).
`min_operations.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and prefix arms check clean as first written. The
brute arm was first written with Rust's turbofish, `.sum::[i64]()`, and
a `*c` on the `filter` closure's `char`; `karac fix` took both, in 2
fixes. The delta arm's `filter(|b| **b)` lost one `*`, since the item is
a copied `bool`, and its `vec![moves]` became the list literal
`[moves]`, 2 fixes. The Rust solution takes one round of 19 fixes by
`karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `Vec<i32>` to `Vec[i32]` in both signatures, `as_bytes()`
to `bytes()`, `vec![0; n]` to `Vec.filled(n, 0i32)`, each `let (mut cnt,
mut ops) = (0, 0)` to `let mut (cnt, ops) = (0i32, 0)`, each
`(b[i] - b'0') as i32` to `b[i] - b'0'`, the `u8` widening on its own,
and `Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each box, the balls moved one operation at a time into an
adjacent box toward it, counting operations until every ball is there.
LeetCode's examples, the edges, and 1992 random rows of 1 to 14 boxes,
each with its own chance of a ball. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no answer below 0, and the answers convex along the row |
| P3 | the row reversed gives the answers reversed |
| P4 | a ball added to the first empty box raises each box's answer by its distance to that box |
| P5 | an empty box added at the end changes no answer, and its own is the last box's plus one move for every ball |
| P6 | the ★ arm's answer |

P4 runs where the row has an empty box. The differential's P4 first
joined the new row as `boxes[..k].to_string() + "1" + boxes[k + 1..]`,
and check asked for `.to_string()` on the last slice, since `+` takes an
owned `String` on its right; `karac fix` wrote it. The error's caret
underlines the left operand, `boxes[..k].to_string() + "1"`, though the
message is about the right one (B-2026-11-26-84). All 58,345 checks pass
on every arm: `2000 cases: checksum 6803454, 58345 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, summing each ball's distance, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the first box never swept from the right | P1 1526, P2 1407, P3 1585, P4 666, P6 6104 |
| M2 | ★: the left sweep's balls carried into the right sweep | P1 1585, P3 1585, P4 1596, P5 1651, P6 6340 |
| M3 | brute: distances signed, so the two sides cancel | P1 1526, P2 1526, P3 1585, P4 666, P6 1526 |
| M4 | brute: every ball read one box to the right | P1 1651, P3 1585, P4 1669, P5 984, P6 1651 |
| M5 | prefix: each ball's position summed one too far | P1 1585, P2 723, P3 1585, P4 1596, P5 984, P6 1585 |
| M6 | prefix: a box's own ball counted on its right | P1 1526, P2 1184, P3 1562, P4 666, P5 918, P6 1526 |
| M7 | delta: the new box's ball counted on its left | P1 1320, P2 97, P3 1320, P4 1596, P5 997, P6 1320 |
| M8 | delta: the first box's moves counted as its balls | P1 1533, P2 1011, P3 1206, P4 1367, P6 1533 |
| M9 | solution: the last box left out of the right sweep | P1 918, P3 1230, P4 84, P5 918, P6 918 |
| M10 | solution: every answer started at 1 | P1 2000, P6 2000 |

## Benchmarks

The bench builds 200 rows of 2000 boxes once, each row with its own
chance of a ball, and makes 40000 calls of the ★ arm, each on a row
chosen from the checksum so far. Every implementation prints `40000
calls over 200 rows: checksum 139818037`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.63 s against Rust's 0.13 s (0.69 s with overflow checks
on), C's 0.12 s and Go's 0.28 s; Python takes 15.0 s.
