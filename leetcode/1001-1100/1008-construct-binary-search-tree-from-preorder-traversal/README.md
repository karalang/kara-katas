# 1008. Construct Binary Search Tree from Preorder Traversal

Given an array of integers `preorder`, which represents the preorder
traversal of a BST (i.e., binary search tree), construct the tree and
return its root.

It is guaranteed that there is always possible to find a binary search
tree with the given requirements for the given test cases.

A binary search tree is a binary tree where for every node, any
descendant of `Node.left` has a value strictly less than `Node.val`,
and any descendant of `Node.right` has a value strictly greater than
`Node.val`.

A preorder traversal of a binary tree displays the value of the node
first, then traverses `Node.left`, then traverses `Node.right`.

```
preorder = [8,5,1,7,10,12]  ->  [8,5,10,1,7,null,12]
preorder = [1,3]            ->  [1,null,3]
```

**Constraints:** `1 <= preorder.length <= 100`;
`1 <= preorder[i] <= 1000`; all the values of `preorder` are unique.

The answer is printed the way LeetCode shows a tree: level by level,
`null` for a missing child, and the trailing `null`s dropped.

## Approaches

The first value is the root, the values after it that are smaller make
its left subtree and the rest its right, each again in preorder. The
arms differ in how they find where the left subtree ends and in what
the tree is made of.

| file | mechanism |
|---|---|
| `bst_from_preorder.kara` ★ | recursion with an upper bound: one cursor reads the values, and a call builds the subtree of values below its bound, taking the next value as its root, then the left subtree below the root and the right below the bound; a value at or above the bound is left for an ancestor. `shared struct` nodes. O(n) |
| `bst_from_preorder_insert.kara` | insertion: the first value is the root and the rest are inserted in the order given, each by an iterative walk from the root that attaches a new leaf; a value's ancestors all come before it, so the walk rebuilds the same tree. `shared struct` nodes. O(n * height), O(n^2) for a sorted preorder |
| `bst_from_preorder_stack.kara` | an arena and a monotonic stack: nodes in parallel arrays of values and child indexes, and a stack of the nodes still waiting for a right child; a smaller value is the top's left child, and a larger one the right child of the last node popped while popping every smaller one. O(n) |
| `bst_from_preorder_split.kara` | divide and conquer: each call scans its slice for the first value greater than the root and recurses on the two parts, building an immutable `shared enum`. O(n * height) |
| `bst_from_preorder_inorder.kara` | preorder and inorder: the sorted values are the inorder, a map gives each value's place in it, and one cursor over the preorder takes each root, whose place splits its inorder range. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines. The first nine are LeetCode's two
examples and seven more: one value; three falling, a chain to the left;
three rising, a chain to the right; a full tree of seven; a tree whose
left subtree has two levels below a right child; and two zigzags, one
turning left first and one turning right below a leaf on the left,
whose level order has `null`s inside it. Then three trees of LeetCode's
longest, 100 values up to 1,000, given by the length of their text and
a hash of it: rising, falling, and alternating high and low. Then
totals over random trees, each the preorder of a BST of distinct random
values inserted in random order: 2,000 trees of up to 8 values up to
20, 500 of up to 100 values up to 1,000, and 5 of up to 100 values up
to 100. `bst_from_preorder.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms, turns each arm's tree
into one shared shape, and checks it against the statement read
literally: every binary tree whose preorder is the input, kept when
every node is greater than every value in its left subtree and less
than every value in its right, and there must be exactly one. It checks
2,400 random preorders drawn as above: 2,000 of 1 to 7 values up to 20
against the statement, and 400 of up to 300 values up to 1,000 against
the other properties.

| | property |
|---|---|
| P1 | the statement's one tree, on the first 2,000 preorders |
| P2 | the tree's preorder is the input |
| P3 | the tree's inorder rises strictly |
| P4 | mapping every value `v` to `3v + 7`, which keeps their order, gives the same tree with its values mapped |
| P5 | the root's left and right subtrees are the trees of the values below and above it, in their input order |
| P6 | each arm agrees with at least two of the other four |

P2 and P3 together fix the tree: a binary tree is determined by its
preorder and its inorder, and a strictly rising inorder makes it a
search tree. P5 is the recursion the statement implies, checked one
level down with the arm's own answers for the two parts.

It prints `2400 rows of 65583 values: checksum 100723689, 70000 checks
over 5 arms: 0 failures` under `karac __mir-run` (34 s, most of it the
statement's enumeration of every tree of up to seven nodes) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twenty-six edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the children swapped | P1 1687, P2 1427, P3 2084, P5 2084, P6 2084 |
| M2 | ★: the left subtree bounded by the ancestor's bound | P1 1477, P3 1872, P5 1622, P6 1872 |
| M3 | ★: the outer bound 1,000, not `i64.MAX` | P2 62, P4 398, P6 62 |
| M4 | insert: a right leaf hung on the left | P1 1477, P2 1658, P3 1872, P5 1622, P6 1872 |
| M5 | insert: the root inserted again | P1 2000, P2 2400, P3 2400, P5 2400, P6 2400 |
| M6 | insert: the last value dropped | P1 1687, P2 2084, P5 1220, P6 2084 |
| M7 | stack: the bottom compared, not the top | P1 335, P3 717, P5 605, P6 717 |
| M8 | stack: one node popped at most | P1 1036, P3 1427, P5 1132, P6 1427 |
| M9 | stack: the bottom taken as the top | P1 986, P2 1378, P5 1138, P6 1378 |
| M10 | split: at the first smaller value | P1 1687, P3 2084, P5 2084, P6 2084 |
| M11 | split: the value after the root always on the left | P1 1091, P3 1481, P5 490, P6 1481 |
| M12 | split: the last value never on the left | P1 1082, P3 1474, P5 462, P6 1474 |
| M13 | inorder: the preorder taken as the inorder | P1 1455, P3 1851, P5 1594, P6 1851 |
| M14 | inorder: the left subtree used twice | P1 1687, P2 2084, P3 1594, P5 2084, P6 2084 |
| M15 | inorder: the right subtree dropped | P1 1477, P2 1872, P5 1622, P6 1872 |

P6 kills all fifteen, P1 and P5 fourteen each, P3 eleven, P2 eight and
P4 one. The checks draw no random number that depends on an answer, so
every mutant sees the same preorders and their counts can be compared.
P2 and P3 split the edits between them. An edit that keeps every value
once but puts some on the wrong side of a node breaks the inorder and
keeps the preorder (M2, M7, M8, M10 to M13); one that still builds a
search tree, but of the wrong shape or of too few values, breaks only
the preorder (M3, M6, M9, M15); and one that swaps subtrees, or repeats
values, breaks both (M1, M4, M5, M14). M3 is the one edit P1 misses and
P4 sees: the statement's preorders stop at 20, far under the bound,
while the values mapped to `3v + 7` reach 3,007, so P4 fails on 398 of
the 400 large preorders, and only the 62 large preorders that hold the
value 1,000 itself fail P2.

Eleven other edits were tried and set aside. Five change no answer:
four because the values are distinct, each sending a value equal to the
one it is compared with the other way (the ★ arm's bound, insertion's
comparison, the stack's pops, the split's scan), and the inorder arm
testing an empty range with `>=`, since a range never runs past its
end. Four failed exactly the same checks as a kept one: the ★ arm's
right subtree unbounded and the stack hanging a right child on the top,
as M8; and insertion sending larger values left and the split arm
swapping the children, as M1. Two crashed with an index out of bounds
under both backends, as the edit makes it: the inorder arm reading the
right subtree first, or taking the inorder falling, sends a root
outside its range, and the range below it never empties.

## Verification

Every arm prints the same output as `bst_from_preorder.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is at kara
`8b6e8a9088`, with the runtime archives rebuilt there. Under `karac
__mir-run` each arm takes 1.1 s to 1.6 s.

