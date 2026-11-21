# 2497. Maximum Star Sum of a Graph

There is an undirected graph consisting of `n` nodes numbered from `0`
to `n - 1`. You are given a **0-indexed** integer array `vals` of
length `n` where `vals[i]` denotes the value of the `i`th node.

You are also given a 2D integer array `edges` where
`edges[i] = [ai, bi]` denotes that there exists an **undirected** edge
connecting nodes `ai` and `bi`.

A **star graph** is a subgraph of the given graph having a center node
containing `0` or more neighbors. In other words, it is a subset of
edges of the given graph such that there exists a common node for all
edges.

The **star sum** is the sum of the values of all the nodes present in
the star graph.

Given an integer `k`, return *the **maximum star sum** of a star graph
containing **at most*** `k` *edges.*

```
vals = [1,2,3,4,10,-10,-20], edges = [[0,1],[1,2],[1,3],[3,4],[3,5],[3,6]], k = 2  ->  16
vals = [-5], edges = [], k = 0                                                     ->  -5
```

**Constraints:** `n == vals.length`; `1 <= n <= 10^5`;
`-10^4 <= vals[i] <= 10^4`; `0 <= edges.length <= min(n * (n - 1) / 2, 10^5)`;
`edges[i].length == 2`; `0 <= ai, bi <= n - 1`; `ai != bi`; `0 <= k <= n - 1`.

A star round a centre may take any of its neighbours, up to `k`, and
each one taken adds its value, so the best star round a centre takes
its largest neighbours while they are positive, and the answer is the
best of those stars over every centre. No sum passes `10^4 * 10^5`, so
the template's `i32` is enough. The approaches differ in how they find
each centre's largest neighbours.

## Approaches

| file | mechanism |
|---|---|
| `star_sum.kara` ★ | each node's neighbours' values listed, sorted, `reverse`d, and added while positive and fewer than `k`. O(n + m log m) |
| `star_sum_heap.kara` | a least-first `PriorityQueue` per node of its positive neighbours' values, popped whenever it holds more than `k`, so it ends with the `k` largest. O(n + m log k) |
| `star_sum_greedy.kara` | every positive edge end offered to the other end, all offers sorted, and taken largest first by any centre that has taken fewer than `k`. O(n + m log m) |
| `star_sum_select.kara` | a recursive quickselect over each node's positive neighbours' values, partitioned round a middle pivot, the sum of the `k` largest read off the larger side; nothing sorted. O(n + m) expected |
| `star_sum_iter.kara` | iterators: every node `map`ped to its star, its neighbours' values `filter`ed to the positive and sorted, then `rev`, `take(k)` and `sum`, and the `max` of the stars. O(n + m log m) |
| `star_sum_solution.kara` | LeetCode's Rust template: `Vec<i32>`, `Vec<Vec<i32>>` and `k: i32` in, `i32` out; positive neighbours pushed, `sort_unstable_by` largest first, `take(k as usize)` summed; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and six
more; then 2000 random graphs of 1 to 30 nodes and up to 60 tries at an
edge, with values to 20 and 2000 with values to `10^4`, `k` from 0 to
`n - 1`, each as a checksum; then the constraints' largest, `10^5`
nodes: a star of `10^4`s round node 0 with `k = n - 1`; `10^5` tries at
a random edge with `k` of 50 and of 0; and a path whose values
alternate in sign, `k = 2`. `star_sum.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 3000 random
graphs of 1 to 6 nodes against every set of at most `k` neighbours of
every centre, and the two agreed on every graph.

`check` first reports 6 errors on the template: `struct Solution;`, the
three `Vec<...>` types, the `&` of `&edges`, and `i32::MIN`. `karac fix`
carries it in one call, reporting 19 edits: `struct Solution {}`; the
brackets; `vec![vec![]; n]` becomes `Vec.filled(n, Vec.new())`;
`&edges` becomes `ref edges`; the two `as usize` casts of the ends
become `as i64`; `i32::MIN` becomes `i32.MIN`; `sort_unstable_by`
becomes `sort_by`; `take(k as usize)` becomes `take(k)`; and the
wrapper's `as i64` on the template's answer is dropped, since an `i32`
widens to `i64` on its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every node as the centre, every set of at most `k` of
its neighbours is tried, each set read off the bits of a mask, and the
greatest sum of a centre and its set is taken. Nothing is sorted. It
checks 300 random graphs of 1 to 7 nodes and up to 12 tries at an edge,
values from -2 to 5 or from -5000 to `10^4`, and `k` from 0 to 3 and
below `n`; then 20 of one node; and 40 of 12 to 20 nodes with up to 60
tries. All 360 are drawn before any arm answers. The values lean
positive and `k` stays small so that most centres have more positive
neighbours than they may take.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | at least the greatest value, and at most that plus `k` times it |
| P3 | the edges in the other order, each end for end: the same answer |
| P4 | `k = 0`: the greatest value |
| P5 | `k` one more, below `n`: no less, and at most the greatest value more |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a single node is a star, and no star holds more than
`k + 1` values. P5 holds because a star that may take one more
neighbour may take the same ones, and one more adds at most the
greatest value.

The differential prints `360 cases: checksum 141180968, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that builds the same cases and tries every set of neighbours. On a
failure it prints the first ten and then the count by property.

