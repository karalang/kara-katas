# 2508. Add Edges to Make Degrees of All Nodes Even

There is an **undirected** graph consisting of `n` nodes numbered from
`1` to `n`. You are given the integer `n` and a **2D** array `edges`
where `edges[i] = [ai, bi]` indicates that there is an edge between
nodes `ai` and `bi`. The graph can be disconnected.

You can add **at most** two additional edges (possibly none) to this
graph so that there are no repeated edges and no self-loops.

Return `true` *if it is possible to make the degree of each node in the
graph even, otherwise return* `false`*.*

The degree of a node is the number of edges connected to it.

```
n = 5, edges = [[1,2],[2,3],[3,4],[4,2],[1,4],[2,5]]  ->  true
n = 4, edges = [[1,2],[3,4]]                          ->  true
n = 4, edges = [[1,2],[1,3],[1,4]]                    ->  false
```

**Constraints:** `3 <= n <= 10^5`; `2 <= edges.length <= 10^5`;
`edges[i].length == 2`; `1 <= ai, bi <= n`; `ai != bi`; there are no
repeated edges.

An added edge flips the parity of its two ends, so two edges mend at
most four odd nodes. None needs nothing. Two, `a` and `b`, need the
edge `a-b` absent or, failing that, a third node joined to neither.
Four need one of their three pairings to be two absent edges. Any other
count is `false`. The approaches differ in how an edge's presence is
asked and how the cases are walked.

## Approaches

| file | mechanism |
|---|---|
| `even.kara` ★ | the edges in a `Set`, each as one number `min (n + 1) + max`; a `free` closure over it, and a `match` on the number of odd nodes. O(n + edges) |
| `even_adj.kara` | every node's neighbours in a `Set` of their own, a node's degree the size of its set, and an edge absent when one end's set lacks the other |
| `even_sorted.kara` | the same numbers in a sorted `Vec`, an edge's presence asked by `binary_search`. O(n log edges + edges log edges) |
| `even_rec.kara` | a recursion that mends the odd nodes with at most `budget` new edges: the first odd node joined to each other odd node it lacks and the rest mended with one edge fewer, or two left with two edges joined through a third node. At most two deep |
| `even_iter.kara` | iterators: the degrees `fold`ed from the edges, the edges `map`ped into a `Set` of pairs, the odd nodes `filter`ed; two odd nodes ask `any` third node, four `any` of their three pairings |
| `even_solution.kara` | LeetCode's Rust template: `n: i32` and `Vec<Vec<i32>>` in, `bool` out; the edges as pairs in a `HashSet`, a `has` closure over it, and a `match` on the number of odd nodes; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples and five
more; then 2000 random graphs of 3 to 8 nodes and 2000 of 3 to 30, with
1 to every possible edge, each as a count of those that can be mended
and a checksum; then the constraints' largest: a star and a path on
`10^5` nodes; 33000 nodes, 3 to `n` in a ring, 1 and 2 joined, and both
joined to every ring node, then the same with one ring node left alone;
and `10^5` random edges on `10^5` nodes. `even.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 3000
random graphs of 3 to 7 nodes against a search that adds every set of
none, one or two absent edges, and the two agreed on every graph.

The sorted arm was first written with `binary_search(..).is_ok()`.
`binary_search` gives an `Option` in Kāra, and `check` warns that
`is_ok()` on an `Option` is deprecated and means `is_some()`; `karac
fix` makes it `is_some()`.

`check` first reports 26 errors on the template, all Rust's spellings:
the `use std::collections::HashSet;` line, `struct Solution;`, two
`Vec<..>` in angle brackets, `HashSet::new`, the `&edges` borrow, the
`&` pattern of `|&v|`, the `&` on the argument of `contains`, nine `!`,
six `&&` and three `||`. `karac fix` carries it in one call, reporting
37 edits: the `use` line goes, since `Set` is in the prelude, and
`HashSet` becomes `Set`; `struct Solution {}`; the brackets; `vec![0; n
+ 1]` becomes `Vec.filled(n + 1, 0)`; the `usize` indices, casts and
closure parameters become `i64`; `for e in ref edges`; the `&` pattern
and the argument's `&` dropped; and `not`, `and` and `or`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: no edge added, every absent edge added alone, and every two
absent edges added together, each tried by counting every node's degree
afresh. No odd node is named. It checks 300 random graphs of 3 to 7
nodes with 1 to every possible edge; then 20 of 3 nodes; and 40 of 8
nodes. All 360 are drawn before any arm answers, and 255 of them can be
mended.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `true` only when 0, 2 or 4 nodes have an odd degree |
| P3 | every node `v` renumbered `n + 1 - v`: the same answer |
| P4 | the edges in the other order, each with its ends swapped: the same answer |
| P5 | a node `n + 1` with no edges added: `true` exactly when the answer was `true` or two nodes have an odd degree |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the new node is even and joined to nothing, so it
changes nothing for four odd nodes, and for two it is always a third
node joined to neither.

The differential prints `360 cases, 255 possible: checksum 859248925,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and tries the same added edges. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a pairing's second edge never asked | P1 9, P3 18, P6 9 |
| M4 | ★: the edges coded apart from their asking | P1 83, P3 29, P6 83 |
| M6 | ★: the even nodes taken as odd | P1 256, P2 12, P5 223, P6 256 |
| M7 | adj: neighbours kept one way | P1 199, P2 3, P3 47, P4 47, P5 120, P6 199 |
| M9 | adj: node n never a third | P1 8, P3 17, P5 34, P6 8 |
| M11 | adj: no odd node a failure | P1 41, P6 41 |
| M12 | sorted: the codes unsorted | P1 85, P3 6, P4 5, P6 85 |
| M13 | sorted: the edge a-b never asked | P1 46, P6 46 |
| M14 | sorted: only node n a third | P1 37, P3 41, P6 37 |
| M17 | rec: the budget unchecked | P1 8, P2 8, P6 8 |
| M18 | rec: a pairing paid nothing | P1 8, P3 6, P5 13, P6 8 |
| M21 | rec: the first odd node kept in | P1 111, P6 111 |
| M24 | iter: the pairs kept as given | P1 62, P3 39, P4 39, P6 62 |
| M25 | iter: two pairings only | P1 8, P6 8 |
| M26 | iter: any other count possible | P1 17, P2 17, P6 17 |
| M27 | solution: a present edge a-b taken as enough | P1 80, P6 80 |
| M31 | solution: node n never asked | P1 104, P3 125, P5 41, P6 104 |

