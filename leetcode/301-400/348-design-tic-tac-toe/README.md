# 348. Design Tic-Tac-Toe

An `n x n` board starts empty. `make_move(row, col, player)` puts player 1's
or player 2's mark on an empty cell and returns the player who has just won,
or `0` if nobody has. A player wins by holding all `n` cells of a row, a
column, or either diagonal. Every move is to an empty cell, and no move
follows a win.

```
TicTacToe(3)
make_move(0, 0, 1) -> 0     X . O
make_move(0, 2, 2) -> 0     O O .
make_move(2, 2, 1) -> 0     X X X
make_move(1, 1, 2) -> 0
make_move(2, 0, 1) -> 0
make_move(1, 0, 2) -> 0
make_move(2, 1, 1) -> 1     player 1 holds the bottom row
```

## Approaches

| file | mechanism | cost per move |
|---|---|---|
| `tic_tac_toe.kara` ★ | one signed counter per row, per column and per diagonal: player 1 adds 1, player 2 subtracts 1, and a line is won when its counter reaches `n` or `-n` | `O(1)` time, `O(n)` space |
| `tic_tac_toe_board.kara` | the board itself, with the four lines through the new mark read back | `O(n)` time, `O(n²)` space |
| `tic_tac_toe_per_player.kara` | unsigned counters, one set per player, so no sign trick | `O(1)` time, `O(n)` space |
| `tic_tac_toe_map.kara` | the star arm's counters in a `Map` keyed by `(kind, index)`; only touched lines exist | `O(1)` expected time |
| `tic_tac_toe_closure.kara` | no struct: a closure captures the counters and mutates them | `O(1)` time, `O(n)` space |
| `differential.kara` | the five arms and a full-board oracle on 1,440 games, five properties | — |
| `bench/tic_tac_toe.kara` | 100 games of up to 1,000,000 moves on a 1,000 x 1,000 board, by the ★ arm | — |

The signed counter works because a line that holds marks from both players
can never reach `n` or `-n`, so the sign carries the "only one player is on
this line" fact for free. The map arm never iterates its map, so the map's
unspecified order cannot reach the output.

Every arm prints the same 6 lines: the problem's example, a 1 x 1 board won
by the first mark, a column win for player 2, an anti-diagonal win on a 4 x 4
board, a full 3 x 3 board that nobody wins, and 1,000 random games on boards
from 1 x 1 to 40 x 40, each playing every cell in a shuffled order. Random
play rarely wins a big board, so most of those end full:

```
1000 random games: player 1 won 83, player 2 won 28, 553336 moves
```

`tic_tac_toe.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` plays 160 games on every board size from 1 x 1 to
9 x 9, 1,440 games in all. Each game plays every cell of the board in a
shuffled order. Random play wins rarely, so half the games are steered: the
cells of one line, chosen by the seed, go to player 1's turns first, and
player 1 wins by move `2n - 1` unless player 2 wins sooner. Every arm is
compared with a sixth version, the oracle, which after each move rescans all
`n` rows, all `n` columns and both diagonals of a full board.

| | property |
|---|---|
| P1 | all five arms equal the oracle exactly |
| P2 | transposing every move, `(r, c)` to `(c, r)`, changes no result |
| P3 | mirroring every move, `(r, c)` to `(r, n - 1 - c)`, changes no result |
| P4 | a game that nobody wins fills the board, `n * n` moves |
| P5 | only a game's last move can return a winner, and it returns the player who made it |

It prints `failures 0` and all properties hold on every surface, with
`1440 games: player 1 won 989, player 2 won 82, 28665 moves`. An
independent Python replay of the game generator and the oracle gives the same
line.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each run under
`karac run`. All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | counter: player 2 adds 1 as well | P1, P2 and P3, 2,160 failures |
| M2 | counter: the anti-diagonal test uses `n` for `n - 1` | P1, P2 and P3, 552 failures |
| M3 | counter: never check the anti-diagonal | P1, P2 and P3, 552 failures |
| M4 | board: read the row back as a column | P1, 262 failures |
| M5 | per player: win at `n - 1` marks | P1, 1,345 failures |
| M6 | per player: columns share the rows' counters | P1, 928 failures |
| M7 | map: the goal is `n` for both players | P1, 82 failures |
| M8 | map: count every cell right of the diagonal as on it | P1, 226 failures |
| M9 | closure: the goal is `n - 1` | P1, 1,164 failures |
| M10 | closure: never switch players | P1, 728 failures |
| M11 | oracle: keep playing after a win | P1, P2, P3 and P5, 11,414 failures |

One further edit survived because it changes nothing: in the board arm,
starting `whole_anti` at `true` instead of `row + col == n - 1`, so the
anti-diagonal is read back after every move. A move off the anti-diagonal
cannot complete it, and had it been complete earlier the game would already
have ended. It is an equivalent mutant, not a gap in the differential.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 6
programs, 0 divergences). Built with `KARAC_AUTO_PAR=0`, all six are
valgrind-clean: `0 errors` and `0 bytes in use at exit`.

## Benchmarks

`bench/tic_tac_toe.kara` and its four mirrors time the ★ arm as written. The
order of all 1,000,000 cells of a 1,000 x 1,000 board is shuffled once. Each
of 100 games starts a fresh board and plays that order from its own starting
point, wrapping around and alternating players, until somebody wins or the
board is full. Every game's move count and winner are folded into the sink,
so no move can be skipped. Random play on a board this size never completes a
line, so all 100 games run to a full board: 100,000,000 moves, each with its
win check, but the check never succeeds.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10448+g76727438c`, measured 2026-10-05, with the timed lane built
with `KARAC_AUTO_PAR=0`. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 381.6 ms ± 14.1 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 387.7 ms ± 12.6 | 1.02× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 408.6 ms ± 26.9 | 1.07× |
| rust `-O -C overflow-checks=on` (equal-safety) | 415.1 ms ± 17.9 | 1.09× |
| **kāra `karac build`** | **439.0 ms ± 23.2** | **1.15×** |
| rust `-O` | 443.9 ms ± 13.2 | 1.16× |
| go `go build` | 607.9 ms ± 30.5 | 1.59× |
| python 3 | 51075 ms ± 341 | 134× |

**Kāra ties Rust and is 15% behind C; Go is 1.6× behind.** The three Rust
builds and Kāra are within about two standard deviations of each other.
Unchecked `rust -O` coming out slowest of the Rust builds is inside that
spread, not a real ordering. Where C's 15% comes from was not investigated.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 94.5 ms ± 2.7 | 15.8 KiB | 9.0 MiB |
| rust | 156.5 ms ± 5.8 | 3863.7 KiB | 9.7 MiB |
| kāra | 334.1 ms ± 15.8 | 341.6 KiB | 10.1 MiB |
| go | — | 2178.6 KiB | 11.3 MiB |
| python | — | — | 46.0 MiB |

Peak memory is mostly the 8 MB shuffled order. `karac build` is 3.5× clang's
cold compile and 2.1× rustc's. Its binary is 22× clang's and 11× smaller than
rustc's. Raw numbers are in `bench/results.container-x86.json`. Methodology
and caveats are in [`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

None. Every arm compiled and ran correctly as first written. A probe in a
seventh phrasing (an `enum Player`, a board of `Option[Player]`, lines built
with `map` and checked with `all`) also agreed across `run`, `run --interp`
and `build`. Its first draft used Rust's `{w:?}`; the compiler build used here
reported that as an unsupported radix, which `B-2026-10-05-48` had already
fixed on `main`, so it is not a new finding.
