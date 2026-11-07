# 1059. All Paths from Source Lead to Destination

Given the `edges` of a directed graph on nodes `0` to `n - 1`, where
`edges[i] = [a, b]` is an edge from `a` to `b`, and two nodes `source` and
`destination`, decide whether every path starting at `source` ends at
`destination`:

- at least one path leads from `source` to `destination`;
- any path from `source` that reaches a node with no outgoing edge reaches
  `destination` there;
- the number of paths from `source` to `destination` is finite.

```
n = 3, edges = [[0,1],[0,2]], source = 0, destination = 2                ->  false
n = 4, edges = [[0,1],[0,3],[1,2],[2,1]], source = 0, destination = 3    ->  false
n = 4, edges = [[0,1],[0,2],[1,3],[2,3]], source = 0, destination = 3    ->  true
```

**Constraints:** `1 <= n <= 10^4`; `0 <= edges.length <= 10^4`; the
graph may have self-loops and parallel edges.

The second example settles how "finite" reads: `0 -> 1 -> 2 -> 1` never
reaches 3, yet the answer is false because a walk can go round `1 <-> 2`
for ever. So every walk from `source` must stop, and stop at
`destination`.

## Approaches

Every walk from `source` stops at `destination` exactly when no cycle is
reachable from `source` and every reachable node without an outgoing edge
is `destination`.

| file | mechanism |
|---|---|
| `paths.kara` ★ | an iterative depth-first search with three colours and its own stack of (node, next edge): a node met again while on the path closes a cycle, a node with no edge must be the destination. O(n + e) |
| `paths_recursive.kara` | the same search as recursion, a finished node keeping its answer; a path of 10000 nodes recurses 10000 deep. O(n + e) |
| `paths_kahn.kara` | a breadth-first search for the reached nodes, then Kahn's algorithm over the edges between them: they have no cycle when it removes them all. O(n + e) |
| `paths_reverse.kara` | safe nodes found backward from the destination: a node is safe once each of its edges leads to a safe one, counted down over the reversed edges. O(n + e) |
| `paths_map.kara` | a recursive search over a `Map` of successors, a `Set` of the nodes on the path and a `Map` of finished answers. O(n + e) expected |
| `paths_enum.kara` | a recursive search matching on an `enum State`, written the way Rust writes it and carried to Kāra by `karac fix`. O(n + e) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's three
examples and seven more; how many of 3000 random graphs of 1 to 8 nodes
and of 3000 graphs of 1 to 12 nodes leaning toward the last node lead
there, with a checksum of the answers; the same for 100 leaning graphs of
10000 nodes (about 10600 edges each, a little past the constraint); every
source of one graph of 2000 nodes; and a path of 10000 nodes, open and
then closed into a cycle. `paths.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every walk from `source`, extended edge by edge, where a walk
of `n` edges has met some node twice and so can go round for ever, and a
walk that stops must stop at `destination`. It checks 3000 problems: 1500
of 1 to 9 nodes with up to 14 edges anywhere, self-loops and parallel
edges included, and 1500 graphs leaning toward their last node, of 1 to 9
or 1 to 60 nodes.

| | property |
|---|---|
| P1 | the answer is the statement read literally (9 nodes or fewer) |
| P2 | the nodes renamed by a random permutation leave the answer |
| P3 | the edges listed in reverse, or a node added that nothing reaches with edges into the graph, leave the answer |
| P4 | every edge doubled leaves the answer |
| P5 | when every path leads to the destination, an edge added from a node the source reaches to the destination leaves it true, and an edge out of the destination makes it false |
| P6 | each arm agrees with at least three of the other five |

The differential prints `3000 problems: checksum 835049432, 120246 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a dead end tested against the wrong node | P1 1396, P5 1139, P6 1937 |
| M2 | ★: a finished node taken for a cycle, a cycle missed | P1 660, P4 756, P5 1894, P6 844 |
| M3 | ★: the destination never searched | P1 67, P5 991, P6 67 |
| M4 | recursive: a finished node answered false | P1 53, P4 288, P6 124 |
| M5 | recursive: the first edge of each node ignored | P1 452, P3 163, P4 537, P5 1842, P6 537 |
| M6 | kahn: parallel edges counted once | P1 78, P5 734, P6 84 |
| M7 | kahn: the destination never explored | P1 492, P5 5, P6 928 |
| M8 | kahn: a node with one edge in taken as ready | P1 419, P4 840, P5 8, P6 840 |
| M9 | reverse: a destination with edges still safe | P1 468, P5 1796, P6 468 |
| M10 | reverse: only one step backward | P1 167, P6 412 |
| M11 | map: every dead end accepted | P1 556, P5 904, P6 699 |
| M12 | map: only the last edge of each node kept | P1 33, P3 154, P6 83 |
| M13 | enum: a node on the path marked finished, cycles missed | P1 812, P5 2002, P6 825 |
| M14 | enum: a dead end past the destination accepted | P1 236, P2 352, P5 347, P6 236 |
| M15 | enum: only the first two edges followed | P1 19, P3 26, P4 113, P6 24 |

