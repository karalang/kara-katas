# 1742. Maximum Number of Balls in a Box

You are working in a ball factory where you have `n` balls numbered from
`lowLimit` up to `highLimit` **inclusive** (i.e., `n == highLimit -
lowLimit + 1`), and an infinite number of boxes numbered from `1` to
`infinity`.

Your job at this factory is to put each ball in the box with a number
equal to the sum of digits of the ball's number. For example, the ball
number `321` will be put in the box number `3 + 2 + 1 = 6` and the ball
number `10` will be put in the box number `1 + 0 = 1`.

Given two integers `lowLimit` and `highLimit`, return *the number of
balls in the box with the most balls.*

```
lowLimit = 1, highLimit = 10   ->  2
lowLimit = 5, highLimit = 15   ->  2
lowLimit = 19, highLimit = 28  ->  2
```

**Constraints:** `1 <= lowLimit <= highLimit <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `balls.kara` ★ | no number up to `10^5` has a digit sum above 45, so a fixed array of 46 counts holds every box; each ball's digits are summed by repeated division, and the answer is the largest count. O(n log n) |
| `balls_map.kara` | each ball's digit sum from its decimal text, `f"{ball}".chars()` mapped through `to_digit` and summed; the boxes a `Map` filled by `entry`, and the largest of its values. O(n log n) |
| `balls_step.kara` | only the first ball's digits are summed in full: the next number adds 1 to the sum and takes 9 off for each trailing 9 of the number before, so every later sum follows from the last, and the largest count is kept as the boxes fill. O(n) amortized |
| `balls_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `[0; 46]` count array, a `for mut i in lowLimit..=highLimit` loop that divides `i` down, `cnt[s as usize] += 1`, and `*cnt.iter().max().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, then one
ball, the whole range from 1 to `10^5`, and 99999 to `10^5`, whose two
balls go to boxes 45 and 1; then the largest boxes summed and a checksum
for 3000 random ranges inside 1 to 100 and 1000 inside 1 to `10^5`.
`balls.py` mirrors the ★ arm and its output is byte-identical.

```
2
2
2
1
6000
1
3000 ranges inside 1 to 100: largest boxes sum to 12048, checksum 268619120
1000 ranges inside 1 to 100000: largest boxes sum to 2229532, checksum 366277184
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every box from 1 to 45, the balls in the range whose
digits, read from the number's text, add up to it, counted one box at a
time, and the most any box holds. It checks 1000 random ranges of 1 to
120 balls starting from 1 to 1000, each with a random split point. Every
case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | one ball more leaves the answer or adds one to it |
| P3 | the answer is at least 1, at most the balls, and 45 boxes of it hold them all |
| P4 | the answer is at least either part's and at most the two together |
| P5 | each arm agrees with at least two of the other three |

The differential prints `1000 problems: checksum 354027593, 20000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, each ball's digits summed from its text and counted, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: digits summed while more than one is left, the leading digit dropped | P1 168, P5 168 |
| M2 | ★: every other digit summed, the ball divided by 100 a step | P1 363, P5 363 |
| M3 | ★: the last ball left out | P1 92, P3 12, P4 14, P5 92 |
| M4 | map: the text's first digit skipped | P1 168, P5 168 |
| M5 | map: the smallest box, not the largest | P1 916, P2 6, P3 617, P4 12, P5 916 |
| M6 | step: each trailing 9 taking 8 off the sum, not 9 | P1 571, P5 571 |
| M7 | step: only the last trailing 9 taken off | P1 453, P5 453 |
| M8 | step: the latest box's count kept, not the largest so far | P1 538, P2 398, P3 43, P4 259, P5 538 |
| M9 | solution: each digit taken modulo 9, not 10 | P1 492, P5 492 |
| M10 | solution: the first ball left out | P1 89, P3 12, P4 20, P5 89 |

## Benchmarks

The bench draws 200 random ranges inside 1 to `10^5`, LeetCode's
limits, all of them first, then answers each 20 times by the ★ arm in
all five languages; each answer sums the digits of about 33000 balls on
average. Every implementation prints `200 ranges inside 1 to 100000, 20
rounds: largest boxes sum to 8079960, checksum 474257803`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.381 s |
| Rust (`rustc -O`) | 0.405 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.425 s |
| Go | 0.498 s |
| Kāra (`karac build`) | 0.549 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.550 s |
| Python | 24 s |

The sequential Kāra build takes 1.36x Rust's time and 1.29x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
That is a gap the checks do not explain; the loop is a division by 10
and an indexed increment per digit, and where the time goes is not yet
measured. C is the fastest here at 0.381 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.530 s and 0.531 s on one
run).

## Verification

All four arms print the same output as `balls.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★ and `Map` arms checked clean as first written. The step arm took
one `karac fix` of 2 edits: its `[0; 46]` counts and `best = 0`, plain
literals that meet the `i32` answer only through `max` and the return,
became `[0i32; 46]` and `best: i32`.

LeetCode's Rust template took one `karac fix` of 3 edits: `struct
Solution {}` added, and `for mut i in low_limit..=high_limit`, a pattern
Kāra does not take, became `for i in low_limit..=high_limit` with `let
mut i = i;` as the loop body's first line. `[0; 46]`, `s as usize` and
`*cnt.iter().max().unwrap()` carried over as written.

The differential checked clean as generated.
