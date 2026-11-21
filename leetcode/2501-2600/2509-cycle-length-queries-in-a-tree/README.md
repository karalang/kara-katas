# 2509. Cycle Length Queries in a Tree

You are given an integer `n`. There is a **complete binary tree** with
`2^n - 1` nodes. The root of that tree is the node with the value `1`,
and every node with a value `val` in the range `[1, 2^(n - 1) - 1]` has
two children where:

- The left node has the value `2 * val`, and
- The right node has the value `2 * val + 1`.

You are also given a 2D integer array `queries` of length `m`, where
`queries[i] = [ai, bi]`. For each query, solve the following problem:

1. Add an edge between the nodes with values `ai` and `bi`.
2. Find the length of the cycle in the graph.
3. Remove the added edge between nodes with values `ai` and `bi`.

**Note** that:

- A **cycle** is a path that starts and ends at the same node, and each
  edge in the path is visited only once.
- The length of a cycle is the number of edges visited in the cycle.
- There could be multiple edges between two nodes in the tree after
  adding the edge of the query.

Return *an array* `answer` *of length* `m` *where* `answer[i]` *is the
answer to the* `i`*th query.*

```
n = 3, queries = [[5,3],[4,7],[2,3]]  ->  [4,5,3]
n = 2, queries = [[1,2]]              ->  [2]
```

**Constraints:** `2 <= n <= 30`; `m == queries.length`; `1 <= m <=
10^5`; `queries[i].length == 2`; `1 <= ai, bi <= 2^n - 1`; `ai != bi`.

The added edge closes the one cycle made of itself and the tree path
from `a` to `b`, so the answer is that path's length plus 1. The parent
of `v` is `v / 2`, and a node is never above a smaller one, so the path
meets at the lowest common ancestor. The approaches differ in how the
two ends are brought to it.

## Approaches

| file | mechanism |
|---|---|
| `cycle.kara` ★ | the larger node halved until the two meet, each halving one edge. O(n) a query |
| `cycle_bits.kara` | a node's depth its bit length less one: the deeper node lifted by one shift, then the place of the highest bit where the two differ is how far each still climbs, from `leading_zeros`. O(1) a query |
| `cycle_path.kara` | every ancestor of `a` kept in a `Map` with its distance from `a`, and `b` climbing until it reaches one |
| `cycle_rec.kara` | a recursion: the distance is 0 when the two are one node, else one more than the distance from the larger's parent to the other. At most 58 deep |
| `cycle_iter.kara` | iterators: each node's path from the root, its shifts `take_while` they are above 0, `collect`ed and reversed; the two paths `zip`ped and the shared start `count`ed |
| `cycle_solution.kara` | LeetCode's Rust template: `n: i32` and `Vec<Vec<i32>>` in, `Vec<i32>` out; each query `map`ped to a walk that shifts the larger node right until the two meet; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and four
more, among them the two edge leaves of 30 levels; then 2000 random
trees of 2 to 30 levels and 2000 of 2 to 6, with 1 to 20 queries, each
as the sum of the answers and a checksum; then the constraints' largest,
30 levels with `10^5` queries: random; between leaves at the two edges;
and from the root to every depth in turn. `cycle.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 3000
random trees of 2 to 7 levels with 1 to 10 queries against a
breadth-first search over the tree's edges, and the two agreed on every
query.

`check` first reports 5 errors on the template: `struct Solution;`, the
three `Vec<..>` in angle brackets, and the `mut a` and `mut b` inside
`let (mut a, mut b)`. `karac fix` carries it in one call, reporting 9
edits: `struct Solution {}`; the brackets; and `let mut (a, b)`, since
in Kāra `mut` goes before the whole pattern. The `i32` walk, the `>>=
1`, and the wrapper's `as i64` on each answer stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each query, the whole tree of `2^n - 1` nodes built as
neighbour lists, the edge `a-b` added, and every node of one neighbour
peeled away until none is left; the nodes that stay are the cycle. No
parent is halved and no path is walked. It checks 300 random trees of 2
to 7 levels with 1 to 8 queries; then 20 of 2 levels; and 40 of 10
levels with 10 queries. All 360 are drawn before any arm answers, and
they ask 1941 queries.

| | property |
|---|---|
| P1 | every answer is the statement read literally |
| P2 | an answer for every query, each from 2 to `2 n - 1` |
| P3 | every query's ends swapped: the same answers |
| P4 | the queries in the other order: the answers in the other order |
| P5 | one level more, and every node `v` of depth `d` written `v + 2^d`: the same answers |
| P6 | each arm agrees with at least three of the other five |

P5 holds because `v + 2^d` puts a 0 under `v`'s leading 1, which is
`v`'s place in the root's left subtree, a copy of the whole tree one
level down, so every path keeps its length.

The differential prints `360 cases, 1941 queries: checksum 43308211,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and runs a breadth-first search from
`a` for each. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: each step counted twice | P1 360, P2 327, P6 360 |
| M5 | ★: the smaller stepped down by one | P1 340, P2 224, P3 357, P5 339, P6 340 |
| M6 | ★: the first query only | P1 325, P2 325, P4 256, P6 325 |
| M8 | bits: the deeper lifted one too far | P1 286, P2 211, P3 347, P5 286, P6 286 |
| M9 | bits: one end's climb only | P1 336, P6 336 |
| M11 | bits: the lift left out | P1 347, P2 226, P6 347 |
| M12 | path: a's steps counted twice | P1 352, P2 310, P3 347, P6 352 |
| M13 | path: b's climbs counted twice | P1 353, P2 307, P3 347, P6 353 |
| M14 | path: the new edge counted twice | P1 360, P2 220, P6 360 |
| M18 | rec: the larger's climb uncounted | P1 352, P2 144, P3 347, P6 352 |
| M20 | rec: asked from b's parent | P1 360, P2 115, P3 226, P6 360 |
| M21 | rec: both halved together | P1 343, P2 40, P3 360, P5 337, P6 343 |
| M23 | iter: the shared start counted once | P1 360, P2 220, P5 360, P6 360 |
| M25 | iter: a's path counted twice | P1 347, P2 177, P3 347, P6 347 |
| M26 | iter: eight shifts only | P1 40, P5 39, P6 40 |
| M30 | solution: the first query skipped | P1 360, P2 360, P4 315, P6 360 |
| M31 | solution: b taken as its odd sibling | P1 132, P2 66, P3 203, P5 106, P6 132 |

