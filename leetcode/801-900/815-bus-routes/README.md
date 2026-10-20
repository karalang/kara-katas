# 815. Bus Routes

`routes[i]` is the loop of stops that bus i drives, over and over. From
the stop `source`, not on any bus yet, return the fewest buses to take
to reach the stop `target`, or -1 if no ride reaches it.

```
routes = [[1, 2, 7], [3, 6, 7]], source = 1, target = 6                         ->  2
routes = [[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], source = 15, target = 12  ->  -1
```

The first ride takes bus 0 to stop 7 and bus 1 on to stop 6.

**Constraints:** `1 <= routes.length <= 500`, `1 <= routes[i].length <=
10^5`, the stops of one route are distinct, `sum(routes[i].length) <=
10^5`, and `0 <= routes[i][j], source, target < 10^6`.

## Approaches

Riding one bus reaches every stop on its route, so the answer counts
buses, not stops: two buses link when they share a stop. Every arm but
one is a breadth-first search, one bus more at each level. A ride from a
stop to itself takes no bus, and a source or target on no route has no
ride unless the two are the same stop.

| file | mechanism |
|---|---|
| `bus_routes.kara` ★ | index the buses by stop, then search over buses from those at the source; the first bus whose route holds the target answers. Each bus and each stop is expanded once, O(total stops) |
| `bus_routes_stops.kara` | search over stops: from each stop board every bus not yet boarded and step off at every stop of its route not yet seen. O(total stops) |
| `bus_routes_graph.kara` | sort each route and link two buses when a merge of their routes finds a shared stop, then search the graph of buses, testing a route for the target by binary search. O(b^2 l) for b buses of up to l stops |
| `bus_routes_meet.kara` | search over buses from both ends at once, always widening the side with the smaller frontier by a whole level; a bus reached from both sides, d buses from the source and e from the target, makes a ride of d + e - 1 |
| `differential.kara` | the four arms against a sweep over every route until nothing changes, four properties |

The two-ended arm returns the best join found while widening one level,
not the first: the other side has searched every bus within its depth,
so the best join of the level is the shortest ride.

Every arm prints the same 12 lines: LeetCode's two examples; a ride from
a stop to itself, on a route and off every route; a source on no route;
one bus; a ring of five routes, whose short way round starts on the last
route; a long route joined to the target by two short ones; two buses
that never meet; LeetCode's largest, 500 routes of 1 to 400 stops below
a million, about 100,000 in all, from the first route to the last; 500
routes of 200 stops in a chain, 500 buses from one end to the other; and
300 random rounds of 1 to 10 routes, with a total and a checksum.
`bus_routes.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out over stops: the fewest buses found so far to each stop, the
source at 0, and every route swept again and again, each carrying a
rider from its best reached stop to all its stops for one bus more,
until a sweep changes nothing. Its 1,600 cases come in four kinds of
400: 1 to 8 routes of 1 to 5 stops among up to 16; chains of 1 to 10
routes, each sharing a stop with the one before, walked either way and
shuffled, so that rides are long; 1 to 10 routes of 1 or 2 stops among
up to 30, so that most pairs are cut off; and routes of up to 8 stops
among up to 9, so that most rides take a bus or two. Each end is a stop
on a random route, or one time in four any stop, perhaps on no route.
523 cases have no ride, and the longest ride takes 8 buses.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the same with the buses in reverse order, each route walked backwards |
| P3 | the same from the target back to the source |
| P4 | the same with every stop s renamed 3 s + 1 |

It prints `1600 cases (523 with no ride, the longest ride 8 buses),
25600 checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no shortcut when the source is the target | P1 297, P2 297, P3 297, P4 297 |
| M2 | ★: a bus boarded from another counted on the same level | P1 249, P2 249, P3 249, P4 249 |
| M3 | ★: the queue taken from the back | P1 39, P2 40, P3 43, P4 39 |
| M4 | stops: a stop stepped off at counted on the same level | P1 249, P2 249, P3 249, P4 249 |
| M5 | stops: the queue taken from the back | P1 4, P2 4, P3 2, P4 4 |
| M6 | stops: a route's first stop never stepped off at | P1 294, P2 287, P3 290, P4 294 |
| M7 | graph: the merge steps the larger side | P1 236, P2 236, P3 236, P4 236 |
| M8 | graph: buses next to each other in the list never linked | P1 117, P2 117, P3 117, P4 117 |
| M9 | graph: the routes not sorted | P1 516, P2 512, P3 516, P4 516 |
| M10 | meet: a joining bus counted on both sides | P1 249, P2 249, P3 249, P4 249 |
| M11 | meet: no answer of 1 when a bus serves both ends | P1 531, P2 531, P3 531, P4 531 |
| M12 | meet: a bus already reached reached again | P1 215, P2 218, P3 223, P4 215 |

