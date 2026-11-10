# 2054. Two Best Non-Overlapping Events

You are given an array of `events` where `events[i] = [startTime, endTime,
value]`. The `i`th event starts at `startTime`, ends at `endTime`, and
attending it earns `value`. Choose at most two events that do not overlap
so that the sum of their values is as large as possible, and return that
sum. Start and end times are inclusive: two events cannot both be
attended when one starts at the time the other ends, so the second must
start at least one after the first ends.

```
events = [[1,3,2],[4,5,2],[2,4,3]]  ->  4
events = [[1,3,2],[4,5,2],[1,5,5]]  ->  5
events = [[1,5,3],[1,5,1],[6,6,5]]  ->  8
```

**Constraints:** `2 <= events.length <= 10^5`; `events[i].length == 3`;
`1 <= startTime <= endTime <= 10^9`; `1 <= value <= 10^6`.

The best pair is some event and the best of those that start after it
ends, or the event alone. Every approach finds, for each event, the best
value on one side of it in time: after it, from the events sorted by
start, or before it, from the events sorted by end.

## Approaches

| file | mechanism |
|---|---|
| `two.kara` ★ | the events sorted by start, the best value from each one on kept from the end, and each event paired with the best of those starting after it ends, the first of them found with `partition_point` |
| `two_brute.kara` | the statement read directly: each event alone, and each pair where one ends before the other starts. O(n²) |
| `two_sweep.kara` | the events in two orders, by start and by end (`sort_by_key`); walking the starts, a cursor over the ends takes in every event that ends before the current start, keeping the best value it has passed |
| `two_heap.kara` | the events by start, each pushed as it is passed into a `PriorityQueue` of (end, value), soonest end first; before each event, every one that ended before its start is popped and its value kept if it is the best so far |
| `two_floor.kara` | a `SortedMap` from each end time to the best value of any event ending then or earlier, built from the events by end; each event asks its `floor` for the last end before its start |
| `two_solution.kara` | LeetCode's Rust template (`use std::collections::BinaryHeap` and `std::cmp::Reverse`, `sort_unstable_by_key`, a min-heap of `Reverse((end, value))` drained with `while let Some(&Reverse((end, val))) = heap.peek()`), carried by `karac fix` in five rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four more,
each set of events and its answer; then the sum and a checksum of the
answers for 2000 random sets of 2 to 30 events starting from 1 to 54 and
lasting up to 10, worth up to 100, so that events touch, overlap and tie;
then the same for 20 sets of 2000 events over the constraints' times and
values, lasting up to a thousand, a million, a hundred million or half a
billion. The brute-force arm makes the larger sets 2000 events, not the
constraints' 100000, which would be five billion pairs; the bench takes
the ★ arm to the limit. `two.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every choice of one event, or of two that share no moment of
time, two events sharing one when the later start is no later than the
earlier end. It checks 500 random sets of 2 to 30 events, drawn as the
harness draws its small ones, before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least the best value and at most the two best values together |
| P3 | the events mirrored in time, each (start, end) to (100 - end, 100 - start), and listed backwards, have the same answer |
| P4 | a new event worth 1 that spans every other leaves the answer the same |
| P5 | a new event after every other, worth 10000000, makes the answer 10000000 and the best value |
| P6 | each arm agrees with at least three of the other five |

The differential prints `500 sets: checksum 794699427, 18000 checks over 6
arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-five edits to the differential, five to seven to each of its arms,
each run under `karac __mir-run` and `karac __mir-llvm-run`. Every one is
killed, fails the same way under both backends and not by a crash.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm, no two of them failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: touching events paired (`<` for `<=`) | P1 182, P2 137, P6 182 |
| M2 | ★: the events never sorted | P1 292, P2 101, P3 365, P4 154, P6 292 |
| M3 | ★: the best from each on summed | P1 470, P2 469, P3 399, P5 497, P6 470 |
| M4 | brute: touching events paired | P1 48, P6 48 |
| M5 | brute: a pair only when the first comes first | P1 252, P6 252 |
| M6 | brute: no pair of neighbours | P1 113, P5 44, P6 113 |
| M7 | sweep: the last event passed, not the best | P1 377, P3 252, P5 449, P6 377 |
| M8 | sweep: the ends sorted by start | P1 45, P3 57, P4 346, P6 45 |
| M9 | sweep: the starts never sorted | P1 294, P2 266, P3 277, P6 294 |
| M10 | heap: the latest end first (`max_first`) | P1 158, P4 391, P6 158 |
| M11 | heap: each event pushed as (value, end) | P1 496, P2 3, P3 498, P4 474, P5 500, P6 496 |
| M12 | heap: the events never sorted | P1 211, P3 179, P6 211 |
| M13 | floor: the ends sorted by start | P1 41, P3 63, P5 9, P6 41 |
| M14 | floor: the floor two before the start | P1 55, P5 58, P6 55 |
| M15 | floor: an end keeps its first best | P1 29, P3 41, P5 7, P6 29 |
| M16 | solution: each event pushed by its start | P1 91, P3 27, P6 91 |
| M17 | solution: the events sorted by end | P1 32, P3 46, P6 32 |

