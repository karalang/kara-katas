# 2349. Design a Number Container System

Design a number container system that can do the following:

- **Insert** or **Replace** a number at the given index in the system.
- **Return** the smallest index for the given number in the system.

Implement the `NumberContainers` class:

- `NumberContainers()` Initializes the number container system.
- `void change(int index, int number)` Fills the container at `index`
  with the `number`. If there is already a number at that `index`,
  replace it.
- `int find(int number)` Returns the smallest index for the given
  `number`, or `-1` if there is no index that is filled by `number` in
  the system.

```
["NumberContainers", "find", "change", "change", "change", "change", "find", "change", "find"]
[[], [10], [2, 10], [1, 10], [3, 10], [5, 10], [10], [1, 20], [10]]
->  [null, -1, null, null, null, null, 1, null, 2]
```

**Constraints:** `1 <= index, number <= 10^9`; at most `10^5` calls in
total will be made to `change` and `find`.

An index holds one number at a time, so a change must take the index
away from the number it held. The lazy way never does: each number
keeps a min-heap of every index ever given it, and find throws away the
indices at the top that now hold something else. Each index is pushed
once per change and popped at most once, so the work is `O(log n)` per
call, amortized.

## Approaches

| file | mechanism |
|---|---|
| `containers.kara` ★ | lazy heaps: a map from each index to its number, and for each number a min-first `PriorityQueue` of every index ever given it; a change only pushes, and find pops the indices at the top that now hold another number. O(log n) amortized |
| `containers_set.kara` | sorted sets: a map from each index to its number and a map from each number to the `SortedSet` of indices that hold it; a change moves the index from its old number's set to the new one's, and find reads the set's least. O(log n) |
| `containers_naive.kara` | no maps: a vector of (index, number) pairs; a change overwrites its index's pair or appends one, and find walks every pair for the least index that holds the number. O(n) per call |
| `containers_walk.kara` | one `SortedMap` from each index to its number; find walks the indices in rising order and stops at the first that holds the number. O(n) per find |
| `containers_iter.kara` | iterators: a map from each index to its number, and find as `filter` over its entries, `map` to the index and `min`, -1 through `unwrap_or` |
| `containers_solution.kara` | LeetCode's Rust template: a `HashMap<i32, i32>` and a `HashMap<i32, BTreeSet<i32>>`, the old index removed through `if let Some(&old)` and `get_mut`, the new one put in through `entry().or_default()`, and find as `and_then` on the set's `iter().next().copied()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

The calls are given to a `run` function as `(kind, a, b)` triples,
`(0, index, number)` for a change and `(1, number, 0)` for a find, and
it returns the finds' answers. Every arm prints the same 5 lines:
LeetCode's example; an index changed twice; the largest index and
number; `2 * 10^4` calls over 500 indices and 50 numbers, with a
checksum and how many finds found an index; then 2000 random scripts of
1 to 40 calls over indices 1 to 8 and numbers 1 to 4, three changes to
every two finds, with a checksum, the answers' sum and how many found
nothing. `containers.py` mirrors the ★ arm with `heapq` and its output
is byte-identical, and the mirror was checked against a plain dict on
3000 random scripts.

The ★ arm gives a new number its heap with `self.heaps[number] =
PriorityQueue.new();`. `check` first refused that as a queue whose
element type nothing fixed (E0238), though the map's value type fixes
it, as a typed `let` would; a generic constructor assigned to a typed
place now takes its type from the place (B-2026-11-21-39, fixed).

The sorted-set arm was first written to read the set with `first()`,
Rust's `BTreeSet::first`; `check` says Kāra's is `min()`, and `karac
fix` makes the change in one edit.

`karac fix` carries the template in one call, reporting 24 edits.
`check` first reports 12 errors and offers 16 edits for them: the
`use std::collections::{BTreeSet, HashMap};` line deleted, since both
are in the prelude; the six brackets of `HashMap<i32, i32>` and
`HashMap<i32, BTreeSet<i32>>`; `HashMap::new` to `.` twice; `&mut self`
to `mut ref self` and `&self` to `self`; the `&` of the pattern
`Some(&old)` dropped with `.cloned()` put on the value matched, three
edits; and the `&` of the arguments `&index` twice, `&old` and
`&number` dropped. The other eight follow from those: `HashMap` to
`Map` in the two types and the two calls; `BTreeSet` to `SortedSet`;
`or_default()` to `or_insert(SortedSet.new())`; `copied()` to
`cloned()`; and the wrapper's `as i64` on the `i32` answer dropped.
`entry`, `get_mut`, `and_then` and `iter().next()` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: no container is kept at all, only the calls so far; find
reads them back, and an index holds the number of the latest change
that names it. The least index whose latest change gave the number, or
-1. It checks 300 random scripts of 1 to 20 calls over indices 1 to 8
and numbers 1 to 4, three changes to every two finds; then 30 of up to
300 calls over indices up to `10^9` and numbers 1 to 3; then 30 of up
to 300 calls over indices 1 to 3 and numbers 1 and 2. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | up to 20 calls, the answers are the literal reading's |
| P2 | one answer to each find, each -1 or an index some earlier change named |
| P3 | every index doubled: every answer doubled, -1 kept |
| P4 | every number made 100 more, in the changes and the finds: the same answers |
| P5 | every find made twice in a row: each answer twice |
| P6 | each arm agrees with at least three of the other five |

P3 holds because doubling keeps the indices' order; P5 because a find
changes nothing the statement can see, though the ★ arm's find does pop
its heaps.

The differential prints `360 cases: checksum 938671020, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same scripts and keeps a plain dict. On a failure it prints the
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
| M2 | ★: the stale index kept and the next one skipped | P1 43, P5 67, P6 71 |
| M5 | ★: a missing number answered 0 | P1 239, P2 281, P6 281 |
| M6 | ★: a change never pushed when the number has a heap | P1 109, P6 165 |
| M9 | set: an emptied number answered 0 | P1 51, P2 79, P6 79 |
| M10 | set: a number made fresh on every change | P1 105, P6 163 |
| M11 | set: the new number's even index dropped | P1 141, P3 237, P6 198 |
| M12 | naive: a change appended, the old pair kept | P1 86, P6 115 |
| M13 | naive: a change to a held index ignored | P1 115, P6 143 |
| M15 | naive: the first pair found taken | P1 78, P6 126 |
| M17 | walk: the last index found returned | P1 130, P6 188 |
| M18 | walk: the index after the match returned | P1 212, P2 243, P3 270, P6 270 |
| M21 | walk: a number matched by its parity | P1 189, P6 217 |
| M23 | iter: every held index matched | P1 191, P6 246 |
| M25 | iter: the index found counted, not named | P1 275, P2 326, P3 270, P6 335 |
| M26 | iter: an index equal to the number matched | P1 206, P3 223, P4 203, P6 264 |
| M29 | solution: the new position never stored | P1 212, P6 270 |
| M31 | solution: an emptied number answered 0 | P1 245, P2 298, P6 298 |

