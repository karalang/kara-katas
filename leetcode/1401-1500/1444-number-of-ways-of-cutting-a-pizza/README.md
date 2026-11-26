# 1444. Number of Ways of Cutting a Pizza

Given a rectangular pizza represented as a `rows x cols` matrix
containing the following characters: `'A'` (an apple) and `'.'` (empty
cell) and given the integer `k`. You have to cut the pizza into `k`
pieces using `k-1` cuts. For each cut you choose the direction: vertical
or horizontal, then you choose a cut position at the cell boundary and
cut the pizza into two pieces. If you cut the pizza vertically, give the
left part of the pizza to a person. If you cut the pizza horizontally,
give the upper part of the pizza to a person. Give the last piece of
pizza to the last person. Return the number of ways of cutting the pizza
such that each piece contains at least one apple. Since the answer can
be a huge number, return this modulo `10^9 + 7`.

```
pizza = ["A..","AAA","..."], k = 3     ->  3
pizza = ["A..","AA.","..."], k = 3     ->  1
pizza = ["A..","A..","..."], k = 1     ->  1
```

**Constraints:** `1 <= rows, cols <= 50`, `rows == pizza.length`, `cols
== pizza[i].length`, `1 <= k <= 10`, `pizza` consists of characters
`'A'` and `'.'` only.

Each arm is `fn ways(pizza: Vec[String], k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | the apples from each row and column on to the far corner, as suffix sums over the rows' `bytes()`, and for each count of pieces still to give, a table of the ways to cut the part from each row and column on: a cut gives away the part above or left of it when that part holds an apple, and the rest goes on with one piece fewer. O(k · rows · cols · (rows + cols)) |
| `ways_memo.kara` | top down from the whole pizza, each answer kept in a `Map[(i64, i64, i64), i64]` by its pieces, row and column, the map passed down as a `mut ref`, each cell read by `chars().nth(c)`. O(k · rows · cols · (rows + cols)) |
| `ways_sums.kara` | the cuts that give away an apple are those past the first row, or column, with an apple in the part, so each table is a running sum of the last one's ways from that row, or column, to the edge. O(k · rows · cols) |
| `ways_rows.kara` | the apples in each row from each column on, and every cut's part checked row by row with `any`. O(k · rows · cols · (rows + cols) · rows) |
| `ways_solution.kara` | a Rust solution as LeetCode's Rust users write it (`const MOD: i64`, the rows as `Vec<&[u8]>` through `as_bytes()`, `vec![vec![0; n + 1]; m + 1]` for the apples from each cell on and `vec![vec![vec![0i64; n]; m]; k]` for the ways), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and five
more (`3 1 1 1 0 2 1 2`); the constraints' most, 50 by 50 all apples
with k = 10, an apple a tenth of the time with k = 10, and one apple in
the far corner with k = 1 (`50 by 50: 184014604 760830129 1`); and 2000
random pizzas of 1 to 8 by 1 to 8, an apple 0 to 100 times in 100, with
k from 1 to 10 (`2000 random pizzas: 2382380 in all, checksum
932135130`). `ways.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, sums and rows arms check clean as first written.
The memo arm first walked a row's cells from the right by
`pizza[r].chars().enumerate().collect().iter().rev()`, which `karac
check` refuses, the `collect` having no type to make and nothing to
settle one, as Rust's would; the arm reads each cell by `chars().nth(c)`
instead. The Rust solution takes one round of 20 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]` and `Vec<&[u8]>` to `Vec[Slice[u8]]`, `as_bytes()` to
`bytes()`, each `vec![..; ..]` to `Vec.filled(..)`, `k as usize` to `k
as i64`, and `Solution::` to `Solution.`; its `const MOD: i64 =
1_000_000_007;` inside the method is taken as written. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to make the cuts one after another, each horizontal
cut giving away the part above it and each vertical one the part left of
it, every piece checked for an apple cell by cell and the ways counted
one by one, while there are at most 16 cells and 5 pieces. LeetCode's
examples, six edge cases (one cell with an apple and without, more
pieces than a pizza can give, a row and a column of apples cut into
every cell, and apples only in the last cell), the constraints' most
three ways (all apples, an apple a tenth of the time, and one apple in
the far corner), and 1991 random pizzas drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 16 cells and 5 pieces |
| P2 | the pizza turned about its diagonal, rows for columns, gives the same count |
| P3 | one piece gives 1 exactly when there is an apple |
| P4 | an empty row below and an empty column to the right give the same count, while there is room |
| P5 | an empty row above and an empty column to the left give the same count, while there is room |
| P6 | the ★ arm's answer |

All 52,800 checks pass on every arm: `2003 cases: checksum 930622242,
52800 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, top down with
`lru_cache` and each part's apples found by a scan, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a part with no apple taken as one way to finish | P1 110, P3 184, P4 1060, P6 1416 |
| M2 | ★: a horizontal cut allowed to give away no apple | P1 122, P2 775, P5 1164, P6 2340 |
| M3 | memo: a vertical cut allowed to give away no apple | P1 101, P2 775, P5 1185, P6 588 |
| M4 | memo: each answer read back from the memo one more | P1 109, P2 580, P6 945 |
| M5 | sums: the cut at the first apple's row counted, giving that part away empty | P1 400, P6 1653 |
| M6 | sums: the ways across a row not summed to the edge | P1 124, P2 790, P6 714 |
| M7 | rows: a part held to have an apple only when every row has one | P1 196, P2 701, P3 678, P4 753, P5 753, P6 845 |
| M8 | rows: a vertical cut's part checked to the right edge, not to the cut | P1 101, P2 775, P5 1185, P6 588 |
| M9 | solution: one more way for every horizontal cut | P1 304, P2 1542, P4 1651, P6 1445 |
| M10 | solution: the first vertical cut never made | P1 199, P2 640, P5 710, P6 849 |

## Benchmarks

The bench draws 200 pizzas of 50 by 50, each cell an apple 5 to 50 times
in 100, and cuts each for k = 10 with the ★ arm, folding the ways to a
checksum. Each implementation keeps the same suffix sums and makes a
fresh table for each count of pieces, as the ★ arm makes a fresh `Vec`.
Every implementation prints `200 pizzas of 50 by 50: checksum
496779076`.

BENCHTAB

Measured by hand, Kāra takes 0.43 s against Rust's 0.39 s (0.46 to 0.48
s with overflow checks on), C's 0.27 to 0.28 s and Go's 0.66 to 0.69 s;
Python takes 18 s.
