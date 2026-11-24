# 1326. Minimum Number of Taps to Open to Water a Garden

There is a one-dimensional garden on the x-axis. The garden starts at the
point `0` and ends at the point `n`, so its length is `n`. There are
`n + 1` taps at the points `[0, 1, ..., n]`. Given an integer `n` and an
integer array `ranges` of length `n + 1`, where `ranges[i]` means the
`i`-th tap, if opened, waters the area `[i - ranges[i], i + ranges[i]]`,
return the minimum number of taps that should be open to water the whole
garden. If the garden cannot be watered, return `-1`.

```
n = 5, ranges = [3,4,1,1,0,0]  ->  1
n = 3, ranges = [0,0,0,0]      ->  -1
```

**Constraints:** `1 <= n <= 10^4`, `ranges.length == n + 1`, `0 <=
ranges[i] <= 100`.

The arms are `fn min_taps(n: i32, ranges: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_taps.kara` ★ | each tap turned into how far right it waters from the leftmost point it reaches, the farthest kept for each point; then the garden crossed as a jump game, a tap opened each time the watered stretch runs out, reaching as far as any tap starting inside it. O(n) |
| `min_taps_dp.kara` | `least[x]`, the fewest taps that water everything from 0 to x; each tap, from left to right, extends any point it waters to its right end with one more tap. O(n r) for taps reaching r |
| `min_taps_sorted.kara` | every open tap as the stretch it waters, a `(left, right)` pair, sorted; then the classic cover of a line by intervals, each step taking, among the stretches that start inside what is already watered, the one that reaches farthest. O(n log n) |
| `min_taps_solution.kara` | a Rust solution as LeetCode's Rust users write it (the jump-game form on `usize`: `let mut max_reach = vec![0; n + 1]`, each left end clamped by `i.saturating_sub(r)`, and the crossing with `cur_end` and `next_end`), carried to Kāra by `karac fix` |
| `min_taps_table.kara` | a second Rust solution as LeetCode's Rust users write it (the table form: `let mut dp = vec![i32::MAX; n + 1]`, each tap relaxing `dp[right]` from every point it waters, `std::cmp::min` for the right end), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, three more
gardens whose answers are 3, 2 and 1, a garden of `10^4`, the
constraints' longest, with every tap shut and with every tap reaching 1
either way, and only the middle tap open, reaching 100 either way, which
waters a garden of 200 but not 201 (`1 -1 3 2 1 -1 5000 1 -1`); then 600
random gardens of 1 to `10^4`, most of them short, each tap shut or
reaching up to 3, 10 or 100 either way, open one time in 1, 3 or 20 (`600
random gardens: taps total 50064, checksum 313759977`). `min_taps.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`.

The Mend loop: the three Kāra arms checked clean as first written. The
first Rust arm takes one round of 11 fixes by `karac fix`'s count, from 5
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `vec![0; n + 1]` to `Vec.filled(n + 1, 0)`, every `usize` to
`i64`, `for (i, &r)` to `for (i, r)`, `::` to `.`, and
`i.saturating_sub(r)` to `i.saturating_sub(r).max(0)`, the floor Rust's
type gave, which an `i64` does not. The second takes one round of 16
fixes from 8 errors: the same rewrites, `i32::MAX` to `i32.MAX`,
`std::cmp::min` to `min`, and each `ranges[i] as usize` to `ranges[i]`,
an `i32` that widens to `i64` by itself. Both outputs match on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of taps tried, a set watering the garden when each
stretch from x to x + 1 lies inside what one of its taps waters, and the
fewest taps of any set that does, or -1. 2000 gardens of 1 to 8 in four
kinds, 500 each: every tap reaching 0 or 1; 0 to 2; 0 to 4; and three
taps in four shut, the rest reaching 1 to 3. Every garden and shut tap is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the garden turned round: the same answer |
| P3 | every tap reaching one further: no more taps, and -1 only where it was -1 before |
| P4 | one tap shut: no fewer taps, -1 counting as more than any |
| P5 | the garden stretched to twice its length, every tap twice as far apart and reaching twice as far, a shut tap between each two: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 gardens: checksum 268502656,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python, trying the sets of taps by size, gives the
same checksum.

## Mutation testing

Eleven edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the first Rust
arm's every left end clamped at 1 waters nothing from 0, so it answers -1
for every garden and fails exactly the checks of the table arm's start
costing a tap (M4). The ten kept, two to each arm, are each killed, fail
the same way under both backends and not by a crash, and no two fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a stretch that reaches no further than where it stands taken as watered | P1 702, P2 438, P3 257, P4 119, P6 2808 |
| M2 | ★: each left end keeping the last tap's reach, not the farthest | P1 8, P2 16, P3 4, P4 4, P6 32 |
| M3 | dp: a tap extending only the points from its own place | P1 1020, P2 637, P6 1020 |
| M4 | dp: the garden's start costing a tap | P1 1298, P6 1298 |
| M5 | sorted: taps reaching 1 left out | P1 438, P5 438, P6 438 |
| M6 | sorted: the stretches taken in the taps' order, not by left end | P1 50, P2 83, P3 30, P4 8, P6 50 |
| M7 | solution: each opened tap trusted to one point short of its reach | P1 1103, P5 303, P6 1103 |
| M8 | solution: a tap opened when the stretch is reached, not passed | P1 1298, P5 303, P6 1298 |
| M9 | table: the last point under a tap left out | P1 419, P2 85, P3 13, P5 419, P6 419 |
| M10 | table: the right end's count overwritten by every point, not the least | P1 676, P2 552, P3 347, P4 183, P6 676 |

P1 and P6 kill all ten, P2 six, P3 five, and P4 and P5 four each. A tap
more on every answer (M4) keeps every property, since a turned, wider,
narrower or stretched garden is charged the same extra tap; only the
literal reading sees it. Stretching the garden (P5) catches exactly the
edits that go wrong by one point, which a stretched garden turns into two
or a gap of one: taps reaching 1 left out (M5), a tap trusted to one
point short (M7) or opened a point early (M8), and the last point under a
tap left out (M9). Turning the garden round (P2) catches the edits that
treat the two ends of a stretch differently, and misses those whose
mistake looks the same from either end (M4, M5, M7, M8).

## Benchmarks

The bench builds 20 gardens of `10^4`, the constraints' longest, with
taps reaching up to 100, the constraints' most, once from its own
generator, a tap open one time in 1, 3, 10 or 30; then makes 300 passes,
each setting one tap of every garden from the checksum so far, so no
answer carries over, answering it with the ★ arm and folding the answer
plus the pass into the checksum. Each call takes a fresh table in every
language, a `calloc` in C. Every implementation prints `300 passes over 20
gardens of 10^4: checksum 217481798`.

BENCHTAB
