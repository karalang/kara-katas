# 1674. Minimum Moves to Make Array Complementary

You are given an integer array `nums` of **even** length `n` and an
integer `limit`. In one move, you can replace any integer from `nums`
with another integer between `1` and `limit`, inclusive.

The array `nums` is **complementary** if for all indices `i`
(**0-indexed**), `nums[i] + nums[n - 1 - i]` equals the same number. For
example, the array `[1,2,3,4]` is complementary because for all indices
`i`, `nums[i] + nums[n - 1 - i] = 5`.

Return the ***minimum** number of moves required to make* `nums`
***complementary***.

```
nums = [1,2,4,3], limit = 4   ->  1
nums = [1,2,2,1], limit = 2   ->  2
nums = [1,2,1,2], limit = 2   ->  0
```

**Constraints:** `n == nums.length`; `2 <= n <= 10^5`;
`1 <= nums[i] <= limit <= 10^5`; `n` is even.

## Approaches

| file | mechanism |
|---|---|
| `complementary.kara` ★ | each pair (a, b), a <= b, costs 2 moves at any target sum, 1 at the sums from a + 1 to b + limit, and 0 at a + b; those steps go into a difference array over the sums 2 to 2 * limit, and one pass of running totals gives every sum's cost. O(n + limit) |
| `complementary_every.kara` | every target sum from 2 to 2 * limit tried, each pair costing 0, 1 or 2 by the same ranges. O(n * limit) |
| `complementary_sweep.kara` | the same steps in a `SortedMap` from sum to change, only at the sums where some pair's cost changes, walked in sum order from 2 per pair. O(n log n), whatever the limit |
| `complementary_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's difference array as `vec![0i32; 2 * limit + 2]` indexed through `usize` casts, `a.min(b)` and `ans.min(cur)`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, a pair of
ones beside (1, 4) with limit 4 (1), and a single pair (0); then the
moves summed and a checksum for 3000 random arrays of up to 6 pairs with
limits up to 6, 300 of up to 100 pairs with limits up to 100, and 10 of
up to 1000 pairs with limits up to 1000 (the every arm is O(n * limit),
so the batches stay where it runs in a second). `complementary.py`
mirrors the ★ arm and its output is byte-identical.

```
1
2
0
1
0
3000 arrays of up to 6 pairs, limits up to 6: 4570 moves, checksum 649630649
300 arrays of up to 100 pairs, limits up to 100: 14008 moves, checksum 73113911
10 arrays of up to 1000 pairs, limits up to 1000: 4246 moves, checksum 92089498
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every target sum from 2 to 2 * limit, and for each pair
nothing if it already sums to it, one move if some value from 1 to
`limit` put in place of either of its values reaches it, else two; the
cheapest sum wins. It checks 3000 random arrays of 1 to 6 pairs with a
limit of 1 to 6, each with a random order of its pairs. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | the pairs in another order give the same answer |
| P4 | a limit one higher never needs more moves |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 483284411, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Every one is caught by P1 and P5
alone: each wrong cost is still a function of the pairs as a set, so
it is the same when the array is reversed or its pairs reordered.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the one-move range starts at a, not a + 1 | P1 2445, P5 2445 |
| M2 | ★: the pair's own sum never ends | P1 1944, P5 1944 |
| M3 | ★: the one-move range ends one short | P1 967, P5 967 |
| M4 | every: one move reaches only from max + 1 to min + limit | P1 494, P5 494 |
| M5 | every: a pair already at the target costs 1 | P1 2917, P5 2917 |
| M6 | every: the target 2 * limit never tried | P1 549, P5 549 |
| M7 | sweep: the cost starts at 1 per pair, not 2 | P1 3000, P5 3000 |
| M8 | sweep: the pair's own sum never starts | P1 3000, P5 3000 |
| M9 | solution: the base cost 1 per pair | P1 3000, P5 3000 |
| M10 | solution: the target 2 never tried | P1 2992, P5 2992 |

## Benchmarks

The bench draws 100 arrays of `10^5` values with limits up to `10^5`,
LeetCode's largest, all of them first, then answers each 20 times by the
★ arm in all five languages. Every implementation prints `100 arrays of
100000 values, 20 rounds: 99983180 moves, checksum 633165535`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.478 s |
| Kāra (`karac build`) | 0.491 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.497 s |
| Rust (`rustc -O`) | 0.628 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.674 s |
| Go | 1.099 s |
| Python | 39 s |

The sequential Kāra build is 21% faster than Rust and 26% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.478 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.508 s and 0.530 s on one
run).

## Verification

All four arms print the same output as `complementary.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, every and sweep arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 8 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, each
`as usize` written `as i64`, `vec![0i32; 2 * limit + 2]` written
`Vec.filled(2 * limit + 2, 0i32)`, and the running cost `let mut cur = 0`
declared `: i32` (an `i32` added to a literal does not fix the
literal's type, and it kept the default `i64`).

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
