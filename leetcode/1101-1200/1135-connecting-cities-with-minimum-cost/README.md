# 1135. Connecting Cities With Minimum Cost

There are `n` cities labeled from `1` to `n`. You are given the integer
`n` and an array `connections` where `connections[i] = [xi, yi, costi]`
indicates that the cost of connecting city `xi` and city `yi`
(bidirectional connection) is `costi`.

Return the minimum cost to connect all the `n` cities such that there is
at least one path between each pair of cities. If it is impossible to
connect all the `n` cities, return `-1`.

The cost is the sum of the connections' costs used.

```
n = 3, connections = [[1,2,5],[1,3,6],[2,3,1]]  ->  6
n = 4, connections = [[1,2,3],[3,4,4]]          ->  -1
```

**Constraints:** `1 <= n <= 10^4`; `1 <= connections.length <= 10^4`;
`1 <= xi, yi <= n`; `xi != yi`; `0 <= costi <= 10^5`.

The arms are `fn minimum_cost(n: i64, connections: Vec[Vec[i64]]) -> i64`.

## Approaches

The answer is the weight of a minimum spanning tree, or -1 when the
roads leave the cities in more than one part.

| file | mechanism |
|---|---|
| `minimum_cost.kara` ★ | Kruskal's algorithm: the roads cloned and sorted by cost, and a road kept when it joins two parts, the parts kept in a union-find with path halving and union by size. O(m log m) |
| `minimum_cost_prim.kara` | Prim's algorithm: the network grown from city 1, a `PriorityQueue` of `(cost, city)` handing out the cheapest road to a city not yet reached, a city popped again passed over. O(m log m) |
| `minimum_cost_boruvka.kara` | Borůvka's algorithm: in each round every part finds its cheapest road out, ties going to the road listed first, and all of those that still join two parts are kept. O(m log n) |
| `minimum_cost_labels.kara` | Kruskal's algorithm with labels in place of a union-find: every city carries its part's label and every part a list of its cities, and a join relabels the smaller part. O(m log m + n log n) |
| `minimum_cost_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `UnionFind` struct of `Vec<usize>` with a recursive `find(&mut self)` and union by rank returning `bool`, `mut connections: Vec<Vec<i32>>` sorted with `sort_unstable_by_key`, an early return once `n - 1` roads are kept), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and six more (three roads between the same two cities, a ring
of equal costs, a dear hub beside cheap roads, two parts, a ring of
falling costs, and the dearest roads), then over 2000 random networks of
2 to 12 cities and 1 to 20 roads costing 1 to 20 the costs summed, how
many are not connected, and a checksum (`2000 random networks: costs
total 34398, 815 not connected, checksum 411847789`), and two of
LeetCode's largest: 10000 cities on a random tree and one more road
(`504781226`), and 1000 cities with 10000 random roads (`6223233`).
`minimum_cost.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of roads that connects all the cities, a set chosen
by the bits of a mask and connected when a walk from city 1 along it
reaches every city, and the least cost among them, or -1. It checks 2000
problems of 2 to 6 cities and up to 8 roads in five kinds of 400: costs
from 1 to 100; from 1 to 3, so many tie; all 5; a random tree with costs
to 20 and up to three roads more; and two parts with no road between
them. Every random choice, the renaming and the road P5 copies among
them, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the roads listed in reverse give the same answer |
| P3 | each road's two ends swapped give the same answer |
| P4 | every cost doubled doubles the answer, and -1 stays -1 |
| P5 | a dearer copy of one road, added at the front, changes nothing |
| P6 | the cities renamed by a drawn order give the same answer |

