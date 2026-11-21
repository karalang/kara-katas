# 2385. Amount of Time for Binary Tree to Be Infected

You are given the `root` of a binary tree with **unique** values, and an
integer `start`. At minute `0`, an **infection** starts from the node
with value `start`.

Each minute, a node becomes infected if:

- The node is currently uninfected.
- The node is adjacent to an infected node.

Return *the number of minutes needed for the entire tree to be
infected.*

```
root = [1,5,3,null,4,10,6,9,2], start = 3  ->  4
root = [1], start = 1                      ->  0
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^5]`; `1 <= Node.val <= 10^5`; each node has a **unique** value;
a node with a value of `start` exists in the tree.

The answer is the farthest any node lies from the start, counting the
edges up through the parents as well as down. Below the start that is
its subtree's height; through an ancestor `d` edges up, it is `d` plus
the height of the ancestor's other side.

## Approaches

| file | mechanism |
|---|---|
| `infect.kara` ★ | one post-order walk: each subtree returns its height and how far down the start lies, or -1; the start's own height, and each ancestor's distance plus its other side's height, kept as the largest. O(n) |
| `infect_graph.kara` | the tree turned into a graph: a walk lists every node's neighbours in a `Map` by value, and a breadth-first search from the start counts the minutes. O(n) |
| `infect_parents.kara` | parent links: a walk records each node's parent in a `Map` and finds the start; a depth-first search from it goes down and up, never back the way it came, and the deepest it reaches is the answer. O(n) |
| `infect_stack.kara` | no recursion: an explicit stack lists the nodes root first; read backwards every child comes before its parent, and one pass carries the ★ arm's height and distance up. O(n) |
| `infect_iter.kara` | iterators: the edges gathered by `flat_map` over each node's children, both ways round, folded into a `Map` of neighbours; each minute's newly infected the last minute's neighbours by `flat_map`, kept by `filter` when not yet seen |
| `infect_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` in, a `build` nested in the method filling a `HashMap<i32, Vec<i32>>` by `entry().or_default()`, a `VecDeque` search with a `HashSet`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

The harness's node is LeetCode's own, `shared struct TreeNode` with an
`i32` value. Every arm prints the same 9 lines: LeetCode's two examples
and five more (a root's two leaves from the root, 1, and from a leaf, 2;
a left chain from its bottom, 3; a right chain from its middle, 2; and a
leaf below a long other side, 5); then 2000 random trees of 1 to 60
nodes from a random start, with the total and a checksum; then a random
tree of the constraints' largest, `10^5` nodes, from node 1 and from the
root, and a chain of 2000 left children from its middle. `infect.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 3000 random trees of up to 80 nodes against a breadth-first
search.

The iter arm was first written with the lookups as Rust would, and
`karac fix` carried it in one round of 3 edits: the `flat_map` closure's
`Vec` returned as `here.into_iter()`, and `g.get(a).unwrap_or(Vec.new())`
in the `fold`, which kept a borrow of a temporary, written
`g.get(a).cloned().unwrap_or(Vec.new())`. The same round also wrote the
store after it `g[a] = list.clone()`, for an error that its own
`.cloned()` had already removed, so the arm carried a needless copy of
the list; the `.clone()` was taken back out by hand. The frontier's
`flat_map(|v| graph.get(v).unwrap_or(Vec.new()))` was refused as a
closure returning a `ref Vec[i64]`, which is not an `Iterator`, with no
hint and no fix, where the owned `Vec` above got `.into_iter()`; it was
written `.cloned().unwrap_or(Vec.new()).into_iter()` by hand (both
B-2026-11-21-47). The parents arm's `t.val as i64 != came_from` lost its cast, one
that widens anyway, to the same fix.

`check` first reports 24 errors on the template, and `karac fix` carries
it in one round, reporting 55 edits: the three `use` lines deleted,
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, the nested
`build` moved above the `impl`, `&Option` to a bare parameter and `&mut
HashMap<i32, Vec<i32>>` to `mut ref Map[i32, Vec[i32]]`, `HashMap` and
`HashSet` to `Map` and `Set`, `entry().or_default()` to
`entry().or_insert(Vec.new())`, `let n = n.borrow();` deleted, `&n.left`
and `&root` to bare arguments and `&mut graph` to `mut graph`, `::new`
to `.new`, `!` to `not`, `for &w in &graph[&v]` to `for w in ref
graph[v]`, `struct Solution;` to `struct Solution {}`, `Solution::` to a
dot, and the adapter's `as i64` dropped. The `VecDeque`, the level loop
over `queue.len()` and `seen.insert(w)` as the test stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the nodes listed with their parents, and minute by minute
every node not yet infected checked against every infected one for
being its parent or its child, until all are. No heights and no search.
It checks 300 random trees of 1 to 12 nodes, which the literal reading
answers; then 30 of up to 300; then 30 of up to 300 that are nearly a
chain, each node hung below one of the last two. Each starts from a
random node, and all 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 nodes, the answer is the literal reading's |
| P2 | at most the nodes less one, and at least the start's depth |
| P3 | the tree mirrored: the same answer |
| P4 | every value `v` made `n + 1 - v`, the start too: the same answer |
| P5 | a new root above the old one: the larger of the answer and the start's depth plus one |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the root is infected no sooner than the start's depth,
and the infection reaches at least one new node a minute. P3 and P4 hold
because neither mirroring nor relabelling moves any node nearer or
farther. P5 holds because the new root is one edge above the old one
and nothing else moves.

The differential prints `360 cases: checksum 886553907, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that grows
the same trees and searches each from its start. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the start's shorter side | P1 75, P6 86 |
| M2 | ★: the far side's height left out | P1 57, P3 163, P6 76 |
| M3 | ★: the distance not grown going up | P1 88, P2 48, P3 141, P5 88, P6 128 |
| M7 | graph: no link from a parent down | P1 218, P6 265 |
| M9 | graph: the minutes from 0 | P1 304, P2 85, P5 95, P6 360 |
| M11 | graph: a child of node 1 never linked | P1 134, P2 67, P4 222, P5 82, P6 153 |
| M13 | parents: no minute counted per step | P1 289, P2 288, P5 360, P6 345 |
| M14 | parents: never down to the left | P1 164, P3 226, P6 209 |
| M15 | parents: a right child's parent never recorded | P1 139, P2 142, P3 204, P5 176, P6 179 |
| M17 | stack: the start's own side one short | P1 81, P6 92 |
| M18 | stack: the other side the start's own | P1 213, P2 117, P5 360, P6 268 |
| M20 | stack: the tallest child the last one | P1 38, P3 88, P6 80 |
| M23 | iter: only the root's edges | P1 246, P2 219, P5 288, P6 302 |
| M24 | iter: each node keeping its last neighbour | P1 190, P2 181, P3 124, P5 249, P6 246 |
| M26 | iter: the left child twice, the right never | P1 245, P2 226, P3 174, P5 226, P6 301 |
| M29 | solution: a right child linked to its grandparent | P1 213, P2 117, P3 308, P5 195, P6 269 |
| M31 | solution: the new infected queued in front | P1 111, P3 78, P5 166, P6 167 |

