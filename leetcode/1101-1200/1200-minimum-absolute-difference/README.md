# 1200. Minimum Absolute Difference

Given an array of distinct integers `arr`, find all pairs of elements
with the minimum absolute difference of any two elements. Return a list
of pairs in ascending order (with respect to pairs), each pair `[a, b]`
following: `a, b` are from `arr`; `a < b`; `b - a` equals the minimum
absolute difference of any two elements in `arr`.

```
arr = [4, 2, 1, 3]                        ->  [[1, 2], [2, 3], [3, 4]]
arr = [1, 3, 6, 10, 15]                   ->  [[1, 3]]
arr = [3, 8, -10, 23, 19, -4, -14, 27]    ->  [[-14, -10], [19, 23], [23, 27]]
```

**Constraints:** `2 <= arr.length <= 10^5`; `-10^6 <= arr[i] <= 10^6`;
the values are distinct.

The arms are `fn minimum_abs_difference(arr: own Vec[i64]) ->
Vec[Vec[i64]]`, or `arr: Vec[i64]` for an arm that only reads it. The two
Rust arms keep the method LeetCode gives Rust users, on `Vec<i32>`,
inside `impl Solution`, and a one-line `minimum_abs_difference` calls
it.

## Approaches

Sorted, the least difference of any two values lies between neighbours,
and the pairs that have it come out in order with the smaller first.

| file | mechanism |
|---|---|
| `minimum_abs_difference.kara` ★ | the values sorted, one pass for the least difference between neighbours and a second collecting the neighbours that have it. O(n log n) |
| `minimum_abs_difference_onepass.kara` | sorted, then a single pass: a difference smaller than any so far clears the pairs and starts them afresh, and an equal one adds to them |
| `minimum_abs_difference_marks.kara` | no comparison sort: the values marked in a `Vec[bool]` over their own range, least to greatest, and walked in order, which visits them sorted. O(n + range), the range at most `2 * 10^6 + 1` |
| `minimum_abs_difference_windows.kara` | iterator chains over `windows(2)` of the sorted values: the least difference by `min`, then the windows that have it by `filter` |
| `minimum_abs_difference_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut arr: Vec<i32>`, `sort_unstable`, the least of `windows(2)`, then the windows that have it as `vec![w[0], w[1]]`), carried to Kāra by `karac fix` |
| `minimum_abs_difference_loop.kara` | another Rust solution, one indexed loop (`arr: Vec<i32>` rebound by `let mut arr = arr`, `i32::MAX` to start, `res.clear()` on a smaller difference), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 9 lines: LeetCode's three examples; two values,
`[5, -5]`, and the constraints' two ends, `[1000000, -1000000]`; an
array whose last value falls between two others (`[0, 2, 4, 6, 8, 7]`:
`[[6, 7], [7, 8]]`); 1000 random arrays of 2 to 21 distinct values
(`1000 random arrays: 3665 pairs, checksum 266723484`); the 100000 even
numbers from -100000, given largest first (`99999 pairs`); and 100000
random distinct values from -10^6 to 10^6 (`4934 pairs, first [-999428,
-999427]`). `minimum_abs_difference.py` mirrors the ★ arm with `sorted`,
and its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and onepass arms check clean as written. The marks
arm, which only reads its values, takes one fix, the harness's
`.clone()` on its argument dropped. The windows arm was first written as
Rust chains `windows(2)`; Kāra's `windows` gives a `Vec`, and `karac fix`
puts `.into_iter()` after each of the two calls. The solution arm takes
one round of 13 fixes (among them `mut arr: Vec<i32>` to `arr: own
Vec[i32]` with a `let mut arr = arr;`, `sort_unstable` to `sort`,
`windows(2)` to `windows(2).into_iter()`, `vec![w[0], w[1]]` to `[w[0],
w[1]]`, and `Solution::` to `Solution.`), and the loop arm one round of
14 (among them `arr: Vec<i32>` rebound by `let mut arr = arr` to `own`,
`i32::MAX` to `i32.MAX`, `Vec::new()` to `Vec.new()`, and `vec![arr[i -
1], arr[i]]` to `[arr[i - 1], arr[i]]`). Both outputs match. The kata
found no gap: both Rust arms take their `Vec<i32>` by value, and `karac
fix` keeps that as `own` in each, the reading kata 1199's row
B-2026-11-18-31 asks for where the Rust consumes the vector instead.

