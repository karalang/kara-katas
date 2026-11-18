# 2276. Count Integers in Intervals

Given an **empty** set of intervals, implement a data structure that
can:

- **Add** an interval to the set of intervals.
- **Count** the number of integers that are present in **at least one**
  interval.

Implement the `CountIntervals` class:

- `CountIntervals()` Initializes the object with an empty set of
  intervals.
- `void add(int left, int right)` Adds the interval `[left, right]` to
  the set of intervals.
- `int count()` Returns the number of integers that are present in
  **at least one** interval.

**Note** that an interval `[left, right]` denotes all the integers `x`
where `left <= x <= right`.

```
["CountIntervals", "add", "add", "count", "add", "count"]
[[], [2, 3], [7, 10], [], [5, 8], []]
  ->  [null, null, null, 6, null, 8]
```

**Constraints:** `1 <= left <= right <= 10^9`; at most `10^5` calls in
total will be made to `add` and `count`; at least **one** call will be
made to `count`.

The covered integers are a union of disjoint intervals, and the count
is their total length, kept as it changes. An added interval swallows
every interval it overlaps into one, so each interval is inserted once
and removed at most once: O(log n) amortised per call with an ordered
map.

## Approaches

| file | mechanism |
|---|---|
| `intervals.kara` ★ | a `SortedMap` from start to end and the total; `add` takes the interval at or below its right end by `floor`, merging and removing while it reaches the left end |
| `intervals_vec.kara` | a `Vec` of intervals in start order; two `partition_point`s bound the run an added interval overlaps, which `drain` takes out and one merged interval replaces |
| `intervals_tree.kara` | a dynamic segment tree over `[1, 10^9]`, nodes made only where an interval reaches, each holding how many of its integers are covered; a node covered whole is never entered again |
| `intervals_range.kara` | a `SortedMap` read by `range_inclusive`: from the start of the interval reaching the left end, found by `floor`, up to the right end, every interval collected in one walk, then merged and removed |
| `intervals_iter.kara` | in chains, over a `Vec` in no order: the overlapped intervals by `filter`, dropped by `retain`, a `fold` widening the new one over them, and the total moved by `map` and `sum` |
| `intervals_solution.kara` | LeetCode's Rust template: `BTreeMap<i32, i32>` and an `i32` count; `while let Some((&a, &b)) = self.map.range(..=r).next_back()` merges; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Each arm also has `play`, which takes the calls as pairs, `(left,
right)` to add and `(0, 0)` to count, and returns the counts. Every arm
prints the same 9 lines: LeetCode's example and five more (one interval
inside another, 10; two touching, 4; one added twice, 1; a gap bridged,
`[4, 6, 6]`; the widest, 10^9), each with its counts; then 1000 random
runs of 1 to 40 calls, intervals starting below 10, 100 or 10^9 and up
to 3, 30 or 10^9 wide, with a checksum; then two long runs of 10^4
calls with intervals up to 1000 wide, starting below 10^9, where they
stay apart, and below 10^6, where they merge, each with its last count
(3318165, 961080). `intervals.py` mirrors the ★ arm and its output is
byte-identical.

The long runs are 10^4 calls, a tenth of the constraints' 10^5, because
the vec and iter arms are O(n) per call: at 10^5 the vec arm took 18 s
under the interpreter. The bench takes the ★ arm to
10^5.

The iter arm was first a `partition` into the overlapped and the rest,
rebuilding the list and summing the total afresh on every add. `karac
check` named its `let (touched, mut rest)` as Rust's placement of `mut`
and `karac fix` moved it before the pattern, with the `.cloned()` the
`partition` needed. It took 53 s under the interpreter, and now drops
the overlapped in place by `retain` and moves the total by the
difference.

A sixth design, lazily merged, appended each interval to a pending list
and sorted everything at each count. It was dropped: with a count every
third call it re-sorts the whole set each time, and it did not finish
in 10 minutes under the interpreter. Writing it met two of Kāra's
choices, each named by `karac check` and rewritten by `karac fix`:
`Vec.append` is `extend(mem.take(mut b))`, and `last_mut()` is an index
write.

`karac fix` carries the template in one round, reporting 24 edits:
`use std::collections::BTreeMap;` dropped, `BTreeMap<i32, i32>` to
`SortedMap[i32, i32]`, `BTreeMap::new()` to `SortedMap.new()`, `&mut
self` to `mut ref self` and `&self` to `self`, the patterns `(&a, &b)`
to `(a, b)`, `range(..=r)` to `range_inclusive(i32.MIN, r)`,
`remove(&a)` to `remove(a)`, and in `play` the generics, `&Vec` to a
bare `Vec`, `::` to `.`, the pattern `&(left, right)` and the `as i64`
dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every integer from 1 to 60 marked when an added interval
holds it, and a count the number marked. No intervals kept. It checks
300 random runs of 1 to 20 calls, a third of them counts, intervals
starting below 10, 30 or 60 and up to 3, 10 or 60 wide within 60; then
30 runs of intervals each inside the last; then 30 runs of intervals of
three that touch end to end, shuffled. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the counts are the literal reading's |
| P2 | each interval mirrored, `[l, r]` made `[61 - r, 61 - l]`: the same counts |
| P3 | each interval moved 10^8 up: the same counts |
| P4 | the counts never fall, each at most the widths added so far and at least the widest of them, and 0 before any add |
| P5 | every add made twice in a row: the same counts |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 963864411, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that keeps
the covered integers in a `set`. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the floor of the left end | P1 123, P2 152, P4 23, P6 123 |
| M5 | ★: one more counted | P1 330, P4 262, P6 330 |
| M6 | ★: the right end never widened | P1 185, P2 211, P4 138, P6 185 |
| M7 | vec: an interval ending at the left end kept apart | P1 59, P2 81, P4 1, P5 92, P6 59 |
| M9 | vec: the drained not taken off | P1 224, P4 217, P5 315, P6 224 |
| M10 | vec: the right end from the first swallowed | P1 30, P2 39, P4 11, P6 30 |
| M12 | tree: a covered node entered again | P1 191, P2 185, P3 200, P4 119, P6 191 |
| M14 | tree: the root over `[1, 10^6]` | P3 315 |
| M15 | tree: one child for both halves | P1 315, P2 103, P3 93, P4 315, P6 315 |
| M17 | range: an interval ending at the left end kept apart | P1 45, P2 68, P4 2, P6 45 |
| M18 | range: the range half-open | P1 62, P2 82, P5 104, P6 62 |
| M21 | range: the first swallowed left in place | P1 224, P2 118, P4 12, P5 315, P6 224 |
| M22 | iter: an interval starting at the right end lost | P1 64, P2 85, P5 104, P6 64 |
| M23 | iter: the swallowed never dropped | P1 170, P4 156, P5 224, P6 170 |
| M24 | iter: the left end never widened | P1 185, P2 211, P4 120, P6 185 |
| M27 | solution: an interval ending at the left end kept apart | P1 58, P2 79, P4 2, P5 103, P6 58 |
| M29 | solution: each swallowed one short | P1 224, P5 315, P6 224 |

P1 and P6 kill sixteen, P4 thirteen, P2 twelve, P5 eight, and P3
three. The one P1 misses is the tree arm's root over `[1, 10^6]`,
right for every interval the literal reading can hold and wrong only
once they are moved 10^8 up, which P3 does. P3 catches only the tree
arm's edits: the tree alone reads a coordinate against fixed bounds,
and every other arm reads one only against another. P2 catches the edits
that treat an interval's two ends unalike, which mirroring swaps. P5
catches an edit that goes wrong when an interval meets itself: one
ending or starting where the other does kept apart, or one swallowed
and not taken off. A count off by a fixed amount, one more counted,
passes P2, P3 and P5 alike.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Five fail as a kept one does: the ★ arm's
interval ending at the left end kept apart (M1) as the template's
(M27); the ★ and iter arms' swallowed not taken off (M3, M25) as the
vec arm's drained (M9); the ★ arm's left end never widened (M4) as the
iter arm's (M24); and the iter arm's each swallowed one short (M26) as
the template's (M29). Nine fail in ways of their own and are left out
because their arms keep enough: the vec arm's interval starting at the
right end kept apart and its merged interval pushed at the end (M8,
M11), the tree arm's larger half only and its whole cover one short
(M13, M16), the range arm's floor of the right end and its first
swallowed only (M19, M20), and the template's range half-open, its
stored start the one asked and each add one short (M28, M30, M31).

## Verification

Every arm prints the same output as `intervals.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 0.4 s, the template 0.5 s, the
range arm 0.7 s, the vec arm 0.9 s, the differential 2.0 s, the tree
arm 3.2 s, and the iter arm 24.4 s, O(n) per call over the long runs.

## Benchmarks

The bench plays 10 runs of the constraints' longest, 10^5 calls, a
third of them counts, with intervals up to 1000 wide starting below
10^9 and 10^6 in turn, with the ★ arm in all five languages. Every
implementation prints `10 runs of 10^5: checksum 324613421`. Rust uses
`BTreeMap` and Python a sorted list of starts by `bisect` beside a dict
of ends. C and Go have no ordered map in their standard libraries, so
each carries a treap keyed by start with `floor` and removal by key:
the same algorithm over a different ordered structure, which the
comparison should be read with.

BENCHTAB