`karac check` warns that the differential's first name for the arena
type, `Arena`, shadows a prelude type, so it is called `Nodes` there.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages: 50 preorders of 100
values up to 1,000, LeetCode's longest, drawn once, and 4,000 rounds
that each build every tree, starting from a different preorder, and fold
it into a checksum by a walk. That is 20 million nodes allocated and
freed. The C version frees each tree after the walk, Rust builds
LeetCode's `Rc<RefCell<TreeNode>>`, the counterpart of a Kāra `shared
struct`, Go leaves the trees to its collector, and Python builds a
class with slots. Every implementation prints `4000 rounds over 50
preorders of 100 values: checksum 162449455`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `8b6e8a9088`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.823 to 0.948 s | 0.865 s |
| Rust (`rustc -O`) | 0.918 to 1.075 s | 0.954 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.875 to 0.993 s | 0.917 s |
| Go | 0.870 to 1.017 s | 0.904 s |
| Python | 11.0 s | |
| Kāra (`karac build`) | 0.889 to 1.217 s | 0.918 s |

`bench.sh` builds the Kāra program with `karac build`, which is the v2
compiled backend since M3. Python's run is about 12 times Kāra's.

v2 took 1.00 times Rust's median time under overflow checks and 1.06
times C's: allocation dominates every version. Under valgrind's
cachegrind v2 ran 6,744 million instructions with 83.2 million branches
mispredicted, Rust with overflow checks 7,147 million and 63.2 million,
Rust without them 7,208 million and 61.8 million, and C 5,858 million
and 57.8 million. Rust's two builds trade places from run to run; the
gap between them is within the spread.
