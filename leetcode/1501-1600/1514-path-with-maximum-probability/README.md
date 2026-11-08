# 1514. Path with Maximum Probability

You are given an undirected weighted graph of `n` nodes (0-indexed),
represented by an edge list where `edges[i] = [a, b]` is an undirected
edge connecting the nodes `a` and `b` with a probability of success of
traversing that edge `succProb[i]`. Given two nodes `start` and `end`,
find the path with the maximum probability of success to go from `start`
to `end` and return its success probability. If there is no path, return
0. Answers within `10^-5` of the correct one are accepted.

```
n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2  ->  0.25
n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2  ->  0.3
n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2                      ->  0.0
```

**Constraints:** `2 <= n <= 10^4`; `0 <= start, end < n`, `start != end`;
`0 <= a, b < n`, `a != b`; `0 <= succProb.length == edges.length <= 2 * 10^4`;
`0 <= succProb[i] <= 1`; at most one edge between every two nodes.

## Approaches

| file | mechanism |
|---|---|
| `chance.kara` ★ | Dijkstra for the largest product: every chance is at most 1, so a path's chance only falls as it grows, and the node with the largest chance found is final when it leaves a largest-first `PriorityQueue`. The queue holds `(F64, i64)`: `f64` has no order (NaN), and `F64` is the library's totally ordered float. O((n + m) log m) |
| `chance_bellman.kara` | Bellman-Ford: relax every edge both ways until a whole pass changes nothing. O(n m) at worst |
| `chance_spfa.kara` | a work queue (SPFA): a node whose chance rose goes back on a `VecDeque` to relax its edges, unless it is already waiting |
| `chance_dense.kara` | Dijkstra without a heap: each round settles the unsettled node with the largest chance, found by a scan. O(n^2 + m) |
| `chance_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>` edges, `vec![0.0f64; n as usize]`, `loop` with a `changed` flag), the Bellman-Ford arm, carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples and a chain
of ten at 0.9 each to five places, then a checksum of the answers, in
hundred-thousandths, for 2000 graphs of 2 to 8 nodes, 200 of 2 to 200,
and 3 of 2 to 10000, each with up to two edges per node and each edge's
chance a whole number of hundredths from 0.80 to 1. `chance.py` mirrors
the ★ arm and its output is byte-identical.

Every arm multiplies a path's chances in the same order, from `start`
out, so the same path gives the same `f64` in every arm and in Python,
and the arms are compared exactly.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every simple path from `start` to `end` walked by recursion,
the largest product kept. It checks 2000 graphs of 2 to 7 nodes, with up
to two edges per node and chances of 0.01 to 1. Every random choice of a
problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `start` and `end` swapped leave the answer to within `10^-12` |
| P3 | the edges listed backwards leave the answer |
| P4 | a new edge from `start` to `end` with chance `q` makes the answer the larger of the two |
| P5 | every chance set to 1 makes the answer 1 when it was above 0, and 0 when it was 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2000 problems: checksum 444086567, 60000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

P2 first compared the two answers rounded to five places, and failed on
2 of the 2000 graphs in all five arms alike: swapped, the product is
taken from the other end, rounds differently in the last bit, and those
two answers sat on a rounding boundary. The property now allows `10^-12`.

## Mutation testing

Eighteen edits to the differential, three to five to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept.
Thirteen are killed by a property and one by hanging, each the same way
under both backends; four survive, all equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each edge added one way only | P1 958, P2 1423, P6 958 |
| M2 | ★: a smallest-first queue | P1 627, P2 173, P3 661, P4 650, P6 627 |
| M3 | ★: each step's chance squared | P1 1538, P4 1387, P6 1538 |
| M4 | ★: a node improved only by 1% or more | P1 3, P2 1, P4 4, P6 3 |
| M5 | Bellman-Ford: one pass only | P1 357, P2 494, P3 494, P6 357 |
| M6 | Bellman-Ford: one way's chances raised to at least 0.5 | P1 335, P2 543, P3 75, P4 373, P6 335 |
| M7 | SPFA: chances capped at 0.9 | P1 396, P4 216, P5 1552, P6 396 |
| M8 | dense: the smallest chance settled first | P1 263, P2 73, P4 113, P6 263 |
| M9 | dense: a node settled as soon as it improves | P1 558, P6 558 |
| M10 | Rust: each edge read as a loop from its first node | P1 1552, P4 2000, P6 1552 |
| M11 | Rust: `start` begins at 0.9 | P1 1552, P4 1249, P5 1552, P6 1552 |
| M12 | Rust: an improvement taken only above 0.05 | P1 89, P2 148, P3 77, P4 96, P5 33, P6 89 |

P1 and P6 kill all twelve, P4 nine, P2 seven, P3 four, and P5 three. M4
is the faintest: a 1% bar loses only the rare graph whose best path wins
by less, 3 in 2000. M9 is seen only by P1 and P6: settling a node early
keeps the first chance it gets, which no symmetry of the graph exposes.

The other one killed by a property: the Bellman-Ford arm relaxing each
edge one way only (as M1). One hangs: the Rust arm's `if changed
{ break }`, which loops forever once nothing changes. Four survive and
are equivalent: the ★ arm skipping a stale entry only below half its
node's chance (more work, same answer), the SPFA arm never requeueing
`end` or `start` (no better path to `end` goes through `end`, and
`start` stays at 1), and the dense arm settling past `end`.

## Benchmarks

The bench builds 10 graphs of 50000 nodes and 100000 edges once, chances
from 0.80 to 1, and asks 5 random `start` to `end` questions of each by
the ★ arm in all five languages; Rust orders its heap entries by
`total_cmp`, C and Go hand-write theirs. Every implementation prints
`50 questions over 10 graphs of 50000 nodes: checksum 496251368` (the
answers in units of `10^-12`).

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `1dce193ad` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.670 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.858 s |
| Rust (`rustc -O`) | 0.860 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.00 s |
| Kāra (`karac build`) | 1.04 s |
| Go | 1.72 s |
| Python | 12.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.987 s and 1.023 s on one run).

Kāra is 1.17x Rust under overflow checks by median. Each question builds
its adjacency lists afresh, as LeetCode's signature asks, so the
allocation of 50000 small `Vec`s is part of every timing in every
language but C, which packs them into one array.

## Verification

All five arms print the same output as `chance.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.5 to 0.6 s, the dense arm 1.6 s,
and the differential 1.7 s.

## Writing it

The arms were written in Kāra and `karac fix` had nothing to change. A
first try at the ★ arm's queue as `PriorityQueue[(f64, i64)]` was refused
with "`(f64, i64)` does not implement `Ord`"; the same refusal for a bare
`f64` adds the note that names `F64`, but the tuple's does not. The Rust
arm took 11, 2, 1 and 1 `karac fix` edits, among them
`vec![0.0f64; n as usize]` to `Vec.filled(n as i64, 0.0)`, and checks.
