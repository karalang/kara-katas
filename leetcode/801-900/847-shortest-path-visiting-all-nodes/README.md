# 847. Shortest Path Visiting All Nodes

There is an undirected, connected graph of `n` nodes labelled `0` to
`n - 1`, given as `graph`, where `graph[i]` lists the nodes joined to
node `i` by an edge. Return the length of the shortest walk that visits
every node. The walk may start and stop at any node, revisit nodes and
reuse edges.

```
graph = [[1,2,3],[0],[0],[0]]               ->  4   (1, 0, 2, 0, 3)
graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]     ->  4   (0, 1, 4, 2, 3)
```

**Constraints:** `1 <= n <= 12`, `0 <= graph[i].length < n`, no node
lists itself, `j` is in `graph[i]` exactly when `i` is in `graph[j]`,
and the graph is connected.

## Approaches

| file | mechanism |
|---|---|
| `shortest_path_length.kara` ★ | breadth-first search over states: a walk's future depends only on the node it stands on and the set of nodes it has visited, so those pairs, `n * 2^n` of them, are the states; every node alone is a start at distance 0, a step moves to a neighbour and adds it to the set, and the search from all the starts at once meets the states in order of distance, the first whose set holds every node ending the shortest walk. O(2^n * n^2) |
| `shortest_path_length_tsp.kara` | all-pairs distances, then a travelling-salesman table: Floyd-Warshall gives every distance; a shortest walk meets the nodes for the first time in some order and goes the shortest way between them, so `best[set][v]`, the shortest walk that has met exactly `set` and stands on its last node `v`, extends to each node `w` not yet met for `dist[v][w]`, the sets filled in order of their bitmasks. O(n^3 + 2^n * n^2) |
| `shortest_path_length_memo.kara` | breadth-first distances, then a memoized recursion: `rest(set, v)`, the shortest walk from `v` that meets every node outside `set`, is none when `set` is every node, else the best over the next new node `w` of `dist[v][w] + rest(set + w, w)`, each state worked out once and kept. O(n * (n + e) + 2^n * n^2) |
| `shortest_path_length_levels.kara` | the ★ arm's states packed into one integer each, `set * n + node`, and searched a whole level at a time: the next level is every unseen neighbour state of this one, and the first level holding a state with every node gives the answer. O(2^n * n^2) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 18 lines: LeetCode's two examples; seven more
(one node, two, a triangle, a path of four, a square, and two trees of
six, one with three leaves on its root and one with two pairs of
leaves); eight graphs of LeetCode's most nodes, 12: a path, a cycle, a
hub with 11 spokes, all 66 edges, a broom of a handle of six and six
bristles, and random trees with 0, 4 and 30 random edges more; and 300
random connected graphs of up to nine nodes, with the sum of their
answers and a checksum. `shortest_path_length.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every walk of 0 steps is tried from every node, then every
walk of 1 step, and so on, and the first length at which some walk has
visited every node is the answer. Its 1,600 cases of up to seven nodes
are random trees, each node joined to an earlier one, in four kinds of
400: the tree alone; the tree and up to two random edges more; the tree
and `n^2` random edges, which comes near a complete graph; and the tree
and about half of all the other pairs. Their answers sum to 5,341.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the nodes renamed by a random permutation give the same answer |
| P3 | one more edge never makes the answer longer |
| P4 | a new node joined to one node only makes the answer one or two steps longer: a walk of the new graph that leaves out each trip to the new node is a walk of the old one, at least one step shorter, and the old walk with one trip there and back added visits it |
| P5 | the answer lies between `n - 1`, a step to each new node, and `2(n - 1)`, a walk around a spanning tree |

It prints `1600 cases, lengths sum to 5341, 32000 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search started from node 0 only | P1 458, P2 381 |
| M2 | ★: a step adding the node it leaves, not the one it reaches | P1 1391 |
| M3 | ★: steps counted from 1 | P1 1600, P5 209 |
| M4 | tsp: a detour counted one step long | P1 308, P4 279, P5 2 |
| M5 | tsp: the answer read at the last node only | P1 42, P2 259, P4 49 |
| M6 | tsp: walks starting at node 0 only | P1 458, P2 381 |
| M7 | memo: every node's result stored under node 0 | P1 461, P2 392 |
| M8 | memo: the first next node kept | P1 287, P2 500, P4 230, P5 1 |
| M9 | memo: the walk started at node 0 only | P1 458, P2 381 |
| M10 | levels: the goal counted one level late | P1 1600, P5 209 |
| M11 | levels: the goal not requiring the last node | P1 1378, P4 222, P5 1203 |
| M12 | levels: node 0 taken as visited from the start | P1 954, P2 366, P4 220, P5 904 |

P1 kills all twelve. The three arms started from node 0 alone (M1, M6,
M9) fail the same 458 cases, those where no shortest walk can start
there. P2 sees every edit that treats one node apart from the rest, node
0 or the last (M1, M5 to M9, M12), since renaming moves which node that
is. P4 sees the edits whose mistake grows or shrinks with the graph, so
that the new node's cost comes out wrong; P5 sees the steps counted one
too many where the answer was already at its bound (M3, M10, among them
every graph of one node), and the walks that skip a node (M11, M12),
which can come in under `n - 1`.

P3 kills nothing: none of the twelve edits gave a longer answer to any
of these graphs with an edge added.

One first draft was replaced: in the levels arm, reading a state's node
out of its packed set sent the search to the wrong neighbours, and with
no level ever reaching every node it never ended.

## Verification

Every arm prints the same output as `shortest_path_length.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `0cf32f3e6f`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 1.2 to 2.1 s
and the differential 24 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends refuse every arm, the differential and the
bench program at a neighbour read as `*w` through `graph[v].iter()`:
legacy types the loop variable as an `i64`, not a reference, though
`karac check` accepts it on v2. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
graphs once, each of LeetCode's most nodes, 12: a random tree, each node
joined to an earlier one, and then `g % 16 * 3` random edges more for
graph `g`, so from trees to graphs near complete. Each of 4,000 rounds
asks the next graph. Every implementation prints `4000 rounds of 64
graphs: lengths sum to 46750, checksum 848431315`, the Kāra program
under `karac __mir-run` included, in 547 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.11 to 1.28 s |
| Rust (`rustc -O`) | 1.39 to 1.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.48 to 2.15 s |
| Go | 3.87 to 4.96 s |
| Python | 30.0 to 31.7 s |
| Kāra (`karac build --mir`) | 2.35 to 2.73 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 2.49 s, against Rust's
1.49 (1.59 under overflow checks), C's 1.22 and Go's 4.29: 1.57 times
Rust's time under overflow checks, 2.04 times C's and 0.58 times Go's.
Under valgrind's cachegrind v2 runs 16.9 billion instructions and 3.51
billion branches, 134 million of them indirect, against Rust's 7.25
billion and 1.45 billion and C's 4.44 billion and 931 million, though
the three mispredict about alike, 118, 119 and 111 million. So v2's
extra time is most likely the extra instructions around the queue of
three-number states and the `seen` table, the work the search repeats
for every state, but where they come from was not traced. C keeps its
queue in one array allocated at full size, where Rust's `VecDeque` and
v2's grow; Go's slice grows by appending too, and Go is the slowest (not
traced). Built for `x86-64-v3`, the target `karac build` uses, C takes
1.18 to 1.26 s and Rust with overflow checks 1.77 to 2.00 s, against
v2's 2.46 to 2.62 s in the same five interleaved runs. Python takes 30.5
s, about 25 times C's time. The comparison with C and Rust waits until
after M4.
