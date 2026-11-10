# 1110. Delete Nodes And Return Forest

Given the `root` of a binary tree, each node in the tree has a distinct
value.

After deleting all nodes with a value in `to_delete`, we are left with a
forest (a disjoint union of trees).

Return the roots of the trees in the remaining forest. You may return
the result in any order.

```
root = [1,2,3,4,5,6,7], to_delete = [3,5]   ->  [[1,2,null,4],[6],[7]]
root = [1,2,4,null,3], to_delete = [3]      ->  [[1,2,4]]
```

**Constraints:** the number of nodes in the tree is at most `1000`;
each node has a distinct value between `1` and `1000`;
`to_delete.length <= 1000`; `to_delete` contains distinct values
between `1` and `1000`.

The arms are `fn del_nodes(root: Option[TreeNode], to_delete: Vec[i32])
-> Vec[Option[TreeNode]]`, where `TreeNode` is a `shared struct` with
`mut` fields: LeetCode's Rust `Option<Rc<RefCell<TreeNode>>>` is Kāra's
`Option[TreeNode]`. A value in `to_delete` need not be in the tree.

## Approaches

| file | mechanism |
|---|---|
| `del_nodes.kara` ★ | one walk from the root: each call is told whether its node's parent is gone, adds the node to the forest when it stays and its parent does not, cuts the links to deleted children on the way back, and returns the node or, when it is deleted, nothing. O(n) |
| `del_nodes_bfs.kara` | a walk level by level: a `VecDeque` holds each node with whether its parent is gone, a node that stays below a gone parent starts a tree, and a link to a deleted child is cut as the child is queued. O(n) |
| `del_nodes_stack.kara` | an explicit stack, as Rust writes a walk with no recursion: each node is pushed with whether its parent is gone, and its links to deleted children are cut when it is popped. Written as Rust and carried to Kāra by `karac fix`. O(n) |
| `del_nodes_parents.kara` | every node and its parent first, in two `Map`s by value, then each deleted value in turn: its parent's link to it cut, and its children that stay starting trees, with the root's tree when the root stays. O(n) |
| `del_nodes_pairs.kara` | a recursion that builds new trees and changes no node: each call returns its subtree with the deleted nodes taken out, `None` when its own node is deleted, and the trees that start below it, through `let mut (left, below) = ..`; a deleted node hands its children up as trees of their own. O(n) |
| `del_nodes_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Rc<RefCell<TreeNode>>`, a nested `fn dfs` that takes each child out with `take()` and puts back what stays), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines, each forest written as LeetCode
writes trees, level by level, and its trees sorted by their roots: the
answers for LeetCode's two examples and eight more (the root deleted,
nothing deleted, everything deleted, a lone node deleted and a lone node
kept, a right-leaning chain, a full tree losing both children of its
root, and a value not in the tree among others), then over 2000 random trees of up to 40 nodes,
each value deleted one time in three, the trees left and a checksum
(`2000 random trees: 10187 trees left, checksum 201786803`), and two of
LeetCode's largest: 1000 nodes with the even values deleted, and a chain
of 1000 with every third deleted. `del_nodes.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a node that stays roots a tree when it has no parent or its
parent is deleted, and its tree is every node below it that stays with
no deleted node between. Each arm answers a freshly parsed tree, since
every arm but the pairs arm changes the tree it is given. It checks
2000 problems in four kinds of 500: up to 12 nodes hung at random, each
value deleted one time in three, and half the time a value from anywhere
in 1 to 1000 put among them; one to three nodes, any of them deleted; a
chain of up to 20, each node to a random side, half deleted; and a
complete tree of up to 31, a quarter deleted. Every random choice is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the forest is the literal one |
| P2 | by a second reading, the links: every node of the forest is a node that stays, met once; every link in it is a link of the tree, on the same side; every root's parent is deleted or there is none; and the forest holds as many nodes as stay |
| P3 | the values to delete in another order, reversed and rotated, give the same forest |
| P4 | deleting in two steps, a random share of the values and then the rest from each tree the first step leaves, gives the same forest |
| P5 | the tree mirrored gives the forest mirrored |
| P6 | the values renamed by a random permutation of 1 to 1000 give the forest renamed |

All 72,000 checks pass on every arm: `2000 problems: checksum 75376671,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, taking every node that stays below a deleted parent and
writing out what stays beneath it, gives the same checksum.

P1 writes the forest from the tree and P2 judges it by its links; P3 to
P6 compare the arm only with itself. P4 feeds an arm's own trees back to
it, and P5 and P6 change the forest back with `mirror` and `relabel`,
which write the `mut` fields of the nodes the arm returned.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a right child never told its parent is gone | P1 988, P2 988, P4 123, P5 1239 |
| M2 | ★: the root never a tree | P1 1206, P2 1206, P4 1195 |
| M3 | ★: a deleted node with a left child left linked | P1 664, P2 664, P4 307, P5 803, P6 664 |
| M4 | bfs: a tree with no left child lost | P1 1314, P2 1314, P4 434, P5 934 |
| M5 | bfs: every right child a tree | P1 1100, P2 1100, P4 1275, P5 1290, P6 1099 |
| M6 | stack: the right children never walked | P1 1345, P2 1345, P5 1251 |
| M7 | stack: a child told its own fate, not its parent's | P1 1239, P2 1239 |
| M8 | stack: every kept node a tree | P1 1290, P2 1290, P4 1446, P5 874, P6 1290 |
| M9 | parents: the left link cut whichever side the node is on | P1 393, P2 393, P3 129, P4 138, P5 593, P6 178 |
| M10 | parents: a deleted child with a left child made a tree | P1 502, P2 502, P3 412, P4 319, P5 576, P6 439 |
| M11 | parents: a value not in the tree ends the deletions | P1 131, P2 131, P3 161, P4 404 |
| M12 | pairs: every kept node's children swapped | P1 1290, P2 1290, P4 1290 |
| M13 | pairs: a deleted leaf kept | P1 1448, P2 1448, P4 187 |
| M14 | solution: a deleted node hands its left child up | P1 664, P2 664, P4 205, P5 879, P6 664 |
| M15 | solution: the first value never deleted | P1 1656, P2 1656, P3 908, P4 967 |

