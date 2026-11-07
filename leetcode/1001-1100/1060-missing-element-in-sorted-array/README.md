# 1060. Missing Element in Sorted Array

Given an integer array `nums` sorted in ascending order with unique
values, and an integer `k`, return the `k`-th missing number starting from
the leftmost number of the array.

```
nums = [4,7,9,10], k = 1  ->  5      (5 is the first missing number)
nums = [4,7,9,10], k = 3  ->  8      (the missing numbers are 5, 6, 8, ...)
nums = [1,2,4],    k = 3  ->  6      (the missing numbers are 3, 5, 6, ...)
```

**Constraints:** `1 <= nums.length <= 5 * 10^4`; `1 <= nums[i] <= 10^7`;
`nums` is sorted ascending with unique values; `1 <= k <= 10^8`.

The answer can lie past the last value: in `[1, 2, 3]` nothing is missing
inside, so the first missing number is 4. The largest answer the
constraints allow is about `1.1 * 10^8`, which fits an `i32`.

## Approaches

Before index `i`, `missing(i) = nums[i] - nums[0] - i` numbers are
missing, and `missing` never decreases. The k-th missing number lies just
past the last index `i` with `missing(i) < k`, at `nums[i] + k - missing(i)`.

| file | mechanism |
|---|---|
| `missing.kara` ★ | a binary search on `missing(i)` through a closure over `nums`, keeping `missing(lo) < k <= missing(hi)`. O(log n) |
| `missing_linear.kara` | a walk over `nums.windows(2)`, taking each gap's `b - a - 1` from `k` until one holds what is left. O(n) |
| `missing_values.kara` | a binary search on the answer itself: up to `x`, `x - nums[0] + 1 - nums.partition_point(\|v\| v <= x)` numbers are missing. O(log(k + n) log n) |
| `missing_recursive.kara` | the bisection as recursion over `(lo, hi)`. O(log n) |
| `missing_iter.kara` | `nums.iter().enumerate().take_while(..).last()`: the last value with fewer than `k` missing before it. O(n) |
| `missing_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<i32>`, `usize` indices, a half-open search), carried to Kāra by `karac fix`. O(log n) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's three
examples and seven more; the sum and a checksum of the answers for 3000
arrays of 1 to 10 values with `k` to 20 and for 3000 dense arrays of 1 to
50 values with `k` to 60; the same for 100 arrays of 50000 values with 10
values of `k` each, two of them up to `10^8`; every `k` from 1 to 3000
against one array of 1000 values; and 50000 consecutive values, with
nothing missing inside. `missing.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the numbers from `nums[0]` upward, one at a time, those not in
a `Set` of `nums` counted until the k-th. It checks 3000 problems: 1500 of
1 to 10 values with gaps up to 5 and `k` up to 30, and 1500 of 1 to 300
values, dense (gaps up to 2) or sparse (gaps up to 60), with `k` up to 40
past the last value. Every random choice of a problem is drawn before any
arm answers, so a wrong arm cannot change the problems the others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally (when the walk is at most 3000 numbers) |
| P2 | every value moved up by the same amount moves the answer by it |
| P3 | with the answer added to `nums`, the k-th missing number is the (k+1)-th of `nums` alone |
| P4 | a value above the answer removed from `nums`, or one added past both the answer and the last value, leaves the answer |
| P5 | the (k+1)-th missing number lies above the k-th, with exactly as many values of `nums` between them as their distance less one |
| P6 | each arm agrees with at least three of the other five |

The differential prints `3000 problems: checksum 490579524, 114078 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the k-th equal to the last count taken as past the end | P1 56, P3 56, P4 345, P5 41, P6 56 |
| M2 | ★: the answer counted from the upper bound | P1 1019, P3 1600, P4 1467, P5 574, P6 1600 |
| M3 | ★: the search stopped one step early | P1 448, P3 776, P4 2705, P5 287, P6 710 |
| M4 | linear: one too few taken from each gap | P1 2149, P3 3000, P5 151, P6 2732 |
| M5 | linear: counted down from the gap's top | P1 500, P3 811, P4 1582, P5 1145, P6 1072 |
| M6 | linear: past the end off by one | P1 1394, P3 59, P4 1511, P6 1400 |
| M7 | values: a present value counted missing | P1 633, P3 3000, P5 641, P6 641 |
| M8 | values: the first value with k missing passed by | P1 2413, P6 3000 |
| M9 | values: the lower bound one too high | P1 53, P3 18, P5 35, P6 53 |
| M10 | recursive: the index left out of the count | P1 2149, P3 3000, P6 2732 |
| M11 | recursive: past the end, the count missing inside ignored | P1 1207, P3 1449, P4 1308, P5 56, P6 1213 |
| M12 | iter: only the first two values looked at | P1 1906, P3 2781, P6 2486 |
| M13 | iter: the walk capped at fifty values | P1 488, P3 917, P6 901 |
| M14 | solution: an index with exactly k missing passed by | P1 558, P3 586, P4 101, P5 579, P6 586 |
| M15 | solution: every value converted one too low | P1 2413, P3 694, P4 271, P5 630, P6 3000 |

