# 1146. Snapshot Array

Implement a SnapshotArray that supports the following interface:

- `SnapshotArray(int length)` initializes an array-like data structure
  with the given length. Initially, each element equals 0.
- `void set(index, val)` sets the element at the given `index` to be
  equal to `val`.
- `int snap()` takes a snapshot of the array and returns the `snap_id`:
  the total number of times we called `snap()` minus 1.
- `int get(index, snap_id)` returns the value at the given `index`, at
  the time we took the snapshot with the given `snap_id`.

```
["SnapshotArray","set","snap","set","get"]
[[3],[0,5],[],[0,6],[0,0]]                  ->  [null,null,0,null,5]
```

**Constraints:** `1 <= length <= 5 * 10^4`; `0 <= index < length`;
`0 <= val <= 10^9`; `0 <= snap_id <` (the total number of times we call
`snap()`); at most `5 * 10^4` calls will be made to `set`, `snap`, and
`get`.

The arms are `struct SnapshotArray` with `new(length)`, `set(mut ref
self, index, val)`, `snap(mut ref self) -> i64` and `get(self, index,
snap_id) -> i64`. The harness passes LeetCode's `int`s as `i32`, which the
Kāra arms take as `i64` and the Rust arm as `i32`.

## Approaches

A snap need not copy anything: a place's value at a snap is the value of
its last set made before that snap was taken, so each place needs only
the snaps at which it changed.

| file | mechanism |
|---|---|
| `snapshot_array.kara` ★ | a history for each place, the (snap, value) pairs at which it changed, starting from (0, 0); a set in the snap the history ends with overwrites that pair; a get takes the last pair at or before the snap asked, found with `partition_point`. O(1) set and snap, O(log s) get |
| `snapshot_array_sorted.kara` | a `SortedMap` for each place from the snap a value was set in to the value; a get takes the `floor` of the snap asked, or 0. O(log s) set and get |
| `snapshot_array_keyed.kara` | one `SortedMap` for the whole array keyed by (place, snap); the `floor` of (place, snap asked) is that place's last entry unless it falls on an earlier place. O(log m) set and get |
| `snapshot_array_diffs.kara` | what each snap changed: the sets since the last snap in a `Map` from place to value, stored by the snap (`mem.take`); a get walks the stored maps back from the snap asked to the first that changed the place. O(1) set and snap, O(s) get |
| `snapshot_array_solution.kara` | a Rust solution as LeetCode's Rust users write it (`i32` fields, `vec![vec![(0, 0)]; length as usize]`, `last_mut` to overwrite the current snap's pair, `binary_search_by_key` matched on `Ok` and `Err`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 14 lines: LeetCode's example; a get before any
set (0); two sets before a snap, the second kept; a snap with nothing set;
an old snap read after its value is overwritten; one place set and
snapped five times. Then over 2000 random sessions of 1 to 60 calls on 1
to 20 places, a third of the calls snaps or, every other session, a
tenth, the gets' answers summed and a checksum (`2000 random sessions:
gets total 1937645146745, checksum 3360841`), and three sessions at the
constraints' largest, 50000 places and up to 50000 calls: half the places
set once, one snap, and those places read back; one place set and
snapped 12500 times and read at every 50th snap; and 50000 random calls,
one in a hundred a snap. `snapshot_array.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every snap copies the whole array, and a get reads the copy.
It checks 2000 sessions of 1 to 40 calls on 1 to 8 places in four kinds
of 500: values 0 to 4; a snap every other call; at most three places and
sets two calls in three, so a snap's sets overwrite each other; values up
to 10^9. A get asks a snap already taken. Every random choice, P5's
names, P6's values, P7's snaps and P8's places among them, is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answers are the literal ones |
| P2 | each snap's id is the number of snaps before it |
| P3 | every get asked again after the session's last call answers the same |
| P4 | a get answers 0 or a value some set wrote to its place |
| P5 | the places renamed gives the same answers |
| P6 | every set made first with another value gives the same answers |
| P7 | every snap taken twice, a get asking either of the pair, gives the same answers |
| P8 | more places, never set, gives the same answers |

