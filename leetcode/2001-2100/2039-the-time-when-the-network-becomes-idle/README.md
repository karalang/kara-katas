# 2039. The Time When the Network Becomes Idle

There is a network of `n` servers, labeled from `0` to `n - 1`. You are
given a 2D integer array `edges`, where `edges[i] = [ui, vi]` means there
is a message channel between servers `ui` and `vi`, and they can pass any
number of messages to each other directly in one second. You are also
given a 0-indexed integer array `patience` of length `n`.

All servers are connected. Server `0` is the master server; the rest are
data servers. Each data server sends its message to the master at the
beginning of second 0, and messages travel by the fewest hops. The master
processes every message instantly and sends a reply back along the reversed
path. Starting from second 1, at the beginning of every second, each data
server checks whether it has received a reply. If it has not, it resends
its message every `patience[i]` seconds: whenever `patience[i]` seconds
have passed since it last sent. Otherwise it sends no more. The network is
idle when no messages are passing between servers or arriving at them.
Return the earliest second from which the network is idle.

```
edges = [[0,1],[1,2]], patience = [0,2,1]          ->  8
edges = [[0,1],[0,2],[1,2]], patience = [0,10,10]  ->  3
```

**Constraints:** `2 <= n <= 10^5`; `patience[0] == 0`; `1 <= patience[i]
<= 10^5` for the data servers; `1 <= edges.length <= min(10^5, n (n - 1) /
2)`; no edge joins a server to itself and none is listed twice; every
server can reach every other.

A server `d` hops from the master has its first reply back at second `2 d`.
It sends at `0, p, 2 p, ...` while that reply has not come, so its last
message leaves at the largest multiple of `p` below `2 d`, `(2 d - 1) / p
* p`, and that message's reply arrives `2 d` later. The network is idle
the second after the last such reply, so one breadth-first search from the
master gives every `d`.

## Approaches

| file | mechanism |
|---|---|
| `network.kara` ★ | adjacency lists from `Vec.filled(n, Vec.new())`, breadth-first search with a `VecDeque` and `while let Some(u) = queue.pop_front()`, then the last reply over the data servers. O(n + edges) |
| `network_dijkstra.kara` | Dijkstra's search with a min-first `PriorityQueue` of `(hops, server)`, every edge one hop, stale entries skipped as they are popped. O((n + edges) log n) |
| `network_levels.kara` | the search one level at a time, the whole frontier per round, so the round number is the hop count; each server's idle time taken as it is reached. O(n + edges) |
| `network_flat.kara` | compressed adjacency: degrees counted, offsets by prefix sums, both ends of every edge in one flat array; a `Vec` queue read from a moving head; a server's sends counted as `ceil(2 d / p)`. O(n + edges) |
| `network_maps.kara` | neighbours in a `Map` from server to `Vec` filled through `entry(..).or_insert(..)`, hop counts in a second `Map`, the answer a `fold` over `patience.iter().enumerate().skip(1)`. O(n + edges) expected |
| `network_solution.kara` | LeetCode's Rust template (`use std::collections::VecDeque`, `Vec<Vec<i32>>`, `vec![vec![]; n]`, `for e in &edges`, `as usize`, `for &v in &graph[u]`, `i32` arithmetic), carried by `karac fix` in three rounds to a clean check |
| `differential.kara` | the six arms against the network run second by second, six properties |

