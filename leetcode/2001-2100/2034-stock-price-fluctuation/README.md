# 2034. Stock Price Fluctuation

You receive a stream of records about a stock, each a timestamp and the
price at that timestamp. The records arrive out of order, and a record can
be wrong: a later record with the same timestamp corrects the earlier one.
Design `StockPrice`:

- `update(timestamp, price)` records `price` at `timestamp`, correcting any
  earlier record there;
- `current()` returns the price at the latest timestamp recorded;
- `maximum()` and `minimum()` return the highest and lowest price over all
  the current records.

```
update(1, 10); update(2, 5)
current()  ->  5      the latest timestamp is 2
maximum()  ->  10
update(1, 3)          timestamp 1 corrected to 3
maximum()  ->  5
update(4, 2)
minimum()  ->  2
```

**Constraints:** `1 <= timestamp, price <= 10^9`; at most `10^5` calls in
all; `current`, `maximum` and `minimum` are called only after an update.

A correction can remove the price that was the maximum or the minimum, so
the extremes need either a structure that removes a price (an ordered
multiset) or one that can tell a stale record from a live one when it
reaches the top (a heap checked against the map).

## Approaches

| file | mechanism |
|---|---|
| `stock.kara` ★ | a `Map` from timestamp to price, the latest timestamp, and two `PriorityQueue`s of `(price, timestamp)` records, `max_first()` and `new()`; a correction leaves its old record behind, and a query pops records off the top until the one there still matches the map. O(log n) amortized |
| `stock_sorted.kara` | a `SortedMap` from each price to how many timestamps hold it: a correction lowers the old price's count (removing it at zero, through `insert`'s returned old value) and bumps the new one through `entry(..).or_insert(0)`; the extremes are `first()` and `last()`. O(log n) a call |
| `stock_pairs.kara` | every `(price, timestamp)` record in one `SortedSet`, so two timestamps at one price are two records; a correction removes the old record before inserting the new; the extremes are the set's `min()` and `max()`. O(log n) a call |
| `stock_scan.kara` | the extremes cached as `Option`s beside the map: an update raises the maximum or lowers the minimum in place, and only a correction that lowers the timestamp holding the maximum (or raises the one holding the minimum) clears it, to be rescanned with `values().max()` at the next query. O(1), or O(n) after such a correction |
| `stock_vec.kara` | all current prices kept sorted in a plain `Vec`, a multiset: a correction finds the old price with `binary_search` and removes it, and the new one goes in at its `partition_point`; the extremes are the two ends. O(n) an update, O(1) a query |
| `stock_solution.kara` | LeetCode's Rust template (`HashMap`, a `BinaryHeap` beside a `BinaryHeap<Reverse<..>>`, `while let Some(&..) = heap.peek()`, `unreachable!()`, `&mut self`), with a `Tracker` adapting its `i32`s to the harness, carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: the answers for LeetCode's example and
five more sessions, written as `(kind, timestamp, price)` operations (kind
0 an update, 1 `current`, 2 `maximum`, 3 `minimum`); then the number of
queries and a checksum of the answers for 3000 sessions of 1 to 30
operations, timestamps up to 20 and prices up to 50, and for 5 sessions of
100000 operations, the most the constraints allow, timestamps and prices up
to 10^9 in some and crowded onto a few values in others. `stock.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the records kept in a list, an update overwriting the one with
its timestamp or appending, and every query a scan of the list for the
latest timestamp, the highest and the lowest price. It checks 1500
sessions of 1 to 25 operations, timestamps up to 12 and prices up to 30.
Every session, and the lift P2 uses, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | every price raised by the same amount raises every answer by it |
| P3 | every query asked twice in a row gives its answer twice |
| P4 | every price `p` turned into `31 - p`, with the maximum and minimum queries swapped, turns every answer `a` into `31 - a` |
| P5 | every update preceded by a wrong record at its timestamp, priced `31 - p`, leaves the answers |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a lift keeps every comparison among the prices. P3
because a query changes no record, though two of the arms pop stale
records and one rescans as it answers. P4 because `31 - p` reverses the
order of the prices, turning the highest into the lowest. P5 because the
right record corrects the wrong one at once, so every arm has to drop the
wrong price from its maximum and minimum before any query sees it: the
property doubles the corrections a session makes.

The differential prints `1500 sessions: checksum 115875527, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the top record returned without the stale check | P1 280, P4 453, P5 919, P6 280 |
| M2 | ★: a minimum record live while its timestamp is | P1 277, P4 453, P5 127, P6 277 |
| M3 | ★: the current price read as the largest | P1 495, P4 704, P6 495 |
| M4 | sorted: an old price's count never lowered | P1 453, P5 1009, P6 453 |
| M5 | sorted: the latest timestamp the last one updated | P1 500, P6 500 |
| M6 | sorted: the maximum read as its count | P1 980, P2 1011, P4 1213, P6 980 |
| M7 | pairs: the maximum read from the smallest record | P1 702, P4 869, P6 702 |
| M8 | pairs: the maximum read as its timestamp | P1 968, P2 1011, P4 1210, P6 968 |
| M9 | pairs: the current price read at the earliest timestamp | P1 675, P6 675 |
| M10 | scan: a lowered maximum never marked stale | P1 185, P4 307, P5 665, P6 185 |
| M11 | scan: the minimum never lowered | P1 455, P4 754, P5 176, P6 455 |
| M12 | scan: the stale maximum rescanned from the timestamps | P1 258, P2 271, P4 420, P5 557, P6 258 |
| M13 | vec: the old price searched one higher | P1 466, P4 108, P5 1012, P6 466 |
| M14 | vec: the new price appended unsorted | P1 725, P4 862, P5 12, P6 725 |
| M15 | vec: the new price inserted one early | P1 669, P4 852, P5 448, P6 669 |
| M16 | Rust: each price halved on its way in | P1 1306, P2 1306, P4 1306, P6 1306 |
| M17 | Rust: a correction never stored | P1 666, P5 1304, P6 666 |

