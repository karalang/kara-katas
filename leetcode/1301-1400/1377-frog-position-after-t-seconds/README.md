# 1377. Frog Position After T Seconds

Given an undirected tree consisting of `n` vertices numbered from `1` to
`n`. A frog starts jumping from vertex 1. In one second, the frog jumps
from its current vertex to another unvisited vertex if they are directly
connected. The frog can not jump back to a visited vertex. In case the
frog can jump to several vertices, it jumps randomly to one of them with
the same probability. Otherwise, when the frog can not jump to any
unvisited vertex, it jumps forever on the same vertex.

The edges of the undirected tree are given in the array `edges`, where
`edges[i] = [ai, bi]` means that exists an edge connecting the vertices
`ai` and `bi`.

Return the probability that after `t` seconds the frog is on the vertex
`target`. Answers within `10^-5` of the actual answer will be accepted.

```
n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 2, target = 4  ->  0.16666666666666666
n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 1, target = 7  ->  0.3333333333333333
```

**Constraints:** `1 <= n <= 100`, `edges.length == n - 1`,
`edges[i].length == 2`, `1 <= ai, bi <= n`, `1 <= t <= 50`, `1 <= target
<= n`.

Each arm is `fn frog_position(n: i32, edges: Vec[Vec[i32]], t: i32,
target: i32) -> f64`.

## Approaches

| file | mechanism |
|---|---|
| `frog_position.kara` ★ | the chance of the frog being on each vertex, moved one second at a time: each second, a vertex it can be on with unvisited neighbours hands its chance to them in equal shares and keeps none, and a vertex with none keeps its chance for good. O(n) |
| `frog_position_dfs.kara` | a recursive walk from 1 looking for the target: the chance there is one over the product of the ways on at each vertex above it, if the frog gets there by `t` and does not get there early with somewhere still to go. O(n) |
| `frog_position_climb.kara` | the tree hung from 1 first, each vertex's parent, depth and number of children found by a breadth-first walk; then the answer read by climbing from the target to 1, dividing by the children of each vertex on the climb. O(n) |
| `frog_position_stack.kara` | the frog's jumps followed with a stack of (vertex, where it came from, chance, seconds left), as if each were tried in turn, until the target is popped. O(n) |
| `frog_position_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![vec![]; n + 1]` graph, `let (a, b) = (e[0] as usize, e[1] as usize);`, a `VecDeque<(usize, f64)>` taken a level at a time, and the ways on counted with `.filter(\|&&v\| !visited[v]).count()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, and 100
vertices, the constraints' most, as a path from 1 (50 seconds to vertex
51, and to vertex 100, out of reach), as a star around 1 (1 second and
50 to a leaf), and as a binary heap (6 seconds to vertex 64, and 50 to
vertex 100), each to six places (`0.166667 0.333333 1.000000 0.000000
0.010101 0.010101 0.015625 0.031250`); and 2000 random trees of 1 to 100
vertices, numbered in a random order, each vertex joined to any vertex
taken before it, to one of the last three, so the tree runs deep, to one
of the first three, so it runs wide, or to one of the last half, 500 of
each, each edge either way round and the edges in a random order, with 1
to 12 seconds and a target at random, each answer counted in units of
2^-20 (`2000 random trees: 765 targets reachable, checksum 498034521`).
Every answer is one over a product of whole numbers, so a count rounded
half up from a product computed in any order lands on the same unit: a
tie needs the product to be a power of two, which every order computes
exactly. `frog_position.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, recursive and stack arms check clean as first
written. The climbing arm took one round of one fix from one error. Its
`let mut at = target;` is an `i32`, from `target`, and `at = parent[at]`
reads an `i64`: `parent` is `Vec.filled(n + 1, 0)`, and storing
`parent[v] = u`, with `u` an `i64` read out of the walk's order, settled
its literal so. The fix offered was the literal's suffix, `Vec.filled(n
+ 1, 0i32)`, which `parent[v] = u` then refused, with only the advice to
truncate. Since B-2026-11-25-20, a fill holding a stored `i64` is fixed
by widening the binding instead, `let mut at: i64 = target;`, which
keeps every value. The Rust solution takes one round of 29 fixes from 15
errors: the `use std::collections::VecDeque;` line deleted, `struct
Solution;` to `struct Solution {}`, each `Vec<..>` to `Vec[..]`, `n as
usize`, `e[0] as usize` and `e[1] as usize` to `as i64`, `vec![vec![]; n
+ 1]` and `vec![false; n + 1]` to `Vec.filled`, `for e in &edges` and
`for &v in &g[u]` to `for e in ref edges` and `for v in ref g[u]`,
`(1usize, 1.0f64)` to `(1, 1.0)`, `|&&v|` to `|v|`, `target as usize` to
`target`, each `!`, `&&` and `||` to `not`, `and` and `or`, and
`VecDeque::` and `Solution::` to `VecDeque.` and `Solution.`. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the frog's whole state is where it sits, which vertices it
has visited and the chance of that state; each second, every state with
an unvisited neighbour of where it sits gives way to one state for each,
the chance split evenly, read off the edges as given, and a state with
none stays as it is; after `t` seconds, the chances of the states on the
target are added. LeetCode's two examples and 2000 trees of 1 to 12
vertices, drawn as above, 500 of each kind, with 1 to 8 seconds, a
target, and a renumbering that keeps 1. Every case is drawn before any
arm answers. Two chances are the same when they are within 10^-9.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the vertices renumbered, 1 kept: the same chance |
| P3 | the chances on every vertex add up to 1 |
| P4 | after `n` seconds the frog has stopped: `n + 5` the same |
| P5 | the edges listed the other way, each written the other way round: the same chance |
| P6 | the ★ arm's chance |

All 60,060 checks pass on every arm: `2002 cases: checksum 178749055,
60060 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, following the
same states, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a vertex's chance split over all its neighbours, the visited one too | P1 533, P3 1407, P6 2132 |
| M2 | ★: a vertex keeps its chance after handing it on | P1 809, P3 1836, P6 3236 |
| M3 | dfs: the target reached early counted as 0 though it has nowhere to go | P1 784, P3 1558, P6 784 |
| M4 | dfs: the chance never split | P1 652, P3 1346, P6 652 |
| M5 | climb: a target one second too deep still reached | P1 102, P3 514, P6 102 |
| M6 | climb: the climb divides by the target's children and not by 1's | P1 389, P3 907, P6 389 |
| M7 | stack: a vertex with no time left still pushes its ways on | P1 67, P3 360, P6 67 |
| M8 | stack: a jump that takes no time | P1 218, P6 218 |
| M9 | solution: the levels taken while `time < t`, not `time <= t` | P1 196, P3 746, P6 196 |
| M10 | solution: vertex 1 never marked visited | P1 549, P3 1611, P5 270, P6 549 |