P1 and P6 kill all seventeen, P2 fifteen, P3 nine, P5 six, and P4 two,
the two edits that drop a query (M6, M30).

One of the first thirty-one edits was replaced. The path arm's `a`
itself never kept, its climb begun at `a`'s parent, leaves the `Map`
empty when `a` is the root, since the root's parent is 0; `b` then
climbs to 0 and stays there, never finding an ancestor, and the run
never ends. It became `a`'s distances one short (M15).

Fourteen are not kept, and none survives. Three fail exactly as a kept
one: the path arm's every distance kept as 0 (M16) as the rec arm's
larger's climb uncounted (M18); the rec arm's meeting worth 1 (M17) as
the path arm's new edge counted twice (M14), each answer one more; and
the rec arm's smaller's climb counted twice (M19) as the path arm's
`b`'s climbs counted twice (M13). Eight fail as one another, in three
sets: the ★ and template arms' length begun at 0 and the path arm's
distances one short (M1, M27, M15), each answer one less; the ★ arm's
larger quartered and the template's larger shifted by two (M3, M28);
and the bits arm's shared bits by `and`, and the iter arm's paths left
leaf first and differing start counted (M10, M22, M24), each answer the
cycle through a node above the root. Three fail in ways of their own,
but their arms already hold their kept edits: the ★ arm's stop at a
shared parent (M4), the bits arm's bit length one short (M7), and the
template's walk in which only `a` climbs (M29).

## Verification

Every arm prints the same output as `cycle.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.9 to 10.4 s, but for the iter arm, which collects two paths for every query and takes 33.5 s, and the differential 3.0 s; under `karac __mir-llvm-asan` the arms take 0.7 to 2.6 s, the iter arm 11.7 s, and the differential 1.4 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds `10^5` random queries on the tree of 30 levels once
from its own generator, then makes 34 passes. Each pass sets the second
node of the query at place `check % 10^5` to `(check + p) % (2^30 - 1)
+ 1`, or the node after it when that is the first, asks every query,
and puts the node back, folding each answer plus the pass into the
checksum. The bench uses the ★ arm in all five languages. Every
implementation prints `34 passes over 10^5 queries on 30 levels:
checksum 236032332`.

BENCHTAB
