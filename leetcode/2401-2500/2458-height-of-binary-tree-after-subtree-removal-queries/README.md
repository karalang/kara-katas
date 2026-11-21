# 2458. Height of Binary Tree After Subtree Removal Queries

You are given the `root` of a **binary tree** with `n` nodes. Each node
is assigned a unique value from `1` to `n`. You are also given an array
`queries` of size `m`.

You have to perform `m` **independent** queries on the tree where in the
`i`th query you do the following:

- **Remove** the subtree rooted at the node with the value `queries[i]`
  from the tree. It is **guaranteed** that `queries[i]` will **not** be
  equal to the value of the root.

Return *an array* `answer` *of size* `m` *where* `answer[i]` *is the
height of the tree after performing the* `i`th *query*.

**Note:**

- The queries are independent, so the tree returns to its **initial**
  state after each query.
- The height of a tree is the **number of edges in the longest simple
  path** from the root to some node in the tree.

```
root = [1,3,4,2,null,6,5,null,null,null,null,null,7], queries = [4]  ->  [2]
root = [5,8,9,2,1,3,7,4,6], queries = [3,2,4,8]                     ->  [3,2,3,2]
```

**Constraints:** the number of nodes is `n`; `2 <= n <= 10^5`;
`1 <= Node.val <= n`; all the values are unique; `m == queries.length`;
`1 <= m <= min(n, 10^4)`; `1 <= queries[i] <= n`;
`queries[i] != root.val`.

Measuring the tree afresh for every query is O(m n), up to `10^9`. But
the tree without a node is the tree without one branch, so what it
keeps is fixed by the node's position alone: the deepest node on the
other side of each ancestor, or the node's parent if nothing goes
deeper. One walk down can carry that height to every node at once, and
every answer is then a lookup.

## Approaches

| file | mechanism |
|---|---|
| `heights.kara` ★ | two walks: every subtree's height into a `Map`, then down from the root carrying the height kept without the node reached, a child's being its parent's or the depth reached through its sibling, whichever is larger. O(n + m) |
| `heights_naive.kara` | the statement read directly: for each query the tree's height measured afresh, the removed node's subtree skipped. O(m n) |
| `heights_euler.kara` | an Euler tour: the nodes in pre-order with their depths, so every subtree is one run of the list; without it the tree keeps the deepest node before the run or after it, read from running maxima taken from each end. O(n + m) |
| `heights_levels.kara` | by levels: every path below depth `d` passes through a node at depth `d`, so without a node the height is the deepest reach of the others at its depth, or `d - 1` when it is alone there; each level keeps its two deepest reaches and its count. O(n + m) |
| `heights_iter.kara` | iterators over the Euler tour: the running maxima by `scan` from the front and by `rev` and `scan` from the back, each node's place by `enumerate` collected into a `Map`, and each answer by `map`. O(n + m) |
| `heights_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` and `i32` queries, with `height` and `walk` nested in the method, memoised in a `HashMap<i32, i32>`, and the siblings' heights read by `as_ref().map_or`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; then four
more, a root's two leaves, a left chain cut at every node, a right
chain cut below its root, and a deep left side whose removal leaves the
short right one; then 2000 random trees of 2 to 60 nodes with every node
but the root asked, a random tree of 2000 nodes and a chain of 2000
left children, each with 2000 random queries, as checksums. The trees
stop at 2000 nodes, below the constraints' `10^5`, because the naive arm
is O(m n) and would run for hours under the interpreter. `heights.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 5000 random trees of 2 to 12 nodes against a walk of each
tree with the removed subtree left out.

`check` first reports 32 errors on the template, and `karac fix` carries
it in one call, reporting 67 edits. The three `use` lines go;
`Rc<RefCell<TreeNode>>` becomes the `TreeNode` handle, declared a
`shared struct`, and each `borrow()` and `let n = n.borrow();` goes with
it; the two nested functions move above the `impl`, since Kāra has no
nested items; `HashMap` becomes `Map` and `HashMap::new` `Map.new`; the
generic brackets of `Option<..>`, `Vec<..>` and `HashMap<..>`; every `&`
and `&mut` on a parameter becomes a bare borrow, `ref` or `mut ref`, and
every one on an argument goes or becomes `mut`; the `&` on each map
index goes; and `struct Solution;` is given its braces. The `i32`
values, `as_ref().map_or(-1, ..)` and the closure over `queries` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every node listed with its parent by a breadth-first walk;
for each query, a node is removed when the query is it or one of its
ancestors, found by climbing its parents; and the height is the most
steps any remaining node climbs to the root. No subtree height is kept.
It checks 300 random trees of 2 to 12 nodes; then 30 of up to 60; then
30 paths of up to 30 nodes, each step left or right at random. Every
node but the root is asked. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | the tree mirrored, left and right swapped at every node: the same answers |
| P3 | each answer at least the depth of the asked node's parent |
| P4 | each answer no more than the whole tree's height |
| P5 | a new root put above the old one: every answer one more, and the old root's answer 0 |
| P6 | each arm agrees with at least three of the other five |

P2 holds because mirroring keeps every depth. P3 holds because the
asked node's parent stays, and P4 because removing nodes never makes a
path longer. P5 holds because the new root adds one edge above every
path, and removing the old root leaves the new one alone. P3 was at first
the queries asked in reverse order, the answers coming back reversed; it
killed none of the 31 mutants, since every arm answers each query on its
own, and it was replaced.

The differential prints `360 cases: checksum 312511325, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks each tree with the asked node's subtree left
out. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an empty side of height 0 | P1 253, P4 253, P6 253 |
| M4 | ★: the sibling one level high | P1 309, P2 326, P3 141, P5 92, P6 309 |
| M5 | ★: the right child given its own height | P1 305, P2 340, P6 305 |
| M8 | naive: the right side never measured | P1 312, P2 326, P3 237, P6 312 |
| M10 | naive: the next value removed | P1 351, P3 296, P5 360, P6 351 |
| M11 | naive: a leaf never removed | P1 283, P2 265, P5 108, P6 283 |
| M12 | euler: the last depth for the most | P1 160, P2 183, P6 160 |
| M13 | euler: the run after never read | P1 253, P2 253, P6 253 |
| M14 | euler: the run's last node kept | P1 338, P2 166, P5 360, P6 338 |
| M18 | levels: the old first dropped | P1 194, P2 215, P6 194 |
| M19 | levels: the node's own reach never set aside | P1 212, P6 212 |
| M20 | levels: the node's own depth kept | P1 311, P5 360, P6 311 |
| M22 | iter: each maximum from the front one node late | P1 307, P2 249, P3 159, P5 200, P6 307 |
| M23 | iter: each maximum from the back one node late | P1 101, P2 140, P6 101 |
| M25 | iter: every run one node long | P1 306, P5 360, P6 306 |
| M29 | solution: the left child given its own height | P1 308, P2 340, P5 360, P6 308 |
| M30 | solution: each answer one more | P1 360, P4 253, P5 360, P6 360 |

