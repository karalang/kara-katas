# 1606. Find Servers That Handled Most Number of Requests

You have `k` servers numbered from `0` to `k-1` that are being used to
handle multiple requests simultaneously. Each server has infinite
computational capacity but **cannot handle more than one request at a
time**. The requests are assigned to servers according to a specific
algorithm:

- The `i`th (0-indexed) request arrives.
- If all servers are busy, the request is dropped (not handled at all).
- If the `(i % k)`th server is available, assign the request to that
  server.
- Otherwise, assign the request to the next available server (wrapping
  around the list of servers and starting from 0 if necessary). For
  example, if the `i`th server is busy, try to assign the request to the
  `(i+1)`th server, then the `(i+2)`th server, and so on.

You are given a **strictly increasing** array `arrival` of positive
integers, where `arrival[i]` represents the arrival time of the `i`th
request, and another array `load`, where `load[i]` represents the load
of the `i`th request (the time it takes to complete). Your goal is to
find the **busiest server(s)**. A server is considered **busiest** if it
handled the most number of requests successfully among all the servers.

Return *a list containing the IDs (0-indexed) of the* ***busiest
server(s)***. You may return the IDs in any order.

```
k = 3, arrival = [1,2,3,4,5], load = [5,2,3,3,3]  ->  [1]
k = 3, arrival = [1,2,3,4],   load = [1,2,1,2]    ->  [0]
k = 3, arrival = [1,2,3],     load = [10,12,11]   ->  [0,1,2]
```

**Constraints:** `1 <= k <= 10^5`;
`1 <= arrival.length, load.length <= 10^5`;
`arrival.length == load.length`;
`1 <= arrival[i], load[i] <= 10^9`;
`arrival` is **strictly increasing**.

## Approaches

A server busy until time `t` is free for a request arriving at `t`.
Every arm returns the busiest servers in increasing order.

| file | mechanism |
|---|---|
| `servers.kara` ★ | the free servers in a `SortedSet[i32]`, the first at or after `i % k` found as `free.range(start, k).next().or(free.min())`; the busy ones in a `PriorityQueue[(i64, i32)]` of (time free, server), given back to the set as each request arrives. O(n log k) |
| `servers_scan.kara` | each server's next free time in a `Vec[i64]`, scanned from `i % k` round the circle for the first free one. O(n k) |
| `servers_heaps.kara` | two heaps: the free servers in a `PriorityQueue[i64]` too, each keyed by the request number at which its turn comes round, `i + (s - i).rem_euclid(k)`, so the smallest key is the first free server at or after `i % k`, and the server is the key mod `k`. O(n log k) |
| `servers_solution.kara` | LeetCode's Rust template (`BTreeSet<usize>` searched by `range(i % k..)`, `BinaryHeap<Reverse<..>>`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one server, every request dropped but the first, and requests that
each wrap past the last server), then the request count, the busiest
count and a checksum of the answers for 3000 problems of up to 4 servers
and 10 requests, 300 of up to 100 servers and 3000 requests, and 3 of up
to 1000 servers and 100000 requests. `servers.py` mirrors the ★ arm
(`bisect` on a sorted list, `heapq`) and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each request walks the servers from `i % k` round the circle,
one at a time, and takes the first whose last request has finished. It
checks 3000 problems of 1 to 4 servers and 1 to 10 requests, each
arriving 1 to 3 after the one before and lasting 1 to 8, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every arrival 100 later leaves the answer |
| P3 | every arrival and every load doubled leaves the answer |
| P4 | a request of load 1 added after every server is free goes to server n mod k: the answer becomes that server alone if it was busiest, and otherwise stays or gains it |
| P5 | the requests spread so none overlaps go round the circle: the busiest are the first n mod k servers, or all when k divides n |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 17233912, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M3, M4 and M7 are the ones P4 and P5
miss: when no two requests overlap, when a server counts as free, or
whether it was taken out of the free set, changes nothing.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a server busy until `t` not yet free at `t` | P1 488, P6 488 |
| M2 | ★: always the smallest free server | P1 958, P4 561, P5 1341, P6 958 |
| M3 | ★: the server taken left in the free set | P1 616, P6 616 |
| M4 | scan: a server busy until `t` not yet free at `t` | P1 488, P6 488 |
| M5 | scan: the walk starting one server late | P1 1627, P4 1941, P5 1517, P6 1627 |
| M6 | heaps: a freed server keyed by its number, not its turn | P1 958, P4 561, P5 1341, P6 958 |
| M7 | heaps: each server freed one tick early | P1 412, P3 412, P6 412 |
| M8 | template: only the first busiest server returned | P1 1218, P4 301, P5 1341, P6 1218 |
| M9 | template: each odd server counted twice | P1 1784, P4 250, P5 2008, P6 1784 |
| M10 | ★: the search starting at `(i + 1) % k` | P1 1627, P4 1941, P5 1517, P6 1627 |

## Benchmarks

The bench makes 20 problems of 10000 servers and 100000 requests, all of it first. Then: free servers in an ordered set (C/Go: segment tree), busy in a min-heap. Every implementation prints `20 problems of 10000 servers and 100000 requests: 45 busiest, checksum 854878309`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.370 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.379 s |
| C (`clang -O3`) | 0.414 s |
| Go | 0.483 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.618 s |
| Kāra (`karac build`) | 0.649 s |
| Python | 3.5 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.604 s and 0.605 s on one run).

## Verification

All four arms print the same output as `servers.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The ★, scan and heaps arms were written in Kāra and checked as written.
The differential's harness wrote `let mut t = 0` for an arrival time
pushed as `i32`, and `karac fix` typed it `let mut t: i32 = 0`.

The Rust template took one `karac fix` of 28 edits: the `use` lines
dropped, `struct Solution;` to `struct Solution {}`, the `<..>` types to
`[..]`, `usize` to `i64` throughout (`k as usize` became `k as i64`),
`BTreeSet` to `SortedSet`, `BinaryHeap::new()` to `PriorityQueue.new()`
with every `Reverse(..)` taken off since a `PriorityQueue` is smallest
first, `busy.peek()` matched by `Some(&Reverse((end, s)))` to
`busy.peek().cloned()` matched by `Some((end, s))`,
`free.range(i % k..)` to `free.range_inclusive(i % k, i64.MAX)`,
`Some(&s)` to `Some(s)`, `free.remove(&s)` to `free.remove(s)`, the
`as i64` on `load[i]` dropped, `vec![0; k]` to `Vec.filled(k, 0)`, the
`|&i|` closure pattern to `|i|`, and `Solution::` to `Solution.`. It then
checks and agrees with no hand edit.
