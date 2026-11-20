# 2363. Merge Similar Items

You are given two 2D integer arrays, `items1` and `items2`,
representing two sets of items. Each array `items` has the following
properties:

- `items[i] = [value_i, weight_i]` where `value_i` represents the
  **value** and `weight_i` represents the **weight** of the `i`th item.
- The value of each item in `items` is **unique**.

Return *a 2D integer array* `ret` *where* `ret[i] = [value_i, weight_i]`*,
with* `weight_i` *being the **sum of weights** of all items with value*
`value_i`.

**Note:** `ret` should be returned in **ascending** order by value.

```
items1 = [[1,1],[4,5],[3,8]], items2 = [[3,1],[1,5]]        ->  [[1,6],[3,9],[4,5]]
items1 = [[1,1],[3,2],[2,3]], items2 = [[2,1],[3,2],[1,3]]  ->  [[1,4],[2,4],[3,4]]
items1 = [[1,3],[2,2]], items2 = [[7,1],[2,2],[1,4]]        ->  [[1,7],[2,4],[7,1]]
```

**Constraints:** `1 <= items1.length, items2.length <= 1000`;
`items1[i].length == items2[i].length == 2`;
`1 <= value_i, weight_i <= 1000`; each `value_i` in `items1` is
unique, and so is each in `items2`.

## Approaches