All 80,000 checks pass on every arm: `2000 sessions: checksum 939195126,
80000 checks over 5 arms: 0 failures`. A Python reading of the same
sessions, by the same copying, with the seven properties asserted against
the ★ arm's mirror, gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-eight are caught; two are
equivalent. The diffs arm never clearing its changes at a snap stores in
each snap's map every change so far, at its value then, so the walk back
finds the place in the map of the snap asked, with the right value. The
solution arm's first search taken past the snap asked lands at the end of
the pairs at or before it, never below the second search, so every get
takes the `Err` branch, `h[i - 1]`, which is the right pair either way.
Fifteen are kept, no two failing the same checks; one of them stops the
run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pair before the snap asked | stops: index out of bounds |
| M2 | ★: snap ids from 1 | P1 1872, P2 1872 |
| M3 | ★: the larger of a snap's sets kept | P1 482, P6 1011 |
| M4 | ★: a set overwrites the last snap's pair too | P1 573, P3 348, P7 573 |
| M5 | sorted: the floor of the snap before | P1 1041, P7 766 |
| M6 | sorted: a place never set reads -1 | P1 1193, P4 1193 |
| M7 | sorted: the first of a snap's sets kept | P1 660, P6 1352 |
| M8 | keyed: an earlier place's entry taken | P1 778, P3 677, P4 700, P5 773 |
| M9 | keyed: entries keyed (snap, place) | P1 1212, P3 243, P4 527, P5 801, P7 798 |
| M10 | keyed: the floor of the snap after | P1 935, P3 574, P7 665 |
| M11 | diffs: the walk from snap 0 forward | P1 581 |
| M12 | diffs: a place never set reads the snap | P1 851, P4 789, P7 1075 |
| M13 | solution: the first pair never overwritten | P1 659, P7 461 |
| M14 | solution: the overwrite test turned | P1 1324, P3 1157, P7 482 |
| M15 | solution: a get reads the next place | P1 1111, P4 821, P5 654, P8 771 |

P1 catches all twenty-six edits that let the run finish. P7 catches
ten, the edits that read a snap next to the one asked or let a set
reach one: with every snap taken twice, the snap next to the one asked
is half the time its twin, which holds the same array, so an edit off by
one snap answers differently there than in the session as given (M4, M5,
M9, M10, M12, M13, M14). P4 catches nine, the edits that answer a value
never set at the place: a fixed or computed value for a place never set
(M6, M12), or another place's value (M8, M9, M15). P3 catches five, the
edits whose answer for an old snap changes as later calls come: a set
reaching back into the snap before (M4); another place's last entry,
which a later set to that place moves (M8); entries filed by snap, among
which later snaps' entries fall (M9); a floor past the snap asked, which
a later set reaches (M10); and the overwrite test turned, which
overwrites the pair of an earlier snap (M14). P5 catches six, the edits that tell places apart by their number
(M8, M9, M15 and three not kept). P2 catches the five edits to the snap
ids, P6 the four that keep the first or the larger of a snap's sets
rather than the last (M3, M7), and P8 only M15, whose next place, taken
around the end of the array, changes when the array is longer. The edit
that stops the run is the ★ arm's pair before the snap asked: at snap 0
it asks for the pair before the first, at index -1; the solution arm's
pair before an exact match stops the same way.

Of the thirteen caught and not kept, eight fail exactly as a kept one:
snap ids from 1 in the sorted and diffs arms and by twos in the keyed
arm, as M2; a set filed under the next snap in the sorted arm and the
snap asked never read in the diffs arm, as M5; the first of a snap's sets
kept in the keyed and diffs arms, as M7; and the solution arm's pair
before an exact match, which stops as M1. The other five (a place never
set reading 1 and places paired up for sets in the ★ arm, a get reading
the place mod 3 in the sorted arm, a place never set reading its index in
the keyed arm, and snap ids from 1 in the solution arm, whose history
starts at a snap no get asks) each fail in a way of their own and were
not needed.

