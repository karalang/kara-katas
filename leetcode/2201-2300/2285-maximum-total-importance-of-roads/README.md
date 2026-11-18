# 2285. Maximum Total Importance of Roads

You are given an integer `n` denoting the number of cities in a
country. The cities are numbered from `0` to `n - 1`.

You are also given a 2D integer array `roads` where
`roads[i] = [a_i, b_i]` denotes that there exists a **bidirectional**
road connecting cities `a_i` and `b_i`.

You need to assign each city with an integer value from `1` to `n`,
where each value can only be used **once**. The **importance** of a
road is then defined as the **sum** of the values of the two cities it
connects.

Return *the **maximum total importance** of all roads possible after
assigning the values optimally.*

```
n = 5, roads = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]  ->  43
n = 5, roads = [[0,3],[2,4],[1,3]]                    ->  20
```

**Constraints:** `2 <= n <= 5 * 10^4`; `1 <= roads.length <= 5 * 10^4`;
`roads[i].length == 2`; `0 <= a_i, b_i <= n - 1`; `a_i != b_i`; there
are no duplicate roads.

A city's value is counted once for each of its roads, so the total is
the sum of value times degree, and it is largest when the values go up
with the degrees (the rearrangement inequality): sort the degrees and
give the k-th smallest the value k. O(n log n + m). Which of several
cities of one degree takes which value does not change the total.

## Approaches

| file | mechanism |
|---|---|
| `importance.kara` ★ | `Vec.filled(n, 0)` of degrees over the roads, `sort`, then each degree times its place plus one by `enumerate` |
| `importance_naive.kara` | each city's degree by a walk of every road, then the values n down to 1 handed out each time to the unvalued city with the most roads, and the total summed road by road. O(n * m + n^2) |
| `importance_heap.kara` | the degrees into a `PriorityQueue.max_first()`, each pop valued one less than the last, from n |
| `importance_struct.kara` | `struct City` of an id and its roads, `sort_by_key` on the roads, each city valued by its place, the total summed road by road |
| `importance_iter.kara` | the degrees by `fold` over the roads, `sort`, then `zip(1..)`, `map` and `sum` |
| `importance_solution.kara` | LeetCode's Rust template: `n: i32` and `Vec<Vec<i32>>` in, `i64` out; `vec![0i64; n as usize]`, `sort_unstable`, then `enumerate().map(..).sum()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples, one road,
the complete graph on 50 cities (62475), a path through 5000 cities
(25004997); then 2000 random graphs of 2 to 30 cities and 1 to 60
distinct roads, with a checksum and the largest answer.
`importance.py` mirrors the ★ arm and its output is byte-identical.
The harness passes the roads as `(a, b)` tuples; the template's adapter
turns them into LeetCode's rows.

`karac fix` carries the template in one round, reporting 10 edits:
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `vec![0i64; n as usize]` to
`Vec.filled(n, 0)`, `sort_unstable()` to `sort()`, the `&d` pattern to
`d`, `(i as i64 + 1)` to `(i + 1)`, since `enumerate`'s index is
already an `i64`, and `struct Solution;` to `struct Solution {}`. The
`r[0] as usize` indexes stay as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every assignment of the values 1 to n tried, and the largest
total of the roads kept. No degrees. It checks 300 random graphs of 2
to 7 cities and 1 to all of their roads; then 30 of 2 to 7 cities that
are a ring, every city two roads, or a star, one city joined to every
other; then 30 of 20 to 60 cities and up to 80 roads, too many to try,
judged by P2 to P6 only. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's (7 cities or fewer) |
| P2 | `m * (n + 1) <= answer <= m * (2n - 1)` for `m` roads: no better than every road on the two largest values, no worse than the average assignment |
| P3 | the roads in reverse order, each turned round: the same answer |
| P4 | the cities renamed, `c` to `(c + 1) % n`: the same answer |
| P5 | a new road between the first two cities not yet joined: the answer grows by 3 to `2n - 1` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 408888301, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by
`itertools.permutations`. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the second end never counted | P1 330, P2 360, P3 158, P5 61, P6 360 |
| M5 | ★: each degree squared | P1 238, P2 268, P5 257, P6 268 |
| M6 | ★: the last city skipped | P1 330, P2 330, P5 51, P6 360 |
| M9 | naive: only the first end counted | P1 172, P2 29, P3 204, P4 157, P5 7, P6 202 |
| M10 | naive: each road its first end twice | P1 303, P2 145, P3 333, P4 224, P5 137, P6 333 |
| M11 | naive: the first road never counted | P1 154, P2 16, P3 132, P4 166, P5 2, P6 183 |
| M13 | heap: the values from n + 1 | P1 330, P2 168, P5 72, P6 360 |
| M14 | heap: the values two apart | P1 330, P2 300, P5 151, P6 360 |
| M16 | heap: each degree pushed twice | P1 325, P2 268, P5 206, P6 355 |
| M17 | struct: sorted by id | P1 196, P2 116, P4 243, P6 226 |
| M19 | struct: sorted the other way | P1 227, P2 257, P6 257 |
| M20 | struct: the first end counted twice | P1 171, P2 31, P3 211, P4 157, P5 14, P6 201 |
| M22 | iter: the values from 0 | P1 330, P2 283, P5 82, P6 360 |
| M24 | iter: degree plus value | P1 311, P2 297, P5 270, P6 341 |
| M26 | iter: each value squared | P1 330, P2 360, P5 221, P6 360 |
| M29 | solution: the first end counted twice | P1 309, P2 129, P3 158, P5 103, P6 339 |
| M30 | solution: the smallest degree left out | P1 258, P2 105, P5 41, P6 264 |

P1, P2 and P6 kill all seventeen, P5 fifteen, P3 six and P4 five. P1
judges only the 330 graphs small enough to try every assignment, so it
counts fewer failures than P6 on the same edit; P2's bounds judge all
360 and miss nothing here. P3 and P4 are the symmetries: they catch
the edits that treat a road's two ends differently, and P4 also the
sort by id, which ties a value to a city's name. P5,
a road added, misses the two edits that leave the sum of degree times
place intact while ordering it wrongly: sorted by id and sorted the
other way.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Each fails as a kept one does: the degrees never
sorted in the ★, iter and template arms and each value to the city of
its place (M1, M23, M28, M21) as the struct arm's sorted by id (M17);
the values from 0 in the ★, naive, struct and template arms (M2, M8,
M18, M27) as the iter arm's (M22); sorted the other way, the fewest roads first and smallest first
(M4, M7, M12) as the struct arm's sorted the other way (M19); the
second end never counted in the heap and iter arms (M15, M25) as the ★
arm's (M3); and the template's values from 2 (M31) as the heap arm's
values from n + 1 (M13), every value one more.

One edit of the first draft failed as a kept one does and left the
template one short: each road a loop at its first end, in the adapter,
fails exactly as the first end counted twice (M29). It is replaced by
the smallest degree left out (M30).

## Verification

Every arm prints the same output as `importance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 1 s, except the naive arm,
whose degree walk over the 5000-city path is 25 million steps: about
10 s.

## Benchmarks

The bench builds 200 graphs once, each of 5000 cities and 5000 random
roads (a pair may repeat), then makes 20 passes over all of them, with
the ★ arm in all five languages. Every implementation prints `20
passes over 200 graphs of 5000 cities: checksum 666974971`. Kāra's and
Rust's `sort` are stable merge sorts, C's `qsort` and Go's
`slices.Sort` are not; on integers the order is the same.

BENCHTAB
