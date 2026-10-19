# 787. Cheapest Flights Within K Stops

There are `n` cities and `flights[i] = [from, to, price]`, a one-way
flight. Return the cheapest price from `src` to `dst` with at most `k`
stops, or `-1` when there is no such way.

```
n = 4, flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], src = 0, dst = 3, k = 1  ->  700
n = 3, flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]], src = 0, dst = 2, k = 1  ->  200
n = 3, flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]], src = 0, dst = 2, k = 0  ->  500
```

**Constraints:** `n` is from 1 to 100, there are at most `n (n - 1) / 2`
flights, no two the same and none from a city to itself, each price is
from 1 to 10,000, `src` and `dst` are different cities, and `k` is from
0 to `n - 1`.

## Approaches

At most `k` stops is at most `k + 1` flights. A way may pass a city more
than once, but a cheapest way never needs to, since prices are positive.

| file | mechanism |
|---|---|
| `find_cheapest_price.kara` ★ | Bellman-Ford for `k + 1` rounds: after round `r`, `cost[c]` is the cheapest way to `c` in at most `r` flights, as long as each round relaxes every flight from the costs of the round before, so each round reads a copy of the last; O(k e) |
| `find_cheapest_price_levels.kara` | breadth first by flights: a `VecDeque` of (city, cost so far) for the cities reached by the last flight, spread out `k + 1` times, a city going into the next level only when its cost beats the best seen for it, since a dearer way with more flights cannot help; O(k e) |
| `find_cheapest_price_dijkstra.kara` | Dijkstra over (city, flights taken): a smallest-first `PriorityQueue` of (cost, city, flights) settles states cheapest first, so the first time the destination comes out its cost is the answer, and a state is skipped when its city was settled with no more flights; O(k e log(k e)) |
| `find_cheapest_price_memo.kara` | recursion with a memo: the cheapest way from `c` to the destination in at most `r` flights is 0 at the destination and otherwise the least over the flights out of `c` of the price plus the answer for the next city with `r - 1`, each (city, `r`) worked out once; O(k e) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: LeetCode's three examples; a network
with no way to the destination, one where the cheapest way needs more
stops than allowed, and one where it needs exactly as many as allowed; a
chain of 100 cities with a dear direct flight from the first to the
last, at four values of `k`; and 300 random networks of 2 to 100 cities
with a random `k`, with how many have a way and a checksum of the
answers. `find_cheapest_price.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the cheapest of every walk from `src` of at most `k + 1` flights, found
by walking them all. Its 1,600 random networks are 1,200 of 2 to 6
cities with `k` up to 3, where walking every way is cheap, and 400 of 7
to 100 cities, whose answer is the cheapest walk of exactly `f` flights
for `f` from 1 to `k + 1`, worked out one flight at a time from the
walks of `f - 1` flights. A quarter of each have random flights at
prices up to 10,000, a quarter prices up to 10, so ties are common, a
quarter three flights for each city, and a quarter a chain through every
city of cheap flights with dear random shortcuts, from the first city to
the last, so the cheapest way needs the most stops.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the same flights in another order give the same answer |
| P3 | one more stop allowed is never worse |
| P4 | when there is no direct flight from `src` to `dst`, adding one gives the least of its price and the answer |

It prints `1600 networks (1195 with a way), 4 arms, 22472 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a round reading the costs it has already lowered | P1 246, P2 126 |
| M2 | ★: k rounds, not k + 1 | P1 415, P4 159 |
| M3 | ★: k + 2 rounds | P1 156 |
| M4 | levels: the next level carrying the cost before the flight | P1 691, P4 20 |
| M5 | levels: a city reached put back in the same level | P1 266 |
| M6 | levels: as many levels as cities, whatever k | P1 266 |
| M7 | dijkstra: each city settled once, whatever its flights | P1 20, P3 5 |
| M8 | dijkstra: one flight too few | P1 415, P4 159 |
| M9 | dijkstra: the flights never counted | P1 266 |
| M10 | memo: the memo kept by city alone | P1 145, P2 161, P3 54 |
| M11 | memo: the destination counted only with every flight used | P1 778, P3 782, P4 454 |
| M12 | memo: the dearest way kept | P1 727, P3 775, P4 427 |

