# 2874. Maximum Value of an Ordered Triplet II

You are given a **0-indexed** integer array `nums`.

Return ***the maximum value over all triplets of indices*** `(i, j, k)`
*such that* `i < j < k`*.* If all such triplets have a negative value,
return `0`.

The **value of a triplet of indices** `(i, j, k)` is equal to
`(nums[i] - nums[j]) * nums[k]`.

```
nums = [12,6,1,2,7]   ->  77
nums = [1,10,3,4,19]  ->  133
nums = [1,2,3]        ->  0
```

**Constraints:** `3 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^6`.

The statement is [2873](../2873-maximum-value-of-an-ordered-triplet-i/)'s
with 10^5 values rather than 100, so the triple loop is gone and every
arm here is one or two passes.

## Approaches

| file | mechanism |
|---|---|
| `triplet.kara` ★ | one pass, k moving right, carrying the largest value seen so far, for i, and the largest nums[i] - nums[j] seen so far, for the pair before k; every value is positive, so the best k for a pair is its largest |
| `triplet_sides.kara` | for each middle j, the best i is the largest value left of it and the best k the largest right of it: a prefix maximum and a suffix maximum, each one pass, then every j tried, raised to 0 |
| `triplet_fold.kara` | the ★ arm's pass as one `fold` over (best, largest, largest gap) |
| `triplet_scan.kara` | the sides arm's two maxima as iterator chains: `scan` hands on the largest value before each place, once forward and once from the back, and the three sequences zipped, every middle j tried, raised to 0 |
| `triplet_solution.kara` | a Rust solution as LeetCode's Rust users write it: a suffix maximum in a `vec![0; n + 1]`, then the middle j walked with the prefix maximum, each product taken `as i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 10^5
values, LeetCode's most, rising, falling, and 10^6 with a 1 between;
then 3000 random arrays of 3 to 8 values from 1 to 9, and 100 of 1000
to 10^5 values up to 10^6, every other one falling with noise, as a
total of the answers and a checksum. `triplet.py` mirrors the ★ arm and
its output is byte-identical.

```
77 133 0
0 2499950000 999999000000
3000 short arrays: values total 81869, checksum 593639146
100 long arrays: values total 63683394727348, checksum 152169814
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every i < j < k tried, the largest (nums[i] - nums[j]) *
nums[k] kept, 0 when every one is negative. It draws 2000 random arrays
of 3 to 8 values from 1 to 9, then 50 of 3 to 20000 values up to 10^6,
every other one falling with noise, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 values, the answer is the literal reading's |
| P2 | every value doubled: four times the answer |
| P3 | a 1 put in front: the same answer |
| P4 | the values sorted rising: 0 |
| P5 | from 0 to the largest value squared, and at least (nums[0] - nums[1]) * nums[n - 1] |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, values total 31739538493343:
checksum 687188218, 61500 checks over 5 arms: 0 failures` under every
lane in Verification, and a Python reading of the same cases gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, three to the solution, two each to the
★ arm, the sides and the scan, and one to the fold, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gap taken with k as j | P1 349, P6 349 |
| M2 | ★: the gap not kept at its largest | P1 472, P5 85, P6 520 |
| M3 | sides: the left maximum taken from 1 to i | P1 734, P3 736, P5 476, P6 736 |
| M4 | sides: the right maximum not set at n - 2 | P1 814, P5 283, P6 814 |
| M5 | fold: the gap taken the wrong way round | P1 1877, P3 1473, P4 2050, P6 1927 |
| M6 | scan: the right maxima left back to front | P1 1005, P3 378, P6 1048 |
| M7 | scan: the left maximum taken for k | P1 1580, P5 110, P6 1630 |
| M8 | solution: the suffix maximum taken from j | P1 129, P6 129 |
| M9 | solution: the prefix maximum started at nums[1] | P1 734, P3 736, P5 476, P6 736 |
| M10 | solution: j from 2 | P1 874, P3 844, P5 346, P6 874 |

## Benchmarks

The bench draws 50 arrays of 10^5 values, LeetCode's most, up to 10^6,
every other one falling with noise, all first, then answers each 20
times by the ★ arm in all five languages. Every implementation prints
`50 arrays of 100000, 20 rounds: values total 650711365961660, checksum
98208093`.

BENCHTAB

## Verification

All five arms print the same output as `triplet.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written: the `scan` closures
return `Some((state, output))`, Kāra's form, and the zip destructures
`|((v, l), r)|`.

LeetCode's Rust template took 10 `karac fix` edits over two runs, the
wrapper included: `struct Solution {}` came for the `impl`; `Vec<..>`
became `Vec[..]` in both signatures; `vec![0; n + 1]` became
`Vec.filled(n + 1, 0)`; the wrapper's `|&x|` lost its `&` and
`Solution::` took `.`. The fix also took out both `as i64` casts in
`(pre - nums[j]) as i64 * suf[j + 1] as i64` as redundant: `suf`, filled
from an untyped `0`, is a `Vec[i64]`, so the `i32` difference widens to
meet it. A product of two `i32`s with nothing wider beside it keeps its
casts: `x as i64 * y as i64` is left alone, as it must be, since `let z: i64
= x * y` multiplies in `i32` and stops on the overflow at 10^6 squared.
