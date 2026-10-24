# 975. Odd Even Jump

You are given an integer array `arr`. From some starting index, you can
make a series of jumps. The (1st, 3rd, 5th, ...) jumps in the series are
called odd-numbered jumps, and the (2nd, 4th, 6th, ...) jumps are called
even-numbered jumps. Note that the jumps are numbered, not the indices.

You may jump forward from index `i` to index `j` (with `i < j`) in the
following way:

- During odd-numbered jumps, you jump to the index `j` such that
  `arr[i] <= arr[j]` and `arr[j]` is the smallest possible value. If
  there are multiple such indices `j`, you can only jump to the smallest
  such index `j`.
- During even-numbered jumps, you jump to the index `j` such that
  `arr[i] >= arr[j]` and `arr[j]` is the largest possible value. If
  there are multiple such indices `j`, you can only jump to the smallest
  such index `j`.
- It may be the case that for some index `i`, there are no legal jumps.

A starting index is good if, starting from that index, you can reach the
end of the array (index `arr.length - 1`) by jumping some number of
times (possibly 0 or more than once). Return the number of good starting
indices.

```
arr = [10,13,12,14,15]  ->  2
arr = [2,3,1,1,4]       ->  3
arr = [5,1,3,4,2]       ->  3
```

**Constraints:** `1 <= arr.length <= 2 * 10^4`; `0 <= arr[i] < 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `odd_even_jumps.kara` ★ | a sorted map, right to left: walking from the right, a `SortedMap` from value to the leftmost index seen so far answers the odd jump with `ceiling` and the even jump with `floor`, since a later insert of the same value comes from further left and replaces the index. Then higher[i], whether the end is reachable starting with an odd jump at i, is lower[] at the odd jump's landing place, and lower[i] is higher[] at the even jump's; the good starts are those with higher[i]. O(n log n) |
| `odd_even_jumps_stack.kara` | sorted order and a monotonic stack: the odd jump from i goes to the first index after i in the order of (value, index), so sorting the indices that way and pushing them onto a stack, each index popped by a later, larger one learns its target; the even jump is the same over (-value, index). O(n log n) |
| `odd_even_jumps_scan.kara` | jump targets by scanning: from i, every j > i is looked at, keeping the smallest value at or above arr[i] and the largest at or below it, the first on a tie by keeping only strict improvements. O(n^2) |
| `odd_even_jumps_sortedvec.kara` | a sorted vector of values: the distinct values seen so far are kept in a sorted `Vec`, each new one inserted where a binary search finds its place, beside a table from value to leftmost index; the search's place is the odd jump's value, and the value there or the one before it the even jump's. O(n log n) comparisons, O(n^2) moves in the worst case |
| `odd_even_jumps_segtree.kara` | a segment tree over ranks: the values are replaced by their ranks among the distinct values, and a tree over the ranks, each node counting the ranks present below it, finds the first present rank at or above r and the last at or below it by walking down. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's three
examples and seven more: a lone value; four equal values, where every
jump goes to the next index; a strictly increasing array, where no even
jump exists; a strictly decreasing one, where no odd jump exists;
LeetCode's smallest and largest values alternating; [3, 1, 2, 3, 1, 2];
and [1, 3, 2, 3, 1]. The last three are totals and checksums over
random arrays: 300 of up to 12 values below 5 (1,220 good starts),
3,000 of up to 60 values below 1,000 (48,285), and 20 of 2,000 values
below 10^5 (20,212). `odd_even_jumps.py` mirrors the ★ arm, with a
sorted list searched by `bisect` beside a dict for the sorted map that
Python lacks, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from each start, the jumps are made one by one, each found by
looking at every index to the right, until the end is reached or no
jump is possible. It checks 3,200 arrays: 3,000 of 1 to 30 values below
3, 10 or 1,000, so that many values repeat, against the statement, and
200 of 100 values over LeetCode's whole range against the other
properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | only the order of the values matters: their ranks, or every value raised alike by up to 1,000 within LeetCode's range, give the same count |
| P3 | whether a start is good depends only on what follows it, so the suffix from a random place s counts no more than its length and than the whole array, and at most one more than the suffix from s + 1 |
| P4 | the end value repeated adds exactly one good start: every jump that reached the old end still lands there, and from it either jump reaches the new end |
| P5 | a value above every other put in front can never make its first jump, so the count stays, when there is room for one |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays of 66360 values: 37210 good starts, checksum
142519182, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(29.5 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twenty-nine edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd jump followed by another odd jump | P1 2390, P6 2583 |
| M2 | ★: an odd jump only to a strictly larger value | P1 1628, P4 3200, P6 1630 |
| M3 | ★: an even jump only to a strictly smaller value | P1 1414, P4 2902, P6 1416 |
| M4 | stack: the rightmost index first among equal values going down | P1 1338, P4 2902, P6 1340 |
| M5 | stack: the rightmost index first among equal values going up | P1 1494, P4 3200, P6 1495 |
| M6 | stack: at most one index popped | P1 2547, P3 101, P6 2747 |
| M7 | scan: the last of equal values taken going up | P1 1243, P6 1245 |
| M8 | scan: the next index never a target | P1 2510, P4 2972, P6 2709 |
| M9 | scan: every possible odd jump good | P1 2426, P6 2624 |
| M10 | sortedvec: no even jump to the smallest value | P1 1641, P6 1781 |
| M11 | sortedvec: the rightmost index kept on a tie | P1 1203, P6 1205 |
| M12 | sortedvec: the search never past the last value | P1 2115, P5 2397, P6 2312 |
| M13 | segtree: an even jump followed by another even jump | P1 2128, P6 2325 |
| M14 | segtree: the left subtree never searched going up | P1 2691, P3 721, P4 2946, P5 270, P6 2891 |
| M15 | segtree: the right subtree never searched going down | P1 2279, P3 173, P4 2473, P6 2475 |

P1 and P6 kill all fifteen, P4 seven (M2, M3, M4, M5, M8, M14, M15),
P3 three (M6, M14, M15), P5 two (M12, M14) and P2 none. Every edit
still decides each jump by comparing values, so relabelling the values
without changing their order cannot reveal it; P2 guards against an arm
that depends on the values themselves, as the sorted vector's table and
the segment tree's ranks could. P4 sees an edit that mishandles equal
values, since from the old end the only jump is onto the equal value
after it.

Fourteen other edits were tried and set aside. Seven failed exactly the
same checks as a kept one: scan's even jump only to a strictly smaller
value and segtree's to a strictly smaller rank, as M3; sortedvec's
search finding the first value above and segtree's odd jump only to a
strictly larger rank, as M2; sortedvec's odd jump followed by another,
as M1; sortedvec's even jump onto an equal value followed by another
even jump, as M7; and segtree keeping the rightmost index on a tie, as
M11. Six were sound but beyond three an arm: ★ keeping the rightmost
index on a tie and not counting the last index; stack's even jump
followed by another and counting starts with an even jump; scan taking
the smallest value below; segtree never taking the smallest rank as an
odd jump target. One crashed and was not counted: sortedvec taking the
next larger value for an even jump when v is absent reads the table at
an absent value (`index out of bounds`).

## Verification

Every arm prints the same output as `odd_even_jumps.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 1.1 s (★) to 19.5 s (scan, quadratic), and the differential
29.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

