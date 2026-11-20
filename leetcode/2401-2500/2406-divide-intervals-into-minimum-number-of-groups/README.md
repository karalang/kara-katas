# 2406. Divide Intervals Into Minimum Number of Groups

You are given a 2D integer array `intervals` where `intervals[i] =
[left_i, right_i]` represents the **inclusive** interval `[left_i,
right_i]`.

You have to divide the intervals into one or more **groups** such that
each interval is in **exactly** one group, and no two intervals that are
in the same group **intersect** each other.

Return *the **minimum** number of groups you need to make*.

Two intervals **intersect** if there is at least one common number
between them. For example, the intervals `[1, 5]` and `[5, 8]`
intersect.

```
intervals = [[5,10],[6,8],[1,5],[2,3],[1,10]]  ->  3
intervals = [[1,3],[5,6],[8,10],[11,13]]       ->  1
```

**Constraints:** `1 <= intervals.length <= 10^5`; `1 <= left_i <=
right_i <= 10^6`.

The fewest groups is the most intervals that share one point: that many
can never be split apart, and taking the intervals by left end and
putting each into any group already over before it never needs more.
Intervals that only touch, as `[1, 5]` and `[5, 8]` do, share a point.

## Approaches

| file | mechanism |
|---|---|
| `groups.kara` ★ | a heap of group ends: the intervals sorted by left end, a `PriorityQueue` of each group's last right end, the smallest first; an interval starting after that end takes its group, and otherwise opens one. O(n log n) |
| `groups_sweep.kara` | a difference array up to the largest end: one added at each left end and taken away just past each right end, the running sum's most the answer. O(n + the largest end) |
| `groups_events.kara` | sorted events: an open at each left end and a close just past each right end, a close sorting before an open at one point, the most open at once the answer. O(n log n) |
| `groups_two.kara` | the left ends and the right ends sorted apart; walking the left ends, one past the earliest right end not yet passed reuses that group. O(n log n) |
| `groups_iter.kara` | iterators: `flat_map` to two events each, sorted, the open count by `scan`, its `max` the answer; carried by `karac fix` |
| `groups_solution.kara` | LeetCode's Rust template: `intervals.sort_unstable()`, then a `BinaryHeap` of `Reverse` right ends; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one
interval at `10^6`; two intervals sharing an end point; ten copies of
one; `10^5` intervals of up to 100 points and `10^5` of up to `10^5`
points, within `10^6`; then 2000 random cases of up to 30 intervals
within 1 to 60, with a checksum and the total of the answers.
`groups.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 3000 random cases of up to 6 intervals against
trying every way to put them into groups.

`groups_iter.kara` was written as Rust would write it, and `karac fix`
carries it in one call, reporting 2 edits: the array the `flat_map`
closure returns given `.into_iter()`, since Kāra's `flat_map` takes an
`Iterator`, not a collection; and the `scan` closure, written to change
its state through `*open` as Rust's does, rewritten to take the state by
value and return `Some((open, open))`.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 16 edits: `use std::cmp::Reverse;` and `use
std::collections::BinaryHeap;` deleted, and every `Reverse(..)`
unwrapped, since Kāra's `PriorityQueue` pops the smallest first;
`struct Solution;` given its braces; `mut intervals: Vec<Vec<i32>>`
written `intervals: own Vec[Vec[i32]]` with `let mut intervals =
intervals;` at the body's start; `BinaryHeap::new` written
`PriorityQueue.new`; `sort_unstable` written `sort`; the `&` of
`Some(&Reverse(e))` dropped and the peeked value `.cloned()`; and the
wrapper's widening `as i64` removed.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for one group, then two, and so on, every way to put the
intervals into that many groups tried by backtracking, any two in one
group compared point for point, and the first count that works. No
sorting, no heap, and no counting of overlaps. It checks 300 random
cases of 1 to 8 intervals within 1 to 26, which the literal reading
answers; then 30 of up to 400 intervals of up to `10^4` points within 1
to `10^5`; then 30 of up to 3000 intervals of up to 50 points within 1
to 250. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 8 intervals, the answer is the literal reading's |
| P2 | up to 400 intervals, the answer is the most intervals holding any one left end, every pair compared; above that, it is between 1 and n |
| P3 | every interval mirrored, `x` to `m + 1 - x` for `m` the largest right end: the same answer |
| P4 | the intervals in the reverse order: the same answer |
| P5 | every interval given twice: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the point most intervals share can be taken to be a
left end: move it left until it meets one. P3 holds because mirroring
keeps which pairs intersect, P4 because the groups do not depend on the
order given, and P5 because two copies of the most crowded point's
intervals must all be apart, while two copies of a best grouping give
one.

The differential prints `360 cases: checksum 703558982, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and backtracks the same way. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the intervals never sorted | P1 168, P2 201, P3 218, P4 217, P5 175, P6 227 |
| M2 | ★: touching intervals taken as apart | P1 167, P2 170, P5 75, P6 197 |
| M6 | ★: the intervals sorted by right end | P1 7, P2 34, P3 54, P4 26, P5 25, P6 59 |
| M8 | sweep: the largest end never summed | P1 29, P2 29, P3 28, P6 29 |
| M9 | sweep: no interval ever closed | P1 163, P2 196, P6 221 |
| M11 | sweep: each close counted twice | P1 108, P2 141, P3 181, P6 167 |
| M14 | events: each interval a point longer | P1 120, P2 123, P6 149 |
| M15 | events: the first event skipped | P1 300, P2 333, P5 360, P6 360 |
| M16 | events: only the latest event counted | P1 225, P2 258, P5 360, P6 285 |
| M18 | two: the right ends never sorted | P1 191, P2 224, P3 257, P4 225, P5 172, P6 250 |
| M19 | two: the left ends never sorted | P1 83, P2 116, P3 107, P4 133, P5 124, P6 141 |
| M21 | two: the left ends taken as right ends | P1 137, P2 170, P3 125, P6 196 |
| M24 | iter: the count starting at 1 | P1 300, P2 334, P5 360, P6 360 |
| M25 | iter: no interval ever closed | P1 229, P2 262, P6 288 |
| M26 | iter: each interval starting a point late | P1 212, P2 215, P6 242 |
| M30 | solution: the latest end compared | P1 126, P2 159, P5 206, P6 185 |
| M31 | solution: the right end compared with the end | P1 137, P2 166, P3 128, P6 193 |

