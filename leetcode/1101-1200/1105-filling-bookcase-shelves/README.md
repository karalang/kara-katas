# 1105. Filling Bookcase Shelves

You are given an array `books` where `books[i] = [thickness_i,
height_i]` indicates the thickness and height of the `i`th book. You
are also given an integer `shelfWidth`.

We want to place these books in order onto bookcase shelves that have a
total width `shelfWidth`. We choose some of the books to place on this
shelf such that the sum of their thickness is less than or equal to
`shelfWidth`, then build another level of the shelf of the bookcase so
that the total height of the bookcase has increased by the maximum
height of the books we just put down. We repeat this process until
there are no more books to place.

At each step the order of the books we place is the order given: with
5 books, we might place the first and second on the first shelf, the
third on the second shelf, and the fourth and fifth on the last.

Return the minimum possible height that the total bookshelf can be
after placing shelves in this manner.

```
books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]], shelfWidth = 4  ->  6
books = [[1,3],[2,4],[3,2]],                         shelfWidth = 6  ->  4
```

**Constraints:** `1 <= books.length <= 1000`; `1 <= thickness_i <=
shelfWidth <= 1000`; `1 <= height_i <= 1000`.

The arms are `fn min_height_shelves(books: Vec[Vec[i64]], shelf_width:
i64) -> i64`. Every book fits a shelf alone, so there is always a way
to place them, and a shelf holds at most `shelfWidth` books.

## Approaches

| file | mechanism |
|---|---|
| `min_height_shelves.kara` ★ | dynamic programming over the books in order: the least height for the first `i` books is, over every run of books ending at book `i` that fits one shelf, the least height for the books before the run plus the run's tallest, the run grown leftward while it fits. O(n * width) |
| `min_height_shelves_memo.kara` | top-down: the least height for the books from `i` on, over every run starting at book `i`, by recursion, each answer kept in a `Vec[Option[i64]]` the first time it is found |
| `min_height_shelves_heap.kara` | a shortest path: the places between books are nodes, a shelf of books `i` to `j - 1` an edge from `i` to `j` weighing their tallest, and Dijkstra's search over a `PriorityQueue` of `(height, place)` finds the least height to the last place |
| `min_height_shelves_back.kara` | from the back: the least height for the books from `i` to the end, filled from the last book backward, each a `fold` over the runs that fit, cut short by `take_while` on a running width the closure updates |
| `min_height_shelves_rows.kara` | the books one at a time into states: a `Map[i64, (i64, i64)]` from the width taken on the open shelf to the height of the shelves above it and the open shelf's tallest; a book opens a new shelf under the best state, or joins the open shelf of every state it fits. The width names the run of books on the open shelf, so no two states share one |
| `min_height_shelves_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `books: Vec<Vec<i32>>`, `dp = vec![i32::MAX; n + 1]`, `for j in (1..=i).rev()` with a `break`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the answers for LeetCode's two
examples and eight more (one book on a shelf as thin, one as wide as
the shelf, two that cannot share a shelf and two that can, a tall book
between two short ones either way, two tall books at the ends, a tall
book in the middle of a narrow case, two books of 1000 on a shelf of
1000), then over 2000 random bookcases of up to 40 books the sum of the
answers (`heights total 331600, checksum 910145622`), and three of
LeetCode's largest: 1000 books at random on a shelf 1000 wide, and 1000
thin books on a shelf 1000 wide and 7 wide. `min_height_shelves.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to cut the row of books into shelves, a cut or
none after each book but the last, and of the ways whose every shelf
fits, the least sum of the shelves' tallest books. Trying every way
needs short rows, so no row has more than 12 books. It checks 2000
problems in four kinds of 500: 1 to 10 books on a shelf 1 to 10 wide,
heights to 10; 1 to 12 books 1 to 3 thick on a shelf 3 to 6 wide,
heights to 3, so that many ways tie; 1 to 8 books on a shelf that holds
them all or nearly; and 2 to 10 books with one as wide as the shelf
among them. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | at least the tallest book, no more than the shelves filled one after another as far as each goes, and the tallest book when all fit one shelf |
| P3 | the row reversed gives the same answer |
| P4 | every height tripled triples the answer; every thickness and the shelf doubled leave it |
| P5 | a shelf one wider never gives more, nor the row without its last book |
| P6 | the row cut in two never does better than the whole, and a book as wide as the shelf put at the cut adds just its own height to the two |

