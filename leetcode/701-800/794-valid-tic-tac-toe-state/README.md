# 794. Valid Tic-Tac-Toe State

A tic-tac-toe board is given as three strings of three characters, each
`'X'`, `'O'` or `' '`. Return whether the board can come up in a game: X
moves first, the players take turns putting their mark on an empty cell,
and the game ends when a player has three in a row, column or diagonal,
or the board is full.

```
["O  ", "   ", "   "]  ->  false   (X moves first)
["XOX", " X ", "   "]  ->  false   (the players take turns)
["XOX", "O O", "XOX"]  ->  true
```

**Constraints:** the board is 3 by 3, of `'X'`, `'O'` and `' '`.

## Approaches

| file | mechanism |
|---|---|
| `valid_tic_tac_toe.kara` ★ | by the rules: X has as many marks as O or one more, when X has a line X made the last move and has one more, and when O has a line the counts are equal; the cells counted with `filter` and `count`, and the eight lines checked from a table; O(9) |
| `valid_tic_tac_toe_masks.kara` | each player's marks as nine bits, counted with `count_ones`, and a line when one of eight line masks is all inside a player's bits; then the same rules; O(9) |
| `valid_tic_tac_toe_replay.kara` | search for a game that ends at the board: from the empty board the player to move puts a mark where the board has that player's mark, and the game stops at a line; which marks are down fixes a position, so each of the 2^9 is searched once; O(2^9 × 9) |
| `valid_tic_tac_toe_undo.kara` | taking moves back: the empty board is valid, and any other is valid when the player who moved last has a mark whose removal leaves a valid board with no line on it; each board met is settled once, in a `Map` from the board's text to its answer |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: LeetCode's three examples; the empty
board; a line for X with X a mark ahead, and one with the counts equal;
lines for both players, in two rows and in two columns; a full board
with a line for X; and 300 random boards, half with each cell filled at
random and half from a random game of 0 to 9 moves that may go on past a
line, with how many are valid and a checksum. `valid_tic_tac_toe.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every game, played from the empty board with every move at every
position until a line or a full board, marking each board met in a table
of all 3^9 boards; a board met before is not played on again, since the
player to move follows from the marks. It finds the 5,478 boards that
can come up. Every arm is held to it on all 19,683 boards, and to three
properties on 1,000 random boards, a third filled at random and the rest
from random games, a quarter of which go on past a line.

| | property |
|---|---|
| P1 | the answer is the definition's, for every board |
| P2 | the board turned and mirrored all eight ways gives the same answer |
| P3 | on a valid board with no line, every move by the player to move gives a valid board |
| P4 | on a valid board with a mark, some mark of the player who moved last can be taken back to a valid board with no line |

It prints `all 19683 boards (5478 valid) and 1000 random ones (736
valid), 4 arms, 90732 checks, 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error. Under `__mir-run` it takes about 32 s; the replay arm, before
it kept the positions it had tried, took 27 s of that alone, and a first
version with 1,600 random boards ran past the corpus's 60 s.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second diagonal not a line | P1 71, P2 6, P4 2 |
| M2 | ★: X two marks ahead allowed | P1 1372, P3 5, P4 17 |
| M3 | ★: an O line needing X one mark ahead | P1 484, P3 43, P4 11 |
| M4 | masks: two cells of the middle row taken as a line | P1 332, P2 100, P3 31, P4 2 |
| M5 | masks: an O line allowed when X is a mark ahead | P1 168, P4 11 |
| M6 | masks: O's marks counted from X's bits | P1 11022, P3 129, P4 14 |
| M7 | replay: play going on after an O line | P1 168, P4 11 |
| M8 | replay: either player may put down any of the board's marks | P1 3909, P2 418, P3 125 |
| M9 | replay: every position after the first taken as tried | P1 5468, P3 87 |
| M10 | undo: the wrong player taken as the last to move | P1 5477, P3 61 |
| M11 | undo: a board with a line taken as one play went on from | P1 568, P4 23 |
| M12 | undo: any board with no X taken as the empty board | P1 511, P4 1 |

P1 kills all twelve, as it sees every board. P2 kills the three edits
that treat a line unlike its turned and mirrored copies: the dropped
diagonal, which a quarter turn makes the other one; the two cells taken
as a line; and the replay that lets either player put down any mark,
whose answer then depends on the order it tries the cells in, since the
marks down no longer fix the position. P3 kills seven, the edits that
call some board one move on from a valid one invalid, and P4 nine, the
edits that let a board count as valid without one before it.

## Verification

Every arm prints the same output as `valid_tic_tac_toe.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) runs the ★, masks
and undo arms unchanged and prints the same output. The legacy `karac
build` panics in its method-call lowering on the harness's
`rows.iter().map(|r| r.to_string()).collect()` over an `Array[Str, 3]`
parameter; written as a loop it still fails, as it cannot pass an
`Array[Str, 3]` argument (module verification rejects the call) and has
no `to_string` for a `Str` parameter. Legacy refuses the replay arm and
the differential at the type check, where a `mut ref Vec[u8]` or `mut
ref Vec[i64]` is passed to a parameter declared `Vec[u8]` or `Vec[i64]`.
Copies whose harness takes the three rows as `String`s and builds the
board with `vec!`, and whose `has_line`, `goal`, `code_of` and `line_of`
parameters are written `ref`, print the same output as v2 under the
legacy interpreter, the legacy JIT (`karac run`), `karac build` and an
auto-par build. Legacy also refuses the bench program's
`valid_tic_tac_toe(boards[r % 4096])` as a move out of an index; a copy
with `ref` parameters builds and prints the same line, and the bench
timing below is of it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 4,096 boards are
made once, half with each cell filled at random and half by a random
game of 0 to 9 moves that may go on past a line. Each of 6,000,000
rounds asks whether the next board can come up in a game. Every
implementation prints `6000000 boards: 3622545 valid, checksum
678377503`, the Kāra program under `karac __mir-run` included (in 412
s).

The bench measures a short function called often: copying nine bytes out
of three strings, two counts and sixteen line checks. Kāra and Rust
gather the cells into a new `Vec` and count them with `filter`, Go
appends them to a slice of capacity 9, and C copies them into an array
on the stack. Spot timings on a shared 4-core container, eight runs of
each compiled program, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.17 to 0.20 s |
| Rust (`rustc -O`) | 0.50 to 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.46 to 0.65 s |
| Go | 0.50 to 0.66 s |
| Python | 11.13 to 11.56 s |
| Kāra (`karac build --mir`) | 1.81 to 2.12 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 7.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.05 s,
against C's 0.18, Rust's 0.52 (0.55 under overflow checks) and Go's
0.55. Under valgrind's cachegrind v2 runs 17.5 billion instructions and
2.89 billion branches, against C's 1.05 billion and 0.07 billion and
Rust's 4.06 billion and 0.61 billion, so it does about four times Rust's
work for the same function. Where that work lies is not profiled. The
legacy build of the copy ran 1.97 to 2.23 s, a median of 2.06 s in the
interleaved runs, so v2 takes 1.00 times legacy, and the two backends
are equally far behind. The comparison with C and Rust waits until after
M4.

## Compiler findings

Nothing new in v2.
