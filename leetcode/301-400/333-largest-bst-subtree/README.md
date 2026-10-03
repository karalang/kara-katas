# 333. Largest BST Subtree

Given the root of a binary tree, return the number of nodes in its largest
subtree that is a binary search tree. In a BST every value in a node's left
subtree is smaller than the node's and every value in its right subtree is
larger, so equal values are not allowed. A subtree is a node and all of its
descendants.

```
[10,5,15,1,8,null,7]                             ->  3   (5, 1 and 8)
[4,2,7,2,3,5,null,2,null,null,null,null,null,1]  ->  2
```

## Approaches

A subtree is a BST exactly when both child subtrees are, the left one's
largest value is below the node's, and the right one's smallest is above it.
Three arms decide that bottom-up, one node at a time. The fourth checks each
subtree from scratch.

| file | mechanism | cost |
|---|---|---|
| `largest_bst.kara` ★ | post-order over the index pool. Each call returns an `Info { bst, size, lo, hi }` struct, and the best size goes in a `best: mut ref i64` | `O(n)` time, `O(height)` stack |
| `largest_bst_shared.kara` | the same post-order over linked `shared struct TreeNode`s with `Option` children, returning a tuple `(size, lo, hi)` where size 0 is the empty tree and -1 is "not a BST" | `O(n)` time, `O(height)` stack |
| `largest_bst_iter.kara` | no recursion: a preorder walk with an explicit stack lists every node after its parent, and walking that list backwards fills parallel arrays | `O(n)` time and space |
| `largest_bst_naive.kara` | top-down: if the subtree here is a BST its size is the answer, otherwise take the larger child answer. The check passes the open interval down, with a missing bound as `None` | `O(n · height)` time |
| `differential.kara` | the four arms, a brute-force oracle and eight properties on 11,797 trees | — |
| `bench/largest_bst.kara` | 200 solves of a 100,000-node tree with one node damaged each time, by the ★ arm | — |

The index pool is the corpus's usual tree (`Vec[Node]` with child indices,
-1 for none), built from LeetCode's level-order array. The linked arm builds
the same pool and links it into `TreeNode`s before solving, so all four arms
answer the same trees.

The three bottom-up arms only read a child's range when that child exists,
and the top-down arm uses `None` for a missing bound, so no arm needs a
sentinel value. One edge case checks that: a root of `i64.MIN` with a right
child of `i64.MAX` answers 2.

Every arm prints the same 19 lines: the two examples, ten edge cases (empty,
one node, three equal values, a BST, a non-BST of three, left and right
chains, a BST under a non-BST root, an eight-node BST, and the two extreme
values), six random trees, and two trees of 20,000 nodes, one intact and one
with 40 nodes damaged. The random trees are BSTs built by insertion with
equal values sent right, which a strict BST does not allow, and some damaged
nodes. The four arms' output is byte-identical, and `largest_bst.py` mirrors
the ★ arm.

## Differential

`differential.kara` checks every tree shape with at most 5 nodes, with every
assignment of values from {0, 1, 2}: 11,497 trees, most of them with
repeated values. The oracle is brute force: a subtree is a BST exactly when
its in-order walk is strictly increasing, and the oracle tries every subtree.
It then runs eight properties on 300 random trees of 1 to 40 nodes, in four
kinds: BSTs of distinct values, BSTs with repeated values, BSTs with one to
three damaged nodes, and random shapes with random values.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | the answer equals the brute-force oracle (exhaustive and random trees) |
| P3 | a BST of distinct values answers its own size |
| P4 | a non-empty tree answers between 1 and its size |
| P5 | a tree answers at least as much as each child's subtree does |
| P6 | mirroring the tree and negating every value keeps the answer |
| P7 | adding a constant to every value keeps the answer |
| P8 | under a new root larger than every value, the answer becomes size + 1 when the tree was a BST, and stays the same when it was not |

Only 14 of the exhaustive trees are BSTs as a whole, because three values
leave room for at most three distinct ones (3 one-node trees, 6 two-node
trees and 5 three-node trees, one per shape).

