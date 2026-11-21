# 2421. Number of Good Paths

There is a tree (i.e. a connected, undirected graph with no cycles)
consisting of `n` nodes numbered from `0` to `n - 1` and exactly `n - 1`
edges.

You are given a **0-indexed** integer array `vals` of length `n` where
`vals[i]` denotes the value of the `i`th node. You are also given a 2D
integer array `edges` where `edges[i] = [ai, bi]` denotes that there
exists an **undirected** edge connecting nodes `ai` and `bi`.

A **good path** is a simple path that satisfies the following
conditions:

1. The starting node and the ending node have the **same** value.
2. All nodes between the starting node and the ending node have values
   **less than or equal to** the starting node (i.e. the starting node's
   value should be the maximum value along the path).

Return *the number of distinct good paths*.

Note that a path and its reverse are counted as the **same** path. For
example, `0 -> 1` is considered to be the same as `1 -> 0`. A single node
is also considered as a valid path.

```
vals = [1,3,2,1,3], edges = [[0,1],[0,2],[2,3],[2,4]]  ->  6
vals = [1,1,2,2,3], edges = [[0,1],[1,2],[2,3],[2,4]]  ->  7
vals = [1], edges = []                                 ->  1
```

**Constraints:** `n == vals.length`; `1 <= n <= 3 * 10^4`;
`0 <= vals[i] <= 10^5`; `edges.length == n - 1`; `edges` represents a
valid tree.

Taken in order of value, the nodes no larger than `v` form a forest, and
two nodes of value `v` are the ends of a good path exactly when they lie
in one of its trees. Union-find grows that forest one value at a time,
so each value's nodes need only be counted by the tree they fall in.

## Approaches

| file | mechanism |
|---|---|
| `paths.kara` ★ | union-find over the nodes in order of value, with path halving: each value's nodes joined to their neighbours no larger, then counted by root, `c` of them in one tree being `c (c - 1) / 2` paths of two ends, on top of the `n` one-node paths. O(n log n) |
| `paths_naive.kara` | from every node, a walk of the tree through the nodes no larger than it, counting the nodes of its own value reached with a larger index. O(n^2) |
| `paths_edges.kara` | edges in order of their larger end's value, union-find keeping each set's largest value and how many of its nodes hold it; two sets with the same largest value make a path for each pair of such nodes, one from each, and otherwise the larger keeps its count. O(n log n) |
| `paths_struct.kara` | a `UnionFind` struct, union by size with path halving, and the nodes grouped by value in a `SortedMap[i64, Vec[i64]]` walked from the smallest. O(n log n) |
| `paths_iter.kara` | iterators: the ★ arm's union-find, each value's run of nodes by `take_while`, the neighbours joined through `filter`, and the count by `fold` into a `Map` of roots, then `map` and `sum`. O(n log n) |
| `paths_solution.kara` | LeetCode's Rust template: a recursive `fn find` declared inside the method, `sort_by_key(\|&i\| vals[i])`, and each value's roots counted by `*cnt.entry(..).or_insert(0) += 1`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; a line of
five nodes of one value; a star whose centre is the largest; a line
rising to its middle and falling; the constraints' largest, random trees
of `3 * 10^4` nodes with values up to `10^5` and with values 1 to 3;
then 3000 random trees of 1 to 12 nodes with values 1 to 4, as a
checksum and the total. A random tree joins each node to one of those
before it, the two ends in either order, and shuffles the edges.
`paths.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 20000 random trees of up to 9 nodes against every
pair of nodes tested along its path.

`check` first reports 20 errors on the template, and `karac fix`
carries it in one call, reporting 42 edits: the
`use std::collections::HashMap;` line deleted, with `HashMap` written
`Map`; the brackets of every `Vec<..>` and `HashMap<..>`; `HashMap::new`
written `.`; `vec![vec![]; n]` written `Vec.filled(n, Vec.new())`;
`usize` written `i64` throughout; `&edges` and `&adj[u]` written as `ref`
borrows, and the `&` of the patterns `|&i|`, `for &v` and `for &c`
dropped; `&mut Vec<usize>` written `mut ref Vec[i64]` and each
`&mut parent` argument `mut parent`; `&&` written `and`; `struct
Solution;` given its braces; and the `fn find` declared inside the
method moved out to the top level, since Kāra has no nested items and
the function captures nothing. The wrapper's `as i64` on the method's
`i32` answer is dropped, since it widens without one. The recursion,
`sort_by_key`, `*cnt.entry(..).or_insert(0) += 1` and `as i32` stand as
Kāra.

The edges arm keeps each set's largest value in `top`, a copy of `vals`
declared `let mut`; `check` warns that it is never written, since a
root only ever absorbs a set no larger than itself, and `karac fix`
drops the `mut`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of nodes of one value, the tree's path between them
found by a walk from one end, and the pair counted when no node on it is
larger, plus the one-node paths. No union-find. It checks 300 random
trees of 1 to 10 nodes with values from 1 up to 1 to 4, then 30 of up to 120
nodes with values up to 20, then 30 of up to 120 with values 1 to 3. All
360 are drawn before any arm answers, and every tree's edges are
shuffled. The first version listed each node's edge to the node before
it in order of the node, which hid one mutant: with the edges in that
order, the edges arm never joins two sets that each hold two nodes of
their largest value, so the count of pairs across them cannot go wrong.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least `n` and at most `n` plus, for each value, the pairs of its nodes |
| P3 | the nodes renamed, `i` as `n - 1 - i`: the same answer |
| P4 | every value `v` made `2 v + 3`: the same answer |
| P5 | a leaf of the largest value hung on a node of the largest value: the answer plus 1 and plus the count of the largest value |
| P6 | each arm agrees with at least three of the other five |

P3 holds because renaming keeps the tree and every path, P4 because
`2 v + 3` keeps every comparison. P5 holds because no node is larger
than the new leaf, so it ends a good path with itself and with every
node of the largest value, and its own paths are the only new ones.

The differential prints `360 cases: checksum 478331890, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks the path of every pair. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: only smaller neighbours joined | P1 281, P5 360, P6 281 |
| M4 | ★: each pair counted twice | P1 294, P2 210, P5 360, P6 294 |
| M6 | ★: the nodes never sorted | P1 181, P3 132, P5 211, P6 181 |
| M7 | naive: a node one larger walked through | P1 137, P4 137, P6 137 |
| M9 | naive: the walk only downhill | P1 145, P5 128, P6 145 |
| M10 | naive: every node reached counted | P1 219, P2 194, P3 223, P6 219 |
| M12 | edges: edges taken by the smaller end | P1 138, P6 138 |
| M13 | edges: the pairs counted as the larger count | P1 93, P6 93 |
| M15 | edges: the smaller-valued set kept as root | P1 153, P5 191, P6 153 |
| M18 | struct: the one-node paths left out | P1 360, P2 215, P5 360, P6 360 |
| M20 | struct: every group counted under its first root | P1 165, P6 165 |
| M21 | struct: only the first neighbour read | P1 176, P5 158, P6 176 |
| M22 | iter: the run taken past its value | P1 202, P2 87, P4 202, P5 155, P6 202 |
| M23 | iter: larger neighbours joined | P1 144, P6 144 |
| M24 | iter: the fold never counting past one | P1 294, P5 360, P6 294 |
| M30 | solution: only the first node of each value joined | P1 236, P3 168, P5 257, P6 236 |
| M31 | solution: the values sorted from the largest | P1 172, P5 77, P6 172 |


