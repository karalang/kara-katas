# 999. Available Captures for Rook

You are given an `8 x 8` matrix representing a chessboard. There is
**exactly one** white rook represented by `'R'`, some number of white
bishops `'B'`, and some number of black pawns `'p'`. Empty squares are
represented by `'.'`.

A rook can move any number of squares horizontally or vertically (up,
down, left, right) until it reaches another piece or the edge of the
board. A rook is **attacking** a pawn if it can move to the pawn's
square in one move.

Note: A rook cannot move through other pieces, such as bishops or
pawns. This means a rook cannot attack a pawn if there is another piece
blocking the path.

Return *the number of pawns the white rook is **attacking***.

```
. . . . . . . .      . . . . . . . .      . . . . . . . .
. . . p . . . .      . p p p p p . .      . . . p . . . .
. . . R . . . p      . p p B p p . .      . . . p . . . .
. . . . . . . .      . p B R B p . .      p p . R . p B .
. . . . . . . .      . p p B p p . .      . . . . . . . .
. . . p . . . .      . p p p p p . .      . . . B . . . .
. . . . . . . .      . . . . . . . .      . . . p . . . .
. . . . . . . .      . . . . . . . .      . . . . . . . .
      ->  3                ->  0                ->  3
```

**Constraints:** `board.length == 8`; `board[i].length == 8`;
`board[i][j]` is `'R'`, `'.'`, `'B'`, or `'p'`; there is exactly one
cell with `board[i][j] == 'R'`.

## Approaches

The rook can reach only the nearest piece in each of its four
directions, so the answer is how many of those four, at most, are
pawns. Two arms walk out from the rook; three read its row and column
whole, and find the nearest pieces from the line itself.

