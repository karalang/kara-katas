# 2080. Range Frequency Queries

Design a data structure to find the frequency of a given value in a
given subarray.

The frequency of a value in a subarray is the number of occurrences of
that value in the subarray.

Implement the `RangeFreqQuery` class:

- `RangeFreqQuery(int[] arr)` Constructs an instance of the class with
  the given 0-indexed integer array `arr`.
- `int query(int left, int right, int value)` Returns the frequency of
  `value` in the subarray `arr[left...right]`.

A subarray is a contiguous sequence of elements within an array.
`arr[left...right]` denotes the subarray that contains the elements of
`arr` between indices `left` and `right` (inclusive).

```
["RangeFreqQuery", "query", "query"]
[[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], [1, 2, 4], [0, 11, 33]]
->  [null, 1, 2]
```

**Constraints:** `1 <= arr.length <= 10^5`; `1 <= arr[i], value <=
10^4`; `0 <= left <= right < arr.length`; at most `10^5` calls will be
made to `query`.

A value's places, kept in order, answer every query for it: the count
in `[left, right]` is the places below `right + 1` less the places below
`left`, two binary searches. Built once in O(n), each query is O(log n).
The approaches differ in how they keep the places and search them.

## Approaches

| file | mechanism |
|---|---|
| `frequency.kara` ★ | every value's places in order, a `Map` of `Vec`s, and a query two `partition_point`s, the places `<= right` less those `< left`. O(n) to build, O(log n) a query |
| `frequency_scan.kara` | no index: the array kept as it is, `new(arr: own Vec[i64])`, and a query a `filter` over the slice `[left..=right]`, `count()`ed. O(right - left) a query |
| `frequency_pairs.kara` | one sorted `Vec` of `(value, place)` tuples, and a query's ends found by `partition_point` comparing tuples, from `(value, left)` to `(value, right)`. O(n log n) to build |
| `frequency_tree.kara` | every value's places in a `SortedSet`, kept in a `Map`, and a query the `range_inclusive(left, right)` walked and `count()`ed. O(log n + count) a query |
| `frequency_search.kara` | the binary search written out: a function `first_at_least(places, x)` over a `Slice`, with `lo` and `hi`, and a query the distance from `left` to `right + 1` |
| `frequency_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, `HashMap<i32, Vec<usize>>` filled through `entry(..).or_default()`, `&self`, `partition_point(\|&p\| ..)`, `map_or`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's example and four more,
each array, its queries and their counts; then the sum and a checksum of
the counts of 300 random arrays of 1 to 200 values up to 3, 30 or
`10^4`, asked 50 queries each, half for a value in the array; then the
sum of 200 queries over at least half of the constraints' largest array,
`10^5` values up to 100. `frequency.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for a query every place of the array looked at, and counted
when it lies between `left` and `right` and holds `value`. It checks 300
random arrays of 1 to 20 values up to 2, 3 or 10, each asked 12 queries;
then 20 of one value, and 20 of values all different. All 340 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | each count is the statement read literally |
| P2 | the counts for the first query's range, over every value in the array, add up to the range's length |
| P3 | a range cut in two at its middle counts the sum of its halves |
| P4 | the array reversed counts the same in the range reversed |
| P5 | each one-place range counts 1 for its own value, and the value 0, in no array, counts 0 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 arrays: checksum 688826308, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
arrays. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the range's last place left out | P1 318, P2 340, P3 291, P4 286, P5 340, P6 318 |
| M2 | ★: each place recorded one on | P1 328, P2 109, P4 316, P5 340, P6 328 |
| M3 | ★: each value's places in reverse order | P1 279, P2 228, P4 191, P5 287, P6 279 |
| M4 | scan: the other values counted | P1 340, P2 223, P5 340, P6 340 |
| M5 | scan: the values at least the one asked counted | P1 324, P2 269, P5 340, P6 324 |
| M6 | scan: the scan run to the array's end | P1 308, P2 249, P3 315, P4 319, P5 287, P6 308 |
| M7 | pairs: the range's first place left out | P1 319, P2 340, P3 294, P4 286, P5 340, P6 319 |
| M8 | pairs: the pairs left unsorted | P1 263, P2 169, P4 291, P5 263, P6 263 |
| M9 | pairs: the pairs made place first | P1 340, P2 319, P4 286, P5 340, P6 340 |
| M10 | tree: every place up to the right end counted | P1 313, P2 231, P3 318, P4 319, P5 287, P6 313 |
| M11 | tree: a value not in the array counting the range | P1 302, P5 340, P6 302 |
| M12 | tree: a value counted once at most | P1 270, P2 195, P3 261, P6 270 |
| M13 | search: the search for the first place above | P1 326, P2 91, P4 316, P5 340, P6 326 |
| M14 | search: the search never reaching the last place | P1 329, P2 235, P4 275, P5 340, P6 329 |
| M15 | search: the high end moved past the middle | P1 275, P2 163, P4 279, P5 287, P6 275 |
| M16 | solution: the adapter's array halved | P1 340, P2 287, P5 340, P6 340 |
| M17 | solution: the adapter's range one place wide | P1 314, P2 264, P3 294, P4 286, P6 314 |

