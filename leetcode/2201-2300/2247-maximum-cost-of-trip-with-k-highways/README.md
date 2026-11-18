# 2247. Maximum Cost of Trip With K Highways

A series of highways connect `n` cities numbered from `0` to `n - 1`.
You are given a 2D integer array `highways` where `highways[i] =
[city1_i, city2_i, toll_i]` indicates that there is a highway that
connects `city1_i` and `city2_i`, allowing a car to go from `city1_i` to
`city2_i` **and vice versa** for a cost of `toll_i`.

You are also given an integer `k`. You are going on a trip that crosses
**exactly** `k` highways. You may start at any city, but you may only
visit each city **at most** once during your trip.

Return *the **maximum** cost of your trip. If there is no trip that
meets the requirements, return* `-1`.

```
n = 5, highways = [[0,1,4],[2,1,3],[1,4,11],[3,2,3],[3,4,2]], k = 3  ->  17
n = 4, highways = [[0,1,3],[2,3,2]], k = 2                           ->  -1
```

**Constraints:** `2 <= n <= 15`; `1 <= highways.length <= 50`;
`highways[i].length == 3`; `0 <= city1_i, city2_i <= n - 1`;
`city1_i != city2_i`; `0 <= toll_i <= 100`; `1 <= k <= 50`; there are
no duplicate highways.

A trip of `k` highways visits `k + 1` distinct cities, so it is
impossible when `k + 1 > n`. Otherwise the cities a trip has used and
the city it stands in are all that matter for how it can go on, so the
dearest trip to each (set of cities, city) pair is enough: 2^n * n
states, each extended by the highways out of its city.
O(2^n * (n + m)).

## Approaches

