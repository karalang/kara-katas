# 2242. Maximum Score of a Node Sequence

There is an **undirected** graph with `n` nodes, numbered from `0` to
`n - 1`. You are given a **0-indexed** integer array `scores` of length
`n` where `scores[i]` denotes the score of node `i`, and a 2D integer
array `edges` where `edges[i] = [a_i, b_i]` denotes that there exists an
undirected edge connecting nodes `a_i` and `b_i`.

A node sequence is **valid** if every pair of adjacent nodes in the
sequence is connected by an edge, and no node appears more than once in
the sequence. The score of a node sequence is the sum of the scores of
its nodes.

Return *the **maximum score** of a valid node sequence with a length of
`4`*. If no such sequence exists, return `-1`.

```
scores = [5,2,9,8,4], edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]  ->  24
scores = [9,20,6,4,11,12], edges = [[0,3],[5,3],[2,4],[1,3]]          ->  -1
```

**Constraints:** `4 <= n <= 5 * 10^4`; `1 <= scores[i] <= 10^8`;
`1 <= edges.length <= 5 * 10^4`; `a_i != b_i`; there are no duplicate
edges.

Every sequence of four is a middle edge `(b, c)` with a neighbour `a` of
`b` and a neighbour `d` of `c`, all four distinct. Only the three
best-scored neighbours of a node can be its `a` or `d`: at most two of
its neighbours are ruled out (`c` and `d`, or `b` and `a`), so one of
the best three is always free and no worse. Each edge is tried one way
round only, since the other gives the same sequences reversed.
O(n + m log m).

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | each node's neighbours sorted by score, largest first, with `sort_by` and cut with `truncate(3)`; every edge tries the nine pairs |
| `score_insert.kara` | no sort: a `keep` helper (`top: mut ref Vec[i64]`) pushes a new neighbour, slides it up past smaller scores with `swap`, and `pop`s a fourth off the end, as the edges are read. O(n + m) |
| `score_heap.kara` | a min-first `PriorityQueue[(i64, i64)]` of `(score, neighbour)` per node, popped whenever it holds a fourth, then drained into a list with `while let Some(..) = pop()`. O(n + m) |
| `score_struct.kara` | a `struct Graph` of the scores and the three best neighbours, built by `Graph.build`; `end` (`ref self`) the best neighbour that is neither of two others as an `Option`, and `through` (`ref self`) the best sequence with `(b, c)` in the middle |
| `score_iter.kara` | iterator chains: the neighbour lists `map`ped to sorted copies and `take(3)`; the best over the edges by nested `filter_map`, `filter`, `map` and `max`, `unwrap_or(-1)` when there is none |
| `score_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `Vec<Vec<i32>>` in, `i32` out, the adjacency a `Vec<Vec<usize>>` from `vec![vec![]; n]`, each list sorted with `sort_by(\|&x, &y\| ...)` and `truncate(3)`, the pairs through `for &a in &g[b]`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four
more (a path of exactly four, a star with no four in a row, a triangle
with a tail, and a square of the largest scores), each with its answer;
then how many of 2000 graphs of 4 to 12 nodes and up to 20 edges
(scores up to 1 to 100) have a sequence, with a checksum of the
answers; then the constraints' largest, 5 * 10^4 nodes and 5 * 10^4
edges with scores up to 10^8; then a hub of 49999 spokes with one edge
between two of its leaves, where a node has 49999 neighbours to cut to
three. `score.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 37 edits: `Vec<..>`
to `Vec[..]`, `vec![vec![]; n]` to `Vec.filled(n, Vec.new())`, `for e
in &edges` and `for &a in &g[b]` to `for e in ref edges` and `for a in
ref g[b]`, the `&` patterns dropped from the closures' parameters and
the `&` from `cmp(&scores[x])`, `&&` to `and`, `let mut ans = -1` typed
`i32`, `struct Solution;` to `struct Solution {}`, `Solution::` to
`Solution.`, `vec![a as i32, b as i32]` to `[a as i32, b as i32]`, and
the adapter's `as i64` removed.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered four of distinct nodes tried, kept when each is
joined to the next by an edge, and the best score of those taken; no
neighbour lists. It checks 300 random graphs of 4 to 7 nodes and up to
12 edges, scores up to 50; then 30 whose scores are 1 to 3, full of
ties; then 30 stars with one edge between two leaves. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the best sequence's score, read literally, or -1 |
| P2 | every edge written the other way round and the list reversed: the same answer |
| P3 | the nodes renumbered by a rotation, their scores with them: the same answer |
| P4 | one more edge: no lower answer |
| P5 | every score one higher: four more, or -1 again |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 144200307, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that walks
every path of three edges by depth-first search over adjacency sets,
never revisiting a node. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two neighbours kept | P1 16, P2 2, P4 7, P6 16 |
| M5 | ★: d taken from b's neighbours | P1 296, P2 231, P6 296 |
| M6 | ★: c scored twice and d not at all | P1 273, P2 216, P6 273 |
| M7 | insert: a new neighbour slid no further than second | P1 4, P2 5, P4 1, P6 4 |
| M9 | insert: the best dropped instead of the fourth | P1 50, P2 2, P4 3, P6 50 |
| M10 | insert: b kept as its own neighbour | P1 298, P2 197, P6 298 |
| M12 | heap: a max-first queue, keeping the worst three | P1 49, P3 1, P4 2, P6 49 |
| M13 | heap: two kept | P1 8, P2 10, P3 2, P6 8 |
| M14 | heap: a's neighbours ranked by number, not score | P1 17, P2 27, P3 19, P4 2, P6 17 |
| M18 | struct: the worst sequence kept | P1 77, P2 65, P4 12, P6 77 |
| M19 | struct: one neighbour kept | P1 192, P2 13, P4 26, P6 192 |
| M20 | struct: d sought among b's neighbours | P1 125, P2 60, P6 125 |
| M23 | iter: a allowed to be c | P1 247, P2 132, P6 247 |
| M24 | iter: d allowed to be b | P1 267, P2 132, P6 267 |
| M25 | iter: no sequence answered 0 | P1 75, P5 75, P6 75 |
| M29 | solution: a allowed to be d | P1 170, P6 170 |
| M31 | solution: the scores halved on the way in | P1 285, P5 264, P6 285 |