P1 and P6 kill all seventeen, P3 eleven, P5 seven, P2 five and P4 four.
P2 bounds the answer by the values alone, so it catches an arm that pairs
events that touch (M1) or that sums more than two values (M3), and one
whose order is lost (M2, M9). P3 mirrors time, which swaps which side of
an event an arm looks at: an arm that reads its order wrongly (M7, M8,
M11, M12, M13, M15 to M17) answers the mirror differently. P4's event
spans all the others, so it pairs with none of them, but it is the first
to start and the last to end: an arm that takes the latest end first
(M10), or orders its ends by start (M8), meets it where it should not.
P5's event comes after every other and is worth more than any two of
them, so the answer is it and the best value: an arm that loses the best
value before an event (M3, M6, M7, M11, M13 to M15) fails it. Two kept
edits fail P1 and P6 alone, both brute force: touching events paired (M4)
and a pair only when the first listed comes first in time (M5).

Of the thirty-five, eighteen were not kept. Six fail in ways of their own
and were left out only because each arm keeps three (the Rust arm two):
in the ★ arm, the best from each on only that event and the next event
found by its end; in brute force, pairs that overlap taken; in the Rust
arm, an event ending at a start popped, the event's own value left out,
and the adapter swapping start and end. The other twelve fail as a kept
one or another discarded one does. Touching events paired fails the same in the
★, sweep and floor arms (M1), and in the heap arm as in brute force (M4).
The larger of the two taken rather than the sum (★), the best before and
the value apart (sweep), and a popped value dropped (heap) fail alike, as
do the last popped value kept rather than the best in the heap and Rust
arms, and the last passed value in the sweep and floor arms (M7). Each
event alone left out (brute) and a billion charged when no event comes
before (floor) fail the same three questions, where the best answer is
one event alone. The adapter ending each event one later fails as the
floor two before the start (M14): both move an end by one.

## Verification

Every arm prints the same output as `two.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.6 s (sweep) to 1.7 s (Rust), the
brute-force arm 21 s, and the differential 2.4 s.

The floor arm was written with `Some((_, b)) => *b` over the `floor`'s
`Option[(ref K, ref V)]`, as Rust would; `karac check` refuses the `*`,
since a borrowed `i64` reads as a copy, and `karac fix` drops it.

The Rust arm was written as LeetCode's Rust template, and met a compiler
gap: the template's `while let Some(&Reverse((end, val))) = heap.peek()`
comes before the first `heap.push(..)`, so the heap's element type was
still open at the pattern. The tuple pattern bound its leaves to no type,
`karac check` passed, and the MIR builder refused the program with "a type
that failed to check is not lowered yet". kara `6c629e8cb6` makes a tuple
pattern over an open type a tuple of open parts, which the later push
solves, as Rust's inference does, and lets `best.max(val)` with `best:
i32` take the open `val` to be `i32` (tests in
`tests/kata_2054_tuple_pattern_later_type.rs`).

With it, `karac fix` carries the template in five rounds of 11, 1, 3, 4
and 1 edits to a clean check: the two `use` lines dropped, `struct
Solution;` to `struct Solution {}`, `mut events: Vec<Vec<i32>>` to `events:
own Vec[Vec[i32]]` and a `let mut events = events;`, `BinaryHeap::new()`
to `PriorityQueue.new()`, `for e in &events` to `for e in ref events`, the
`&` pattern to `.cloned()` on the value matched, each `Reverse` dropped,
`sort_unstable_by_key` to `sort_by_key`, and `best` and `ans` declared
`i32`, since a method does not fix a literal's type. The adapter hands
the harness's events to it as `Vec[Vec[i32]]` and widens the answer back.

## Benchmarks

The bench answers 50 sets of 100000 events, the constraints' limit, over
times up to a billion and values up to a million, with the ★ arm in all
five languages: five million events sorted and searched. Building the
sets is part of the work timed. Every implementation sorts by (start,
end, value): Rust's and Kāra's `sort`, Go's `slices.SortStableFunc` and
C's `qsort` with a comparator. Every implementation prints `50 sets: sum
99998170, checksum 735902695`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `0142335972` and the fixes from
katas 2054 to 2057, on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.534 to 0.623 s | 0.560 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.549 to 0.608 s | 0.572 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.730 to 0.784 s | 0.749 s |
| Kāra (`karac build`) | 0.723 to 0.789 s | 0.751 s |
| C (`clang -O3`) | 1.585 to 1.730 s | 1.640 s |
| Go | 2.305 to 2.558 s | 2.404 s |
| Python | 12.6 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.736 s) is not above its real time (0.751 s).

The sequential Kāra program is 1.31x Rust under overflow checks and 0.46x
C. C's `qsort` and Go's `slices.SortStableFunc` call their comparator
through a pointer or a closure for every comparison; Rust's and Kāra's
`sort` compile the comparison into the sort. Where the rest of Kāra's 31%
over Rust goes has not been measured.
