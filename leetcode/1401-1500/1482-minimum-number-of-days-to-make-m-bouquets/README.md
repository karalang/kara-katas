# 1482. Minimum Number of Days to Make m Bouquets

You are given an integer array `bloomDay`, an integer `m` and an integer
`k`. You want to make `m` bouquets. To make a bouquet, you need to use
`k` adjacent flowers from the garden. The garden consists of `n`
flowers, the `i`th flower will bloom in the `bloomDay[i]` and then can
be used in exactly one bouquet. Return the minimum number of days you
need to wait to be able to make `m` bouquets from the garden. If it is
impossible to make `m` bouquets return `-1`.

```
bloomDay = [1,10,3,10,2],       m = 3, k = 1  ->  3
bloomDay = [1,10,3,10,2],       m = 3, k = 2  ->  -1
bloomDay = [7,7,7,7,12,7,7],    m = 2, k = 3  ->  12
```

**Constraints:** `1 <= n <= 10^5`, `1 <= bloomDay[i] <= 10^9`, `1 <= m
<= 10^6` and `1 <= k <= n`.

The arms are `fn min_days(bloom_day: Vec[i32], m: i32, k: i32) -> i32`.
`m * k` can reach `10^6 * 10^5`, past `i32`, so every arm first compares
it with `n` in `i64`, and answers `-1` when the garden is too small.

## Approaches

| file | mechanism |
|---|---|
| `min_days.kara` ★ | a binary search over the days: by a given day, a walk along the garden counts the bouquets the bloomed runs make, a bouquet each time a run reaches `k`; more days never make fewer, so the first day that makes `m` is found by halving the range from the earliest bloom to the latest. O(n log D) |
| `min_days_candidates.kara` | the answer is always some flower's bloom day, so the search runs over the distinct bloom days, sorted and deduplicated, with `partition_point` finding the first that makes `m`. O(n log n) |
| `min_days_union.kara` | the flowers taken in the order they bloom, each joined to a bloomed neighbour's run in a union-find (`struct Runs`) that keeps each run's length; the total of bouquets kept as runs merge, a run of length L making L / k, and the first day the total reaches `m` is the answer. O(n log n) |
| `min_days_windows.kara` | each window of `k` adjacent flowers is ready on its latest bloom day, found for every window by a sliding maximum over a `VecDeque`; then a binary search over the days, each day's bouquets counted by taking ready windows greedily from the left, each one starting past the last. O(n log D) |
| `min_days_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `can` closure over `&bloom_day`, `let (mut lo, mut hi) = ...`, `*bloom_day.iter().min().unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`3 -1
12`); six edges, one flower, every flower needed in one bouquet, a
garden one flower short, the latest day at the constraints' most, three
bouquets of two around one late flower, and one bouquet that must wait
for the late flower in its middle (`5 5 -1 1000000000 2 9`); the
constraints' most, 100000 days from 1 to 10^9, for `(m, k)` of (1, 1),
(100, 50), (900, 100), (50000, 2) and (100000, 1) (`100000 flowers: 3113
904318628 997904798 999999704 999999704`); and 3000 random gardens of 1
to 60 flowers from 1 to top, top from 1 to 10^9, `m` from 1 to 10 and
`k` from 1 to 6, each answer folded into a checksum (`3000 random
gardens: 958 with no way, checksum 831125871`). `min_days.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, candidates and union arms check clean as first
written. The windows arm was first written `window.front() ==
Some(i - k)`, an `Option` of a reference into the deque against an
`Option[i64]`, and `let mut lo = 1;`, an `i64` against the `i32` days;
`karac fix` wrote `window.front().cloned() == Some(i - k)` and `let mut
lo: i32 = 1;`. The Rust solution takes one round of 13 fixes by `karac
fix`'s count, and its diff is: `struct Solution;` to `struct Solution
{}`, `Vec<i32>` to `Vec[i32]`, `bloom_day.len() as i64` to
`bloom_day.len()`, since `len()` is already `i64`, the closure's `->
bool` dropped, since a Kāra closure declares no return type, `for &d in
&bloom_day` to `for d in ref bloom_day`, and `let (mut made, mut run)`
and `let (mut lo, mut hi)` to `let mut (made, run)` and `let mut (lo,
hi)`. The `*` on `*bloom_day.iter().min().unwrap()` stays.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each bloom day in order, a recursion that either starts a
bouquet at a flower, if its `k` flowers are all in bloom, or leaves the
flower unused, and the first day on which `m` bouquets can be made, or
`-1`. LeetCode's examples, the edges, and 1991 random gardens, half of 1
to 8 flowers from 1 to 5, so days repeat, `m` from 1 to 4 and `k` from 1
to 3, and half of 1 to 12 flowers from 1 to top, top from 1 to 10^9, `m`
and `k` from 1 to 4. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the garden reversed has the same answer |
| P3 | every flower 5 days later makes the answer 5 days later |
| P4 | one bouquet of one flower is ready on the first bloom day, and bouquets that need every flower on the last |
| P5 | one bouquet fewer is never later |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 964243983,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, choosing the
bouquets' starts by `itertools.combinations`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: one bouquet more than m asked for | P1 730, P4 1449, P6 2920 |
| M2 | ★: a late flower does not break a run, so bouquets need not be adjacent | P1 309, P6 1236 |
| M3 | candidates: a late flower does not break a run | P1 309, P6 309 |
| M4 | candidates: a bouquet made of k - 1 flowers | P1 878, P4 1001, P6 878 |
| M5 | union: every flower makes a bouquet as it blooms | P1 620, P4 540, P6 620 |
| M6 | union: a joined neighbour's bouquets not taken back off the total | P1 277, P2 10, P4 652, P6 277 |
| M7 | windows: a sliding minimum, so a window is ready on its earliest day | P1 614, P4 510, P6 614 |
| M8 | windows: ready windows taken overlapping | P1 212, P4 279, P6 212 |
| M9 | solution: one bouquet more than m asked for | P1 730, P4 1449, P6 730 |
| M10 | solution: a bouquet needs k + 1 flowers | P1 731, P4 1605, P6 731 |

## Benchmarks

The bench makes one garden of 100000 flowers blooming from day 1 to 10^9
once; then makes 150 passes, each punching one flower's day and asking
the ★ arm for `m` bouquets of `k` flowers, `k` from 1 to 10 and `m` up
to 100 past what the garden can make, all chosen from the checksum so
far. Each pass is about 30 walks of the garden. Every implementation
prints `150 passes over 100000 flowers: checksum 435356411`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 1.5 s against Rust's 1.2 s (1.6 s with overflow checks on),
C's 1.2 s and Go's 1.5 s; Python takes 26.9 s.