All 72,000 checks pass on every arm: `2000 problems: checksum
184019679, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, trying every way to cut the row, gives the same
checksum.

P1 tries every way and P2 bounds the answer by the tallest book and one
way to place them; P3 to P6 compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a shelf never filled to its width | stops: integer overflow |
| M2 | ★: the longest run taken, not the best | P1 269, P2 238, P3 495, P5 65, P6 58 |
| M3 | ★: the heights counted as the width | P1 1285, P2 965, P3 1069, P4 1519, P6 514 |
| M4 | memo: the last book never shelved | P1 1553, P2 360, P3 1393, P6 1133 |
| M5 | memo: every book of a run as thick as its first | P1 1198, P2 171, P3 1281, P6 1032 |
| M6 | heap: a place keyed by the height before its shelf | P1 2000, P2 2000, P6 2000 |
| M7 | heap: the greatest height taken first | P1 286, P3 495, P5 45, P6 56 |
| M8 | heap: a shelf one wider | P1 915, P4 915, P6 400 |
| M9 | back: the tallest forgotten after each book | P1 1121, P2 307, P3 1223, P5 355 |
| M10 | back: the run's first book taken for its tallest | P1 1149, P2 327, P3 1223 |
| M11 | rows: a shelf never filled to its width | P1 849, P2 778 |
| M12 | rows: no new shelf ever opened | stops: called unwrap() on None |
| M13 | rows: a new shelf opened under the worst state | P1 969, P2 949, P3 999, P6 645 |
| M14 | solution: the run grown from the first book | P1 1763, P2 1270, P3 1583, P6 2000 |
| M15 | solution: the empty bookcase one high | P1 2000, P2 1714, P4 2000, P6 1464 |

Of the thirteen that run to the end, P1 catches all thirteen, P2
eleven, P6 ten, P3 nine, and P4 and P5 three each. P2 misses the two
heap edits whose answer is still the height of a real way to place the
books, never above the greedy one here: M7, whose search takes the
greatest height first and stops at the first way to reach the end, and
M8, which answers for a shelf one wider. P4 sees M3, M8 and M15, the
edits that treat heights and widths unalike or add a height of their
own, and P5 the three that can answer more for more room or more books
(M2, M7, M9). P3 to P6, which compare the arm only with itself, catch
all but M11: an arm that never fills a shelf to its width answers for a
shelf one narrower, itself a bookcase, so every relation between
bookcases still holds. The two that stop: M1 leaves a book as wide as
the shelf with no way to be placed, and adding a height to the
`i64.MAX` that stands for no way overflows, which Kāra checks; M12,
never opening a shelf, runs out of states at the first book that does
not fit, and `unwrap` finds no least.

One rewrite came of the mutations. The rows arm first kept a list of
states for each width and dropped those another beat, and an edit
keeping only the lowest state for each width changed nothing: the width
taken on the open shelf names the run of books on it, so no two states
ever share a width. The arm now keeps one state for each width, and its
five edits were run again.

Of the fifteen not kept, twelve fail as a kept edit: a shelf never
filled to its width stops as M1 in the memo, back and solution arms,
as do the ★ arm leaving out the first book, the heap arm with no shelf
starting at its own book and the solution arm cutting one book late;
the run's first book taken for its tallest in the ★ and memo arms fails
as M10; the run's last book taken in the heap, rows and solution arms as
M9; and the back arm's least started at 0 as M6. The other three fail
alike in a way of their own but were not needed: the memo and back
arms leaving out the first book, and the rows arm forgetting its
height.

## Verification

Every arm prints the same output as `min_height_shelves.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. The ★ arm was written as Kāra, and the
other five as Rust writes them; `karac fix` carried every Rust spelling
to a clean check, in two to four rounds each:

- The memo arm: `&Vec<Vec<i64>>` to a borrowed `Vec[Vec[i64]]`, `i:
  usize` to `i: i64`, `&mut Vec<Option<i64>>` to `mut ref
  Vec[Option[i64]]` and the call's `memo` to `mut memo`, `vec![None;
  n]` to `Vec.filled(n, None)`, and `let (mut used, mut tallest)` to
  `let mut (used, tallest)`.
- The heap arm: both `use` lines dropped, `BinaryHeap::new()` to
  `PriorityQueue.new()`, which takes the least first, and with it every
  `Reverse(..)` around a pushed or popped pair, and `0i64, 0usize` to
  `0, 0`.
- The back arm: `vec![0i64; n + 1]` to `Vec.filled(n + 1, 0)`, `|&j|`
  to `|j|` and `i64::MAX` to `i64.MAX`.
- The rows arm: `HashMap` to `Map` and its `use` dropped, and every
  `&(above, top)` and `&w` pattern to the plain one.
- The Rust solution: `struct Solution {}` declared, `vec![i32::MAX; n +
  1]` to `Vec.filled(n + 1, i32.MAX)`, `let (mut w, mut h) = (0, 0)`
  to `let mut (w, h) = (0, 0i32)`, and `Solution::` to `Solution.`.

## Benchmarks

The bench builds 32 bookcases of 1000 books once, LeetCode's most, 1 to
50 thick and up to 1000 tall, on a shelf 1000 wide. Each of 200 rounds
changes one book in every bookcase and solves it with the ★ arm: 6400
calls, each trying about 40 runs a book. Every implementation prints
`200 rounds over 32 bookcases of 1000 books: heights total 162034620,
checksum 339335952`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.363 to 0.445 s | 0.395 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.404 to 0.500 s | 0.426 s |
| Kāra (`karac build`) | 0.403 to 0.551 s | 0.432 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.412 to 0.529 s | 0.435 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.404 to 0.475 s | 0.438 s |
| C (`clang -O3`) | 0.543 to 0.644 s | 0.565 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.603 to 0.646 s | 0.619 s |
| Go | 1.008 to 1.086 s | 1.028 s |
| Python | 59.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust is the fastest; Kāra ties overflow-checked Rust at about
1.1x plain Rust. C takes about 1.3x Kāra's time: its loop updates the
tallest book and the best height with `if`, where the Rust mirror writes
`max` and `min`, so the difference is likely branches against
conditional moves (inferred, not measured). Go takes about 2.4x Kāra's
time and Python about 135x.
