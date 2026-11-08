# 1530. Number of Good Leaf Nodes Pairs

You are given the `root` of a binary tree and an integer `distance`. A
pair of two different leaf nodes of a binary tree is said to be good if
the length of the shortest path between them is less than or equal to
`distance`. Return the number of good leaf node pairs in the tree.

```
root = [1,2,3,null,4],                         distance = 3  ->  1
root = [1,2,3,4,5,6,7],                        distance = 3  ->  2
root = [7,1,4,6,null,5,3,null,null,null,null,null,2], distance = 3  ->  1
```

**Constraints:** the tree has 1 to 2^10 nodes; `1 <= Node.val <= 100`;
`1 <= distance <= 10`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | a walk after the children returns, for each node, how many leaves sit each number of edges below it (up to the distance). Two leaves meet at the one node whose two sides hold them, so each node counts the pairs across its sides whose depths add up to at most the distance. O(n d^2) |
| `pairs_paths.kara` | each leaf's path from the root as its turns; two leaves part where their paths first differ, so every pair is measured as both lengths less twice the shared start. O(L^2 h) for L leaves and height h |
| `pairs_graph.kara` | the tree as an undirected graph: from every leaf a breadth-first search out to the distance counts the other leaves it reaches, and the total is halved. O(L n) |
| `pairs_iter.kara` | the ★ arm with iterator adapters: the pairs across a node by `enumerate`, `take` and `sum`, the counts one level up by `once`, `chain`, `zip` and `take` |
| `differential.kara` | the four arms against the statement read literally, six properties |

There is no LeetCode Rust template arm. LeetCode's template takes
`Option<Rc<RefCell<TreeNode>>>`, and `karac fix` carries it to
`import std.rc.Rc` and `Option[Rc[RefCell[TreeNode]]]`, then stops at
`unknown module std.rc` with no word of `shared struct`, which is how
Kāra spells a reference-counted node. Filed as B-2026-11-08-65; the arm
joins once a fix carries the template.

The tree is a `shared struct TreeNode` with `Option[TreeNode]` children,
as in katas 226 and 998. Every arm prints the same 8 lines: LeetCode's
three examples, a single node and two two-leaf trees, then checksums of
the answers for 3000 random trees of 1 to 12 nodes and 300 of 1 to 1024,
each with a distance from 1 to 10. A random tree adds each node by
walking down from a random node, a random way at each step, to the first
free place. `pairs.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the tree's edges between numbered nodes, every shortest path
by Floyd-Warshall, and every pair of leaves asked. It checks 3000 trees
of 1 to 10 nodes, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the tree mirrored has the same answer |
| P3 | the answer does not fall as the distance grows by one, and at twice the node count every pair of leaves is good |
| P4 | the answer is at least 0, at most the pairs of leaves, and 0 at distance 1 |
| P5 | a new root over the tree and one more leaf adds the tree's leaves within distance - 2 edges of its root |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 35136813, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Ten are killed, each
the same way under both backends; one survives, and it is equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: pairs one edge too far counted | P1 389, P4 564, P5 535, P6 389 |
| M2 | ★: the right side's counts lifted from one level too deep | P1 987, P2 1015, P3 1368, P5 1455, P6 987 |
| M3 | ★: a leaf counted twice | P1 1454, P3 1939, P4 1424, P5 2118, P6 1454 |
| M4 | paths: the shared start taken off once, not twice | P1 290, P5 321, P6 290 |
| M5 | paths: each leaf paired with itself | P1, P3, P4, P5, P6 3000 each |
| M6 | graph: the search stopped one edge short | P1 352, P5 517, P6 352 |
| M7 | graph: each pair counted from both ends | P1 1454, P3 1939, P4 1284, P5 2118, P6 1454 |
| M8 | graph: the start counted as a leaf it reaches | P1 1939, P3 1939, P4 1939, P5 1818, P6 1939 |
| M9 | iter: pairs one edge too far counted | P1 389, P4 564, P5 535, P6 389 |
| M10 | iter: the counts not moved down a level | P1 558, P5 880, P6 558 |

The survivor is the ★ arm not filling the deepest count (M11): a leaf
`distance - 1` below a node is at least `distance + 1` from any leaf
across it, and moving up only pushes it further, so that count is never
read.

## Benchmarks

The bench builds 1000 random trees of 1 to 1024 nodes once, each with a
distance from 1 to 10, and answers each 10 times by the ★ arm, in all
five languages. Each node's counts are a fresh list, as the arm returns
them (`calloc` and `free` in C). The Rust tree is LeetCode's
`Option<Rc<RefCell<TreeNode>>>`. Every implementation prints `10 passes
over 1000 trees of up to 1024 nodes: checksum 653462042`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.190 s |
| Kāra (`karac build`) | 0.265 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.270 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.282 s |
| Rust (`rustc -O`) | 0.296 s |
| Go | 0.383 s |
| Python | 4.57 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.28 s and 0.30 s on one run).

Kāra is 0.96x Rust under overflow checks by median. Not traced. Building
the trees is part of every time.

## Verification

All four arms print the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The four arms were written in Kāra and checked as written. The harness
took two edits from `karac fix`: an f-string interpolation that wrote
`join(\",\")` with escaped quotes (refused, with the plain-quote form as
the fix), and a `.to_string()` dropped from `"null"` where a branch's
other side is a `String`.
