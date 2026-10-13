# 510. Inorder Successor in BST II

Given a `node` in a binary search tree, return the in-order successor
of that node in the BST. If that node has no in-order successor,
return `null`.

The successor of a `node` is the node with the smallest key greater
than `node.val`.

You will have direct access to the node but not to the root of the
tree. Each node will have a reference to its parent node:

```
class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
}
```

```
tree = [2,1,3], node = 1                ->  2
tree = [5,3,6,2,4,null,null,1], node = 6  ->  null
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-10^5 <= Node.val <= 10^5`; all nodes have unique
values.

**Follow up:** could you solve it without looking up any of the node's
values?

## Approaches

Every arm is `fn inorder_successor(node: Node) -> Option[Node]` over
a `shared struct Node` whose children are `Option[Node]` and whose
parent link is a `weak Node`, so a child does not keep its parent
alive and the tree holds no cycle of strong handles (design.md §
Cycles and `weak`). Reading the parent yields an `Option[Node]`, which
is `None` at the root.

| file | mechanism |
|---|---|
| `inorder_successor.kara` ★ | with a right subtree, its leftmost node; without one, climb the parent links to the first ancestor with a larger value, since the ancestors passed on the way are smaller (the node is in their right subtrees). O(height) |
| `inorder_successor_identity.kara` | the follow-up: the same two cases told by shape alone. Without a right subtree, climb while the node is its parent's right child; the first parent it is the left child of is the successor. Left or right is decided by identity, `Some(l) if l.ref_eq(child)` in a match guard. O(height) |
| `inorder_successor_search.kara` | climb the parent links to the root, then search the tree for the smallest value above the node's, a larger value being a candidate that sends the search left. O(height) |
| `inorder_successor_walk.kara` | climb to the root and walk the whole tree in order on an explicit stack, watching for the node by identity (`ref_eq`); the next node visited is the successor. O(n), and no value compared |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, a node
with a right subtree, one two steps below its successor, the
smallest, one node, chains to the right and to the left, the
extremes, and for 300 random search trees (1 to 40 different values,
spread 1, 7 or 5,000 apart in turn, shuffled) the successor of every
node: how many nodes, how many have none, and a checksum. The trees
are built by inserting the values in order, each new node pointing
back at its parent. `inorder_successor.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random search trees of 1 to 30 different values, spread 1, 3 or
1,000 apart in turn and shuffled, with one of the values as the node.

| | property |
|---|---|
| P1 | the successor is the next larger value |
| P2 | the answer is the tree's own node with that value, by identity, not a copy |
| P3 | successors followed from the smallest node visit every value in order, then stop |
| P4 | the same values inserted in another order, another shape, give the same answer |
| P5 | the tree, parent links included, is as it was |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right child, not the leftmost node under it | P1 266, P3 1271, P4 454 |
| M2 | ★: the climb stops at the first smaller ancestor (`<`) | P1 785, P3 1448, P4 880 |
| M3 | identity: the climb stops where the node is the right child | P1 767, P3 1421, P4 890 |
| M4 | identity: only one step up | P1 272, P3 1287, P4 373 |
| M5 | search: a candidate sends the search right | P1 1147, P3 1411 |
| M6 | search: an equal value is a candidate (`>=`) | P1 1500, P3 1500 |
| M7 | walk: the root is watched for, not the node | P1 1299, P3 1448, P4 1308 |
| M8 | walk: right subtrees are never walked | P1 1174, P3 1419, P4 300 |
| E1 | identity: left or right told by value, `l.val == child.val` | 0 |
| E2 | ★: an equal ancestor would do (`>=`) | 0 |
| E3 | search: a node with a right subtree searches only under itself | 0 |
| E4 | walk: the node found by value, `top.val == node.val` | 0 |

E1, E2 and E4 are equivalent because the values are all different: a
value names one node, so comparing values is comparing identity, and
no ancestor has the node's own value. That is also why the follow-up
is a question of style here rather than of answers. E3 is equivalent
because when the node has a right subtree the next larger value is in
it.

M5 always goes right, so it walks the root's right spine and answers
with the largest value whenever that is above the node's; M6 answers
with the node itself. Both answers depend only on the values, not the
shape, so P4 cannot see them. The others answer for a particular
shape, which another insertion order changes. P3 sees all eight,
since a wrong successor anywhere breaks the walk from the smallest
node.

P2 and P5 kill none of the eight: they are there for an arm that
returns a copy of a node, or rewrites links as it goes, and none of
these edits does. Two more edits, outside the table, were aimed at
them. One returns a fresh copy of the walk's answer, and fails P2 1306
and P3 1411, so P2 does see what it is for. The other rewrote the
node's parent link during the ★ arm's climb (`node.parent =
p.parent;`) so that P5 would fire, and found kara B-2026-10-13-23
instead (below): `karac __mir-run` refuses it as invalid MIR.

## Verification

All four arms print the same output as `inorder_successor.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `30000 checks, 0 failures` on both and
runs clean under the third. `karac check` passes on every file, the
bench program included.

On the frozen legacy backends, `karac run --interp` prints the same
output for the ★ and search arms, and stops on the identity and walk
arms and the differential at their first `ref_eq` ("method 'ref_eq'
not found on type 'Node'"), which the shared type checker accepts
since kara `32540012cd` but no legacy backend runs. LLJIT and legacy
`karac build` fail on every arm at codegen: on the ★ and search arms
at the harness's calls to `show`, whose first parameter is a `Str`
given a string literal ("Module verification failed: Call parameter
type does not match function signature!", as on katas 501 and 508),
and on the other two and the differential at `ref_eq` ("no handler for
method 'ref_eq'"). Legacy `karac build` builds the bench program,
which has neither. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random search trees of
10,000 different values (the problem's most), the j-th value j * 20
plus less than 20, shuffled, keeping every node, once. Then it asks
for the successor of every node, 50 times over. Every implementation
prints `100 trees of 10000 nodes, 50 times each: 5000 without a
successor, checksum 974699157`, the Kāra program under `karac
__mir-run` included (in 341 s).

Every mirror keeps the parent link beside the two children: C, Go and
Python a plain pointer or reference, and Rust a `Weak` in an
`Rc<RefCell<Node>>`, the closest match to a `shared struct` with a
`weak` field, so each step up upgrades it, as each read of a Kāra
`weak` field does. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.85 to 2.03 s |
| Rust (`rustc -O`) | 2.58 to 2.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.42 to 2.79 s |
| Go | 1.61 to 1.73 s |
| Python | 14.6 to 14.9 s |
| Kāra (legacy `karac build`) | 2.76 to 2.99 s |
| Kāra (`karac build --mir`) | 3.28 to 3.51 s |

Legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build; the
`--mir` row is timed by hand at kara `10fdedabfc`. Under `karac
__mir-llvm-run` the program prints the same line in 6.7 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

kara B-2026-10-13-23 (leak, open), found by the second extra edit
under Mutation testing, not by the kata's own files, which store only locals into `parent` and
run clean: a strong handle stored into a `weak` field is downgraded
only when it is a plain local. Stored from a call (`c.parent =
get(a)`, `c.parent = b.parent.expect(...)`, or in a struct literal),
`karac __mir-run` prints the output and then stops at the drop with "a
weak-typed place holds no handle", and `karac __mir-llvm-run` prints
it right but leaks the object, which only the AddressSanitizer lane
sees. Stored from another `weak` field (`c.parent = b.parent`),
`karac __mir-run` refuses it as invalid MIR ("move out of ... which is
inside a shared value") and the compiled backend leaks the same way.
`karac check` passes all of them, and the legacy backends run them
right.
