# 2065. Maximum Path Quality of a Graph

There is an undirected graph with `n` nodes numbered from `0` to `n - 1`
(inclusive). You are given a 0-indexed integer array `values` where
`values[i]` is the value of the `i`-th node. You are also given a
0-indexed 2D integer array `edges`, where each `edges[j] = [u_j, v_j,
time_j]` indicates that there is an undirected edge between the nodes
`u_j` and `v_j`, and it takes `time_j` seconds to travel between the two
nodes. Finally, you are given an integer `maxTime`.

A valid path in the graph is any path that starts at node `0`, ends at
node `0`, and takes at most `maxTime` seconds to complete. You may visit
the same node multiple times. The quality of a valid path is the sum of
the values of the unique nodes visited in the path (each node's value is
added at most once to the sum).

Return the maximum quality of a valid path.

**Note:** There are at most four edges connected to each node.

```
values = [0,32,10,43], edges = [[0,1,10],[1,2,15],[0,3,10]], maxTime = 49  ->  75
values = [5,10,15,20], edges = [[0,1,10],[1,2,10],[0,3,10]], maxTime = 30  ->  25
values = [1,2,3,4], edges = [[0,1,10],[1,2,11],[2,3,12],[1,3,13]], maxTime = 50  ->  7
```

**Constraints:** `n == values.length`; `1 <= n <= 1000`;
`0 <= values[i] <= 10^8`; `0 <= edges.length <= 2000`;
`edges[j].length == 3`; `0 <= u_j < v_j <= n - 1`;
`10 <= time_j, maxTime <= 100`; all the pairs `[u_j, v_j]` are unique;
there are at most four edges connected to each node; the graph may not
be connected.

Every edge takes at least 10 and the time is at most 100, so a walk has
at most 10 edges, and with at most four edges at a node there are at
most `4^10`, about a million, walks to try: a plain search over all of
them fits. What makes it a search and not a sum is that a node's value
counts once however often the walk comes back to it, so the search
keeps which nodes the walk has stood on, and takes a visit back on the
way out. The approaches differ in how they keep that, and in which walks
they skip.

## Approaches

| file | mechanism |
|---|---|
| `quality.kara` ★ | a depth-first search over every walk from 0 that keeps within the time: a count of visits per node adds a value on its first visit only and takes it back on the way out; the best quality is taken at each arrival at 0 |
| `quality_stack.kara` | the same search with no recursion: a `Vec` of `Frame`s (a node, the time and quality on arriving there, the next edge to try), a struct deriving `Copy`; a frame whose edges are spent is popped and its visit taken back |
| `quality_prune.kara` | the search pruned by the way home: Dijkstra's shortest times from 0 from a min-first `PriorityQueue`, and a step taken only when the walk can still get back to 0 in time from where it lands; a `Vec[bool]` of nodes seen, undone by the visit that set it |
| `quality_levels.kara` | breadth first, one edge a round: every walk so far kept whole, as the node it stands at, its time and the `SortedSet` of nodes it has visited, and each extended by every edge that keeps within the time; a walk's quality is its set's values summed |
| `quality_struct.kara` | the search as a value: a `struct Search` owning a list of `Edge`s per node, the values, the time, the visit counts and the best so far, and a method `walk(mut ref self, ..)` recursing through it |
| `quality_solution.kara` | LeetCode's Rust template (`values: Vec<i32>`, an adjacency `vec![vec![]; n]` of `(usize, i32)`, a nested `fn dfs` taking `&[i32]`, `&Vec<..>`, `&mut Vec<i32>` and `&mut i32`, `as usize` indices), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each graph's size, time and answer; then the sum of the answers
and a checksum for 400 random graphs of 1 to 30 nodes, up to 60 edges
tried, each from a node to one of the next three with no node on more
than four and no edge twice, times 10 to 50, values up to 10 or
`10^8`, and a time of 10 to 100; then the answer for a graph of 1000
nodes, 2000 edges tried and a time of 100. `quality.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every walk from 0 written out as its list of nodes, one edge
longer each round while it keeps within the time, and of those that end
at 0, the best sum of the values of the different nodes on it. It checks
300 random graphs of 1 to 8 nodes, edges between any two with no node on
more than four, times 10 to 50 and a time of 10 to 100; then 20 with
every edge 10 and a time of 60, so a walk can take six edges. All 320
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the nodes other than 0 numbered backwards have the same answer |
| P3 | ten more time never lowers the answer |
| P4 | an edge taken away never raises the answer |
| P5 | the answer is at least node 0's value and at most all the values added |
| P6 | each arm agrees with at least three of the other five |

The differential prints `320 graphs: checksum 699690986, 11520 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
graphs. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, four to seven to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivor under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node's value added on every visit | P1 129, P5 48, P6 129 |
| M2 | ★: the best taken anywhere, not only at 0 | P1 139, P6 139 |
| M3 | ★: node 0 not counted visited at the start | P1 126, P5 34, P6 126 |
| M4 | stack: the walk of no edges not counted | P1 172, P5 172, P6 172 |
| M5 | stack: a node's last edge never tried | P1 108, P6 108 |
| M6 | stack: a value added again on a second visit | P1 129, P5 41, P6 129 |
| M7 | prune: a first visit never undone | P1 10, P3 2, P6 10 |
| M8 | prune: every way home ten longer | P1 49, P6 49 |
| M9 | prune: the walks' qualities added | P1 131, P5 74, P6 131 |
| M10 | levels: a walk's nodes never added to | P1 133, P6 133 |
| M11 | levels: the best single value, not the sum | P1 124, P6 124 |
| M12 | levels: each node's first edge never taken | P1 114, P6 114 |
| M13 | struct: a visit never taken back | P1 36, P3 17, P4 6, P6 36 |
| M14 | struct: a walk using the whole time refused | P1 9, P6 9 |
| M15 | struct: a value half counted on a revisit | P1 124, P5 36, P6 124 |
| M16 | solution: a value added on the second visit only | P1 127, P5 18, P6 127 |
| M17 | solution: the adapter's values backwards | P1 218, P2 219, P5 63, P6 218 |

