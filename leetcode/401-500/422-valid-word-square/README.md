# 422. Valid Word Square

Given an array of strings `words`, return `true` if it forms a valid
word square. A sequence of strings forms a valid word square if the
k-th row and the k-th column read the same string, for
`0 <= k < max(numRows, numColumns)`.

```
words = ["abcd","bnrt","crmy","dtye"]  -> true
words = ["abcd","bnrt","crm","dt"]     -> true
words = ["ball","area","read","lady"]  -> false   (row 2 "read", column 2 "lead")
```

**Constraints:** `1 <= words.length <= 500`;
`1 <= words[i].length <= 500`; `words[i]` holds lowercase English
letters.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `valid_word_square.kara` ★ | every cell against its mirror: for each letter at row `i`, column `j`, there must be a row `j`, longer than `i`, with the same letter at `i`. A cell whose mirror is missing fails from its own side, so one pass covers both directions | O(cells) | O(1) |
| `valid_word_square_grid.kara` | a padded grid as wide as the longest word or the number of words, with 0 where no word reaches; the words are a word square exactly when the grid is symmetric | O(side^2) | O(side^2) |
| `valid_word_square_columns.kara` | read column `k` down from the top while the rows reach it, and compare it with row `k`. Nothing else needs checking (see below) | O(rows^2) | O(rows) |
| `valid_word_square_cells.kara` | a `Map` from each cell, `row * 1000 + column`, to its letter; every cell's mirror must be in the map with the same letter | O(cells) | O(cells) |
| `differential.kara` | the four arms on 1,500 random squares, five properties, one of them a brute force over a list of every cell | — | — |

Every arm prints the same 11 lines: the three LeetCode examples, seven
edge cases (one letter, one word longer than the list, two rows of
different lengths, a symmetric pair, two rows whose first is longer
than the list, a column longer than its row, a staircase), and for
2,000 random word squares of 1 to 12 rows, how many are valid and a
checksum. `valid_word_square.py` mirrors the ★ arm and its output is
byte-identical. The random squares start from a symmetric grid of two
letters cut to a symmetric staircase of row lengths, then five in six
get one change: a letter, a row cut short, a row made longer or a row
added. Some changes leave the square valid (a letter on the diagonal,
or a cell at the corner of the staircase), so the count is not simply
the unchanged ones.

The columns arm first also checked that no row further down reached
column `k` again after a row that stopped short, and that no word was
longer than the number of rows. Mutation testing showed the first
check could not fail once every column matches its row, and the
second follows the same way, so both were removed. A row `s` reaching
column `k` past a gap has a letter at column `k`; its own column check
needs row `k` to reach column `s`, but row `k` equals column `k`, which
stopped above `s`. And each word equals a column of at most as many
letters as there are rows.

The cells arm walks its `Map`, whose order is the per-process hash
order; it returns `false` at the first cell without a matching mirror,
and whether one exists does not depend on the order.

## Differential

`differential.kara` holds copies of the four arms. Each of 1,500 random
cases builds a valid word square of 1 to 10 rows over three letters, as
the harness does:

| | property |
|---|---|
| P1 | after one of five changes (a letter, a row cut short, a row made longer, a row added, two rows swapped) or none, the answer is that of a brute force that looks for each cell's mirror by scanning a list of every cell |
| P2 | renaming the letters gives the same answer |
| P3 | the square is valid, and so is its top-left `k` by `k` corner |
| P4 | the square with an off-diagonal letter changed, with a row made longer by a cell off the diagonal, or with a row added is not valid |
| P5 | words that all have one length are valid exactly when they are as many as their length and their grid is symmetric |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

P4 first said that any row made one letter longer is invalid. It is
not: when row `r` has exactly `r` letters, the new cell is `(r, r)`, on
the diagonal, its own mirror, and the result can still be valid. All
four arms and the brute force agreed on those cases, so the property
was corrected, not the arms.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | mirror: a missing mirror cell is accepted | P1 667, P4 1500, P5 329 |
| M2 | mirror: a letter past the last row is skipped | P1 93, P4 689, P5 329 |
| M3 | grid: the last column is not compared | P1 596, P4 1500, P5 254 |
| M4 | grid: missing cells read as `a` | P1 248, P2 482, P4 1500, P5 157 |
| M5 | columns: the last row is never read into a column | P1 415, P3 1500, P5 106 |
| M6 | columns: only the lengths are compared | P1 216, P4 1344, P5 220 |
| M7 | cells: every cell is its own mirror | P1 1060, P4 1500, P5 1394 |
| M8 | cells: a missing mirror is accepted | P1 760, P4 1500, P5 658 |

A first M6, which dropped the columns arm's check for a row reaching a
column past a gap, survived every property; that is how the check was
found to be redundant (see Approaches). P2 sees only M4: renaming the
letters turns some `a`s into `b`s, so a missing cell that read as
`a` stops matching. M5 rejects every square, so P3 sees it on every
case and P4, which expects rejections, never does.

## Verification

All four arms print the same output as `valid_word_square.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `30000 checks, 0 failures` on all six backends:
those three, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`.

The arms do not run on the last three: the frozen legacy codegen has
no `split_whitespace()` on a `Str` parameter, which the harness's
`show(text: Str)` uses, as in katas 418 and 419. Legacy is frozen, so
this is noted, not filed. The arms' own code builds there, as the
differential and the bench program show.

## Benchmarks

The bench program uses the ★ arm on one word square of 500 rows (the
problem's limit) of 195,633 letters: a symmetric grid of `a` and `b`
cut to a symmetric staircase. Each of 6,000 rounds flips one letter
and, two rounds in three, its mirror as well, which keeps the square
valid; on the third round the lone flip makes it invalid (unless it is
on the diagonal) and is undone after the check. A flip rebuilds the
row's string in every implementation. The program counts the valid
answers and folds them into a checksum. Every implementation prints
`6000 rounds on 500 words, 195633 letters: 4003 valid, checksum
310447774`; a 30-round cut of the Kāra program under `karac __mir-run`
prints the same as the C program cut the same way. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.73 to 0.83 s |
| Kāra (legacy `karac build`) | 0.71 to 0.94 s |
| Rust (`rustc -O`) | 0.92 to 1.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.97 to 1.11 s |
| Go | 1.30 to 1.46 s |
| Python | 70 to 71 s |

The machine was busy with other runs, so the spread is wide and the
compiled languages are within its noise of each other. The Kāra program
also prints the same line under `karac __mir-llvm-run` in 6.6 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark. The `karac build` time is the frozen legacy
backend.

The 30-round cut takes 40 s under `karac __mir-run`, because the MIR
interpreter's `String.bytes()` copies the string (one value per byte)
rather than handing out a view, so the ★ arm's `words[j].bytes()` costs
the length of row `j` on every cell. That is how the interpreter
implements it (see B-2026-10-12-8's fix, which keeps the copy and frees
it sooner), not a wrong answer, so it is not filed; the language makes
`bytes()` an O(1) view, and both compiled backends treat it as one.

## Compiler findings

No new findings. The legacy `karac build` warns that `words` is moved
into `valid_word_square(words)` and used again by the next `flip`; that
is its pre-D5 ownership checker, in which a bare parameter takes
ownership, and the program builds and runs correctly.
