# 1301. Number of Paths with Max Score

You are given a square `board` of characters. You can move on the board
starting at the bottom right square marked with the character `'S'`.

You need to reach the top left square marked with the character `'E'`.
The rest of the squares are labeled either with a numeric character
`1, 2, ..., 9` or with an obstacle `'X'`. In one move you can go up,
left or up-left (diagonally) only if there is no obstacle there.

Return a list of two integers: the first integer is the maximum sum of
numeric characters you can collect, and the second is the number of such
paths that you can take to get that maximum sum, taken modulo `10^9 +
7`.

In case there is no path, return `[0, 0]`.

```
board = ["E23","2X2","12S"]  ->  [7,1]
board = ["E12","1X1","21S"]  ->  [4,2]
board = ["E11","XXX","11S"]  ->  [0,0]
```

**Constraints:** `2 <= board.length == board[i].length <= 100`.

The arms are `fn paths_with_max_score(board: Vec[String]) -> Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `paths_with_max_score.kara` ★ | a table from the bottom-right corner back, each square holding the most points any path from `'S'` collects reaching it and how many paths collect that many, from the best of the three squares a step below, to the right and both; a tie adds their counts. O(n^2) |
| `paths_with_max_score_forward.kara` | a path read backwards is a path from `'E'` down, right or down and right to `'S'` over the same squares, so the table is filled from the top-left corner instead. O(n^2) |
| `paths_with_max_score_memo.kara` | the best score and its count from `'S'` to a square, by recursion on the three squares a path can come from, each square worked out once and kept in a `Map` from its place. O(n^2), up to 2n calls deep |
| `paths_with_max_score_kahn.kara` | the squares as a graph whose edges are the moves, taken in an order where every square comes after all the squares that step into it (Kahn's algorithm, a `VecDeque` of squares with no moves left to come in), each passing its best score and count on to the squares it steps to. O(n^2) |
| `paths_with_max_score_solution.kara` | a Rust solution as LeetCode's Rust users write it (the board as `Vec<Vec<u8>>` from `as_bytes().to_vec()`, a `vec![vec![(-1i64, 0i64); n + 1]; n + 1]` table with a border row and column so that no step needs a bounds check, a `const MOD`, and the digit as `b[i][j] - b'0'`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, the
smallest board with both other squares obstacles, which the diagonal
move still crosses (`0,1`, a path worth 0, not `0,0`), and two paths that
tie (`7,1 4,2 0,0 0,1 5,2`); then 602 random boards, 600 of 2 to 30
squares a side with obstacles from 0 to 60 in 100, and two of 100 by 100,
the constraints' largest, one without obstacles (`602 random boards: 200
with no path, scores total 64284, checksum 305845443`).
`paths_with_max_score.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: every arm's harness writes a digit drawn as an `i64` with
`char.from_digit(d, 10)`, whose digit is a `u32`. `E0200` names the cast,
and `karac fix` writes it, `char.from_digit(d as u32, 10)` (1 fix in each
Kāra arm): that machine fix was added for an earlier draft of this kata,
lost since, whose harness met the refusal with no fix
(B-2026-11-21-59). Beyond that the four Kāra arms checked clean as
first written. The Rust arm takes one round of 23 fixes by `karac fix`'s
count, from 11 errors: `struct Solution;` to `struct Solution {}`,
`Vec<..>` to `Vec[..]`, `as_bytes()` to `bytes()`, `vec![vec![(-1i64,
0i64); n + 1]; n + 1]` to `Vec.filled(n + 1, Vec.filled(n + 1, (-1,
0)))`, `&&` and `||` to `and` and `or`, `for &(x, y) in &[..]` to `for
(x, y) in [..]`, `vec![..]` to `[..]`, `::` to `.`, the wrapper's `|&x|`
to `|x|`, and the harness's cast. Its `const MOD` inside the function
stays as written. Its output matches on the first run. No other gap was
met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every path from `'S'`, one move at a time up, left or up-left
onto any square that is not an obstacle, each digit stepped on added,
and at `'E'` the path's score compared with the best so far. 2000 boards
of 2 to 5 squares a side in four kinds, 500 each: no obstacles;
obstacles 30 in 100; only the digits 1 and 2, so that paths tie; and
obstacles 50 in 100. 198 have no path, and 518 have more than one best
path. Every board, obstacle and raised digit is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the board transposed: the same answer |
| P3 | the board turned half round, `'S'` and `'E'` put back in their corners: the same answer |
| P4 | one more obstacle: no better, a lower score or the same with no more paths |
| P5 | one digit raised by one: the best score the same or one more |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 boards: checksum 374737792,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Twelve edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out: the Rust arm
counting `'E'` as a digit and the same arm's start worth a point each
change the answer on exactly the boards that have a path, as the
memoized arm counting its start as two paths (M6) does, and fail the
same checks. The ten kept, two to each arm, are each killed, fail the
same way under both backends and not by a crash, and no two fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie keeping the later count alone | P1 518, P6 2072 |
| M2 | ★: no step up and left at once | P1 243, P6 972 |
| M3 | forward: obstacles walked over | P1 497, P6 497 |
| M4 | forward: each digit counted one short | P1 1757, P6 1757 |
| M5 | memoized: a square remembered under its mirror's place | P1 1317, P2 1326, P3 1376, P4 111, P6 1317 |
| M6 | memoized: the start counted as two paths | P1 1802, P6 1802 |
| M7 | topological: a square taken before its last move in | P1 1232, P2 653, P3 1132, P4 16, P5 270, P6 1232 |
| M8 | topological: a tie adding one path | P1 205, P2 143, P3 41, P4 4, P6 205 |
| M9 | solution: each square's count reset to one | P1 518, P6 518 |
| M10 | solution: the border taken for squares worth 0 with no paths | P1 189, P3 261, P6 189 |

P1 and P6 kill all ten, P3 four, P2 and P4 three each, and P5 one.
Transposing the board or turning it round keeps every path and its
score, and the edits that change the answer as a fixed function of the
paths (a count doubled, a digit short, a tie's count dropped) pass both,
as they pass P4 and P5. The ones that fail them depend on where a square
sits or when it is reached: the memo filed under the mirrored place
(M5), and the topological arm taking a square early (M7) or counting its
ties by arrival (M8). Turning the board also moves which squares touch
the Rust arm's border (M10). Only M7, which can add a square's digit
twice, ever gains more than one from a digit raised by one (P5).

## Benchmarks

The bench builds 20 boards of 100 by 100, the constraints' largest, with
obstacles from 0 to 38 in 100, once from its own generator, then makes
150 passes; each sets one square of every board to an obstacle or a
digit from the checksum so far, so no answer carries over, answers it
with the ★ arm and folds the score plus the pass, and the count, into the
checksum. The board is rows of text in every language, copied into a
grid of characters each call, and the tables are fresh each call. Every
implementation prints `150 passes over 20 boards of 100 by 100: checksum
352689701`.

BENCHTAB
