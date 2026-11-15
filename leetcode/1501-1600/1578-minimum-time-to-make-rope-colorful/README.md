# 1578. Minimum Time to Make Rope Colorful

Alice has `n` balloons arranged on a rope. You are given a 0-indexed
string `colors` where `colors[i]` is the color of the `i`th balloon.

Alice wants the rope to be colorful. She does not want two consecutive
balloons to be of the same color, so she asks Bob for help. Bob can
remove some balloons from the rope to make it colorful. You are given a
0-indexed integer array `neededTime` where `neededTime[i]` is the time
(in seconds) that Bob needs to remove the `i`th balloon from the rope.

Return the minimum time Bob needs to make the rope colorful.

```
colors = "abaac", neededTime = [1,2,3,4,5]   ->  3
colors = "abc",   neededTime = [1,2,3]       ->  0
colors = "aabaa", neededTime = [1,2,3,4,1]   ->  2
```

**Constraints:** `n == colors.length == neededTime.length`;
`1 <= n <= 10^5`; `1 <= neededTime[i] <= 10^4`; `colors` contains only
lowercase English letters.

## Approaches

In every run of one colour, all balloons but the slowest to remove go,
so the answer is each run's total time less its largest.

| file | mechanism |
|---|---|
| `rope.kara` ★ | one pass over `colors.bytes()` keeping the largest time of the current run; each balloon adds the smaller of it and that largest, and the largest is reset where the colour changes. O(n) |
| `rope_runs.kara` | the colours collected into a `Vec[char]`, each run found by a second index, and its slice of the times summed less its `max()`. O(n) |
| `rope_fold.kara` | `colors.chars().zip(needed_time.iter()).fold(..)` over a `(colour, keep, paid)` tuple. O(n) |
| `rope_solution.kara` | LeetCode's Rust template (`min_cost(..) -> i32`, keeping the index `prev` of the run's slowest balloon), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, a single
balloon, `aaaa` and `bbbaaa`; then the sum of the answers and a checksum
for 3000 random ropes of up to 8 balloons, 300 of up to 1000 and 30 of
up to 100000, each drawn as runs whose colour changes with a chance of
one in one to three. `rope.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of balloons to remove tried, the cheapest that
leaves no two neighbours of one colour kept. It checks 3000 ropes of 1
to 9 balloons in 3 colours with times from 1 to 9, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the rope reversed leaves the answer |
| P3 | every time doubled doubles the answer |
| P4 | the colours renamed (`a` to `b`, `b` to `c`, `c` to `a`) leave the answer |
| P5 | a balloon of a new colour put at the end leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 872366335, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M4 stopped a run one balloon short, which left a run of one
balloon empty and was killed only by the `unwrap()` on its `max()`
panicking. It was replaced by one that keeps the run's first balloon in
place of its slowest.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run's largest updated before the balloon is paid for, so every balloon pays itself | P1 3000, P5 3000, P6 3000 |
| M2 | ★: the reset tested from the third balloon on, so the first two always share a run | P1 1761, P2 1879, P5 338, P6 1761 |
| M3 | ★: each balloon pays the larger of it and the run's largest | P1 3000, P2 1825, P5 3000, P6 3000 |
| M4 | runs: a run keeps its first balloon in place of its slowest | P1 1201, P2 1818, P6 1201 |
| M5 | runs: a run keeps its fastest balloon | P1 1911, P6 1911 |
| M6 | fold: the run's largest replaced by the newest time | P1 276, P6 276 |
| M7 | fold: an odd time paid where the colour changes | P1 2600, P2 1102, P3 2600, P5 3000, P6 2600 |
| M8 | template: the slower of two neighbours removed | P1 1911, P6 1911 |
| M9 | template: `prev` not moved to a slower balloon | P1 243, P2 460, P6 243 |
| M10 | template: the walk starts at the third balloon | P1 1944, P2 1715, P6 1944 |

## Benchmarks

The bench draws 200 ropes of 100000 balloons first, each colour one of
three and each time from 1 to 1000, then costs every rope by the ★ arm,
in all five languages. Every implementation prints `200 ropes of 100000
balloons: time total 2424692613, checksum 896800076`. The C mirror grows
each rope's colours and times by doubling, as Kāra's `String` and `Vec`
grow.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.200 s |
| C (`clang -O3`) | 0.207 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.231 s |
| Kāra (`karac build`) | 0.239 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.250 s |
| Go | 0.654 s |
| Python | 13.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.169 s and 0.277 s on one run).

Kāra is 0.92x Rust under overflow checks by median. Most of the time in
every compiled lane is drawing the ropes; the pass itself is a few
milliseconds. Go's `string(colors)` copies each rope once more.

## Verification

All four arms print the same output as `rope.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`76e5a13ad`.

## Writing it

The ★, runs and fold arms were written in Kāra and checked as written.

The Rust template took three rounds of `karac fix`:

1. three lines: the `Vec<i32>` types to `Vec[i32]`, the `|&x|` pattern
   to a plain name, and `Solution::` to `Solution.`;
2. `as_bytes()` to `bytes()`, `let mut ans = 0` given the type `i32`,
   `0usize` to `0`, and the wrapper's `as i64` dropped;
3. the wrapper's `colors.clone()` to `colors`.

It then checks and agrees with no hand edit.
