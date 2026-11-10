# 2056. Number of Valid Move Combinations On Chessboard

There is an 8 x 8 chessboard holding `n` pieces (rooks, queens or
bishops). You are given a string array `pieces` of length `n`, where
`pieces[i]` is the type of the `i`th piece, and a 2D integer array
`positions`, where `positions[i] = [ri, ci]` is the 1-based square the
`i`th piece stands on.

Each piece makes a move: it picks a destination square and travels toward
it in a straight line, one square a second, as its type allows. A rook
moves along rows and columns, a bishop along diagonals, a queen either
way. A piece may also choose its own square and not move. Every piece
starts at second 0 and they all move at once; a piece stops once it
reaches its destination. A move combination is invalid if at any second
two or more pieces occupy the same square; two adjacent pieces may move
past each other, swapping squares, within one second. Return the number
of valid move combinations.

```
pieces = ["rook"],   positions = [[1,1]]  ->  15
pieces = ["queen"],  positions = [[1,1]]  ->  22
pieces = ["bishop"], positions = [[4,3]]  ->  12
```

**Constraints:** `n == pieces.length == positions.length`; `1 <= n <= 4`;
`pieces` only holds `"rook"`, `"queen"` and `"bishop"`; there is at most
one queen on the board; `1 <= ri, ci <= 8`; each `positions[i]` is
distinct.

A move is a direction and a number of squares, with staying put a move of
its own, and where a piece stands at second `t` is its start plus
`min(t, squares)` steps. Two pieces collide when they stand on one square
at some second up to the longer of their two moves; after that neither
moves. With at most four pieces and at most 28 moves each, the
combinations can be listed; the approaches differ in how they prune and
how they test a collision.

The harness draws boards with any number of queens, which the
constraints' "at most one queen" does not stop any approach from
answering: it only bounds the work.

## Approaches

| file | mechanism |
|---|---|
| `moves.kara` ★ | each piece's moves listed as (row step, column step, squares) in a `#[derive(Copy, Clone)]` struct; the pieces given moves one at a time by backtracking, each new move walked against the moves already chosen until both have stopped |
| `moves_brute.kara` | every combination of moves, an odometer turning over each piece's list, each combination checked pair by pair; no pruning |
| `moves_table.kara` | every pair of two pieces' moves walked once, up front, into a table of which pairs collide; the combinations then counted by backtracking with table lookups |
| `moves_board.kara` | the board as a `Set` of (row, column, second) for every square a chosen piece stands on in each of the first seven seconds; a new move is valid when none of its own cells are taken, and its cells are removed again on the way back |
| `moves_layers.kara` | the valid combinations built a piece at a time, breadth first: each valid combination of the first pieces extended with `flat_map` by each move of the next piece that collides with none of it |
| `moves_solution.kara` | LeetCode's Rust template (`[(i32, i32); 8]` directions sliced by a `match` on `pieces[i].as_str()` into ranges, `vec![vec![]; n]` of `(dr, dc, k)` moves, and two nested `fn`s, `ok` and a `dfs` over `&mut Vec`), carried by `karac fix` in five rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four more,
each board and its count; then the sum and a checksum of the counts for
300 random boards of 1 to 3 pieces of any kinds on distinct squares of a
corner from 3 x 3 to 8 x 8, so that pieces crowd and block each other;
then the same for 4 boards of 4 pieces on the whole board. `moves.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each piece's destinations found from the board's geometry (its
own square, or any square along a row, column or diagonal its kind may
take, with no list of directions), every choice of destinations tried,
and the pieces stepped one square a second toward theirs, the
combination failing if two ever share a square. It checks 60 random
boards of 1 to 3 pieces, drawn as the harness draws its small ones,
before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the count is at least 1, every piece staying, and at most the product of the pieces' moves; for one piece, it is that piece's moves |
| P3 | the board mirrored top to bottom, and the board transposed, have the same count |
| P4 | the pieces listed backwards have the same count |
| P5 | the first piece as a queen counts at least as many as it does as a rook or a bishop, and at most the two together |
| P6 | each arm agrees with at least three of the other five |

The differential prints `60 boards: checksum 200221522, 2160 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and no
two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: staying put not a move | P1 60, P2 19, P6 60 |
| M2 | ★: each move checked against the first piece only | P1 12, P4 13, P6 12 |
| M3 | ★: the board seven squares wide | P1 56, P2 15, P3 52, P6 56 |
| M4 | brute: only neighbouring pieces compared | P1 13, P6 13 |
| M5 | brute: the odometer skipping each wheel's last move | P1 60, P2 19, P3 33, P5 14, P6 60 |
| M6 | brute: the rows compared, not the squares | P1 41, P3 40, P6 41 |
| M7 | table: the table read with its moves swapped | P1 36, P3 33, P5 8, P6 36 |
| M8 | table: the first second never walked | P1 22, P6 22 |
| M9 | table: a queen moving as a rook | P1 33, P2 4, P6 33 |
| M10 | board: the second left out of each cell | P1 34, P6 34 |
| M11 | board: a bishop moving as a rook | P1 33, P2 31, P6 33 |
| M12 | board: the start square taken as the first second | P1 7, P6 7 |
| M13 | layers: the pieces compared a second apart | P1 39, P4 37, P6 39 |
| M14 | layers: a rook's moves along rows only | P1 49, P2 11, P3 35, P6 49 |
| M15 | layers: staying put listed twice | P1 60, P2 44, P6 60 |
| M16 | solution: a bishop's directions one short | P1 32, P2 8, P3 30, P5 57, P6 32 |
| M17 | solution: the move to the edge left out | P1 57, P2 16, P3 51, P6 57 |

