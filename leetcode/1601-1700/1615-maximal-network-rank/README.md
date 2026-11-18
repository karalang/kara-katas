# 1615. Maximal Network Rank

There is an infrastructure of `n` cities with some number of `roads`
connecting these cities. Each `roads[i] = [ai, bi]` indicates that there
is a bidirectional road between cities `ai` and `bi`.

The **network rank** of **two different cities** is defined as the total
number of **directly** connected roads to **either** city. If a road is
directly connected to both cities, it is only counted **once**.

The **maximal network rank** of the infrastructure is the **maximum
network rank** of all pairs of different cities.

Given the integer `n` and the array `roads`, return *the* ***maximal
network rank*** *of the entire infrastructure*.

```
n = 4, roads = [[0,1],[0,3],[1,2],[1,3]]              ->  4
n = 5, roads = [[0,1],[0,3],[1,2],[1,3],[2,3],[2,4]]  ->  5
n = 8, roads = [[0,1],[1,2],[2,3],[2,4],[5,6],[5,7]]  ->  5
```

**Constraints:** `2 <= n <= 100`; `0 <= roads.length <= n * (n - 1) / 2`;
`roads[i].length == 2`; `0 <= ai, bi <= n-1`; `ai != bi`; each pair of
cities has **at most one** road connecting them.

## Approaches

A pair's rank is its two degrees added, less one when a road joins the
two, since that road was counted from both ends.

| file | mechanism |
|---|---|
| `rank.kara` ★ | each city's degree in a `Vec.filled`, and a table of joined pairs in a `Vec.filled(n, Vec.filled(n, false))`; then every pair's rank. O(n^2 + roads) |
| `rank_top.kara` | only the cities of the two highest degrees: if two or more share the top degree the answer is twice it, less one only when every pair of them is joined; otherwise the top city with one of the second degree, less one only when it is joined to all of them. The roads in a `Set[(i32, i32)]`, read by a closure. O(n + roads) beside the pairs among the top cities |
| `rank_pairs.kara` | every pair, from a `flat_map` over `(0..n)`, counted afresh: the roads that touch either city, by `filter(..).count()`. O(n^2 * roads) |
| `rank_solution.kara` | LeetCode's Rust template (`vec![vec![false; n]; n]`, `as usize` indices, `adj[i][j] as i32` taken off the sum), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (two cities and no road, two cities and their road, and a star),
then the roads, the highest rank and a checksum for 3000 networks of up
to 6 cities and 8 roads, 300 of up to 40 cities and 600 roads, and 30 of
up to 100 cities and 50 roads. `rank.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each ordered pair of different cities, the set of roads
that touch either city, so a road at both counts once, and the largest
set. It checks 3000 networks of 2 to 7 cities with any number of distinct
roads, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the cities numbered backwards leave the answer |
| P3 | the roads listed backwards, each turned round, leave the answer |
| P4 | one more city, with no road, leaves the answer |
| P5 | the answer is the two highest degrees added, or one less |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 927167631, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3, M4 and M6 are the ones P5 cannot
see: each gives the two highest degrees added or one less, just not the
right one of the two.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a road marked joined one way only | P1 1457, P2 1320, P3 1320, P6 1457 |
| M2 | ★: no pair of neighbouring numbers tried | P1 448, P4 254, P5 392, P6 448 |
| M3 | ★: a shared road counted twice | P1 2148, P6 2148 |
| M4 | top: a pair of top cities not joined given one less | P1 755, P6 755 |
| M5 | top: the second degree allowed to equal the top | P1 693, P5 73, P6 693 |
| M6 | top: one less unless no second city is joined, not unless one is not | P1 97, P6 97 |
| M7 | pairs: a road ending at the second city not counted | P1 842, P2 732, P3 656, P4 2, P5 704, P6 842 |
| M8 | pairs: each city paired with itself | P1 1690, P2 289, P4 125, P5 1604, P6 1690 |
| M9 | template: a road's second city not given its degree | P1 1941, P3 560, P4 286, P5 1859, P6 1941 |
| M10 | template: each city paired with itself too | P1 2245, P5 782, P6 2245 |

## Benchmarks

The bench makes 2000 networks of 100 cities, each pair joined with chance 1/4, all of it first. Then: degrees and a joined table, then every pair. Every implementation prints `2000 networks of 100 cities: 2474735 roads, checksum 281335568`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.050 s |
| Go | 0.103 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.187 s |
| Kāra (`karac build`) | 0.191 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.193 s |
| Rust (`rustc -O`) | 0.194 s |
| Python | 2.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.147 s and 0.199 s on one run).

## Verification

All four arms print the same output as `rank.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`, and again at `428299b56e` after the bench's `let n = 100` was restored.

## Writing it

The ★ arm wrote `let mut best = 0`, kept by `max` and returned as `i32`,
and `karac fix` typed it `let mut best: i32 = 0`. The top arm compared a
copied `i32` as `*c != first`, and `karac fix` took the `*` off. The
pairs arm wrote Rust's `map(move |b| (a, b))`, and `karac fix` deleted
the `move`, since a Kāra closure's captures are inferred. The
differential wrote `let n = *n` for a copied `i32`, and `karac fix` took
the `*` off.

The bench's harness wrote `let n = 100`, ran `for a in 0..n` and passed
`n` to the `i32` parameter, and the call was refused: `n` is an `i64`
because its literal kept the default. By design.md §8 an argument fixes
a literal's type and a literal defaults only at the end of the body, so
the `for` range's end should not settle it first; it does even with
`println(a)` as the loop's only body (B-2026-11-18-13). That was fixed at
kara e05a5afee6, and the bench now writes `let n = 100` as it was first
written.

The Rust template took one `karac fix` of 13 edits: `struct Solution;`
to `struct Solution {}`, the `<..>` types to `[..]`, every `as usize` to
`as i64`, `vec![0; n]` to `Vec.filled(n, 0i32)`,
`vec![vec![false; n]; n]` to `Vec.filled(n, Vec.filled(n, false))`,
`let mut ans = 0` typed `i32`, and `Solution::` to `Solution.`. It then
checks and agrees with no hand edit.
