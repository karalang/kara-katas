# 2045. Second Minimum Time to Reach Destination

A city is represented as a bi-directional connected graph with `n`
vertices, labeled from `1` to `n`. The edges are given as a 2D integer
array `edges`, where `edges[i] = [ui, vi]` is an edge between `ui` and
`vi`. Every pair of vertices is joined by at most one edge, and no vertex
has an edge to itself. Crossing any edge takes `time` minutes.

Each vertex has a traffic signal that changes its color from green to red
and red to green every `change` minutes. All signals change at the same
time. You may enter a vertex at any time, but may leave it only while its
signal is green, and you cannot wait at a vertex whose signal is green.
The second minimum value is the smallest value strictly larger than the
minimum value. Given `n`, `edges`, `time` and `change`, return the second
minimum time it takes to go from vertex `1` to vertex `n`. You may pass
through any vertex any number of times, including `1` and `n`, and every
signal is green when the journey starts.

```
n = 5, edges = [[1,2],[1,3],[1,4],[3,4],[4,5]], time = 3, change = 5  ->  13
n = 2, edges = [[1,2]], time = 3, change = 2                          ->  11
```

**Constraints:** `2 <= n <= 10^4`; `n - 1 <= edges.length <= min(2 *
10^4, n (n - 1) / 2)`; `edges[i].length == 2`; `1 <= ui, vi <= n`; `ui !=
vi`; no edge is repeated; the graph is connected; `1 <= time, change <=
10^3`.

Nobody may wait at a green light, so a journey's time depends only on how
many edges it crosses, and grows with them. The second minimum time is
then the time of the second smallest walk length from `1` to `n`: the
shortest length `d` plus one if some walk has the other parity, else `d +
2`, there and back across one edge.

## Approaches

| file | mechanism |
|---|---|
| `second.kara` ★ | a breadth-first search with a `VecDeque[(i64, i64)]` and `while let Some((u, d)) = queue.pop_front()` that keeps each vertex's two smallest distinct walk lengths, visiting it at most twice; then the lights applied step by step. O(n + edges) |
| `second_dijkstra.kara` | Dijkstra's search on the clock: the state is a vertex and the minute it is reached, leaving waits out a red light, and each vertex keeps its two smallest distinct arrival times in a min-first `PriorityQueue[(i64, i64)]`. O(edges log n) |
| `second_ends.kara` | two plain searches, from `1` and from `n`; every edge `u - w` bounds a walk at `from_start[u] + 1 + from_end[w]`, and the walk of the other parity is `d + 1` exactly when some bound is. O(n + edges) |
| `second_parity.kara` | one search over `(vertex, parity)` states, `2 * v + p`, each edge joining one parity to the other; the shortest walk of each parity gives the second length. O(n + edges) |
| `second_levels.kara` | the walks level by level: the frontier at level `k` holds the vertices first or second reached by a walk of `k` edges, and the second level that holds `n` is the answer's length. O(n + edges) |
| `second_solution.kara` | LeetCode's Rust template (`use std::collections::VecDeque`, `vec![vec![]; n + 1]`, `vec![[i32::MAX; 2]; n + 1]`, `for &v in &g[u]`, `as usize`, `&&`, `i32` arithmetic), carried by `karac fix` in three rounds to a clean check |
| `differential.kara` | the six arms against the walks enumerated by length and timed, six properties |

