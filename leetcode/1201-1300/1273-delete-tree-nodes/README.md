# 1273. Delete Tree Nodes

A tree rooted at node 0 is given as follows:

- The number of nodes is `nodes`;
- The value of the `i`th node is `value[i]`;
- The parent of the `i`th node is `parent[i]`.

Remove every subtree whose sum of values of nodes is zero.

Return the number of the remaining nodes in the tree.

```
nodes = 7, parent = [-1,0,0,1,2,2,2], value = [1,-2,4,0,-2,-1,-1]  ->  2
nodes = 7, parent = [-1,0,0,1,2,2,2], value = [1,-2,4,0,-2,-1,-2]  ->  6
```

**Constraints:** `1 <= nodes <= 10^4`; `parent.length == nodes`; `0 <=
parent[i] <= nodes - 1`; `parent[0] == -1`, which indicates that `0` is
the root; `value.length == nodes`; `-10^5 <= value[i] <= 10^5`; the given
input is guaranteed to represent a valid tree.

The arms are `fn delete_tree_nodes(nodes: i64, parent: Vec[i64], value:
Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `delete_tree_nodes.kara` ★ | by recursion: the children listed from the parents, then a depth-first search returns each subtree's sum and the nodes it keeps; a subtree summing to zero keeps none. O(n) |
| `delete_tree_nodes_stack.kara` | by an explicit stack: each node pushed back once more after its children, so it is finished after them, and its sum and count folded into its parent's then |
| `delete_tree_nodes_peel.kara` | by peeling leaves: each node's children counted, the leaves queued in a `VecDeque`, and a node whose children are all done done itself, its sum and count passed up; the children are never listed |
| `delete_tree_nodes_owned.kara` | by an owned tree: the parents built into nested `struct Node`s, each owning a `Vec` of its children, and a method folding its children's (sum, kept) pairs into its own |
| `delete_tree_nodes_shared.kara` | by shared nodes: every node made first as a `shared struct`, each then pushed onto its parent's children through the handle, and the counts taken by recursion over the handles |
| `delete_tree_nodes_solution.kara` | a Rust solution as LeetCode's Rust users write it (`i32` in and out, `vec![vec![]; n]` children, a nested `fn dfs` returning a tuple), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples (`2 6`); 2000
random trees of 1 to 60 nodes, half bushy and half deep, the labels other
than 0 shuffled so a parent can follow its child, with values from -3 to
3 so that zero sums are common (`2000 random trees: 43074 nodes left,
checksum 216986212`); and the constraints' top, 10^4 nodes as a path of
alternating 5 and -5, and as a bush, a deep tree and a path with values
up to 10^5 either way (`0 10000 10000 10000`). `delete_tree_nodes.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the five arms written in Kāra checked clean as first
written. The solution arm takes one round of 35 fixes by `karac fix`'s
count. Kāra has no nested functions, and `karac fix` moved the inner
`fn dfs` out to the top level whole; it also wrote `usize` as `i64`,
dropped the `as usize` casts on indices, rewrote `&Vec<Vec<usize>>`
parameters as plain borrowed `Vec[Vec[i64]]`, `for &v in &children[u]` as
`for v in ref children[u]`, `vec![vec![]; n]` as `Vec.filled(n,
Vec.new())`, gave `cnt` the `i32` type Rust inferred from the return, and
fixed `struct Solution;` and `::`. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a node's subtree is every node whose chain of parents reaches
it, each subtree's sum is added up over all the nodes, and a node remains
when no subtree holding it sums to zero. O(n^3) at worst, on 2000 random
trees of 1 to 30 nodes with values from -2 to 2.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | nothing is left exactly when the whole tree sums to zero |
| P3 | the labels other than 0 renamed by a random permutation, the same count |
| P4 | every value negated, the same count |
| P5 | a new leaf of value 0 anywhere is removed and changes nothing else |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 trees: checksum 339000402,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a subtree summing to zero keeps its nodes | P1 1613, P2 181, P5 2000, P6 8065 |
| S2 | ★: node 1 never hung from its parent | P1 1597, P2 299, P3 1379, P6 7985 |
| K1 | stack: a node's count not cleared at a zero sum | P1 1613, P2 181, P5 2000, P6 1613 |
| K2 | stack: the sums not passed up | P1 1553, P2 477, P6 1553 |
| P1 | peel: a parent finished while a child still waits | P1 1549, P2 263, P3 520, P5 558, P6 1549 |
| P2 | peel: a child adds one node to its parent, not its count | P1 1642, P5 223, P6 1642 |
| W1 | owned: a node not counting itself | P1 1819, P2 1819, P6 1819 |
| W2 | owned: a child adds one node, not its count | P1 1642, P5 223, P6 1642 |
| H1 | shared: a node not counting itself | P1 1819, P2 1819, P6 1819 |
| H2 | shared: the last node never hung from its parent | P1 1588, P2 302, P3 1399, P5 1588, P6 1588 |
| O1 | solution: a lone node of value 0 kept | P1 1026, P2 26, P5 1469, P6 1026 |
| O2 | solution: the children's sums added as absolute values | P1 1176, P2 180, P4 1330, P6 1176 |

All twelve are caught, every one by P1, the statement read literally. P3,
the labels renamed, sees the three edits tied to a label or to the order
labels are met in (S2 and H2 drop a particular node, P1 finishes nodes in
an order the labels decide), and P4, the values negated, only O2, whose
absolute values break the symmetry. P5, a zero leaf added, catches every
edit that keeps a zero-sum subtree.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the children listed from the parents, then a depth-first search
returning each subtree's sum and the nodes it keeps) on 20 random trees
of 10,000 nodes with values from -3 to 3, drawn once, 60 rounds; every
answer folded into a checksum. Every program prints `60 rounds of 20
trees of 10000 nodes: checksum 896149453`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.723 to 0.805 s | 0.742 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.725 to 0.783 s | 0.749 s |
| Rust (`rustc -O`) | 0.720 to 0.776 s | 0.751 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.711 to 0.804 s | 0.725 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.714 to 0.784 s | 0.734 s |
| C (`clang -O3`) | 0.730 to 0.789 s | 0.741 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.729 to 0.801 s | 0.750 s |
| Go | 0.698 to 0.784 s | 0.728 s |
| Python | 4.502 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.725 s
against 0.749 s), and the two ranges overlap. C runs level with Kāra
(0.741 s against 0.749 s); Go runs level with Kāra (0.728 s against
0.749 s). Python takes about 6x Kāra's time. No profile was taken.
