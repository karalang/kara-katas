# 2331. Evaluate Boolean Binary Tree

You are given the `root` of a **full binary tree** with the following
properties:

- **Leaf nodes** have either the value `0` or `1`, where `0` represents
  `False` and `1` represents `True`.
- **Non-leaf nodes** have either the value `2` or `3`, where `2`
  represents the boolean `OR` and `3` represents the boolean `AND`.

The **evaluation** of a node is as follows:

- If the node is a leaf node, the evaluation is the **value** of the
  node, i.e. `True` or `False`.
- Otherwise, **evaluate** the node's two children and **apply** the
  boolean operation of its value with the children's evaluations.

Return *the boolean result of **evaluating** the* `root` *node.*

A **full binary tree** is a binary tree where each node has either `0`
or `2` children. A **leaf node** is a node that has zero children.

```
root = [2,1,3,null,null,0,1]  ->  true
root = [0]                    ->  false
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 1000]`; `0 <= Node.val <= 3`; every node has either `0` or `2`
children; leaf nodes have a value of `0` or `1`; non-leaf nodes have a
value of `2` or `3`.

The evaluation is the definition, recursive on the children. O(n).

## Approaches

| file | mechanism |
|---|---|
| `evaluate.kara` ★ | a `match` on the node's value: a leaf its own truth, an OR or an AND node its children evaluated recursively and joined by `or` or `and`, which stop at the first child that settles it |
| `evaluate_minmax.kara` | as numbers: a leaf its 0 or 1, an OR node the `max` of its subtrees and an AND node their `min`, the tree true at 1; both subtrees always evaluated |
| `evaluate_stack.kara` | no recursion: a stack of nodes, each pushed once to open it and once to close it after its children, and a second stack of results that a closing node pops two from and pushes their join |
| `evaluate_levels.kara` | level by level: a breadth-first walk lists every node with its children's places in the list, and a pass from the last node back to the first settles each one from its children's truths |
| `evaluate_iter.kara` | iterators: a node's children gathered by `filter_map`, evaluated by `map`, and joined by `any` for an OR and `all` for an AND |
| `evaluate_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` in, the node `unwrap`ped and `borrow`ed, a `match` on its value, and each child handed down by `clone` to `Self::evaluate_tree`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

LeetCode's `TreeNode` is `shared struct TreeNode { mut val: i32, mut
left: Option[TreeNode], mut right: Option[TreeNode] }` with its `new`,
reference counted as Rust's `Rc<RefCell<TreeNode>>` is.

Every arm prints the same 7 lines: LeetCode's two examples; a lone true
leaf; an AND of false and true; an OR of two falses; a chain of 500
ANDs down the left over true leaves, ending in a false; then 3000
random full trees of depth up to 8, with a checksum of the truths and
how many are true. `evaluate.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 23 edits.
`check` first reports twelve errors and offers 16 edits for them: the
two `use` lines for `RefCell` and `Rc` deleted, since a `shared struct`
is already reference counted; the brackets of the two
`Option<Rc<RefCell<TreeNode>>>`; the four `Self::evaluate_tree` to
`Solution.evaluate_tree`; `||` to `or` and `&&` to `and`; `struct
Solution;` to `struct Solution {}`; and `Solution::` to `Solution.` in
the harness's wrapper. The rest follow from those: the two
`Rc[RefCell[TreeNode]]` to `TreeNode`, and `let node = node.borrow();`
deleted. The four `.clone()` on the children stand, each counting one
more reference.

The iter arm was first written with Rust's
`[node.left, node.right].iter().filter_map(|child| child)`. `karac
check` refuses it with a bare `expected 'Fn(ref Option[TreeNode]) ->
Option[_]', found 'Fn(ref Option[TreeNode]) -> ref Option[TreeNode]'`
and no hint, which ledger row B-2026-11-18-94 records. Rust
refuses it too, and suggests a copy. `into_iter().flatten()` is refused
with a message naming `filter_map(|v| v)` instead, since Kāra's
`Option` is not an iterator; the arm uses
`into_iter().filter_map(|child| child)`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the tree written out as a fully bracketed formula of `T`,
`F`, `|` and `&`, and every innermost bracket, two truths and an
operator, rewritten to its truth by text replacement, eight rules over
and over, until one letter is left. No recursion over the tree's
values. It checks 300 random full trees of depth up to 6; then 30
combs of depth up to 60, each node's other child a leaf; then 30
random trees of depth up to 10. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the tree under an AND with a true leaf, and under an OR with a false leaf: the same answer both times |
| P3 | every node's children swapped: the same answer |
| P4 | every leaf flipped and every OR and AND swapped: the answer flipped |
| P5 | the tree under an OR with a true leaf: true; under an AND with a false leaf: false |
| P6 | each arm agrees with at least three of the other five |