P1 and P6 kill all seventeen, P4 thirteen, P5 ten, P2 four and P3 none.
P4 mirrors the prices and swaps the two extreme queries, so it sees every
edit that treats the maximum and the minimum unevenly: one side's stale
check dropped or loosened (M1, M2, M10, M11), the wrong end or the wrong
field read (M3, M6, M7, M8, M12), a halved price (M16) and the sorted Vec
kept unsorted or off by one (M13 to M15).
P5 doubles the corrections, so it sees each edit that lets a corrected
price linger, and kills the ones P4 cannot: a count never lowered (M4) and
a correction never stored (M17). P2 lifts every price, so it sees only the
edits that answer with something other than a price: a count (M6), a
timestamp (M8, M12) and a halved price (M16). P3 asks every query twice
and kills nothing: no edit here made a query change what the next one
sees, though the ★ and Rust arms pop records and the scan arm rescans as
they answer. Three edits are caught by P1 and P6 alone: the latest
timestamp set by the last update (M5), the current price read at the
earliest timestamp (M9) and, unkept, the scan arm's latest frozen at the
first timestamp.

The other thirteen fail as a kept one does, or with counts of their own.
The latest timestamp set by the last update fails alike in the ★, Vec and
Rust arms (M5); a stale price left in place fails as M4 in three more
edits: the sorted arm counting each price twice and the pairs arm
removing the wrong old record (one timestamp later, or the new price,
looked up after the insert); the maximum read from the wrong end fails as
M7 in the sorted arm and in the Rust arm's maximum heap built smallest
first, the very slip B-2026-11-09-13 made; and the Rust arm's maximum
record accepted while its price is no lower fails as M1. The ★ arm's
minimum heap built largest first, the scan arm's maximum marked stale on
the wrong correction or its latest frozen, and the Vec arm's maximum read
one from the end fail with counts of their own. Five drafts were
replaced. The ★ arm's minimum record accepted while any timestamp holds
its price changed no answer, and neither did the same edit to the Rust
arm's maximum. The sorted arm removing a price at one
timestamp left, and setting a new price's count to one, both crash on a
later lookup of the removed key. The pairs arm keying a new record by
price alone fails as M4, and was replaced to give that arm a third kept
edit of its own.

