# 419. Battleships in a Board

Given an `m x n` board where each cell is a battleship part `'X'` or
water `'.'`, return the number of battleships on it. Every battleship is
a straight line of cells, one cell wide, placed across or down, and no
two battleships touch along a side: at least one cell of water separates
them across and down. Diagonal corners may touch.

```
board = [["X",".",".","X"],
         [".",".",".","X"],
         [".",".",".","X"]]  -> 2
board = [["."]]              -> 0
```

**Constraints:** `1 <= m, n <= 200`; every board is valid. The follow-up
asks for one pass, O(1) extra memory, and no change to the board.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `battleships.kara` ★ | count the first cells: each ship has exactly one `'X'` with no `'X'` above it and none to its left, so count those in one pass, as the follow-up asks | O(m n) | O(1) |
| `battleships_flood.kara` | flood fill: each unvisited `'X'` starts a ship, and a stack visits every `'X'` joined to it across or down. It counts ships of any shape, so it does not rely on the ships being straight | O(m n) | O(m n) |
| `battleships_union.kara` | union-find over the cells, with path halving and union by size: start each `'X'` as a ship of its own, join it to the `'X'` to its right and below, and lower the count at every join that merges two ships | O(m n α(m n)) | O(m n) |
| `battleships_links.kara` | cells less links: a straight ship of `k` cells has `k - 1` links between neighbours, and ships never touch, so the answer is all `'X'` cells less all side-by-side pairs | O(m n) | O(1) |
| `differential.kara` | the four arms on 2,000 random boards, five properties, one of them the number of ships the generator placed | — | — |

Every arm prints the same 10 lines: the two LeetCode examples, seven
edge cases (one ship cell, one ship across a row, one down a column,
six one-cell ships, three ships across in two rows, ships of every
direction in a 5 x 5 board, all water) and for 1,000 random boards of
1 to 12 by 1 to 12 cells with ships of 1 to 4 cells placed where they
touch no other ship, the total of the answers and a checksum. Each
board is written as its rows separated by `/`. `battleships.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000
random cases makes a board of 1 to 10 by 1 to 10 cells and tries up to
24 ships of 1 to 5 cells, each placed only where no ship lies beside it
or at either end; corners may touch, as the problem allows, so the
arms are tested on diagonal neighbours too:

| | property |
|---|---|
| P1 | the answer is the number of ships the generator placed |
| P2 | the board transposed, or with each row reversed, gives the same answer |
| P3 | an empty row, and then a row with one ship cell, added below the board add one ship |
| P4 | the board twice side by side, with a column of water between, gives twice the answer |
| P5 | one-cell ships on every other cell of every other row number `ceil(m / 2) · ceil(n / 2)` |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | first: only the cell above is checked | P1 981, P2 1447 |
| M2 | first: the last cell of each row is skipped | P1 889, P2 1417, P3 562, P4 889, P5 1009 |
| M3 | flood: the fill never steps down | P1 1042, P2 1447 |
| M4 | flood: the fill never enters the last column | P1 776, P2 1253, P4 776 |
| M5 | union: a join does not lower the count | P1 1539 |
| M6 | union: cells are joined only downward | P1 981, P2 1447 |
| M7 | links: links to the right are not counted | P1 981, P2 1447 |
| M8 | links: each downward link counts twice | P1 1042, P2 1447 |

M1, M6 and M7 are one mistake in three arms: each miscounts exactly the
ships that run across, so they fail exactly the same checks; M3 and M8
likewise miscount the ships that run down. P2's transpose turns one
kind into the other, which is why it sees all five. M5 counts every
cell, which changes nothing a symmetry or a one-cell ship can see, and
only P1 does. P3, P4 and P5 add only one-cell ships or copies in the
same direction, so they see only the mutants that lose cells at an
edge (M2, M4).

## Verification

All four arms print the same output as `battleships.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac run --interp`,
and `karac check` passes on every file. The differential prints
`40000 checks, 0 failures` on every backend: `karac __mir-run`,
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`.

The arms' harness stops on the other four. Under
`karac __mir-llvm-run` it stops at the missing `String.as_str` native:
`show(text: Str)` is passed a string literal, as in katas 383 to 418.
The frozen legacy codegen has no `split` on that `Str` parameter,
which stops LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`.
Neither is filed. The differential and the bench program pass no
`Str`, and both run on every backend.

## Benchmarks

The bench program uses the ★ arm on one 200 x 200 board (the problem's
limit) holding about 2,300 ships of 1 to 4 cells. Each of 20,000 rounds
places a one-cell ship on a cell whose neighbours are all water, or
sinks a one-cell ship standing alone, so the board stays valid, and
counts the ships again; no compiler can hoist the count out of the
loop. It folds the counts into a total and a checksum. Every
implementation prints `20000 rounds on a 200x200 board: total
101025039, checksum 307155649`; a 50-round cut of the Kāra program
under `karac __mir-run` prints the same as the C program cut the same
way. The C mirror's cells are one-byte `char`s; Kāra's `char`, Rust's
`char` and Go's `rune` are four bytes. Spot timings on a shared 4-core
container, three runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Go | 2.26 to 2.31 s |
| Kāra (legacy `karac build`) | 2.42 to 2.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.46 to 2.59 s |
| Rust (`rustc -O`) | 2.46 to 2.60 s |
| C (`clang -O3`) | 2.84 to 2.93 s |
| Python | 44 s |

All five compiled programs are within about a quarter of each other,
and C with the smallest cells is the slowest; why has not been looked
into. The Kāra program also prints the same line under
`karac __mir-llvm-run` in 6.1 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend, which warns that the
bench reuses `board` after passing it to `clear`, since it predates
bare parameters borrowing; it still builds and runs.

## Compiler findings

No new findings.
