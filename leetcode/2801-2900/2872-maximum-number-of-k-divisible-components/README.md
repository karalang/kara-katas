# 2872. Maximum Number of K-Divisible Components

There is an undirected tree with `n` nodes labeled from `0` to `n - 1`.
You are given the integer `n` and a 2D integer array `edges` of length
`n - 1`, where `edges[i] = [ai, bi]` indicates that there is an edge
between nodes `ai` and `bi` in the tree.

You are also given a **0-indexed** integer array `values` of length `n`,
where `values[i]` is the **value** associated with the `i`th node, and
an integer `k`.

A **valid split** of the tree is obtained by removing any set of edges,
possibly empty, from the tree, such that the resulting components all
have values that are divisible by `k`, where the **value of a connected
component** is the sum of the values of its nodes.

Return *the **maximum number of components** in any valid split*.

```
n = 5, edges = [[0,2],[1,2],[1,3],[2,4]], values = [1,8,1,4,4], k = 6                ->  2
n = 7, edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [3,0,6,1,5,2,1], k = 3  ->  3
```

**Constraints:** `1 <= n <= 3 * 10^4`; `edges.length == n - 1`;
`edges[i].length == 2`; `0 <= ai, bi < n`; `values.length == n`; `0 <=
values[i] <= 10^9`; `1 <= k <= 10^9`; the sum of `values` is divisible
by `k`; the input is generated such that `edges` represents a valid
tree.

## Approaches

| file | mechanism |
|---|---|
| `components.kara` ★ | the whole tree's sum divides by k, so an edge can be cut exactly when the part below it divides by k, and every such edge can be cut at once; the answer is the subtrees, rooted at 0, whose sums divide by k, taken mod k children before parents in reverse breadth-first order |
| `components_dfs.kara` | the same count by depth-first recursion, each call returning its subtree's sum mod k and counting the subtree when that is 0; it recurses 3 * 10^4 deep on the harness's path |
| `components_leaves.kara` | leaves peeled off with no root: each node keeps its degree and the XOR of its neighbours' labels, so a leaf's one neighbour left is that XOR; a leaf whose sum divides by k is a component, else its sum goes to the neighbour, and the last node standing closes the last component |
| `components_tour.kara` | an Euler tour: a preorder walk with an explicit stack gives each node the stretch of places its subtree fills, and a prefix sum of the values in tour order gives every subtree's sum as a difference, tested mod k |
| `components_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `vec![vec![]; n]` adjacency list and a nested `fn dfs` taking `&Vec<Vec<usize>>` and `ans: &mut i32`, its root's parent `usize::MAX`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 3 * 10^4
nodes, LeetCode's most, as a path of values k and a star of zeros; then
3000 random trees of 1 to 10 nodes, values 0 to 9 and k 1 to 5, and 30
of 10^3 to 3 * 10^4, values up to 10^9, every other one with k up to 10
and deep, each node's parent among the five before it, the first value
raised so the sum divides by k, as a total of components and a
checksum. `components.py` mirrors the ★ arm and its output is
byte-identical.

```
2 3
30000 30000
3000 small trees: 9489 components, checksum 228901168
30 large trees: 41593 components, checksum 874619415
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of edges to cut tried, as a bit mask, the
parts left found by flood fill, and the most parts kept whose sums all
divide by k. It draws 2000 random trees of 1 to 10 nodes, then 50 of up
to 3000, drawn as the harness draws them, all before any arm answers;
the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 nodes, the answer is the literal reading's |
| P2 | up to 10 nodes, every value times k: n |
| P3 | a leaf of value 0 added to node 0: one more |
| P4 | every label v made n - 1 - v: the same answer |
| P5 | from 1 to n, and n with k made 1 |
| P6 | each arm agrees with at least three of the other four |

P2 is asked only of the small trees: values times k up to 10^9 pass
`i32`, which the solution arm takes its values in, as LeetCode's
signature does.

The differential prints `2050 cases, 15861 components: checksum
33186371, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. A first draft of M6 crashed with an index out
of bounds before any property was asked, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a part counted whose sum was not 0 | P1 807, P4 400, P6 832 |
| M2 | ★: a part's sum handed up one too many | P1 1023, P4 383, P5 307, P6 1073 |
| M3 | dfs: the node's own value left out | P1 1332, P6 1382 |
| M4 | dfs: the sum not taken mod k on the way up | P1 1332, P4 463, P5 512, P6 1382 |
| M5 | leaves: the last node not counted | P1 2000, P2 2000, P5 2050, P6 2050 |
| M6 | leaves: a leaf's remainder handed on in place of its neighbour's | P1 712, P3 124, P4 601, P6 737 |
| M7 | tour: a subtree one place short | P1 994, P4 806, P6 1044 |
| M8 | tour: sizes not handed up | P1 793, P4 755, P5 198, P6 842 |
| M9 | solution: a subtree summing to 0 not counted | P1 657, P2 805, P3 2050, P5 805, P6 657 |
| M10 | solution: a node's own value left out | P1 1332, P6 1382 |

## Benchmarks

The bench draws 30 trees of 3 * 10^4 nodes, LeetCode's most, values up
to 10^9 and k from 2 to 10, every other one deep, all of them first,
then answers each 20 times by the ★ arm in all five languages; C keeps
the adjacency in one array indexed by offsets, counted first, and every
implementation builds it on each call. Every implementation prints `30
trees of 30000, 20 rounds: 3737940 components, checksum 154557813`.

BENCHTAB

## Verification

All five arms print the same output as `components.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, the dfs arm's
recursion 3 * 10^4 deep included, under every lane.

LeetCode's Rust template took 46 `karac fix` edits in one run, the
wrapper included: the nested `fn dfs` moved out to the top level, as
Kāra has no nested functions, its `&Vec<Vec<usize>>` becoming `ref
Vec[Vec[i64]]` and `ans: &mut i32` `ans: mut ref i32`, with
`dfs(v, u, g, values, k, ans)` passing `mut ans`; `usize::MAX` became
`i64.MAX`; `struct Solution {}` was added for the `impl`; `Vec<..>`
became `Vec[..]` and every `usize` `i64`; `vec![vec![]; n]` became
`Vec.filled(n, Vec.new())`; `for e in &edges` and `for &v in &g[u]`
became `ref` loops; `&g, &values` were passed bare and `&mut ans` as
`mut ans`; `k as i64` lost its cast, and so did the wrapper's `as i64`,
both `i32` widenings; `|&x|` lost its `&`, and `Solution::` took `.`.
`values[u] as i64` and `s % k` were accepted as written.