P1 and P6 kill all seventeen, P5 eleven, P2 four, P3 three and P4 two.

Fourteen are not kept. Ten fail exactly as a kept one: a larger
neighbour joined in the ★, struct and template arms (M1, M17, M28) as
the iter arm's (M23); the ★ arm's one-node paths left out and the
template's answer without them (M3, M27) as the struct arm's (M18); the
★ arm's each node counted as its own set, the struct arm's union that
never joins and the iter arm's node joined to itself (M5, M19, M26) as
the iter arm's fold never counting past one (M24), since each leaves
every value's nodes in sets of one; the naive arm's pair counted from
both ends (M8) as the ★ arm's pair counted twice (M4); and the edges
arm's edges never sorted (M16) as its edges taken by the smaller end
(M12). Four fail apart from every kept one and were left out because
those arms keep their share already: the naive arm's only the first
neighbour walked (M11), the edges arm's counts never added (M14), the
iter arm's pairs counted as half the square (M25) and the template's
each count one more (M29).

## Verification

Every arm prints the same output as `paths.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 3.2 s, but for the naive
arm: it walks the tree from every node, and on the two trees of
`3 * 10^4` nodes, the second with values 1 to 3, where most walks cross
most of the tree, that is about `10^9` steps. It takes 914 s under
`karac __mir-run`, 80 s under `karac __mir-llvm-asan` and 14 s under
`karac run`. The differential takes 3.1 s under `karac __mir-run`,
1.3 s under `karac __mir-llvm-asan` and 1.0 s under `karac run`.

## Benchmarks

The bench builds 10 random trees of `3 * 10^4` nodes once from its own
generator, tree `i` with values from 1 to `3 + 1000 i`, so the first has
long runs of equal values and the last few. It then makes 20 passes,
answering every tree and folding the answer plus the pass into the
checksum. The bench uses the ★ arm, union-find over the nodes in order
of value, in all five languages. Every implementation prints `20 passes
over 10 trees of 3 * 10^4 nodes: checksum 85836190`. Each builds its
adjacency, order and union-find afresh for every tree; Kāra, Rust, Go
and Python keep the adjacency as a list of lists and count each value's
roots in a hash map (`Map`, `HashMap`, `map`, `dict`), while C keeps the
adjacency in two flat arrays and counts the roots in an array indexed
by root, cleared after each value. Every order is a stable sort by
value.

BENCHTAB