## Verification

Every arm prints the same output as `stock.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 4.8 s (sorted) to 13.4 s (pairs),
but the Vec arm 166 s, its sorted `Vec` of prices shifted on every insert
and removal through the 100000-operation sessions; the differential takes
3.9 s.

The five arms were written in Kāra and checked clean but two. The pairs
arm read the set's ends with `first()` and `last()`, as Rust's `BTreeSet`
does; the check refused them with Kāra's names, `min()` and `max()`, as
machine fixes, which `karac fix` applied. The Vec arm matched
`binary_search` with Rust's `Ok(at)` and `Err(_)`; Kāra's returns an
`Option[i64]` (docs/library/collections.md), and the check refused the two
patterns as variants `Option` does not have, with no fix and no word that
the method is where the Rust and Kāra types part. The arm was edited by
hand to `Some(at)` and `None`. Neither Rust shape of `binary_search` (an
`Ok`/`Err` match, or `unwrap_or_else(|x| x)` for the insertion point) has
a fix yet; B-2026-11-09-13 tracks it, with `partition_point` as the
translation.

The scan arm was first written to scan the map at every query. That is
O(n) a query, and on the 100000-operation sessions it ran 12 s under `karac
__mir-llvm-run` and exceeded the MIR interpreter's step limit after 950 s
under `karac __mir-run`; it now caches the extremes and rescans only when a
correction invalidates one.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (29, 1, 9 and 3 edits).
The first carries the `<..>` generics, the `::` paths, the `&mut self` and
`&self` receivers, the `&` in `prices[&ts]`, `unreachable!()`, and the
`&(..)` patterns over `peek()`, which become `peek().cloned()`; the second
deletes the `use std::collections` line; the third renames `HashMap` to
`Map` and `BinaryHeap` to `PriorityQueue`, drops each `Reverse`, and builds
the minimum heap with `PriorityQueue.new()` and the maximum heap with
`PriorityQueue.max_first()`; the fourth drops three `as i64` widenings
`Tracker` no longer needs.

That third round was wrong when this kata was written. `karac fix` decided
a heap's direction for the whole program: one `Reverse` anywhere made
every `BinaryHeap::new()` the smallest-first `PriorityQueue.new()`, so the
maximum heap became a second minimum heap, and the carried program checked
clean and answered `maximum()` with the minimum: `[5, 5, 3, 2]` for
LeetCode's `[5, 10, 5, 2]`. Each constructor's side is now read from the
heap it builds, its declared item type and what is pushed onto it, and a
constructor that cannot be told gets no fix (B-2026-11-09-13, kara
4899210bd7, `tests/kata_2034_heap_sides.rs`).

## Benchmarks

The bench builds 10 sessions of 100000 operations once in all five
languages (updates, some correcting an earlier timestamp, and the three
queries, timestamps up to 10^9 or as few as 1000, prices up to 10^9 or as
few as 100) and replays each 15 times on a fresh tracker: 150 sessions, 15
million operations, 8394285 of them queries. The map is each language's
hash map (C's an open-addressing table written for the bench) and the heaps
its binary heap (C's written for the bench). Every implementation prints
`150 sessions: 8394285 queries, checksum 968536250`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `7a9ac8e23f` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.720 to 0.787 s | 0.739 s |
| Rust (`rustc -O`) | 0.736 to 0.792 s | 0.773 s |
| C (`clang -O3`) | 0.836 to 0.887 s | 0.853 s |
| Kāra (`karac build`) | 0.871 to 0.922 s | 0.901 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.864 to 0.970 s | 0.911 s |
| Go | 1.098 to 1.145 s | 1.126 s |
| Python | 7.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.874 s) is not above its real time (0.901 s).

The sequential Kāra program is 1.23x Rust under overflow checks and 1.07x
C.
