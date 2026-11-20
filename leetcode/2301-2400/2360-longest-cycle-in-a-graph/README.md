# 2360. Longest Cycle in a Graph

You are given a **directed** graph of `n` nodes numbered from `0` to
`n - 1`, where each node has **at most one** outgoing edge.

The graph is represented with a given **0-indexed** array `edges` of
size `n`, indicating that there is a directed edge from node `i` to
node `edges[i]`. If there is no outgoing edge from node `i`, then
`edges[i] == -1`.

Return *the length of the **longest** cycle in the graph*. If no cycle
exists, return `-1`.

A cycle is a path that starts and ends at the **same** node.

```
edges = [3,3,4,2,3]  ->  3
edges = [2,-1,3,1]   ->  -1
```

**Constraints:** `n == edges.length`; `2 <= n <= 10^5`;
`-1 <= edges[i] < n`; `edges[i] != i`.

With one edge out of every node, a walk from any node either ends at
`-1` or runs into a cycle, and every node lies on at most one cycle. So
the cycles can be found by walking from every node once, never walking
a node twice.

## Approaches

| file | mechanism |
|---|---|
| `longest.kara` ★ | each node stamped with the time it is first visited; a walk that reaches a node stamped since it began has closed a cycle as long as the time between the two visits. O(n) |
| `longest_kahn.kara` | peeling, as Kahn's topological sort does: every node no edge comes into removed until none is left, so that only the cycles remain, each then walked once to count it. O(n) |
| `longest_union.kara` | union-find: the edges added one by one, and an edge whose ends are already joined closes a cycle, walked from its head round to its tail to count it. O(n α(n)) |
| `longest_naive.kara` | no tables: from every node, at most `n` edges followed, and a node that comes back to itself lies on a cycle as long as the walk. O(n^2) |
| `longest_iter.kara` | iterators: from every start, the walk as a `scan` that stamps each node until it meets a stamped one or the end; the cycle closed, if any, from the stamp where it stopped, and the longest by `filter_map` and `max` |
| `longest_solution.kara` | LeetCode's Rust template: the ★ walk with `usize::MAX` for an unstamped node and a `usize` clock; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

The union-find arm is right because, before the edge out of `u` is
added, `u` has no edge out in the forest built so far, so every node of
its tree leads to `u`; an edge from `u` to a node of that tree therefore
closes a cycle through it, and walking from the edge's head reaches
`u`.

Every arm prints the same 8 lines: LeetCode's two examples; two nodes
pointing at each other; a cycle of 2000; a chain of 2000 into a cycle
of 1000; 1000 cycles of 2 and one of 3; a chain of 3000 with no cycle;
then 3000 random graphs of 2 to 30 nodes, each edge `-1` with a chance
of 1 in 1 to 1 in 8 and otherwise to another node, with a checksum and
how many have a cycle. `longest.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked against walking from every
node on 3000 random graphs.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: `struct Solution;` given its
braces, `Vec<i32>` its brackets, `vec![usize::MAX; n]` written
`Vec.filled(n, usize.MAX)`, `usize::MAX` written with a dot, `&&`
written `and`, and `Solution::` written with a dot. It also writes
`let mut best: i32 = -1`, since the bare `-1` would otherwise be an
`i64` and `best.max(... as i32)` would not type, and drops the harness's
`as i64` on the template's answer, an `i32` that widens on its own.
`usize::MAX` as the mark of an unstamped node and the `0usize` clock
stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every node and every length `k` from 1 to `n`, `k` edges
followed from the node, and `k` kept when they come back to it through
`k` different nodes. No stamps and no peeling. It checks 300 random
graphs of 2 to 30 nodes, each edge `-1` with a chance of 1 in 1 to 1 in
8 and otherwise to another node; then 30 of up to 2000 nodes; then 30 of
up to 300 nodes made of up to four cycles with trees hanging off them,
every node outside the cycles pointing at a lower one. All 360 are
drawn before any arm answers; 221 hold a cycle.

| | property |
|---|---|
| P1 | up to 40 nodes, the answer is the literal reading's |
| P2 | `-1`, or from 2 to `n` with some node coming back to itself in exactly that many steps |
| P3 | the nodes numbered backwards: the same answer |
| P4 | a new node with an edge into the graph: the same answer |
| P5 | a separate cycle one longer than the answer (at least 2) added: its length |
| P6 | each arm agrees with at least three of the other five |

P4 holds because nothing points at the new node, so it lies on no
cycle and every cycle stays as it was.

The differential prints `360 cases: checksum 113104622, 221 with a
cycle, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and tests each walk's nodes
with a `set`. On a failure it prints the first ten and then the count by
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
| M2 | ★: the cycle one longer | P1 178, P2 198, P5 360, P6 221 |
| M3 | ★: the walk from the start, not the cycle | P1 85, P2 76, P3 154, P6 100 |
| M5 | ★: the shortest cycle, not the longest | P1 35, P5 221, P6 62 |
| M9 | kahn: each cycle counted one short | P1 178, P2 197, P5 360, P6 221 |
| M10 | kahn: the edges counted as going in to the start | P1 233, P2 229, P3 256, P6 262 |
| M11 | kahn: the first cycle found, not the longest | P1 15, P3 46, P5 221, P6 34 |
| M12 | union: the walk started at the tail | P1 178, P2 221, P5 360, P6 221 |
| M13 | union: every joined pair a cycle of two | P1 115, P2 124, P5 221, P6 157 |
| M14 | union: only the tail's root looked up | P1 178, P5 360, P6 221 |
| M17 | naive: the walk capped at half the nodes | P1 4, P4 3, P5 4, P6 6 |
| M18 | naive: a walk that stops counted as a cycle | P1 177, P2 175, P4 19, P6 201 |
| M20 | naive: the start checked against the walk before its first step | P1 306, P2 360, P5 360, P6 360 |
| M24 | iter: any stamped stop taken as a cycle | P1 297, P2 269, P3 278, P4 97, P6 350 |
| M25 | iter: the walk capped at 5 steps | P1 44, P3 33, P5 6, P6 82 |
| M26 | iter: the last cycle found, not the longest | P1 26, P3 28, P6 41 |
| M29 | solution: a walk that starts on its cycle not counted | P1 93, P3 103, P5 360, P6 121 |
| M30 | solution: a cycle of two not counted | P1 63, P5 203, P6 64 |