P1, P2 and P6 kill all seventeen, P5 nine, P3 eight, and P4 four. P4
reverses the intervals, so it catches only a mutant whose answer
depends on the order they come in: the ★ and two arms' ends never
sorted (M1, M18, M19) and the ★ arm's sort by right end (M6), which
sweeps the groups out of left-end order.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for one, left over: the ★ arm's latest end compared
(M4) as the template's (M30); the left end kept as the group's end (M5,
M29) as the two arm's left ends taken as right ends (M21); touching
intervals taken as apart in the sweep, events, two and iter arms (M7,
M12, M17, M22) as the iter arm's each interval starting a point late
(M26), and in the template (M27) as the ★ arm's (M2); each interval
starting a point early (M10) as each interval a point longer (M14); the
events never sorted (M13, M23) as only the latest event counted (M16);
a reused group counted too (M20) as no interval ever closed (M25); and
the template's intervals never sorted (M28) as the ★ arm's (M1). The ★
arm's every ended group freed (M3) fails apart from every kept one, and
was left out because that arm keeps three already.

## Verification

Every arm prints the same output as `groups.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.7 to 5.8 s. The differential
takes 29 s there, 5.3 s under `karac __mir-llvm-asan` and 1.0 s under
`karac run`.

## Benchmarks

The bench builds 10 sets of `10^5` intervals starting below `9 * 10^5`,
set `i` covering up to `1 + 1000 i` points, once from the harness's
generator, then makes 5 passes, answering every set and folding each
answer plus the pass into the checksum, with the ★ arm in all five
languages. Every implementation prints `5 passes over 10 sets of 10^5
intervals: checksum 715255776`. Each copies the intervals and sorts the
copy by (left, right) ends: Kāra with `sort`, Rust with `sort`, Python
with `sorted`, C with `qsort` through a comparison function and Go with
`sort.Slice` through a closure; the last two pay a call per comparison,
and both were measured slower than Kāra and Rust here. Kāra keeps the
ends in a `PriorityQueue`, Rust in a `BinaryHeap` of `Reverse`, Python
in `heapq`, and C and Go in a binary heap written out by hand.

BENCHTAB