Every arm prints the same 8 lines: the answers for LeetCode's two examples
and four more; then the sum and a checksum of the answers for 2000 networks
of 2 to 12 servers (a random tree and up to `n` more edges, patience up to
1 to 10), and for 4 networks of 100000 servers and 100000 edges, the most
the constraints allow: a random tree, a chain of short branches, a bushier
one and a path, each with one more edge. `network.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the network run second by second. Every server's hop count
comes from Floyd and Warshall's all-pairs table rather than a search; each
server keeps the seconds its messages' replies are due, checks at the start
of every second whether its first reply has come, and resends on its
patience if not. The answer is the first second with nothing in flight or
arriving. It checks 1500 networks of 2 to 9 servers (a random tree and up
to two more edges, patience up to 1 to 12), each with a relabelling of the
data servers and an edge to add. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the network run second by second |
| P2 | the data servers relabelled, with their patience, leave the answer |
| P3 | the edges listed backwards, each end for end, leave the answer |
| P4 | an edge added never makes the answer later |
| P5 | with every patience 100000 the answer is twice the farthest server's hop count, plus one |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 networks: checksum 221152826, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search as a stack (`pop_back` for `pop_front`) | P1 76, P3 77, P4 62, P5 76, P6 76 |
| M2 | ★: each edge one way only | P1 72, P3 1483, P5 72, P6 72 |
| M3 | ★: the last message counted from the whole round trip (`2 d / p` for `(2 d - 1) / p`) | P1 978, P6 978 |
| M4 | dijkstra: the master's neighbours two hops out | P1 1500, P5 1500, P6 1500 |
| M5 | dijkstra: the last message two seconds before the reply | P1 718, P6 718 |
| M6 | dijkstra: every other server skipped | P1 522, P2 534, P5 418, P6 522 |
| M7 | levels: levels past three taken as three | P1 134, P5 147, P6 134 |
| M8 | levels: the last send rounded down a patience more | P1 816, P6 816 |
| M9 | levels: only the first server reached counted | P1 1158, P3 252, P5 1122, P6 1158 |
| M10 | flat: the ceiling taken as a floor | P1 584, P5 1500, P6 584 |
| M11 | flat: every server searched from the master (`queue[0]` for `queue[head]`) | P1 1122, P4 15, P5 1122, P6 1122 |
| M12 | flat: the offsets summed one short | P1 7, P2 317, P5 6, P6 7 |
| M13 | maps: the first data server skipped | P1 227, P2 205, P5 207, P6 227 |
| M14 | maps: the last send rounded to an even second | P1 781, P6 781 |
| M15 | maps: the last data server skipped | P1 678, P2 434, P5 597, P6 678 |
| M16 | solution: a patience of 1 never resending | P1 484, P6 484 |
| M17 | solution: the first edge skipped | P1 1067, P3 920, P4 230, P5 1023, P6 1067 |

P1 and P6 kill all seventeen, P5 twelve, P2 four, P3 four and P4 three. P5
fixes the patience, so it sees every edit to the hop counts or to which
servers count (M1, M2, M4, M6, M7, M9, M11, M12, M13, M15, M17) and the
ceiling taken as a floor, which at patience 100000 sends nothing (M10); it
misses the five edits to the last send alone, which a patience longer than
any round trip makes the first send (M3, M5, M8, M14, M16). P2 sees the
edits that depend on which label a server has: every other one skipped
(M6), the first or last one skipped (M13, M15), and the offsets summed one
short, which loses the last server's neighbours (M12). P3 sees the edits
that depend on the order or direction the edges are listed in: a search in
stack order (M1), edges one way (M2), the first one skipped (M17), and the
first server reached taken alone (M9). P4 sees the edits under which one
more edge can make the answer later: a stack-order search may then find a
longer path first (M1); a search that expands only the master gives the
servers it misses a negative time, and an edge that brings one within a
hop makes it real (M11); and with the first edge skipped, an added edge
can reconnect the servers that cut off (M17).

The other thirteen fail as a kept one does. The ★ arm's hops counted twice
and last reply's second dropped, the Dijkstra arm's resend reply a second
late, the levels arm's last reply's second dropped, the flat arm's one send
too many and master one hop out, and the maps arm's round trip one way all
change every answer and fail as M4. The last message counted from the
whole round trip fails as M3 in the Dijkstra, levels and Rust arms. The
maps and Rust arms' searches as a stack fail as M1, and the Rust arm's
edges one way as M2. Ten first drafts were replaced. Nine changed every
answer and failed as M4 (the Dijkstra arm's hops twice, maximum taken as a
minimum and round trip one way; the levels arm's level counted after its
round and counted twice; the maps arm's hops its finder's and fold seeded
late; the Rust arm's round trip a hop longer each way and its last reply's
second dropped), and the one that replaced the Dijkstra arm's hops counted
twice crashed: relaxing only a server's first two
neighbours left some unreached at `i64.MAX`, and `2 * hops` overflowed.

## Verification

Every arm prints the same output as `network.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 3.9 s (levels) to 11 s (dijkstra) and
the differential 3.7 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds (ten edits, three, then one) to a clean check: the `use
std::collections::VecDeque` line deleted (it is in Kāra's prelude),
`Vec<..>` to `Vec[..]`, `for e in &edges` to `for e in ref edges`,
`VecDeque::new` to `VecDeque.new`, `for &v in &graph[u]` to `for v in ref
graph[u]`, `vec![-1i32; n]` to `Vec.filled(n, -1i32)`, `vec![vec![]; n]` to
`Vec.filled(n, Vec.new())` over two rounds (the empty `vec![]` has no
element type until the pushes give it one), and `let mut ans = 0` to `ans:
i32`, since an operator or a method does not fix a literal's type. The
empty `vec![]` first also stopped `dist[v]` with "index must be an integer
or range, found 'ref <error>'", a knock-on of the same error that went
with it.

## Benchmarks

The bench builds 4 networks of 100000 servers and 100000 edges once in all
five languages, the most the constraints allow, and runs the ★ arm for 25
rounds, one server's patience changed in every network before each call:
100 calls. Every implementation prints `100 calls: sum 10051627, checksum
207463364`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.497 to 0.564 s | 0.510 s |
| Rust (`rustc -O`) | 0.616 to 0.707 s | 0.634 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.597 to 0.669 s | 0.635 s |
| Kāra (`karac build`) | 0.605 to 0.672 s | 0.638 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.627 to 0.735 s | 0.650 s |
| Go | 1.039 to 1.110 s | 1.090 s |
| Python | 11.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.609 s) is not above its real time (0.638 s).

The sequential Kāra program is 0.98x Rust under overflow checks and 1.25x
C.
