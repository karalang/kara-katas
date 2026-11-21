# 2477. Minimum Fuel Cost to Report to the Capital

There is a tree (i.e., a connected, undirected graph with no cycles)
structure country network consisting of `n` cities numbered from `0` to
`n - 1` and exactly `n - 1` roads. The capital city is city `0`. You are
given a 2D integer array `roads` where `roads[i] = [a_i, b_i]` denotes
that there exists a **bidirectional road** connecting cities `a_i` and
`b_i`.

There is a meeting for the representatives of each city. The meeting is
in the capital city.

There is a car in each city. You are given an integer `seats` that
indicates the number of seats in each car.

A representative can use the car in their city to travel or change the
car and ride with another representative. The cost of traveling between
two cities is one liter of fuel.

Return *the minimum number of liters of fuel to reach the capital city*.

```
roads = [[0,1],[0,2],[0,3]], seats = 5                          ->  3
roads = [[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], seats = 2        ->  7
roads = [], seats = 1                                           ->  0
```

**Constraints:** `1 <= n <= 10^5`; `roads.length == n - 1`;
`roads[i].length == 2`; `0 <= a_i, b_i < n`; `a_i != b_i`; `roads`
represents a valid tree; `1 <= seats <= 10^5`.

Every representative beyond a road must cross it, so a road with `c`
people beyond it needs at least `ceil(c / seats)` cars. Gathering every
representative of a subtree at its top city and driving them on in as
few cars as hold them meets that bound on every road at once, so the
fuel is the sum, over the cities but the capital, of `ceil(size /
seats)` for the city's subtree.

## Approaches

| file | mechanism |
|---|---|
| `fuel.kara` ★ | by subtree sizes: a breadth-first order from the capital, walked backwards, gives each city its subtree's size before its parent's, and its road adds `ceil(size / seats)`. O(n) |
| `fuel_dfs.kara` | depth first: a recursive walk from the capital returns each subtree's size, adding the cars for the road it leaves by. O(n) |
| `fuel_peel.kara` | peeling leaves: a city other than the capital with one road left has heard from everyone beyond it, so it sends its people down that road and the road goes; a `VecDeque` of such cities reaches every city but the capital. No root is chosen. O(n) |
| `fuel_trips.kara` | every trip walked: each representative's road to the capital walked city by city through a parent list, counting how many pass through each city; the road out of a city then carries `ceil(count / seats)` cars. O(n h), `h` the depth |
| `fuel_iter.kara` | iterators: the breadth-first order grown by `extend` with each city's unseen neighbours taken by `filter`, the sizes by a `rev` walk over it, and the fuel by `map` and `sum`. O(n) |
| `fuel_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` and `i32` in, `i64` out; a `vec![vec![]; n]` of `usize` neighbours and a `dfs` nested in the method, its parent `usize::MAX` at the capital, adding to a `&mut i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples; then
three more, a path from the capital with one seat, a star round it with
two, and a path with the capital in the middle; then a random tree of
`10^5` cities, the constraints' largest, with 1, 3 and `10^5` seats, and
a path of 2000 cities from the capital with 1 and 7 seats; and 3000
random trees of 1 to 40 cities with 1 to 10 seats, as a checksum. A
random tree joins each city after the first to a random earlier one,
puts each road's ends in a random order, and shuffles the roads. The
path stops at 2000 cities, below the constraints' `10^5`, because the
trips arm is O(n h). `fuel.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 5000 random trees of 1 to
12 cities against two readings that share none of its code: a
simulation in which every city, deepest first, gathers the cars that
reach it, adds its own representative and drives on in as few cars as
hold them, and the bound above, each road's cut-off side counted by a
search that avoids it. The three agreed on every tree.

