# 1676. Lowest Common Ancestor of a Binary Tree IV

Given the `root` of a binary tree and an array of `TreeNode` objects
`nodes`, return *the lowest common ancestor (LCA) of **all the nodes** in*
`nodes`. All the nodes will exist in the tree, and all values of the
tree's nodes are unique.

Extending the definition of LCA on Wikipedia: "The lowest common ancestor
of `n` nodes `p1`, `p2`, ..., `pn` in a binary tree `T` is the lowest
node that has every `pi` as a **descendant** (where we allow **a node to
be a descendant of itself**) for every valid `i`". A descendant of a node
`x` is a node `y` that is on the path from node `x` to some leaf node.

```
root = [3,5,1,6,2,0,8,null,null,7,4], nodes = [4,7]       ->  2
root = [3,5,1,6,2,0,8,null,null,7,4], nodes = [1]         ->  1
root = [3,5,1,6,2,0,8,null,null,7,4], nodes = [7,6,2,4]   ->  5
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-10^9 <= Node.val <= 10^9`; all `Node.val` are unique; all
`nodes[i]` will exist in the tree; all `nodes[i]` are distinct.

## Approaches

| file | mechanism |
|---|---|
| `lca.kara` ★ | #236's search widened from two nodes to a set: a node in the set answers for its whole subtree, a node with an answer on both sides is the ancestor, and one with an answer on one side passes it up. The values in a `Set`. O(n + k) |
| `lca_count.kara` | one walk counts how many of the set each subtree holds; the walk meets the deepest first, so the first count to reach k is the answer. O(n + k) |
| `lca_pairwise.kara` | #236's search for two nodes folded over the list: the ancestor so far and the next node. O(n * k) |
| `lca_parents.kara` | one walk with a stack records each node's parent and depth in two `Map`s; every node climbs to the shallowest one's depth, then all climb together until they meet. O(n + k * h) |
| `differential.kara` | the four arms against the statement read literally, five properties |

The tree is a `shared struct TreeNode` with `Option[TreeNode]` children,
as LeetCode's `Rc<RefCell<TreeNode>>`, and `nodes` is a `Vec[TreeNode]`
of the tree's own nodes. The values are unique, and every arm compares by
value. LeetCode offers no Rust template for this problem, so there is no
Rust-template arm.

Every arm prints the same 9 lines: LeetCode's three examples, every node
of the example (3), two leaves under the root's left child (5), and a
one-node tree (1); then the answers summed and a checksum for 3000 random
trees of up to 8 nodes, 300 of up to 1000 and 30 of up to `10^4`, each
asked 5 times about 1 to 20 distinct nodes. A random tree holds 0 to
n - 1 shuffled, each node hung from a random node already placed, down a
random walk to the first free child, as #1644's are. `lca.py` mirrors the
★ arm and its output is byte-identical.

```
2
1
5
3
5
1
3000 trees of up to 8 nodes: answers sum to 26039, checksum 496895106
300 trees of up to 1000 nodes: answers sum to 379137, checksum 98206857
30 trees of up to 10000 nodes: answers sum to 378915, checksum 314438368
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every node whose subtree holds all the values (a node being
its own descendant) is a common ancestor, and the lowest is the one
furthest from the root. It checks 3000 random trees of 1 to 10 nodes,
each asked about 1 to all of its nodes. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the nodes in reverse order give the same answer |
| P3 | the answer's own node added to the nodes gives the same answer |
| P4 | the tree mirrored (every node's children swapped) gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 454468545, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M9 stops on both before any property
is checked: with the first node left where it is, the nodes climbing
together never meet, and the climb asks the `Map` for the root's parent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an answer on both sides passes up the left one | P1 327, P4 327, P5 327 |
| M2 | ★: an answer on one side makes this node the answer | P1 474, P4 773, P5 474 |
| M3 | ★: a node in the set answers only when it has no left child | P1 1103, P4 1601, P5 1103 |
| M4 | count: the last node to reach k kept, not the first | P1 773, P5 773 |
| M5 | count: a node one short of k taken | P1 1915, P4 391, P5 1915 |
| M6 | pairwise: only p ends #236's search | P1 1581, P2 2115, P5 1581 |
| M7 | pairwise: the second node skipped | P1 547, P2 753, P5 547 |
| M8 | parents: the answer one level too high | P1 773, P3 289, P5 773 |
| M9 | parents: the first node left at its depth | `key not found` |
| M10 | ★: the first node left out of the set | P1 1438, P2 1023, P5 1438 |

## Benchmarks

The bench draws one random tree of `10^4` nodes, LeetCode's largest, and
500 sets of 1 to 50 of its nodes, all of them first, then asks about each
set 10 times by the ★ arm in all five languages: Kāra's `shared struct`
and `Set`, Rust's `Rc<RefCell<TreeNode>>` and `HashSet`, pointer nodes in
Go with a `map` as the set and in Python with a `set`, and in C nodes
malloc'd one by one with an open-addressing hash set written for the
bench. Every implementation prints `10000 nodes, 500 sets, 10 rounds:
answers sum to 21332810, checksum 433083142`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.617 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.788 s |
| Go | 0.815 s |
| Rust (`rustc -O`) | 0.823 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.851 s |
| Kāra (`karac build`) | 0.881 s |
| Python | 4.2 s |

The sequential Kāra build takes 1.03x Rust's time and 1.08x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.617 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.872 s and 0.875 s on one
run).

## Verification

All four arms print the same output as `lca.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

All four arms checked clean as first written. The differential's P3
first compared the answer, an `i64`, with the `i32` values in
`with_answer.contains(got)`; `karac check` refused the narrowing (E0200)
and it was written `got as i32`. `arm_name` in it indexes a list of
string literals for a `Str`, as #1662's does (B-2026-11-19-131).
