# 2194. Cells in a Range on an Excel Sheet

A cell `(r, c)` of an excel sheet is represented as a string
`"<col><row>"` where:

- `<col>` denotes the column number `c` of the cell. It is represented
  by **alphabetical letters**. For example, the `1st` column is denoted
  by `'A'`, the `2nd` by `'B'`, the `3rd` by `'C'`, and so on.
- `<row>` is the row number `r` of the cell. The `rth` row is
  represented by the **integer** `r`.

You are given a string `s` in the format `"<col1><row1>:<col2><row2>"`,
where `<col1>` represents the column `c1`, `<row1>` represents the row
`r1`, `<col2>` represents the column `c2`, and `<row2>` represents the
row `r2`, such that `r1 <= r2` and `c1 <= c2`.

Return *the **list of cells*** `(x, y)` *such that* `r1 <= x <= r2`
*and* `c1 <= y <= c2`. The cells should be represented as **strings** in
the format mentioned above and be sorted in **non-decreasing** order
first by columns and then by rows.

```
s = "K1:L2"  ->  ["K1", "K2", "L1", "L2"]
s = "A1:F1"  ->  ["A1", "B1", "C1", "D1", "E1", "F1"]
```

**Constraints:** `s.length == 5`; `'A' <= s[0] <= s[3] <= 'Z'`; `'1' <=
s[1] <= s[4] <= '9'`; `s` consists of uppercase English letters, digits
and `':'`.

Two loops, the column outside and the row inside, over the range's own
bytes. O(cells), at most 26 x 9.

## Approaches

| file | mechanism |
|---|---|
| `cells.kara` ★ | the range's four bytes read off, two loops over them, the column outside and the row inside, each cell's two bytes made a `String` by `String.from_utf8` |
| `cells_format.kara` | the range read as `char`s and numbers: the two corners by `split(":")`, the columns an inclusive `char` range over their first `char`s, the rows parsed by `i64.parse` from the text after each letter, each cell written by an `f`-string |
| `cells_iter.kara` | one chain: the columns' bytes `flat_map`ped to the rows' bytes, each pair `map`ped to a `String` by `collect`ing its two `char`s, the whole `collect`ed |
| `cells_struct.kara` | a `struct Cell` of a column letter and a row number written by an `impl Display` (Kāra's `to_string(ref self) -> String`), and a `struct Corners` of two cells, read by `parse` from the range and walked by `cells` (`ref self`) |
| `cells_count.kara` | the cells counted first, columns times rows, and each one made from its index alone by `Vec.from_fn`: the index divided by the rows gives the column, the remainder the row |
| `cells_solution.kara` | LeetCode's Rust template: `-> Vec<String>`, `s.as_bytes()`, inclusive ranges over `u8`s, `Vec::new()`, `format!("{}{}", c as char, r as char)`, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and four more
(one cell, one column, one row, and the whole sheet), each with its
cells; then, over every range there is (each pair of columns A to Z with
each pair of rows 1 to 9, 15795 ranges), the cells' total and a
checksum. `cells.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in three rounds of 6, 1 and 1 edits:
first Rust's spellings (`Vec<..>` to brackets, `Vec::new()` to
`Vec.new()`, `format!("{}{}", c as char, r as char)` to the `f`-string
`f"{c as char}{r as char}"`, `struct Solution;` to `struct Solution
{}`, `Solution::` to `.`); then `s.as_bytes()` to `s.bytes()`; then the
adapter's `.clone()` dropped, which the call only borrows.

Writing the struct arm first as Rust does, `impl fmt::Display for Cell
{ fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f,
"{}{}", self.col, self.row) } }`, `karac fix` mends the `use`, `&self`
and `&mut` and then stops: the `fmt::` paths in the impl's header and
the parameter's type are parse errors with no fix, and `write!` says
only that Kāra has no macros, with nothing on Kāra's `Display`, whose
one method is `to_string(ref self) -> String`. kara B-2026-11-15-36 asks for
the mend.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every cell of the sheet, A1 to Z9, listed column by column,
and kept when its column and its row both lie between the range's. It
checks 300 random ranges; then 30 of one column; then 30 of one row.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the cells are the statement read literally |
| P2 | as many cells as the columns times the rows |
| P3 | the cells rise strictly, and each lies in the range |
| P4 | the first cell is the range's first corner, the last its second |
| P5 | the range less its last column (or, in one column, its last row), then that column (or row): the same cells |
| P6 | each arm agrees with at least three of the other five |

P3 holds since a cell's two characters, a letter and one digit, sort as
text the way the statement orders them, columns first. P5 holds since
the last column's cells come after every other column's, and in one
column the last row's after every other row's.

The differential prints `360 ranges: checksum 382239336, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
ranges. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-nine edits to the differential, six to the ★, format and count
arms and seven to the iter, struct and template arms, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the last column left out | P1 360, P2 360, P4 360, P5 313, P6 360 |
| M4 | ★: the cell written row first | P1 360, P3 360, P4 360, P6 360 |
| M5 | ★: the rows from the range's colon | P1 360, P2 360, P4 360, P6 360 |
| M6 | format: the last row left out | P1 360, P2 360, P4 360, P5 40, P6 360 |
| M7 | format: the columns to the first corner's | P1 313, P2 313, P4 313, P5 313, P6 313 |
| M9 | format: the cells listed backward | P1 353, P3 353, P4 353, P5 353, P6 353 |
| M13 | iter: the columns one past | P1 360, P2 360, P3 360, P4 360, P5 353, P6 360 |
| M15 | iter: the rows from the one before | P1 360, P2 360, P3 360, P4 360, P5 40, P6 360 |
| M32 | iter: row 9 never reached | P1 73, P2 73, P4 73, P6 73 |
| M18 | struct: the corners swapped | P1 353, P2 353, P4 353, P5 100, P6 353 |
| M20 | struct: the cells walked row by row | P1 253, P3 253, P5 253, P6 253 |
| M34 | struct: the first cell twice | P1 360, P2 360, P3 360, P5 353, P6 360 |
| M23 | count: the column from the remainder | P1 353, P3 353, P4 334, P5 353, P6 353 |
| M25 | count: the row from the first byte | P1 331, P3 331, P4 331, P5 353, P6 331 |
| M35 | count: a wide range's last cell dropped | P1 92, P2 92, P4 92, P5 92, P6 92 |
| M26 | solution: the adapter's range reversed | P1 360, P2 353, P3 7, P4 360, P5 100, P6 360 |
| M36 | solution: a single cell listed as none | P1 7, P2 7, P4 7, P5 100, P6 7 |

