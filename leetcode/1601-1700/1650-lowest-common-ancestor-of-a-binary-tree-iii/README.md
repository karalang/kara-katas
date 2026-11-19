# 1650. Lowest Common Ancestor of a Binary Tree III

Given two nodes of a binary tree `p` and `q`, return *their lowest common
ancestor (LCA)*.

Each node will have a reference to its parent node. The definition for
`Node` is below:

```
class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
}
```

According to the definition of LCA on Wikipedia: "The lowest common
ancestor of two nodes p and q in a tree T is the lowest node that has
both p and q as descendants (where we allow **a node to be a descendant
of itself**)."

```
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1  ->  3
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4  ->  5
root = [1,2], p = 1, q = 2                          ->  1
```

**Constraints:** the number of nodes is in `[2, 10^5]`;
`-10^9 <= Node.val <= 10^9`; all `Node.val` are unique; `p != q`; `p`
and `q` exist in the tree.

## Approaches

| file | mechanism |
|---|---|
| `lca.kara` ★ | two climbers, one from p and one from q, each starting over from the other's node when it passes the root: each walks p's path and then q's, the same length in all, so they meet at the first node the paths share. O(h), no extra memory |
| `lca_ancestors.kara` | p's ancestors, p included, in a `Set`; q climbs until it reaches one. O(h) time and space |
| `lca_depth.kara` | each node's depth by climbing to the root; the deeper one is lifted until the two are level, then both together until they meet. O(h) |
| `lca_root.kara` | climb to the root, then #236's search down the child links. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

The node is a `shared struct Node` with `Option[Node]` children and a
`weak Node` parent, so the back-links do not keep the tree alive (design.md
§ Cycles and `weak`); reading a parent gives an `Option[Node]`. Nodes are
compared by value, which the statement makes unique. LeetCode offers no
Rust template for this problem, so there is no Rust-template arm.

Every arm prints the same 8 lines: LeetCode's three examples, a node and
its child in the first tree (2), and two leaves on either side of the
root (3); then the answers summed and a checksum for 3000 random trees
of 2 to 8 nodes, 300 of up to 1000 and 30 of up to `10^5`, each asked
about 5 pairs of its nodes. A random tree holds 0 to n - 1 shuffled, each
node hung from a random node already placed, down a random walk to the
first free child. `lca.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a node is a common ancestor when both p and q are among its
descendants, found by walking down its children, itself included, and the
lowest is the one with the fewest descendants. It checks 3000 random
trees of 2 to 8 nodes, each asked about one pair of its nodes. Every case
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | p and q swapped give the same answer |
| P3 | an answer other than p, asked about with p, is its own answer |
| P4 | the mirrored tree, built anew with its parent links, gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 551626117, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Four stop on both backends before any
property is checked: three of them climb past the root, where the parent
read is `None` and `.expect("the referent is alive")` panics, and the
root arm's M8 finds nothing and unwraps `None`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the meeting node's parent returned | P1 1151, P3 392, P5 1151 |
| M2 | ★: both climbers start from p | P1 1726, P2 3000, P5 1726 |
| M3 | ancestors: p itself left out of its ancestors | `the referent is alive` |
| M4 | ancestors: q's ancestors gathered, not p's | P1 1907, P2 3000, P3 3000, P5 1907 |
| M5 | depth: a deeper q never lifted | `the referent is alive` |
| M6 | depth: only p's side climbs once level | `the referent is alive` |
| M7 | root: the first node with either side found taken | P1 1151, P5 1151 |
| M8 | root: p and q not taken where they are met | `called unwrap() on None` |
| M9 | root: the search starts at p, not the root | P1 1726, P2 3000, P5 1726 |
| M10 | root: only p looked for | P1 1726, P2 3000, P5 1726 |

## Benchmarks

The bench draws 30 random trees of `10^5` nodes, LeetCode's largest,
each with 50000 pairs of its nodes, all of them first, then answers each
pair by the ★ arm in all five languages: Kāra's `shared struct` with a
`weak` parent, Rust's `Rc<RefCell<Node>>` with a `Weak` parent, pointer
nodes in Go and Python, and nodes malloc'd one by one in C. Every
implementation prints `30 trees of 100000 nodes, 50000 pairs each:
answers sum to 80348337452, checksum 504282657`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.769 s |
| Go | 0.796 s |
| Kāra (`karac build`) | 1.019 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.028 s |
| Rust (`rustc -O`) | 1.029 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.046 s |
| Python | 17 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.769 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.897 s and
1.018 s on one run).

## Verification

All four arms print the same output as `lca.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ and root arms checked clean as first written. The ancestors and
depth arms climbed with `.parent.unwrap()`, and the `weak_read_unwrap`
lint asked for the invariant to be written out: `karac fix` wrote
`.expect("the referent is alive")`. The depth arm also declared its pairs
Rust's way, `let (mut a, mut b) = ..`, and the fix moved the `mut` before
the pattern. The harness's `for (parent, left, right) in [(3, 5, 1), ..]`
passed the numbers where `i32` values are wanted, and the fix wrote the
first tuple `(3i32, 5i32, 1i32)`.

The ancestors arm's `at = at.parent.unwrap();` printed the
`weak_read_unwrap` warning twice, once for the read and once for the
assignment's value. Since kara `bd214fffc0` it prints once.
