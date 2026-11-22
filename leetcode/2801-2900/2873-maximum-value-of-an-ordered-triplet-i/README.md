# 2873. Maximum Value of an Ordered Triplet I

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

**Constraints:** `3 <= nums.length <= 100`; `1 <= nums[i] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `triplet.kara` ★ | one pass, k moving right, carrying the largest value seen so far, for i, and the largest nums[i] - nums[j] seen so far, for the pair before k; every value is positive, so the best k for a pair is its largest. Each value is a k before it is a j, and a j before it is an i |
| `triplet_brute.kara` | every triplet i < j < k tried, with 100 values at most: the statement as written |
| `triplet_sides.kara` | for each middle j, the best i is the largest value left of it and the best k the largest right of it: a prefix maximum and a suffix maximum, each one pass, then every j tried, raised to 0 |
| `triplet_fold.kara` | the ★ arm's pass as one `fold` over (best, largest, largest gap) |
| `triplet_solution.kara` | a Rust solution as LeetCode's Rust users write it: three nested loops, `(nums[i] - nums[j]) as i64 * nums[k] as i64`, kept by `ans.max(..)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 100
values, LeetCode's most, rising, falling, and 10^6 with a 1 between;
then 3000 random arrays of 3 to 8 values from 1 to 9, and 3000 of 3 to
100 values up to 10^6, as a total of the answers and a checksum.
`triplet.py` mirrors the ★ arm and its output is byte-identical.

```
77 133 0
0 2450 999999000000
3000 short arrays: values total 81163, checksum 416028229
3000 long arrays: values total 2508878265385415, checksum 58310688
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every i < j < k tried, the largest (nums[i] - nums[j]) *
nums[k] kept, 0 when every one is negative. It draws 2000 random arrays
of 3 to 8 values from 1 to 9, then 50 of 3 to 100 values up to 10^6,
all before any arm answers; the literal reading is asked only of the
first 2000.

| | property |
|---|---|
| P1 | up to 8 values, the answer is the literal reading's |
| P2 | every value doubled: four times the answer |
| P3 | a 1 put in front: the same answer |
| P4 | the values sorted rising: 0 |
| P5 | from 0 to the largest value squared, and at least (nums[0] - nums[1]) * nums[n - 1] |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, values total 41834743760162:
checksum 977993825, 61500 checks over 5 arms: 0 failures` under every
lane in Verification, and a Python reading of the same cases gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, three to the sides arm, two each to the
★ arm, the brute force and the solution, and one to the fold, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All ten are killed,
each the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gap taken with k as j | P1 364, P6 365 |
| M2 | ★: the gap not kept at its largest | P1 452, P5 78, P6 493 |
| M3 | brute: i from 1 | P1 691, P3 700, P5 451, P6 700 |
| M4 | brute: the last k left out | P1 819, P5 276, P6 824 |
| M5 | sides: the left maximum taken from 1 to i | P1 691, P3 700, P5 451, P6 700 |
| M6 | sides: the right maximum not set at n - 2 | P1 819, P5 276, P6 824 |
| M7 | sides: a negative best not raised to 0 | P1 197, P3 103, P4 773, P5 197, P6 197 |
| M8 | fold: the gap taken the wrong way round | P1 1858, P3 1423, P4 2050, P6 1908 |
| M9 | solution: nums[j] taken for nums[k] | P1 1625, P5 460, P6 1675 |
| M10 | solution: the answer started at -1 | P1 197, P2 197, P3 59, P4 773, P5 197, P6 197 |

## Benchmarks

The bench draws 100000 arrays of 100 values, LeetCode's most, each from
1 to 10^6, all first, then answers each 30 times by the ★ arm in all
five languages. Every implementation prints `100000 arrays of 100, 30
rounds: values total 2847359345282861940, checksum 488245773`.

BENCHTAB

## Verification

All five arms print the same output as `triplet.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, the `fold` over a
tuple destructured in the closure's parameter among them.

LeetCode's Rust template took 7 `karac fix` edits over two runs, the
wrapper included: `struct Solution {}` came for the `impl`; `Vec<..>`
became `Vec[..]` in both signatures; the wrapper's `|&x|` lost its `&`
and `Solution::` took `.`. `(nums[i] - nums[j]) as i64 * nums[k] as
i64`, a cast of an `i32` difference, was accepted as written.