P1 and P2 catch all fifteen, P4 thirteen, P5 nine, P6 six and P3
four. P1 and P2 fail on the same problems every time: a forest whose
nodes are the nodes that stay, each met once and linked as in the tree,
with every root's parent gone, is the literal one. P4 is the strongest
self-comparison: two steps feed the first step's trees back in, so an
edit that loses or keeps a node in a way that depends on what is still
attached shows; it misses M6 and M7, which lose the same trees however
the deletions are split. P5 sees the edits that treat left and right
apart, and misses M12, whose swap of every node's children is itself a
mirror. P6 sees the edits that leave a node in two trees: renaming each
tree back renames a shared node twice. P3 sees the four edits that
depend on the order of the values: the parents arm cutting by side
before or after a sibling goes (M9, M10), stopping at a value not in the
tree (M11), and losing the first value (M15). M11 needs the stray value
placed among the others: with it always last, as the generator first
had it, P1 missed M11 and only P3 and P4 caught it. P3 to P6 together
catch fourteen of the fifteen; M7 they cannot, since a kept child of a
deleted node never becomes a tree in every form of the problem alike.

Of the fifteen not kept, two fail as a kept edit: the pairs arm losing a
deleted node's right child as M1, and the solution arm never walking the
right subtree as M6. Two more fail alike in two arms: a deleted node
below a deleted one kept as a tree (★ and solution), and a left child
told its grandparent's fate (bfs and solution). The other nine fail in
ways of their own but were not needed: the ★ arm never cutting a link to
a deleted left child, the bfs arm cutting the right link when the parent
is deleted and cutting the wrong link for a deleted left child, the
stack arm walking the left child twice and keeping a link to a deleted
child with no left child, the parents arm keeping a deleted root with a
left child and taking every node's parent as the root, and the pairs
arm losing the trees below a left child and losing the root's tree when
another starts.

## Verification

Every arm prints the same output as `del_nodes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. The ★, bfs, parents and pairs arms were
written as Kāra, the stack and solution arms as Rust writes them.
`karac fix` carried the stack arm to a clean check in two rounds
(`Option<TreeNode>` to `Option[TreeNode]`, `HashSet` to `Set` and its
`use` dropped, `Vec::new()` to `Vec.new()`, `contains(&n.val)` to
`contains(n.val)`, `&&` and `!` to `and` and `not`) and the solution arm
in seven: `Rc<RefCell<TreeNode>>` to `TreeNode`, each
`n.borrow().val` and `n.borrow_mut().left` to `n.val` and `n.left` with
`take()` kept, the nested `fn dfs` moved out of the `impl`, `&HashSet`
and `&mut Vec` to `Set` and `mut ref Vec`, `struct Solution {}`
declared and `Solution::` to `Solution.`, and `to_delete.into_iter()`
on a borrowed parameter to `to_delete.clone().into_iter()`. Two edits
came from habit and `karac fix` undid them in the Kāra arms: the pairs
arm's Rust `let (left, mut below) = ..` became `let mut (left, below) =
..`, and the ★ arm's `gone: ref Set[i32]` became `gone: Set[i32]`, a
parameter borrowing by default (the `redundant_ref_param` style lint,
which `karac fix` applies and `karac check` does not report). Two hand
edits: the solution arm's discarded `dfs(root, true, set, mut ans);`,
whose warning deliberately has no machine fix, written `let _ = ..`, and
the differential's `back[p.map[v]] = v`, an `i64` into a `Vec[i32]`,
written `v as i32` to acknowledge the narrowing as its warning asks.
The solution arm keeps one leftover of the `use` lines it lost, a blank
line after its header comment.

## Benchmarks

The bench builds 16 tree shapes of 1000 nodes once, LeetCode's largest,
each node hung at a random free place below the ones before it. Each of
200 rounds builds every tree afresh, a heap node per value, and deletes
a third of its values with the ★ arm, a different third each round:
3200 calls, each building its set of values to delete. Every
implementation prints `200 rounds over 16 trees of 1000 nodes: 715498
trees, checksum 151130031`. Rust's nodes are LeetCode's own
`Rc<RefCell<TreeNode>>` and its set a `HashSet`, Go's nodes are on its
collected heap and its set a built-in map, Python's nodes are objects
with `__slots__` and its set a `set`, and C `malloc`s each node, frees
them all after each call, and keeps the values in an open-addressing
table with a multiplicative hash and linear probing.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.124 to 0.176 s | 0.126 s |
| C (`clang -O3`) | 0.123 to 0.176 s | 0.129 s |
| Go | 0.290 to 0.344 s | 0.309 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.308 to 0.356 s | 0.318 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.311 to 0.354 s | 0.320 s |
| Rust (`rustc -O`) | 0.311 to 0.398 s | 0.324 s |
| Kāra (`karac build`) | 0.426 to 0.502 s | 0.440 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.435 to 0.511 s | 0.449 s |
| Python | 1.660 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.4x the time of Rust and Go, and about 3.5x
C's, whose nodes carry no reference count and whose set is a plain
open-addressing table; the gap to Rust was not traced. Python takes
about 4x Kāra's time.
