# 1354. Construct Target Array With Multiple Sums

You are given an array `target` of `n` integers. From a starting array
`arr` consisting of `n` 1's, you may perform the following procedure:

- let `x` be the sum of all elements currently in your array;
- choose index `i`, such that `0 <= i < n`, and set the value of `arr`
  at index `i` to `x`;
- you may repeat this procedure as many times as needed.

Return `true` if it is possible to construct the `target` array from
`arr`, otherwise return `false`.

```
target = [9,3,5]      ->  true    [1,1,1] -> [1,1,3] -> [1,5,3] -> [9,5,3]
target = [1,1,1,2]    ->  false
target = [8,5]        ->  true
```

**Constraints:** `n == target.length`, `1 <= n <= 5 * 10^4`, `1 <=
target[i] <= 10^9`.

Each arm is `fn is_possible(target: Vec[i32]) -> bool`.

## Approaches

Every arm undoes the moves from the target. The value set last is the
largest, since it is the sum of all the others and itself, and before
that move it was itself less the sum of the rest, so the undo is
unique; many undos in a row of the same value are one remainder. A
largest value of 1, or a rest of 1 (two values, one of them 1), can
always be reached; a largest value no larger than the rest, or a
multiple of it, cannot.

| file | mechanism |
|---|---|
| `is_possible.kara` ★ | the values in a max-first `PriorityQueue` with a running total. O(n log n log M) for values up to M |
| `is_possible_scan.kara` | the values in a list, the largest found each time by a scan of every place. O(n) for each undo |
| `is_possible_sorted.kara` | the values as a multiset, a `SortedMap` from each value to how many places hold it, the largest its last key. O(n log n log M) |
| `is_possible_tree.kara` | the values in a segment tree whose every node holds the place of the largest value below it; an undo rewrites one leaf and the nodes above it. O(log n) for each undo after an O(n) build |
| `is_possible_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `BinaryHeap<i64>` collected from `target.iter().map(\|&x\| x as i64)`, `while let Some(x) = heap.pop()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one value,
1 and 2, two values sharing no factor and two sharing one at the
constraints' largest, and 5 * 10^4 values, the constraints' most: all
1, reached by moves, and one of those raised by 1 (`true false true true
false true true false true true false`); and 2000 random targets of 1
to 8 values, half reached by up to 30 moves, a quarter of those with
one value then raised by 1 or 2, half drawn at random from 1 to 10, 1
to 1000 or 1 to 10^9 (`2000 random targets: 849 possible, checksum
884692404`). `is_possible.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the scan and tree arms check clean. The ★ arm was written
`total += x as i64; heap.push(x as i64);` over `target.iter()`; `karac
check` warns that the second cast is unnecessary, an `i32` widening to
`i64` implicitly (W0310, `lossless_cast`), and `karac fix` drops it, but
it says nothing of the first, which is just as unnecessary: `total += x`
checks and runs. The lint misses a widening of the `ref i32` that
`iter()` yields when it is an operator's operand, filed as
B-2026-11-25-19. The sorted arm was written with Rust's
`counts.last_key_value()`; `karac check` says that Kāra's is `last()`
(E0236), and `karac fix` renames it and copies the pair out of its
references, `let (x, k) = (*x, *k);`. The Rust solution takes one round
of 13 fixes by `karac fix`'s count: the `use` line goes, `struct
Solution;` becomes `struct Solution {}`, `Vec<i32>` `Vec[i32]`, each
`|&x|` `|x|` and each `||` `or`, and the `BinaryHeap<i64>` collected
from an iterator becomes a `PriorityQueue[i64]` made by
`PriorityQueue.max_first_from(..collect())`, since Kāra's queue pops the
smallest first unless it is made largest-first. Every arm matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the moves made forward from the ones, every choice of place
tried, never setting a place above its target, since a value only
grows. Each array but the ones has one move that made it, its largest
value, so the search meets no array twice. 2000 targets of 1 to 4
values in four kinds, 500 each: reached by up to 8 moves with no value
past 200; values from 1 to 6; values from 1 to 30; and reached by up to
8 moves, one value then raised by 1 or 2. Every target is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the values in the opposite order: the same answer |
| P3 | one move more, at the place the sum picks: the same answer, since the move can be undone only one way |
| P4 | a target that can be reached has its largest value 1, or above the sum of the rest |
| P5 | the first two values alone: possible exactly when they share no factor |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 targets: checksum 512561980,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, searching the arrays forward
breadth-first, gives the same checksum: all 500 targets reached by
moves can be reached, 114 of those from 1 to 6, 90 from 1 to 30 and
113 of those raised.

The differential's harness was written `gcd(target[0] as i64,
target[1] as i64)`, and `karac fix` drops both casts (W0310).

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pair with a 1 not taken at once | P1 366, P3 17, P5 1081, P6 1464 |
| M2 | ★: the smallest value undone first | P1 613, P3 125, P4 144, P5 745, P6 2452 |
| M3 | scan: the last place never the largest | P1 381, P2 227, P3 108, P4 6, P5 600, P6 381 |
| M4 | scan: the first place never the largest | P1 376, P2 227, P3 45, P4 3, P5 590, P6 376 |
| M5 | sorted: a largest value held twice taken as possible | P1 193, P3 31, P4 132, P5 84, P6 193 |
| M6 | sorted: a largest value of 1 not taken at once | P1 284, P6 284 |
| M7 | tree: an undone value's parent never refreshed | P1 286, P2 33, P3 94, P5 445, P6 286 |
| M8 | tree: the root never built | P1 336, P2 534, P3 283, P4 57, P5 364, P6 336 |
| M9 | solution: a remainder of 0 kept as a value | P1 26, P3 18, P6 26 |
| M10 | solution: one value always possible | P1 348, P5 348, P6 348 |

P1 and P6 kill all ten, P3 and P5 eight, P4 five and P2 four. The first
two values alone (P5) are the pairs, where the answer is a gcd, and
catch every edit that is wrong on two values; the edit that misses
only three or more ones (M6) gets every pair right, and so does the
solution's 0 kept as a value (M9), whose guard on a rest of 0 answers
false as it should. One move more (P3) leaves the answer unchanged, and
catches the edits whose wrong answer depends on how far the undos run;
the edit that misses three or more ones (M6) answers false for every
target of three or more values that can be reached, a move more or
not, and a lone value (M10) has no move that changes it. The opposite
order (P2) catches the edits that depend on the place a value holds:
the scan that skips the last or the first place (M3, M4) and the tree's
two (M7, M8). The largest value above the rest (P4) holds of every
target that can be reached, and catches the edits that answer true
where it fails (M2, M3, M4, M5, M8). The weakest edit, the solution's
remainder of 0 kept (M9), differs only where the largest value is a
multiple of the rest, in 26 of the 2000 targets.

## Benchmarks

The bench builds 20 targets of 5 * 10^4 values, the constraints' most,
each reached from the ones by moves until a value would pass 10^9, once;
then makes 2000 rounds, each changing one place of one target, drawn
from the checksum so far, so no answer carries over, answering with the
★ arm's undos, and putting the place back; one round in four leaves the
value as it was, so a quarter of the answers run every undo back to the
ones. Each answer folds into the checksum with the round. Every
implementation prints `2000 rounds over 20 targets of 5 * 10^4 values:
checksum 367757099`. C and Go push onto a binary max-heap written out,
Rust onto `BinaryHeap`, Python onto `heapq` with the values negated.

BENCHTAB
