# 2123. Minimum Operations to Remove Adjacent Ones in Matrix

You are given a 0-indexed binary matrix `grid`. In one operation, you
can flip any `1` in `grid` to be `0`.

A binary matrix is well-isolated if there is no `1` in the matrix that
is 4-directionally connected (i.e., horizontal and vertical) to another
`1`.

Return the minimum number of operations to make `grid` well-isolated.

```
grid = [[1,1,0],[0,1,1],[1,1,1]]  ->  3
grid = [[0,0,0],[0,0,0],[0,0,0]]  ->  0
grid = [[0,1],[1,0]]              ->  0
```

**Constraints:** `m == grid.length`; `n == grid[i].length`; `1 <= m, n
<= 300`; `grid[i][j]` is either `0` or `1`.

Two adjacent cells differ in the parity of row plus column, so the ones
form a bipartite graph: even cells on one side, odd on the other, an
edge for each adjacent pair. The ones to flip are a vertex cover of that
graph, and by König's theorem the smallest vertex cover of a bipartite
graph is as large as its maximum matching. Every arm computes that
matching; they differ in how.

## Approaches

| file | mechanism |
|---|---|
| `isolated.kara` ★ | the graph as a `Vec[Vec[i64]]` of each even one's odd neighbours; Kuhn's augmenting paths, a recursive search from each even one that marks the odd ones it visits with the round's stamp. O(V * E) |
| `isolated_hopcroft.kara` | Hopcroft-Karp: each phase layers the even ones by breadth-first search from the free ones over a `VecDeque`, then takes shortest augmenting paths along the layers. O(E * sqrt(V)) |
| `isolated_bfs.kara` | no graph built: from each even one, a breadth-first search over the grid alternating a step to an odd neighbour with the step back along its match, parents kept per cell; the path flipped by walking them back. Iterative |
| `isolated_struct.kara` | a `struct Matching { adj, partner, seen }` with `new`, a `greedy` first pass, `grow` (`mut ref self`, recursive) and `size` |
| `isolated_flow.kara` | Dinic's maximum flow over a `struct Network` of flat edge vectors (`head`, `next`, `to`, `cap`), each edge's reverse at the index `e ^ 1`; source to the even ones, the even ones to their odd neighbours, the odd ones to the sink |
| `isolated_solution.kara` | LeetCode's Rust template: Kuhn's search as a `fn` nested in the method, taking the graph by `&` and the matches by `&mut Vec<Option<usize>>`, a fresh `vis` per even one, carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (one cell, a row of five ones, a plus sign, a 3 by 3 block of
ones), each with its answer; then the total and a checksum of the
answers over 1000 random grids of 1 to 8 by 1 to 8, each cell a one
with chance a quarter, a half or three quarters in turn; then the
constraints' largest, a 300 by 300 grid of ones and one with each cell
a one with chance one half. `isolated.py` mirrors the ★ arm and its
output is byte-identical.

The template's nested `fn` is one of Rust's spellings `karac fix`
carries: it moved the function out of the method in its second round.
No compiler gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a one with a one beside it must go, or every one beside it
must, so the fewest flips are found by trying both, one such one at a
time, recursively. It checks 300 random grids of 1 to 5 by 1 to 5, each
cell a one with chance a quarter, a half or three quarters in turn;
then 30 strips of 1 or 2 by up to 16, three quarters ones; then 30
grids of up to 6 by 6, a quarter ones. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid transposed: the same answer |
| P3 | the grid mirrored left to right: the same answer |
| P4 | a row of zeros added on top: the same answer |
| P5 | the answer is at most the even ones and at most the odd ones that have a one beside them, and the first zero made a one raises it by 0 or 1 |
| P6 | each arm agrees with at least three of the other five |

P3 and P4 change which cells are even when the width or the height is
even and odd in turn, so an arm that treats the two sides unequally
answers differently.

