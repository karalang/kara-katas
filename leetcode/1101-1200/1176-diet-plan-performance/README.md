# 1176. Diet Plan Performance

A dieter consumes `calories[i]` calories on the `i`-th day.

Given an integer `k`, for every consecutive sequence of `k` days
(`calories[i], calories[i+1], ..., calories[i+k-1]` for all
`0 <= i <= n-k`), they look at `T`, the total calories consumed during
that sequence of `k` days:

- If `T < lower`, they performed poorly on their diet and lose 1 point;
- If `T > upper`, they performed well on their diet and gain 1 point;
- Otherwise, they performed normally and there is no change in points.

Initially, the dieter has zero points. Return the total number of points
the dieter has after dieting for `calories.length` days.

Note that the total points can be negative.

```
calories = [1,2,3,4,5], k = 1, lower = 3, upper = 3  ->  0
calories = [3,2],       k = 2, lower = 0, upper = 1  ->  1
calories = [6,5,0,0],   k = 2, lower = 1, upper = 5  ->  0
```

**Constraints:** `1 <= k <= calories.length <= 10^5`,
`0 <= calories[i] <= 20000`, `0 <= lower <= upper`.

The arms are `fn diet_plan_performance(calories: Vec[i64], k: i64, lower:
i64, upper: i64) -> i64`. The two Rust arms keep the `i32` method LeetCode
gives Rust users, inside `impl Solution`, and a one-line
`diet_plan_performance` calls it.

## Approaches

| file | mechanism |
|---|---|
| `diet_plan.kara` ★ | one window slid across the plan over `calories.iter().enumerate()`: the day coming in added, the day `k` back taken away, each window scored as it is reached. O(n) |
| `diet_plan_prefix.kara` | prefix sums, each window's total one subtraction, `sums[i + k] - sums[i]`. O(n) time and space |
| `diet_plan_windows.kara` | the statement as written: `calories.windows(k)`, each window summed afresh and scored by a `score` function, the scores summed. O(n * k) |
| `diet_plan_queue.kara` | the window's days held in a `VecDeque`, the oldest popped and taken away once more than `k` are held, the window scored whenever it holds exactly `k`. O(n) time, O(k) space |
| `diet_plan_solution.kara` | a Rust solution as LeetCode's Rust users write it (the first window summed from the slice `calories[..k]`, a scoring closure `\|s: i32\| if s < lower { -1 } else if s > upper { 1 } else { 0 }`, the window slid over `k..calories.len()` with `usize` indices), carried to Kāra by `karac fix` |
| `diet_plan_chain.kara` | another Rust solution, one iterator chain: `calories.windows(k as usize)`, each window `sum::<i32>()`, each total mapped to -1, 0 or 1 and the points summed, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five properties |

Every arm prints the same 10 lines: LeetCode's three examples; one window
over every day, below and above; sums exactly at each bound, which score
nothing; days of 0 against bounds of 0 and of 1; 300 random plans of 1 to
40 days (`300 random plans: 1160 points, checksum 470125271`); and one
plan of 100000 days, the constraints' most, each day up to 20000, at k =
1, 317 and 100000 with the bounds 40 * k either side of the mean window.
`diet_plan.py` mirrors the ★ arm and its output is byte-identical; with
`lit` it sums every window afresh, as the statement reads, and its output
is the same. Every arm gives the same output under `karac run` and `karac
build`.

The Mend loop: the four Kāra arms take no fixes. The Rust arms take one
round each, 9 fixes and 12. The closure arm's: `struct Solution;` to
`struct Solution {}`; `Vec<i32>` and `Vec<i64>` to `Vec[i32]` and
`Vec[i64]`; `k as usize` to `k as i64`; `Solution::` to `Solution.`;
`|&c|` to `|c|`; and the harness's `as i64` dropped, since `i32` widens to
`i64` by itself. The chain arm's: the same, with `windows(k as usize)` to
`windows(k).into_iter()` and `sum::<i32>()` to `sum()`. Both arms' outputs
match on the first run.

One compiler gap came up on the way, fixed in kara `a3ae3b2036`:

- The closure arm was refused with no fix (kara B-2026-11-16-211). A closure whose
  body is a join of literals, `|s: i32| if s < lower { -1 } else if s >
  upper { 1 } else { 0 }`, was typed `i64` where the closure was written,
  since an unsuffixed literal defaults to `i64`, so `points`, which
  starts as `score(sum)`, was an `i64`, and returning it as the method's
  `i32` was refused as a narrowing. Rust types the literals from the closure's
  use, as Kāra already does for a `let` whose value is such a join. Now
  the closure's body is left open in the same way: a use that needs `i32`
  fixes it, and the literals are range-checked against `i32`; a closure
  no use fixes still returns `i64`. A body whose blocks hold a statement stays
  closed, since a statement may `return` a value of a fixed type.

