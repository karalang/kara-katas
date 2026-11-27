# 1812. Determine Color of a Chessboard Square

You are given `coordinates`, a string that represents the coordinates of
a square of the chessboard, a letter from `a` to `h` for its file and a
digit from `1` to `8` for its rank. Return `true` if the square is
white, and `false` if the square is black. The coordinate will always
represent a valid chessboard square, and the letter comes first.

```
coordinates = "a1"  ->  false
coordinates = "h3"  ->  true
coordinates = "c7"  ->  false
```

**Constraints:** `coordinates.length == 2`, `'a' <= coordinates[0] <=
'h'` and `'1' <= coordinates[1] <= '8'`.

The arms are `fn square_is_white(coordinates: String) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `square_is_white.kara` ★ | a1 is black and the colours alternate along ranks and files, so a square is white exactly when its file and rank, counted from `a` and `1`, sum to an odd number, read off the name's two bytes. O(1) |
| `square_is_white_board.kara` | the board itself: an 8 by 8 `Vec[Vec[bool]]` filled square by square, each the opposite of the one before it in its rank and each rank starting opposite to the one below, and the square looked up by `find` on the files and `to_digit` on the rank. O(1), 64 squares built per call |
| `square_is_white_xor.kara` | the bytes' own parities: `a` is 97 and `1` is 49, both odd, so a square is white exactly when the low bits of its two bytes differ. O(1) |
| `square_is_white_match.kara` | by name: a square on the a, c, e or g file is white on an even rank, and one on the b, d, f or h file on an odd rank, read with `match` on the two chars. O(1) |
| `square_is_white_solution.kara` | a Rust solution as LeetCode's Rust users write it (`coordinates.as_bytes()`, `(c[0] - b'a' + c[1] - b'1') % 2 == 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 11 lines: LeetCode's three examples (`false
true false`); the other three corners and b1 beside a1 (`true true false
true`); the whole board, rank 8 at the top, `W` for a white square and
`B` for a black one, from `WBWBWBWB` to `BWBWBWBW`; and the count (`32
white squares`). `square_is_white.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, board and xor arms and the harness check clean as
first written. The match arm read the rank with Rust's `matches!(rank,
'2' | '4' | '6' | '8')`; Kāra has no macros, check says to write a
`match` with a `true` arm and a `_ => false` arm, and `karac fix` did, 3
fixes by its count. The Rust solution takes 10 fixes by `karac fix`'s
count, and its diff is: `struct Solution {}` added above the `impl`;
`coordinates.as_bytes()` to `coordinates.bytes()`; and `Solution::` to
`Solution.` in the harness. The `u8` arithmetic `c[0] - b'a' +
c[1] - b'1'` is Kāra as it stands, and cannot fall below 0, as
`c[0] - b'a'` is added to `c[1]` before `b'1'` is taken away. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a1 is black, and every step to a square beside it changes the
colour, so the square is reached from a1 a file and then a rank at a
time and the colour flipped at each step. It runs every one of the 64
squares. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every square beside it along a rank or a file has the other colour |
| P3 | its mirror across the board, the a file for the h, has the other colour |
| P4 | the board turned half round, a1 for h8, keeps its colour |
| P5 | its rank holds 4 white squares |
| P6 | the ★ arm's answer |

The differential's checksum was first written to double at each square,
which an `i64` cannot hold over 64 squares, and was changed before its
first run to multiply by 31 modulo `10^9 + 7`. It checks clean. All
1,920 checks pass on every arm: `64 cases: checksum 684980512, 1920
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`. Python, running the ★ arm's
mirror over the same squares, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the parity read the wrong way round | P1 64, P6 256 |
| M2 | ★: the rank halved | P1 32, P2 64, P6 128 |
| M3 | board: every rank started on the same colour | P1 32, P2 64, P4 64, P6 32 |
| M4 | board: a1 built white | P1 64, P6 64 |
| M5 | xor: the bytes' second bits compared, not their first | P1 32, P2 60, P3 64, P6 32 |
| M6 | xor: the file's byte read twice | P1 32, P2 64, P3 64, P5 64, P6 32 |
| M7 | match: the g file left with the b, d, f and h files | P1 8, P2 24, P3 16, P4 16, P5 64, P6 8 |
| M8 | match: rank 8 taken as odd | P1 8, P2 16, P4 16, P6 8 |
| M9 | solution: the rank counted from 0, not 1 | P1 64, P6 64 |
| M10 | solution: the rank left out | P1 32, P2 64, P4 64, P6 32 |

## Benchmarks

The bench builds the 64 square names once and makes `3 * 10^7` calls of
the ★ arm, each name drawn from the checksum so far. It checks clean as
first written. Every implementation prints `30000000 calls: checksum
447863378`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.35 s against Rust's 0.39 s (0.38 s with
overflow checks on), C's 0.33 s and Go's 0.41 s; Python takes 6.7 s.