P1 and P6 kill all seventeen, P5 eleven, P2 ten, P3 nine and P4 one.
P3, the tree mirrored, fails the edits that treat the two sides
unalike, as the far side's height left out and the distance not grown
on the left only (M2, M3), never down to the left (M14), a right child's
parent never recorded (M15), the left child twice (M26) and a right
child linked to its grandparent (M29), and those that depend on the
order the children come in, as the tallest child the last one (M20),
each node keeping its last neighbour (M24) and the queue's front (M31).
P4, the values relabelled, fails only the edit that singles out one
value, a child of node 1 never linked (M11). P5, a new root above the
old one, fails the edits that misjudge the path up or count the minutes
wrong, and passes those that only misjudge the start's own subtree, as
its shorter side (M1, M17).

Of the thirty-one, fourteen were not kept. No link from a child up in
the graph arm and the template (M8, M28), never up to the parent in the
parents arm (M12), the distance passed up one short in the stack arm
(M19) and each edge one way in the iter arm (M22) all never look above
the start, answer the height of its own subtree, and fail alike. The
parents arm's branches added and the template's minute per node (M16,
M27) both answer the nodes less one, and the iter arm's start not seen
and the template's start infected again (M25, M30) both count the start
a second time, each pair failing alike. The ★ arm's right-side distance
never passed up, empty side of height -1 and far side of a right start
the right again (M4, M5, M6), the graph arm's only the first infected
spreading (M10) and the stack arm's left child's parent lost (M21) each
fail apart from every kept one, and were left out to keep three to an
arm and two to the template.

## Verification

Every arm prints the same output as `infect.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.9 to 5.7 s, but the iter arm
80 s: its edges come back as a `Vec` from each subtree, extended into
its parent's, so each edge is copied once per level above it, over the
`10^5`-node tree. The differential takes 12.2 s there and 1.0 s under
`karac __mir-llvm-run`.

## Benchmarks

The bench grows 200 random trees of 1000 nodes from the harness's
generator and asks each from 400 starts, start `s` of tree `t` being
`1 + (37s + t) % 1000`, with the ★ arm in all five languages. Every
implementation prints `200 trees of 1000, 400 starts each: checksum
146887072`. Rust's nodes are LeetCode's `Rc<RefCell<TreeNode>>`, the
model of Kāra's `shared struct`; C's are one `malloc`'d array linked by
pointers, Go's `*TreeNode`, and Python's objects with `__slots__`.

BENCHTAB
