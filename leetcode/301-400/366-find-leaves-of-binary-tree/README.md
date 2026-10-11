# 366. Find Leaves of Binary Tree

Given the root of a binary tree, collect its leaves, remove them, and repeat
until the tree is empty. Return the collected nodes, one group per round.

```
[1,2,3,4,5]   -> [[4, 5, 3], [2], [1]]
[1]           -> [[1]]
```

**Constraints:** `1 <= number of nodes <= 100`; `-100 <= Node.val <= 100`.

## Approaches

Every arm reads the tree in LeetCode's level-order form, `"[1,2,null,3]"`,
into child links by node id, and returns each group left to right.

| file | mechanism | time |
|---|---|---|
| `find_leaves.kara` ★ | a node leaves in round `h` exactly when its height is `h`, a leaf being height 0, so one postorder walk over a `shared enum Tree` that files each value under its height gives every round at once | O(n) |
| `find_leaves_strip.kara` | do what the problem says: each round walks the tree, collects the leaves, and builds the tree without them, until it is empty | O(n · h) |
| `find_leaves_peel.kara` | peel on the links alone: count each node's children, start from the nodes with none, and let a parent join the next round when its count reaches zero, like Kahn's algorithm; each round is sorted by preorder position | O(n log n) |
| `differential.kara` | the three arms against an oracle that simulates the rounds on the links, 30,000 checks, five properties | — |

The tree is `shared enum Tree { Empty, Node(i64, Tree, Tree) }`, the form
the spec gives for recursive data. The strip arm builds new nodes for what
survives each round rather than mutating the old ones.

Every arm prints the same 10 lines: the two LeetCode examples, seven edge
cases (an empty tree, a left chain, a right chain, a perfect tree, a
shallow leaf beside a deep one, negative and repeated values, a two-node
tree), and the group count and a checksum over 400 random trees.
`find_leaves.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the three arms, plus an oracle that
simulates the rounds directly: each round takes, in preorder, every
remaining node whose children are all gone. The test draws 2,000 random
level-order lists of up to 25 slots, a third of them empty, half with
values in `[-2, 2]` so that repeated values are common.

| | property |
|---|---|
| P1 | each arm gives the oracle's groups |
| P2 | the groups hold every value exactly once |
| P3 | there is one group per level of height |
| P4 | mirroring the tree reverses every group |
| P5 | the first group is the leaves and the last is the root alone |

It prints `2000 cases, 30000 checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | height: the shorter child decides | P1, P3, P4 and P5, 6395 failures |
| M2 | height: the right child's height is ignored | P1, P3, P4 and P5, 5032 failures |
| M3 | strip: a node is a leaf when its left child is empty | P1 to P5, 5646 failures |
| M4 | strip: strips the right subtree first | P1, 1329 failures |
| M5 | peel: rounds left in level order, unsorted | P1 and P4, 1922 failures |
| M6 | peel: counts only left children | P1, P3, P4 and P5, 5032 failures |
| M7 | peel: preorder visits right before left | P1, 1329 failures |
| M8 | oracle: scans the right subtree first | P1, 3987 failures |

## Verification

All three arms print the same output as `find_leaves.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program turns five random level-order lists of 400,000 slots
into trees and groups each with the ★ arm. The Rust mirror uses `Rc` for
the shared enum and the C mirror counts references by hand; Go uses plain
pointers under its garbage collector. The Kāra build and all four mirrors
print `151 groups, checksum 70374960`, and `karac __mir-run` does too, in
188 seconds against Python's 2.2. Timings are not taken yet; they need a
quiet machine.

## Compiler findings

None.
