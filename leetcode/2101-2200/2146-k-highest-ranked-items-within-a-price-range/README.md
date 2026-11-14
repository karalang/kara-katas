# 2146. K Highest Ranked Items Within a Price Range

You are given a **0-indexed** 2D integer array `grid` of size `m x n`
that represents a map of the items in a shop. The integers in the grid
represent the following:

- `0` represents a wall that you cannot pass through.
- `1` represents an empty cell that you can freely move to and from.
- All other positive integers represent the price of an item in that
  cell. You may also freely move to and from these item cells.

It takes `1` step to travel between adjacent grid cells.

You are also given integer arrays `pricing` and `start` where
`pricing = [low, high]` and `start = [row, col]` indicates that you
start at the position `(row, col)` and are interested only in items
with a price in the range of `[low, high]` (**inclusive**). You are
further given an integer `k`.

You are interested in the **positions** of the `k` **highest-ranked**
items whose prices are **within** the given price range. The rank is
determined by the **first** of these criteria that is different:

1. Distance, defined as the length of the shortest path from the
   `start` (**shorter** distance has a higher rank).
2. Price (**lower** price has a higher rank, but it must be **in the
   price range**).
3. The row number (**smaller** row number has a higher rank).
4. The column number (**smaller** column number has a higher rank).

Return *the* `k` *highest-ranked items within the price range* ***sorted***
*by their rank (highest to lowest)*. If there are fewer than `k`
reachable items within the price range, return ***all*** of them.

```
grid = [[1,2,0,1],[1,3,0,1],[0,2,5,1]], pricing = [2,5], start = [0,0], k = 3  ->  [[0,1],[1,1],[2,1]]
grid = [[1,2,0,1],[1,3,3,1],[0,2,5,1]], pricing = [2,3], start = [2,3], k = 2  ->  [[2,1],[1,2]]
grid = [[1,1,1],[0,0,1],[2,3,4]], pricing = [2,3], start = [0,0], k = 3        ->  [[2,1],[2,0]]
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 10^5`; `1 <= m * n <= 10^5`; `0 <= grid[i][j] <= 10^5`;
`pricing.length == 2`; `1 <= low <= high <= 10^5`; `start.length == 2`;
`0 <= row <= m - 1`; `0 <= col <= n - 1`; `grid[row][col] > 0`;
`1 <= k <= m * n`.

A breadth-first search from the start gives every reachable cell its
distance, the first rank; each item in range is then the tuple
(distance, price, row, column), which is its rank spelled out, and the
first k of the tuples in order are the answer. O(m n log(m n)).

Every range drawn here starts at 2 or more. The constraints allow a
range from 1, which would take in the empty cells, of value 1, that the
statement does not call items; every arm reads a cell's value as its
price, so such a range would count them, and the statement does not
settle which is meant.

## Approaches

