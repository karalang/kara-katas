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
188 seconds against Python's 2.2.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 51.8 ms ± 0.5 | 1.76× |
| go `go build` | 66.7 ms ± 1.0 | 1.37× |
| **kāra `karac build`, seq** | **91.3 ms ± 1.2** | **—** |
| rust `-O` | 96.0 ms ± 1.4 | 0.95× |
| rust `-O -C overflow-checks=on` (equal-safety) | 97.3 ms ± 1.6 | 0.94× |

Kāra is 0.95× `rustc -O`, 0.94× equal-safety Rust, 1.76× C and 1.37× Go.
The gaps were not investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 51.9 ms ± 0.9 | 32.9 KiB | 26.5 MiB |
| rust | 125.4 ms ± 2.0 | 456.7 KiB | 54.1 MiB |
| kāra | 135.8 ms ± 2.9 | 66.9 KiB | 50.1 MiB |
| go | — | 2450.6 KiB | 42.9 MiB |

`karac build` is 2.6× clang's cold compile and 1.1× rustc's. Kāra's
68,520-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`151 groups, checksum 70374960`).

## Compiler findings

None.