The marks arm was first written over the whole range of the
constraints, a fixed `Vec.filled(2000001, false)` from -10^6; that is
correct, and under `karac __mir-run` the 1000 random arrays, each
walking two million marks, took 283 s. Over each array's own range,
from its least value to its greatest, the arm runs in under a second
and gives the same answers.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of values weighed for the least difference of any
two, then every ordered pair `[a, b]` with `b - a` equal to it, and the
pairs sorted. 2000 random arrays of 2 to 20 distinct values from -10,
-50 or -1000 to the same above.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least one pair and at most `n - 1`, each rising by one same difference, the pairs in order |
| P3 | the values reversed give the same |
| P4 | the values negated give the pairs mirrored: each `[a, b]` to `[-b, -a]`, in the reverse order |
| P5 | the values doubled give the pairs doubled |
| P6 | the values 500 higher give the pairs 500 higher |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 arrays: checksum 339777176,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same arrays, weighing every pair, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: pairs one wider kept too | P1 911, P2 911, P5 911, P7 4555 |
| S2 | ★: each pair the larger first | P1 2000, P2 2000, P7 10000 |
| O1 | onepass: the pairs never started afresh | P1 1266, P2 1266, P4 1633, P7 1266 |
| O2 | onepass: an equal difference starts afresh | P1 868, P4 868, P7 868 |
| K1 | marks: the second value never visited | P1 444, P2 7, P4 646, P5 444, P7 444 |
| K2 | marks: the last value never moves on | P1 1683, P4 1889, P7 1683 |
| W1 | windows: the greatest difference | P1 1887, P7 1887 |
| W2 | windows: the pairs without it | P1 2000, P2 1710, P7 2000 |
| X1 | solution: each pair its smaller twice | P1 2000, P2 2000, P4 2000, P7 2000 |
| X2 | solution: the values left unsorted | P1 1921, P2 1921, P3 2000, P4 2000, P7 1921 |
| L1 | loop: the first pair skipped | P1 734, P2 111, P4 1003, P7 734 |
| L2 | loop: the pairs never started afresh | P1 1266, P2 1266, P4 1633, P7 1266 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. O1 and L2 are one fault in two arms, the pairs of a larger
difference kept after a smaller one is found, and fail alike. P4, the
values negated, catches every fault that treats the two ends of the
sorted values differently (a pair kept or dropped by where it falls, or
the walk starting late), since negating turns the order around; S1, S2,
W1 and W2 treat every pair alike and pass it. P6, the values shifted,
catches none: every arm, mutated or not, looks only at differences, and
a shift moves no difference. P5, the values doubled, catches only S1,
whose `least + 1` does not double with the values. W1 passes on the 113
arrays whose neighbours are all one difference apart, two values among
them, where the greatest difference is the least.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 20 arrays of 10^5 distinct values, the constraints' most, built
once, from -10^6 to 10^6, -10^5 to 10^5 and -60000 to 60000 in turn;
then 10 rounds over the arrays, each call sorting its own copy, every
pair folded into a checksum. Every program prints `10 rounds of 20
arrays of 100000 values: checksum 112533360`. The sort is most of the
work: C sorts with `qsort`, Rust with the standard `sort`, Go with
`slices.Sort`, and Python with `sorted`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.653 to 0.854 s | 0.704 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.629 to 0.816 s | 0.704 s |
| Rust (`rustc -O`) | 0.541 to 0.736 s | 0.588 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.476 to 0.705 s | 0.597 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.580 to 0.772 s | 0.595 s |
| C (`clang -O3`) | 2.294 to 2.566 s | 2.374 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.978 to 2.434 s | 2.313 s |
| Go | 1.861 to 2.194 s | 1.895 s |
| Python | 11.85 to 11.87 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 15% ahead of Kāra (0.597 s
against 0.704 s), and the two ranges overlap. C takes about 3.4x Kāra's
time, `qsort` calling its comparison through a pointer for every pair it
weighs, and Go about 2.7x; no profile was taken. Python takes about 17x
Kāra's time.