All 60,000 checks pass on every arm: `2000 problems: checksum
272792148, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, every set of roads tried and its connection checked
with a union-find rather than a walk, gives the same checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All thirty are caught. One edit
first tried in the Borůvka arm, a part joined through its road's first
city rather than the city's root, made a cycle of parents and hung both
backends; it was replaced by each join counted twice. Fifteen are kept,
no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the roads never sorted | P1 533, P2 661, P5 1126 |
| M2 | ★: a road of cost 1 always kept | P1 98, P4 98 |
| M3 | ★: the second end joined in place of its part | P1 412, P2 157, P3 503, P5 107 |
| M4 | prim: a city popped again counted again | P1 1035, P5 338, P6 70 |
| M5 | prim: each road one way only | P1 805, P3 799, P6 315 |
| M6 | prim: the dearest road out first | P1 722, P5 937 |
| M7 | boruvka: a road inside a part taken as a way out | P1 219, P2 69 |
| M8 | boruvka: only the first end's part looks out | P1 330, P2 18, P3 472, P6 202 |
| M9 | boruvka: two parts accepted | P1 468 |
| M10 | labels: a moved city keeps its old label | P1 1053, P2 1, P3 3, P5 454 |
| M11 | labels: the parts never counted down | P1 1135 |
| M12 | labels: an odd cost rounded down | P1 984, P4 984 |
| M13 | solution: equal ranks never joined | P1 566, P2 22, P3 88, P5 306 |
| M14 | solution: the roads sorted by their first city | P1 531, P2 430, P3 549, P5 855, P6 357 |
| M15 | solution: costs above 50 clipped to 50 | P1 111, P4 183 |

P1 catches all fifteen, P2 and P5 seven each, P3 six, P6 four and P4
three. P4 doubles every cost, so it sees only the edits that treat a
cost as something other than a weight to compare and add: a road of
cost 1 always kept (M2), an odd cost rounded down (M12), and costs
clipped (M15). P2 and P5 change which road comes first among equals and
put a dearer road ahead of its twin, so they see the edits that depend on
the roads' order: the roads unsorted or sorted by city (M1, M14), the
dearest road out first (M6), and joins that land on the wrong city
(M3, M10, M13). P3 and P6 see the edits that treat a road's two ends
apart or depend on the cities' numbers: each road one way only (M5),
only the first end's part looking out (M8), and the same wrong joins. A
rule that is wrong the same way on every listing and every naming, such
as two parts accepted (M9) or parts never counted down (M11), is seen by
P1 alone.

Of the fifteen not kept, six fail exactly as a kept one: one part too
many accepted in the ★ arm as M9; the joins counted from 0 in the ★
arm, and the queue told the city a road comes from in the Prim arm, as
M11; the dearest road out of each part in the Borůvka arm, and the
dearest roads first in the labels arm, as M6; and a single Borůvka round
as M7. The other nine fail each in a way of its own and were not needed.

## Verification

Every arm prints the same output as `minimum_cost.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no gap. The ★, Prim and labels arms were written as Kāra
and checked clean as written. The Borůvka arm first read a road as `let
road = connections[i]`, a move out of an index that Kāra refuses, and
`karac fix` made it `ref connections[i]` in one round, since the binding
is only read. `karac fix` carried the solution arm in five rounds:
`Vec<..>` to `Vec[..]`, `&mut self` to `mut ref self`, `mut connections`
to `connections: own Vec[..]` with a `let mut` rebinding, `::` to `.`,
and the `&v` pattern to `v`; then `struct Solution {}` declared; then
`vec![0; n]` to `Vec.filled(n, 0)`, `sort_unstable_by_key` to
`sort_by_key`, the cost declared `i32`, and the `as i64` at the call
dropped; then `usize` to `i64` through the `UnionFind` struct and its
methods; then the `as i64` casts at `union`'s arguments dropped, each an
`i32` widening by itself.

## Benchmarks

The bench builds 8 networks of 1000 cities and 10000 roads once,
LeetCode's largest road count, costs from 1 to 100000. Each of 50 rounds
changes one road's cost in every network and answers the network with
the ★ arm: 400 calls. Every implementation prints `50 rounds over 8
networks of 1000 cities and 10000 roads: costs total 2407044935,
checksum 35911899`. Each keeps every road as its own allocation of three
values (`Vec[i64]`, `Vec<i64>`, `[]int64`, a Python list, and C's
`int64_t *`), copies the roads one by one and sorts the copy in every
call, by the kata's convention with the language's own sort: Kāra's and
Rust's `sort_by_key`, C's `qsort` and Go's `sort.Slice`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `73ec8b248f`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.229 to 0.298 s | 0.253 s |
| Kāra (`karac build`) | 0.224 to 0.307 s | 0.254 s |
| Rust (`rustc -O`) | 0.258 to 0.357 s | 0.305 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.279 to 0.351 s | 0.306 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.257 to 0.380 s | 0.313 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.398 to 0.494 s | 0.456 s |
| C (`clang -O3`) | 0.404 to 0.510 s | 0.467 s |
| Go | 0.757 to 0.882 s | 0.787 s |
| Python | 2.480 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Most of each call is the copy and the sort of 10000 roads. C
takes about 1.85x Kāra's time: `qsort` calls its comparison through a
function pointer for every compare, and the copy is 10000 calls to
`malloc`. Rust takes about 1.2x Kāra's time, with or without overflow
checks; it clones and sorts the same way, and this README has not
measured where Kāra's lead over it comes from. Go takes about 3.1x
Kāra's time, its `sort.Slice` swapping through reflection. Python takes
about 9.8x Kāra's time.
