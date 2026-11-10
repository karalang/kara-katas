# 2070. Most Beautiful Item for Each Query

You are given a 2D integer array `items` where `items[i] = [price_i,
beauty_i]` denotes the price and beauty of an item respectively.

You are also given a 0-indexed integer array `queries`. For each
`queries[j]`, you want to determine the maximum beauty of an item whose
price is less than or equal to `queries[j]`. If no such item exists, then
the answer to this query is `0`.

Return an array `answer` of the same length as `queries` where
`answer[j]` is the answer to the `j`-th query.

```
items = [[1,2],[3,2],[2,4],[5,6],[3,5]], queries = [1,2,3,4,5,6]  ->  [2,4,5,5,6,6]
items = [[1,2],[1,2],[1,3],[1,4]], queries = [1]                   ->  [4]
items = [[10,1000]], queries = [5]                                 ->  [0]
```

**Constraints:** `1 <= items.length, queries.length <= 10^5`;
`items[i].length == 2`; `1 <= price_i, beauty_i, queries[j] <= 10^9`.

Sorted by price, the items a query affords are a prefix, so its answer
is the best beauty of that prefix. One pass leaves every prefix's best,
and each query finds the end of its prefix by binary search:
O((n + m) log n). The approaches differ in how they find a query's
prefix: by search, by a sweep over the queries in order, or by a lookup
in an ordered map.

## Approaches

| file | mechanism |
|---|---|
| `beauty.kara` ★ | the items sorted with `sort_by_key`, a `Vec` of every prefix's best, and each query's prefix ended by `partition_point(\|item\| item[0] <= q)`. O((n + m) log n) |
| `beauty_sweep.kara` | offline: the queries' places sorted by the query, and one cursor over the sorted items moved past every price the next query affords, the best so far carried with it and written back at the query's place |
| `beauty_floor.kara` | a `SortedMap` of the best beauty at each price, then a second of the best at each price or below, built by a walk in key order; a query's answer is `floor(q)`'s value, or 0 |
| `beauty_stairs.kara` | the items as `struct Item`s, sorted, and only those that raise the best beauty kept as a staircase rising in price and beauty; a binary search over `lo` and `hi` written out finds the last step a query affords |
| `beauty_peek.kara` | two sorted streams: the queries with their places, sorted, and the sorted items as a `peekable` iterator that owns them, taken with `next_if(\|item\| item[0] <= q)` while the next query affords them |
| `beauty_solution.kara` | LeetCode's Rust template (`mut items: Vec<Vec<i32>>`, `sort_unstable()`, a `vec![0; n]` of bests, `queries.iter().map(\|&q\| ..)` with `partition_point` and `.collect()`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples and two
more, each shop's size, queries and answers; then a checksum of the
answers for 300 random shops of 1 to 50 items and 1 to 50 queries,
prices, beauties and queries up to 10, 1000 or `10^9`; then the checksum
and sum of the answers for the constraints' largest, 100000 items and
100000 queries. `beauty.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each query every item looked at, and the greatest beauty
of those whose price is at most the query kept, 0 if there is none. It
checks 300 random shops of 1 to 8 items and 1 to 8 queries, prices,
beauties and queries up to 10; then 20 whose every item has one price,
and 20 whose every query is an item's price, one less or one more. All
340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | the items in reverse order and the queries reversed give the answers reversed |
| P3 | one more item never lowers an answer |
| P4 | every query one higher never lowers its answer |
| P5 | every answer is 0 when its query affords no item, and otherwise the beauty of an item it affords |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 shops: checksum 501702083, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
shops. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivors under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the best of each prefix not carried | P1 205, P2 106, P3 85, P4 103, P6 205 |
| M2 | ★: the items sorted by beauty | P1 116, P2 77, P3 53, P5 59, P6 116 |
| M3 | ★: a query affording nothing given the first best | P1 141, P2 33, P3 19, P5 141, P6 141 |
| M4 | sweep: the queries left in their order | P1 166, P2 138, P5 166, P6 166 |
| M5 | sweep: a query's own price out of reach | P1 179, P5 129, P6 179 |
| M6 | sweep: every other item passed over | P1 138, P2 87, P3 43, P6 138 |
| M7 | floor: the last item at a price kept, not the best | P1 58, P2 97, P3 31, P6 58 |
| M8 | floor: the price at or above the query | P1 251, P3 30, P4 138, P5 251, P6 251 |
| M9 | floor: a query affording nothing answered 1 | P1 141, P5 141, P6 141 |
| M10 | stairs: the last step never searched | P1 289, P2 53, P3 13, P5 113, P6 289 |
| M11 | stairs: the first step's beauty | P1 187, P2 70, P3 20, P6 187 |
| M12 | stairs: the steps sorted by beauty | P1 115, P2 85, P3 35, P5 62, P6 115 |
| M13 | peek: one item taken for each query | P1 136, P2 115, P3 23, P6 136 |
| M14 | peek: the items left unsorted | P1 170, P2 206, P5 143, P6 170 |
| M15 | peek: the best forgotten after each query | P1 241, P2 111, P4 164, P5 218, P6 241 |
| M16 | solution: the items left unsorted | P1 119, P2 169, P3 14, P5 104, P6 119 |
| M17 | solution: the adapter's items with price and beauty swapped | P1 306, P5 289, P6 306 |

P1 and P6 kill all seventeen, P2 thirteen, P5 twelve, P3 eleven and P4
three. P5 sees an answer no affordable item has: a query's own price
out of reach (M5), a query affording nothing answered with something
(M3, M9), or the price and beauty swapped (M17). P2, which reverses both
lists, sees an edit whose answer depends on the order of the items or
the queries, which no correct arm's does: a sort left out (M4, M14, M16),
or the last item at a price kept in place of the best (M7). P3 sees an
answer that falls when an item is added, an arm that keeps the last
beauty in place of the best (M1) or the wrong step (M10, M11); P4, which
raises every query, the three edits whose answer can fall as the
queries rise, the best not carried (M1), the price at or above (M8),
and the best forgotten between queries (M15).

Of the thirty-two, fifteen were not kept. Two survive, and both are
equivalent: the ★ arm's best starting at 1, since every beauty is at
least 1 and a query affording nothing is answered 0 by its own branch,
and the stairs arm's step for an equal beauty too, which answers the
same beauty. Ten fail as a kept one: the ★, floor, stairs, peek and Rust
arms' query's own price out of reach as M5; the sweep, stairs and peek
arms' last item's beauty in place of the best as M1; the peek arm's
queries left in their order as M4; the sweep arm's items left unsorted
as M14. Two fail alike and neither is kept: the floor arm's each price's
own best and the Rust arm's each item's own beauty (P1 182, P3 53, P4
108). One is killed with checks of its own but was left out because its
arm keeps two: the Rust adapter's queries one higher (P1 154, P5 154).

## Verification

Every arm prints the same output as `beauty.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 1.9 s to 5.7 s, the largest
problem's 100000 items most of it, except the floor arm at 10.9 s, which
builds two trees of them, and the differential 1.6 s (timed while other
work shared the machine).

