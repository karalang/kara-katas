# 1761. Minimum Degree of a Connected Trio in a Graph

You are given an undirected graph. You are given an integer `n` which is
the number of nodes in the graph and an array `edges`, where each
`edges[i] = [ui, vi]` indicates that there is an undirected edge between
`ui` and `vi`. A connected trio is a set of three nodes where there is
an edge between every pair of them. The degree of a connected trio is
the number of edges where one endpoint is in the trio, and the other is
not. Return the minimum degree of a connected trio in the graph, or `-1`
if the graph has no connected trios.

```
n = 6, edges = [[1,2],[1,3],[3,2],[4,1],[5,2],[3,6]]                  ->  3
n = 7, edges = [[1,3],[4,1],[4,3],[2,5],[5,6],[6,7],[7,5],[2,6]]      ->  0
```

**Constraints:** `2 <= n <= 400`, `edges[i].length == 2`, `1 <=
edges.length <= n * (n-1) / 2`, `1 <= ui, vi <= n`, `ui != vi`, and
there are no repeated edges.

The arms are `fn min_trio_degree(n: i32, edges: Vec[Vec[i32]]) -> i32`.

## Approaches

A trio's degree is the sum of its three nodes' degrees less the six ends
of its own three edges.

| file | mechanism |
|---|---|
| `min_trio_degree.kara` ★ | an adjacency matrix of `bool`s and the degrees, then every edge `u < v` with each `w` above `v` joined to both. O(n^3) |
| `min_trio_degree_bitset.kara` | each node's neighbours as a bitset of `u64` words, and for every edge the common neighbours found a word at a time with `&` and `trailing_zeros`. O(m n / 64) |
| `min_trio_degree_merge.kara` | sorted neighbour lists, and for every edge the lists of its two ends merged with two pointers. O(m n) |
| `min_trio_degree_oriented.kara` | each edge pointed from its end of lower degree to the higher, ties by number, so each triangle is found once from its lowest node, with a `Set[(i64, i64)]` of edges for the third side. O(m sqrt(m)) |
| `min_trio_degree_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![false; n + 1]; n + 1]`, `usize` indices, every edge with every third node), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`3 0`); five
edges, no trio, a lone triangle, a square, which has none, a complete
graph on 5, and a triangle with a tail (`-1 0 -1 6 1`); the constraints'
most, 400 nodes sparse, middling and dense (`400 nodes: 2 38 521`); and
3000 random graphs of 2 to 12 nodes (`3000 random graphs: checksum
885829445`). `min_trio_degree.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, bitset and oriented arms check clean as first
written. The merge arm was first written `let (mut i, mut j) = (0, 0)`,
and `karac fix` moved the `mut` before the pattern in 3 fixes. The Rust
solution takes one round of 20 fixes by `karac fix`'s count, and its
diff is: `struct Solution;` to `struct Solution {}`, `Vec<Vec<i32>>` to
`Vec[Vec[i32]]` twice, `n as usize` and `e[0] as usize` to `as i64`,
`vec![vec![false; n + 1]; n + 1]` to `Vec.filled(n + 1, Vec.filled(n +
1, false))`, `vec![0; n + 1]` to `Vec.filled(n + 1, 0i32)`, `i32::MAX`
to `i32.MAX` twice, `&&` to `and`, and `Solution::` to `Solution.`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every three nodes joined to each other, and for each such
trio the edges with exactly one end in it, counted from the edge list.
LeetCode's examples, the edges, and 1993 random graphs of 2 to 9 nodes,
each pair joined with a chance drawn for the graph. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the nodes numbered the other way round give the same |
| P3 | the edges in reverse order, every other one with its ends swapped, give the same |
| P4 | a node joined to nothing changes nothing |
| P5 | a new node hung from node 1 makes no trio and adds at most one to any trio's degree |
| P6 | the ★ arm's answer |

P3 first swapped the ends of every edge, and mutation M3 survived it:
the random graphs list each edge from its lower end, so with every end
swapped or none, a triangle's edges never run round it in a cycle, and a
bitset that records each edge at its first end only still finds every
triangle. Swapping every other edge's ends gives the cycle. All 60,000
checks pass on every arm: `2000 cases: checksum 981431625, 60000 checks
over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`. Python, reading every trio with
`itertools.combinations`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The solution
arm's first M10, node 1 never a third node, was equivalent, since that
arm finds each trio from all three of its edges, and was replaced.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the trio's inner edges subtracted four times, not six | P1 1005, P6 4020 |
| M2 | ★: a third node just above v never tried | P1 294, P2 292, P6 1176 |
| M3 | bitset: each edge recorded at one end only | P3 279 |
| M4 | bitset: the first 64 nodes never a third node | P1 1005, P6 1005 |
| M5 | merge: equal neighbours stepped past as if smaller | P1 1005, P6 1005 |
| M6 | merge: one too many in each trio's degree | P1 1005, P6 1005 |
| M7 | oriented: the next out-neighbour never paired | P1 557, P2 109, P5 26, P6 557 |
| M8 | oriented: an edge recorded in the order given | P1 2, P2 1004, P3 225, P5 1, P6 2 |
| M9 | solution: a third node joined to either end taken | P1 1520, P5 1405, P6 1520 |
| M10 | solution: no trio answered 0 | P1 995, P6 995 |

## Benchmarks

The bench draws one weight for every pair of 400 nodes and makes 40
calls of the ★ arm, each on the pairs whose weight is below a threshold
chosen from the checksum so far, so each graph holds 30 to 80 percent of
the pairs. C keeps the matrix as one flat array of `bool`; Kāra, Rust
and Go keep a vector per row. Every implementation prints `40 calls on
400 nodes: checksum 789013515`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 1.9 s against Rust's 1.8 s (1.9 s with overflow checks on),
C's 1.5 s and Go's 2.4 s; Python takes 16.6 s.
