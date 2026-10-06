# 353. Design Snake Game

A snake starts in the top-left cell of a `width x height` board with length
1. Food appears one piece at a time, in a given order. Each move (`U`, `D`,
`L`, `R`) puts the head one cell over. If the head lands on the current food,
the snake eats it and grows by one (its tail stays put); otherwise the tail
moves first, so the head may enter the cell the tail is leaving. A head off
the board or on the body ends the game and the move returns `-1`; otherwise
the move returns the score, the number of pieces eaten.

```
width 3, height 2, food (1,2) then (0,1)
R -> 0    D -> 0    R -> 1 (eats)    U -> 1    L -> 2 (eats)    U -> -1 (wall)
```

**Constraints:** `1 <= width, height <= 10^4`; at most `50` pieces of food;
at most `10^4` calls to `move`. A piece of food never appears on the body.

## Approaches

| file | mechanism | cost per move |
|---|---|---|
| `snake_game.kara` ★ | a `VecDeque` of body cells (`row * width + col`, head last) and a `Set` of the cells it covers | `O(1)` expected |
| `snake_game_grid.kara` | a `Vec[bool]` of the whole board and the body in a ring buffer the size of the board; no hashing | `O(1)`, `O(width * height)` memory |
| `snake_game_stamps.kara` | no body list at all: one number per cell, the move at which the head last entered it. After move `t` the body is exactly the cells entered after `t - len`, so one comparison is both the bite test and the tail-leaves-first rule | `O(1)`, `O(width * height)` memory |
| `snake_game_points.kara` | the sketch a reader would draw: a `Point` struct with derived `Hash`, a `Dir` enum parsed from the letter, `Point.moved` returning `None` at a wall, and the food as a queue | `O(1)` expected |
| `differential.kara` | the four arms and an independent oracle, 35,291 checks, five properties | — |

Every arm prints the same 14 lines: the example, five edge cases (a wall on
the first move, a length-3 snake chasing its tail round a 2 x 2 board
forever, a bite, turning back at length 2, which is legal because the tail
leaves first, and at length 3, which is not), and a long game. The long game
follows a Hamiltonian cycle round a 60 x 40 board for three laps with food
three cells ahead until 1000 pieces are eaten, prints the score and length
every 1200 moves and a checksum over every move, then turns into its own
body. `snake_game.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and an oracle that shares no
code with them: the body as a plain `Vec` of `(row, col)` pairs, head last,
searched linearly. 1500 random games on boards from 1 x 1 to 7 x 7, each with
up to 11 pieces of food at random cells and up to 60 random moves; nine moves
in ten are steered away from walls and the body so games last long enough to
eat. A piece of food may lie on the body when it comes up (LeetCode rules
that out), and the arms and the oracle all treat that as a bite.

| | property |
|---|---|
| P1 | every arm returns the oracle's answer on every move |
| P2 | while alive, the score is the number of pieces eaten and every arm's length is score + 1 |
| P3 | while alive, the oracle's body is a simple path: in bounds, distinct, each cell next to the one before |
| P4 | a move off the board returns `-1` |
| P5 | on every board from 2 x 2 to 8 x 8 with an even number of rows, a snake that follows the Hamiltonian cycle with food three cells ahead never dies in three laps |

It prints `failures 0` with `35291 checks, 1294 deaths, 1111 pieces eaten,
84 laps, checksum 849565222` on every surface. An independent Python replay of
the random games and the oracle gives the same check count, deaths, pieces
eaten and checksum.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each built and run.
All twelve are killed.

| # | mutation | how |
|---|---|---|
| M1 | set: forget to uncover the tail cell | P1; the arm then indexes an empty deque and panics |
| M2 | set: test for a bite before the tail moves | P1, 5932 failures |
| M3 | grid: read the head one slot past the ring's end | P1 and P2, 32284 failures |
| M4 | grid: write the new head over the old head | P1; the arm then reads past its ring and panics |
| M5 | stamps: `>=` for `>` in the body test | P1 and P2, 9707 failures |
| M6 | stamps: compare against `t - len + 1` | P1, 135 failures |
| M7 | stamps: never move the head | P1, P2 and P5, 34282 failures |
| M8 | points: parse `L` as `Right` | P1 and P2, 28444 failures |
| M9 | points: let the head reach column `width` | P1, 230 failures |
| M10 | points: eat without scoring | P1, 12835 failures |
| M11 | oracle: compare the food's row with the column | P1 and P2, 59333 failures |
| M12 | oracle: the tail never leaves first | P1, 1988 failures |

## Verification

All four arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py --filter
353- --include-bench`: 0 divergences), and the four arms match
`snake_game.py` byte for byte. The bench program prints `714297392` under
LLJIT and both builds, as do its C, Rust, Go and Python mirrors. Under
`karac run --interp` it outran the sweep's 400-second budget, so the bench
program has no interpreter verdict. Built at `-O0` with
`KARAC_AUTO_PAR=0`, the four arms and the bench program are valgrind-clean.
The differential is not: it leaks one small block per board in P5, from
**B-2026-10-06-99** below. The differential takes 28 seconds under
`karac run --interp` on a release build.

