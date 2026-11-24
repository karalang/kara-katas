# 1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance

There are `n` cities numbered from `0` to `n - 1`. Given the array
`edges` where `edges[i] = [from_i, to_i, weight_i]` represents a
bidirectional and weighted edge between cities `from_i` and `to_i`, and
given the integer `distanceThreshold`, return the city with the smallest
number of cities that are reachable through some path and whose distance
is at most `distanceThreshold`. If there are multiple such cities, return
the city with the greatest number. The distance of a path connecting
cities i and j is equal to the sum of the edges' weights along that path.

```
n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4                  ->  3
n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2  ->  0
```

**Constraints:** `2 <= n <= 100`, `1 <= edges.length <= n * (n - 1) /
2`, `0 <= from_i < to_i < n`, `1 <= weight_i, distanceThreshold <=
10^4`, and all pairs `(from_i, to_i)` are distinct.

The arms are `fn find_the_city(n: i32, edges: Vec[Vec[i32]],
distance_threshold: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `find_the_city.kara` ★ | every pair's shortest distance by Floyd-Warshall over a `Vec[Vec[i64]]`, then each city's count of others within the threshold by `filter(..).count()`; the fewest wins, and the later city on a tie through `<=`. O(n^3) |
| `find_the_city_dijkstra.kara` | Dijkstra from each city over an adjacency list, a `PriorityQueue` of (distance, city) popping the nearest first, nothing pushed past the threshold. O(n m log n) |
| `find_the_city_bellman.kara` | Bellman-Ford from each city: every road relaxed both ways, round after round, until a round changes nothing; the cities walked from the last down, so only a strict improvement replaces the answer. O(n^2 m) at worst |
| `find_the_city_dense.kara` | Dijkstra from each city on a weight matrix with no queue: each round settles the nearest city not yet settled, found by a scan of every city, and stops past the threshold. O(n^3) |
| `find_the_city_solution.kara` | a Rust solution as LeetCode's Rust users write it (Floyd-Warshall over `vec![vec![i32::MAX / 2; n]; n]` indexed by `usize`, each road unpacked with `let (u, v, w) = (e[0] as usize, e[1] as usize, e[2])`, `dist[i][j].min(..)`, and the counts by `filter(\|&j\| ..).count()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, two cities
alone, and two joined by a road longer than the threshold (`3 0 1 1`);
100 cities, the constraints' most, every pair joined, under two
thresholds, and a line of 100 (`100 cities: 4950 roads 78 54, a line
97`); and 300 random maps of 2 to 100 cities, most of them small, with
each pair joined with chance 1 in 5 or 7 in 10, weights up to 10 or
10^4, and the threshold up to twice the heaviest weight (`300 random
maps: checksum 186805156`). `find_the_city.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, Bellman-Ford and dense arms check clean. The
Dijkstra arm draws two warnings for casts an `i32` does not need on its
way to an `i64` (`n as i64`, `distance_threshold as i64`), and `karac
fix` drops both. The Rust arm takes one round of 18 fixes by `karac
fix`'s count, from 8 errors: `struct Solution;` to `struct Solution {}`,
each `Vec<..>` to `Vec[..]`, `usize` to `i64`, `vec![vec![x; n]; n]` to
`Vec.filled(n, Vec.filled(n, x))`, `i32::MAX` to `i32.MAX` and
`usize::MAX` to `i64.MAX`, `|&j|` to `|j|`, `&&` to `and`, and
`Solution::` to `Solution.`. Its output matches on the first run. The
differential's `let mut total = 0;`, summed from `i32` weights and
passed as an `i32`, is refused because the literal keeps `i64`, and
`karac fix` annotates it `i32`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every path that visits no city twice is walked from each city,
the shortest to each other city kept, and the city with the fewest others
within the threshold, the greatest on a tie, is the answer. 2000 maps of
2 to 6 cities in four kinds, 500 each: each pair joined with chance 1 in
3 and weights from 1 to 3; with chance 2 in 3 and weights from 1 to 10;
every weight 1; and weights up to 10^4. The threshold runs from 0 to
twice the heaviest weight. Every map is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the roads listed backwards, each written from its other end: the same answer |
| P3 | every weight and the threshold doubled: the same answer |
| P4 | the threshold every weight summed: the greatest city of a smallest group of cities joined by roads |
| P5 | a road longer than the threshold added between two cities not yet joined: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 maps: checksum 128630234,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, by Floyd-Warshall, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each road entered one way only | P1 508, P2 1258, P4 324, P6 2032 |
| M2 | ★: the city passed through looped innermost | P1 21, P4 77, P6 84 |
| M3 | dijkstra: a city settled again on every pop | P1 169, P4 248, P6 169 |
| M4 | dijkstra: the threshold never checked | P1 379, P5 235, P6 379 |
| M5 | bellman: a road's first direction ending no round | P1 114, P2 217, P4 326, P5 95, P6 114 |
| M6 | bellman: the cities walked from the first | P1 1560, P4 1668, P6 1560 |
| M7 | dense: a city on the threshold left out | P1 199, P4 206, P6 199 |
| M8 | dense: the first distance found kept | P1 60, P5 241, P6 60 |
| M9 | solution: the first road forgotten | P1 474, P2 550, P4 538, P6 474 |
| M10 | solution: the fewest count started at 0 | P1 914, P4 1335, P6 914 |

P1 and P6 kill all ten, P4 eight, P2 three, P5 three and P3 none. A
threshold of every weight summed (P4) makes every reachable city count,
so it catches each edit that loses a road or a direction (M1, M5, M9),
reaches a city the long way (M2), counts a city twice (M3), breaks a tie
the wrong way (M6, M10), or turns the limit strict (M7), since the
summed threshold is often met exactly. Writing each road from its other
end (P2) catches the three edits that treat a road's two ends
differently (M1, M5) or depend on which road comes first (M9). The long
road (P5) catches the edits that would use it: the threshold never
checked (M4), a relaxation left half done (M5), and the first distance
kept when the long road is found first (M8). Doubling every weight and
the threshold (P3) catches none: every edit here is unchanged by scale.

## Benchmarks

The bench builds 10 maps of 100 cities, the constraints' most, each pair
joined with chance one in two and weights up to 10^4, once; then makes
30 passes, each setting one road's weight of every map and the threshold
from the checksum so far, so no answer carries over, answering every map
with the ★ arm and folding the answer plus the pass into the checksum.
Every language reads the roads in place; C keeps its distances in one
flat array, the others in a list of rows. Every implementation prints
`30 passes over 10 maps of 100 cities: checksum 90129943`.

BENCHTAB
