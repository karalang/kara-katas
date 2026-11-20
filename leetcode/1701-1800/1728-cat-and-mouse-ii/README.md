# 1728. Cat and Mouse II

A game is played by a cat and a mouse named Cat and Mouse. The
environment is represented by a `grid` of size `rows x cols`, where each
element is a wall, floor, player (Cat, Mouse), or food.

- Players are represented by the characters `'C'` (Cat) and `'M'`
  (Mouse).
- Floors are represented by the character `'.'` and can be walked on.
- Walls are represented by the character `'#'` and cannot be walked on.
- Food is represented by the character `'F'` and can be walked on.
- There is only one of each character `'C'`, `'M'`, and `'F'` in `grid`.

Mouse and Cat play according to the following rules:

- Mouse **moves first**, then they take turns to move.
- During each turn, Cat and Mouse can jump in one of the four directions
  (left, right, up, down). They cannot jump over the wall nor outside of
  the `grid`.
- `catJump, mouseJump` are the maximum lengths Cat and Mouse can jump at
  a time, respectively. Cat and Mouse can jump less than the maximum
  length.
- Staying in the same position is allowed.
- Mouse can jump over Cat.

The game can end in 4 ways:

- If Cat occupies the same position as Mouse, Cat wins.
- If Cat reaches the food first, Cat wins.
- If Mouse reaches the food first, Mouse wins.
- If Mouse cannot get to the food within 1000 turns, Cat wins.

Given a `rows x cols` matrix `grid` and two integers `catJump` and
`mouseJump`, return `true` *if Mouse can win the game if both Cat and
Mouse play optimally, otherwise return* `false`.

```
grid = ["####F","#C...","M...."], catJump = 1, mouseJump = 2   ->  true
grid = ["M.C...F"], catJump = 1, mouseJump = 4                 ->  true
grid = ["M.C...F"], catJump = 1, mouseJump = 3                 ->  false
```

**Constraints:** `rows == grid.length`; `cols = grid[i].length`;
`1 <= rows, cols <= 8`; `grid[i][j]` consists only of `'C'`, `'M'`,
`'F'`, `'.'`, and `'#'`; one each of `'C'`, `'M'` and `'F'`;
`1 <= catJump, mouseJump <= 8`.

## Approaches

| file | mechanism |
|---|---|
| `mouse.kara` ★ | the game solved backwards from its ends: a state is the mouse's cell, the cat's cell and whose move; the ends are known from the cells, and working back, a state with a move into the mover's win is won, and one whose moves, counted down, all go to the other's win is lost. What is never decided is a draw, which the turn limit gives to the cat. O(cells^2 (rows + cols)) |
| `mouse_rounds.kara` | the mouse's wins grown round by round: starting from the mouse on the food, each sweep adds a mouse-to-move state with some move into the set and a cat-to-move state with every move into it, until a round adds nothing |
| `mouse_turns.kara` | the statement's limit as it stands: the table of who wins from each pair of cells after t moves, built back from the thousandth move, each from the one after it; once the tables two moves apart agree every earlier one is the same, and the walk stops |
| `mouse_solution.kara` | a Rust solution as LeetCode's Rust users write it, a search from the start with a memo on (turn, mouse, cat) as `vec![vec![vec![-1i8; ..]; ..]; limit + 1]`, the turns cut at twice the open cells, a labelled `'outer` loop over the directions, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, a mouse
beside the food with the cat beside it too, and a cat between the mouse
and the food in a corridor; then the mouse's wins and a checksum for
3000 random grids of up to 3 by 3 with jumps up to 3, 300 of up to 5 by
5 with jumps up to 5, and 20 of up to 8 by 8 with jumps up to 8, a wall
in each cell with a chance of 1 in 4. `mouse.py` mirrors the ★ arm and
its output is byte-identical.

```
true
true
false
true
false
3000 grids of up to 3 by 3: the mouse wins 2225, checksum 523589565
300 grids of up to 5 by 5: the mouse wins 195, checksum 566429022
20 grids of up to 8 by 8: the mouse wins 12, checksum 141123751
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the game played back from its thousandth move, all 1000 of
them, the mouse's and the cat's in turn, each move up to the player's
jump in one of four directions or none, the ends as the statement lists
them, and a mouse not on the food after the 1000th move lost. It checks
3000 random problems: a grid of 1 to 3 rows and columns, at least three
cells, a wall in each with a chance of 1 in 4, the three marks on
different cells, and jumps of 1 to 3. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid mirrored left to right gives the same answer |
| P3 | the grid turned upside down gives the same answer |
| P4 | the grid transposed, rows made columns, gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 523589565, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. Its cases are
drawn the same way as the first batch the arms print, so the checksums
match. A Python reading of the statement, the same walk back from the
1000th move, stopped once the tables two moves apart agree since each
table is a function of the one after it, gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Three first edits were replaced. An
M2 that dropped `c == food` from the ★ arm's ends was equivalent: a cat
on the food can stay there, and the mouse that cannot reach it loses
anyway. An M7 that stopped the turns arm when one table matched the
next, not the one two moves on, ran the interpreter past its step limit.
An M10 that started the solution's jumps at 1, so that no player stays
put, changed no answer on these grids. M4 and M7 both let the cat take
any move that loses, and fail the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a mouse win taken as the cat's when the cat moved into it | P1 109, P5 109 |
| M2 | ★: the cat given one move fewer to lose before its state is lost | P1 3, P5 3 |
| M3 | ★: a cell's moves without staying where it is | P1 3, P5 3 |
| M4 | rounds: the cat's state won by the mouse if any move is, not every move | P1 496, P5 496 |
| M5 | rounds: the mouse on the food with the cat to move counted lost | P1 2225, P5 2225 |
| M6 | turns: the game cut at 2 moves, not 1000 | P1 109, P5 109 |
| M7 | turns: the cat's state won by the mouse if any move is, not every move | P1 496, P5 496 |
| M8 | turns: the fourth direction right again, not up | P1 770, P3 1513, P4 1171, P5 770 |
| M9 | solution: the cat that reaches the food not winning there | P1 343, P5 343 |
| M10 | solution: a jump carried on past a wall | P1 36, P5 36 |