## Benchmarks

`bench/snake_game.kara` and its four mirrors time the **grid + ring-buffer
arm**, the one arm that is the same algorithm in C, Rust, Go and Python (the
★ arm's `Set` has no C equivalent). Each of 30 rounds builds a board of
1000 × (400 + 2·round) cells, lays food three cells ahead of the snake along a
Hamiltonian cycle until a quarter of the board is eaten, and plays three full
laps of the cycle, folding every move's result into the sink. All five print
`sink 714297392`.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10553+g87d927e95`, measured 2026-10-06, with the timed lane built
with `KARAC_AUTO_PAR=0`. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 503 ms ± 44 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 532 ms ± 58 | 1.06× |
| **kāra `karac build`** | **536 ms ± 76** | **1.06×** |
| rust `-O -C overflow-checks=on` (equal-safety) | 549 ms ± 52 | 1.09× |
| rust `-O` | 561 ms ± 87 | 1.11× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 614 ms ± 82 | 1.22× |
| go `go build` | 1038 ms ± 36 | 2.06× |
| python 3 | 28507 ms ± 162 | 56.6× |

**Kāra, C and Rust are level.** The spread between them is smaller than one
standard deviation on this run (the container was noisy, at 8–16% CV), so read
the top six rows as a tie. The work is a modulo-indexed ring, a boolean-per-cell
grid and a branch per move, which every compiled language turns into much the
same loop. Go is 2× behind. Python is 57× behind, against 16× on #352, because every move is a handful of interpreted list reads and writes
with no library call to hide them in.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 107.2 ms ± 9.5 | 15.8 KiB | 7.4 MiB |
| rust | 196.0 ms ± 8.9 | 3865.8 KiB | 8.0 MiB |
| kāra | 435.9 ms ± 32.0 | 345.6 KiB | 19.4 MiB |
| go | — | 2166.9 KiB | 26.2 MiB |
| python | — | — | 57.0 MiB |

Kāra's peak RSS is 2.6× C's. Part of that is the move list: a Kāra `char` is
a 4-byte Unicode scalar, where the C and Rust mirrors hold one byte per move,
so the 460,000-move list of the last round is 1.8 MB against 0.46 MB. That
does not cover all of it. Rebuilt with fewer rounds, the Kāra binary peaks at
10.2 MiB after 1 round, 18.7 MiB after 10 and 19.5 MiB after 30, against
6.6 MiB for C after 1 round. So the extra is reached in the first few rounds
and then stays flat; valgrind finds nothing leaked (below). The rest was not
traced; allocator growth under repeated `push` doubling is the likeliest
cause, but that is inferred, not measured.

## Compiler findings

- **B-2026-10-06-99 (open, codegen): a `.chars()` chain whose receiver is a fresh
  `String` temporary never frees the string.** P5 builds each board's moves
  with `cycle_moves(w, h).chars().collect()`, and valgrind shows one block
  per board lost, 28 in all. `collect`, `count`, a `for` loop and `map` over
  `.chars()` of a temporary all leak it; `.len()` and `.bytes()` of the same
  temporary do not, nor does the same chain over a `let`-bound string. The
  differential keeps the natural one-liner.
- **B-2026-10-06-98 (open, codegen): a trait method called through a generic bound is
  not dispatched when the type argument is a `shared struct`.** A probe that
  drove all the game types through one `fn drive[G: Snake](g: mut ref G, ..)`
  ran under `--interp` and was refused by every compiled surface. A plain
  struct or a `shared enum` in the same place builds.
- **B-2026-10-06-74 (open), widened:** that row says the predicates of `find`
  and `filter` get the item by value where the design says `ref`. The same
  holds for `for x in v.iter()` and `any`: `*x` is refused, so `body.iter().any(|p| p == next)`
  is the spelling that compiles.

The author already knows the language, so none of this counts toward the
machine-fix rate.
