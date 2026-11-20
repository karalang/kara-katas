# 1722. Minimize Hamming Distance After Swap Operations

You are given two integer arrays, `source` and `target`, both of length
`n`. You are also given an array `allowedSwaps` where each
`allowedSwaps[i] = [ai, bi]` indicates that you are allowed to swap the
elements at index `ai` and index `bi` **(0-indexed)** of array `source`.
Note that you can swap elements at a specific pair of indices
**multiple** times and in **any** order.

The **Hamming distance** of two arrays of the same length, `source` and
`target`, is the number of positions where the elements are different.
Formally, it is the number of indices `i` for `0 <= i <= n-1` where
`source[i] != target[i]` **(0-indexed)**.

Return *the **minimum Hamming distance** of* `source` *and* `target`
*after performing **any** amount of swap operations on array* `source`*.*

```
source = [1,2,3,4], target = [2,1,4,5], allowedSwaps = [[0,1],[2,3]]                  ->  1
source = [1,2,3,4], target = [1,3,2,4], allowedSwaps = []                             ->  2
source = [5,1,2,4,3], target = [1,5,4,2,3], allowedSwaps = [[0,4],[4,2],[1,3],[1,4]]  ->  0
```

**Constraints:** `n == source.length == target.length`;
`1 <= n <= 10^5`; `1 <= source[i], target[i] <= 10^5`;
`0 <= allowedSwaps.length <= 10^5`; `allowedSwaps[i].length == 2`;
`0 <= ai, bi <= n - 1`; `ai != bi`.

## Approaches

| file | mechanism |
|---|---|
| `hamming.kara` ★ | swaps compose, so the places joined by a chain of allowed swaps can trade values in any order, and nothing crosses between such groups: a group's most matches is the common part of its source and target values, as multisets. A union-find with path halving and union by size finds the groups, and a `Map` keyed by (group, value) counts the source's values for the target's to take. O((n + m) α(n)) |
| `hamming_groups.kara` | the swaps as an adjacency list, each group gathered by a walk with a stack, and its source and target values sorted and matched by two cursors. O(n log n + m) |
| `hamming_pairs.kara` | each place labelled with its group by a breadth-first walk over a `VecDeque`, each array turned into (label, value) pairs, and the two lists sorted and merged once for every group's matches. O(n log n + m) |
| `hamming_solution.kara` | a Rust solution as LeetCode's Rust users write it, a nested recursive `find` with path compression over a `Vec<usize>`, a `HashMap<usize, HashMap<i32, i32>>` of each group's counts filled with `entry().or_insert_with(HashMap::new)`, and `if let Some(c) = g.get_mut(&target[i])`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one value,
and swaps that join every place; then the distances summed and a
checksum for 3000 random problems of up to 8 values up to 4 and up to 6
swaps, 300 of up to 1000 values up to 20 and up to 800 swaps, and 10 of
up to `10^5` values up to `10^5` and up to `10^5` swaps. `hamming.py`
mirrors the ★ arm and its output is byte-identical.

```
1
2
0
1
0
3000 problems of up to 8 values up to 4: distances sum to 8051, checksum 1869750
300 problems of up to 1000 values up to 20: distances sum to 92050, checksum 460289132
10 problems of up to 100000 values up to 100000: distances sum to 130324, checksum 713840238
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every arrangement of the source that the allowed swaps reach,
any number of times in any order, found by a breadth-first walk with a
`Set` of the arrangements seen; the least Hamming distance among them.
It checks 3000 random problems: two arrays of 1 to 6 values from 1 to 3
and up to 4 allowed swaps of two different places. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the source and the target swapped give the same answer |
| P3 | the swaps listed in reverse, each pair turned round, give the same answer |
| P4 | with no swaps allowed, the answer is the places that differ |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 306064401, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same walk over tuples, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M7 and M9 all leave every place
in a group of its own, and fail the very same checks; no swap allowed
(P4) is the one case they get right.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a union that joins nothing | P1 778, P5 778 |
| M2 | ★: a source value taken when none is left | P1 641, P2 936, P5 641 |
| M3 | ★: a target value looked for under its own place, not its group | P1 1273, P2 662, P3 637, P5 1273 |
| M4 | groups: the walk never goes past a place's first neighbours | P1 1421, P5 1421 |
| M5 | groups: a match moves only the source's cursor | P1 606, P2 958, P5 606 |
| M6 | groups: the source's values left unsorted | P1 675, P2 732, P3 52, P5 675 |
| M7 | pairs: each place reached labelled with itself | P1 778, P5 778 |
| M8 | pairs: a mismatch moves both cursors | P1 336, P5 336 |
| M9 | solution: a union that joins nothing | P1 778, P5 778 |
| M10 | solution: a matched value never taken from its count | P1 641, P2 958, P5 641 |

## Benchmarks

The bench draws 10 random problems of `10^5` values up to `10^5` in
each array and `10^5` swaps, LeetCode's largest, all of them first, then
answers each 5 times by the ★ arm in all five languages; each answer
builds its union-find and its map anew. Every implementation prints `10
problems of 100000 values and 100000 swaps, 5 rounds: distances sum to
3300310, checksum 993145194`. C has no map: its mirror probes a table of
`2^18` slots linearly, the (group, value) key packed into one word and
hashed by one multiply, which is less work than Kāra's SipHash `Map`,
Rust's SipHash `HashMap` or Go's `map` do. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.214 s |
| Rust (`rustc -O`) | 0.572 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.589 s |
| Kāra (`karac build`) | 0.635 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.682 s |
| Go | 1.067 s |
| Python | 10 s |

The sequential Kāra build takes 1.19x Rust's time and 1.16x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.214 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.607 s and 0.634 s on one
run).

## Verification

All four arms print the same output as `hamming.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm first swapped its two roots as Rust does, `(a, b) = (b, a);`.
In Kāra a parenthesized tuple is a value, not a place; `karac check`
said so and to drop the parentheses, and `karac fix` wrote
`a, b = b, a;`.

The groups and pairs arms first wrote their two cursors
`let (mut i, mut j) = (0, 0);`. Kāra puts `mut` before the whole
pattern; `karac fix` wrote `let mut (i, j) = (0, 0);`. Both also pushed
`swap[1] as i64` onto a `Vec[i64]`; the `lossless_cast` lint saw that
the `i32` widens by itself, and the fix dropped the casts.

LeetCode's Rust template took one `karac fix` of 42 edits:
`struct Solution {}` added, `use std::collections::HashMap;` deleted,
the nested `fn find` moved out of the method to the top level, `usize`
written `i64` throughout, `Vec<..>` and `HashMap<usize, HashMap<i32,
i32>>` written `Vec[..]` and `Map[i64, Map[i32, i32]]`,
`HashMap::new()` written `Map.new()` (and `or_insert_with(HashMap::new)`
`or_insert_with(Map.new)`), `&mut p` written `mut p`, `for s in
&allowed_swaps` written `for s in ref allowed_swaps`, the casts
`s[0] as usize` dropped, and the `&` on `get_mut(&r)` and
`get_mut(&target[i])` dropped.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