## Benchmarks

The bench draws 200 random 8 by 8 grids, LeetCode's largest, a wall in
each cell with a chance of 1 in 4, with jumps of 1 to 8, all of them
first, then answers each 20 times by the ★ arm in all five languages.
Every implementation prints `200 grids of 8 by 8, 20 rounds: the mouse
wins 1700, checksum 103979563`. Each answer lists every cell's moves,
sets up 8192 states and walks back from the ends; Kāra, Rust and Python
keep a deque, Go a slice it appends to and C an array, each state pushed
at most once. The C build also runs clean under gcc's AddressSanitizer
and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.414 s |
| Rust (`rustc -O`) | 0.514 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.591 s |
| Kāra (`karac build`) | 0.628 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.632 s |
| Go | 0.829 s |
| Python | 18 s |

The sequential Kāra build takes 1.23x Rust's time and 1.07x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.414 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.594 s and 0.602 s on one
run).

## Verification

All four arms print the same output as `mouse.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The turns arm checked clean as first written.

The ★ arm first wrote `let (mut mouse, mut cat, mut food) = (0, 0, 0);`
as Rust has it; the parser's E0001 says that `mut` goes before the whole
pattern, and `karac fix` wrote `let mut (mouse, cat, food) = ...`. The
rounds arm first wrote its pair of flags `[bool; 2]`, Rust's array type;
E0001 named it and the fix wrote `Array[bool, 2]`.

LeetCode's Rust template took one `karac fix` of 52 edits:
`struct Solution {}` added; `Vec<..>` written `Vec[..]`; `&Vec<..>` and
`&mut Vec<..>` parameters written `Vec[..]` and `mut ref Vec[..]`, and
the `&g` and `&mut memo` arguments `g` and `mut memo`; every `usize`
written `i64`, with the casts to and from it dropped;
`s.as_bytes().to_vec()` written `s.bytes().to_vec()`; the
`vec![vec![vec![-1i8; n]; n]; limit + 1]` memo written as three nested
`Vec.filled`; `Self::dfs` written `Solution.dfs`; `&&`, `||` and `!`
written `and`, `or` and `not`; and `&(dr, dc)` written `(dr, dc)`. The
labelled `'outer` loop with its `break 'outer`, `0..=jump`, and the byte
literals `b'F'` and `b'#'` carried over as written.

It first took 58. `mouse`, `cat` and `floors` start as plain `0`, and
in the round where they first met the template's `usize` parameters, the
fix both declared them `: usize` and rewrote those parameters to `i64`;
the next round turned the declarations to `: i64`, which the literal's
default already is, six edits for nothing. Since kara `93fd9b2078` (B-2026-11-20-49) a
round that rewrites the `usize`s offers no declaration for a literal
that meets one, and the three stay `let mut mouse = 0;` and so on.

The differential's literal reading first gave a closure a return type,
`|at: i64, jump: i32| -> Vec[i64] { .. }`; E0001 says a closure does not
declare one, and it was dropped in the generator's source.
`arm_name` in it indexes a list of string literals for a `Str`, as
#1662's does (B-2026-11-19-131).
