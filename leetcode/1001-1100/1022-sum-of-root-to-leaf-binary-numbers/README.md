# 1022. Sum of Root To Leaf Binary Numbers

Each node of a binary tree holds 0 or 1, so each path from the root down
to a leaf spells a binary number, most significant bit first. Return the
sum of the numbers of all root-to-leaf paths.

```
root = [1,0,1,0,1,0,1]  ->  22   (100 + 101 + 110 + 111 = 4 + 5 + 6 + 7)
root = [0]              ->  0
```

**Constraints:** the tree has 1 to 1,000 nodes, each 0 or 1, and the
answer fits in a 32-bit integer.

## Approaches

Going down to a child doubles the number read so far and adds the
child's bit, so each node's number is its parent's times two plus its
own bit. The node type is a `shared struct`, Kāra's reference-counted
form, as in kata 1008.

| file | mechanism |
|---|---|
| `sum_root_to_leaf.kara` ★ | recursion: pass each call the number read down to its parent; a leaf gives its own number and any other node the sum of its children's. O(n) |
| `sum_root_to_leaf_stack.kara` | an explicit stack: depth first without recursion, each node pushed with its parent's number; a node popped extends it and either adds it, at a leaf, or pushes its children. O(n) |
| `sum_root_to_leaf_bfs.kara` | level by level: breadth first over a `VecDeque` of nodes with their numbers; every leaf taken off the queue adds its number. O(n) |
| `sum_root_to_leaf_paths.kara` | every path spelled out: the statement as written, recording a copy of the bits from the root at each leaf, then reading each path as a binary number. O(n * height) |
| `sum_root_to_leaf_morris.kara` | Morris traversal: preorder with no stack, threading the last node of each left subtree back to its parent with the `mut` link and recognising the thread with `ref_eq`; on the way back it drops as many bits as the thread is long and removes the thread, so the tree is left as it was. O(n) time, O(1) space |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for seven trees in
LeetCode's level order (with -1 for a missing child), LeetCode's two
examples among them; for six groups of random trees (7 to 1,000 nodes,
with a 1 at each node with probability 1/8 to 8/8), the sum of the
answers, the largest and a checksum; and the answers for a path of 31
ones (`2^31 - 1`) and the full tree of 10 levels, all ones. A random
tree hangs each new node at the end of a random walk from the root and
is kept to 31 levels, so every number fits in 31 bits, as LeetCode's
bound on the answer implies. `sum_root_to_leaf.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: find every leaf, search the tree for the path down to it,
spell the path as a string of `0`s and `1`s and read it as a binary
numeral. It checks 2,799 trees: every tree of 1 to 5 nodes with every
choice of bits (1,618), every shape of 6 or 7 nodes with random bits
(561), 600 random trees of 8 to 60 nodes and 20 of 300 to 1,000, with a
1 at each node with probability 1/8 to 7/8. Each arm gets a copy of the
tree of its own, and each tree is also asked with every bit turned
over, mirrored, and hung below a new root of 0 and of 1.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree left as the arm found it, compared in preorder |
| P3 | with every bit turned over each path reads as its complement, so the two answers add up to the all-ones number of every path, `2^d - 1` for a leaf `d` deep |
| P4 | below a new root of 0 the answer does not change, and below a new root of 1 each path gains a top bit, adding `2^d` for each leaf |
| P5 | the mirror image has the same paths and the same answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `2799 trees: checksum 413835313, 83970 checks
over 5 arms: 0 failures` under `karac __mir-run` (19 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error, so the Morris arm's threads, a reference cycle while they stand,
are all removed.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, each fails the same checks under both, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the number never doubled | P1 2557, P3 2797, P4 2799, P6 2557 |
| M2 | ★: a right child missing its parent's bit | P1 2346, P3 2735, P4 2799, P5 2261, P6 2346 |
| M3 | ★: every bit read inverted | P1 2799, P4 2799, P6 2799 |
| M4 | stack: a node with no left child taken for a leaf | P1 2023, P3 2339, P4 2799, P5 2417, P6 2023 |
| M5 | stack: right children never pushed | P1 2628, P3 2735, P4 2799, P5 1481, P6 2628 |
| M6 | stack: a left child given 1 more than its parent's number | P1 2735, P3 2735, P4 2799, P5 2600, P6 2735 |
| M7 | bfs: the root's bit ignored | P1 1392, P3 2799, P4 2799, P6 1392 |
| M8 | bfs: every left child read as 1 | P1 2155, P3 2735, P4 1407, P5 2544, P6 2155 |
| M9 | bfs: a node with no left child taken for a leaf, its right subtree dropped | P1 2253, P3 2339, P4 2799, P5 2438, P6 2253 |
| M10 | paths: each path read least significant bit first | P1 2406, P4 2799, P6 2406 |
| M11 | paths: bits never taken back | integer overflow panic at the shift that reads a path, exit 101 |
| M12 | paths: the number carried over from path to path | P1 1883, P3 2021, P4 2021, P5 1807, P6 1883 |
| M13 | morris: one bit too few dropped on the way back | integer overflow panic at the sum, exit 101 |
| M14 | morris: every thread's node taken for a leaf | P1 1552, P3 1719, P4 2161, P5 2195, P6 1552 |
| M15 | morris: threads never removed | P2 2735 |

P1, P4 and P6 kill twelve of the thirteen that finish, P3 ten, P5 eight
and P2 one; M11 and M13 are killed by Kāra's overflow checks, M11's path
growing past 63 bits and M13's number keeping a bit too many on every
way back. M15 answers every
tree correctly and leaves it threaded: only P2 sees it, on the 2,735
trees with a left child somewhere (the other 64 are chains of right
children, where Morris makes no thread). M3 and M10 read every path the
wrong way, inverted or backwards, but consistently, so the complement
of a path still adds up to all ones under them (P3) and a mirror image
still has the same paths (P5); a new root on top is what shows them. P4
fails on every tree for most edits because a new root of 1 adds a top
bit to every path, which any error in reading a path changes. The checks
draw no random number that depends on an answer, so every mutant sees
the same trees and their counts can be compared.

Fifteen other edits were tried and set aside, none of them equivalent.
Three failed exactly the same checks as a kept one: stack leaving a right
child without its parent's bit (as M2), paths ignoring the root's bit
(as M7) and morris counting its steps from 0, which overflows at the
same sum (as M13). The other twelve were killed too, beyond three per
arm: ★ taking a node with one child for a leaf, giving a missing child
its parent's number, and starting below a 1; stack adding a leaf's
parent's number and doubling every number, which fail alike; bfs
counting leaves, not doubling a right child's number and never queueing
left children; paths skipping the first leaf and recording every bit as
1; and morris taking a node with no left child for a leaf and not
reading a node with a left child.

## Verification

Every arm prints the same output as `sum_root_to_leaf.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. Under `karac __mir-run` the arms take 4.9 s (★) to 6.7 s (paths). No
compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 200 random trees of 1 to 1,000 nodes (LeetCode's
sizes, 99,389 nodes in all), no more than 31 deep, once in all five
languages and answers each tree 500 times with the ★ arm, folding the
answers into a sum and a checksum: about 50 million node visits, each
a recursive call. The Rust version uses
`Option<Rc<RefCell<TreeNode>>>`, LeetCode's Rust signature, walked by
reference with a `borrow()` per node, C a `malloc` per node and Go a
pointer per child. Every implementation prints `200 trees, 99389
nodes, 500 rounds: sum 10959179000, checksum 677717791`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.512 to 0.609 s | 0.549 s |
| Rust (`rustc -O`) | 0.686 to 0.796 s | 0.720 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.751 to 0.953 s | 0.780 s |
| Go | 0.454 to 0.573 s | 0.496 s |
| Python | 7.9 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.699 to 0.776 s | 0.726 s |
| Kāra (`karac build`) | 0.706 to 0.761 s | 0.722 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 0.93 times Rust's median time under overflow checks and 1.32
times C's. Go ran fastest, ahead of C; we did not measure why, nor
where Kāra's time goes against C's. Each Kāra node is reference-counted,
as is each Rust one.
