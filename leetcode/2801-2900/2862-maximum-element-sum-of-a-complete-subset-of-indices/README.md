# 2862. Maximum Element-Sum of a Complete Subset of Indices

You are given a **1-indexed** array `nums` of `n` integers.

A set of numbers is **complete** if the product of every pair of its
elements is a perfect square.

For a subset of the indices set `{1, 2, ..., n}` represented as `{i1,
i2, ..., ik}`, we define its **element-sum** as: `nums[i1] + nums[i2] +
... + nums[ik]`.

Return *the **maximum element-sum** of a **complete** subset of the
indices set* `{1, 2, ..., n}`.

A perfect square is a number that can be expressed as the product of
an integer by itself.

```
nums = [8,7,3,5,7,2,4,9]       ->  16
nums = [8,10,3,8,1,13,7,9,4]   ->  20
```

**Constraints:** `1 <= n == nums.length <= 10^4`; `1 <= nums[i] <=
10^9`.

## Approaches

| file | mechanism |
|---|---|
| `complete.kara` ★ | two indices multiply to a square exactly when they share their square-free part k, so the complete sets are the indices k·1², k·2², k·3², ... for each k; every k from 1 to n is walked up its squares and the best sum kept |
| `complete_sieve.kara` | each index's square-free part found by factoring with a sieve of smallest prime factors, a prime that divides an odd number of times kept in; the values added up by part in a `Map`, the best taken from `values().max()` |
| `complete_squares.kara` | each index's square-free part by dividing out squares: each j from 2 up while j² is no more than what is left, divided out as often as it goes; the sums kept in a vector indexed by part |
| `complete_groups.kara` | the indices sorted by square-free part, found as i over the largest square dividing it, tried from an integer square root through `f64` down, so each part's indices lie together; `chunk_by` on equal parts splits them into the complete sets, each summed |
| `complete_solution.kara` | a Rust solution as LeetCode's Rust users write it: `for k in 1..=n`, an inner `while k * j * j <= n` over `usize` with `as i64` on each value, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 10^4
values of 10^9, LeetCode's most, and 10^4 values each its own index;
then 3000 random arrays of 1 to 30 values up to 20, and 30 of 1000 to
10^4 values up to 10^9, as a total of the best sums and a checksum.
`complete.py` mirrors the ★ arm and its output is byte-identical.

```
16 20
100000000000 338350
3000 short arrays: best sums total 109301, checksum 519779928
30 long arrays: best sums total 967453867399, checksum 652039223
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: for arrays of up to 9, every set of indices tried, kept
when every pair of its indices multiplies to a perfect square, found by
counting up to the root, and the best sum taken. It draws 2000 random
arrays of 1 to 9 values up to 20, then 50 of up to 3000 values up to
10^9, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 9 values, the answer is the literal reading's |
| P2 | every value doubled: twice the answer |
| P3 | one value raised by d: the answer rises by no more than d, and does not fall |
| P4 | the first half of the array alone: no more than the answer |
| P5 | from the largest value to the sum of all of them |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, best sums total 803563630758:
checksum 179256195, 61500 checks over 5 arms: 0 failures` under every
lane in Verification, and a Python reading of the same cases, every
subset tried for the first 2000, gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the squares started at 2², the index k itself left out | P1 2000, P5 1605, P6 2050 |
| M2 | ★: the walk stopping before the last index | P1 874, P5 516, P6 875 |
| M3 | sieve: every prime kept, not only odd powers | P1 1130, P6 1180 |
| M4 | sieve: the sieve stopping one prime short | P1 325, P6 325 |
| M5 | squares: j squared divided out once only | P6 50 |
| M6 | squares: the largest sum not taken, the first part's | P1 646, P5 569, P6 647 |
| M7 | groups: the part taken as i over the root, not its square | P1 1122, P6 1172 |
| M8 | groups: neighbours grouped by index, not part | P1 1007, P6 1057 |
| M9 | solution: one square too few for each k | P1 2000, P5 1591, P6 2050 |
| M10 | solution: k stopping short of n | P1 452, P5 452, P6 452 |

## Benchmarks

The bench draws 200 arrays of 10^4 values up to 10^9, LeetCode's most,
all of them first, then answers each 50 times by the ★ arm in all five
languages. Every implementation prints `200 arrays of 10000, 50
rounds: best sums total 465658601486750, checksum 501181893`.

BENCHTAB

## Verification

All five arms print the same output as `complete.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The groups arm, as first written, summed the groups with
`order.chunk_by(|a, b| a.0 == b.0).map(..)`, and `karac check` reported
E0236, `chunk_by` returning a `Vec` of the groups where Rust's returns
an iterator, so the chain needs `.into_iter()`, which `karac fix`
added. Beside it the same run printed a second error, "tuple pattern
used but type is `?T7`", at the inner `|(_, i)|`, naming an inference
variable rather than a type; it went with the first (the cascade kata 2896 describes). The
other arms checked clean.

LeetCode's Rust template took 10 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `0i64` lost its suffix twice; the `as i64` on each
value went, an `i32` widening; `|&x|` lost its `&`, and `Solution::`
took `.`.