The first differential drew values from `-top` to `top` and `k` from
0 to `n - 1`, with P4 the nodes numbered backwards and P5 every value
doubled. It was too weak: six of the edits below were killed on one
case only, the select arm's pivot's place not fixed survived, and P4
and P5 killed nothing, since both hold for every edit that keeps the
answer's shape. The cases were drawn again as above, and P4 and P5
replaced by the two that ask how the answer moves with `k`.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the neighbours left smallest first | P1 68, P6 68 |
| M2 | ★: negative neighbours taken too | P1 41, P2 37, P5 30, P6 41 |
| M5 | ★: edges one way only | P1 32, P3 32, P6 32 |
| M8 | heap: the queue kept to k + 1 | P1 96, P2 69, P4 180, P6 96 |
| M10 | heap: the centre's value offered for each neighbour | P1 135, P6 135 |
| M11 | heap: only the least kept added | P1 53, P5 23, P6 53 |
| M13 | greedy: every centre one offer short | P1 98, P6 98 |
| M14 | greedy: an offer sent to its own end | P1 147, P3 143, P6 147 |
| M16 | greedy: offers taken never counted | P1 53, P2 29, P5 20, P6 53 |
| M17 | select: the pivot's value lost | P1 16, P3 14, P5 1, P6 16 |
| M19 | select: one largest never summed | P1 96, P3 3, P5 20, P6 96 |
| M20 | select: the pivot's place not fixed | P1 4, P3 2, P5 2, P6 4 |
| M23 | iter: only zeros refused | P1 42, P2 37, P5 29, P6 42 |
| M25 | iter: the least star | P1 279, P2 268, P4 295, P6 279 |
| M26 | iter: the centre's value for its neighbours | P1 186, P6 186 |
| M28 | solution: only zeros refused at one end | P1 27, P2 25, P3 35, P5 13, P6 27 |
| M31 | solution: an edge's ends read the same | P1 169, P3 127, P6 169 |

P1 and P6 kill all seventeen, P5 eight, P3 seven, P2 six, and P4 two.

Fourteen are not kept, and none survives. Three fail exactly as a kept
one: the ★ arm's one neighbour too many and the iter arm's `k + 1`
taken (M3, M24) as the heap arm's queue kept to `k + 1` (M8); and the
heap arm's only zeros refused (M9) as the iter arm's (M23), since both
let negative neighbours in. Ten fail as one
another, in three sets: the heap arm's largest popped, the greedy
arm's offers taken smallest first, the select arm's smaller values put
first, the iter arm's smallest `k` taken and the template's sorted
smallest first (M7, M12, M18, M22, M27), all of which take a centre's
smallest positive neighbours when it has more than `k`, and are seen on
the same 29 cases; the ★,
greedy and select arms' centre's own value left out (M4, M15, M21);
and the ★ arm's best begun at 0 and the template's answer begun at 0
(M6, M30), wrong only on the 26 cases whose every value is negative.
Each set could give one kept edit, but every arm with a member already
keeps three that fail apart from every other, or, for the template,
two. The template's largest skipped (M29) fails in a way of its own,
but its arm already holds its two.

One edit was replaced before this table was drawn: the template's
answer begun at 0 was first `let mut ans = 0;`, which `check` refused,
since an unannotated literal keeps the default `i64` (`docs/design.md`
§8 Literals) and `ans` is returned as the template's `i32`; it runs as
`let mut ans: i32 = 0;` (M30).

## Verification

Every arm prints the same output as `star_sum.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.4 to 10.9 s and the differential 1.1 s; under `karac __mir-llvm-asan` the arms take 1.3 to 3.1 s and the differential 0.8 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds one graph of `10^5` nodes once from its own generator,
values from `-10^4` to `10^4` and `10^5` tries at a random edge, 99997
of them taken; then makes 125 passes. Each sets one node's value and
`k`, below 50, from the checksum so far, asks, and puts the value back,
folding the answer plus the pass into the checksum. Every answer builds
its lists afresh and sorts every node's. The bench uses the ★ arm in
all five languages: C with the lists in compressed rows sorted by
`qsort` and the edges deduplicated in an open-addressed table, Go with
`slices.Sort` and `slices.Reverse`. Every implementation prints `125
passes over 10^5 nodes and 99997 edges: checksum 264651993`.

BENCHTAB