| file | mechanism |
|---|---|
| `num_rook_captures.kara` ★ | a walk each way: from the rook, step up, down, left and right, a table of four directions, until a pawn, which counts, a bishop or the edge. O(1) on an 8 by 8 board |
| `num_rook_captures_scan.kara` | four loops: the rook's column read upwards and downwards and its row leftwards and rightwards, each by a loop of its own, and the first piece each meets counted when it is a pawn. O(1) |
| `num_rook_captures_nearest.kara` | the nearest pieces: each of the rook's two lines read from one end to the other, keeping the last piece before the rook and the first after it, and the pawns among those counted. O(1) |
| `num_rook_captures_strings.kara` | the pieces in a string: the rook's row and column made strings with the empty squares filtered out, and each `p` right beside the `R` counted. O(1) |
| `num_rook_captures_bits.kara` | bit masks: each line becomes a mask of its pieces and one of its pawns; the lowest set bit above the rook's place is the nearest piece one way, the highest below it the other, and a capture when it is also a pawn's. O(1) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines. The first ten are LeetCode's three
examples and seven more: the rook alone in a corner; the rook amid
pawns on every other square, in the middle and in a corner, where it
captures 4 and 2; pawns in the other three corners, two of them on the
rook's lines; a bishop shielding each pawn on its lines; four pawns
right beside the rook; and the rook amid bishops. Then the total over
the rook on each of the 64 squares of a board otherwise all pawns, 224.
Then totals over random boards, the rook on a random square and every
other square a pawn or a bishop at random: 300 boards with a pawn on 1
square in 16 and a bishop on 1, 3,000 with 3 and 2, and 3,000 with 6
and 4. `num_rook_captures.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every square holding a pawn is attacked when it is in
the rook's row or column and every square strictly between them is
empty, and the answer is how many are. It checks 3,200 random boards,
made as the arms' random boards are: 3,000 with a pawn on up to 8
squares in 16 and a bishop on up to 4, chosen at random for each
board, against the statement, and 200 with 10 and 3 against the other
properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 boards |
| P2 | the board transposed gives the same answer |
| P3 | the board turned upside down gives the same answer |
| P4 | a pawn put on a random empty square adds 0 or 1, and 1 only where the rook can move to that square |
| P5 | a bishop put on a random empty square takes off 0 or 1, and 1 only where the rook can move to that square |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 boards with 54715 pawns: 5330 captures, checksum
98049816, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (8.1 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-four edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a bishop does not stop the walk | P1 745, P4 60, P6 831 |
| M2 | ★: a pawn does not stop the walk | P1 1462, P4 173, P5 118, P6 1645 |
| M3 | ★: the bottom row off the board | P1 441, P2 847, P3 956, P6 485 |
| M4 | scan: bishops counted, not pawns | P1 2450, P4 69, P5 298, P6 2624 |
| M5 | scan: the bottom row never read | P1 213, P2 443, P3 451, P6 235 |
| M6 | scan: the leftward loop starts on the rook | P1 1205, P2 1268, P6 1337 |
| M7 | nearest: the first piece before the rook kept | P1 974, P3 1197, P4 69, P5 78, P6 1087 |
| M8 | nearest: the last piece after the rook kept | P1 593, P3 754, P4 32, P5 53, P6 664 |
| M9 | nearest: the rook read as a piece | P1 1757, P3 1402, P6 1935 |
| M10 | strings: a pawn first in the string not seen | P1 861, P3 868, P4 30, P5 28, P6 902 |
| M11 | strings: any piece after the rook counted | P1 1073, P3 1037, P5 105, P6 1137 |
| M12 | strings: bishops filtered out of the row, not empty squares | P1 1112, P2 1461, P4 11, P5 21, P6 1180 |
| M13 | bits: the lowest bit below the rook, not the highest | P1 410, P3 501, P4 31, P6 463 |
| M14 | bits: bishops in the row's pawn mask | P1 2256, P2 2091, P4 34, P5 170, P6 2404 |
| M15 | bits: the rook in the mask below it | P1 1800, P3 1402, P6 1982 |

P1 and P6 kill all fifteen, P3 and P4 nine each, P5 eight and P2 five.
A transposed board swaps the rook's row with its column, so P2 sees
only the edits that treat the two differently: M3 and M5, which lose
the bottom row but not the right-hand column; M6, which goes wrong to
the left but not upwards; and M12 and M14, which spoil the row alone.
Turned upside down, a board swaps up with down, and so P3 sees the
edits that treat one end of a line unlike the other in both lines
alike: the nearest pieces kept wrongly before or after the rook (M7,
M8, M13), a pawn missed or a bishop counted on one side (M10, M11),
and M9 and M15, which never reach past the rook on one side, M9 the
side after it and M15 the side before. Those two fail on the same
1,402 boards, those whose column has a capture on one side of the rook
and not the other. P4 sees the edits whose count can rise for a pawn
the rook cannot move to, such as one beyond a bishop (M1) or beyond
another pawn (M2), and P5 those whose count can drop for a bishop
where the rook cannot reach, or rise for one, as M4's does, since it
counts bishops. M9 and M15 count one side of each line, and that side
rightly, so a pawn or a bishop added changes their count only as P4
and P5 allow.

Nine other edits were tried and set aside. One failed exactly the same
checks as a kept one: bits putting the rook in the mask above it,
which leaves it blind to everything after the rook, as M9. Seven were
sound but beyond three an arm: ★ walking left twice and never right;
scan's upward loop never stopping; nearest reading the column from the
row, and reading it at the rook's column; strings reading the column
from the row, and counting the row twice, which fail the same checks;
and bits reading the column's pieces from the row. One survived and is
equivalent: ★ starting each walk on the rook's own square, which holds
neither a pawn nor a bishop, so the walk steps past it. None crashed.

## Verification

Every arm prints the same output as `num_rook_captures.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 1.6 s (scan) to 2.1 s (strings,
which builds two strings for every board), and the differential 8.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
random boards once, the rook on a random square and every other square
a pawn 4 times in 16 and a bishop 2 times in 16. In each of 500,000
rounds it runs the arm on every board, each round starting from a
different one, folds every count into a checksum, and then puts a pawn
on, or takes one off, one square of that board, a different square
each time, so that no board stays the same from call to call. Every
implementation prints `500000 rounds over 20 boards: 18237326
captures, checksum 443917126`. Each call reads all 64 squares to find
the rook and then walks out from it. Each board is in LeetCode's shape
for its language: `char **` in C, `Vec<Vec<char>>` in Rust, `[][]byte`
in Go, and a `Vec[Vec[char]]` in Kāra.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.433 to 0.490 s | 0.458 s |
| Rust (`rustc -O`) | 0.512 to 0.592 s | 0.546 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.525 to 0.628 s | 0.563 s |
| Go | 1.323 to 1.775 s | 1.408 s |
| Python | 48.3 s | |
| Kāra (`karac build --mir`) | 0.609 to 0.718 s | 0.651 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 74 times
Kāra's.

v2 took 1.16 times Rust's median time under overflow checks and 1.42
times C's. Under valgrind's cachegrind v2 ran 5,508 million
instructions and 921 million branches with 69.4 million mispredicted,
Rust with overflow checks 5,445 million, 560 million and 52.4 million,
and C 2,998 million, 254 million and 48.0 million. Over the 10 million
calls that is about 92 branches a call for v2, 56 for Rust and 25 for
C, and about 2 more mispredicts a call for v2 than for Rust; where its
extra branches are was not traced. The mispredicts the three share fit
the walks, whose length is as random as the boards (inferred).