P1 and P6 kill all seventeen, P2 thirteen, P4 seven, P3 three and P5
two. P2 turns every edge round, so an arm that looks at an edge from one
side only and gets that side wrong answers differently; it misses only
the edits that stay symmetric. P3's rotation changes nothing but the
numbering, and catches only the heap edits: the queue ranks equal
scores by node number, and M14 ranks every neighbour by it. P5 is there for the answer when there
is no sequence (M25) and for scores changed on the way in (M31).

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. One survives and is equivalent: the insert arm
keeping four neighbours (M8), since more than three never loses the
best. Eight fail as a kept one does: the ★ and struct arms' a allowed
to be c (M3, M21) as the iter arm's (M23); the ★ arm's d allowed to be
b (M4) as the iter arm's (M24); the heap and struct arms' a or end
allowed to be the far one (M15, M17) as the template's (M29); the iter
arm's and the template's two neighbours (M22, M27) as the ★ arm's (M1);
and the template's no sequence answered 0 (M28) as the iter arm's (M25).
Three fail alike in a group of their own: the neighbours sorted smallest
first in the ★, iter and template arms (M2, M26, M30). Two fail their
own way and are left out for the count of three: the insert arm's ends
taken from the wrong sides (M11) and the heap arm's b scored for c
(M16).

## Verification

Every arm prints the same output as `score.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the insert, struct and ★ arms take 1.5 s to
1.7 s, the template 2.5 s, the heap arm 3.2 s, the iter arm 3.8 s, and
the differential 1.3 s.

## Benchmarks

The bench answers 40 graphs of 5 * 10^4 nodes and 5 * 10^4 edges, edge
`j` joining node `j` to a node 1 to 24998 after it round the ring so
that no two edges join the same pair, scores up to 10^8, with the ★ arm
in all five languages. C keeps the neighbours in one array by offsets
(CSR) and sorts each node's slice with `qsort`; the others keep a list
per node. Every implementation prints `40 graphs of 50000 nodes:
checksum 132004844`.

BENCHTAB
