# 1028. Recover a Tree From Preorder Traversal

We run a preorder depth-first search on the root of a binary tree. At
each node we output `D` dashes, where `D` is the depth of the node (the
root has depth 0, its children depth 1), then the value of the node. If
a node has only one child, that child is guaranteed to be the left
child. Given the output `traversal`, recover the tree and return its
root.

```
traversal = "1-2--3--4-5--6--7"     ->  [1,2,5,3,4,6,7]
traversal = "1-2--3---4-5--6---7"   ->  [1,2,5,3,null,6,null,4,null,7]
traversal = "1-401--349---90--88"   ->  [1,401,null,349,88,90]
```

**Constraints:** the tree has 1 to 1,000 nodes, each value from 1 to
10^9.

## Approaches

In preorder a node comes straight after its parent or after a subtree
of its parent's left child, so its parent is the last node before it
one level up, and the parent's first child to come is its left one. The
node type is a `shared struct`, Kāra's reference-counted form, as in
katas 1022 and 1026.

| file | mechanism |
|---|---|
| `recover_tree.kara` ★ | a stack of the path: read each node's dashes and digits from the string's bytes, pop the path from the root down to the node's depth, and hang the node on the top, on the left if that is free, otherwise on the right. O(n) |
| `recover_tree_recursive.kara` | recursive descent: read the string as the grammar it is, a subtree at depth `d` being `d` dashes, a number, then its left and right subtrees at depth `d + 1`, each there only if the dashes that come next number exactly `d + 1`; one position into the string is shared by every call through a `mut ref`. O(n) |
| `recover_tree_split.kara` | split on dashes: `split("-")` gives each number after as many empty pieces as its depth less one; keep the last node met at each depth in a table, and hang each node below the entry one depth up, read with `i64.parse`. O(n) |
| `recover_tree_slices.kara` | cutting the list: turn the string into a list of (depth, value) nodes, then build each subtree from its stretch of the list, its root first and its right subtree starting at the second node one level below the root. O(n * height) |
| `recover_tree_parents.kara` | looking back for the parent: turn the string into the same list, make every node with `map` and `collect`, then join each to the nearest node before it one level up, in list order. O(n * width) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the trees recovered from seven
strings in LeetCode's level order, LeetCode's three examples among them;
and for six groups of random trees (2,000 of 5 nodes down to 2 of 1,000,
with values up to 1 to 10^9), written out the statement's way, how many
are recovered exactly, how many letters the strings hold and a checksum
of the trees recovered. A random tree hangs each new node at the end of
a random walk from the root, always on the left of a node with no
children. `recover_tree.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms. The statement is
read literally as a check rather than a search: whatever tree an arm
returns, written out the statement's way it must give back the string,
and no node in it may have a right child alone. It checks 588 trees:
every shape of 1 to 7 nodes in which no node has a right child alone (89
shapes), each with values up to 9 and up to 10^9 (178), then 400 random
trees of 8 to 60 nodes and 10 of 200 to 300, with values up to 9, 100
or 10^9. Each string is also asked with every node one level deeper
below a new root of a random value, and joined with the next tree's
string below such a root.

| | property |
|---|---|
| P1 | the statement read literally: written out, the tree gives back the string, and no node has a right child alone |
| P2 | the tree is the one the string was written from |
| P3 | one level deeper below a new root, the arm's tree is the new root's left subtree, and the root has no right one |
| P4 | the tree has as many nodes as the string has numbers, and one more level than the longest run of dashes |
| P5 | joined with the next string below a new root, the two trees are the new root's two subtrees, in order |
| P6 | each arm agrees with at least two of the other four |

The differential prints `588 trees: checksum 410630647, 17640 checks
over 5 arms: 0 failures` under `karac __mir-run` (14.7 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all fifteen
are killed, each fails the same checks under both, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one node too few popped | P1 574, P2 574, P4 512, P5 588, P6 574 |
| M2 | ★: the first child hung on the right | P1 586, P2 586, P3 588, P5 588, P6 586 |
| M3 | ★: each dash counted twice | P1 574, P2 574, P3 500, P4 555, P5 588, P6 574 |
| M4 | recursive: a right child sought a level too deep | P1 574, P2 574, P3 173, P4 538, P5 588, P6 574 |
| M5 | recursive: the string's last digit never read | P1 588, P2 588, P5 588, P6 588 |
| M6 | recursive: the first letter skipped | P1 588, P2 588, P3 588, P4 247, P5 588, P6 588 |
| M7 | split: every node pushed, not kept by depth | P1 522, P2 522, P4 475, P5 587, P6 522 |
| M8 | split: one-digit numbers taken for dashes | index out of bounds panic, exit 101 |
| M9 | split: a node kept in its parent's place | P1 546, P2 546, P3 509, P4 514, P5 588, P6 546 |
| M10 | slices: any deeper node taken for a child | P1 574, P2 574, P3 586, P4 510, P5 586, P6 574 |
| M11 | slices: the first child taken for the second | P1 586, P2 586, P3 588, P4 544, P5 588, P6 586 |
| M12 | slices: the first child skipped in the search | P1 574, P2 574, P4 567, P5 588, P6 574 |
| M13 | parents: the first node a level up taken | P1 522, P2 522, P4 431, P5 587, P6 522 |
| M14 | parents: the right child's place tested | P1 574, P2 574, P4 574, P5 588, P6 574 |
| M15 | parents: the second node never joined | P1 586, P2 586, P3 588, P4 586, P5 588, P6 586 |

P1, P2, P5 and P6 kill the fourteen that finish, P4 twelve and P3 eight;
M8 is killed by its own bounds check, a one-digit number counted as a
level and the node hung below a depth with no node yet. Many counts are
574 or 586: the 14 trees that are a single chain, each node the left
child of the one before, need no pop and no right child, so most edits
get them right, and the 2 trees of one node need no joining at all. P3
compares an arm with itself, a level deeper, so it passes the edits that
go wrong the same way at every depth (M1, M5, M7, M12, M13, M14) and
sees the ones that put the new root's only child on the right or lose
it (M2, M11, M15), or whose error depends on how deep a node is or where
it sits in the string (M3, M4, M6, M9, M10). P4 misses only M2 and M5, which
keep every node and every level and only put a child or a digit in the
wrong place. P5 fails almost every tree for every edit, since the
joined string holds two whole trees and is checked against the trees
themselves. The checks draw a random number for every tree whatever the
answers, so every mutant sees the same trees and their counts can be
compared.

Fifteen other edits were tried and set aside. Three change no answer,
because in a preorder string a node is at most one level deeper than
the node before it. Recursive ending a subtree only at a shorter run of
dashes, rather than at any different one: a subtree is only ever sought
where the next run is no longer than its depth, since a longer one would
have been read into the subtree before it. Slices not stopping its search at a
subtree's second child: the stretch holds no node one level below the
root after it. Parents taking the nearest shallower node rather than the
nearest one level up: that is the same node. The other twelve were
killed too, beyond three per arm. Nine fail exactly as a kept one: ★
putting a second child over the first, split taking the deepest node
seen for the parent, split testing the right child's place and parents
putting a second child over the first, as M14; ★ returning the last
node on the path, split starting the depth after a number at 0 and
parents returning the last node, as M15; and recursive reading the
right child first and slices building the halves the wrong way round, as
M2. ★ adding up the digits and recursive reading numbers in base 16 fail
alike, and slices dropping leaves fails on its own.

## Verification

Every arm prints the same output as `recover_tree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error; the differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program. `karac run` and a `karac build` binary print the
same output for every arm and the differential. The release build is
kara `56c60bdf7c`, with runtime archives rebuilt at `ce706dd131`, the
last commit before it to change the runtime. Under `karac __mir-run` the
arms take 5.9 s (★) to 29.7 s (recursive).

