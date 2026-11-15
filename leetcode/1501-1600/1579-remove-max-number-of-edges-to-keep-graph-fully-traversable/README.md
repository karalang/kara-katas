# 1579. Remove Max Number of Edges to Keep Graph Fully Traversable

Alice and Bob have an undirected graph of `n` nodes and three types of
edges:

- Type 1: can be traversed by Alice only.
- Type 2: can be traversed by Bob only.
- Type 3: can be traversed by both Alice and Bob.

Given an array `edges` where `edges[i] = [type_i, u_i, v_i]` represents a
bidirectional edge of type `type_i` between nodes `u_i` and `v_i`, find
the maximum number of edges you can remove so that after removing the
edges, the graph can still be fully traversed by both Alice and Bob. The
graph is fully traversed by Alice and Bob if starting from any node, they
can reach all other nodes.

Return the maximum number of edges you can remove, or return `-1` if
Alice and Bob cannot fully traverse the graph.

```
n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]  ->  2
n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]                  ->  0
n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]                          ->  -1
```

**Constraints:** `1 <= n <= 10^5`;
`1 <= edges.length <= min(10^5, 3 * n * (n - 1) / 2)`;
`edges[i].length == 3`; `1 <= type_i <= 3`; `1 <= u_i < v_i <= n`; all
tuples `(type_i, u_i, v_i)` are distinct.

## Approaches

A type 3 edge does the work of two, so every arm spends the type 3 edges
first and each person's own edges only on what is left to join.

| file | mechanism |
|---|---|
| `edges.kara` ★ | two disjoint-set forests, one for Alice and one for Bob, each a `struct Dsu` with `mut ref self` methods: `find` with path halving, `join` with union by size, and a count of parts. The type 3 edges go into both, then type 1 into Alice's and type 2 into Bob's; an edge that joins two parts is kept. O(m α(n)) |
| `edges_parts.kara` | no union-find: a graph on `n` nodes in `c` parts needs `n - c` edges to span it, so with the type 3 graph in `c3` parts the answer is `m - (n - c3) - 2 (c3 - 1)`. The parts are counted by a walk with a stack over adjacency lists. O(n + m) |
| `edges_kruskal.kara` | Kruskal over the edges sorted by type, 3 first, each forest a bare `Vec[i64]` passed by `mut ref` to a recursive `find` that compresses its path; the parts counted at the end by a `filter` whose closure calls `find`. O(m log m) |
| `edges_solution.kara` | LeetCode's Rust template (a `UnionFind` struct over 0-based `usize` nodes with a recursive `self.find` and a method named `union`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three of
2 or 3 nodes, then the edges removed, the count of graphs that cannot be
traversed and a checksum for 3000 random graphs of up to 6 nodes, 300 of
up to 301 and 10 of up to 10001. From each node the generator draws a few
edges to nodes a little further on, half of them type 3, drops repeats
and shuffles them. `edges.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of edges to keep tried, and the answer the most
edges left out of a set over which both Alice and Bob reach every node.
It checks 3000 graphs of 2 to 5 nodes and 1 to 8 distinct edges, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the edges in reverse order leave the answer |
| P3 | the nodes numbered backwards (`x` to `n + 1 - x`) leave the answer |
| P4 | the type 1 and type 2 edges swapped leave the answer |
| P5 | a new node joined to node 1 by a type 3 edge leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 898829412, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two edits that would have been
equivalent were not used: in the ★ arm both forests hold the same parts
while the type 3 edges go in, so `a or b` and `a and b` agree, and union
by size only changes the shape of the trees.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: path halving points a node at itself, so `find` stops short of the root | P1 1423, P6 1423 |
| M2 | ★: the type 3 edges never go into Bob's forest | P1 1412, P4 295, P5 1014, P6 1412 |
| M3 | ★: each forest starts one part too many | P1 1463, P6 1463 |
| M4 | parts: the edges each person still needs counted once, not for both | P1 320, P6 320 |
| M5 | parts: Alice's and Bob's walks leave out the type 3 edges | P1 599, P5 864, P6 599 |
| M6 | parts: the walk never starts from node `n` | P1 237, P3 438, P5 237, P6 237 |
| M7 | kruskal: the type 3 edges sorted last | P1 1340, P2 44, P6 1340 |
| M8 | kruskal: `link` points the node, not its root, at the other root | P1 270, P2 170, P3 509, P5 1291, P6 270 |
| M9 | template: a type 3 edge goes into Alice's forest only | P1 1412, P4 295, P5 1014, P6 1412 |
| M10 | template: traversable when either forest is in one part | P1 568, P6 568 |

## Benchmarks

The bench draws 40 graphs of 13000 nodes first, from each node 4 to 11
edges to a node at most 12 further on, half of them type 3 (repeats kept),
about 97000 edges a graph, each shuffled; then solves each by the ★ arm,
in all five languages. Every implementation prints `40 graphs of 13000
nodes: 2 not traversable, edges removed 3206626, checksum 993677523`.
Each edge is its own allocation in every language, as in Kāra's
`Vec[Vec[i64]]`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.432 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.529 s |
| Rust (`rustc -O`) | 0.532 s |
| Kāra (`karac build`) | 0.584 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.594 s |
| Go | 0.797 s |
| Python | 18.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.563 s and 0.650 s on one run).

Kāra is 1.12x Rust under overflow checks by median here; a second
measurement of just those two, twenty interleaved runs each, gave 0.607 s
and 0.522 s (1.16x). The first full run was noisier (0.700 s and 0.532 s).
Most of the time in every lane is drawing the 3.9 million edges.

## Verification

All four arms print the same output as `edges.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`76e5a13ad`.

## Writing it

The ★ arm was written in Kāra; `karac fix` dropped one redundant
`as i64` on `edges.len()`. The parts and Kruskal arms were written with
a Rust-style `!` on a bool, which `karac fix` turned into `not`.

The Rust template took two rounds of `karac fix`:

1. twenty edits: the `Vec<..>` types to `Vec[..]`, `&mut self` to
   `mut ref self`, `UnionFind::new` to `UnionFind.new`, `!` to `not`,
   `&&` to `and`, the `|&x|` pattern to a plain name, and `Solution::` to
   `Solution.`;
2. the wrapper's `as i64` dropped.

It then checks and agrees with no hand edit.