P1 and P6 kill all seventeen, P5 twelve, P2 nine, P3 seven and P4
three. P3, the nodes numbered backwards, fails the edits whose answer
depends on the order the nodes are taken in: the walk counted from its
start, which counts the tail before the cycle and so depends on where
the walks begin; the edges counted into the start, which peels a
different set; the first or last cycle found; the walk capped at 5
steps; any stamped stop taken as a cycle; a walk that starts on its
cycle not counted. P4, a new node with an edge into the graph, fails
three: the naive walk capped at half the nodes, whose cap the new node
raises; a walk that stops counted as a cycle, which the new node's walk
can make longer; and any stamped stop taken as a cycle, since the new
node is walked last and reaches nodes stamped long before. P5, a
separate cycle one longer than the answer, fails every edit that
miscounts a cycle's length or keeps one other than the longest.

Five edits were rewritten before this set was run to its end, since
they could not be kept. The peel taking a node at one edge in looped
forever, and node 0 never queued for the peel, its replacement, crashes
on reaching `-1` from a node left unpeeled (M7); the peel stopped after
the first wave crashes the same way (M8). The union-find arm's path
never compressed and a closing edge also joined are both equivalent to
it, since compression and a join of one root with itself change no
answer; they became only the tail's root looked up (M14) and a cycle
counted only when its head is lower (M15). That one is equivalent too:
the edge that closes a cycle is the one out of its highest node, the
last of the cycle to be added, so its head is always lower. The
iterator arm's empty walk stopped at `-1` rather than its start gives
`None` either way and became the last cycle found (M26). The template's
clock reset each walk underflows its `usize` and crashes, and its last
node never a start is equivalent, as every cycle has a second node to
start from; they became a walk that starts on its cycle not counted
(M29) and a cycle of two not counted (M30).

Of the thirty-one, fourteen were not kept. Besides M7, M8 and M15 above,
three more change no answer: node 0 never a start in the ★ arm (M6),
for the same reason as the template's last node, and the iterator arm's
walk carried on through nodes earlier walks stamped (M22), which only
finds again a cycle already found. Any stamped node taken as closing a
cycle and the clock never advanced past a walk in the ★ arm (M1, M4)
fail as the iterator arm's any stamped stop (M24) and the template's
earlier walk taken as closing (M28); the cycle one longer in the ★ arm
(M2) as the naive walk started one step late (M19); each cycle counted
one short in the peel (M9) as the cycle counted from 0 in union-find
(M16) and the cycle one shorter in the iterator arm and the template
(M23, M31); the walk from the start, not the cycle, in the ★ arm (M3)
as the template's cycle counted from the walk start (M27); and the
shortest cycle in the ★ arm (M5) as the naive arm's shortest kept
(M21).

## Verification

Every arm prints the same output as `longest.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.7 s but the naive one,
2.6 s, which walks up to `n` edges from every node of the 3000-node
graphs. The differential takes 6.8 s there and 0.60 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 graphs of `10^5` nodes once from the harness's
generator: graph `a` shuffles the nodes into one line and cuts it into
pieces with a chance of 1 in `2^(a + 4)` at each link, and each piece's
last node points back to the piece's first with a chance of 1 in 2 and
otherwise at a random node. It then makes 50 passes, pass `p` folding
each answer plus `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `50 passes over 10 graphs of
10^5 nodes: checksum 174697543`. Each call allocates its stamp table,
in every language alike, since the table is the algorithm.

BENCHTAB