| file | mechanism |
|---|---|
| `ranked.kara` ★ | a breadth-first search over a `VecDeque` of (row, column, distance), the items kept as rank tuples and ranked by one `sort` |
| `ranked_levels.kara` | level by level, a `Vec` of the cells at one distance making the next; a level's items share the first rank, so each level is sorted by (price, row, column) alone, and the search stops once k are in hand |
| `ranked_heap.kara` | no search order and no sort: every reached cell goes into a `PriorityQueue.new()`, smallest first, as its rank tuple; a step costs one, so a distance is settled when the cell is first reached, and the cells come off in rank order |
| `ranked_struct.kara` | a `struct Shop` asked whether a cell is `open` and holds an item `for_sale` (`ref self`), and for its `distances`, a search over a `Vec` read from a moving head; the items gathered row by row and ranked by `sort_by`, the four ranks chained with `then` |
| `ranked_flat.kara` | the grid laid out in one `Vec` by `flat_map`, a cell named by `r * n + c`; the items gathered in index order, which is row and then column order, and ranked by a stable `sort_by_key` on (distance, price) |
| `ranked_solution.kara` | LeetCode's Rust template: `use std::collections::VecDeque`, `usize` cells and `as i32` casts, the directions as `[(i32, i32); 4]`, `vec![vec![false; n]; m]`, the rank tuples by `sort_unstable` and `truncate`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (the start an item in range itself, fewer items than k behind a
wall, and four items at one distance and one price, ranked by row and
column), each with its items; then the count and a checksum over 2000
random grids of up to 6 by 6, a wall one cell in 4, prices of 1 to 5 or
1 to 100000 in turn, with a random range from 2 up, start and k; then
the constraints' largest, 316 by 316 cells: every price from 1 up, the
odd rows broken by walls, every item ranked from the middle and the ten
cheapest from a corner. `ranked.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 48, 10 and 5 edits: Rust's spellings (the `use` dropped,
`<..>` to `[..]`, `[(i32, i32); 4]` to `Array[(i32, i32), 4]`, `&&` and
`||` to `and` and `or`, the `&(dr, dc)` and `&v` patterns to bare ones,
`VecDeque::new` to `VecDeque.new`, `struct Solution;` to `struct
Solution {}`, the adapter's `&Vec` to `ref Vec`, `Solution::` to `.`);
then each `as usize` to `as i64`, since Kāra's indices are `i64`, the
inner `vec![false; n]` to `Vec.filled(n, false)`, `sort_unstable` to
`sort`, and `vec![r as i32, c as i32]` to the list literal; then the
outer `vec![..; m]` to `Vec.filled(m, ..)`, `truncate(k as i64)` to
`truncate(k)`, since an `i32` widens, and the `ref` dropped from the
adapter's parameters, which borrow already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the distance of every cell is settled by sweeping the grid,
each open cell taking one more than its nearest neighbour, until a sweep
changes nothing; then every reachable item in range is given its rank
by counting the items that beat it on distance, price, row and column,
in that order, and those ranked below k are listed in rank order; no
queue is kept and nothing is sorted. It checks 300 random grids of up to
5 by 5, a wall one cell in 4, prices of 1 to 5; then 30 with prices of
1 to 2, full of ties; then 30 of up to 7 by 7 with prices of 1 to 100;
every range from 2 up. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the items are the statement read literally |
| P2 | every price outside the range made an empty cell: the same items |
| P3 | k raised to every cell: the items for k are its first k |
| P4 | every price and the range doubled: the same items |
| P5 | the grid walled round, the start moved in by one: every item moved in by one |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 grids: checksum 925419489, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal items was checked against a Python breadth-first search
and sort of the same grids. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Twenty-nine edits to the differential, four to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the price ranked before the distance | P1 106, P6 106 |
| M3 | ★: the top of the range left out | P1 199, P6 199 |
| M5 | ★: the column ranked before the row | P1 245, P6 245 |
| M6 | levels: every level's items kept whole | P1 17, P3 17, P6 17 |
| M9 | levels: the search stopped one level early | P1 85, P3 77, P6 85 |
| M10 | levels: the row put first in a level's tuples, so the price is read back as the row | P1 271, P4 281, P5 281, P6 271 |
| M11 | heap: the heap popping the largest | P1 118, P2 40, P6 118 |
| M12 | heap: every step costing nothing | P1 80, P2 28, P6 80 |
| M13 | heap: one item too many | P1 63, P3 63, P6 63 |
| M16 | struct: the price rank turned round | P1 69, P6 69 |
| M18 | struct: the last row closed | P1 140, P5 140, P6 140 |
| M20 | struct: one item short | P1 101, P3 93, P6 101 |
| M21 | flat: the row above never tried | P1 111, P6 111 |
| M22 | flat: the price rank dropped | P1 49, P6 49 |
| M23 | flat: the column a row on | P1 30, P5 30, P6 30 |
| M26 | solution: the template sorted largest first | P1 197, P6 197 |
| M29 | solution: the template's distance not added | P1 148, P6 148 |

P1 and P6 kill all seventeen, P3 four, P5 three, P2 two and P4 one. The
answer is a list in rank order, so nearly any wrong edit shows at once
against the literal reading and the other arms; the other properties
see the edits that tie the answer to something a right answer ignores.
P3 asks that the items for k be the first k of the whole ranking; it
sees an edit that stops at the wrong count (M6, M9, M13, M20). P5 walls
the grid round, which moves every item in by one; it sees an edit that
reads the grid's edge where the wall now is (M18, M23), and the levels
arm's tuples reordered (M10), which print a price as a row, and the
walls move the rows but not the prices. P4 doubles every price and the
range; it sees that same edit (M10), since doubling moves the prices but
not the rows. P2 makes every out-of-range price an empty cell; it sees
the heap edits that let such a cell change the order they pop in (M11,
M12).

Of the twenty-nine, twelve were not kept. One is equivalent: the struct
arm's distance grown by one or two by the parity of the cell, which
keeps every distance in the same order. Two fail by a crash or never
finish: the ★ arm marking a cell seen only when it is taken from the
queue, which lets a cell in once for every way to it, so the queue
outgrows memory; and the adapter's start given column first, which
reads outside the grid. One fails as a kept one does: the flat index
read as column first, as M5. Eight are killed with checks of their own
but were left out because their arms keep their share: the ★ arm's
queue taken from the back (P1 34, P6 34), a level's items unsorted (P1
73, P6 73), the walls walked through (P1 60, P6 60), the heap's start
priced 0 (P1 125, P6 125) and its range's bottom left out (P1 188, P6
188), the struct's rows not tried (P1 30, P6 30), the flat start not
counted as reached (P1 98, P6 98), and the template's range read from
its top (P1 171, P6 171).

## Verification

Every arm prints the same output as `ranked.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 s to 6.7 s and the
differential 1.6 s.

## Benchmarks

The bench builds 4 grids of 316 by 316 cells once, a wall one cell in 5
and prices of 2 to 100000 elsewhere; then searches every grid 25 times
for the 1000 highest ranked items priced 2 to 50000, one cell redrawn
and the start moved before each search so that no search repeats one
before, with the ★ arm in all five languages. Every implementation
prints `100 searches: 100000 items in all, checksum 727609236`.

BENCHTAB
