# 1619. Mean of Array After Removing Some Elements

Given an integer array `arr`, return *the mean of the remaining integers
after removing the smallest* `5%` *and the largest* `5%` *of the
elements.*

Answers within `10^-5` of the **actual answer** will be considered
accepted.

```
arr = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3]               ->  2.00000
arr = [6,2,7,5,1,2,0,3,10,2,5,0,5,5,0,8,7,6,8,0]              ->  4.00000
arr = [6,0,7,0,7,5,7,8,3,4,0,7,8,1,6,8,1,1,2,4,8,1,9,5,4,3,8,
       5,10,8,6,6,1,0,6,10,8,2,3,4]                           ->  4.77778
```

**Constraints:** `20 <= arr.length <= 1000`; `arr.length` is a multiple
of `20`; `0 <= arr[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `trim.kara` ★ | sort a copy, then the middle slice `sorted[k..n - k]` for `k = n / 20`, summed and divided by its length. O(n log n) |
| `trim_count.kara` | no sort: a count of each value up to the largest, walked from the bottom, each value's copies at sorted places `k` to `n - k - 1` added. O(n + m) for values below m |
| `trim_heaps.kara` | the whole sum less the `k` smallest and the `k` largest, each kept in a `PriorityQueue` of size `k` as the values stream past: a max-first queue of the values for the smallest, one of `Reverse { value: x }` for the largest. O(n log k) |
| `trim_solution.kara` | LeetCode's Rust template (`arr.sort_unstable()`, then `arr[k..n - k].iter().map(\|&x\| x as f64).sum::<f64>()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples, then the
values, the means' sum and a checksum of every mean (times 10^5,
rounded) for 3000 random arrays of up to 40 values below 11, 300 of up to
1000 below 100001, and 30 of up to 1000 below 6. `trim.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: one smallest value taken away, `n / 20` times, then one
largest, `n / 20` times, each found by a scan and taken with
`Vec.remove`; the mean of what is left. It checks 3000 random arrays of
20 to 200 values below 1 to 50, so ties at the cut are common. Every
random choice is drawn before any arm answers. Each mean is one division
of an exact integer sum, so the means are compared exactly, except under
P3, where the shifted mean and the shift added to the mean can round
apart and are held to 1e-9.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values shuffled leave the answer |
| P3 | every value raised by c raises the answer by c, to 1e-9 |
| P4 | the answer lies between the values at sorted places `n / 20` and `n - n / 20 - 1` |
| P5 | the array written twice over leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 183231700, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P4 is the weak one: a mean that takes
away too few or too many values, or the wrong ones, still lies between
the cut values unless it is far off.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 10% taken from each end, not 5% | P1 2906, P2 2906, P3 2906, P5 2906, P6 2906 |
| M2 | ★: the largest 5% kept | P1 2936, P2 2936, P3 2936, P5 2936, P6 2936 |
| M3 | ★: the sort left out | P1 2843, P2 2828, P3 2843, P5 2882, P6 2843 |
| M4 | count: the smallest values kept | P1 1471, P2 1471, P3 2989, P5 1471, P6 1471 |
| M5 | count: each value added once, not once per copy kept | P1 2934, P2 2934, P3 2999, P4 77, P5 2936, P6 2934 |
| M6 | count: the sorted place moved on by one value, not by its copies | P1 2906, P2 2906, P3 2997, P4 31, P5 2931, P6 2906 |
| M7 | heaps: one smallest value too few taken away | P1 1471, P2 1471, P3 2989, P5 1471, P6 1471 |
| M8 | heaps: half of each largest value taken away | P1 2936, P2 2936, P3 3000, P5 2936, P6 2936 |
| M9 | template: the array reversed, not sorted | P1 2843, P2 2828, P3 2843, P5 2882, P6 2843 |
| M10 | template: one value too many cut from the bottom | P1 1790, P2 1790, P3 2990, P5 1790, P6 1790 |

## Benchmarks

The bench makes 20000 random arrays of 1000 values below 100001, all of
it first. Then each one's trimmed mean by the ★ arm, a copy sorted and
its middle summed, in all five languages. Every implementation prints
`20000 arrays of 1000 values: means sum to 999919431.91667, checksum
389985012`. C sorts with `qsort` and a comparison function, Rust with
`sort` (stable), Go with `slices.Sort`, Python with `sorted`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9691a6290e` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.306 s |
| Kāra (`karac build`) | 0.313 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.375 s |
| Rust (`rustc -O`) | 0.397 s |
| Go | 1.234 s |
| C (`clang -O3`) | 1.467 s |
| Python | 9.8 s |

Kāra is ahead of both Rust builds here: its `sort` on `i32` and Rust's
stable `sort` take different algorithms, so this measures the sorts as
much as the languages. C's `qsort` calls its comparison through a
pointer for every comparison, about 10^4 of them per array, and is the
slowest compiled program; Go's `slices.Sort` is close behind it.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.265 s and 0.307 s on one run).

## Verification

All four arms print the same output as `trim.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`9691a6290e`.

## Writing it

The ★ and counting arms were written in Kāra and checked as written. The
heaps arm was written with Rust's `BinaryHeap.new()` and
`Reverse(x)`, and `karac fix` made them `PriorityQueue.max_first()` and
`Reverse { value: x }`, Kāra having no tuple structs. It was then
refused: `x` from `for x in arr.iter()` is a `ref i32`, and the literal
bound `Reverse`'s `T` to `ref i32` against the queue's `Reverse[i32]`,
"field 'value' has type 'ref i32', but the type parameter was already
bound to 'i32' by an earlier field of 'Reverse'". A non-generic struct,
a tuple and `Some(x)` copy a borrowed number into a slot of a fixed
type; a generic struct literal, a user enum's variant `Box2.B(x)` and its
struct-shaped `Box2.N { v: x }` did not. Kara 9691a6290e copies it in for
all three (B-2026-11-18-50). With no fixed type the literal still views its value,
as `Some(x)` alone does.

The Rust template took one `karac fix` of 9 edits: `struct Solution;` to
`struct Solution {}`, the parameter `mut arr: Vec<i32>` to
`arr: own Vec[i32]` with `let mut arr = arr;` at the body's start,
`sort_unstable()` to `sort()`, `|&x|` to `|x|`, `sum::<f64>()` to
`sum()`, and `Solution::` to `Solution.`. It then checks and agrees with
no hand edit.