P1 and P6 kill all seventeen, P4 fifteen, P5 fourteen, P2 twelve and P3
nine. P3 checks that the cells rise and lie in the range, and misses
the eight edits that only leave cells out (M2, M5, M6, M7, M18, M32,
M35, M36). P2 counts, and misses the five that list the right number of
cells: the text written row first (M4), the cells backward (M9) or row
by row (M20), and the count arm's index read wrong (M23, M25). P4 looks
at the two ends, and misses the cells walked row by row (M20), whose
ends are still the corners, and the first cell twice (M34). P5 lists the
range in two parts, and misses the edits that go wrong the same way in
each part: the text written row first (M4), no rows at all (M5), and
row 9 never reached (M32).

Of the thirty-nine, twenty-two were not kept; none is equivalent and
none crashes. Seven fail all alike and are left out to keep three to an
arm: one row only, the rows run to the first corner's or from the
second's (M3, M8, M11, M21 and M27, across five arms), and column Z
never reached (M31, M39). Fifteen fail as a kept one does: the ★ arm's
rows outside the columns (M1) and the count arm's index split by the
columns (M22) as M20; the iter arm's first column skipped (M14) and the
template's columns exclusive (M30) as M2; the iter arm's cell written
row first (M12), the struct arm's row one more (M16) and the template's
column one on (M29) as M4; the format arm's top one row down (M10) as
M6; the struct arm's columns to the first corner's (M19) as M7; the
template's cells listed backward (M28) as M9; the count arm's one cell
more (M24) as M13; the struct arm's first row one less (M17) as M15;
the struct arm's single cell listed as none (M33) as M36; and the format
arm's first cell twice and the ★ arm's last cell twice (M37, M38) as
M34.


## Verification

Every arm prints the same output as `cells.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the template, format, count and ★ arms take
2.7 s to 4.8 s over the 540540 cells, the struct arm 5.5 s, which builds
a `Cell` for each and then its text, and the iter arm 7.5 s. The
differential takes 2.2 s.

## Benchmarks

The bench builds every range there is once, 15795 of them, then lists
each one's cells 20 times over, with the ★ arm in all five languages;
each list is checked by its length and its last cell. Every cell is a
string of its own: C `malloc`s each and frees them after; Rust, Go,
Python and Kāra build a list of strings. Every implementation prints
`20 passes over 15795 ranges: checksum 842920152`.

BENCHTAB
