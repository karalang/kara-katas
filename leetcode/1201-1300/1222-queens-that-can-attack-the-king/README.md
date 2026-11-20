# 1222. Queens That Can Attack the King

On a **0-indexed** `8 x 8` chessboard, there can be multiple black queens
and one white king.

You are given a 2D integer array `queens` where `queens[i] = [xQueen_i,
yQueen_i]` represents the position of the `i`th black queen on the
chessboard. You are also given an integer array `king` of length `2` where
`king = [xKing, yKing]` represents the position of the white king.

Return the coordinates of the black queens that can directly attack the
king. You may return the answer in **any order**.

```
queens = [[0,1],[1,0],[4,0],[0,4],[3,3],[2,4]], king = [0,0]
    ->  [[0,1],[1,0],[3,3]]     [0,4] is hidden by [0,1], [4,0] by [1,0]
queens = [[0,0],[1,1],[2,2],[3,4],[3,5],[4,4],[4,5]], king = [3,3]
    ->  [[2,2],[3,4],[4,4]]
```

**Constraints:** `1 <= queens.length < 64`; `queens[i].length ==
king.length == 2`; `0 <= xQueen_i, yQueen_i, xKing, yKing < 8`; all the
given positions are **unique**.

The arms are `fn queens_attackthe_king(queens: Vec[Vec[i64]], king:
Vec[i64]) -> Vec[Vec[i64]]`. The Rust arm keeps the method LeetCode gives
Rust users, on `i32`, inside `impl Solution`, and a short
`queens_attackthe_king` converts to and from it. Since the answer may come
in any order, every harness sorts it before printing.

## Approaches

| file | mechanism |
|---|---|
| `queens_that_can_attack_the_king.kara` ★ | mark the queens on an 8 by 8 board of `bool`s, then walk out from the king in each of the eight directions, `dx` and `dy` each from −1 to 1; the first queen met in each attacks and hides any behind her. O(64) |
| `queens_that_can_attack_the_king_set.kara` | the queens in a `Set[(i64, i64)]`, the eight directions a list of pairs, each walked from the king until it leaves the board or finds a queen |
| `queens_that_can_attack_the_king_nearest.kara` | from the queens' side: a queen in line with the king lies in one of eight directions, the signs of her offsets, at a distance, the larger offset; the nearest in each direction is kept in a `Map` from direction to distance and square. O(queens) |
| `queens_that_can_attack_the_king_closest.kara` | the queens sorted by distance from the king (`sort_by_key` through a closure that captures the king), then the first queen in line in each direction is an attacker, and the direction is closed in an `Array[bool, 9]`. O(queens log queens) |
| `queens_that_can_attack_the_king_board.kara` | a Rust solution as LeetCode's Rust users write it (a `[[bool; 8]; 8]` board indexed by `as usize`, a `dirs` list of eight `(dx, dy)` pairs, `for &(dx, dy) in dirs.iter()`, `vec![x, y]` pushed), carried to Kāra by `karac fix` |
| `queens_that_can_attack_the_king_iter.kara` | a second Rust solution, LeetCode's iterator form: the queens in a `HashSet<(i32, i32)>`, the directions by `flat_map` over two `-1..=1` ranges, and each direction's attacker by `(1..8).map(..).take_while(..).find(..)` inside a `filter_map`, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's two examples and a board
where no queen is in line (`[]`), the total and a checksum of the
attackers on 1000 random boards of 1 to 63 queens (`4917`, `909168263`),
and the attackers of a king on every other square of the board, from a
corner (3), the middle (8) and an edge (5).
`queens_that_can_attack_the_king.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, nearest and closest arms check clean. The set arm
was first written with Rust's `let (mut x, mut y) = ..`, and the
diagnostic's fix made it `let mut (x, y) = ..`. The board arm takes one
round of 22 fixes (among them `Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `for q
in &queens` to `for q in ref queens`, `vec![]` to an annotated
`Vec.new()`, `&(dx, dy)` to `(dx, dy)`, `let (mut x, mut y)` to `let mut
(x, y)`, `&&` to `and`, `vec![x, y]` to `[x, y]`) and checks clean. Two
of them are the suffixes `(-1i32, -1i32)` on the `dirs` list, which
before B-2026-11-19-26 it did not get (see below).

The iterator arm, a second Rust solution, takes one round of 24 fixes
and checks clean: among them `HashSet<(i32, i32)>` to `Set[(i32, i32)]`,
`move |dy|` to `|dy|`, `|&(dx, dy)|` to `|(dx, dy)|`, `||` and `&&` to
`or` and `and`, `contains(&x)` to `contains(x)`, `vec![x, y]` to `[x, y]`,
and the suffixes `-1i32..=1`, `-1i32..=1` and `1i32..8` on its three
ranges. Those three it did not get before B-2026-11-19-29: it stopped
at two errors with no fix, and the arm waited on that row.

## Gaps

Two, in the fixes `karac fix` offers when an unsuffixed literal keeps the
default `i64` beside an `i32` (design.md §8 Literals).

