# 1367. Linked List in Binary Tree

Given a binary tree `root` and a linked list with `head` as the first
node.

Return True if all the elements in the linked list starting from the
`head` correspond to some downward path connected in the binary tree
otherwise return False.

In this context downward path means a path that starts at some node and
goes downwards.

```
head = [4,2,8],       root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]  ->  true
head = [1,4,2,6],     root = same                                                     ->  true
head = [1,4,2,6,8],   root = same                                                     ->  false
```

**Constraints:** the tree has 1 to 2500 nodes, the list 1 to 100, and
every value is from 1 to 100.

Each arm is `fn is_sub_path(head: Option[ListNode], root:
Option[TreeNode]) -> bool`, over `shared struct` nodes.

## Approaches

| file | mechanism |
|---|---|
| `linked_list_in_binary_tree.kara` ★ | every tree node tried as the start of the list, and from each the list matched down the tree by recursion, one node a step, either child carrying the next value. O(n m) for n tree nodes and a list of m |
| `linked_list_in_binary_tree_kmp.kara` | the list read into a pattern and its Knuth-Morris-Pratt failure table built; one walk down the tree carries how much of the pattern the path above ends with. O(n + m) |
| `linked_list_in_binary_tree_paths.kara` | the list read into a pattern; one walk down the tree keeps the values on the path from the root in a `Vec`, and at each node checks whether the path ends with the pattern. O(n m) |
| `linked_list_in_binary_tree_stack.kara` | the ★ arm's search without recursion: a stack of (tree node, list node, start) triples, each a list node still to be matched at a tree node, the start flag also trying the list afresh at every child. O(n m) |
| `linked_list_in_binary_tree_solution.kara` | a Rust solution as LeetCode's Rust users write it (two `fn`s nested in the method over `&Option<Box<ListNode>>` and `&Option<Rc<RefCell<TreeNode>>>`, `match head { None => true, Some(h) => match root { .. } }`, `let r = r.borrow();`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, and a
chain of 2500 nodes valued 1 against 100 1s and against 99 1s and a 2
(`true true false true false`); and 2000 random trees of up to 300
nodes valued from 1 to 2, 3 or 100, half the lists read down a path of
the tree and half drawn at random, folded into a checksum (`2000 random
trees: 1473 found, checksum 60156236`). `linked_list_in_binary_tree.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`, the chain taking the recursive arms 2500 calls deep.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 66 fixes by `karac fix`'s count, from 30
parse errors: the two `use` lines deleted, `struct Solution;` to `struct
Solution {}`, `Option<Box<ListNode>>` to `Option[ListNode]` and
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `&Option<..>` on
the list to `ref Option[..]` and on the tree dropped, `&&` and `||` to
`and` and `or`, every `&` on an argument dropped, `let r = r.borrow();`
to the handle itself, and the two nested `fn`s lifted to the top level.
Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every node is the bottom of one downward path of each
length, so the tree's nodes are listed with their parents, and from
each the path is read upward, as long as the list, and compared with it.
It checks the examples, 1000 random trees of up to 30 nodes valued 1 or
2, where partial matches are common, and 1000 of up to 300 valued from
1 to 2, 3 or 100; half the lists are read down a path of the tree and
half drawn at random.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree mirrored, the same answer |
| P3 | a list found leaves the list without its last value, and without its first, found too |
| P4 | the tree hung under a new root valued 0, a value no list holds, the same answer |
| P5 | a list read down a random path of the tree is found |
| P6 | the ★ arm's answer |

All 53,375 checks pass on every arm: `2003 cases: checksum 242121326,
53375 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, matching each list against
every root-to-node path's end, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the left child carrying the next value | P1 256, P2 191, P5 375, P6 1024 |
| M2 | ★: starts tried only at the root and its children | P1 460, P3 88, P4 459, P5 605, P6 1840 |
| M3 | kmp: a mismatch falls back to the start | P1 18, P3 6, P5 11, P6 18 |
| M4 | kmp: the right child handed the parent's state | P1 179, P2 165, P5 317, P6 179 |
| M5 | paths: the pattern compared backwards | P1 176, P5 278, P6 176 |
| M6 | paths: a node's value never popped | P1 143, P2 144, P5 144, P6 143 |
| M7 | stack: the first mismatch ends the search | P1 1030, P2 122, P3 78, P4 492, P5 1326, P6 1030 |
| M8 | stack: only a smaller value a mismatch | P1 178, P6 178 |
| M9 | solution: the left subtree never searched | P1 417, P2 386, P3 75, P4 1105, P5 556, P6 417 |
| M10 | solution: a missing child matches the last value | P1 92, P3 5, P6 92 |

P1 and P6 kill all ten, P5 eight, P2 and P3 five each, and P4 three.
Mirroring the tree (P2) catches the edits that treat the two children
differently: only the left child followed (M1), the right child handed
the wrong state (M4), the left subtree skipped (M9), the first mismatch
ending a stack that holds the right child's work (M7), and a path that
keeps a left sibling's value (M6). Shortening a found list (P3) catches
the edits that can find a list and miss one of its shorter forms: the
list without its first value starts a level lower, which the edits that
try too few starts miss (M2, M7, M9); the KMP walk falling back to the
start (M3) misses a list that begins partway through an earlier near
match; and a missing child taken for the last value (M10) finds a list
that runs one past a leaf, whose tail need not be in the tree at all. A
new root above the tree (P4) moves every start one level down and puts
the whole old tree on the left, which the edits that search only part of
the tree feel: starts near the root only (M2), a search ended at the
first mismatch (M7), which the new root's 0 always is, and the left
subtree skipped (M9). A path read from the tree (P5) is missed by every
edit that loses matches, but not by the two that find too many: a larger
value let through (M8) and a missing child taken for the last value
(M10).

## Benchmarks

The bench builds 20 trees of 2500 nodes valued 1 or 2, the
constraints' most nodes, each node hung on a random empty child place,
once; then makes 2 * 10^4 rounds, each flipping one node's value and
searching that tree for a list of 8 to 15 values, all drawn from the
checksum so far, with the ★ arm. Every implementation prints `20000
rounds over 20 trees of 2500 nodes: 8858 found, checksum 160201273`. The
work is the recursive search through the tree's nodes, the same in
every language; each round also builds its list of nodes. C and Go use
plain pointers, Rust LeetCode's own `Option<Box<ListNode>>` and
`Rc<RefCell<TreeNode>>`.

BENCHTAB
