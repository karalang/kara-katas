# 1644. Lowest Common Ancestor of a Binary Tree II

Given the `root` of a binary tree, return *the lowest common ancestor
(LCA) of two given nodes,* `p` *and* `q`. If either node `p` or `q`
**does not exist** in the tree, return `null`. All values of the nodes in
the tree are **unique**.

According to the definition of LCA on Wikipedia: "The lowest common
ancestor of two nodes `p` and `q` in a binary tree `T` is the lowest node
that has both `p` and `q` as **descendants** (where we allow **a node to
be a descendant of itself**)". A **descendant** of a node `x` is a node
`y` that is on the path from node `x` to some leaf node.

```
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1   ->  3
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4   ->  5
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 10  ->  null
```

**Constraints:** the number of nodes is in `[1, 10^4]`;
`-10^9 <= Node.val <= 10^9`; all `Node.val` are unique; `p != q`.

**Follow up:** Can you find the LCA traversing the tree, without checking
nodes existence?

## Approaches

| file | mechanism |
|---|---|
| `lca.kara` ★ | the follow-up: one walk counts, for every subtree, how many of p and q it holds; the first node whose count reaches 2, which the walk meets deepest first, is the answer. O(n) |
| `lca_parents.kara` | one walk with a stack records every node by value in a `Map` and every child's parent; q climbs until it meets p's ancestors, kept in a `Set`. O(n) |
| `lca_paths.kara` | the path from the root to p and to q, each by a depth-first search that keeps the nodes on the way; the answer is the last node the two share. O(n) |
| `lca_classic.kara` | #236's search, which is right whenever both are in the tree, run only after a search for each finds it. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

The tree is a `shared struct TreeNode` with `Option[TreeNode]` children,
as LeetCode's `Rc<RefCell<TreeNode>>`. p and q are passed as nodes of
their own: the values are unique, and every arm compares by value.
LeetCode offers no Rust template for this problem, so there is no
Rust-template arm.

Every arm prints the same 9 lines: LeetCode's three examples, p the root
(3), both in one line down `[1, 2, null, 3]` (2), and neither in the
tree (-1, for `null`); then the answers plus one summed, a missing
ancestor counted as 0, and a checksum for 3000 random trees of up to 8
nodes, 300 of up to 1000 and 30 of up to 10000, each asked about 5 pairs
of values, about one in five of them not in the tree. A random tree
holds 0 to n - 1 shuffled, each node hung from a random node already
placed, down a random walk to the first free child. `lca.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a node is a common ancestor when both p and q are among its
descendants, itself included, and the lowest is the one with the fewest
descendants; if no node is one, there is no answer. It checks 3000
random trees of 1 to 8 nodes, each asked about one pair, one value in
four on average not in the tree. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | p and q swapped give the same answer |
| P3 | the mirrored tree gives the same answer |
| P4 | an answer other than p, asked about with p, is its own answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 277924739, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The parents arm starting p's
ancestors at its parent (M4) sends q climbing past the root when p is
the answer, and stops with `key not found` on both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every node that counts both taken, so the last, the highest, wins | P1 470, P5 470 |
| M2 | ★: the first node to count either taken | P1 2804, P3 223, P5 2804 |
| M3 | ★: q never counted | P1 1114, P5 1114 |
| M4 | parents: p's ancestors start at its parent | `key not found` |
| M5 | parents: right children never walked | P1 878, P3 461, P5 878 |
| M6 | paths: the last step of the shorter path taken, whether the paths still agree there or not | P1 223, P2 223, P5 223 |
| M7 | paths: a dead end left on the path | P1 223, P3 223, P5 223 |
| M8 | classic: run when either is in the tree | P1 1690, P5 1690 |
| M9 | classic: the first node with either side found taken | P1 470, P5 470 |
| M10 | classic: only the left side's find passed up | P1 350, P3 463, P5 350 |

## Benchmarks

The bench draws 60 random trees of 10000 nodes, LeetCode's largest, each
with 50 pairs of values from 0 to 12499, so one in five is not in the
tree, all of them first, then answers each pair by the ★ arm in all five
languages: Kāra's `shared struct`, Rust's `Rc<RefCell<TreeNode>>`,
pointer nodes in Go and Python, and nodes malloc'd one by one in C. Every
implementation prints `60 trees of 10000 nodes, 50 pairs each: answers
sum to 10713104, checksum 342244860`. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.448 s |
| Go | 0.486 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.604 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.626 s |
| Rust (`rustc -O`) | 0.632 s |
| Kāra (`karac build`) | 0.639 s |
| Python | 8.1 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.448 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.632 s and
0.642 s on one run).

## Verification

All four arms print the same output as `lca.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The harness first queued the level order in a `Deque`, and `karac fix`
named Kāra's `VecDeque`; it also dropped a widening `node.val as i64`.
The paths arm returned `last`, an `Option` of a node borrowed from the
path, and the fix added `.cloned()`. The parents and classic arms checked
clean as first written, `let n = node?;` and `left.or(right)` included.

The classic arm's `let n = node?;` passes a `None` up from every empty
subtree, and each one recorded an error-return trace frame, though a
`None` is no error. The review thread ruled that an `Option`'s `?`
records none, and since kara `bd214fffc0` it does not (design.md §
Error return traces).