## Verification

Every arm prints the same output as `snapshot_array.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The ★, sorted, keyed and diffs arms were written as Kāra. `karac fix`
dropped the `*` from what a `SortedMap`'s `floor` hands back in the
sorted and keyed arms (`*v`, `*place`), as a pair of borrows
destructured binds its numbers by value, and `std.mem.take` to `mem.take` in the diffs arm.
`karac fix` carried the solution arm in five rounds: `Vec<..>` to
`Vec[..]`, `&mut self` and `&self` to `mut ref self` and `self`, `&mut`
and `&` at the borrows to `mut ref` and `ref`, and `&snap_id` and
`|&(s, _)|` to `snap_id` and `|(s, _)|`; then the inner `vec!` to an array
literal, `last_mut` to an index of the last element, and the
`binary_search_by_key` match to two `partition_point`s; then
`vec![..; length as usize]` to `Vec.filled`; then the `as usize` casts to
`as i64`; then those casts dropped, an `i32` widening to `i64` by itself.

The kata found two gaps. The match on `binary_search_by_key` was refused
with only "no method 'binary_search_by_key' on type 'Vec'", where the
same match on `binary_search` is carried through `partition_point`
(B-2026-11-09-14). Kāra has neither `binary_search_by_key` nor
`binary_search_by`, and now a match, an `if let` or an `unwrap_or_else`
on either is carried too: the key closure `|p| key` against `k` searches
with `partition_point(|p| key < k)`, and the index found holds `k` when
it lies below `partition_point(|p| key <= k)`; an ordering closure reads
`order == Ordering.Less` and `order != Ordering.Greater` for the two
(B-2026-11-13-6, fixed). And `Vec.filled(length as i64, ..)`, left once
`as usize` had become `as i64`, was not reported as a cast `i32` takes by
itself, as the same cast at a user function's `i64` parameter is: a
library argument was checked against `i64` only after it was typed with
none expected. Now it is reported and `karac fix` drops it
(B-2026-11-13-7, fixed). The solution arms of four other katas and
their differentials carried the same kind of cast at a library `i64`
argument (`Vec.filled(n as i64, ..)` in 1514 and 2028, `chunks(n as
i64)` in 2022, `truncate(k as i64)` in 2099), and lost it, with the same
output.

## Benchmarks

The bench builds one array of 50000 places, LeetCode's longest. Each of
50000 rounds sets 50 random places to random values, takes a snap, and
asks 50 random places at random snaps taken so far, with the ★ arm:
5,050,000 calls, the histories growing to 2.5 million pairs. Every
implementation prints `50000 rounds of 50 sets, a snap and 50 gets on
50000 places: gets total 1068070399382382, checksum 623776380`. Each
place's history is a growable vector of pairs: Kāra's `Vec`, Rust's
`Vec`, Go's slice, and in C an array grown by doubling with `realloc`.
The get is `partition_point` in Kāra and Rust, `sort.Search` in Go, a
hand-written binary search of the same shape in C, and `bisect_right`
with a key in Python.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `4341008d1e`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.399 to 0.457 s | 0.428 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.402 to 0.526 s | 0.428 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.383 to 0.465 s | 0.431 s |
| Kāra (`karac build`) | 0.397 to 0.509 s | 0.433 s |
| Rust (`rustc -O`) | 0.415 to 0.515 s | 0.434 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.421 to 0.460 s | 0.438 s |
| C (`clang -O3`) | 0.431 to 0.486 s | 0.451 s |
| Go | 0.636 to 0.771 s | 0.673 s |
| Python | 14.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra, Rust with and without overflow checks, and C all land within
5% of one another, inside each other's ranges. Each call is a few
comparisons on one place's history, chosen at random among 50000 that
together outgrow the cache, so the calls likely wait on memory more than
they compute; this README infers that from the tie and has not measured
it. Go takes about 1.6x Kāra's median and Python about 33x.
