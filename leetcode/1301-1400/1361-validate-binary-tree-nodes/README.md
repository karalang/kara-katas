# 1361. Validate Binary Tree Nodes

You have `n` binary tree nodes numbered from `0` to `n - 1` where node
`i` has two children `leftChild[i]` and `rightChild[i]`; return `true`
if and only if all the given nodes form exactly one valid binary tree.

If node `i` has no left child then `leftChild[i]` will equal `-1`,
similarly for the right child.

Note that the nodes have no values and that we only use the node
numbers in this problem.

```
n = 4, leftChild = [1,-1,3,-1], rightChild = [2,-1,-1,-1]  ->  true
n = 4, leftChild = [1,-1,3,-1], rightChild = [2,3,-1,-1]   ->  false
n = 2, leftChild = [1,0], rightChild = [-1,-1]             ->  false
```

**Constraints:** `n == leftChild.length == rightChild.length`,
`1 <= n <= 10^4`, `-1 <= leftChild[i], rightChild[i] <= n - 1`.

Each arm is `fn validate_binary_tree_nodes(n: i32, left_child: Vec[i32],
right_child: Vec[i32]) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `validate_binary_tree_nodes.kara` ★ | every node's parents counted: a tree has exactly one node with none, the root, and no node with two; then a breadth-first search from the root must reach all n nodes, none twice, else a cycle hangs apart from it. O(n) |
| `validate_binary_tree_nodes_dsu.kara` | union-find: each edge joins the child's set to its parent's; an edge to a child that already has a parent, or within one set, fails at once, and a tree is left as exactly one set. O(n α(n)) |
| `validate_binary_tree_nodes_dfs.kara` | the root found as the one node no edge points to, then a recursive walk from it that marks each node when first reached; reaching a marked node is a second path to it, and a tree's walk counts all n nodes. O(n) |
| `validate_binary_tree_nodes_climb.kara` | each node's one parent written down, the one node with none the root, then every node climbs toward the root, a node known to reach it ending the climb early; a climb longer than n is going round a cycle. O(n) amortized |
| `validate_binary_tree_nodes_solution.kara` | a Rust solution as LeetCode's Rust users write it (in-degrees in a `vec![0; n]`, then `while let Some(u) = stack.pop()` and `for &c in [left_child[u], right_child[u]].iter()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one node,
a node with two parents, two roots, a node its own child, and a cycle
under the root (`true false false true false false false false`); and
2000 random sets of up to 40 nodes, each made as a tree and, one time
in two, broken or not, folded into a checksum (`2000 random cases: 1469
valid, checksum 141636357`). `validate_binary_tree_nodes.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`.

The Mend loop: the ★, union-find and depth-first arms check clean. The
climbing arm wrote `let mut at = start;` with `start` an `i32` from
`0..n`, then `at = parent[at]` with `parent` a `Vec[i64]`; `karac check`
refuses the narrowing (E0200) and asks for an `as i32`
(B-2026-11-25-20), and the binding was given its type by hand, `let mut
at: i64 = start;`. The Rust solution takes 15 fixes: `struct Solution;`
becomes `struct Solution {}`, `Vec<i32>` becomes `Vec[i32]`, `vec![0;
n]` and `vec![false; n]` become `Vec.filled(..)` and `vec![root as
usize]` becomes `[root as i64]`, `n as usize` becomes `n as i64` and the
index casts `as usize` go, and `for &c in` loses its `&`. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the nodes form one binary tree when some node, the
root, reaches every node by exactly one path. For each candidate root
the paths to every node are counted by length, 0 to n, each count held
at 2; a path of n edges goes round a cycle. That reading takes O(n^3),
so it answers sets of up to 10 nodes; the other properties cover the
rest. It checks the examples, then 1500 random sets of up to 10 nodes
and 500 of up to 40.

| | property |
|---|---|
| P1 | the statement read literally, for n up to 10 |
| P2 | the nodes renamed by a random permutation, the same answer |
| P3 | every node's two children swapped, the same answer |
| P4 | a new node hung on a free side, the same answer |
| P5 | a tree with that free side pointed at any node, or with an edge cut, is no longer one |
| P6 | the ★ arm's answer |

All 62,540 checks pass on every arm: `2005 cases: checksum 258483026,
62540 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, testing each set by its parent
counts and a search, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a search one node short accepted | P1 6, P4 2, P6 24 |
| M2 | ★: only left children given a parent | P1 1001, P3 157, P4 48, P6 5148 |
| M3 | union-find: an edge within one set let through | P1 15, P6 15 |
| M4 | union-find: a second parent let through | P1 10, P6 16 |
| M5 | depth-first: a node reached again counted as nothing | P1 156, P5 1343, P6 189 |
| M6 | depth-first: the walk started at node 0 | P1 861, P2 357, P6 1126 |
| M7 | climb: a climb of two steps taken for a cycle | P1 433, P2 267, P6 693 |
| M8 | climb: one child on both sides let through | P1 30, P5 143, P6 31 |
| M9 | solution: the left child pushed in place of the right | P1 1093, P4 140, P6 1369 |
| M10 | solution: the last node's children not counted | P1 642, P2 645, P4 816, P6 816 |

P1 and P6 kill all ten, P4 four, P2 three, P5 two and P3 one. Renaming
the nodes (P2) catches the edits that depend on a node's number: the
walk started at node 0 (M6), a climb's length, which depends on the
order the nodes start in (M7), and the last node's children (M10).
Swapping every node's children (P3) catches the one edit that treats a
left child apart from a right one only one way round: with only left
children given a parent (M2), a tree of left children passes and its
mirror does not. Pointing a tree's free side at one of its nodes (P5)
catches the two edits that let a node have a second parent inside the
tree: reached again and counted as nothing (M5), or the same child on
both sides (M8). The union-find edits (M3, M4) are caught only on the
few sets that join two parts through a second parent or a cycle, which
the literal reading and the ★ arm see.

## Benchmarks

The bench makes 20 sets of 5000 nodes once, 11 of them trees, then asks
5000 questions, each set drawn from the checksum so far, answered by
the ★ arm and folded into the checksum. Every implementation prints
`5000 questions: checksum 250028945`. A set that is a tree takes the
count, the root's scan and the whole search; a broken one stops where
it first fails, the same in every language.

BENCHTAB