`11497 exhaustive trees (14 wholly BSTs), 300 random trees, 0 failures`, on
every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: allow an equal value on the left | **killed** | P1, P2, P6 |
| M2 | ★: allow an equal value on the right | **killed** | P1, P2, P6 |
| M3 | ★: compare the left subtree's smallest value, not its largest | **killed** | P1, P2, P6 |
| M4 | ★: do not carry the left subtree's smallest value up | **killed** | P1, P2, P6 |
| M5 | ★: count a subtree that is not a BST | **killed** | P1, P2 |
| M6 | linked: allow an equal value on the left | **killed** | P1 |
| M7 | linked: take the left range even from an empty subtree | **killed** | P1 |
| M8 | top-down: allow a value equal to the lower bound | **killed** | P1 |
| M9 | top-down: check each node only against its parent | **killed** | P1 |
| M10 | top-down: take the left child's answer only | **killed** | P1 |
| M11 | iterative: push the right child before the left | silent (equivalent) | — |
| M12 | iterative: carry the right subtree's smallest value as its largest | **killed** | P1 (21 failures) |
| M13 | all four arms: allow an equal value on the left | **killed** | P2, P6 |
| M14 | oracle: accept a non-decreasing in-order walk | **killed** | P2 |

M11 is equivalent: the backwards walk only needs each node listed after its
parent, which either push order gives. M13 breaks every arm the same way, so
P1 cannot see it. The oracle catches it, and so does P6, because mirroring
turns "equal on the left" into "equal on the right". M9 is the classic
mistake for this problem (a grandchild on the wrong side of its grandparent),
and only P1 catches it because the other arms are right. P3, P4, P5, P7 and
P8 killed nothing that P1 or P2 did not already catch.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all five programs are
valgrind-clean (`All heap blocks were freed`) at `-O0` with
`KARAC_AUTO_PAR=0`. The four arms' output is byte-identical to
`largest_bst.py`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 42385374`).

## Benchmarks

`bench/largest_bst.kara` and its four mirrors time the ★ arm as written. One
random BST of 100,000 distinct values is built once, by inserting a shuffled
range into the index pool. Each of 200 punches gives one random node a random
value, which usually breaks the BST around it, solves, and puts the value
back, so every punch walks the whole tree. The sink is a rolling hash of the
answers. The Python mirror keeps the pool as three parallel lists rather than
a list of node objects; the other three mirror the Kāra struct layout.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, karac built
from `main` at `bc22c5fe2` with this thread's unpushed commits (none touches
the code this kernel compiles to), measured 2026-10-03. Python is its own
lane.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O -C overflow-checks=on` (equal-safety) | 397.9 ms ± 15.7 | 1.00× |
| rust `-C target-cpu=x86-64-v3` (matched) | 398.5 ms ± 19.7 | 1.00× |
| rust `-O` | 401.7 ms ± 20.6 | 1.01× |
| c `-march=x86-64-v3` (matched-ISA) | 406.3 ms ± 16.6 | 1.02× |
| c `clang -O3` | 413.1 ms ± 26.2 | 1.04× |
| **kāra `karac build`** | **418.6 ms ± 11.6** | **1.05×** |
| go `go build` | 440.8 ms ± 19.4 | 1.11× |
| python 3 | 4959.5 ms ± 194.4 | 12.5× |

**All four compiled languages are within 11% of each other, and Kāra is 5%
behind equal-safety Rust and level with C within the noise.** The kernel
chases child indices through a pool laid out in insertion order, so most of
each visit is probably a cache miss, which would hide the instruction counts
that separate the languages elsewhere. That is inferred from the near-tie,
not measured. The order of the Rust and C rows is not
meaningful at these spreads.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 79.5 ms ± 5.6 | 15.8 KiB | 4.5 MiB |
| rust | 141.7 ms ± 6.2 | 3864.3 KiB | 5.2 MiB |
| kāra | 400.7 ms ± 10.4 | 354.0 KiB | 6.1 MiB |
| go | — | 2167.2 KiB | 11.0 MiB |
| python | — | — | 17.1 MiB |

`karac build` is 5.0× clang's cold compile and 2.8× rustc's. Kāra's binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**None.** Every arm was byte-identical on every surface and valgrind-clean
from the first run. Writing the differential hit two diagnostics, both
correct: `distinct` is a reserved word (the parser named the
`r#distinct` escape), and `!placed` is not Kāra (`karac fix` rewrote both uses to
`not`). That says little about the diagnostics: the author already knows the
language, which is why authoring like this never counts toward the
machine-fix rate.