P1 and P6 kill all seventeen, P5 eight, P3 two, and P2 and P4 one each.
P5's upper bound sees a value counted more than once (M1, M6, M9, M15,
M16) and its lower bound a walk that never counts node 0 (M3, M4). P3
and P4 see a visit that is never taken back (M7, M13): a node wrongly
left seen keeps its value from counting on a later walk, so a longer
time or one edge fewer can change which walk finds it first, and the
answer moves the wrong way. P2 sees only the adapter that hands the
values over backwards (M17), the one edit that ties the answer to the
nodes' numbers; every arm reads the graph through its edges alone.

Of the thirty-one, fourteen were not kept. One survives, and it is
equivalent: the prune arm with no pruning, which still takes its best
only at 0, so the walks it no longer skips are the ones that never get
home and add nothing. Thirteen fail as a kept one: the stack arm's value
added on every visit as M1; the ★, stack and Rust arms' visit never
taken back as M13; the struct arm's best taken anywhere as M2; the ★ and
levels arms' walk using the whole time refused, and the prune arm's way
home using the whole time refused, as M14; the levels arm's node 0 left
out of the first walk as M4; the Rust arm's adapter time ten short and
the stack arm's ten units of time held back as M8; the prune and Rust
arms' node 0 not counted at the start as M3.

## Verification

Every arm prints the same output as `quality.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.35 s to 0.46 s and the
differential 1.1 s (timed while other work shared the machine).

No arm met a compiler gap. The stack arm's `Frame` was written with
`#[derive(Copy)]`, and `karac fix` added the `Clone` it needs.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in four rounds of 24, 2, 5 and 3 edits: Rust's spellings (`Vec<..>`
to brackets, `&[i32]` to `Slice[i32]`, `&mut` to `mut ref` and a `mut`
marker at each call, the `&` of `&(v, t)` and `&edges` dropped,
`struct Solution;` to `struct Solution {}`, `Solution::` to
`Solution.`); then the nested `fn dfs` hoisted out of the method (it
captures nothing); then `0i32` for the visit counts and `ans: i32`, whose
literals kept the default `i64`, and the remaining `mut` markers; then
the two `vec![..]` to `Vec.filled`, a lint `karac check` allows. The
fixed arm reads as the template does, `usize` nodes and all.

## Benchmarks

The bench answers 1000 graphs of 1000 nodes with the ★ arm in all five
languages: 2000 edges tried, each from a node to one of the next three,
times 10 or 11, a time of 100, so nearly every walk takes nine or ten
edges and every node has close to four. C keeps four adjacency slots per
node and drops a repeated edge by a linear look; Rust and Go a
`HashSet` / `map` of the edges seen, as the Kāra harness's `Set`. Every
implementation prints `1000 graphs: sum 415722591277, checksum
150833110`.

BENCHTAB