P1 and P6 kill all ten, P3 nine, P5 one, and P2 and P4 none. The chances
adding up to 1 (P3) catch every edit that loses chance or makes it,
which all but one do. The jump that takes no time (M8) keeps the total:
its frog always runs on to a leaf, so it answers every leaf's chance and
0 elsewhere, and the leaves' chances add up to 1. Listing the edges the
other way (P5) catches only vertex 1 left unmarked (M10), whose frog can
step back to 1, so how wrong it goes depends on the order its neighbours
were listed in. Renumbering (P2) catches nothing, since no arm looks at
a vertex's number but 1's and the target's, which renumbering carries
along; and `n + 5` seconds (P4) nothing, since every edit's frog, like
the true one, has stopped by `n` seconds.

## Benchmarks

The bench builds 50 trees of 100 vertices, the constraints' most, once:
each vertex after the first, in a random order, joined to any vertex
taken before it, or to one of the last three. Then 100,000 rounds, each
asking one tree, a time of 1 to 50 seconds and a target, all drawn from
the checksum so far, for the frog's chance with the ★ arm, counted in
units of 2^-20. Every implementation prints `100000 rounds over 50 trees
of 100 vertices: checksum 461685223`. The work is the neighbour lists
built and the chance moved for up to `t` seconds, each round. The Rust
function takes `&[Vec<i32>]`, as the Kāra one borrows its `Vec`; C has
no growable list, so its neighbours are counted first and laid out one
vertex after another.

BENCHTAB