The differential takes no fixes.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every `i` from 0 to `n - k`, days `i` to `i + k - 1` summed
afresh, a point lost below `lower` and one gained above `upper`. 400
random plans of 1 to 30 days, days up to 9 and the bounds near the
windows' sums, so that every outcome comes up; the first five plans have
one day and the first ten have `k = n`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the points lost (upper bound 10^9, which nothing passes) and the points gained (lower bound -1, which nothing falls below, no day being negative) counted apart add up to the answer |
| P3 | every day `c` calories more, and both bounds `k * c` more, scores every window the same |
| P4 | bounds no window can meet score every window: 10^9 and 10^9 give `-(n - k + 1)`, -1 and -1 give `n - k + 1` |
| P5 | the ★ arm's answer |

All 14,400 checks pass on every arm: `400 plans: checksum 388131169,
14400 checks over 6 arms: 0 failures`, in 0.8 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: the day leaving taken away one day late | P1 159, P3 172, P5 795 |
| A2 | ★: the first window not scored | P1 249, P4 800, P5 1245 |
| A3 | ★: a sum at the lower bound loses a point | P1 68, P5 340 |
| P1 | prefix: the last window not scored | P1 260, P4 800, P5 260 |
| P2 | prefix: each window one day short | P1 233, P3 262, P5 233 |
| P3 | prefix: a sum at the upper bound gains a point | P1 79, P5 79 |
| W1 | windows: a point lost counted as gained | P1 139, P4 400, P5 139 |
| W2 | windows: each window one day long | P1 310, P3 172, P4 800, P5 310 |
| W3 | windows: a sum one above the upper bound gains nothing | P1 85, P4 32, P5 85 |
| Q1 | queue: the oldest day kept one day too long | P1 277, P4 674, P5 277 |
| Q2 | queue: the day leaving not taken away | P1 207, P3 106, P5 207 |
| Q3 | queue: two points for each window above | P1 254, P4 400, P5 254 |
| X1 | closure: the first window one day short | P1 220, P2 49, P3 277, P4 53, P5 220 |
| X2 | closure: the second window skipped | P1 262, P2 10, P4 674, P5 262 |
| X3 | closure: a sum at the lower bound loses a point | P1 68, P5 68 |
| R1 | chain: a sum at the upper bound gains a point | P1 79, P5 79 |
| R2 | chain: each window's first day dropped | P1 233, P3 262, P5 233 |
| R3 | chain: a window within bounds gains a point | P1 241, P2 400, P5 241 |

A mutation of the ★ arm fails P5 on every arm, since P5 compares each arm
with the ★ arm; P1, P3 and P4 name the ★ arm itself. Three more edits look
like faults and pass all 14,400 checks under both backends, since they are
equivalent: the queue arm scoring when it holds `k` or more days (it never
holds more once it pops), the queue arm popping when it holds exactly `k +
1` (it never holds more), and the ★ arm testing the upper bound before
the lower (`lower <= upper`, so no sum is both).

## Benchmarks

`bench/` times the ★ arm against the same sliding window in C, Rust, Go
and Python: one plan of 100000 days, the constraints' most, each day up to
20000, built once, then 2000 calls at a `k` drawn from 1 to 100000 and
bounds a random spread either side of the mean window's sum, every answer
folded into a checksum. Every program prints `2000 calls: checksum
285365297`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `a3ae3b2036`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.190 to 0.233 s | 0.196 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.194 to 0.257 s | 0.202 s |
| Rust (`rustc -O`) | 0.125 to 0.170 s | 0.131 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.194 to 0.238 s | 0.200 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.195 to 0.241 s | 0.199 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.101 to 0.141 s | 0.103 s |
| C (`clang -O3`) | 0.102 to 0.127 s | 0.105 s |
| Go | 0.125 to 0.147 s | 0.127 s |
| Python | 18.4 to 18.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time equals wall time for both Kāra rows, so
both ran on one core. Kāra takes about the time of overflow-checked Rust,
the equal-safety comparison (1.01x), 1.9x C's and 1.6x Go's; Python takes
about 92x. The loop is two million days a call, each an add, a subtract
and two compares, so checked arithmetic is most of the gap: Rust without
overflow checks takes 0.131 s, 0.65x its checked build. That the checks
explain the rest of the gap to C was not profiled.
