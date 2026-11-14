# 1564. Put Boxes Into the Warehouse I

You are given two arrays of positive integers, `boxes` and `warehouse`,
the heights of some boxes of unit width and the heights of `n` rooms in a
warehouse, labelled `0` to `n - 1` from left to right. Boxes are put into
the warehouse by these rules: boxes cannot be stacked; you can rearrange
the order in which the boxes are inserted; boxes can only be pushed into
the warehouse from left to right; and if the height of some room is less
than the height of a box, that box and all other boxes behind it are
stopped before that room. Return the maximum number of boxes you can put
into the warehouse.

```
boxes = [4,3,4,1], warehouse = [5,3,3,4,1]     ->  3
boxes = [1,2,2,3,4], warehouse = [3,4,1,2]     ->  3
boxes = [1,2,3], warehouse = [1,2,3,4]         ->  1
```

**Constraints:** `1 <= boxes.length, warehouse.length <= 10^5`;
`1 <= boxes[i], warehouse[i] <= 10^9`.

## Approaches

A box reaches a room only if it fits every room before it, so a room's
usable height is the least height up to it, and the usable heights never
grow going in.

| file | mechanism |
|---|---|
| `warehouse.kara` ★ | the usable heights taken in place, the boxes sorted ascending, and the rooms walked from the back: the smallest box left takes a room when it fits. O(n log n + m) |
| `warehouse_front.kara` | from the door: the boxes sorted tallest first by `sort_by` with a reversed `cmp`, the rooms walked from the front; a box too tall for the room in front of it is too tall for every room after, so it is passed over. O(n log n + m) |
| `warehouse_search.kara` | a binary search on the count: if `k` boxes fit, the `k` smallest do, and they fit when, put in the first `k` rooms tallest first, each fits its room's usable height; `partition_point` over the counts finds how many pass. O(n log n + m + min(n, m) log min(n, m)) |
| `warehouse_solution.kara` | LeetCode's Rust template (`max_boxes_in_warehouse(mut boxes: Vec<i32>, mut warehouse: Vec<i32>) -> i32`, the ★ arm with the usable heights written into the `mut` parameter and two indices), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples, then a box
too tall for the one room, one just fitting, three boxes for one room,
three boxes behind a room of 1, and three behind a room of 1 at the back;
then the total and a checksum of the answers for 3000 random problems of
up to 6 boxes and rooms of up to 10, 300 of up to 1000 and up to 1000,
and 30 of up to 100000 and up to 10^9, the rooms drawn from the upper
half of the heights so they narrow slowly. `warehouse.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every order of every choice of boxes pushed in from the left
one at a time, a box entering when the first room is free and tall enough
and rolling on while the next room is free and tall enough; an order
counts when every box in it goes in, and the answer is the longest. (A
box rolling as far as it can leaves the most room behind it, so letting
it stop sooner adds nothing.) It checks 3000 problems of 1 to 5 boxes and
1 to 5 rooms, heights 1 to at most 9, every random choice drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is from 0 to the fewer of boxes and rooms |
| P3 | the boxes in reverse order leave the answer |
| P4 | every room cut to the least height up to it leaves the answer |
| P5 | a box taller than every room leaves the answer, and a box of height 1 adds one unless every room was already full |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 319923216, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M7, the search running over
every count up to the number of boxes, was killed only by an index out of
bounds in `fits`, and was replaced by one that answers wrong.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rooms' own heights, not the usable ones | P1 765, P4 765, P5 434, P6 765 |
| M2 | ★: the rooms walked from the door | P1 394, P5 428, P6 394 |
| M3 | ★: a box as tall as its room refused | P1 1222, P5 1111, P6 1222 |
| M4 | front: the boxes smallest first | P1 650, P4 361, P5 1003, P6 650 |
| M5 | front: a placed box used again | P1 1144, P2 656, P5 751, P6 1144 |
| M6 | search: the boxes put smallest first by the door | P1 394, P5 428, P6 394 |
| M7 | search: the largest count never tried | P1 1405, P5 1863, P6 1405 |
| M8 | template: the usable height the most up to a room | P1 942, P4 644, P5 425, P6 942 |
| M9 | template: a box that does not fit dropped | P1 533, P5 289, P6 533 |
| M10 | template: the first room never used | P1 1480, P5 1345, P6 1480 |

## Benchmarks

The bench draws 20 problems of 100000 boxes of 1 to 10^9 and 100000
rooms in the upper half of that once, and asks each 10 times by the ★
arm, in all five languages. Every call copies the rooms and the boxes and
sorts the boxes' copy: Kāra with its `sort`, Rust with `sort`, Go with
`slices.Sort` and C with `qsort`. Every implementation prints `10 passes
over 20 problems of 100000 boxes and rooms: 10736460 boxes, checksum
948968598`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.422 s |
| Kāra (`karac build`) | 0.429 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.627 s |
| Rust (`rustc -O`) | 0.635 s |
| Go | 1.887 s |
| C (`clang -O3`) | 2.809 s |
| Python | 7.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.38 s and 0.40 s on one run).

Kāra is 0.67x Rust under overflow checks by median, and as in kata 1561
the sort is the difference: Kāra's `sort` on a `Vec[i64]` is the
runtime's `karac_vec_sort_i64_8`, Rust's `sort_unstable`, where the Rust
mirror's `sort` is the stable one; C pays a call through `qsort`'s
comparison function for every comparison. Not traced further.

## Verification

All four arms print the same output as `warehouse.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, front and search arms were written in Kāra and checked as written.
The bench reads each problem as `let (boxes, warehouse) = ref
problems[p];`, the form `karac fix` gave kata 1560's bench.

The Rust template took 5 changed lines and 2 added, then 1 added, then 2
changed, over three rounds of `karac fix`: Rust's two `mut` parameters to
`own Vec[i32]` with a `let mut` for each added at the body's start, the
`Vec<..>` types to `Vec[..]`, `&&` to `and`, the wrapper's `|&b|` and
`|&w|` to `|b|` and `|w|`, and `Solution::` to `Solution.`; then
`struct Solution {}` added; then `sort_unstable` to `sort` and the
wrapper's closing `as i64` dropped. It checks and agrees with no hand
edit.
