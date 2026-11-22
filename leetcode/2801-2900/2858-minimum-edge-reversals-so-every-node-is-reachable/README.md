# 2858. Minimum Edge Reversals So Every Node Is Reachable

There is a **simple directed graph** with `n` nodes labeled from `0` to
`n - 1`. The graph would form a **tree** if its edges were
bi-directional.

You are given an integer `n` and a **2D** integer array `edges`, where
`edges[i] = [ui, vi]` represents a **directed edge** going from node
`ui` to node `vi`.

An **edge reversal** changes the direction of an edge, i.e., a directed
edge going from node `ui` to node `vi` becomes a directed edge going
from node `vi` to node `ui`.

For every node `i` in the range `[0, n - 1]`, your task is to
**independently** calculate the **minimum** number of **edge
reversals** required so it is possible to reach any other node starting
from node `i` through a **sequence** of **directed edges**.

Return *an integer array* `answer`*, where* `answer[i]` *is the*
***minimum*** *number of* ***edge reversals*** *required so it is
possible to reach any other node starting from node* `i` *through a*
***sequence*** *of* ***directed edges****.*

```
n = 4, edges = [[2,0],[2,1],[1,3]]  ->  [1,1,0,2]
n = 3, edges = [[1,2],[2,0]]        ->  [2,0,1]
```

**Constraints:** `2 <= n <= 10^5`; `edges.length == n - 1`;
`edges[i].length == 2`; `0 <= ui == edges[i][0] < n`; `0 <= vi ==
edges[i][1] < n`; `ui != vi`; the input is generated such that if the
edges were bi-directional, the graph would be a tree.

## Approaches

| file | mechanism |
|---|---|
| `reversals.kara` ★ | rerooting: from node 0 the reversals are the edges pointing back toward it, counted down a walk of an explicit stack; moving the root across an edge from p to c costs one more if the edge points from p to c and one less if it points from c to p, applied in the walk's order |
| `reversals_path.kara` | signed paths: a breadth-first walk from node 0 gives every node a depth, which tells each edge's nearer end; a node's answer is node 0's plus the edges on its path pointing away from 0 less those pointing toward it, carried down in order of depth by `sort_by_key` |
| `reversals_euler.kara` | an Euler tour from node 0 gives each subtree one range of entry times; an edge pointing down into c's subtree costs every root inside that range one reversal, one pointing up costs every root outside it, each added to a difference array over the tour, and a running sum reads the answers off |
| `reversals_recursive.kara` | rerooting by recursion: a call down the tree returns the edges in each subtree that point back toward its top, and a second carries the answer down, passing the answer vector as `mut ref Vec[i64]` |
| `reversals_solution.kara` | a Rust solution as LeetCode's Rust users write it: `vec![vec![]; n]` of `(usize, i32)`, two `fn`s nested in the method, a `dfs` and a `reroot` taking `&mut Vec<i32>`, and `usize::MAX` for the root's missing parent, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; a path of
10^5 nodes, LeetCode's most, every edge pointing on, the same path
pointing each way in turn, and a star of 10^5 with every edge pointing
in, each as the sum of the answers and a checksum over them; then 3000
random trees of 2 to 9 nodes, and 20 of 10^4 to 10^5, every other one
deep (each node hung off one of the three before it), with the labels
shuffled and each edge pointing either way. `reversals.py` mirrors the
★ arm and its output is byte-identical.

```
[1, 1, 0, 2] [2, 0, 1]
path 4999950000 282060600, turns 4999950000 132603394, star 9999800001 91451687
3000 small trees: answers sum to 45217, checksum 123941366
20 large trees: answers sum to 37251917640, checksum 642938269
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: for a tree of up to 8 nodes, every set of edges to
reverse tried, from each node a walk along the edges as they then
point, and the fewest reversals that reach every node; for a larger
one, from each node a walk of the tree counting the edges it meets
pointing the wrong way. It draws 2000 random trees of 2 to 8 nodes,
then 50 of 10 to 300, every other one deep, all before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every edge reversed: n - 1 less each answer |
| P3 | the nodes relabelled: each answer moves with its node |
| P4 | the edges listed the other way round: the same answer |
| P5 | across every edge u -> v, v's answer is one more than u's |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 369065181, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, by the walk from each node, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: node 0's count taken from the edges pointing to it | P1 1689, P3 1300, P6 1689 |
| M2 | ★: the root moved the wrong way across every edge | P1 2050, P3 1300, P5 2050, P6 2050 |
| M3 | path: an edge pointing toward 0 left out of node 0's count | P1 1801, P2 2050, P3 1300, P6 1801 |
| M4 | path: an edge pointing back costing nothing | P1 1801, P2 2050, P3 1564, P5 1801, P6 1801 |
| M5 | euler: a node's leaving time taken before its children | P1 1650, P3 1430, P5 1650, P6 1650 |
| M6 | euler: an upward edge charged inside the subtree, not outside | P1 1801, P2 2050, P3 1564, P5 1801, P6 1801 |
| M7 | recursive: a subtree's own back edges not counted | P1 1801, P2 2050, P3 1300, P6 1801 |
| M8 | recursive: the answer carried down unchanged | P1 2050, P3 1300, P5 2050, P6 2050 |
| M9 | solution: both directions entered as along | P1 1801, P2 2050, P3 1564, P5 1801, P6 1801 |
| M10 | solution: every edge read the other way round | P1 2050, P5 2050, P6 2050 |

## Benchmarks

The bench draws 20 random trees of 10^5 nodes, LeetCode's most, every
other one deep, labels shuffled and each edge pointing either way, all
of them first, then answers each 5 times by the ★ arm in all five
languages. Kāra, Rust, Go and Python build a vector of neighbours per
node on every call; C builds one array of neighbours indexed by
offsets. Every implementation prints `20 trees of 100000, 5 rounds:
answers sum to 500308662915, checksum 790646939`.

BENCHTAB

## Verification

All five arms print the same output as `reversals.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential
first read each arm's answer as `let value = got[arm]`, and `karac
check` reported `E_INDEX_MOVE_NON_COPY`, a `Vec[i64]` moved out of an
index; `karac fix` borrowed it as `ref got[arm]`. The literal
reading's `flips.count_ones() as i64` drew `redundant_cast`, the count
being an `i64` already, and `karac fix` took the cast out.

LeetCode's Rust template took 62 `karac fix` edits in one run, the
wrapper included. The two nested `fn`s were moved to the top level, as
Kāra has no nested items and they capture nothing; `&Vec<..>` became
`ref Vec[..]` and `&mut Vec<i32>` became `mut ref Vec[i32]`, with
`&mut ans` passed as `mut ans`; `usize` became `i64` throughout and
`usize::MAX` became `i64.MAX`; `vec![vec![]; n]` and `vec![0; n]`
became `Vec.filled(n, Vec.new())` and `Vec.filled(n, 0)`; `for &(v, w)
in &g[u]` became `for (v, w) in ref g[u]`; `let mut s = 0` took `:
i32`; `struct Solution {}` was added for the `impl`, and `Solution::`
took `.`.