The differential prints `360 grids: checksum 770832363, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against Python's smallest vertex
cover of the same grids found by trying sets of ones by size, which
does not use König's theorem. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-seven edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the one below never a neighbour | P1 67, P2 98, P3 32, P4 87, P6 67 |
| M5 | ★: every even one with a neighbour counted | P1 65, P3 48, P4 116, P5 65, P6 65 |
| M6 | ★: the first cell's round seeing everything | P1 89, P3 61, P4 89, P6 89 |
| M8 | hopcroft: a free odd one never found | P1 228, P6 228 |
| M11 | hopcroft: a zero to the right taken for a one | P1 121, P2 157, P3 134, P4 189, P5 83, P6 121 |
| M32 | hopcroft: the one above read one column on | P1 45, P2 38, P3 33, P4 91, P5 47, P6 45 |
| M13 | bfs: only the last edge of a path flipped | P1 1, P2 2, P3 1, P4 1, P6 1 |
| M15 | bfs: the one to the right never a neighbour | P1 62, P2 98, P3 38, P4 83, P6 62 |
| M16 | bfs: a search that fails counted | P1 160, P3 94, P4 240, P5 154, P6 160 |
| M20 | struct: a partner at cell 0 not counted | P1 133, P3 73, P4 133, P5 23, P6 133 |
| M21 | struct: no path through a matched one | P1 23, P2 27, P3 12, P4 22, P6 23 |
| M35 | struct: the one above never a neighbour | P1 34, P2 55, P3 32, P4 87, P6 34 |
| M23 | flow: no residual edge | P1 21, P2 25, P3 21, P4 22, P6 21 |
| M33 | flow: each even one fed twice | P1 64, P3 48, P4 116, P5 62, P6 64 |
| M34 | flow: the one to the left never a neighbour | P1 37, P2 55, P3 38, P4 83, P6 37 |
| M36 | solution: the first row never searched | P1 140, P2 127, P3 37, P4 140, P6 140 |
| M37 | solution: the first column never searched | P1 132, P2 127, P3 83, P4 93, P6 132 |

P1 and P6 kill all seventeen, P3 and P4 sixteen, P2 eleven and P5 six.
P3 and P4 miss only M8, which finds no augmenting path at all and so
answers 0 for every grid, the same after any change of it. P2 misses
the edits that are wrong the same way across the diagonal, overcounting
(M5, M16, M33) or losing a cell index (M6, M20) or a phase (M8). P5
sees the overcounts: an answer above the even or the odd ones with a
neighbour, or one that falls, or rises by two, when a one is added.

Of the thirty-seven, twenty were not kept. Six are equivalent: the odd
ones as the searching side in the ★, bfs and Rust arms, since a
matching is the same from either side; Hopcroft-Karp's layers counted
from 1, which only the differences between them matter to; its dead
ends searched again, which only costs time; and one augmenting path per
Dinic phase, which still ends at the maximum. Two survive and are not
equivalent: the struct arm's marks never cleared between searches, and
the flow arm's middle edges made two-way, which lets flow run from an
odd one back to an even one. A Python search over random grids of up to
5 by 5 finds 4 and 11 grids in 20000 where they answer wrong, and none
is among the differential's 360. The flow arm's cursors kept across
phases never ends. Eleven fail as a kept one does: no augmenting path
taken (one stamp for every round, or no path through a matched one, in
the ★ arm; one phase only; only free neighbours in the bfs arm; the
Rust arm's marks kept across rounds, its search through a matched one,
and an odd one matched to itself) as M21; the Rust arm's one below
never a neighbour as M3; the struct arm's greedy pass matching every
free neighbour and a greedily matched one searched again as M33; and
the flow arm's odd ones cut from the sink as M8.

## Verification

Every arm prints the same output as `isolated.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the bfs and Hopcroft-Karp arms take 0.6 s and
0.8 s, the flow arm 4.1 s, the struct arm 7.2 s and the ★ arm 12 s, all
of it the two 300 by 300 grids; the Rust arm takes 171 s, since it
clears a fresh `vis` of 90000 cells for each of the 45000 even ones.
The differential takes 1.8 s; compiled it takes 0.6 s.

`karac fix` carries the template in four rounds of 41, 2, 11 and 1
edits: Rust's spellings (`Vec<..>` and `Option<..>` to `[..]`, `&&` and
`||` to `and` and `or`, `&` and `&mut` parameters to `ref` and `mut
ref`, `for &v in &adj[u]` to `for v in ref adj[u]`, the `&adj` and
`&mut` arguments, `|&x|` to `|x|`, `::new` and `Solution::` to `.`,
`struct Solution;` to `struct Solution {}`); then the nested `fn dfs`
moved out of the method; then `usize` to `i64` throughout, the three
`vec![..; n]` to `Vec.filled(n, ..)`, the recursive call's `mut`
arguments, and the adapter's `as i64`; then the `ref` dropped from the
`adj` parameter, which borrows already.

## Benchmarks

The bench builds 12 grids of 300 by 300 once, each cell a one with
chance a quarter, a half or three quarters in turn, then solves every
grid 10 times, one cell flipped before each solve so that no solve
repeats one before, with the ★ arm in all five languages; the C mirror
keeps each even one's neighbours in a fixed slot of four. Every
implementation prints `120 solves: 2313278 operations, checksum
619554486`.

BENCHTAB