P1 and P6 kill all seventeen, P2 nine, P3 seven, P5 three and P4 two. P2
asks one-piece boards for the piece's own moves, so it catches every edit
that changes a list of moves (M1, M3, M5, M9, M11, M14 to M17) and none
that only changes how two moves collide. P3 mirrors and transposes the
board, so it catches the arms that treat rows and columns, or one side of
the board, unevenly: the seven-wide board, the rows compared alone, a
rook along rows only, a bishop's missing direction, the edge left out.
P4 lists the pieces backwards and catches only the two edits that treat
an earlier piece differently from a later one (M2, M13): a collision is
symmetric, so everything else passes it. P5 compares a queen with a rook
and a bishop on the same square, and catches the edits that break that
sum (M5, M7, M16). A collision missed shows only in P1 and P6, which is
why so many of the edits below fail alike.

Of the thirty-six, nineteen were not kept. One is equivalent: the Rust
arm's adapter swapping row and column transposes the board, which P3
already shows changes no count. Seven fail the same 40 checks, every one
a way of missing a collision: the ★ arm's last second never walked and
only its destinations compared, the table arm's walk stopped with the
shorter move, the board arm's stopped piece leaving the board, the layers
arm's moves checked against no piece and its walk a second short, and
the Rust arm's last second never walked. Three make one kind move as a
queen (a bishop in the ★ arm, a rook in the brute and Rust arms) and fail
alike. The board arm's cells never taken back and the layers arm's last
piece never added fail alike. Four fail as a kept one does: the brute
arm's move one square short of the edge as M1, the table arm's check
against the previous piece only as M4, its columns compared as M6, and
the board arm's first four seconds as M8. The brute arm's stopped piece
leaving the board and the Rust arm's check against the chosen moves from
the second piece on fail on checks of their own, and were left out
because those arms keep three and two.

## Verification

Every arm prints the same output as `moves.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.
Under `karac __mir-run` the arms take 3.7 s (table) to 15 s (brute), and
the board arm 39 s, a `Set` of cells built and taken back for every move
tried; the differential takes 65 s.

The five Kāra arms met no compiler gap. The ★ arm's `Move` was first
declared with no derive: `[Move { .. }].to_vec()` clones each element, and
the error asked for `#[derive(Copy)]`; the warning that followed asked for
`Clone` beside it (a derive never adds another), with a fix. The harness's
`kinds[next_random(mut seed) % 3]` moved a `String` out of an index, and
the error offered `.clone()`. The layers arm first collected each inner
list with Rust's turbofish, `.collect::<Vec<Vec<Move>>>()`, which Kāra
does not have; the error said to annotate the binding instead, and the
closure now returns the inner iterator itself, which `flat_map` takes.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in five rounds of 36, 2, 2, 9 and 2 edits to a clean check: the
`struct Solution;` and Rust's spellings (`Vec<..>`, `&[..]` to
`Slice[..]`, `&mut` to `mut ref` with `mut` at the call, `&&` to `and`,
`[T; 8]` to `Array[T, 8]`, `vec![..]`), the two nested `fn`s moved out
above the `impl` (Kāra has no nested items, and a nested `fn` captures
nothing), `usize` to `i64`, and `res` and `k` declared `i32`. The
`&(r + dr * k)` given to `contains` keeps its parentheses as
`contains((r + dr * k))`. The adapter hands the harness's positions to it
as `Vec[Vec[i32]]`.

## Benchmarks

The bench counts the move combinations of 200 boards of 4 pieces, the
constraints' limit in pieces though not in queens, of random kinds on
random squares, with the ★ arm in all five languages. Every
implementation prints `200 boards: sum 9181033, checksum 869378135`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `0142335972` and the fixes from
katas 2054 to 2057, on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.362 to 0.418 s | 0.368 s |
| Rust (`rustc -O`) | 0.412 to 0.455 s | 0.431 s |
| Kāra (`karac build`) | 0.457 to 0.505 s | 0.460 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.460 to 0.523 s | 0.489 s |
| Go | 0.476 to 0.517 s | 0.503 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.491 to 0.552 s | 0.515 s |
| Python | 25.3 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.457 s) is not above its real time (0.460 s).

The sequential Kāra program is 0.95x Rust under overflow checks and 1.33x
C. Overflow checks cost Rust 19% here: the collision walk is arithmetic
on every square of every second.
