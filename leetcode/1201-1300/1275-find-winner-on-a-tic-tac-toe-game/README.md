# 1275. Find Winner on a Tic Tac Toe Game

Tic-tac-toe is played by two players `A` and `B` on a `3 x 3` grid. The
rules of Tic-Tac-Toe are:

- Players take turns placing characters into empty squares `' '`.
- The first player `A` always places `'X'` characters, while the second
  player `B` always places `'O'` characters.
- `'X'` and `'O'` characters are always placed into empty squares, never
  on filled ones.
- The game ends when there are three of the same (non-empty) character
  filling any row, column, or diagonal.
- The game also ends if all squares are non-empty.
- No more moves can be played if the game is over.

Given a 2D integer array `moves` where `moves[i] = [rowi, coli]`
indicates that the `ith` move will be played on `grid[rowi][coli]`,
return the winner of the game if it exists (`A` or `B`). In case the game
ends in a draw return `"Draw"`. If there are still movements to play
return `"Pending"`.

You can assume that `moves` is valid (i.e., it follows the rules of
Tic-Tac-Toe), the grid is initially empty, and `A` will play first.

```
moves = [[0,0],[2,0],[1,1],[2,1],[2,2]]                          ->  "A"
moves = [[0,0],[1,1],[0,1],[0,2],[1,0],[2,0]]                    ->  "B"
moves = [[0,0],[1,1],[2,0],[1,0],[1,2],[2,1],[0,1],[0,2],[2,2]]  ->  "Draw"
```

**Constraints:** `1 <= moves.length <= 9`; `moves[i].length == 2`; `0 <=
rowi, coli <= 2`; there are no repeated elements on `moves`; `moves`
follow the rules of tic tac toe.

The arms are `fn tictactoe(moves: Vec[Vec[i64]]) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `tictactoe.kara` ★ | by line sums: each row, column and the two diagonals keep a running sum, A's moves adding 1 and B's taking 1 away, and the move that brings a sum to 3 or -3 wins at once. O(moves) |
| `tictactoe_board.kara` | by a board of characters: the nine squares a `Vec[char]`, `X` and `O` written in turn, each of the eight lines read off into a `String` by `collect`, and a line spelling `XXX` or `OOO` a win |
| `tictactoe_bits.kara` | by bit masks: each player's squares a 9-bit mask, and a player has won when one of the eight lines' masks, a `const` `Array`, lies wholly inside theirs |
| `tictactoe_enum.kara` | by an enum: the board nine `Option[Player]`s, the lines triples of squares, and the winner the first line whose three squares `match` one player, found by `find_map` |
| `tictactoe_last.kara` | by the last mover: a game stops at its first line, so only the player who moved last can have one; their squares go into a `Set` of pairs, and the rows, columns and diagonals are checked against it |
| `tictactoe_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Vec<Vec<i32>>`, the eight lines' sums in one `[0i32; 8]`, `as usize` indices, `"A".to_string()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples (`A B
Draw`); every position of every game, each game carried on from a
position while the arm answers `"Pending"` (`549945 positions: A 131184, B
77904, Draw 46080, Pending 294777, checksum 970685987`), which are the
known counts of tic-tac-toe's 255,168 games; and 3000 random games, each
cut short at a random move (`3000 random games: A 503, B 244, Draw 52,
Pending 2201, checksum 241079600`). `tictactoe.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, board and last-mover arms checked clean as first
written. The bit-mask arm returned the name from `for (player, name) in
[(0, "A"), (1, "B")]`, and a string literal is a `String` by default, so
the bare `for` element borrows it; the check said so
(`borrow_projection_copy`), and `karac fix` wrote `name.clone()`. The enum
arm's `match (board[a], board[b], board[c])` read `Option[Player]`s out of
the board by value, E0515 at each, and `karac fix` added `#[derive(Copy,
Clone)]` to `Player`. The solution arm takes one round of 16 fixes by
`karac fix`'s count: `Vec<..>` to brackets, `for &s` to `for s`, the
closure's `|&x|` to `|x|`, `&Vec<..>` to a plain borrowed parameter,
`struct Solution;` to `struct Solution {}`, `::` to `.`, and each
`"..".to_string()` to the bare literal, which a `String` result takes as it
is. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `X` and `O` written in turn on an empty grid, and each of the
eight lines found by asking every square whether it lies on that row,
column or diagonal; three of one character on a line is that player's
win, a full grid without one a draw, and anything else pending. 2000
random games, each played until it ends or is cut short at a random move.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a draw has 9 moves, a pending game fewer, and a win at least 5 |
| P3 | the board turned a quarter, the same answer |
| P4 | the board mirrored left to right, the same answer |
| P5 | each player's moves shuffled among that player's own turns, the same answer |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 games: checksum 860088121,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the anti-diagonal never counted | P1 78, P3 160, P4 160, P6 390 |
| S2 | ★: a game of 8 moves a draw | P1 83, P2 83, P6 415 |
| B1 | board: the anti-diagonal read through the wrong square | P1 98, P3 201, P4 184, P6 98 |
| B2 | board: B's line never seen | P1 190, P6 190 |
| T1 | bits: the diagonal's mask missing a corner | P1 162, P2 21, P3 234, P4 237, P6 162 |
| T2 | bits: any square of a line taken as the line | P1 1660, P2 871, P6 1660 |
| E1 | enum: the anti-diagonal ending in the wrong corner | P1 101, P3 198, P4 205, P6 101 |
| E2 | enum: two of B's squares on a line a win | P1 398, P2 50, P3 352, P4 341, P6 398 |
| L1 | last: the other player's squares checked | P1 530, P6 530 |
| L2 | last: the columns not checked | P1 176, P3 363, P6 176 |
| O1 | solution: a move's column counted as its row | P1 176, P3 363, P6 176 |
| O2 | solution: the centre left off the anti-diagonal | P1 78, P3 160, P4 160, P6 78 |

All twelve are caught, every one by P1, the statement read literally.
P3, the board turned, and P4, mirrored, see the edits that treat one line
unlike its images: P4 maps columns to columns, so it misses the two that
lose the columns (L2 and O1), which P3 turns into rows. The two that treat
A and B unlike each other (B2, L1) are seen by P1 alone. P2 sees a win
claimed too early, by a mask too loose (T1, T2) or a line of two (E2).
P5, each player's moves shuffled, catches none: every edit still answers
from the final position, which the shuffle keeps.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (line sums) asked about every position of every game of tic-tac-toe,
549,945 of them, each game carried on while the answer is "Pending"; 40
rounds, every answer folded into a checksum. Every program prints `40
rounds of every game: checksum 97559836`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 3.693 to 3.852 s | 3.772 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 3.694 to 3.825 s | 3.747 s |
| Rust (`rustc -O`) | 3.056 to 3.257 s | 3.123 s |
| Rust (`rustc -O -C overflow-checks=on`) | 4.307 to 4.459 s | 4.397 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 4.100 to 4.298 s | 4.214 s |
| C (`clang -O3`) | 1.931 to 2.020 s | 1.985 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.944 to 2.094 s | 1.989 s |
| Go | 2.795 to 3.084 s | 2.920 s |
| Python | 106.74 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 15% ahead of Rust with overflow checks on (3.747 s
against 4.397 s). Kāra takes about 1.9x C's time (3.747 s against 1.985
s); Go is about 22% ahead of Kāra (2.920 s against 3.747 s). Python
takes about 28x Kāra's time. No profile was taken.
