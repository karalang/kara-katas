# 1703. Minimum Adjacent Swaps for K Consecutive Ones

You are given an integer array, `nums`, and an integer `k`. `nums`
comprises of only `0`'s and `1`'s. In one move, you can choose two
**adjacent** indices and swap their values.

Return *the **minimum** number of moves required so that* `nums` *has*
`k` ***consecutive*** `1`*'s*.

```
nums = [1,0,0,1,0,1], k = 2          ->  1
nums = [1,0,0,0,0,0,1,1], k = 3      ->  5
nums = [1,1,0,1], k = 2              ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `nums[i]` is `0` or `1`;
`1 <= k <= sum(nums)`.

## Approaches

| file | mechanism |
|---|---|
| `minmoves.kara` ★ | gathering k ones into a block costs what moving them there costs; with the ones at p[0] < p[1] < ..., q[j] = p[j] - j takes the block's own spread out, so a window's cost is the sum of \|q[j] - q[m]\| about its median m, and prefix sums of q give each window's cost at once. O(n) |
| `minmoves_positions.kara` | the median one stays at p[m]; the L ones before it go to p[m] - L .. p[m] - 1 and the R after it to p[m] + 1 .. p[m] + R, so each side costs its count times p[m] against its positions' sum, less 1 + 2 + .. + L. The positions by `enumerate().filter().map().collect()`, their prefix sums in a `Vec.filled`. O(n) |
| `minmoves_sliding.kara` | the first window's cost summed outright, then carried on: sliding one drops q[i], adds q[i + k], and moves the median on by d = q[m + 1] - q[m], which changes the rest by d * (2(m - i) - k), -d for an odd k and 0 for an even one. O(n) |
| `minmoves_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's prefix sums with `k as usize`, `vec![0i64; n + 1]`, `(i + j) / 2` for the median and `.min()` as a method, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, k = 1 (0),
and three 1s a gap apart (2); then the answers summed and a checksum for
3000 random arrays of up to 12 values, 300 of up to 1000 and 10 of up to
`10^5`, each value a 1 with a chance of its array's own, at least one 1,
and k from 1 to the count of 1s. `minmoves.py` mirrors the ★ arm and its
output is byte-identical.

```
1
5
0
0
2
3000 arrays of up to 12 values: answers sum to 1281, checksum 74059467
300 arrays of up to 1000 values: answers sum to 1139330, checksum 144334074
10 arrays of up to 100000 values: answers sum to 292371340, checksum 929125095
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every array reachable by swapping two neighbours, found a
swap at a time, breadth first, into a `SortedSet[Vec[i32]]`; the first
layer that holds an array with k 1s in a row is the answer. It checks
3000 random arrays of 1 to 9 values drawn as the arms' batches are.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | two 0s put in front and one at the end give the same answer |
| P4 | k one less never costs more, and k = 1 costs nothing |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 988467951, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same search over tuples, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The median is any middle value of an
even window, so the lower median for the upper (or `(i + j + 1) / 2` in
the solution arm) is no mutation; neither was tried. M2 and M4 both
leave the block's spread wrong by the same amount and fail the same
checks. M7, the sliding arm's median shift with its sign turned, is
the hardest to see: it only matters for an odd k whose median moves, and
fails 19 problems.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window gathered to its first one, not its median | P1 129, P2 189, P5 129 |
| M2 | ★: the positions taken as they are, the spread not taken out | P1 1141, P5 1141 |
| M3 | ★: the right side counted one too many | P1 1624, P2 1741, P3 3000, P4 1065, P5 1624 |
| M4 | positions: the left side's spread `L(L - 1) / 2` | P1 1141, P5 1141 |
| M5 | positions: one more one after the median | P1 3000, P2 1750, P3 3000, P4 1859, P5 3000 |
| M6 | positions: the window's first position as the median's | P1 697, P2 51, P4 694, P5 697 |
| M7 | sliding: the median's shift subtracted | P1 19, P2 42, P4 6, P5 19 |
| M8 | sliding: the dropped one measured from the next median | P1 338, P2 46, P4 224, P5 338 |
| M9 | solution: each window's end one short | P1 290, P2 176, P5 290 |
| M10 | solution: the median's distance from the start added | P1 680, P5 680 |

## Benchmarks

The bench draws 50 random arrays of `10^5` values, LeetCode's longest,
each value a 1 with a chance of its array's own (1 to 10 in 10), each
with a random k, all of them first, then answers each 40 times by the ★
arm in all five languages. Every implementation prints `50 arrays of
100000 values, 40 rounds: answers sum to 260140959400, checksum
535184941`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.052 s |
| Kāra (`karac build`) | 1.092 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.169 s |
| Rust (`rustc -O`) | 1.172 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.492 s |
| Go | 2.112 s |
| Python | 29 s |

The sequential Kāra build is level with Rust and 22% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 1.052 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.058 s and 1.062 s on one
run).

## Verification

All four arms print the same output as `minmoves.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, positions and sliding arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 15 edits:
`struct Solution {}` added, `Vec<i32>` and `Vec<i64>` written in
brackets, `Vec::new` and `i64::MAX` written with `.`, `for (i, &x)`
written `for (i, x)`, `vec![0i64; n + 1]` written `Vec.filled(n + 1,
0)`, and `k as usize` written `k as i64`, after which the four `as i64`
casts on the `usize` differences had nothing to do and were dropped.
`(i + j) / 2` and `ans.min(left + right)` carried over as written.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