- B-2026-11-19-26, fixed in kara at cc3372dd0f: the board arm's `dirs` list of
  tuple literals, bound by a `let` and walked by `for (dx, dy) in
  dirs.iter()`, then `let mut (x, y) = (king[0] + dx, king[1] + dy)` and
  `ans.push([x, y])` into a `Vec[Vec[i32]]`, was refused twice with no
  fix. Rust infers `i32` for the list from the king. The suffix the same
  loop over an inline list already got now reaches through the `let`, the
  `.iter()` and the tuple `let`, so the fix writes `(-1i32, -1i32)`, which
  types every tuple.
- B-2026-11-19-29, fixed in kara at b46168e5c8: in the iterator form the three ranges' literals reached
  `kx + k * dx` through closure parameters, so each square was an `(i64,
  i64)`, and `placed.contains(p)` and the final `collect()` were refused
  with no fix. The fix now suffixes the three ranges (`-1i32..=1`,
  `-1i32..=1`, `1i32..8`), and the arm checks clean and prints the
  kata's output.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a queen attacks when she shares the king's row, column or a
diagonal and no other queen stands on a square strictly between them,
each queen tested against every other. 2000 boards, a third with 1 to 8
queens, a third with 9 to 32 and a third with 33 to 63.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every attacker a queen, none twice |
| P3 | at most one in each of the eight directions |
| P4 | the board mirrored top to bottom gives the mirrored attackers |
| P5 | the board turned across its diagonal gives the turned attackers |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 cases: checksum 148142890,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's attackers
for the same boards give the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the walk goes on past the first queen | P1 1367, P3 1367, P6 6835 |
| S2 | ★: the diagonals only | P1 1723, P6 8615 |
| T1 | set: the last row off the board | P1 475, P4 978, P5 793, P6 475 |
| T2 | set: no walk down and to the right | P1 889, P4 1222, P6 889 |
| N1 | nearest: the farthest queen kept | P1 1367, P6 1367 |
| N2 | nearest: a knight's move counted in line | P1 823, P4 256, P5 272, P6 823 |
| C1 | closest: the farthest first | P1 1367, P6 1367 |
| C2 | closest: left and right one direction | P1 860, P4 381, P5 1162, P6 860 |
| B1 | board: the board marked across its diagonal | P1 1765, P2 1525, P4 1856, P6 1765 |
| B2 | board: no walk to the right | P1 1097, P5 1452, P6 1097 |
| I1 | iterator: the square next to the king skipped | P1 1501, P6 1501 |
| I2 | iterator: the last row off the board | P1 475, P4 978, P5 793, P6 475 |

All twelve are caught. A mutation of the ★ arm fails P6 on the five other
arms, and P1 catches every mutation. S1, N1 and C1 each return a queen
that another hides, on the same 1367 boards that have one: S1 returns
both, so it also fails P3, one direction twice; N1 and C1 return the far
queen in place of the near one, still one per direction and as symmetric
as the right answer, so only P1 and P6 see them. S2, which keeps the
diagonals only, is symmetric too. P2 catches B1 alone, whose board marks
squares no queen stands on. The two turns catch what breaks a symmetry:
P4 (top to bottom) catches T1 and I2, whose walks stop a row short at
the bottom, on the very same boards, and T2, whose missing down-and-right walk becomes up-and-right;
P5 (across the diagonal) catches T1, I2 and B2, whose missing walk to the
right becomes a walk down, and misses T2, whose diagonal it keeps. N2
and C2 fail the turns only where two queens tie: a knight's move at the
same distance as a queen in line (N2), or the queens to the left and the
right of the king at one distance (C2). Which one is kept depends on the
order of the queens, and a turned board lists them in another. I1,
which skips the square next to the king, misses a queen there and finds
the one behind her, or none, and that is as symmetric as the right
answer, so only P1 and P6 see it.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, mark the queens on an 8 by 8 board, then walk out from the king in
each of the eight directions, over 5000 random boards of 1 to 63 queens
drawn once, 200 passes; checksum of the attackers in the order found.
Every program prints `5000 boards of 1 to 63 queens, 200 passes:
attackers total 4848800, checksum 921105425`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.290 to 0.370 s | 0.320 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.303 to 0.407 s | 0.321 s |
| Rust (`rustc -O`) | 0.309 to 0.384 s | 0.341 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.325 to 0.399 s | 0.348 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.313 to 0.434 s | 0.347 s |
| C (`clang -O3`) | 0.113 to 0.155 s | 0.123 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.116 to 0.169 s | 0.122 s |
| Go | 0.546 to 0.641 s | 0.590 s |
| Python | 5.538 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 8% ahead of Rust with overflow checks on (0.321 s
against 0.348 s), and the two ranges overlap. Kāra takes about 2.6x C's
time (0.321 s against 0.123 s); Go takes about 1.8x Kāra's time. Python
takes about 17x Kāra's time. No profile was taken.
