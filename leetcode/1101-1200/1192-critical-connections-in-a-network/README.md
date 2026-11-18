# 1192. Critical Connections in a Network

There are `n` servers numbered from `0` to `n - 1` connected by undirected
server-to-server `connections` forming a network, where `connections[i] =
[a, b]` represents a connection between servers `a` and `b`. Any server can
reach other servers directly or indirectly through the network. A critical
connection is a connection that, if removed, will make some servers unable
to reach some other server. Return all critical connections in the network
in any order.

```
n = 4, connections = [[0, 1], [1, 2], [2, 0], [1, 3]]  ->  [[1, 3]]
n = 2, connections = [[0, 1]]                          ->  [[0, 1]]
```

**Constraints:** `2 <= n <= 10^5`, `n - 1 <= connections.length <= 10^5`,
`0 <= a, b <= n - 1`, `a != b`, there are no repeated connections.

The arms are `fn critical_connections(n: i64, connections: Vec[Vec[i64]])
-> Vec[Vec[i64]]`. The two Rust arms keep the method LeetCode gives Rust
users, over `i32`, inside `impl Solution`, and a one-line
`critical_connections` converts the values and calls it. The answer's order
is free, so the harness prints each connection with its smaller server
first and the list sorted.

## Approaches

A connection is critical exactly when it lies on no cycle. A depth-first
search finds that in one pass: a connection from a server to a child it
discovered is critical when nothing in the child's subtree has a
connection back to the server or above it.

| file | mechanism |
|---|---|
| `critical_connections.kara` ★ | Tarjan's low-link search, iterative: each server's discovery time and the earliest time its subtree reaches back to, a frame per server on an explicit stack, so a path of 10^5 servers needs no deep call stack. O(n + e) |
| `critical_connections_recursive.kara` | the same search as it is usually written, recursive, its state in a struct passed `mut ref`. O(n + e), the call stack as deep as the search tree |
| `critical_connections_cover.kara` | a spanning tree by breadth-first search; every other connection covers the tree path between its ends, walked up from the deeper end with a union-find skipping covered connections, and a tree connection left uncovered is critical. O((n + e) α(n)) |
| `critical_connections_solution.kara` | a Rust solution as LeetCode's Rust users write it (a nested `fn dfs` taking the graph and five `&mut` arguments, `usize::MAX` as the root's parent), carried to Kāra by `karac fix` |
| `critical_connections_struct.kara` | another Rust solution, the search's state in a `Tarjan` struct with a recursive `fn dfs(&mut self, u: usize, parent: Option<usize>)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six more properties |

Every arm prints the same 11 lines: LeetCode's two examples; a path (every
connection critical); a cycle (none); two triangles joined by one
connection; a star; a cycle with a tail; 2000 random networks of 2 to 9
servers (`2000 random networks: 4160 critical, checksum 214967077`); and
the constraints' largest, a path of 10^5 servers (`path of 100000: 99999
critical, checksum 963752685`), a cycle of 10^5 (`cycle of 100000: 0
critical`), and 5 · 10^4 servers with 99,996 random connections (`18098
critical, checksum 346241758`). `critical_connections.py` mirrors the ★
arm and its output is byte-identical; it also checks every small network
against the statement read literally. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer build;
the recursive arms run the path of 10^5 servers 10^5 calls deep under all
four.

The Mend loop: the ★, recursive and cover arms check clean as written. The
solution arm takes one round of 66 fixes (among them the nested `fn dfs`
moved above the `impl`, since a nested `fn` captures nothing; `&Vec<..>`
parameters to bare ones and `&mut Vec<i32>` to `mut ref Vec[i32]`; `&mut
disc` arguments to `mut disc`; `for &v in &graph[u]` to `for v in ref
graph[u]`; `usize::MAX` to `i64.MAX`; and every `as usize` to `as i64` or
dropped) and its output matches. The struct arm takes one round of 44
(among them `&mut self` to `mut ref self`, `Option<usize>` to
`Option[i64]`, and `vec![0; n]` to `Vec.filled(n, 0)`) and its output
matches. No gap was found.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a connection is critical when, without it, some server cannot
reach server 0. 2000 random networks of 2 to 9 servers drawn as the
harness draws them, a random tree and then up to `n` more connections; the
first 200 are trees alone.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | each one is a connection of the network, and none comes twice |
| P3 | at most one fewer than the servers |
| P4 | the servers numbered backwards give the same connections, renumbered |
| P5 | the connections listed backwards give the same answer |
| P6 | one more connection, between two servers not yet joined, makes no connection critical that was not |
| P7 | the ★ arm's answer |

All 70,000 checks pass on every arm: `2000 networks: checksum 68680734,
70000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a child that reaches back exactly to its parent counted critical | P1 1057, P4 874, P5 1057, P7 4228 |
| S2 | ★: a child's reach not passed to its parent | P1 1057, P4 843, P5 1057, P6 69, P7 4228 |
| R1 | recursive: a connection back to a visited server ignored | P1 1057, P4 800, P5 1057, P6 396, P7 1057 |
| R2 | recursive: the connection a server was entered by taken as a way back | P1 1710, P7 1710 |
| W1 | cover: no connection kept as the tree's | P1 1710, P7 1710 |
| W2 | cover: the covered tree connections reported | P1 2000, P4 924, P5 599, P6 672, P7 2000 |
| X1 | solution: the parent taken as a way back | P1 1710, P7 1710 |
| X2 | solution: a child's reach not passed to its parent | P1 1057, P4 843, P5 1057, P6 69, P7 1057 |
| T1 | struct: a way back reaching one later than it does | P1 1057, P4 874, P5 1057, P7 1057 |
| T2 | struct: a child's reach compared with its parent's reach | P1 159, P4 218, P5 191, P6 40, P7 159 |

A mutation of the ★ arm fails P7 on every arm. R2, W1 and X1 report no
connection at all, so they fail on exactly the 1710 networks with one
critical connection or more, and only P1 and P7 see it: an empty answer
holds every other property. S2 and X2 are one fault in two arms and fail
alike. For S1, S2, R1, X2 and T1, P5 fails as often as P1 (1057 each):
the order the connections are listed picks the search tree, and these
faults' wrong answers change with the tree. T2 is the weakest catch, 159
failures: a reach compared with the parent's reach so far goes wrong only
when the parent already reaches above itself, by an earlier child or
connection, and the child's subtree reaches back to the parent alone.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 4 networks of LeetCode's largest size, built once (5 * 10^4
servers with 10^5 random connections, a random tree of 10^5 servers, a
path of 10^5 and a cycle of 10^5); then 10 rounds over the networks, the
critical connections folded into a checksum in the order the search
finds them. Every program prints `10 rounds of 4 networks of up to
100000 servers: checksum 441603685`. Each call builds the adjacency
lists, the discovery and low-link arrays and an explicit stack.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.513 to 0.731 s | 0.601 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.509 to 0.664 s | 0.573 s |
| Rust (`rustc -O`) | 0.615 to 0.746 s | 0.679 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.610 to 0.814 s | 0.683 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.619 to 0.841 s | 0.649 s |
| C (`clang -O3`) | 0.461 to 0.629 s | 0.498 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.455 to 0.564 s | 0.510 s |
| Go | 0.972 to 1.236 s | 1.040 s |
| Python | 12.28 to 12.93 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 16% ahead of Rust with overflow checks on (0.573 s
against 0.683 s) and of plain Rust; C is about 13% ahead of Kāra, and Go
takes about 1.8x Kāra's time. The ranges of Kāra, Rust and C overlap, so
only Go's gap stands out of the noise; no profile was taken. Python
takes about 22x Kāra's time.
