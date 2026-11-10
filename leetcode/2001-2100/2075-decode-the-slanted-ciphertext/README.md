# 2075. Decode the Slanted Ciphertext

A string `originalText` is encoded using a slanted transposition cipher
to a string `encodedText` with the help of a matrix having a fixed
number of rows `rows`.

`originalText` is placed first in a top-left to bottom-right manner: the
blue cells are filled first, then the red cells, then the yellow cells,
and so on, until the end of `originalText` is reached. The arrow
indicates the order in which the cells are filled. All empty cells are
filled with `' '`. The number of columns is chosen such that the
rightmost column will not be empty after filling in `originalText`.

`encodedText` is then formed by appending all characters of the matrix
in a row-wise fashion.

Given the encoded string `encodedText` and number of rows `rows`, return
the original string `originalText`.

**Note:** `originalText` does not have any trailing spaces `' '`. The
test cases are generated such that there is only one possible
`originalText`.

```
encodedText = "ch   ie   pr", rows = 3              ->  "cipher"
encodedText = "iveo    eed   l te   olc", rows = 4  ->  "i love leetcode"
encodedText = "coding", rows = 1                    ->  "coding"
```

**Constraints:** `0 <= encodedText.length <= 10^6`; `encodedText`
consists of lowercase English letters and `' '` only; `encodedText` is a
valid encoding of some `originalText` that does not have trailing
spaces; `1 <= rows <= 1000`; the test cases are generated such that
there is only one possible `originalText`.

The grid has `cols = len / rows` columns, and the text was written down
its diagonals, one from each column of the top row, left to right. So
the decoding reads each diagonal from `(0, c)` down to the last row or
the last column, whichever comes first, and drops the trailing spaces,
which were the blank cells: O(len). The approaches differ in how they
hold the grid and walk a diagonal.

## Approaches

| file | mechanism |
|---|---|
| `slanted.kara` ★ | the text's `bytes()` read in place: from each column `c`, row `r` down the diagonal at `r * cols + c + r` while `r < rows` and `c + r < cols`, pushed onto a `String`, `trim_end()`ed. O(len) |
| `slanted_grid.kara` | the grid built first, the text's chars cut into rows with `chunks(cols)`, each a `Vec[char]`, and each diagonal walked by row and column; the trailing spaces popped while the answer `ends_with(" ")` |
| `slanted_iter.kara` | one iterator chain: each column `flat_map`ped to the places down its diagonal, `take_while` they stay left of the last column, mapped to their bytes and `collect`ed into a `String` |
| `slanted_step.kara` | a diagonal is every `cols + 1`-th character from its start: `(c..len).step_by(cols + 1).take(rows.min(cols - c))`, the bytes gathered in a `Vec[u8]`, trailing spaces popped, made a `String` by `String.from_utf8` |
| `slanted_struct.kara` | a `struct Grid` of the bytes and the shape, with `at(r, c)` giving `None` off the grid and `diagonal(c)` reading down with `while let Some(b) = self.at(r, c + r)` |
| `slanted_solution.kara` | LeetCode's Rust template (`rows as usize`, `as_bytes()`, `String::with_capacity`, `let (mut i, mut j)`, `&&`, `trim_end().to_string()`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each text and its answer; then the length and a checksum of the
answers for 400 random grids of 1 to 8 rows and 0 to 30 columns, of
letters and spaces in three mixes; then the length and checksum of the
answer for the constraints' largest, 1000 rows of 1000. `slanted.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every cell of the grid given its diagonal, its column less its
row, and its place down it, its row; the cells on a diagonal that starts
in the top row sorted by diagonal and then by place, read out, and the
trailing spaces dropped. It checks 300 random grids of 1 to 6 rows and 0
to 12 columns of letters and spaces; then 20 with more rows than
columns, and 20 all spaces but for one letter. All 340 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer written down the diagonals of a blank grid of the same shape agrees with the text at every cell it writes |
| P3 | the text read as one row is the text with its trailing spaces dropped |
| P4 | the answer ends in no space, is no longer than the diagonals, and holds no letter more often than the text |
| P5 | the cells below the first diagonal changed leave the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 grids: checksum 726462678, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
grids. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last column's diagonal never read | P1 161, P3 152, P6 161 |
| M2 | ★: the leading spaces trimmed too | P1 112, P2 112, P3 127, P6 112 |
| M3 | ★: the spaces dropped, not only the trailing ones | P1 239, P2 239, P3 267, P6 239 |
| M4 | grid: the column not moved on down a diagonal | P1 249, P2 249, P4 216, P5 271, P6 249 |
| M5 | grid: one trailing space dropped at most | P1 87, P3 100, P4 87, P6 87 |
| M6 | grid: each diagonal from the second row | P1 281, P2 202, P3 296, P6 281 |
| M7 | iter: the columns read, not the diagonals | P1 216, P2 206, P5 246, P6 216 |
| M8 | iter: the trailing spaces kept | P1 150, P3 159, P4 150, P6 150 |
| M9 | iter: the diagonals right to left | P1 262, P2 262, P3 290, P6 262 |
| M10 | step: each diagonal as long as the rows | P1 168, P2 168, P4 162, P5 220, P6 168 |
| M11 | step: the first diagonal never read | P1 281, P2 246, P3 296, P6 281 |
| M12 | step: every diagonal a cell short | P1 240, P2 118, P3 152, P6 240 |
| M13 | struct: the last row off the grid | P1 220, P2 173, P3 296, P6 220 |
| M14 | struct: every other row of a diagonal | P1 229, P2 206, P6 229 |
| M15 | struct: the leading spaces trimmed, not the trailing | P1 166, P2 112, P3 188, P4 120, P6 166 |
| M16 | solution: the adapter's rows one more | P1 277, P2 214, P3 290, P5 206, P6 277 |
| M17 | solution: the adapter's text trimmed first | P1 122, P2 85, P5 123, P6 122 |

