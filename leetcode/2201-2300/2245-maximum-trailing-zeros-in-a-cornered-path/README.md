# 2245. Maximum Trailing Zeros in a Cornered Path

You are given a 2D integer array `grid` of size `m x n`, where each cell
contains a positive integer.

A **cornered path** is defined as a set of adjacent cells with **at
most** one turn. More specifically, the path should exclusively move
either **horizontally** or **vertically** up to the turn (if there is
one), without returning to a previously visited cell. After the turn,
the path will then move exclusively in the **alternate** direction:
move vertically if it moved horizontally, and vice versa, also without
returning to a previously visited cell.

The **product** of a path is defined as the product of all the values
in the path.

Return *the **maximum** number of **trailing zeros** in the product of a
cornered path found in* `grid`.

```
grid = [[23,17,15,3,20],[8,1,20,27,11],[9,4,6,2,21],[40,9,1,10,6],[22,7,4,5,3]]  ->  3
grid = [[4,3,2],[7,6,1],[8,8,8]]                                                  ->  0
```

**Constraints:** `1 <= m, n <= 10^5`; `1 <= m * n <= 10^5`;
`1 <= grid[i][j] <= 1000`.

A product's trailing zeros are the fewer of its factors of 2 and of 5,
and both only add up along a path, so a longer path is never worse. The
best path therefore runs from its corner to the edge of the grid both
ways: one of the four corners (left or right, joined to up or down) at
some cell, and a straight path is one of those cut short. Prefix sums of
the twos and fives along every row and column answer each corner in
O(1). O(m * n).

## Approaches

| file | mechanism |
|---|---|
| `zeros.kara` ★ | prefix sums of the twos and the fives in four `Vec[Vec[i64]]`s, by row and by column; every cell tried as the corner, its row's part to the left or right (the corner included) with its column's part above or below (the corner left out) |
| `zeros_sweep.kara` | no subtraction: four sweeps, left to right, right to left, top down and bottom up, leaving at each cell the `(twos, fives)` of the run that ends there; a corner adds a row run to a column run and takes the cell off once |
| `zeros_struct.kara` | a `#[derive(Copy, Clone)] struct Factors` with `Factors.of`, `plus`, `minus` and `zeros` (`ref self`), and a `struct Prefix` built by `Prefix.build` whose `row_span` and `col_span` answer any stretch of a row or column |
| `zeros_flat.kara` | the factors of 1 to 1000 in two tables built once (`twos[v] = twos[v / 2] + 1`), and the prefix sums in four flat `Vec[i64]`s indexed `i * (n + 1) + j` and `i * n + j`, since m * n is bounded and m and n alone are not |
| `zeros_iter.kara` | iterator chains: the grid `map`ped to pairs of factors counted by a recursive `factor`, each row's and column's running sums by `scan` behind `once((0, 0))`, and the best corner by `flat_map` over the cells, then `max` |
| `zeros_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, `i32` out, the prefix sums as `[i32; 2]` pairs in `vec![vec![[0i32; 2]; n + 1]; m]`, each corner's sides and ends from `for &(a, b) in &[..]`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four
more (one cell of 10, one row, one column, and a 125 and an 8 joined
only through a turn), each with its answer; then the most zeros over
2000 grids of 1 to 8 rows and columns with values up to 50, with a
checksum of the answers; then the constraints' largest as 250 x 400
cells with values up to 1000; then one row of 10^5 cells. `zeros.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 23 edits: `Vec<..>` to
`Vec[..]`, `vec![vec![[0i32; 2]; n + 1]; m]` to `Vec.filled(m,
Vec.filled(n + 1, [0i32; 2]))`, `[0; 2]` typed `[0i32; 2]` to match the
sums it is added to, `let mut ans = 0` typed `i32`, `for &(h0, h1) in
&[..]` to `for (h0, h1) in [..]`, `struct Solution;` to `struct Solution
{}`, `Solution::` to `Solution.`, the `&` pattern dropped from the
adapter's closure, and the adapter's `as i64` removed as lossless.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path tried, from every cell, in each of the four
directions for any number of steps, then turned either way for any
number more; the path's values multiplied and the product's trailing
zeros counted by dividing by ten; no factor counting. It checks 300
random grids of 1 to 5 rows and columns with values up to 50; then 30
whose values are drawn from 2, 4, 5, 8, 10, 16, 20, 25, 40 and 50, rich
in both factors; then 30 of one row or one column of up to 9 cells. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the best path's trailing zeros, read literally |
| P2 | the grid transposed: the same answer |
| P3 | the grid turned half round: the same answer |
| P4 | the first cell times ten: the same answer or one more |
| P5 | at least the zeros of any one cell, whole row or whole column; at most those of the whole grid |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 716230126, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
every pair of end cells with both corners joining them (row first or
column first), multiplies the cells as big integers and counts the
zeros of the decimal string. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: fives counted as twos | P1 307, P5 293, P6 307 |
| M5 | ★: the down end short of the last row | P1 28, P2 33, P3 49, P6 28 |
| M6 | ★: each factor counted once at most | P1 117, P5 55, P6 117 |
| M7 | sweep: the corner not taken off | P1 193, P4 170, P5 130, P6 193 |
| M8 | sweep: the top end only | P1 36, P2 39, P3 68, P6 36 |
| M10 | sweep: the bottom run fed from the top one | P1 62, P2 89, P3 116, P4 109, P5 31, P6 62 |
| M13 | struct: the right side without the corner | P1 16, P2 20, P3 39, P6 16 |
| M14 | struct: the down end overlapping the corner | P1 162, P2 58, P3 71, P4 182, P5 114, P6 162 |
| M16 | struct: a five counted as a two | P1 265, P5 262, P6 265 |
| M18 | flat: the rows' twos read from the fives table | P1 47, P2 45, P5 19, P6 47 |
| M20 | flat: the right side and the up end only | P1 16, P3 33, P6 16 |
| M21 | flat: the down end short of the last row | P1 7, P2 19, P3 14, P6 7 |
| M23 | iter: the larger of twos and fives | P1 329, P5 316, P6 329 |
| M25 | iter: the left side without the corner | P1 23, P2 20, P3 39, P6 23 |
| M26 | iter: the first row only | P1 65, P2 86, P3 98, P5 20, P6 65 |
| M28 | solution: values capped at 99 | P4 70 |
| M30 | solution: the columns' sums carried from the rows | P1 91, P2 125, P3 4, P5 21, P6 91 |

