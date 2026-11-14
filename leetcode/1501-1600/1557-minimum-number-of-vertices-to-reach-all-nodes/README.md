# 1557. Minimum Number of Vertices to Reach All Nodes

Given a directed acyclic graph with `n` vertices numbered from `0` to
`n - 1`, and an array `edges` where `edges[i] = [from_i, to_i]` is a
directed edge from `from_i` to `to_i`, find the smallest set of vertices
from which all nodes in the graph are reachable. It is guaranteed that a
unique solution exists. The vertices may be returned in any order.

```
n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]   ->  [0,3]
n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]   ->  [0,2,3]
```

**Constraints:** `2 <= n <= 10^5`; `1 <= edges.length <= min(10^5,
n(n - 1) / 2)`; `0 <= from_i, to_i < n`; all pairs are distinct.

## Approaches

A node with an edge into it is reached from wherever that edge starts,
and in an acyclic graph following edges backwards always ends at a node
with none. So the nodes no edge ends at are exactly the ones every answer
needs, and all an answer needs.

| file | mechanism |
|---|---|
| `vertices.kara` ★ | each edge marks its end in a `Vec.filled(n, false)`; the unmarked nodes are the answer. O(n + e) |
| `vertices_set.kara` | the same characterization as a `Set[i64]` of every edge's end, collected from a `map`, and the nodes `filter`ed out of it. O(n + e) expected |
| `vertices_reach.kara` | the statement worked forward: the nodes taken in topological order (Kahn's, a `VecDeque` collected from a `filter`), and a node still unreached when its turn comes is chosen and everything it reaches is marked by a walk on a stack. A node with an edge in is reached before its turn, so only the sources are chosen. O(n + e) |
| `vertices_solution.kara` | LeetCode's Rust template (`find_smallest_set_of_vertices(n: i32, edges: Vec<Vec<i32>>) -> Vec<i32>`, the ★ arm with `vec![false; n as usize]` and a `filter` over `0..n`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Any order is accepted, so every answer is read sorted. Every arm prints
the same 10 lines: LeetCode's two examples, then `n = 2` with `[(1, 0)]`,
a chain, three edges into one node, three out of one node, and
`n = 5` with two edges; then the count of sources and a checksum for 3000
random acyclic graphs of up to 8 nodes, 300 of up to 1000 and 30 of up to
100000, each edge from earlier to later in a random order of the nodes.
`vertices.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of nodes tried, fewest first, each grown along the
edges until nothing changes, the first that reaches every node the
answer (the smallest is unique). It checks 3000 acyclic graphs of 2 to 8
nodes, each edge from earlier to later in a random order of the nodes,
every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is nonempty, distinct, and names nodes of the graph |
| P3 | the edges given in reverse order leave the answer |
| P4 | every node `v` renamed `n - 1 - v` renames the answer |
| P5 | a new node with an edge to every node of the answer is the answer alone |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 856260384, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each edge marks its start, not its end | P1 3000, P5 3000, P6 3000 |
| M2 | ★: node 0 never a source | P1 1932, P2 241, P4 2763, P6 1932 |
| M3 | ★: the marked nodes taken | P1 3000, P5 3000, P6 3000 |
| M4 | set: the edges' starts collected | P1 3000, P5 3000, P6 3000 |
| M5 | set: the last node never a source | P1 1888, P2 242, P4 2763, P5 3000, P6 1888 |
| M6 | reach: the walk marks nothing it reaches | P1 3000, P5 3000, P6 3000 |
| M7 | reach: nodes with one edge in ready from the start | P1 1625, P4 2811, P5 3000, P6 1625 |
| M8 | reach: node 0 recorded for every choice | P1 2759, P2 2470, P4 3000, P5 3000, P6 2759 |
| M9 | template: each edge marks its start | P1 3000, P5 3000, P6 3000 |
| M10 | template: node 0 never a source | P1 1932, P2 241, P4 2763, P6 1932 |

## Benchmarks

The bench builds 20 acyclic graphs of 100000 nodes once, each from
300000 drawn pairs kept when they run from earlier to later in a random
order of the nodes (so about 150000 edges, and a pair may repeat, which
the arm does not mind), and asks each 20 times by the ★ arm, in all five
languages. Every call allocates its marks and its list of sources. Every
implementation prints `20 passes over 20 graphs of 100000 nodes:
12670940 sources, checksum 110821411`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.365 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.384 s |
| Kāra (`karac build`) | 0.384 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.394 s |
| Rust (`rustc -O`) | 0.403 s |
| Go | 0.703 s |
| Python | 11.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.38 s and 0.39 s on one run).

Kāra is 1.03x Rust under overflow checks by median. Not traced. The
calls are a scattered write per edge and a scan of 100000 marks, and the
graphs' construction is a share of every row; the compiled rows but Go's
sit within 10% of each other.

## Verification

All four arms print the same output as `vertices.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, set and reach arms were written in Kāra and checked as written.

The Rust template took five rounds of `karac fix`, 4 changed lines, then
1 added, then 2, 3 and 3 changed:

1. the `Vec<..>` types to `Vec[..]`, `|&v| !has_in[..]` to
   `|v| not has_in[..]`, the wrapper's `|&(a, b)|` and `|&v|` to `|(a, b)|`
   and `|v|`, and `Solution::` to `Solution.`;
2. `struct Solution {}` added, after which the template checked, with two
   `deprecated vec![..]` warnings;
3. `vec![false; n as usize]` to `Vec.filled(n as usize, false)` and the
   wrapper's `vec![a as i32, b as i32]` to a list literal, after which the
   template was refused: the `as usize` length, and the `as usize` index
   that had checked a round before, now mix `usize` with `i64`;
4. every `as usize` to `as i64`;
5. those casts dropped (an `i32` widens).

So one round turned a checking program into a refused one, and the next
two brought it back. `vec![v; n]` does not check its count the way
`Vec.filled` checks its length, so the `usize` rule only reaches the
program after the rewrite; filed as B-2026-11-14-13. It checks and agrees
with no hand edit.