P1 and P6 kill all fifteen, P5 eleven, P4 five, P3 three and P2 one. P5 sees
every edit that lets a cycle or a wrong dead end through, since the edge
it adds out of the destination must turn a true answer false. P4 sees the
edits that take a node met twice for a cycle (M2, M4), which doubling
the edges makes common, and those that depend on how many edges a node has
(M5, M8, M15). P3 sees the edits that drop
an edge by its place in the list (M5, M12, M15), whose answer then
depends on the order. P2 sees only M14: a dead end accepted when its
number is at least the destination's changes with the names.

Most of the other fifteen fail as kept ones do. Three miss a cycle as
M13 does (the recursive arm marking a node on the path finished, the map
and enum arms accepting a cycle), the recursive arm accepting every dead end fails as M11, a
finished node left on the path (recursive) or answered false (enum) fails
as M4, and the map arm ignoring the first edge fails as M5. The reverse
arm never settling the source fails as its edges not reversed do, and
counting each node as one edge there fails as the map arm needing only
one edge that leads. The rest fail in groups of their own: the ★ arm
skipping its last edge or accepting a dead-end source, Kahn's forgiving
one node left on a cycle or never examining the last node reached.

## Verification

Every arm prints the same output as `paths.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. Under `karac __mir-run` the arms take
6.0 s (Kahn's) to 13.0 s (map), the differential 3.7 s, all at kara
`01b60e526c`.

The ★ arm and four others were written in Kāra and checked clean. The
enum arm was written the way Rust writes it (`&Vec<Vec<usize>>`, `&mut
Vec<State>`, `State::Visiting`, `for &v in &adj[u]`, `vec![State::Unvisited;
n]`, `as usize` casts) and reaches a clean check through `karac fix`
alone. It takes four rounds: the `::` paths, `&` and `<..>` first, then
the call-site `mut`, then the `usize` the casts left behind.

## Benchmarks

The bench builds 20 graphs of 2000 nodes leaning toward the last node
once in all five languages, then asks the ★ arm whether every source of
each graph leads to node 1999. Every implementation prints `40000 calls:
21940 lead, checksum 326470932`. Each call builds the graph's 2000
adjacency lists from about 2500 edges before it searches, as the
LeetCode signature asks, and that dominates: Python is only about 3x the
compiled languages.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `01b60e526c` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 2.220 to 2.543 s | 2.364 s |
| Rust (`rustc -O`) | 2.596 to 2.806 s | 2.656 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.585 to 2.959 s | 2.695 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.634 to 2.841 s | 2.770 s |
| Kāra (`karac build`) | 2.615 to 2.901 s | 2.782 s |
| Go | 3.204 to 3.659 s | 3.470 s |
| Python | 7.22 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (2.758 s) is below its real time. Kāra matches Rust under
overflow checks, and C is ahead of both by about 0.3 s.
