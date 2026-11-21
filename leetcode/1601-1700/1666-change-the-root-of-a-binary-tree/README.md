# 1666. Change the Root of a Binary Tree

Given the `root` of a binary tree and a `leaf` node, reroot the tree so
that the `leaf` is the new root.

You can reroot the tree with the following steps for each node `cur` on
the path **starting from the** `leaf` up to the `root` **excluding the
root**:

1. If `cur` has a left child, then that child becomes `cur`'s right
   child.
2. `cur`'s original parent becomes `cur`'s left child. Note that in this
   process the original parent's pointer to `cur` becomes `null`, making
   it have at most one child.

Return *the new root of the rerooted tree*.

**Note:** Ensure that your solution sets the `Node.parent` pointers
correctly after rerooting or you will receive "Wrong Answer".

```
root = [3,5,1,6,2,0,8,null,null,7,4], leaf = 7  ->  [7,2,null,5,4,3,6,null,null,null,1,null,null,0,8]
root = [3,5,1,6,2,0,8,null,null,7,4], leaf = 0  ->  [0,1,null,3,8,5,null,null,null,6,2,null,null,7,4]
```

**Constraints:** the number of nodes is in `[2, 100]`;
`-10^9 <= Node.val <= 10^9`; all `Node.val` are unique; `leaf` exists in
the tree.

## Approaches

| file | mechanism |
|---|---|
| `flip.kara` ★ | one walk up from the leaf: each node takes its old parent before the link is reset to the node below it, lets the parent let go of it, moves its left child to the right and hangs the parent on its left. O(h), no extra memory |
| `flip_recursive.kara` | `hang(node, below)`: the node lets go of `below`, moves its left child right, recurses into its old parent with itself as the new `below`, then hangs that parent on its left. O(h) time, O(h) stack |
| `flip_path.kara` | the path from the leaf to the root gathered into a `Vec` first; then every parent lets go of its child on the path, and only after that is each node rehung and each parent link set, so no step reads a link another step changed. O(h) time and space |
| `differential.kara` | the three arms against the statement read literally, five properties |

The node is a `shared struct Node` with `Option[Node]` children and a
`weak Node` parent, as in #1650, so the back-links do not keep the tree
alive (design.md § Cycles and `weak`). A weak field takes either a node
(`child.parent = node`) or an `Option[Node]` (`cur.parent = below`, which
sets the new root's link to none). Nodes on the path are told apart by
identity, `ref_eq`, not by value. LeetCode offers no Rust template for
this problem, so there is no Rust-template arm.

Every arm prints the same 7 lines: LeetCode's two examples, a tree of two
nodes, and a leaf two levels down a left spine; then, for 3000 random
trees of 2 to 8 nodes, 300 of up to 1000 and 30 of up to `10^5`, each
turned to hang from a random leaf, the count whose parent links do not
match their child links (0) and a checksum of the new trees in level
order. A random tree holds 0 to n - 1 shuffled, each node hung from a
random node already placed, down a random walk to the first free child.
`flip.py` mirrors the ★ arm and its output is byte-identical.

```
[7,2,null,5,4,3,6,null,null,null,1,null,null,0,8]
[0,1,null,3,8,5,null,null,null,6,2,null,null,7,4]
[2,1]
[4,2,null,1,5,null,3]
3000 trees of up to 8 nodes: 0 with broken parent links, checksum 143655397
300 trees of up to 1000 nodes: 0 with broken parent links, checksum 149039773
30 trees of up to 100000 nodes: 0 with broken parent links, checksum 858137710
```

## Differential

`differential.kara` holds copies of the three arms and the statement
read literally, on plain numbers rather than nodes: each tree is three
lists (left child, right child and parent of each value), and the steps
are applied to them from the leaf up, then the new tree is read out in
level order. It checks 3000 random trees of 2 to 8 nodes, each turned to
hang from a random leaf; every arm is given a tree of its own. Every case
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the new tree is the statement read literally |
| P2 | every parent link names the node above it, and the root's names none |
| P3 | the new tree holds every node once |
| P4 | the leaf is the root, and the old root hangs as deep as the leaf did |
| P5 | the three arms agree |

The differential prints `3000 problems: checksum 701795496, 45000 checks
over 3 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, three or four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. An edit that leaves a parent still
holding its old child makes a cycle in the child links, and the
level-order walk then never ends; two such drafts were dropped for edits
that the properties can see.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no parent link reset | P2 3000, P4 3000 |
| M2 | ★: a left child dropped instead of moved right | P1 600, P3 600, P5 1800 |
| M3 | ★: the left child moved right even when there is none, dropping the right | P1 584, P3 584, P5 1752 |
| M4 | ★: every parent link set to none | P2 3000, P4 3000 |
| M5 | recursive: the old parent hung on the right | P1 3000, P3 584, P5 9000 |
| M6 | recursive: no parent link reset | P2 3000, P4 3000 |
| M7 | recursive: the old parent never hung | P1 3000, P3 3000, P5 9000 |
| M8 | path: only the leaf's parent link reset | P2 3000, P4 3000 |
| M9 | path: every parent link names the leaf | P2 2188, P4 2188 |
| M10 | path: every node hangs the old root, not its own parent | P1 2188, P2 2188, P3 2188, P5 6564 |

## Benchmarks

The bench draws 30 random trees of `10^5` nodes and 50000 start nodes in
each, all of them first. Then, for each start, it walks down at random
to a leaf and turns the tree to hang from it by the ★ arm, so each turn
starts from the tree the last one left, in all five languages: Kāra's
`shared struct` with a `weak` parent, Rust's `Rc<RefCell<Node>>` with a
`Weak` parent, pointer nodes in Go and Python, and nodes malloc'd one by
one in C. Every implementation prints `30 trees of 100000 nodes, 50000
turns each: 2447860 steps down, checksum 561062415`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.372 s |
| Go | 1.395 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.878 s |
| Rust (`rustc -O`) | 1.951 s |
| Kāra (`karac build`) | 2.126 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.330 s |
| Python | 20 s |

The sequential Kāra build takes 1.19x Rust's time and 1.24x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 1.372 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (2.237 s and 2.345 s on one
run).

## Verification

All three arms print the same output as `flip.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The three arms check clean.

The differential's first draft compared the sorted values with
`seen != (0..shape.left.len()).collect()`. Comparing against a `collect`
leaves its type open, and `karac check` asks for it (E0238). Its
machine fix, `Vec[i64].from_iter(..)`, cut `.collect()` back from the
receiver's span, which for a parenthesized range ends before `len())`,
and the edit broke the line (B-2026-11-19-132). Since kara `4e5c719df5` the fix cuts
from the call's closing parenthesis and writes
`(Vec[i64].from_iter(0..shape.left.len()))`; the kata keeps it without
the outer parentheses. The same `karac fix` dropped `got.val as i64`'s
cast, an `i32` widening by itself, and three `shape: ref Shape`
parameters' `ref`, which a parameter already is.

`arm_name` indexes a list of string literals for a `Str`, as #1662's
differential does (B-2026-11-19-131).