Every arm prints the same 8 lines: the answers for LeetCode's two examples
and four more; then the sum and a checksum of the answers for 2000 graphs
of 2 to 10 vertices (a random tree and up to `n` more edges, `time` and
`change` from 1 to 10), and for 4 graphs of 10000 vertices and 20000
edges, the most the constraints allow: a random tree, a bushy one, a chain
of short branches and a path, each with 10001 more edges. `second.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the set of vertices that a walk of exactly `k` edges can reach,
for `k = 0, 1, ..`, every edge tried from every reached vertex, until `n`
has been reached at three lengths; each length timed minute by minute at
the lights, and the second smallest distinct time taken. It checks 1500
graphs of 2 to 8 vertices (a random tree and up to three more edges, `time`
and `change` from 1 to 10), each with a relabelling of the vertices other
than `1` and `n` and an edge to add. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the walks enumerated by length and timed |
| P2 | the vertices other than `1` and `n` relabelled leave the answer |
| P3 | the edges listed backwards, each end for end, leave the answer |
| P4 | an edge added never makes the answer later |
| P5 | `time` and `change` both doubled double the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 graphs: checksum 130947549, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, then six
more, two to each of the Dijkstra, ends and levels arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a second length equal to the first allowed (`<=`) | P1 83, P6 83 |
| M2 | ★: a red light held a whole period | P1 578, P6 578 |
| M3 | ★: each edge one way only | P1 1282, P3 388, P4 196, P6 1282 |
| M4 | dijkstra: the lights ignored | P1 1039, P6 1039 |
| M5 | dijkstra: a red light held one period too long | P1 857, P6 857 |
| M6 | dijkstra: the edge crossed before the wait | P1 847, P6 847 |
| M7 | ends: the other parity sought one step short (`d` for `d + 1`) | P1 1119, P6 1119 |
| M8 | ends: each edge crossed one way | P1 22, P3 270, P6 22 |
| M9 | ends: both searches from the start | P1 761, P6 761 |
| M10 | parity: a missing parity taken as one step on | P1 999, P4 263, P6 999 |
| M11 | parity: the shortest taken as the longer parity | P1 501, P4 180, P6 501 |
| M12 | parity: a green light one minute late | P1 932, P5 1039, P6 932 |
| M13 | levels: the first level that holds n taken | P1 1500, P6 1500 |
| M14 | levels: a green light one minute early | P1 1039, P5 1039, P6 1039 |
| M15 | levels: each edge a minute slower | P1 1500, P5 1500, P6 1500 |
| M16 | solution: the first length plus two | P1 381, P6 381 |
| M17 | solution: the adapter swapping time and change | P1 1363, P6 1363 |

P1 and P6 kill all seventeen, P4 three, P5 three, P3 two and P2 none. Most
edits change the answer for a whole class of graphs and nothing else, so
their counts tell them apart: the second smallest walk length is `d + 1` on
381 of the 1500 graphs and `d + 2` on the other 1119, which is what the
parity edits (M7) and the plus-two edit (M16) fail on. P3 sees only the
edits that take each edge one way, which listing the edges end for end
turns around (M3, M8). P4 sees the edits under which one more edge can make
the answer later: edges one way, where which walks the search can follow
depends on the edges there are (M3), a missing parity taken as one step on,
so a graph with walks of one parity only answers 0 until an edge gives it
the other (M10), and the longer parity taken as the shortest, which an edge
that shortens one parity lengthens (M11). P5 doubles `time` and `change`,
which doubles every honest answer, so it sees only the edits that add a
fixed minute: a green light a minute late or early (M12, M14) and every
edge a minute slower (M15). P2 relabels the vertices other than `1` and
`n`, and no edit here depends on a label.

Of the first thirty, two were not kept. The Dijkstra arm's start never
marked reached survived: `best[1]` then stays at `i64.MAX` until a walk
returns to `1`, but nothing is ever read from vertex `1`'s times, so the
edit changes no answer. And its second arrival never passed on crashed:
`next[n]` stayed at `i64.MAX` and the checksum overflowed. The edge crossed
before the wait and the round trip taken unlit replaced them; the second
is left out, as the arm keeps three. The levels arm's two last drafts both
failed as M13, and a green light a minute early and every edge a minute
slower replaced them; the ends arm's two extra edits, any longer bound
taken as the other parity and the fallback one step on, both fail as M7.

The rest fail as a kept one does: a wait on green rather than red (★ and
Rust arms), each hop counted twice (ends), the first level that holds `n`
and the second counted one late (levels) all change every answer and fail
as M13; a second length or arrival equal to the first allowed (★,
Dijkstra, Rust) and a vertex counted twice in one level fail as M1; a red
light held a whole period in the Rust arm fails as M2; the first length
plus two (★) and the parity never flipped fail as M16; the fallback three
steps on and the frontier never cleared fail as M7. The parity arm's other
parity always the odd one fails on 223 graphs of its own and is left out,
as that arm keeps three.

## Verification

Every arm prints the same output as `second.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.9 s (levels) to 3.4 s (dijkstra)
and the differential 3.6 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds (ten edits, three, then five) to a clean check: the
`use std::collections::VecDeque` line deleted (it is in Kāra's prelude),
`Vec<..>` to `Vec[..]`, `as usize` to `as i64` (Kāra indexes with `i64`)
and `1usize` to `1`, `for e in &edges` to `for e in ref edges`, `for &v in
&g[u]` to `for v in ref g[u]`, `VecDeque::new` to `VecDeque.new`,
`vec![vec![]; n + 1]` to `Vec.filled(n + 1, Vec.new())`, `vec![[i32::MAX;
2]; n + 1]` to `Vec.filled(n + 1, [i32.MAX; 2])`, `&&` to `and`, and `let
mut ans = 0` to `let mut ans: i32 = 0`, since the comparison with an `i32`
does not fix a literal's type.

## Benchmarks

The bench builds 4 graphs of 10000 vertices and 20000 edges once in all
five languages, the most the constraints allow, and runs the ★ arm on every
graph for 250 rounds, each with its own `time` and `change`: 1000 calls.
Every implementation prints `1000 calls: sum 4637415, checksum 801727289`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.045 to 1.104 s | 1.084 s |
| Kāra (`karac build`) | 1.501 to 1.634 s | 1.559 s |
| Rust (`rustc -O`) | 1.541 to 1.662 s | 1.572 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.529 to 1.706 s | 1.576 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.571 to 1.705 s | 1.625 s |
| Go | 3.130 to 3.487 s | 3.224 s |
| Python | 14.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.527 s) is not above its real time (1.559 s).

The sequential Kāra program is 0.97x Rust under overflow checks and 1.45x
C.