P1 kills all twelve. M2, M4 and M10 fail on the same 249 cases, the ones
whose ride takes two buses or more, M2 and M4 counting every such ride
as one bus and M10 counting one bus too many. M3 and M5 turn the search
depth first and are seen only where the first ride found is not the
shortest.

One more edit leaves every answer right and is not counted: letting the
two-ended arm's sides share one set of stops seen. A stop that one side
has already scanned has handed every bus through it to that side, and so
any bus the other side would reach through it is already a join.

## Verification

Every arm prints the same output as `bus_routes.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change in that tree, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`) and `karac build` refuse every arm, the differential and
the bench program: legacy types the item of `route.iter()` over a
`Vec[i64]` as an `i64` rather than a reference and so refuses its `*`,
and in the graph arm reads `share_a_stop(sorted[a], sorted[b])` as
moving a `Vec` out of an index (`E_INDEX_MOVE_NON_COPY`). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 cities of 100
bus routes, each of 1 to 200 distinct stops among 20,000, are drawn
once. Each of 4,000 rounds asks the next city for the fewest buses
between two stops, each on a random route or, one time in eight, any of
the 20,000. The search indexes the city's buses by stop afresh each
round, about 10,000 stops, so most of the time goes to the map from stop
to buses. C has no hash map, so its mirror carries an open-addressing
table with a short integer mix for a hash; Kāra's `Map` and Rust's
`HashMap` hash with SipHash-1-3, and Go uses its built-in map. Every
implementation prints `4000 rounds of 100 routes: total 7458, checksum
142368072`, the Kāra program under `karac __mir-run` included, in 179 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.59 to 2.93 s |
| Rust (`rustc -O`) | 4.02 to 5.46 s |
| Rust (`rustc -O -C overflow-checks=on`) | 4.82 to 5.38 s |
| Go | 5.03 to 5.48 s |
| Python | 8.58 to 9.89 s |
| Kāra (`karac build --mir`) | 3.93 to 4.48 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 30.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 4.20 s,
against C's 2.72, Rust's 4.14 (5.05 under overflow checks) and Go's
5.25. Under valgrind's cachegrind v2 runs 42.9 billion instructions,
Rust 37.6 billion and C 21.4 billion. v2 and Rust are level, and both
run about twice C's instructions, most likely for the keyed SipHash
against C's few multiplies (not traced). Built for `x86-64-v3`, the
target `karac build` uses, C (`clang -O3 -march=x86-64-v3`) takes 2.59
to 2.76 s and runs the same 21.4 billion instructions, and Rust with
overflow checks (`-C target-cpu=x86-64-v3`) 4.07 to 5.48 s, against v2's
3.88 to 4.24 s in the same five interleaved runs. Python takes 9.2 s,
little more than twice v2's time, as its dicts and sets do the same
hashing in C. Legacy refuses the bench program (see Verification), so
there is no legacy timing to set v2 against. The comparison with C and
Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench passed
`karac check` and every v2 lane as first written, apart from a pattern
`let (mut i, mut j) = ..` in the graph arm, which `karac check` refuses
with a diagnostic naming the Kāra spelling, `let mut (i, j) = ..`.
