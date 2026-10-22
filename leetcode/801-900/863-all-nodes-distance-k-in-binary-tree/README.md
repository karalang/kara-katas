# 863. All Nodes Distance K in Binary Tree

Given the `root` of a binary tree, the value of a `target` node in the
tree, and an integer `k`, return an array of the values of all nodes
that are at distance `k` from the target node. The answer may be in any
order; here it is given in increasing order.

```
root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2  ->  [1, 4, 7]
root = [1], target = 1, k = 3                             ->  []
```

**Constraints:** the tree has 1 to 500 nodes; `0 <= Node.val <= 500`;
all values are unique; `target` is the value of a node in the tree;
`0 <= k <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `distance_k.kara` ★ | a tree only points down, so one walk records every node's parent, by value, and finds the target. The tree is then an undirected graph, and a breadth-first search from the target over left, right and parent, never stepping back onto a node already reached, stops after k steps: the level it stands on is the answer. O(n) time and space |
| `distance_k_graph.kara` | every edge in an adjacency list indexed by value, both ways, and the distance of every node from a breadth-first search with a `VecDeque`; the nodes at distance k are read off in order of value. O(n + m) time, m the largest value |
| `distance_k_search.kara` | one recursive search, no parents kept: it returns how far below a node the target is, or -1. At the target it collects the nodes k levels down; an ancestor d steps above the target is an answer when d is k, and otherwise the answers through it lie k - d - 1 levels down its other child. O(n) time, O(height) stack |
| `distance_k_path.kara` | the path from the root to the target found first, then each ancestor d steps up it tried in turn: itself when d is k, else a level-by-level walk k - d - 1 levels down its child off the path. O(n) time |
| `distance_k_lca.kara` | one walk records each node's parent and depth, by value; every node's distance from the target is found by climbing from the deeper of the two until they meet, and kept when it is k. O(n * height) time |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples; eight more
(k of 0, the root and three leaves as targets, k past the tree's height,
and two chains); four queries on a random 500-node tree,
LeetCode's largest, with the number found and a checksum; and 23,778
queries, every target and k from 0 to 5 in 200 random trees of 1 to 40
nodes, which find 55,711 nodes. `distance_k.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the distance between every pair of nodes from Floyd-Warshall
over the tree's edges, and the target's row read at k. Its 496 trees are
every shape of one to six nodes (196 of them), each with its values
shuffled, and 300 random trees of up to twelve nodes; the 16,838 queries
are every target with every k up to n for the shapes and up to 4 for the
random trees, and find 19,568 nodes.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | at distance 0 there is the target alone |
| P3 | distance is symmetric: the target is at distance k from each node found |
| P4 | the mirrored tree gives the same answer |
| P5 | every value raised by n, the target's too, raises every value found by n |
| P6 | over every k from 0 to n - 1, each node is found exactly once (one random target per tree) |

It prints `496 trees, 16838 queries, 19568 nodes found, 367960 checks
over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

P5 was first written as "a target not in the tree finds nothing", and
the graph arm failed it: its adjacency list is sized by the largest value
in the tree, and a target past it indexes out of range. LeetCode
guarantees that the target is in the tree, so that query is outside the
problem and the property was replaced by the shifted values, which also
moves the largest value the graph arm sizes its list by.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no step up to a parent | P1 8415, P4 8415, P5 8415, P6 376 |
| M2 | ★: the target not marked as reached | P1 2988, P3 2988, P4 2988, P5 2988, P6 449 |
| M3 | ★: one step short | P1 12091, P3 17416, P4 12091, P5 12091, P6 470 |
| M4 | graph: each edge one way only | P1 8415, P4 8415, P5 8415, P6 376 |
| M5 | graph: each edge counted twice | P1 12303, P3 10724, P4 12303, P5 12303, P6 365 |
| M6 | graph: the largest value never read | P1 2820, P2 496, P4 2820, P5 2820, P6 496 |
| M7 | search: nothing below the target collected | P1 7181, P2 3014, P4 7181, P5 7181, P6 496 |
| M8 | search: an ancestor on the left never counted | P1 2899, P4 2900, P5 2899, P6 280 |
| M9 | search: down the wrong child from the right | P1 4963, P3 6264, P4 4971, P5 4963, P6 261 |
| M10 | path: down the child on the path | P1 8470, P3 12520, P4 8470, P5 8470, P6 364 |
| M11 | path: the ancestor k steps up left out | P1 8813, P2 3014, P4 8813, P5 8813, P6 496 |
| M12 | path: one level short | P1 9472, P3 11906, P4 9472, P5 9472, P6 470 |
| M13 | lca: a step counted before the climb | P1 15105, P2 3014, P3 17416, P4 15105, P5 15105, P6 124 |
| M14 | lca: every node within k | P1 13824, P3 51094, P4 13824, P5 13824, P6 470 |
| M15 | lca: the largest value taken as absent | P1 2034, P2 496, P4 2034, P5 2034, P6 122 |

P1, P4, P5 and P6 each kill all fifteen. M1 and M4 are one fault, no
edge from a child up to its parent, and fail the same cases. P3 misses
the mutations that only lose nodes (M1, M4, M6, M7, M8, M11, M15): every
node they still find is at the right distance.

## Verification

Every arm prints the same output as `distance_k.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `d1dc5371df`. Under `karac
__mir-run` the arms take 1 to 8 s and the differential 50 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms, the differential and
the bench program at a `*` on a `for` element, or on the entry
`parent.get` returns, saying the value is not a reference, where v2
yields a reference. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: a random tree
of 500 nodes, LeetCode's largest, built once, and 200,000 queries, each
with a random target and a random k below 20. Every query records the
parents and runs the breadth-first search afresh. Rust uses LeetCode's
tree type, `Option<Rc<RefCell<TreeNode>>>`, with a `HashMap` and a
`HashSet`, and Go a map for each; C has no hash map, so its parents and
reached set are arrays indexed by value, which the values from 0 to 500
allow. Every implementation prints `200000 queries on 500 nodes: 3341514
nodes found, checksum 747446165`, the Kāra program under `karac
__mir-run` included, in 389 s.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.40 to 0.53 s | 0.42 s |
| Rust (`rustc -O`) | 6.71 to 7.04 s | 6.86 s |
| Rust (`rustc -O -C overflow-checks=on`) | 6.66 to 7.06 s | 6.79 s |
| Go | 11.17 to 12.19 s | 11.67 s |
| Python | 14.8 s | |
| Kāra (`karac build --mir`) | 4.71 to 5.28 s | 4.83 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 862's does. The frozen legacy `karac build`
refuses the bench program at the `*` on the entry `parent.get` returns,
so there is no legacy time.

v2 takes 0.71 times Rust's median time under overflow checks. Both hash
every parent and every reached node with SipHash-1-3, which is where the
time goes: under valgrind's cachegrind Rust with overflow checks runs
70.5 billion instructions and v2 62.5 billion, against C's 3.6 billion
with no hashing at all, so C's time is not a like-for-like comparison.
The comparison with C and Rust waits until after M4.
