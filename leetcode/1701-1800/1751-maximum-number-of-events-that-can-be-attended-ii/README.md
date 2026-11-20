# 1751. Maximum Number of Events That Can Be Attended II

You are given an array of `events` where `events[i] = [startDay_i,
endDay_i, value_i]`. The `i`-th event starts at `startDay_i` and ends at
`endDay_i`, and if you attend this event, you will receive a value of
`value_i`. You are also given an integer `k` which represents the
maximum number of events you can attend.

You can only attend one event at a time. If you choose to attend an
event, you must attend the **entire** event. Note that the end day is
**inclusive**: that is, you cannot attend two events where one of them
starts and the other ends on the same day.

Return *the **maximum sum** of values that you can receive by attending
events.*

```
events = [[1,2,4],[3,4,3],[2,3,1]], k = 2            ->  7     4 + 3
events = [[1,2,4],[3,4,3],[2,3,10]], k = 2           ->  10    10 alone
events = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]], k = 3    ->  9     2 + 3 + 4
```

**Constraints:** `1 <= k <= events.length`; `1 <= k * events.length <=
10^6`; `1 <= startDay_i <= endDay_i <= 10^9`; `1 <= value_i <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `events.kara` ★ | sorted by last day, `current[i]` is the most the first i events give with at most j attended, one layer of j at a time: the i-th event is skipped, or attended after the best of the previous layer over the events ending before its first day, found once per event with `partition_point` on the ends. O(nk + n log n) |
| `events_memo.kara` | sorted by first day, the best from the i-th event on with j still to attend is the best of skipping it and attending it then going on from the first event that starts after it ends; each (i, j) is kept in a `Vec[Vec[Option[i32]]]` memo. O(nk + n log n) |
| `events_heap.kara` | a sweep in order of first day with a `PriorityQueue` of ends: every event that has ended before the current one starts is popped and its totals folded into a running best per layer, which the current event extends by its value. O(nk + n log n) |
| `events_solution.kara` | a Rust solution as LeetCode's Rust users write it, sorted by first day with `sort_unstable_by_key`, a `vec![vec![0; k + 1]; n + 1]` table filled from the last event back and `partition_point` for the next event, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then one
event, two that share a day, and k larger than the events; then the sum
of the answers and a checksum for 3000 random problems of up to 8 events
in 12 days, 300 of up to 1000 events over LeetCode's 10^9 days with k up
to 1000, and 5 of up to 100000 events with k up to 10, both at
LeetCode's `k * n` limit. `events.py` mirrors the ★ arm and its output
is byte-identical.

```
7
10
9
1000000
6
15
3000 problems of up to 8 events in 12 days: values add to 40314, checksum 608204370
300 problems of up to 1000 events in 1000000000 days: values add to 60126750651, checksum 690669860
5 problems of up to 100000 events in 1000000000 days: values add to 18997612, checksum 950905461
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of events, as a bit mask, with at most k of them
and no two sharing a day, summed in `i64`, and the largest sum. It
checks 3000 random problems of 1 to 8 events starting on days 1 to 10,
each 1 to 4 days long and worth 1 to 9, with k from 1 to 4. Every case
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the events listed in reverse give the same answer |
| P3 | one more event allowed never lowers the answer, nor raises it by more than the largest value |
| P4 | every value doubled doubles the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 94624047, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, every subset tried, gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an event that ends on the day another starts counted as before it | P1 1347, P5 1347 |
| M2 | ★: an event attended after the current layer, not the one before, so k is unbounded | P1 1124, P5 1124 |
| M3 | ★: the events sorted by first day, not last | P1 150, P2 172, P5 150 |
| M4 | memo: after attending, the next event tried, not the first that starts after it ends | P1 1198, P5 1198 |
| M5 | memo: the next event the first that starts on or after the day it ends | P1 1347, P5 1347 |
| M6 | memo: the memo read at one event left, whatever j is | P1 12, P5 12 |
| M7 | heap: an event that ends on the day the current one starts taken as finished | P1 806, P5 806 |
| M8 | heap: a finished event's totals replace the running best, not raise it | P1 674, P5 674 |
| M9 | solution: attending an event does not use up one of k | P1 1124, P5 1124 |
| M10 | solution: the table filled for j up to k - 1 only | P1 3000, P5 3000 |

## Benchmarks

The bench draws 10 random problems of 100000 events over 10^9 days,
each up to 10^8 days long and worth up to 10^6, all of them first, then
answers each 5 times with k = 10, LeetCode's `k * n` limit, by the ★ arm
in all five languages; each answer copies and sorts its events anew. C
sorts an array of structs with `qsort`, breaking ties on the first day
and the value, which leaves the answer as it is. Every implementation
prints `10 problems of 100000 events, k = 10, 5 rounds: values add to
499962420, checksum 445502573`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.102 s |
| Kāra (`karac build`) | 1.119 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.133 s |
| Rust (`rustc -O`) | 1.253 s |
| C (`clang -O3`) | 1.303 s |
| Go | 6.145 s |
| Python | 18 s |

The sequential Kāra build is 12% faster than Rust and level with Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (1.065 s and
1.102 s on one run).

## Verification

All four arms print the same output as `events.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm checked clean as first written. The memo arm took one `karac
fix`: a `k as i64` passed to an `i64` parameter, which widens by itself,
was dropped.

The heap arm was first written with Rust's `BinaryHeap[Reverse[(i32,
i64)]]` to pop the earliest end first. `karac check` named Kāra's
`PriorityQueue`, which pops the smallest first already, and one `karac
fix` of 5 edits wrote `PriorityQueue[(i32, i64)]` and
`PriorityQueue.new()` and took the three `Reverse` wrappers off the
type, the `peek` pattern and the `push`.

LeetCode's Rust template took one `karac fix` of 16 edits: `struct
Solution {}` added, the `mut events` parameter written `events: own
Vec[..]` with `let mut events = events;` at the body's start,
`Vec<Vec<i32>>` written `Vec[Vec[i32]]`, `sort_unstable_by_key` written
`sort_by_key`, `k as usize` written `k as i64`, `vec![vec![0; k + 1]; n +
1]` written `Vec.filled(n + 1, Vec.filled(k + 1, 0i32))`, and
`Solution::max_value` written `Solution.max_value`. `partition_point`,
`1..=k` and the `max` method carried over as written.

The differential and the bench checked clean as generated.