| file | mechanism |
|---|---|
| `merge.kara` ★ | every item of both lists added into a `SortedMap` from value to total weight through `entry(..).or_insert(0)`, which walks out in order of value. O((n + m) log(n + m)) |
| `merge_count.kara` | counting: the weights added into a table of 1001 slots, one per value, and the slots that hold weight read out in order. O(n + m + 1000) |
| `merge_two.kara` | two pointers: both lists sorted, then merged as merge sort merges, a value in both written once with its two weights added. O(n log n + m log m) |
| `merge_map.kara` | a hash `Map` from value to total, its pairs collected and sorted by value, since a `Map` walks in no set order. O((n + m) log(n + m)) |
| `merge_iter.kara` | iterators: both lists chained, sorted, and grouped by `fold` into the merged list, each item added to the last pair when it has the same value and pushed otherwise |
| `merge_solution.kara` | LeetCode's Rust template: a `BTreeMap` filled through `entry(..).or_insert(0)`, its pairs mapped to `vec![v, w]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; one item
in each list with the same value; 1000 items in each list, one per
value, with a weighted sum of the result; then 2000 random pairs of
lists of 1 to 30 items with values from 1 up to 1 to 60, with a
checksum and how many values the two lists share. `merge.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
against summing the weights value by value on 3000 random pairs.

The arms were first written with `vec![a, b]` for each pair, out of
habit from Rust. `check` reports each as `W0245`, the list literal
being `[a, b]`, and `karac fix` wrote them so: 4 edits in each of the
★, count, two-pointer and map arms, and the iter arm's 3 among its 7
below.

The iter arm's `fold` closure was first written as Rust writes it,
`|mut merged: Vec[Vec[i64]], item|`, with the last pair changed through
`match merged.last_mut() { Some(last) if last[0] == item[0] => ..., _
=> ... }`. `check` refuses the `mut` in the parameter's pattern, and
then `last_mut`, which Kāra does not have, and the closure parameter
given away and written through, since a bare closure parameter borrows.
`karac fix` carried it in 7 edits: the parameter taken `own` and
rebound `let mut merged = merged;`, the `match` rewritten as an `if`
that checks the vector is not empty and writes through
`merged[merged.len() - 1]`, and the harness's `vec!`. The `if` came out
with its `else` branch on one line, which `karac fmt` then laid out.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 18 edits: the `use std::collections::BTreeMap`
line deleted, since Kāra's `SortedMap` is in the prelude; `BTreeMap`
renamed `SortedMap` and its `::new` written with a dot;
`struct Solution;` given its braces; `Vec<..>` and `BTreeMap<..>` their
brackets; `vec![v, w]` written `[v, w]`; and `Solution::` written with a
dot. `*totals.entry(..).or_insert(0) += ..` and `into_iter().map(..)` on
the map stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every value from 1 to 1000 in turn, every item of both
lists looked at, and the value written with the sum of the weights of
the items that hold it, when any does. No map and no sort. It checks
300 random pairs of lists of 1 to 30 items with values up to 1 to 60;
then 30 pairs of up to 1000 items with values up to 1 to 1000; then 30
pairs of up to 1000 items with values up to 1000, the constraints'
largest. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | values strictly rising, every weight positive, and the weights summing to all the weights given |
| P3 | the two lists swapped: the same answer |
| P4 | each list's items reversed: the same answer |
| P5 | `items1` merged with itself: `items1` by value, each weight doubled |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 199732778, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and adds the weights in a dict. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: items2 left out | P1 360, P2 360, P3 360, P5 360, P6 360 |
| M2 | ★: a shared value overwritten, not added | P1 333, P2 333, P3 333, P5 360, P6 333 |
| M3 | ★: the weight counted once per item | P1 360, P2 360, P5 360, P6 360 |
| M7 | count: value 1000 never read out | P1 18, P2 18, P5 12, P6 18 |
| M10 | count: a weight of more than 1000 dropped | P1 288, P2 288, P5 338, P6 288 |
| M11 | count: value 1 never read out | P1 252, P2 252, P5 176, P6 252 |
| M12 | two-pointer: items2 sorted by weight | P1 317, P2 317, P3 348, P4 85, P5 331, P6 317 |
| M13 | two-pointer: the lists left unsorted | P1 346, P2 346, P4 351, P5 330, P6 346 |
| M14 | two-pointer: the tail of items2 dropped | P1 120, P2 120, P3 256, P6 120 |
| M17 | map: a value only items2 holds dropped | P1 312, P2 312, P3 349, P6 312 |
| M18 | map: items1's value 1 skipped | P1 176, P2 176, P3 252, P5 176, P6 176 |
| M21 | map: sorted largest value first | P1 352, P2 352, P5 341, P6 352 |
| M23 | iter: a run merged only with the first item | P1 318, P2 318, P5 341, P6 318 |
| M24 | iter: each run counted by its last weight | P1 333, P2 333, P5 360, P6 333 |
| M26 | iter: values merged with their neighbour | P1 346, P5 297, P6 346 |
| M27 | solution: items1 chained twice | P1 360, P2 360, P3 360, P6 360 |
| M28 | solution: each total started at the weight | P1 360, P2 360, P3 333, P5 360, P6 360 |

P1 and P6 kill all seventeen, P2 sixteen, P5 fourteen, P3 eight and P4
two. Most edits here fail nearly every case, since nearly every case
shares a value between the lists, so the kept ones are told apart by
the checks they pass rather than by how often they fail. P2 misses only
values merged with their neighbour, which keeps the total weight and
the values rising. P5, `items1` merged with itself, misses the three
edits that only touch what `items2` holds alone or that read `items1`
twice, which merging a list with itself cannot tell from the right
answer. P3, the lists swapped, fails the edits that treat the two lists
unlike each other, and P4, each list's items reversed, the two that
depend on the order the items come in: the lists left unsorted and
`items2` sorted by weight.

The last 30 cases were first pairs that share every value from 1 up to
1 to 1000, and none of the 360 held the value 1000 itself: the count
arm's value 1000 never read out (M7) failed nothing. They now draw up to
1000 items with values up to 1000, and M7 fails 18 cases. Three other
edits were rewritten before this set was run to its end. The two-pointer
arm's shared value taken from `items1` alone failed as the ★ arm's
shared value overwritten (M2), and became `items2` sorted by weight
(M12). The map arm's pairs left unsorted, and sorted by weight, failed a
different number of checks under each backend: a `Map` walks in the
per-process hash order, so what those edits print differs from run to
run, which is the language's rule and not a compiler bug. They became a
value only `items2` holds dropped (M17) and `items1`'s value 1 skipped
(M18).

Of the thirty-one, fourteen were not kept. Each total started at one,
the pairs written weight first and the largest value dropped in the ★
arm (M4, M5, M6), and the template's first pair dropped and value
written twice (M29, M30), fail every case of P1, P2 and P5 alike, as the
weight counted once per item (M3) does. `items2` written over `items1`
in the count arm (M8), a shared value advancing only `items1` and the
smaller of two values taken from `items2` in the two-pointer arm (M15,
M16), `items2` overwriting in the map arm (M19) and a later weight
written over the total in the template (M31) all fail as the ★ arm's
shared value overwritten (M2). A missing value started at its weight in
the map arm (M20) fails as `items2` left out (M1); `items1` chained
twice in the iter arm (M25) as in the template (M27); and the slots
read out from the top in the count arm (M9) as the map sorted largest
value first (M21). The iter arm's pairs left unsorted (M22) fails apart
from every kept one, and was left out to keep three to an arm.

## Verification

Every arm prints the same output as `merge.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 0.9 s but the template,
2.0 s, which narrows every pair to `i32` and widens it back. The
differential takes 24 s there and 1.2 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 pairs of lists once from the harness's generator,
pair `a` holding `100 (a + 1)` and `1000 - 50 a` items with distinct
values from 1 to 1000 in a shuffled order and weights from 1 to 1000,
then makes 400 passes, pass `p` folding the merged list's length, its
last weight and `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `400 passes over 10 pairs of
lists: checksum 324856420`. Rust uses `BTreeMap` and Python a sorted
list of values by `bisect` beside a dict of totals. C and Go have no
ordered map in their standard libraries, so each carries a treap keyed
by value with insert-or-add and an in-order walk: the same algorithm
over a different ordered structure, which the comparison should be read
with. Every implementation allocates its map and its result in each
call.

BENCHTAB