P1 and P6 kill all seventeen, P2 eleven, P5 nine, P3 four and P4 two.

Fourteen are not kept. Ten fail exactly as a kept one: the ★ arm's
missing sibling taken as a leaf and the naive arm's removed node kept as
a leaf (M3, M7) as the levels arm's node's own depth kept (M20), all
three leaving the asked node's depth standing; the ★ arm's depths
counted from 1, the naive arm's empty side of height 0 and the
template's depths counted from 1 (M6, M9, M31) as the template's each
answer one more (M30); the euler arm's each run one short and the iter
arm's run's last node kept and back maxima one place late (M16, M24,
M26) as the euler arm's run's last node kept (M14); and the levels
arm's empty side reaching its own depth and the template's empty side
of height 0 (M17, M27) as the ★ arm's empty side of height 0 (M1).
Three fail apart from every kept one, and alike among themselves, and
were left out because those arms keep their share already: the ★ arm's
node not counted in its height (M2), the levels arm's level above read
(M21) and the template's each height one short (M28).

One ends in a runtime error, not a wrong answer, under both backends:
the euler arm's each place one late (M15) records a node's place after
pushing its depth, so the last node's run ends one past the maxima from
the back, and the index is out of bounds.

## Verification

Every arm prints the same output as `heights.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 1.6 to 2.4 s but the naive arm,
11.4 s, and the differential 1.9 s; under `karac __mir-llvm-asan` the
differential takes 0.9 s and under `karac run` 0.7 s.

## Benchmarks

The bench builds 20 random trees of `10^4` nodes once from its own
generator, then makes 60 passes; each asks every tree about every value
but the root's, pass `p` starting its queries `101 p` values along, and
folds every answer plus the pass into the checksum. The bench uses the
★ arm, every subtree's height then one walk down, in all five
languages. Every implementation prints `60 passes over 20 trees of
10^4: checksum 939387137`. The two tables are the language's own hash
map, `Map` in Kāra, `HashMap` in Rust, `map` in Go and `dict` in Python;
C has none, and uses two open-addressing tables of `2^15` slots keyed
by the value, cleared for every tree asked. The nodes are a `shared
struct` in Kāra, `Rc<RefCell<TreeNode>>` in Rust, `*TreeNode` in Go,
objects with `__slots__` in Python, and one `malloc`'d array linked by
pointers in C.

BENCHTAB
