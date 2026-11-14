# 1548. The Most Similar Path in a Graph

We have `n` cities and `m` bi-directional `roads`, where `roads[i] = [a, b]`
connects city `a` with city `b`. Each city has a name of exactly three
upper-case English letters, given in `names`. Starting at any city, you can
reach any other city by the roads, so the graph is connected.

Given a `targetPath`, find a path in the graph of the same length with the
minimum edit distance to `targetPath`: the number of places where the
city's name differs from the target's name. Return the cities of such a
path, in order. A path is valid when every pair of consecutive cities is
joined by a road. If there are several answers, return any one.

```
n = 5, roads = [[0,2],[0,3],[1,2],[1,3],[1,4],[2,4]],
names = ["ATL","PEK","LAX","DXB","HND"],
targetPath = ["ATL","DXB","HND","LAX"]                 ->  [0,2,4,2]   (distance 1)

n = 4, roads = [[1,0],[2,0],[3,0],[2,1],[3,1],[3,2]],
names = ["ATL","PEK","LAX","DXB"],
targetPath = ["ABC","DEF","GHI","JKL","MNO","PQR","STU","VWX"]
                                                       ->  distance 8

n = 6, roads = [[0,1],[1,2],[2,3],[3,4],[4,5]],
names = ["ATL","PEK","LAX","ATL","DXB","HND"],
targetPath = ["ATL","DXB","HND","DXB","ATL","LAX","PEK"]
                                                       ->  [3,4,5,4,3,2,1]   (distance 0)
```

**Constraints:** `2 <= n <= 100`; `n - 1 <= m <= n(n - 1) / 2`; no road is
given twice; the graph is connected; `names[i]` and `targetPath[i]` are
three upper-case letters; `1 <= targetPath.length <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `most_similar.kara` ★ | a DP over the target's places: `cost[t][v]` is the least distance of a path for the first `t + 1` names that ends in city `v`, its own mismatch plus the cheapest neighbour one place back, which `from[t][v]` remembers; the path is walked back from the cheapest last city. O(T m) |
| `most_similar_memo.kara` | the recurrence asked from the other end: `rest(t, v)`, the least distance from place `t` on standing in city `v`, kept in a `Map[(i64, i64), i64]`; the path is walked forward by `min_by_key` over the neighbours, the closure recursing with the memo borrowed `mut`. O(T m) |
| `most_similar_dijkstra.kara` | shortest paths over the layered graph of (place, city) states, each step costing the next city's mismatch: Dijkstra from every city at place 0 by a `PriorityQueue` (smallest first), `Map`s of the best cost and the parent of each state, a `Set` of settled ones, and a `while let` on `pop`; the first state popped at the last place ends a best path. O(T m log(T n)) |
| `most_similar_solution.kara` | LeetCode's Rust template (`most_similar(n: i32, roads: Vec<Vec<i32>>, names: Vec<String>, target_path: Vec<String>) -> Vec<i32>`, the ★ arm with `i32` distances), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

The answer is not unique, and the arms break ties differently, so every
arm's path goes through one judge: it checks the path has the target's
length and follows the roads, and counts its distance, -1 when it is no
path. Every arm prints the same 9 lines: LeetCode's three examples, then
two cities against an alternating target, a line of 100 cities against its
names backwards, and a star whose target wants two leaves in a row; then
checksums of the distances, and the count of answers that are not paths,
for 3000 random connected graphs of up to 6 cities with targets of up to
8, 300 of up to 30 with targets of up to 30 and 30 of up to 100 with
targets of up to 100. `most_similar.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every walk along the roads as long as the target, the least
number of places where its city's name is not the target's. It checks
3000 connected graphs of 2 to 6 cities named from 1 to 3 names, each with
a target of 1 to 6 names from one more name, every random choice drawn
before any arm answers. An arm's answer is the distance its path reaches.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is from 0 to the target's length, so the path is a path |
| P3 | the target backwards leaves the answer |
| P4 | the cities numbered backwards, roads and names with them, leave the answer |
| P5 | every name spelled backwards, in the graph and in the target, leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 56699431, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends; M6 by a crash, an integer overflow
(a city with no road out adds a mismatch to `i64.MAX`), under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first place's mismatch inverted | P1 815, P3 685, P4 69, P6 815 |
| M2 | ★: each city remembers itself, not its neighbour | P1 2511, P2 2511, P6 2511 |
| M3 | ★: the most expensive last city taken | P1 1293, P3 437, P6 1293 |
| M4 | memo: the recursion stopping one place early | P1 123, P3 220, P4 171, P6 123 |
| M5 | memo: the forward walk asking one place back | P1 598, P3 505, P4 218, P6 598 |
| M6 | memo: roads one way only | integer overflow |
| M7 | dijkstra: a step charged the mismatch of the place it leaves | P1 884, P3 617, P4 430, P6 884 |
| M8 | dijkstra: the starting states queued at cost 0 | P1 400, P3 409, P4 407, P6 400 |
| M9 | template: each place compared with the target one place back | P1 886, P3 618, P4 384, P6 886 |
| M10 | template: the walk back stopping before the first place | P1 1543, P2 1402, P3 703, P4 897, P6 1543 |

## Benchmarks

The bench builds 100 connected graphs of 50 to 100 cities once, each
named from its own first 1 to 26 names and given up to `4n` extra roads,
with a target of 100 names, and asks each 20 times by the ★ arm, in all
five languages. Every call builds its neighbour lists and both tables;
Kāra, Rust, Go and Python build them as nested vectors, C as flat heap
arrays with the neighbours in one array indexed by city. Every
implementation prints `20 passes over 100 graphs of up to 100 cities:
distance 69060, checksum 39598166`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.330 s |
| Rust (`rustc -O`) | 0.443 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.448 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.458 s |
| Kāra (`karac build`) | 0.460 s |
| Go | 0.586 s |
| Python | 5.8 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.44 s and 0.45 s on one run).

Kāra is 0.98x Rust under overflow checks by median. Not traced. The inner
loop is a string compare per city and a load, add and compare per road,
and C's lead is likely its flat tables, one allocation each instead of a
hundred rows.

## Verification

All four arms print the same output as `most_similar.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, memo and Dijkstra arms were written in Kāra and checked as
written. The shared harness took one edit from `karac fix` that
`karac check` does not report: `for place in [676, 26, 1].iter()` to
`for place in [676, 26, 1]`. The differential took one, from a parse
error that names it: the closure `|s: String| -> String { .. }` to
`let spelled: Fn(String) -> String = |s: String| { .. }`.

The Rust template took five rounds of `karac fix`:

1. the `Vec<..>` types to `Vec[..]`, `for r in &roads` and
   `for &u in &adj[v]` to `for r in ref roads` and `for u in ref adj[v]`,
   `i32::MAX` to `i32.MAX`, the wrapper's `|&(a, b)|` and `|&v|` patterns
   to `|(a, b)|` and `|v|`, and `Solution::` to `Solution.`;
2. `struct Solution {}` added;
3. `let n = n as usize` to `n as i64` with every `as usize` index to
   `as i64`, the inner `vec![]` to `Vec.new()`, the `dp` row and `path` to
   `Vec.filled`, `vec![0usize; n]` to `vec![0; n]`, the wrapper's
   `vec![a as i32, b as i32]` to a list literal, and `let cost: i32`
   annotated;
4. the remaining outer `vec![..; n]`s to `Vec.filled`, and the index casts
   dropped (an `i32` widens), except the first `push`'s `r[1] as i64`,
   which fixes the neighbour lists' type;
5. the last outer `vec![..; m]` to `Vec.filled`.

It checks and agrees with no hand edit.
