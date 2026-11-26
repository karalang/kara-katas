# 1466. Reorder Routes to Make All Paths Lead to the City Zero

There are `n` cities numbered from `0` to `n - 1` and `n - 1` roads such
that there is only one way to travel between two different cities (this
network form a tree). Last year, The ministry of transport decided to
orient the roads in one direction because they are too narrow. Roads are
represented by `connections` where `connections[i] = [ai, bi]`
represents a road from city `ai` to city `bi`. This year, there will be
a big event in the capital (city `0`), and many people want to travel to
this city. Your task consists of reorienting some roads such that each
city can visit the city `0`. Return the minimum number of edges changed.
It's guaranteed that each city can reach city `0` after reorder.

```
n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]   ->  3
n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]         ->  2
n = 3, connections = [[1,0],[2,0]]                     ->  0
```

**Constraints:** `2 <= n <= 5 * 10^4`, `connections.length == n - 1`,
`connections[i].length == 2`, `0 <= ai, bi <= n - 1`, and `ai != bi`.

The arms are `fn min_reorder(n: i32, connections: Vec[Vec[i32]]) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_reorder.kara` ★ | each road listed at both its ends in a `Vec[Vec[(i32, i32)]]`, marked 1 where it leads away from the end it is listed at; the roads form a tree, so a breadth-first search out of 0 on a `VecDeque` crosses each once, away from 0, and adds up the marks of the roads it crosses. O(n) |
| `min_reorder_dfs.kara` | the same lists marked by `bool`, and a recursive depth-first search that never steps back to the city it came from, the 50000-city line 50000 calls deep. O(n) |
| `min_reorder_stack.kara` | each city's neighbours in a plain list and the roads as given in a `Set[(i32, i32)]`; a depth-first search on a stack turns a step from `city` to `next` whenever `(city, next)` is in the set. O(n) |
| `min_reorder_sweeps.kara` | the cities that reach 0 grown by sweeping the road list until nothing changes: a road into a city that reaches 0 carries its other end there, and a road out of one must be turned. O(n) a sweep, O(n^2) at worst |
| `min_reorder_solution.kara` | a Rust solution as LeetCode's Rust users write it (an adjacency list of `Vec<Vec<(usize, i32)>>` indexed through `as usize` casts, `vec![false; n]`, and a `VecDeque` from `std::collections`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, one road away from 0 and one toward it, 50000 cities in a line
each road pointing away from 0, and 50000 roads out of 0 (`3 2 0 1 0
49999 49999`); the constraints' most, a random tree of 50000 cities
(`50000 cities: 24958`); and 2000 random trees of 2 to 60 cities, each
road's direction drawn at random (`2000 random trees: total 29727,
checksum 447867741`). `min_reorder.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the dfs and sweeps arms check clean as first written. The
stack arm held its stack as `[0].to_vec()`, a `Vec[i64]` that widens
each `i32` pushed onto it, and asked `given.contains((city, next))` of
the `Set[(i32, i32)]` of roads. Check passed it, and the compiled lanes
read the `i64` city as an `i32` and printed `1 1 0 0 0 0 0` for
LeetCode's examples and the edges, where the interpreter printed the
right `3 2 0 1 0 49999 49999`. That was B-2026-11-26-85, fixed at
4777a670cf: check now refuses the narrowing, "implicit coercion from
'i64' to 'i32' would narrow or change sign", and the arm writes `city as
i32` as the error says. The ★ arm takes three fixes by `karac fix`: the
two `n as i64` given to `Vec.filled` dropped, since `i32` widens to
`i64` implicitly, and `turned` declared `i32`, since the literal `0`
keeps its default `i64`, which would narrow into the `i32` return. The
harness builds its line and its fan of 50000 roads as
`(0..49999).map(|c| [c, c + 1].to_vec()).collect()` into a
`Vec[Vec[i32]]`, which is refused: the range of literals keeps `i64`.
Its first literal takes `i32`, `0i32..49999`; `karac fix` offers no fix
for it here. The Rust solution takes one round of 21 fixes by `karac
fix`'s count: the `use std::collections::VecDeque;` line deleted,
`struct Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`, each
`usize` to `i64` (the casts and the adjacency list's element),
`vec![vec![]; n]` and `vec![false; n]` to `Vec.filled(..)`,
`VecDeque::new` to `VecDeque.new`, `for &(v, cost) in &adj[u]` to `for
(v, cost) in ref adj[u]`, `!visited[v]` to `not visited[v]`, `ans`
declared `i32`, and `Solution::min_reorder` to `Solution.min_reorder`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of roads to turn, and the fewest whose turning lets
every city reach 0, found by a search backwards from 0, while there are
at most 8 cities. LeetCode's examples, the two one-road trees, a line of
5000 cities each way, a fan of 5000 roads out of 0, a random tree of
5000 cities, and 1994 random trees, half of 2 to 8 cities and half of 2
to 60, drawn as the harness draws them. The sweeps arm takes up to one
sweep a city on a shuffled line, so the constraints' most, 50000 cities,
stays in the harness: shuffled by P2, it passes the interpreter's step
limit. Each list of roads is bound under its type before it is pushed:
the literals in a `.to_vec()` pushed in a tuple keep `i64`
(B-2026-11-26-6), and so does a range behind a `collect` there
(B-2026-11-26-9).

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 8 cities |
| P2 | the roads shuffled give the same answer |
| P3 | every road turned turns the others: n - 1 less the answer |
| P4 | the cities but 0 relabelled at random give the same answer |
| P5 | one city more, joined by a road toward the tree, gives the same answer, and by a road away from it one more |
| P6 | the ★ arm's answer |

All 55,660 checks pass on every arm: `2003 cases: checksum 679319968,
55660 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, turning each
road whose far end lies deeper from 0, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: no road marked as leading away | P1 958, P3 2003, P5 2003, P6 7372 |
| M2 | ★: the roads toward 0 counted, not those away | P1 943, P5 2003, P6 7048 |
| M3 | dfs: the roads toward 0 counted, not those away | P1 943, P5 2003, P6 1762 |
| M4 | dfs: every road marked as leading away | P1 961, P3 2003, P5 2003, P6 1845 |
| M5 | stack: each road filed in the opposite direction | P1 943, P5 2003, P6 1762 |
| M6 | stack: no road listed at the city it leads into | P1 486, P3 1599, P5 1343, P6 1354 |
| M7 | sweeps: a city whose road leads into a city that reaches 0 never marked | P1 486, P3 1599, P5 1343, P6 1354 |
| M8 | sweeps: each road away from 0 counted twice | P1 958, P3 2003, P5 2003, P6 1843 |
| M9 | solution: no road marked as leading away | P1 958, P3 2003, P5 2003, P6 1843 |
| M10 | solution: city 0 never marked as visited | P1 552, P2 240, P3 2003, P6 991 |

## Benchmarks

The bench draws 10 random trees of 50000 cities, the constraints' most,
once; then makes 20 passes, each turning one road of every tree, chosen
from the checksum so far, so no answer carries over, answering it with
the ★ arm and folding the answer into the checksum. Each implementation
builds each city's list of roads as a growable array (C's written out
with `realloc`) and searches with a queue: Rust's `VecDeque`, a plain
array in C, a slice in Go and Python's `deque`. Every implementation
prints `20 passes over 10 trees of 50000 cities: checksum 298424237`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 1.2 s against Rust's 1.5 s (1.1 s with
overflow checks on), C's 0.92 s and Go's 1.8 s; Python takes 15.3 s.
