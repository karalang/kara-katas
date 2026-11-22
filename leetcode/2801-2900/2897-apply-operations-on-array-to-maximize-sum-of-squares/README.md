# 2897. Apply Operations on Array to Maximize Sum of Squares

You are given a **0-indexed** integer array `nums` and a **positive**
integer `k`.

You can do the following operation on the array **any** number of times:

- Choose any two distinct indices `i` and `j` and **simultaneously**
  update the values of `nums[i]` to `(nums[i] AND nums[j])` and
  `nums[j]` to `(nums[i] OR nums[j])`.

You have to choose `k` elements from the final array and calculate the
sum of their **squares**.

Return *the **maximum** sum of squares you can achieve*. Since the
answer can be very large, return it **modulo** `10^9 + 7`.

```
nums = [2, 6, 5, 8], k = 2  ->  261
nums = [4, 5, 4, 7], k = 3  ->  90
```

**Constraints:** `1 <= k <= nums.length <= 10^5`;
`1 <= nums[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `squares.kara` ★ | the operation moves the bits two values share into one of them and never changes how many values hold each bit. Squares favour the uneven, so the best stacks the bits: the first value takes every bit any value holds, the next every bit still held by another, and so on, k times, each bit's count spent one at a time |
| `squares_levels.kara` | the stacked values by formula: the t-th value, counting from 0, holds bit b exactly when more than t values held it, so each of the k values is read off the counts, as a `map` over `0..k` and a `fold` of the squares |
| `squares_runs.kara` | the bits sorted by how many values hold them: the stacked values stay the same between two counts, so each run of equal values is squared once and multiplied by its length, the rarest bit dropped from the value as each run ends |
| `squares_sorted.kara` | the stacked array itself: bit b is set in the first count(b) values of a `Vec.filled(n, 0)`, and the first k are squared |
| `squares_solution.kara` | a Rust solution as LeetCode's Rust users write it: `let mut cnt = [0; 31]` filled bit by bit, then k values assembled from it, `x * x % MOD` in `i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The stacking was checked first against a search in Python over every
array the operation can reach, 1500 random arrays of up to 5 values,
before any arm was written.

Every arm prints the same 4 lines: LeetCode's two examples; 10^5
values, LeetCode's most, all 10^9 with k 10^5, the powers of two in
turn with k 1 and k 30, and 1 to 10^5 with k 10^5; then 3000 random
arrays of 1 to 8 values from 1 to 15, and 100 of 1000 to 10^5 values up
to 10^9, every other one with two bits in each value, as a total and a
checksum. `squares.py` mirrors the ★ arm and its output is
byte-identical.

```
261 90
4900000 388912871 667386053 83550899
3000 small arrays: sums total 1188707, checksum 996545748
100 large arrays: sums total 48577459831, checksum 700347864
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: from the array sorted, every operation on every pair
tried, each array reached kept once in a `Set[String]`, and the largest
sum of the k largest squares over all of them. It draws 2000 random
arrays of 1 to 4 values from 1 to 15, then 50 of up to 3000, every
other one with two bits in each value, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 4 values, the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | every value doubled: four times the answer |
| P4 | the array written twice, with 2k: twice the answer |
| P5 | with k 1, the square of every value's bits together |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, sums total 22719666545: checksum
479971454, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python search over the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, three to the ★ arm and to the runs, two
to the levels and one each to the sorted arm and the solution, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All ten are killed,
each the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: bit 29 never counted | P3 50, P5 50, P6 50 |
| M2 | ★: a held bit never spent | P1 858, P6 899 |
| M3 | ★: the value added unsquared | P1 1970, P3 2050, P5 2020, P6 2020 |
| M4 | levels: a bit held one level too many | P1 2000, P3 2050, P4 2050, P5 2050, P6 2050 |
| M5 | levels: the levels counted from 1 | P1 1898, P4 1939, P5 1707, P6 1939 |
| M6 | runs: a count not capped at k | P1 708, P5 1413, P6 719 |
| M7 | runs: a spent bit kept in the value | P1 767, P6 808 |
| M8 | runs: the bits not sorted by count | P1 591, P6 632 |
| M9 | sorted: one value short | P1 1744, P4 1755, P5 2050, P6 1755 |
| M10 | solution: a held bit never spent | P1 858, P6 899 |

## Benchmarks

The bench draws 20 arrays of 10000 values, half up to 10^9 and half
with two bits in each value, k anywhere from 1 to the length, all
first, then answers each 20 times by the ★ arm in all five languages.
Every implementation prints `20 arrays of 10000, 20 rounds: sums total
183434332800, checksum 246016992`.

BENCHTAB

## Verification

All five arms print the same output as `squares.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as written. The harness first built
LeetCode's examples as `Vec.from([2, 6, 5, 8])`, Rust's way. Kāra has
no `Vec.from`, and the check refused it bare, `no associated function
'from' on type 'Vec'`, with nothing on what to write. It now says that
a list literal is already a `Vec` where no array is asked for, and
that any other sequence is copied by `.to_vec()`, and the fix writes
the one that applies (kara 0d28296389, B-2026-11-21-205); the harness takes the literals.

LeetCode's Rust template took `karac fix` over two runs, the wrapper
included, and the diff shows these: `struct Solution {}` came for the
`impl`; `Vec<..>` became `Vec[..]`; `for &x in &nums` became `for x in
ref nums` and `|&x|` lost its `&`; the wrapper's `as i64` on the
`i32` result went as a lossless cast the call already widens, and
`Solution::` took `.`. `[0; 31]`, `const MOD: i64` and `x |= 1 << i`
stayed as written.