P1 and P6 kill sixteen, P2, P3 and P5 ten each, and P4 four. P2 and P3
catch the edits that treat one side or one end differently from the
others, since transposing or turning the grid hands that side another
corner's work; P5 the edits that miscount a factor or count the corner
twice; P4 the corner counted twice (M7, M14), the sweep fed from the
wrong run (M10), and M28, which P1 cannot see: the cases' values stay
under 100 and only the first cell times ten reaches the cap.

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Six fail as a kept one does: the ★ and
struct arms' larger of twos and fives (M4, M12) as the iter arm's
(M23); the flat arm's table with no twos (M17) as the struct arm's five
counted as a two (M16); the iter arm's factors counted once at most
(M22) as the ★ arm's (M6); the iter arm's down end overlapping the
corner (M24) as the struct arm's (M14); and the template's right side
without the corner (M29) as the struct arm's (M13). Three fail alike in
a group of their own: the up end reaching the corner in the ★, flat and
template arms (M1, M19, M27); and two as a pair of their own: the left
side only in the ★ arm and the first side only in the struct arm (M3,
M15). Three fail their own way and are left out for the count of
three: the sweep arm's left run without its twos (M9) and fives counted
once at most (M11), and the template's answer begun at one (M31). One
first try was replaced: the template's values cut to their last two
digits turned 100 into 0, whose twos never end, and overflowed.

## Verification

Every arm prints the same output as `zeros.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the flat arm takes 1.8 s, the ★ arm 2.1 s, the
sweep arm 2.9 s, the struct arm 3.2 s, the template 4.7 s, the iter arm
9.1 s, and the differential 2.3 s.

## Benchmarks

The bench answers 40 grids of 250 x 400 cells, values 1 to 1000, with
the ★ arm in all five languages. C keeps the grid and the prefix sums
in fixed arrays; the others allocate a list per row. Every
implementation prints `40 grids of 250 x 400: checksum 400799046`.

BENCHTAB
