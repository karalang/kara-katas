# 2374. Node With Highest Edge Score

You are given a directed graph with `n` nodes labeled from `0` to
`n - 1`, where each node has **exactly one** outgoing edge.

The graph is represented by a given **0-indexed** integer array `edges`
of length `n`, where `edges[i]` indicates that there is a **directed**
edge from node `i` to node `edges[i]`.

The **edge score** of a node `i` is defined as the sum of the
**labels** of all the nodes that have an edge pointing to `i`.

Return *the node with the highest **edge score***. If multiple nodes
have the same **edge score**, return the node with the **smallest**
index.

```
edges = [1,0,0,0,0,7,7,5]  ->  7
edges = [2,0,0,2]          ->  0
```

**Constraints:** `n == edges.length`; `2 <= n <= 10^5`;
`0 <= edges[i] < n`; `edges[i] != i`.

Each node adds its label to one score, so one pass over the edges gives
every score, and one more finds the first of the highest. `10^5` nodes
all pointing at node 0 give it a score of `4999950000`, past `i32`,
which is why the scores are kept in `i64`.

## Approaches

| file | mechanism |
|---|---|
| `edge.kara` ★ | the scores in a vector, then the first node of the highest score by a strict comparison. O(n) |
| `edge_sort.kara` | the pairs (target, source) sorted, each run of a target summed, and the first run of the highest sum kept. O(n log n) |
| `edge_online.kara` | the best node kept as the scores rise: a node whose score passes the best's, or meets it at a smaller label, takes its place. O(n) |
| `edge_map.kara` | only the nodes pointed at get a score, summed in a `Map` through `entry(..).or_insert(0)`; the walk over the map compares labels on a tie, so its order does not matter. O(n) |
| `edge_iter.kara` | iterators: the scores folded by `enumerate`, the answer by `max_by_key` on (score, -label) |
| `edge_solution.kara` | LeetCode's Rust template: scores from `vec![0i64; n]`, the edges by `enumerate` with `for (i, &e)`, `e as usize` and `i as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; two nodes;
`10^5` nodes all pointing at node 0, `10^5` each pointing at half its
label, and `10^5` each pointing at the next around a cycle; then 2000
random graphs of 2 to 40 nodes, each edge to any other node or, with a
chance of 1 in 2, to one of the first three, with a checksum and how
many have node 0 for the answer. `edge.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 3000 random
graphs against the smallest node by (minus its score, its label).

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 9 edits: `struct Solution;` given its braces,
`Vec<i32>` its brackets, `vec![0i64; edges.len()]` written
`Vec.filled(edges.len(), 0)`, the `&` of `(i, &e)` dropped, the
`as i64` on the index `i` dropped, and `Solution::` written with a dot.
`e as usize` and `best as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each node's score the sum of the labels of every node whose
edge points at it, by a scan of every edge, and the answer the node that
no other node beats, by a higher score or the same score at a smaller
label, checked against every other node. It checks 300 random graphs of
2 to 40 nodes drawn as the harness draws them; then 30 of up to 600
nodes; then 15 of up to 300 nodes whose edges all go to one of three
nodes; then 15 of up to 300 nodes falling, each pointing at the one
below it or, with a chance of 1 in 64, at a random node below it, node
0 at node 1, so that the last node is the only one pointing at the node
below it, which wins in 7 of them. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | a node from 0 to `n - 1` that some edge points at |
| P3 | a new node `n` pointing at the answer: the same answer |
| P4 | node 0's edge pointed at another node: the same answer |
| P5 | a new node `n` pointing at node `v`: `v` when its score and `n` pass the answer's, or meet it at a smaller label; else the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the labels sum to more than 0, so some node pointed at
scores more than every node no edge points at. P3 holds because only
the answer's score rises, and P4 because node 0 adds 0 to whatever
score it points at. P5 reads the literal scores: only `v`'s score
rises, by `n`. Node `v` is the case's number times 7, plus 3, modulo
`n`.