P1 and P6 kill all seventeen, P3 nine, P5 five, P2 four, and P4 three,
the three edits that make an arm depend on the edges' order or their
ends' (M7, M12, M24).

Fourteen are not kept, and none survives. Two fail exactly as a kept
one: the ★ arm's absent edge `a-b` refused (M1) as the template's
present edge `a-b` taken as enough (M27), each the same `not` on the
edge between two odd nodes; and the rec arm's third node with one edge
left (M19) as its pairing paid nothing (M18), each mending four odd
nodes with three edges. Nine fail as one another, in three sets: the
★, iter and template arms' degrees counted at one end (M5, M22, M30);
the adj, rec, iter and template arms' third node asked of one end only
(M8, M20, M23, M28); and the adj and template arms' two pairings only
(M10, M29). Three fail in ways of their own, but their arms already
hold their kept edits: the ★ arm's one pairing of four only (M2), and
the sorted arm's first pairing's second edge never asked and six odd
nodes let in (M15, M16).

## Verification

Every arm prints the same output as `even.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.6 to 11.2 s and the differential 0.9 s; under `karac __mir-llvm-asan` the arms take 1.0 to 2.9 s and the differential 0.9 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds four graphs once: two of `10^5` nodes, each node
joined to the next in one and to the one two along in the other; and the
harness's two of 33000 nodes, whose odd nodes 1 and 2 are joined to
every ring node, and to all but one. It then makes 90 passes. Each pass,
for every graph, takes out the edge at place `check % edges` by moving
the last edge into its place, asks, and puts it back, folding 2 for
`true` or 1 for `false`, plus the pass, into the checksum. The bench
uses the ★ arm in all five languages, each holding the edges in a fresh
hash set on every ask: Kāra's `Set`, Rust's `HashSet`, Go's map,
Python's `set`, and in C an open-addressed table of `2^18` slots probed
linearly. Every implementation prints `90 passes over 4 graphs: checksum
686903765`.

BENCHTAB