P4 is De Morgan's law: the negation of an OR is the AND of the
negations, so flipping every leaf and every operator flips the whole.
The transformed trees are fresh copies, built by a `copy` that swaps
or flips as it goes.

The differential prints `360 cases: checksum 234916344, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same trees, writes each as a Python expression of `True`,
`False`, `or` and `and`, and `eval`s it. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: an OR its left child alone | P1 66, P2 113, P3 61, P4 132, P5 247, P6 66 |
| M4 | ★: an AND its right child alone | P1 59, P2 122, P3 67, P4 136, P5 238, P6 59 |
| M5 | ★: an AND taken as an XOR | P1 86, P2 360, P4 119, P5 205, P6 86 |
| M7 | minmax: max and min swapped | P1 130, P2 360, P5 360, P6 130 |
| M8 | minmax: the root true at 0 | P1 360, P5 360, P6 360 |
| M9 | minmax: an OR the sum | P1 43, P2 43, P4 93, P5 179, P6 43 |
| M14 | stack: a node closed on its right result twice | P1 84, P2 195, P3 114, P5 165, P6 84 |
| M15 | stack: an AND of the left and not the right | P1 63, P2 176, P3 62, P4 92, P6 63 |
| M16 | stack: an OR its right child alone | P1 77, P3 61, P4 136, P6 77 |
| M18 | levels: the nodes settled first to last | P1 123, P2 56, P4 240, P5 360, P6 123 |
| M19 | levels: a true leaf false | P1 179, P4 360, P5 360, P6 179 |
| M20 | levels: the answer read from the last node | P1 107, P2 64, P3 122, P5 296, P6 107 |
| M23 | iter: an AND by any | P1 106, P2 75, P4 210, P5 285, P6 106 |
| M24 | iter: only the left child gathered | P1 90, P2 183, P3 114, P5 177, P6 90 |
| M26 | iter: an OR true when a child is false | P1 76, P2 171, P4 113, P5 189, P6 76 |
| M27 | solution: an OR taken as an AND | P1 104, P2 75, P4 210, P5 285, P6 104 |
| M29 | solution: an AND its left child alone | P1 66, P3 67, P4 132, P6 66 |

P1 and P6 kill all seventeen, P5 fourteen, P2 thirteen, P4 twelve and
P3 eight. P5 and P2 wrap the tree in a new root, P5's OR with its true
leaf on the right and AND with its false leaf on the left, P2's the
other way about, so they fail wherever an edit misreads an OR or an AND
at the top. P5 misses the edits that read only the new leaf's side
there: an OR its right child alone, and an AND its left child alone or
of the left and not the right. P2 misses the first two, which read the
tree itself under its wrappings, and every answer flipped at the root
and a true leaf false, which its two wrappings flip alike. P4, De
Morgan, fails where an edit treats the OR and the AND unlike each
other; it misses the edits that are their own duals: max and min
swapped, the root flipped, a child read twice or left out under both
operators alike, and the answer read from the wrong node. P3, the
children swapped, fails only where an edit reads one side and not the
other.

Of the thirty-one, fourteen were not kept. An OR taken as an AND fails
alike in the ★ (M1), iter (M22, an OR by all) and template (M27) arms,
and only the template's is kept. An OR its left child alone, or over
the left child twice, fails alike in the ★ (M3, M6), levels (M17) and
template (M31) arms, and only M3 is kept. A false leaf true fails alike
in the ★ (M2), iter (M25) and template (M30) arms, and none is kept;
so do the minmax arm's every leaf flipped (M10) and the stack arm's
leaf true at 0 (M13). The minmax arm's left subtree taken twice (M11)
fails as the iter arm's left child alone (M24), the stack arm's OR and
AND swapped on closing (M12) as the minmax arm's max and min swapped
(M7), the levels arm's AND over the left child twice (M21) as the
template's AND its left child alone (M29), and the template's true leaf
false (M28) as the levels arm's (M19). The stack arm's left child
pushed twice was first M16: every node's left subtree then runs twice,
an exponential walk that did not end on the combs of depth 60, and it
was stopped by hand and replaced by an OR its right child alone.

## Verification

Every arm prints the same output as `evaluate.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 to 0.5 s but the iter arm,
which `collect`s each node's children into a `Vec`, 0.8 s. The
differential takes 3.3 s there, most of it the literal reading's
rewriting of the formulas, and 0.5 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 200 random full trees of depth up to 14 once, a leaf
one time in 8 above the last level, then makes 500 passes evaluating
every tree, with the ★ arm in all five languages. Every implementation
prints `500 passes over 200 trees of depth up to 14: checksum
187176467`. Each stops at the first child that settles an OR or an
AND. The trees are Kāra's `shared struct`, reference counted, Rust's
`Option<Box<..>>`, C's and Go's pointers and Python's objects, with
`__slots__`.

BENCHTAB