P1 and P6 kill all seventeen, P2 fourteen, P3 twelve, and P4 and P5
five each. P3, which hands each arm the text as a grid of one row, sees
an edit to the trimming or to where a diagonal starts or stops short
(M1, M6, M11, M12), but not one that reads too far down a diagonal or
down a column (M4, M7, M10, M14). P2, which writes the answer back down
the diagonals, sees a character taken from the wrong cell or a space
lost from the middle. P4 sees an answer longer than the diagonals hold
(M4, M10), trailing spaces left (M5, M8) or the leading ones trimmed in
their place (M15); P5, which changes the cells no diagonal reaches, an
arm that reads them: the columns (M7), diagonals run past the last
column (M4, M10), or a grid of the wrong shape (M16) or text (M17).

Of the thirty-one, fourteen were not kept. One survives, and it is
equivalent: the grid arm's grid of no columns answered with its text,
which the constraints make empty, since the text fills the grid. The
other thirteen fail as a kept one: the ★, iter and Rust arms' every
diagonal a cell short as M12; the ★, step and Rust arms' columns read
as M7; the ★, grid and Rust arms' trailing spaces kept as M8; the struct
arm's columns read as M4; the iter arm's diagonals from the second row
as M6; the step arm's one trailing space dropped as M5; the struct arm's
diagonals right to left as M9.

## Verification

Every arm prints the same output as `slanted.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 2.1 s to 4.9 s, the iter arm the
slowest, and the differential 1.1 s (timed while other work shared the
machine).

No arm met a compiler gap.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 7 and 2 edits: Rust's spellings (`String::` and
`Solution::` to `.`, `let (mut i, mut j)` to `let mut (i, j)`, `&&` to
`and`, `struct Solution;` to `struct Solution {}`); then `rows as usize`
to `as i64`, as a length is, and `as_bytes()` to `bytes()`. The fixed
arm reads as the template does.

## Benchmarks

The bench decodes 40 grids of about `10^6` characters with the ★ arm in
all five languages, 1, 2, 10, 100 and 1000 rows in turn, letters and
spaces six in 32, the grids built first. Every implementation prints
`40 grids: 35964019 characters, checksum 949306173`.

BENCHTAB