The kata met four gaps, three fixed in the compiler and one a ledger
row. The library's `Peekable` had only `peek`, and the peek arm's
`next_if` was refused "no method 'next_if' on type 'Peekable'"; it was
added, as Rust's. With it, the arm's loop over `sorted.iter()`, the
items borrowed, is refused by MIR borrowck, `write of _11 while it is
borrowed [E0516]`: the closure passed to `next_if`, or to `find`, is
taken to be stored into the iterator it is handed with (B-2026-11-10-24); the
arm takes the items owned, with `into_iter()`, as the sorted copy is the
arm's own. Rust's `best.range(..=q).next_back()` on a `SortedMap`, the
floor arm's first spelling, came with nothing past "method 'range'
expects 2 argument(s), found 1"; it now names the end to supply and
`floor(q)`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 20, 3 and 1 edits: Rust's spellings (`Vec<..>` to
brackets, `mut items:` to `items: own` with a `let mut` in the body, the
`&` of `|&q|`, `|&x|` and `|&a|` dropped, `struct Solution;` to `struct
Solution {}`, `::` paths to `.`); then `sort_unstable()` to `sort()`,
and `vec![0; n]` and `let mut m = 0` to `0i32` and `m: i32`, whose
literals kept the default `i64`; then the `vec![..]` to `Vec.filled`.
Its closure's tail, `if idx == 0 { 0 } else { best[idx - 1] }`, was
first refused at the `collect()`: checked against `map`'s own result
type, the literal branch made it `i64` before the `i32` branch was seen.
The compiler now joins the branches first, and the fixed arm reads as
the template does.

## Benchmarks

The bench answers 20 shops of the constraints' largest size with the ★
arm in all five languages: 100000 items and 100000 queries each,
prices, beauties and queries up to `10^9`. C sorts with a stable merge
sort, as Kāra's `sort_by_key` is stable, and Go with
`sort.SliceStable`. Every implementation prints `20 shops: sum
1999714666400381, checksum 818690329`.

BENCHTAB