The differential prints `360 cases: checksum 909479569, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes the smallest node by (minus its score, its
label). On a failure it prints the first ten and then the count by
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
| M4 | ★: the score kept at the source | P1 318, P2 161, P4 337, P5 97, P6 318 |
| M5 | ★: labels counted from one | P1 5, P3 5, P4 1, P5 5, P6 5 |
| M6 | ★: the best score returned, not its node | P1 360, P2 341, P3 360, P5 79, P6 360 |
| M9 | sort: each edge adding the node's own label | P1 317, P3 11, P4 155, P5 81, P6 317 |
| M10 | sort: the last edge never read | P1 7, P3 7, P4 7, P5 1, P6 7 |
| M11 | sort: the best taken as the run's last source | P1 360, P2 197, P3 360, P5 79, P6 360 |
| M13 | online: the best chosen before the score rises | P1 79, P2 4, P3 79, P5 40, P6 79 |
| M15 | online: each source counted squared | P1 46, P3 44, P5 32, P6 46 |
| M16 | online: the last node's edge never read | P1 84, P3 84, P5 103, P6 84 |
| M17 | map: a node's first source counted twice | P1 47, P3 47, P4 28, P5 44, P6 47 |
| M19 | map: the last node's edge never read | P1 90, P3 90, P5 103, P6 90 |
| M21 | map: the label after the best returned | P1 360, P2 82, P5 79, P6 360 |
| M24 | iter: the lowest score's node | P1 360, P2 332, P3 360, P5 360, P6 360 |
| M25 | iter: node 0 never a candidate | P1 120, P2 1, P5 33, P6 120 |
| M26 | iter: the last source kept, not the sum | P1 206, P3 206, P5 280, P6 206 |
| M27 | solution: a tie won by the larger label | P1 13, P3 13, P5 13, P6 13 |
| M29 | solution: node 1 never tried | P1 107, P5 39, P6 107 |

P1, P5 and P6 kill all seventeen, P3 thirteen, P2 seven and P4 five.
P2 fails only the edits that answer with something other than a node
some edge points at: a score, a source, the label after the best, the
lowest score's node, or a node that may have no edge into it.
P4, node 0's edge moved, fails the edits for which node 0's label is
not 0 or where an edge's place in the list matters: the score kept at
the source, the labels counted from one, the node's own label added,
a node's first source counted twice, and the last edge never read.

The sort arm's last edge never read (M10) first survived: it loses the
last run of the sorted pairs only when that run is a single edge, and
that node wins only when its one source outscores every other node,
which none of the random graphs drew. The falling group, where the last
node alone points at the node below it, was added for it, and it now
fails in 7 cases.

Of the thirty-one, fourteen were not kept. A tie won by the larger
label in the ★, sort, online, map and iter arms (M2, M7, M14, M18,
M22) fails as in the template (M27); the score kept at the source in
the map arm (M20) as in the ★ arm (M4); each edge adding the node's own
label in the iter arm (M23) as in the sort arm (M9); the largest source
kept in the template (M30) as the iter arm's last source kept (M26);
and the template's best started at node 1 (M31) as the iter arm's node
0 never a candidate (M25). Each edge counting one in the ★ arm and the
template (M1, M28) fail alike and apart from every kept one, as do the
★ arm's last node never tried (M3), the sort arm's pairs sorted by
source (M8) and the online arm's tie never taking a smaller label
(M12); they were left out to keep three to an arm and two to the
template.

## Verification

Every arm prints the same output as `edge.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 1.6 s, and the differential
7.8 s there and 1.1 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 graphs of `10^5` nodes once from the harness's
generator, graph `a` sending each edge to one of the first `4^(a + 1)`
nodes (at most all of them), then makes 50 passes, pass `p` folding each
answer plus `p` into the checksum, with the ★ arm in all five languages.
Every implementation prints `50 passes over 10 graphs of 10^5 nodes:
checksum 512854864`. Every implementation builds its scores afresh in
each call.

BENCHTAB
