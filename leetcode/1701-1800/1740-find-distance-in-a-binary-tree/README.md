# 1740. Find Distance in a Binary Tree

Given the root of a binary tree and two integers `p` and `q`, return
*the **distance** between the nodes of value* `p` *and value* `q` *in the
tree*.

The **distance** between two nodes is the number of edges on the path
from one to the other.

```
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 0  ->  3
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 7  ->  2
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 5  ->  0
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `0 <= Node.val <= 10^9`; all `Node.val` are unique; `p`
and `q` are values in the tree.

## Approaches

| file | mechanism |
|---|---|
| `distance.kara` ★ | the path runs up from one node to the lowest common ancestor and down to the other. #236's search finds the ancestor: a node that is p or q answers for its subtree, and a node with an answer on both sides is the ancestor. The distance is the depth of p below it plus that of q. O(n) |
| `distance_once.kara` | one post-order walk returns how far below each subtree's root the one of p and q it holds lies, or -1; where both sides hold one, or the node is one and a side holds the other, the two distances meet and the answer is written through a `mut ref`. O(n) |
| `distance_parents.kara` | a breadth-first walk with a `VecDeque` records each value's parent and depth in two `Map`s; the deeper node climbs to the other's depth, then both climb together until they meet. O(n) |
| `distance_graph.kara` | a walk with a stack lists each value's neighbours in a `Map[i32, Vec[i32]]`, and a breadth-first search from p over that undirected graph finds q at the level that is the distance. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

The tree is a `shared struct TreeNode` with `Option[TreeNode]` children,
as LeetCode's `Rc<RefCell<TreeNode>>`. The problem is premium and has no
Rust template, so there is no Rust-template arm; there are four Kāra
arms instead.

Every arm prints the same 10 lines: LeetCode's three examples, then two
leaves of one parent, two leaves on opposite sides of the root, a leaf
and the root, and a one-node tree; then the distances summed and a
checksum for 3000 random trees of up to 8 nodes, 300 of up to 1000 and
30 of up to `10^4`, LeetCode's largest, each asked about 5 random pairs.
`distance.py` mirrors the ★ arm and its output is byte-identical.

```
3
2
0
2
5
3
0
3000 trees of up to 8 nodes: distances sum to 19469, checksum 507735517
300 trees of up to 1000 nodes: distances sum to 21192, checksum 896165149
30 trees of up to 10000 nodes: distances sum to 3553, checksum 912643139
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the path from the root to each node, found by a walk that
keeps the trail it is on, and the distance the two paths' lengths less
twice the part they share. It checks 3000 random trees of 1 to 12 nodes,
each with random values p, q and r. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | p and q swapped give the same answer |
| P3 | the distance is at most the distance by way of r |
| P4 | the root's distances to p and q, less theirs, are twice a depth: even and not negative |
| P5 | each arm agrees with at least two of the other three |

P4 holds because the root's paths to p and q share the path down to
their ancestor, which the distance between them leaves out. The
differential prints `3000 problems: checksum 847543716, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
breadth-first search over the same trees' edges gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search stops at p only, not at p or q | P1 1482, P2 1548, P3 744, P4 670, P5 1482 |
| M2 | ★: a node with an answer on one side answers itself | P1 949, P5 949 |
| M3 | ★: depths sought down the left side only | P1 1736, P3 877, P4 1076, P5 1736 |
| M4 | once: the two sides' distances meeting one edge short | P1 700, P4 700, P5 700 |
| M5 | once: a node meeting a side's distance with no edge to it | P1 1548, P3 408, P4 1127, P5 1548 |
| M6 | once: a found distance passed up two edges at a time | P1 1309, P3 326, P4 759, P5 1309 |
| M7 | parents: the joint climb counted one edge a step, not two | P1 700, P4 522, P5 700 |
| M8 | parents: q's climb to p's depth counted two edges a step | P1 977, P2 1994, P4 670, P5 977 |
| M9 | graph: each level counted as two edges | P1 2248, P5 2248 |
| M10 | ★: the depths taken below the root, not the ancestor | P1 1458, P5 1458 |

## Benchmarks

The bench draws one random tree of `10^4` nodes, LeetCode's largest, and
1000 random pairs of its values, all of them first, then answers each
pair 4 times by the ★ arm in all five languages: Kāra's `shared struct`,
Rust's `Rc<RefCell<TreeNode>>`, pointer nodes in Go and Python, and in C
nodes malloc'd one by one. Each answer walks the tree up to three times.
Every implementation prints `10000 nodes, 1000 pairs, 4 rounds:
distances sum to 109524, checksum 527095989`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.736 s |
| Go | 0.891 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.933 s |
| Rust (`rustc -O`) | 0.937 s |
| Kāra (`karac build`) | 0.986 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.024 s |
| Python | 10.0 s |

The sequential Kāra build is level with Rust and 9% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.736 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.914 s and 0.922 s on one
run).

## Verification

All four arms print the same output as `distance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★, one-walk and graph arms checked clean as first written. The
parents arm took one `karac fix`: `let (mut a, mut b) = (p, q)`, Rust's
spelling, became `let mut (a, b) = (p, q)`, Kāra's. The differential
took one `karac fix`: an `as i64` on an arm's `i32` answer was dropped,
since it widens by itself.