`check` first reports 12 errors on the template, and `karac fix`
carries it in one call, reporting 21 edits: the nested `fn dfs` moves
above the `impl`, since Kāra has no nested items; the generic brackets
of `Vec<Vec<i32>>` and `&Vec<Vec<usize>>`; `vec![vec![]; n]` becomes
`Vec.filled(n, Vec.new())`; the `&` on each parameter becomes `ref` and
`&mut` `mut ref`, and on each argument the `&` goes and `&mut` becomes
`mut`; the `&` in `for &v in &graph[u]` goes from the pattern and
becomes `ref` on the list, as on `&roads`; `usize::MAX` becomes `usize.MAX`; `seats as
i64` loses its cast, since an `i32` widens by itself; and `struct
Solution;` is given its braces. The `usize` neighbours, `as usize`
casts and the tuple `let (a, b)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each road, the cities it cuts off from the capital,
counted by a search that may not use it, and the cars those people need
summed. No root, order or subtree is used. It checks 300 random trees
of 1 to 10 cities, then 60 of up to 30, with 1 to 6 seats. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the fuel is the literal reading's |
| P2 | as many seats as cities: one liter a road |
| P3 | one seat: the sum of every city's distance from the capital |
| P4 | two copies joined at the capital: twice the fuel |
| P5 | the tree hung below a new capital, the old one its only neighbour: `ceil(n / seats)` more |
| P6 | each arm agrees with at least three of the other five |

P2 holds because every road then needs one car. P3 holds because with
one seat every representative drives alone, one liter a road on the
way. P4 holds because the two copies share only the capital, so no
road carries people of both. P5 holds because every old road keeps the
people beyond it, and the new road carries all `n`.

The differential prints `360 cases: checksum 718855982, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search with sets. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: cars rounded down | P1 268, P2 320, P5 231, P6 268 |
| M2 | ★: one car a road | P1 138, P3 265, P5 238, P6 138 |
| M5 | ★: the capital's road counted too | P1 360, P2 360, P3 360, P4 242, P5 129, P6 360 |
| M9 | dfs: the last city taken as the capital | P1 178, P3 251, P4 255, P5 238, P6 178 |
| M10 | dfs: a grandchild counted as a child | P1 204, P2 108, P3 265, P5 290, P6 204 |
| M11 | dfs: cars one seat short | P1 159, P3 320, P5 210, P6 159 |
| M12 | peel: the capital peeled too | P1 229, P2 232, P3 231, P4 250, P5 229, P6 229 |
| M15 | peel: a city queued at two roads | P1 234, P2 234, P3 237, P5 240, P6 234 |
| M16 | peel: the first leaves from city 2 | P1 102, P2 102, P3 102, P4 102, P5 142, P6 102 |
| M17 | trips: the start not counted | P1 320, P2 320, P3 320, P5 164, P6 320 |
| M19 | trips: each trip one city short | P1 320, P2 320, P3 320, P5 238, P6 320 |
| M20 | trips: the last city never a start | P1 320, P2 320, P3 320, P4 320, P5 292, P6 320 |
| M24 | iter: the order walked forwards | P1 108, P3 164, P5 217, P6 108 |
| M25 | iter: the last city left out | P1 320, P2 320, P3 320, P4 320, P5 278, P6 320 |
| M26 | iter: sizes passed to the city numbered one less | P1 137, P3 258, P4 128, P5 236, P6 137 |
| M30 | solution: one seat more in every car | P1 115, P3 265, P5 161, P6 115 |
| M31 | solution: people counted from zero | P1 320, P2 320, P3 320, P5 360, P6 320 |

P1, P5 and P6 kill all seventeen, P3 sixteen, P2 eleven, and P4 seven.

Fourteen are not kept. Twelve fail exactly as a kept one: the ★ arm's
order walked forwards and sizes never passed up, the dfs arm's child's
size not added, the peel arm's people never passed on, and the
template's child's people not added and one car a road (M3, M4, M8,
M13, M28, M29) as the ★ arm's one car a road (M2); the cars rounded
down in the dfs, peel, trips, iter and template arms (M7, M14, M18,
M22, M27) as in the ★ arm (M1); and the iter arm's capital included
(M23) as the ★ arm's capital's road counted too (M5). Two end with an
index out of bounds rather than a wrong answer: the ★ arm's roads kept
one way only (M6) and the trips arm's city never left (M21). Every edit is killed by some check.

Three edits were replaced before this table was drawn. Two survived
every check because they change nothing the answer reads: the iter
arm's first city after the capital skipped, which only stops a size
being passed to the capital, whose size is never used, and the
template's parent not skipped, a test that is never true in a tree.
The dfs arm's every city its own size failed exactly as a kept one.

## Verification

Every arm prints the same output as `fuel.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.9 to 7.0 s and the differential 1.4 s; under `karac __mir-llvm-asan` the arms take 1.1 to 2.1 s and the differential 1.1 s, and under `karac run` the differential takes 0.8 s.

## Benchmarks

The bench builds 20 random trees of `10^4` cities once from its own
generator, as the arms build theirs, then makes 60 passes; each
answers every tree with 1 to 50 seats chosen by the checksum so far, so
no answer carries over, folding the fuel plus the pass into the
checksum. The bench uses the ★ arm in all five languages: C keeps the
neighbours as compressed rows in one array, and the others a list per
city. Every implementation prints `60 passes over 20 trees of 10^4:
checksum 926375368`.

BENCHTAB