Two things turned up. The recursive arm takes 29.7 s under the
interpreter, against 5.9 to 8.1 s for the others. It calls
`traversal.bytes()` once per node, and the interpreter's `bytes()`
(`src/mir/interp.rs`) copies the whole string into a fresh snapshot on
every call, so each call costs the string's length; compiled code shows
no such cost. A probe reading one byte through `s.bytes()` per call on a
100,000-letter string takes 0.24 s with no calls, 3.56 s with 2,000 and
7.03 s with 4,000 under `karac __mir-run`, and 0.26 s with 2,000 under
`karac __mir-llvm-run`. That is kara `B-2026-10-29-38`. And writing the
split arm the Rust way, `piece.parse::<i64>()`, gets a diagnostic whose
fix-it removes the `::<i64>`, so `karac fix` leaves `piece.parse()`,
which is then refused because nothing gives it a type, with no fix-it,
though the type was there before the first fix took it out; that is kara
`B-2026-10-29-39`. The arm calls `i64.parse(piece)`, which the second
diagnostic names.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench writes 200 random trees of 1,000 nodes (LeetCode's largest)
out the statement's way once in all five languages, 3,950,178 letters
in all, then recovers each tree 50 times with the ★ arm, folding every
tree recovered into a checksum by a recursive walk. Each tree comes from
random values from 1 to 10^9 put one at a time into a binary search
tree, kept in arrays of indices, and a node with one child writes it as
its only child, which comes back on the left. The Rust version uses
`Rc<RefCell<TreeNode>>`, LeetCode's Rust node, C a `malloc` per node,
freed after each walk, and Go a pointer per child. Every implementation
prints `200 traversals of 1000 nodes, 3950178 letters, 50 rounds:
checksum 300230259`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.673 to 0.812 s | 0.756 s |
| Rust (`rustc -O`) | 0.646 to 0.807 s | 0.736 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.746 to 0.905 s | 0.797 s |
| Go | 0.689 to 0.759 s | 0.720 s |
| Python | 23.9 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.649 to 0.827 s | 0.702 s |
| Kāra (`karac build`) | 0.644 to 0.824 s | 0.749 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 0.88 times Rust's median time under overflow checks and 0.93
times C's. The five compiled programs' medians lie within 14% of each
other and their ranges overlap, so this bench does not tell them apart.
Every recovery allocates 1,000 nodes, reference-counted in Kāra and
Rust; we did not measure how much of each language's time that takes.
