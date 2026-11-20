# 1705. Maximum Number of Eaten Apples

There is a special kind of apple tree that grows apples every day for
`n` days. On the `ith` day, the tree grows `apples[i]` apples that will
rot after `days[i]` days, that is on day `i + days[i]` the apples will be
rotten and cannot be eaten. On some days, the apple tree does not grow
any apples, which are denoted by `apples[i] == 0` and `days[i] == 0`.

You decided to eat **at most** one apple a day (to keep the doctors
away). Note that you can keep eating after the first `n` days.

Given two integer arrays `days` and `apples` of length `n`, return *the
maximum number of apples you can eat.*

```
apples = [1,2,3,5,2], days = [3,2,1,4,2]          ->  7
apples = [3,0,0,0,0,2], days = [3,0,0,0,0,2]      ->  5
```

**Constraints:** `n == apples.length == days.length`;
`1 <= n <= 2 * 10^4`; `0 <= apples[i], days[i] <= 2 * 10^4`;
`days[i] = 0` if and only if `apples[i] = 0`.

## Approaches

| file | mechanism |
|---|---|
| `apples.kara` ★ | a min-first `PriorityQueue` of (rotting day, apples left), one entry per day's crop: each day the rotten crops are dropped and one apple eaten from the crop that rots soonest; the days go on past the last crop while any apple is left. O((n + d) log n) |
| `apples_sorted.kara` | a `SortedMap` from rotting day to the apples that rot then, crops of the same day merged by `entry(..).or_insert(0)`: each day its first key is dropped while not after today, then one apple taken from it. O((n + d) log n) |
| `apples_buckets.kara` | a count for every rotting day and a pointer to the soonest: the pointer moves on past days already rotten or empty, back to a new crop's day when that is sooner, and one apple is taken there. O(n + d) but for the moves back |
| `apples_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `BinaryHeap` of `Reverse((rot, count))` popped through `while let Some(&Reverse((r, _))) = heap.peek()`, with `usize` days, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one apple
(1), nothing grown (0), and a crop that outlasts the days it grows on
(6); then the answers summed and a checksum for 3000 random trees of up
to 8 days with up to 5 apples a day lasting up to 5 days, 300 of up to
1000 days with up to 100, and 10 of up to `2 * 10^4`, LeetCode's
largest. `apples.py` mirrors the ★ arm with `heapq` and its output is
byte-identical.

```
7
5
1
0
6
3000 trees of up to 8 days: answers sum to 17504, checksum 904925630
300 trees of up to 1000 days: answers sum to 173937, checksum 707058528
10 trees of up to 20000 days: answers sum to 278684, checksum 249412837
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: on each day, any apple grown by then and not yet rotten may
be eaten, one at most, or none; every way of choosing is searched, day
by day until the last crop has rotted, memoized on the day and the
apples left of each crop in a `Map[Vec[i64], i64]`, and the most eaten
wins. It does not assume the soonest-rotting apple is the one to eat.
It checks 3000 random trees of 1 to 6 days, each day 0 to 3 apples
lasting 1 to 4 days. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a day with no apples put in front gives the same answer |
| P3 | every crop lasting a day longer never gives fewer |
| P4 | the answer is no more than the apples grown, nor than the day the last crop rots |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 931785277, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same search under `lru_cache`, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1 and M9 both let an apple be eaten
on the day it rots and fail the same checks; they are the only ones P4
sees, since only they can eat more than the statement allows. M4, a
second crop with the same rotting day overwriting the first, is the
hardest to see: it fails only where two crops rot on one day and the
first is not yet eaten, 137 problems.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a crop kept on the day it rots | P1 1771, P4 969, P5 1771 |
| M2 | ★: no eating once the tree stops growing | P1 1720, P5 1720 |
| M3 | ★: every crop rotting a day early | P1 2309, P5 2309 |
| M4 | sorted: a crop overwriting another that rots the same day | P1 137, P5 137 |
| M5 | sorted: a day's last two apples taken as one | P1 1504, P5 1504 |
| M6 | sorted: the latest-rotting crop checked for rot, not the soonest | P1 370, P5 370 |
| M7 | buckets: the pointer may rest on today, which has rotted | P1 553, P5 553 |
| M8 | buckets: the pointer never moved back to a sooner crop | P1 2824, P5 2824 |
| M9 | solution: a crop kept on the day it rots | P1 1771, P4 969, P5 1771 |
| M10 | solution: a crop's last two apples taken as one | P1 1506, P5 1506 |

## Benchmarks

The bench draws 50 random trees of `2 * 10^4` days, LeetCode's largest,
one day in four growing nothing and the rest up to `2 * 10^4` apples
lasting up to `2 * 10^4` days, all of them first, then answers each 10
times by the ★ arm in all five languages: Rust's `BinaryHeap` of
`Reverse` pairs, Go's `container/heap`, Python's `heapq`, and a binary
heap written out in C, all ordered by (rotting day, apples left) as
Kāra's tuples are. Every implementation prints `50 trees of 20000 days,
10 rounds: answers sum to 19880250, checksum 447245050`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 1.465 s |
| Rust (`rustc -O`) | 1.524 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.729 s |
| Kāra (`karac build`) | 1.743 s |
| C (`clang -O3`) | 2.848 s |
| Go | 5.164 s |
| Python | 17 s |

The sequential Kāra build takes 1.13x Rust's time and 1.18x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.667 s and 1.688 s on one
run).

## Verification

All four arms print the same output as `apples.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and buckets arms checked clean as first written. The sorted arm's
first draft asked its `SortedMap` for `first_key_value()`, Rust's
`BTreeMap` name; `karac check` named Kāra's `first()` and `karac fix`
wrote it at both calls.

LeetCode's Rust template took one `karac fix` of 21 edits:
`struct Solution {}` added; the two `use` lines deleted, since
`PriorityQueue` is in the prelude and pops the smallest first, so
`BinaryHeap::new()` became `PriorityQueue.new()` and every `Reverse(..)`
was unwrapped, in the pushes and in both patterns; `Vec<i32>` written
`Vec[i32]`; `0usize` and `days[i] as usize` written plain; `||`, `!` and
`&&` written `or`, `not` and `and`; and `while let Some(&Reverse((r,
_))) = heap.peek()` written `while let Some((r, _)) =
heap.peek().cloned()`.

The differential's search first took its state as a bare parameter and
handed it to the memo's `insert`; `karac check` refused that (E0200, a
borrowed parameter given away) and `karac fix` took it `own Vec[i64]`.
`arm_name` indexes a list of string literals for a `Str`, as #1662's
does (B-2026-11-19-131).