P1 and P6 kill all seventeen, P2 sixteen, P5 fifteen, P4 twelve and P3
six. P2, which adds the counts of every value over one range, sees any
edit that miscounts a value the array holds; it misses only M11, whose
error falls on a value the array does not hold. P5 sees an edit that
loses a one-place range, a count off at either end or a place moved
(M1, M2, M7, M13); it misses a count capped at one (M12), right for a
range of one place, and the adapter's range of one place (M17), which a
one-place range does not change. P4, which mirrors the array, sees an
edit that leans on which way the places run: an end left out (M1, M7),
places shifted or reversed (M2, M3), a search that cannot reach the end
(M14); it misses an edit that miscounts the values alike at every place
(M4, M5, M16). P3, which cuts a range in two, sees only an edit that is
not additive over ranges: an end lost at the cut (M1, M7, M17), a range
run to an end of the array (M6, M10), a count capped (M12).

Of the thirty-two, fifteen were not kept, and none survives. Thirteen
fail as a kept one: the scan, pairs, tree, search and Rust arms' range's last
place left out as M1 (the tree's `range(left, right)`, half-open, among
them); the ★ and search arms' first place left out and the Rust
adapter's left end one on as M7; the ★, scan and pairs arms' every place
up to the right end as M10; the tree and search arms' places recorded
one on as M2. Two are killed with checks of their own but were left out
because their arm keeps three or two: the ★ arm's and the Rust arm's
value not in the array counting 1 (P1 302, P3 264, P5 340).

## Verification

Every arm prints the same output as `frequency.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.8 s to 1.5 s, but for the scan
arm's 15.4 s, which walks every query's range on the largest array, and
the differential 2.0 s (timed while other work shared the machine).

No arm met a compiler gap. The scan arm keeps the array it is given, so
its `new` takes `own Vec[i64]`, and the harness that every arm shares
hands it over with `own`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 16, 3 and 5 edits: Rust's spellings (the `use`
deleted, `HashMap<..>` and `Vec<..>` to brackets, `::` to `.`, `&self`
to `self`, the `&` of `&v`, `&value` and `|&p|` dropped); then `HashMap`
to `Map`; then `or_default()` to `or_insert(Vec.new())`, and the
`usize`s of the places and of `left as usize` to `i64`, as Kāra writes a
place. The fixed arm reads as the template does.

## Benchmarks

The bench builds 10 arrays of `10^5` values, up to 100, 1000 and `10^4`
in turn, each into the ★ arm's index once, and asks each 1000000
queries, half for a value in the array, with the ★ arm in all five
languages: `10^7` queries, each two binary searches in one value's
places. Kāra keeps the places in a `Map` and Rust in a `HashMap`, both
searched with `partition_point`; Go keeps a `map` and searches with
`sort.Search`, Python a `dict` and `bisect`, and C an open-addressing
table and a binary search written out. Every implementation prints
`10000000 queries: sum 1438347574, checksum 355759397`.

BENCHTAB