P1 and P6 kill all seventeen, P2 five, P3 four, and P4 and P5 one
each. P4 adds 100 to every number, which keeps every comparison an arm
makes, so only a mutant that sets an index against a number fails it:
the iter arm's index equal to the number matched (M26). P5 asks each
find twice, which changes nothing but the ★ arm's heaps, so only the
★ arm's stale index kept and the next one skipped (M2) fails it: its
first find gives up at a stale top and pops it, and the second finds
the index below.

Of the thirty-one, fourteen were not kept. Eleven fail the same checks
as a kept one: a stale index returned in the ★ arm (M1), the old holder
or position never cleared in the set arm and the template (M7, M27) and
the template's index never recorded (M30), all as the naive arm's change
appended with the old pair kept (M12), since each leaves an index
answering for a number it no longer holds; the largest index taken in
the set, naive and iter arms and the template (M8, M14, M22, M28) as
the walk arm's last index found returned (M17); a change kept only for
a new index in the walk and iter arms (M19, M24) as the naive arm's
change to a held index ignored (M13); and the walk arm's missing number
answered 0 (M20) as the template's (M31). Three end in a runtime error,
not a wrong answer, under both backends: the ★ arm's index pushed under
its old number (M3) and largest index returned by pushing `-index`
(M4) read the index map at a key it never had, and the naive arm's last
pair never read (M16) slices an empty list at `0..len - 1`.

## Verification

Every arm prints the same output as `containers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 5.8 s, the iter arm the
slowest, since each of its finds filters the whole map. The
differential takes 3.4 s there, 1.1 s under `karac __mir-llvm-asan` and
0.6 s under `karac run`.

## Benchmarks

The bench builds `2 * 10^5` calls once from the harness's generator,
two changes to every find, over `10^5` indices and 1000 numbers, then
makes 20 passes, each through a fresh system, pass `p` folding each
answer plus `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `20 passes over 2 * 10^5 calls:
checksum 225954463`. Kāra, Rust, Go and Python use their own hash maps
and heaps (`Map` and `PriorityQueue`; `HashMap` and `BinaryHeap` of
`Reverse`; `map` and a hand-written heap; `dict` and `heapq`); C has
neither, and uses an open-addressing hash map with linear probing and
a hand-written heap.

BENCHTAB