P1 and P6 kill all fifteen, P3 fourteen, P5 ten, P4 eight and P2 none.
P2 would see an arm that reads a value absolutely rather than from
`nums[0]`, and none of the thirty edits does: each is off by a count or an
index, which moving every value leaves alone. P3 misses only M8, which
answers the (k+1)-th missing number for every `k`: adding that number to
`nums` and asking again is consistent with the same mistake, and so is
every other property but the literal reading and the vote. P4 sees the
edits whose answer depends on the values past it (M2, M3, M5, M14) or on
where the last value lies (M1, M6, M11, M15).

Thirteen of the other fifteen fail exactly as a kept one does. The ★ and
recursive arms keeping an index with exactly `k` missing below fail as
M14; the ★ arm's count off by one fails as M8, and the recursion stopping
early as M3; the gaps one too wide, the answer search's upper bound too
low, and the iterator arm leaving out the index or taking the first value
as the last fail as M10; the Rust arm taking the `k`-th equal to the last
count as past the end fails as M1, its answer from the first index past and
the recursion's answer one too high as M2, its count ignored past the end
as M11, and the answer search returning its lower bound as M15. The gap
walk passing the top of a gap and the iterator arm taking values with
exactly `k` missing fail alike, in a group of their own.

## Verification

Every arm prints the same output as `missing.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. Under `karac __mir-run` the three logarithmic arms take 4.4 s (recursive)
to 5.0 s (values), the linear ones 34.1 s (gaps), 63.9 s (the Rust template,
whose caller converts 50000 values on each of its 1000 large calls) and
76.1 s (iterator), and the differential 10.3 s, all at kara `05b89e4f7f`.

The ★ arm and four others were written in Kāra and checked clean. The
Rust arm was written as LeetCode's Rust template (`struct Solution;`,
`Vec<i32>`, `|i: usize| -> i32 { .. }`, `let (mut lo, mut hi) = (0usize,
n - 1);`, `&Vec<i64>`, `|&x| x as i32`, `Solution::missing_element`) and
reaches a clean check through `karac fix` alone, in three rounds: the
syntax first (fourteen fixes), then the `usize` closure parameter and the
`0usize` suffix that met `len()`'s `i64`, then the `ref` parameter. The
suffix had no fix before this kata: `karac fix` rewrote a written `usize`
type to `i64` but left `0usize` in place, and six comparison, arithmetic
and coercion errors stayed (kara `05b89e4f7f`,
`tests/kata_1060_check_gaps.rs`).

## Benchmarks

The bench builds 50 arrays of 50000 values once in all five languages,
each with gaps of 1 up to somewhere between 2 and 149, and asks the ★ arm for 200000 values of `k`
in each, up to 1000 past the last value: ten million calls. Every
implementation prints `10000000 calls: sum 9552369862599, checksum
645760616`. Each call is a binary search of about 16 steps over 400 KB.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `05b89e4f7f` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.072 to 1.144 s | 1.116 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.119 to 1.270 s | 1.159 s |
| Rust (`rustc -O`) | 1.099 to 1.243 s | 1.170 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.304 to 1.458 s | 1.328 s |
| Kāra (`karac build`) | 1.281 to 1.453 s | 1.360 s |
| Go | 1.395 to 1.480 s | 1.430 s |
| Python | 40.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.349 s) is below its real time.

Kāra is 1.15x Rust under overflow checks. Building the arrays and drawing
the values of `k` take 0.06 s in both, so the gap is in the search. It is
not in the instructions: on a run of a hundredth the size, callgrind counts
37.9 million for Kāra and 37.2 million for Rust, and both compile the
search to the same loop of a load, two checked subtractions, a compare and
a branch on it, with no `cmov`. Kāra keeps one more overflow check, on
`lo + (hi - lo) / 2`, which Rust's LLVM proves cannot overflow, and the two
lay out the branch's taken side differently. The search's branch goes
either way at random, so the time is likely mostly mispredictions, where
a small difference in layout shows (inferred from the equal counts, not
measured).