P1 kills all twelve. M3, M5, M6 and M9 are caught by P1 alone: each
allows ways with too many flights, and a cheaper answer from more
flights keeps P2, P3 and P4 true, so only the definition sees it. In the
first run of the mutations the large networks were checked by the
properties alone, and P1 saw those four only on the small networks;
`layered`, the definition for the large networks, was added for this. M7
settles each city once, at its cheapest, whatever flights that took, so
a dearer way with fewer flights is dropped although it could still reach
the destination within `k` stops; it fails in 20 networks. The first M6
never lowered the best cost seen, so every level carried every city
reached, and it ran without end; it was replaced by this one.

## Verification

Every arm prints the same output as `find_cheapest_price.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★ arm unchanged and refuse the
other three arms and the differential at the type check: in `for (to,
price) in out[city].iter()` they take the items for `i64` rather than
references, so `*price` and `*to` are errors. The ★ arm, and copies of
the others and of the differential with those `*`s removed, print the
same output under the legacy interpreter (`karac run --interp`), the
legacy JIT (`karac run`), `karac build` and an auto-par build, each
build with a warning that a borrowed `flights` is used after a move,
since legacy predates borrowed parameters; the legacy interpreter takes
51 minutes over the differential. Legacy refuses the bench program's
`find_cheapest_price(100, networks[r % 64], src, dst, k)` as a move out
of an index; a copy with the parameter written `ref Vec[Vec[i64]]`
builds, and the bench timing below is of it. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 networks of
100 cities, LeetCode's most, are made once, each with 1,000 different
flights at prices from 1 to 10,000. Each of 20,000 rounds asks the next
network for the cheapest way between two random cities with a random `k`
from 0 to 99, so on average about 50 rounds of Bellman-Ford, each
copying the costs and relaxing all 1,000 flights. Every implementation
prints `20000 rounds of 100-city networks: 19746 with a way, checksum
327284007`, the Kāra program under `karac __mir-run` included (in 36
minutes, run with `KARAC_MIR_MAX_STEPS` raised above its default of 40
billion steps).

The bench measures a loop over the flights reading and writing two
arrays of 100 costs. The flights are a `Vec[Vec[i64]]` in Kāra, as
LeetCode gives them, so each flight is a separate allocation of three
numbers; C's are an array of three-field structs, Rust's a `Vec<[i64;
3]>` and Go's a `[][3]int64`, all laid out flat, and Python's a list of
lists. Every implementation allocates a fresh copy of the costs each
round, as the Kāra `clone()` does. Spot timings on a shared 4-core
container, eight runs of each compiled program, five of them
interleaved, and four of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.99 to 1.27 s |
| Rust (`rustc -O`) | 1.35 to 1.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.44 to 2.18 s |
| Go | 2.30 to 2.65 s |
| Python | 56.81 to 59.46 s |
| Kāra (`karac build --mir`) | 2.70 to 3.99 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as for the other katas since the redesign; the legacy
`karac build` refuses it (see Verification), and that edit is by hand,
on top of the `scripts/new-bench.sh` output. Under `karac
__mir-llvm-run` the program prints the same line in 15.3 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

At the medians of the interleaved runs the v2 build takes 3.31 s,
against C's 1.20, Rust's 1.60 (1.71 under overflow checks) and Go's
2.51. Under valgrind's cachegrind v2 runs 31.5 billion instructions and
11.1 billion branches, against C's 11.3 billion and 3.04 billion and
Rust's 15.3 billion and 5.04 billion; none mispredicts more than 18
million. Where v2's extra instructions lie is not profiled; its flights
are each a pointer away, where C's, Rust's and Go's are not. The legacy
build of the copy ran 2.68 to 3.88 s, a median of 3.08 s in the
interleaved runs, so v2 takes 1.07 times legacy. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new.
