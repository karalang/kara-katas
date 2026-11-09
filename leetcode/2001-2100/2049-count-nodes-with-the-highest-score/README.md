# 2049. Count Nodes With the Highest Score

There is a binary tree rooted at `0` consisting of `n` nodes, labelled
`0` to `n - 1`, given as an array `parents` where `parents[i]` is the
parent of node `i`. Since node `0` is the root, `parents[0] == -1`.

The score of a node is found by removing the node and the edges connected
to it: the tree becomes one or more non-empty subtrees, and the score is
the product of their sizes. Return the number of nodes that have the
highest score.

```
parents = [-1, 2, 0, 2, 0]  ->  3
parents = [-1, 2, 0]        ->  2
```

**Constraints:** `2 <= n <= 10^5`; `parents[0] == -1`; `0 <= parents[i] <=
n - 1` for `i != 0`; `parents` represents a valid binary tree.

Taking a node out leaves at most three pieces: its children's subtrees and
the rest of the tree, `n` minus its own subtree's size. So every score
follows from the subtree sizes, and the largest, three pieces of about
`n / 3` each, is under 4 * 10^13, well inside 64 bits.

## Approaches

| file | mechanism |
|---|---|
| `highest.kara` ★ | the children listed from `parents`, an explicit stack gives a preorder, and walking it backwards sums every subtree's size into its parent's. A node's score is its children's sizes times `(n - size).max(1)`; the best and its count kept in one pass |
| `highest_recursive.kara` | a recursive depth-first search: each call returns its subtree's size and scores its node on the way back up, keeping the best and its count behind `mut ref`s. 100000 calls deep on a path |
| `highest_leaves.kara` | from the leaves in, Kahn's order: each node waits for as many children as it has, a `VecDeque` collected from a filter starts with the leaves, and a finished node hands its size to its parent and multiplies it into the parent's score. No child lists |
| `highest_bfs.kara` | breadth-first order from the root with a `VecDeque`, walked backwards for the sizes; each node's parts gathered into a `Vec` and multiplied with `product()` |
| `highest_tree.kara` | the tree as a `Tree` struct of left and right children (`-1` for none), with methods: `sizes` walks it in postorder with an explicit stack of `(node, children pushed)` pairs, `score` multiplies the up to three parts; the scores collected, then `max` and a counting `filter` |
| `highest_solution.kara` | LeetCode's Rust template (`vec![vec![]; n]` children lists filled from index 1, a recursive `Self::dfs` over `&Vec<Vec<usize>>` with `&mut` best and count, `for &child in &children[node]`, `0i64` and `n as i64`), carried by `karac fix` in four rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five more,
each tree and its answer; then the sum and a checksum of the answers for
2000 random binary trees of 2 to 30 nodes, from paths to any shape; then
for four trees of 10^5 nodes, the most the constraints allow: a path, a
comb (a path with a leaf under each of its nodes), a complete binary tree
and a random one. `highest.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each node taken out in turn, the rest of the tree split into
its pieces by a search over the edges in both directions, and the pieces'
sizes multiplied. It checks 500 binary trees of 2 to 30 nodes, each drawn,
relabelled and doubled before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 1 and at most the number of nodes |
| P3 | the tree with its nodes other than the root relabelled at random has the same answer |
| P4 | two copies of the tree hung under a new root: the copies' best nodes pair up, so the answer is odd exactly when the new root's score is the highest |
| P5 | the two copies under a new root have the answer the statement read literally gives |
| P6 | each arm agrees with at least three of the other five |

In P4 the new root is a best node for 99 of 500 random trees, so both
sides of the property are exercised. The relabelling keeps node 0 the
root, as the constraints do.

The differential prints `500 trees: checksum 510980257, 18000 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-three edits to the differential, five or six to each of its arms,
then four more, three to the recursive arm and one to the ★ arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and no
two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the first child pushed | P1 93, P3 52, P4 361, P5 362, P6 93 |
| M2 | ★: the rest counted with the node in it | P1 144, P4 116, P5 118, P6 144 |
| M3 | ★: a new best counted twice | P1 500, P2 20, P4 500, P5 500, P6 500 |
| M4 | recursive: a tie counted twice | P1 133, P2 26, P4 341, P5 362, P6 133 |
| M5 | recursive: an equal score resetting the count | P1 133, P4 341, P5 362, P6 133 |
| M6 | recursive: a child's size not added to its parent's | P1 263, P4 302, P5 339, P6 263 |
| M7 | leaves: a child's part added, not multiplied | P1 195, P4 159, P5 159, P6 195 |
| M8 | leaves: the lowest score counted (`min`) | P1 292, P4 159, P5 378, P6 292 |
| M9 | leaves: the rest counted one short | P1 160, P4 13, P5 34, P6 160 |
| M10 | bfs: the nodes walked in breadth-first order forwards | P1 213, P4 134, P5 291, P6 213 |
| M11 | bfs: a new best counted as 0 | P1 500, P2 500, P4 159, P5 500, P6 500 |
| M12 | bfs: the rest a part of the root too | P1 79, P4 159, P5 159, P6 79 |
| M13 | tree: a second child overwriting the first | P1 106, P3 53, P4 361, P5 362, P6 106 |
| M14 | tree: the right child's size never added | P1 75, P3 50, P4 291, P5 312, P6 75 |
| M15 | tree: a missing child read as size 1 | P1 130, P4 153, P5 177, P6 130 |
| M16 | solution: the size returned one short | P1 461, P4 159, P5 500, P6 461 |
| M17 | solution: the rest left out | P1 120, P4 341, P5 362, P6 120 |