`stack` was first written with `sort_by_key(|i| (arr[*i], *i))` and
`filter(|h| **h)`, Rust's spelling. `karac` refused each `*` that was
one too many with a diagnostic saying the closure's parameter is a
copied `i64` or a `ref bool`, so drop the `*` (core-semantics §5.10),
and the arm uses `|i| (arr[i], i)` and `|h| *h`.

## Benchmarks

The ★ arm keeps its values in a `SortedMap`, which C and Go do not have,
so the bench uses the stack arm, the same algorithm in all five
languages. The program makes 20 arrays of 20,000 random values below
10^5 once. In each of 10 rounds it runs the arm on every array, each
round starting from a different one, and folds every count into a
checksum. Every implementation prints `10 rounds over 20 arrays of 20000
values: 2178570 good starts, checksum 18105189`. Each call sorts two
index vectors with a (value, index) key: Kāra and Rust with
`sort_by_key`, C with `qsort` and a comparator, Go with `sort.Slice` and
Python with `sorted` and a key.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.11 to 1.24 s | 1.16 s |
| Rust (`rustc -O`) | 0.386 to 0.488 s | 0.451 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.373 to 0.515 s | 0.399 s |
| Go | 1.36 to 1.53 s | 1.45 s |
| Python | 5.4 s | |
| Kāra (`karac build --mir`) | 0.735 to 0.924 s | 0.768 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 7 times
Kāra's.

v2 took 1.92 times Rust's median time under overflow checks and 0.66
times C's. Under valgrind's cachegrind v2 ran 8,276 million
instructions and 985 million branches with 23.1 million mispredicted,
Rust with overflow checks 3,545 million, 636 million and 19.1 million,
and C 3,765 million, 958 million and 71.2 million, 116 million of its
branches indirect: `qsort` calls its comparator through a pointer. v2
ran 2.3 times Rust's instructions on the same sorts and stacks; where
they go was not measured.
