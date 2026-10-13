# 529. Minesweeper

You are given an `m x n` char matrix `board` representing the game
board, where `'M'` is an unrevealed mine, `'E'` an unrevealed empty
square, `'B'` a revealed blank square with no adjacent mines (above,
below, left, right and all four diagonals), a digit `'1'` to `'8'` how
many mines are adjacent to a revealed square, and `'X'` a revealed
mine. You are also given `click = [clickr, clickc]`, the position of
the next click among the unrevealed squares (`'M'` or `'E'`). Return
the board after revealing this position:

1. If a mine `'M'` is revealed, the game is over: change it to `'X'`.
2. If an empty square `'E'` with no adjacent mines is revealed, change
   it to a revealed blank `'B'`, and reveal all its adjacent unrevealed
   squares recursively.
3. If an empty square `'E'` with at least one adjacent mine is
   revealed, change it to a digit `'1'` to `'8'`.
4. Return the board when no more squares will be revealed.

```
board = EEEEE    click = [3, 0]  ->  B1E1B
        EEMEE                        B1M1B
        EEEEE                        B111B
        EEEEE                        BBBBB

that board, click = [1, 2]       ->  the same with the M as X
```

**Constraints:** `1 <= m, n <= 50`; `board[i][j]` is `'M'`, `'E'`,
`'B'` or a digit `'1'` to `'8'`; `click.length == 2`; the click is on
an `'M'` or an `'E'`.

## Approaches

Every arm is `fn update_board(board: own Vec[Vec[char]], click:
Vec[i64]) -> Vec[Vec[char]]`: it takes the board, as the problem's
"return the board" asks, and hands it back changed.

| file | mechanism |
|---|---|
| `update_board.kara` ★ | reveal recursively, as the rules read |
| `update_board_queue.kara` | breadth first with a `VecDeque`, each square marked as it is queued |
| `update_board_stack.kara` | depth first with a `Vec` as the stack, each square revealed as it is pushed |
| `update_board_sweep.kara` | count the mines around every square first, then sweep the whole board until a sweep reveals nothing |
| `differential.kara` | the four arms against a union-find definition, five properties |

Every arm prints the same 7 lines: both examples, a board of one
empty square and of one mine, a click beside a mine, a click walled
off by mines, then for 500 random boards of 1 to 12 by 1 to 12 with
up to 30% mines and three clicks each on squares still unrevealed the
blanks, the mines hit and a checksum, and last the largest case, a 50
by 50 board with 2% mines clicked at the top row's first empty square.
`update_board.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a definition
that does not reveal step by step: union-find joins every pair of
touching empty squares no mine touches, and the click's group plus
every unrevealed square touching it is what opens. Each arm is held to
the properties below on 1,000 random boards of 1 to 10 by 1 to 10
with up to 30% mines, a third of them with an earlier click already
made, clicked on a square still unrevealed.

| | property |
|---|---|
| P1 | the board is the definition's |
| P2 | only unrevealed squares change: an `E` to `B` or a digit, and a mine only when it was clicked, to `X` |
| P3 | every revealed digit is its mine count, and every blank touches no mine and no unrevealed square |
| P4 | the same click again changes nothing |
| P5 | the board turned on its diagonal and clicked at `(c, r)` gives the result turned the same way |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a square with one mine beside it opened as a blank (`> 1`) | P1 438, P3 438 |
| M2 | ★: a clicked mine left as `M`, not `X` | P1 187 |
| M3 | queue: only the rows below a blank opened (`0..=1`) | P1 264, P3 264, P5 340 |
| M4 | queue: every digit one too high | P1 583, P3 583 |
| M5 | stack: a digit square also opens its neighbours | P1 505 |
| M6 | stack: the last column never opened | P1 303, P3 303, P5 343 |
| M7 | sweep: one sweep only, not to a fixed point | P1 267, P3 267, P5 223 |
| M8 | sweep: a square opened beside any open square, not only a blank | P1 530 |
| E1 | queue: the square itself counted among its neighbours | 0 |
| E2 | queue: no `queued` grid, so a square can be queued twice | 0 |
| E3 | sweep: a mine's own square not taken off its count | 0 |
| E4 | ★: the square itself counted among its neighbours | 0 |

P2 and P4 kill nothing here. None of the eight mutants touches a
square that was already revealed, and none reveals a square twice in
a different way, so the board after a second click is the first one
again even when both are wrong. They stay as properties of the
problem. E1 and E4 count the square being revealed among its
neighbours; it is never a mine at that point, so the count is the
same. A square queued twice in E2 is revealed again to the same
value. E3 leaves a mine's own square counted in its own total, and a
mine's total is never shown: the comment in the sweep arm that says
the square was counted with its neighbours describes a step the
answer does not need.

## Verification

Every arm prints the same output as `update_board.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program. All of this is at kara `21ffa33dff`.

The frozen legacy backends refuse every file at type checking. Where
`reveal` passes its `mut ref` board on to `mines_around`, which
borrows it, legacy wants the plain type ("expected 'Vec[Vec[char]]',
found 'mut ref Vec[Vec[char]]'"); and it types the items of a `Vec`'s
`iter()` by value, so it refuses the harness's `*ch` ("unary '*'
requires 'ref T' ... found 'char'"). Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 50 boards of 50 by 50 (the
problem's largest) once, each square a mine with a chance of 0 to 20
in 100 chosen per board; then in each of 400 rounds every board gets a
fresh copy clicked at a random square. Every implementation uses the
same generator and prints `50 boards of 50 by 50, 400 rounds of
clicks: 18756720 opened, 1768 exploded, checksum 964194594`, the Kāra
program under `karac __mir-run` included (in 525 s). The C mirror keeps
a board as one flat array of bytes and copies it with `memcpy`; Rust
and Go keep rows of 4-byte `char`/`rune`, as Kāra does. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.72 to 0.77 s |
| Rust (`rustc -O`) | 1.08 to 1.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.28 to 1.37 s |
| Go | 1.58 to 1.61 s |
| Python | 64.0 to 65.1 s |
| Kāra (`karac build --mir`) | 1.19 to 1.49 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`21ffa33dff`, and the `karac __mir-run` time at kara `c8bdf31cda`.
Under `karac __mir-llvm-run` the program prints the same line in
6.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