| file | mechanism |
|---|---|
| `trip.kara` ★ | `best[mask][v]`, the dearest trip that visits exactly the cities of `mask` and ends at `v`, -1 where there is none; the masks in increasing order, since a trip only grows into larger masks; the answer the dearest over masks of `k + 1` cities, by `count_ones` |
| `trip_memo.kara` | top-down: a recursive `go` answers the dearest way to drive `left` more highways from a city, remembered in `memo[mask][v]` (`mut ref`), since `left` follows from the mask's size; -2 marks not yet known |
| `trip_layers.kara` | layer by layer: a `Map[(i64, i64), i64]` from (cities used, city at) to the dearest trip there, every city alone at first, then `k` rounds each driving every trip one highway further; only trips that can still grow are kept |
| `trip_struct.kara` | a `#[derive(Copy, Clone)] struct Road` and a `struct Planner` of the roads, an `Option[i64]` per state (`None` for unreached) and the masks grouped by size; `Planner.new`, `drive` (`mut ref self`) for one size, and `dearest` (`ref self`) |
| `trip_iter.kara` | iterator chains: the roads by `flat_map` over both directions and `fold`; each mask's steps by `filter` and `flat_map` / `filter_map`, collected and then written into the table; the answer by `filter`, `flat_map` and `max` |
| `trip_solution.kara` | LeetCode's Rust template: `i32`, `Vec<Vec<i32>>` and `i32` in, `i32` out, `vec![vec![i32::MIN; n]; 1 << n]` over `1usize << n` masks, `mask.count_ones()` and `mask >> v & 1`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more (one highway, a trip longer than the cities allow, a triangle
whose dearest two highways are not the first two, and a path of free
highways walked whole), each with its answer; then how many of 2000
trips of 2 to 7 cities, any number of highways and `k` from 1 to 7 are
possible, with a checksum of the answers; then the constraints'
largest, 15 cities and 50 highways, with `k = 14` and `k = 50`.
`trip.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 27 edits: `Vec<..>` to
`Vec[..]`, `usize` to `i64` (`n as i64`, `h[0] as i64`, and `1usize <<
n` to `1 << n`), `vec![vec![]; n]` and `vec![vec![i32::MIN; n]; 1 << n]`
to `Vec.filled(..)`, `i32::MIN` to `i32.MIN`, `for h in &highways` and
`for &(v, c) in &g[u]` to `for h in ref highways` and `for (v, c) in ref
g[u]`, `let mut ans = -1` typed `i32`, `struct Solution;` to `struct
Solution {}`, `Solution::` to `Solution.`, the `&` pattern dropped from
the adapter's closure, and its `as i64` removed as lossless.

The iter arm reads the table inside a closure that `flat_map` returns,
and a returned closure takes its captures by move (core-semantics.md
§9.3), so `karac check` asks for a borrow before the statement. The arm
names that borrow `reached`. `karac fix` offers `let best = ref best;`
instead, which shadows the table for the rest of the loop body, where
the steps are written back into it, and the next check refuses the
write (`best` is a shared `ref`); that fix is a compiler gap, recorded
in the kara ledger (B-2026-11-17-150).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of `k + 1` distinct cities tried, from every
start, kept when each is joined to the next by a highway, and the
dearest sum of tolls taken, or -1; no table. It checks 300 random trips
of 2 to 6 cities, any number of highways and `k` from 1 to 6; then 30
with every toll 0; then 30 complete maps with `k = n - 1`, every city on
the trip. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the dearest trip, read literally, or -1 |
| P2 | every highway written the other way round and the list reversed: the same answer |
| P3 | the cities renamed by a rotation: the same answer |
| P4 | every toll one higher: `k` more, or -1 again |
| P5 | one more highway: no lower answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 891448637, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`itertools.permutations` of `k + 1` cities with the tolls in a dict
keyed by unordered pairs. On a failure it prints the first ten and then
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
| M1 | ★: highways one way only | P1 85, P6 85 |
| M3 | ★: a used city driven to again | P1 95, P3 60, P4 103, P6 95 |
| M6 | ★: the answer the last trip found | P1 82, P3 92, P5 9, P6 82 |
| M8 | memo: the memo read by the city alone | P1 102, P3 74, P4 98, P6 102 |
| M9 | memo: a used city driven to again | P1 130, P2 22, P3 15, P4 28, P6 130 |
| M11 | memo: trips from city 0 only | P1 85, P3 94, P6 85 |
| M13 | layers: a cheaper trip written over a dearer one | P1 72, P5 23, P6 72 |
| M15 | layers: the trip kept at its old city | P1 66, P6 66 |
| M16 | layers: the rounds merged, not replaced | P1 31, P4 31, P6 31 |
| M18 | struct: a trip never made dearer | P1 41, P3 39, P5 9, P6 41 |
| M19 | struct: the answer read off trips of k cities | P1 175, P4 192, P6 175 |
| M21 | struct: the cheapest trip answered | P1 127, P5 23, P6 127 |
| M22 | iter: trips of k cities not extended | P1 176, P6 176 |
| M25 | iter: the toll not added | P1 160, P4 176, P6 160 |
| M26 | iter: a step written over, not raised | P1 39, P3 41, P5 11, P6 39 |
| M30 | solution: the toll read from the first city | P1 175, P2 176, P3 129, P4 176, P6 175 |
| M31 | solution: the answer begun at 0 | P1 29, P4 29, P6 29 |

P1 and P6 kill all seventeen, P3 and P4 eight each, P5 five and P2 two.
P3 renames the cities, and catches the edits whose answer depends on
which city is which: the trips from city 0 only (M11), the last trip
found (M6), and the steps that overwrite or revisit. P4 raises every
toll, which moves the answer by exactly `k` only when the trip has `k`
highways and every toll is counted once. P5 catches the edits that keep
the cheaper of two trips, since a new highway can then lower the
answer. P2 changes nothing but the order and direction the highways are
written in, and catches only the memo arm's revisits (M9) and the
template reading the toll from the city column (M30).

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Twelve fail as a kept one does: a trip
of `k` cities, or one round too few, in the ★, layers, iter and
template arms (M2, M12, M24, M28) as the struct arm's answer read off
trips of `k` cities (M19); the ★ and memo arms' toll not added (M4,
M10) as the iter arm's (M25); the ★ arm's trips begun at a toll of 1,
the memo arm's no highways left answered -1, the struct arm's last size
not driven, and the template's only used cities driven to (M5, M7,
M20, M29) as the iter arm's trips of `k` cities not extended (M22),
since all of them answer -1 or one more for every possible trip; and
the struct and iter arms' highways one way only (M17, M23) as the ★
arm's (M1). Two fail their own way and are left out for the count of
three or two: the layers arm's used city driven to again (M14) and the
template's table begun at 0 (M27). Two first tries were replaced: the ★
arm's cheaper way kept failed as M22 does, and the template's table
begun at an untyped `0` was refused by the type checker (`dp` holds
`i32`).

## Verification

Every arm prints the same output as `trip.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, memo and template arms take 1.0 s to
1.1 s, the struct arm 1.8 s, the layers arm 2.2 s, the iter arm 4.0 s,
and the differential 1.9 s.

## Benchmarks

The bench answers 16 maps of 15 cities with the ★ arm in all five
languages: 50 of the 105 possible highways, drawn by a shuffle, tolls 0
to 100, and every trip of 14 highways, so all 2^15 masks are worked. C
keeps the roads in one array by offsets (CSR); the others keep a list
per city. Every implementation prints `16 maps of 15 cities: checksum
484284898`.

BENCHTAB
