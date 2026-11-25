# 1391. Check if There is a Valid Path in a Grid

You are given an `m x n` `grid`. Each cell of `grid` represents a
street. The street of `grid[i][j]` can be:

| street | connects |
|---|---|
| `1` | the left cell and the right cell |
| `2` | the upper cell and the lower cell |
| `3` | the left cell and the lower cell |
| `4` | the right cell and the lower cell |
| `5` | the left cell and the upper cell |
| `6` | the right cell and the upper cell |

You will initially start at the street of the upper-left cell `(0, 0)`.
A valid path in the grid is a path that starts from the upper left cell
`(0, 0)` and ends at the bottom-right cell `(m - 1, n - 1)`. The path
should only follow the streets.

Notice that you are not allowed to change any street.

Return `true` if there is a valid path in the grid or `false` otherwise.

```
grid = [[2,4,3],[6,5,2]]               ->  true
grid = [[1,2,1],[1,2,1]]               ->  false
grid = [[1,1,2]]                       ->  false
grid = [[1,1,1,1,1,1,3]]               ->  true
grid = [[2],[2],[2],[2],[2],[2],[6]]   ->  true
```

**Constraints:** `1 <= m, n <= 300` and `1 <= grid[i][j] <= 6`.

Each arm is `fn has_valid_path(grid: Vec[Vec[i32]]) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `has_valid_path.kara` ★ | a breadth-first search from the top-left cell over a `VecDeque`, each street's two openings looked up in a table of (row step, column step) pairs, and a neighbour entered only when its own street's openings `contains` the step back. O(m n) |
| `has_valid_path_stack.kara` | a depth-first search with a `Vec` for its stack and a `Set` of the cells reached, whose `insert` says whether a cell is new; whether a street opens towards a step is a `match` on the step. O(m n) |
| `has_valid_path_union.kara` | union-find, a `struct` with `mut ref self` methods, path halving and union by size: each cell joined to its right and its lower neighbour when the two streets open towards each other, and the corners asked whether they share a root. O(m n α(m n)) |
| `has_valid_path_follow.kara` | the path followed: every street has exactly two openings, so the cells a walk can reach from the top-left form one chain. Each opening of the first cell is tried in turn, and the chain walked, each cell left by the opening it did not come in by, with the openings as bits, until it leaves the grid, meets a street that does not open back, comes round to the start, or reaches the corner. O(m n) |
| `has_valid_path_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `[[(i32, i32); 2]; 7]` table of openings, `vec![vec![false; n]; m]`, a stack of `(0usize, 0usize)`, and `.any(\|&(x, y)\| ..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's five examples, a loop of
four streets that reaches the corner, a loop that turns back short of
it, and one cell (`true false false true true true false true`); the
constraints' most, six 300 by 300 grids of random streets with a path
planted from corner to corner, every other one then broken at one cell
of its path (`300 by 300, planted, every other one broken: true false
true false true false`); and 2000 random grids of 1 to 12 by 1 to 12,
planted the same way (`2000 random grids: 1264 with a path, checksum
323444262`). `has_valid_path.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, stack and follow arms check clean as first
written, the harness aside, whose
`shown.iter().map(..).collect::[Vec[String]]().join(" ")` is refused as
a turbofish; `karac fix` names the collection before the call,
`Vec[String].from_iter(shown.iter().map(..)).join(" ")`. The union arm,
written with Rust's `self: mut ref Joins` receivers, takes 3 fixes by
`karac fix`'s count: each receiver becomes `mut ref self`, and the swap
`(a, b) = (b, a)`, refused once the receivers parse, since a
parenthesized tuple is a value and not a place, becomes `a, b = b, a`.
The Rust solution takes one round of 25 fixes by `karac fix`'s count,
from 12 errors: `struct Solution;` to `struct Solution {}`,
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, the table's type `[[(i32, i32); 2];
7]` to `Array[Array[(i32, i32), 2], 7]`, `vec![vec![false; n]; m]` to
`Vec.filled(m, Vec.filled(n, false))`, `vec![(0usize, 0usize)]` to `[(0,
0)]`, each `as usize` to `as i64` or away, the patterns `&(di, dj)` and
`|&(x, y)|` to `(di, dj)` and `|(x, y)|`, `&&` and `\|\|` to `and` and
`or`, and `Solution::` to `Solution.`. Its output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the cells a path can reach, grown from the top-left cell a
sweep over the whole grid at a time, a neighbour joining when both
streets open towards each other, until a sweep adds none, and the answer
whether the corner is among them. LeetCode's five examples and 1998
grids of 1 to 12 by 1 to 12, each of random streets with a path planted
from corner to corner; every other one then has a cell of its path given
a random street again, and every third has its streets all drawn again,
with no path planted. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the grid reflected in its main diagonal, each street turned to match: the same |
| P3 | the grid turned half round, each street turned to match, so a path runs back: the same |
| P4 | the start made street 5, open only off the grid: no path, unless it is the corner |
| P5 | the corner made street 4, open only off the grid: no path, unless it is the start |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 grids: checksum 722897404,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, searching the
grid depth first, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the neighbour asked to open the way of the step, not back | P1 782, P3 107, P5 181, P6 3128 |
| M2 | ★: street 3 given street 5's openings | P1 646, P2 117, P3 109, P6 2584 |
| M3 | stack: a step taken whether or not the cell opens that way | P1 424, P3 496, P4 1224, P6 424 |
| M4 | stack: street 6, not 5, opening to the left | P1 168, P2 320, P3 300, P6 168 |
| M5 | union: a cell joined to its right neighbour whatever that street | P1 142, P2 249, P3 252, P5 512, P6 142 |
| M6 | union: street 3, not 5, opening upward | P1 154, P2 320, P3 281, P6 154 |
| M7 | follow: only the first cell's up and right openings tried | P1 415, P2 800, P3 408, P6 415 |
| M8 | follow: one cell no longer a path by itself | P1 16, P4 16, P5 16, P6 16 |
| M9 | solution: the step back matched in either coordinate | P1 217, P3 395, P5 1031, P6 217 |
| M10 | solution: street 6 given street 4's openings | P1 663, P2 140, P3 109, P6 663 |

P1 and P6 kill all ten, P3 nine, P2 six, P5 four and P4 two. Turning the
grid half round (P3) runs every path backwards, so each edit that treats
a way in differently from a way out fails it; only M8, which goes wrong
on one cell alone, passes. Reflecting the grid (P2) swaps rows for
columns and each street for its mirror, which the edits that change one
street's openings (M2, M4, M6, M10) or treat rows and columns apart (M5,
M7) fail. A corner opening only off the grid (P5) is entered only by the
edits that do not ask it to open back, M1, M5 and M9, and a start
opening only off the grid (P4) is left only by M3, which does not ask
the cell it leaves; M8 fails both on one cell.

## Benchmarks

The bench lays a 299 by 300 grid whose streets snake through every cell,
left to right along the even rows and back along the odd, so that the
one path runs from corner to corner. Then 3000 rounds, each breaking one
cell, drawn from the checksum so far, with the next street, asking for a
path, and mending the cell. Every implementation prints `3000 rounds
over a 299 by 300 snake, whole true: checksum 174893352`. The work is a
search that follows the snake up to the broken cell, on average half the
grid, a round. Rust uses a `VecDeque` and `contains` on its table; C
keeps the queue in a static array as large as the grid; Go appends to a
slice read from a moving head; Python uses a `deque`.

BENCHTAB