P1, P4, P5 and P6 kill all seventeen, P3 three and P2 three. P5 asks the
literal question again on a tree twice the size, so it fails wherever P1
does and usually more often. P4 needs no literal answer for the copies
themselves, only the new root's score against the rest, and it still
fails for every kept edit: a wrong count or a wrong score breaks the
pairing of the two copies' best nodes. P3 sees only the edits that drop a
child (M1, M13, M14): which child is dropped depends on the labels, so a
relabelled tree answers differently. P2 sees counts that leave the range,
a new best counted as 0 (M11), or more than the tree has (M3, M4).

Of the first thirty-three, five were not kept for not being killed
cleanly. Two are equivalent: the recursive search started at node 0, not
the root, since the constraints make node 0 the root, and the leaves arm
leaving out a rest of exactly 1, which multiplies by 1. Three crash: a
parent queued in the leaves arm before its last child overflows a score;
the Rust arm taking the root as a child of itself recurses until the stack
is gone; and its adapter dropping the last parent indexes past the end.

The rest fail as a kept one does. The ★, recursive, Rust and BFS arms make
the same mistakes the same way: an equal score resetting the count (★,
Rust) and a child's size added, not multiplied (★) fail as M5; a forwards
walk (★) as M6; the rest left out (recursive, tree) and the rest's part
always 1 (★) as M17; a lower score taken as the best (recursive) as M8; a
child's size added for the score (Rust) as M7; each subtree counted
without its own node (recursive) as M16; and the parts added (BFS) and
each score starting at 0 (recursive) as each other. The other edits to the
tree and BFS arms, only the first child queued, a node's size summed
before its children's and the best nodes counted one short, fail on
checks of their own.

## Verification

Every arm prints the same output as `highest.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
The recursive arms run 100000 calls deep on the path under every lane.
Under `karac __mir-run` the arms take 7.1 s (recursive) to 11.1 s (BFS);
the differential takes 3.6 s; on kara 5b92ac6e23.

The five Kāra arms met no compiler gap and checked as written, apart from
one `vec![..]` that `karac fix` turned into a list literal.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in four rounds of 15, 7, 4 and 1 edits to a clean check: `Vec<..>` to
`Vec[..]`, `Self::dfs` to `Solution.dfs`, the `&` and `&mut` arguments and
parameter types to bare arguments, `ref` and `mut ref`, `vec![vec![]; n]`
to `Vec.filled(n, Vec.new())`, the `0i64` suffix and `n as i64` dropped,
and `&child` in the `for` pattern dropped. The children lists are built
from the `i64` indices `0..parents.len()` gives, while `dfs` took them as
`&Vec<Vec<usize>>`. A `usize` meeting an `i64` as a plain value already
had its fix to `i64`; nested in a parameter's type it was refused, "a
number held inside a collection ... keeps its type", with no fix. Kata
2049 added that fix to the compiler (kara 5b92ac6e23,
`tests/kata_2049_nested_usize_fix.rs`):
every `usize` written in the arm becomes `i64`, and the `parents[i] as
usize` index becomes `as i64`, which the `i32` parents need. The adapter
hands the harness's `i64`s to the template `as i32` and widens the `i32`
count back.

## Benchmarks

The bench draws 50 binary trees of 10^5 nodes, each node hung under one
of the `reach` nodes before it, `reach` running from 1 (a path) to 49001,
and answers each with the ★ arm in all five languages: five million nodes
scored. Drawing the trees is part of the work timed. The C mirror keeps
each node's children in a growable array, as the others keep a list.
Every implementation prints `50 trees: sum 51, checksum 308526581`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `5b92ac6e23` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.860 to 0.955 s | 0.888 s |
| Rust (`rustc -O`) | 0.921 to 0.983 s | 0.946 s |
| Kāra (`karac build`) | 0.906 to 0.997 s | 0.944 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.913 to 1.024 s | 0.957 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.060 to 1.121 s | 1.087 s |
| Go | 1.266 to 1.393 s | 1.331 s |
| Python | 34.7 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.928 s) is not above its real time (0.944 s).

The sequential Kāra program is 0.88x Rust under overflow checks and 1.08x
C.
