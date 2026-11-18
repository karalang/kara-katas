# 1197. Minimum Knight Moves

In an infinite chess board with coordinates from `-infinity` to
`+infinity`, you have a knight at square `[0, 0]`. A knight has 8
possible moves it can make: each move is two squares in a cardinal
direction, then one square in an orthogonal direction. Return the
minimum number of steps needed to move the knight to the square `[x,
y]`. It is guaranteed the answer exists.

```
x = 2, y = 1  ->  1     [0, 0] -> [2, 1]
x = 5, y = 5  ->  4     [0, 0] -> [2, 1] -> [4, 2] -> [3, 4] -> [5, 5]
```

**Constraints:** `-300 <= x, y <= 300`; `0 <= |x| + |y| <= 300`.

The arms are `fn min_knight_moves(x: i64, y: i64) -> i64`. The two Rust
arms keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a one-line `min_knight_moves` calls it.

## Approaches

| file | mechanism |
|---|---|
| `min_knight_moves.kara` ★ | a breadth-first search from the origin over a `VecDeque`. The board is symmetric under each reflection, so the target is folded into the first quadrant; a shortest path there never needs a square below -2 in either coordinate, and none past 302, so the squares seen fit a 305 x 305 `Vec[bool]` |
| `min_knight_moves_memo.kara` | a recursion with a `Map[(i64, i64), i64]` memo: a folded target is best reached through one of the two squares a knight move back towards the origin, `(x - 1, y - 2)` or `(x - 2, y - 1)`, folded again; the origin takes 0 moves and a square with `x + y = 2` takes 2 |
| `min_knight_moves_formula.kara` | in closed form: folded so that `x >= y >= 0`, with `d = x - y`, `d + 2 * ceil((y - d) / 3)` moves when `y > d` and `d - 2 * floor((d - y) / 4)` otherwise, with `(1, 0)` and `(2, 2)` the two exceptions. O(1) |
| `min_knight_moves_meet.kara` | a breadth-first search from both ends at once on the whole board, with no folding and no bound: a `Map` of the squares each end has reached, and the smaller frontier grown a level at a time until it reaches a square the other end has seen |
| `min_knight_moves_solution.kara` | a Rust solution as LeetCode's Rust users write it (folded with `abs`, then a level-at-a-time search over a `VecDeque`, the squares seen in a `HashSet`, none below -1), carried to Kāra by `karac fix` |
| `min_knight_moves_dfs.kara` | another Rust solution, the recursion with a memo (a nested `fn dfs` folding with `abs`, a `HashMap<(i32, i32), i32>` passed as `&mut`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 15 lines: LeetCode's two examples; the origin;
the squares next to it, `(1, 0)` (3 moves), `(1, 1)` (2) and `(2, 2)`
(4); `(-1, -2)`, a single move into the third quadrant; `(0, -1)` and
`(3, 0)` (3 each); the constraints' far corners, `(300, 0)` and `(0,
-300)` (150 each), `(150, 150)` and `(-150, 150)` (100 each), and `(1,
299)` (150); and 100 random targets with `|x| + |y| <= 300` (`100
random targets: 5744 moves, checksum 855265945`).
`min_knight_moves.py` mirrors the ★ arm and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the memo and formula arms check clean as written. The ★
and meet arms each take one fix: their move table was first written
with Rust's array type, `const MOVES: [(i64, i64); 8]`, and `karac fix`
rewrites it to `Array[(i64, i64), 8]`. The solution arm takes one round
of 14 fixes (among them the `use` dropped, `HashSet::new()` to
`Set.new()`, `&&` to `and`, `!` to `not`, `for &(dx, dy)` to `for (dx,
dy)`, `seen.contains(&(nx, ny))` to `seen.contains((nx, ny))`, and the
`as i64` on the widening call dropped), and the dfs arm one round of 18
(among them the nested `fn dfs` moved out to the top level, `&mut
HashMap<(i32, i32), i32>` to `mut ref Map[(i32, i32), i32]`, `if let
Some(&v) = memo.get(&(x, y))` to `if let Some(v) = memo.get((x,
y)).cloned()`, and `dfs(x, y, &mut HashMap::new())` to `dfs(x, y, mut
Map.new())`). Both outputs match. The kata found no gap.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search over every square of the board, with
no folding and no bound, a level at a time until the target is reached.
600 random targets with `|x| + |y| <= 30`, each sign at random, and for
each a random knight move.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | as many moves as `x + y`, mod 2, since each move changes `x + y` by 1 or 3 |
| P3 | the target turned a quarter, `(-y, x)`, takes as many |
| P4 | the target mirrored in the diagonal, `(y, x)`, takes as many |
| P5 | the square a knight move from the target takes one move more or one fewer |
| P6 | at least half the longer side, and a third of `|x| + |y|`, rounded up |
| P7 | the ★ arm's answer |

All 25,200 checks pass on every arm: `600 targets: checksum 662835952,
25200 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same targets, searching the whole board, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`. Ten are caught on both, S2 is caught under
`karac run` and runs past the 300 s limit under the interpreter, and X2
is caught on neither.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: no square below 0 searched | P1 9, P5 2, P7 45 |
| S2 | ★: `x` not folded | `karac run`: P1 210, P2 210, P3 257, P4 266, P5 224, P6 210, P7 1050; `__mir-run`: over 300 s |
| M1 | memo: a square with `x + y = 2` takes one move | P1 278, P2 278, P5 155, P7 278 |
| M2 | memo: the worse of the two squares back | P1 538, P5 159, P7 538 |
| F1 | formula: `(2, 2)` not an exception | P1 4, P7 4 |
| F2 | formula: a third rounded down | P1 77, P5 21, P6 77, P7 77 |
| B1 | meet: the near end's depth never grows | P1 530, P2 296, P5 287, P6 458, P7 530 |
| B2 | meet: a square found from the near end one move short | P1 305, P2 305, P5 584, P6 160, P7 305 |
| X1 | solution: no square below 0 searched | P1 9, P5 2, P7 9 |
| X2 | solution: the move `(-2, -1)` left out | none |
| D1 | dfs: the origin takes one move | P1 322, P2 322, P5 155, P7 322 |
| D2 | dfs: the worse of the two squares back | P1 538, P5 159, P7 538 |

A mutation of the ★ arm fails P7 on the other five arms as well as its
own P1. S1 and X1 are one fault, the search kept out of negative
squares, and fail on the 9 draws of `(±1, ±1)`: folded, `(1, 1)` is the
one square within `|x| + |y| <= 30` whose shortest path, two moves,
needs a negative square (checked by a Python copy of the arm). With `x` not folded (S2), a target with
`x < -2` lies off the searched grid, and every search for one runs
through all 93,025 squares before it gives up with `-1`; natively that
takes no time to speak of, and under the interpreter the run does not
finish. P3 and P4, the target turned and mirrored, catch only S2, the
one fault that breaks the board's symmetry. M2 and D2, the worse of the
two squares back, are one fault in two arms and fail alike.

X2 is caught on neither lane and may not be catchable: once the target
is folded into the first quadrant and no square below -1 is searched,
dropping the move `(-2, -1)`, two back and one down, changed no answer
on any target with `x + y <= 60` (checked by a Python copy of the arm
with and without the move) nor on the harness's 100 far targets. A
shortest path to a square in the first quadrant seems never to need a
move that brings both coordinates down; that was checked, not
proved.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 2000 random targets with `|x| + |y| <= 300`, the constraints'
range, drawn once, each answer folded into a checksum. Every program
prints `2000 targets: checksum 969797604`. Each call allocates the
305 x 305 grid of squares seen and a queue, C an array of `side * side`
entries, Rust a `VecDeque`, Go a slice grown by `append` from one
entry, and searches until the target is reached.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.426 to 0.501 s | 0.467 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.455 to 0.563 s | 0.462 s |
| Rust (`rustc -O`) | 0.274 to 0.385 s | 0.298 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.267 to 0.420 s | 0.277 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.265 to 0.324 s | 0.279 s |
| C (`clang -O3`) | 0.214 to 0.271 s | 0.219 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.215 to 0.286 s | 0.219 s |
| Go | 3.113 to 3.669 s | 3.338 s |
| Python | 41.47 to 42.04 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. C is about 2.1x faster than Kāra (0.219 s against 0.462 s), and
Rust with overflow checks on about 1.7x (0.277 s); both sit well outside
Kāra's range. No profile was taken, so where Kāra spends the difference
on this search is not yet known. Go takes about 7x Kāra's time, its
queue grown from one entry and its grid freed by the collector in every
call (inferred, not profiled). Python takes about 90x Kāra's time.
