# 1580. Put Boxes Into the Warehouse II

You are given two arrays of positive integers, `boxes` and `warehouse`,
representing the heights of some boxes of unit width and the heights of
`n` rooms in a warehouse respectively. The warehouse's rooms are labeled
from `0` to `n - 1` from left to right where `warehouse[i]` (0-indexed)
is the height of the `i`th room.

Boxes are put into the warehouse by the following rules:

- Boxes cannot be stacked.
- You can rearrange the insertion order of the boxes.
- Boxes can be pushed into the warehouse from either side (left or right).
- If the height of some room in the warehouse is less than the height of
  a box, then that box and all other boxes behind it will be stopped
  before that room.

Return the maximum number of boxes you can put into the warehouse.

```
boxes = [1,2,2,3,4], warehouse = [3,4,1,2]    ->  4
boxes = [3,5,5,2],   warehouse = [2,1,3,4,5]  ->  3
boxes = [1,2,3],     warehouse = [1,2,3,4]    ->  3
boxes = [4,5,6],     warehouse = [3,3,3,3,3]  ->  0
```

**Constraints:** `n == warehouse.length`;
`1 <= boxes.length, warehouse.length <= 10^5`;
`1 <= boxes[i], warehouse[i] <= 10^9`.

## Approaches

A box reaches room `i` from the left only past the lowest room before it,
and from the right only past the lowest room after it, so the room's
usable height is the larger of its prefix and suffix minimum. Filling the
rooms deepest first, any set of boxes that fits those heights one to one
goes in.

| file | mechanism |
|---|---|
| `warehouse.kara` ★ | the usable heights from two passes over copies of `warehouse`, sorted, and the boxes sorted; each room in rising order takes the smallest box left when it fits. O(n log n + m log m) |
| `warehouse_multiset.kara` | the same heights, built with a running minimum each way, taken highest first; each room takes the tallest box left that fits, found by `floor` in a `SortedMap` of box heights to their counts. O((n + m) log n) |
| `warehouse_search.kara` | if `k` boxes fit, the `k` smallest do, against the `k` highest usable rooms, element by element once both are sorted; a binary search on `k` over that test. O((n + m) log(n + m)) |
| `warehouse_solution.kara` | LeetCode's Rust template: the boxes tallest first, each pushed in from the left when the leftmost free room is high enough, else from the right, else left out; carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's four examples and two more,
then the boxes placed and a checksum for 3000 random problems of up to 6
boxes and rooms with heights to 6, 300 of up to 1000 with heights to 1000,
and 10 of up to 100000 with heights to `10^9`. `warehouse.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the boxes pushed in one at a time in every order, each from
either side, each going on until the next room is lower than it or holds
a box, the most any sequence leaves inside (a search over the used boxes
and full rooms, memoized). It checks 3000 problems of 1 to 6 boxes and 1
to 6 rooms with heights from 1 to 6, every random choice drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the warehouse reversed leaves the answer |
| P3 | the boxes in reverse order leave the answer |
| P4 | every height doubled leaves the answer |
| P5 | a box taller than every room added leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 165812553, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M8 nudged the binary search's lower bound after every miss; it
was killed (P1 5, P5 5, P6 5) but was not an edit anyone would make, and
was replaced by an upper bound one short.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the usable height the smaller of the two minimums | P1 1600, P6 1600 |
| M2 | ★: the suffix minimum capped by the first room as well | P1 187, P2 348, P6 187 |
| M3 | ★: a box placed only in a room strictly higher than it | P1 1149, P6 1149 |
| M4 | multiset: the usable height the suffix minimum alone | P1 836, P2 1298, P6 836 |
| M5 | multiset: the rooms taken lowest first | P1 1090, P6 1090 |
| M6 | multiset: a box height with more than one box never counted down | P1 278, P6 278 |
| M7 | search: the k smallest boxes matched to the rooms highest first | P1 795, P6 795 |
| M8 | search: the upper bound one short, so all the boxes never fit | P1 1676, P5 637, P6 1676 |
| M9 | template: a box pushed in from the right only below the room | P1 433, P2 693, P6 433 |
| M10 | template: the walk stops while one room is still free | P1 1039, P6 1039 |

## Benchmarks

The bench draws 40 problems first, each of 100000 boxes with heights to
`10^9` and a warehouse of 100000 rooms shaped as a valley (the height
falls by 20000 a room towards the middle, plus noise below `10^6`), then
solves each by the ★ arm, in all five languages. Every implementation
prints `40 problems of 100000 boxes and rooms: boxes placed 3999907,
checksum 403865544`. The C mirror mallocs the three copies the Kāra arm
makes on each call.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.266 s |
| Rust (`rustc -O`) | 0.270 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.299 s |
| Kāra (`karac build`) | 0.299 s |
| Go | 0.686 s |
| C (`clang -O3`, `qsort`) | 0.841 s |
| Python | 6.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.262 s and 0.295 s on one run).

Kāra is 1.12x Rust under overflow checks by median. The time is the two
sorts of 100000 values each problem; C's `qsort` calls its comparator
through a pointer for every comparison, which is why it is last of the
compiled lanes.

## Verification

All four arms print the same output as `warehouse.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`76e5a13ad`.

## Writing it

The ★, multiset and search arms were written in Kāra and checked as
written.

The Rust template took two rounds of `karac fix`:

1. twenty-one edits: the `mut boxes: Vec<i32>` parameter to
   `boxes: own Vec[i32]` with a `let mut boxes = boxes;` rebinding, the
   other `Vec<..>` types to `Vec[..]`, `let (mut l, mut r)` to
   `let mut (l, r)`, the `&b` and `|&x|` patterns to plain names, and
   `Solution::` to `Solution.`;
2. `sort_unstable_by` to `sort_by`, and the wrapper's `as i64` dropped.

It then checks and agrees with no hand edit.
