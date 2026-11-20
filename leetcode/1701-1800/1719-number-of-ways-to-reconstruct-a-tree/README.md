# 1719. Number Of Ways To Reconstruct A Tree

You are given an array `pairs`, where `pairs[i] = [xi, yi]`, and:

- There are no duplicates.
- `xi < yi`

Let `ways` be the number of rooted trees that satisfy the following
conditions:

- The tree consists of nodes whose values appeared in `pairs`.
- A pair `[xi, yi]` exists in `pairs` **if and only if** `xi` is an
  ancestor of `yi` or `yi` is an ancestor of `xi`.
- **Note:** the tree does not have to be a binary tree.

Two ways are considered to be different if there is at least one node
that has different parents in both ways.

Return:

- `0` if `ways == 0`
- `1` if `ways == 1`
- `2` if `ways > 1`

A **rooted tree** is a tree that has a single root node, and all edges
are oriented to be outgoing from the root.

An **ancestor** of a node is any node on the path from the root to that
node (excluding the node itself). The root has no ancestors.

```
pairs = [[1,2],[2,3]]                    ->  1
pairs = [[1,2],[2,3],[1,3]]              ->  2
pairs = [[1,2],[2,3],[2,4],[1,5]]        ->  0
```

**Constraints:** `1 <= pairs.length <= 10^5`;
`1 <= xi < yi <= 500`; the elements in `pairs` are unique.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | a node's pairs are its ancestors and descendants, so an ancestor has at least as many as any node below it, and the root is paired with every node. Taken by degree, most first, a node's parent is its earlier neighbour with the fewest pairs, and every other neighbour of the node must be the parent's too, or no tree fits; a parent with as many pairs as its child could swap with it, so more than one tree does. The pairs as a 501 by 501 matrix of `bool`. O(n^2), n the nodes |
| `ways_sets.kara` | the same rule read from a `Map` of `Set`s: each node's parent the neighbour with the fewest pairs among those with at least as many as it has, and the subset test a `contains` for each neighbour. No sort |
| `ways_bits.kara` | the same rule with each node's neighbours as the bits of eight `u64` words: a degree is the sum of `count_ones()`, and the subset test is `mine & ~(theirs \| the parent's own bit)` being zero in every word. O(n^2 / 64) for the tests |
| `ways_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i32, HashSet<i32>>` built with `entry().or_default()`, the nodes sorted by `sort_by` on their set sizes, and `usize::MAX` as the first fewest, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one pair
(either node may be the root) and a star whose centre is the only root;
then the answers summed and a checksum for 3000 random problems over up
to 6 nodes, 300 over up to 50 and 10 over up to 500, all labels from 1
to 500, half of them the ancestor pairs of a random tree, kept, with one
pair dropped, or with one added, and half random pairs. `ways.py`
mirrors the ★ arm and its output is byte-identical.

```
1
2
0
2
1
3000 problems of up to 6 nodes: answers sum to 4215, checksum 856836697
300 problems of up to 50 nodes: answers sum to 214, checksum 834781237
10 problems of up to 500 nodes: answers sum to 6, checksum 157025538
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every rooted tree on the nodes, each a root and a parent for
every other node among the rest, kept when it has no cycle and its pairs
of an ancestor and a descendant are exactly the pairs given; the count,
2 for more than one. It checks 3000 random problems over 2 to 5 nodes
labelled from 1 to 9, drawn as the arms' are. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every label v written 501 - v gives the same answer |
| P3 | the pairs listed in reverse give the same answer |
| P4 | when some tree fits, a new node paired with every node makes two: it and the old root can swap |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 577095567, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every parent array from
`itertools.product` whose ancestor pairs are the pairs given, gives the
same checksum. On a failure it prints the first ten and then the count
by property. Under `karac __mir-run` it takes about three and a half
minutes: the ★ arm fills its 501 by 501 matrix for each of the 12000
answers.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first edits were equivalent and
were replaced: an M1 that let the root have one pair fewer than every
other node, which the check of each node's pairs against its parent's
then refuses anyway, and an M5 that skipped that check for a neighbour
with one pair: once a root is linked to every node, that one pair is
the root's, and the check never runs for the root. M2, M4 and M8 each pick a parent that is an ancestor but not the
nearest, and fail the very same checks, as do M6 and M9.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the nodes sorted by fewest pairs first | P1 1291, P5 1291 |
| M2 | ★: the parent the first linked node in the order, not the last | P1 492, P5 492 |
| M3 | ★: two ways when the parent has one pair more, not as many | P1 1976, P4 1576, P5 1976 |
| M4 | sets: a parent must have more pairs, not at least as many | P1 492, P5 492 |
| M5 | sets: a node one pair short of a root skipped as one | P1 359, P5 359 |
| M6 | sets: two ways only for three or more roots | P1 1152, P4 618, P5 1152 |
| M7 | bits: the parent's own bit left out of what the child may hold | P1 1291, P5 1291 |
| M8 | bits: the parent the neighbour with the most pairs, not the fewest | P1 492, P5 492 |
| M9 | solution: the second node in the order skipped | P1 1152, P4 618, P5 1152 |
| M10 | solution: a tie with the parent ignored for a leaf | P1 1010, P5 1010 |

## Benchmarks

The bench draws 50 random problems over all 500 nodes, each the
ancestor pairs of a random tree, half its parents picked anywhere above
and half a few places above so some trees run deep, one in three with a
pair dropped and one in three with one added, 228608 pairs in all,
then answers each 50 times by the ★ arm in all five languages. Every
implementation prints `50 problems of 500 nodes, 228608 pairs, 50
rounds: answers sum to 2900, checksum 835453341`. Each answer fills a
fresh 501 by 501 matrix. Python sorts with a stable `sort`, Go with
`sort.SliceStable`, and C's `qsort` breaks ties by node, so every
implementation takes the nodes in the same order. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.506 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.512 s |
| Rust (`rustc -O`) | 0.523 s |
| Kāra (`karac build`) | 0.530 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.535 s |
| Go | 0.910 s |
| Python | 18 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.506 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.555 s and 0.571 s on one
run).

## Verification

All four arms print the same output as `ways.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and sets arms checked clean as first written. The bits arm first
summed its degrees as `w.count_ones() as i64`, as Rust's `u32` count
needs; in Kāra `count_ones()` already gives an `i64`
(docs/library/core-types.md), so the cast was redundant, `karac check`
said so, and `karac fix` dropped it.

LeetCode's Rust template took one `karac fix` of 36 edits:
`struct Solution {}` added, `use std::collections::{HashMap, HashSet};`
deleted, `HashMap<i32, HashSet<i32>>` and `HashMap::new()` written
`Map[i32, Set[i32]]` and `Map.new()`, `Vec<i32>` written `Vec[i32]`,
`for p in &pairs` written `for p in ref pairs`, `.or_default()` written
`.or_insert(Set.new())`, every `&` on an index or argument dropped
(`adj[&b]`, `cmp(&adj[a].len())`, `contains(&nb)`), `for &node in
&nodes[1..]` written `for node in nodes[1..]`, `for &nb in &adj[&node]`
written `for nb in ref adj[node]`, `usize::MAX` written `i64.MAX`, and
`&&` and `!` written `and` and `not`. `adj.keys().cloned().collect()`
and `sort_by(|a, b| ...cmp(...))` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
