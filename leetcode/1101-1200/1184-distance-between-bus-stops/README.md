# 1184. Distance Between Bus Stops

A bus runs on a ring of `n` stops numbered `0` to `n - 1`. `distance[i]` is
the distance between stop `i` and stop `(i + 1) % n`, and the bus goes both
ways round. Return the shortest distance between the stops `start` and
`destination`.

```
distance = [1, 2, 3, 4], start = 0, destination = 1  ->  1
distance = [1, 2, 3, 4], start = 0, destination = 2  ->  3    (1 + 2, or 3 + 4)
distance = [1, 2, 3, 4], start = 0, destination = 3  ->  4    (4 the other way)
```

**Constraints:** `1 <= n <= 10^4`, `distance.length == n`, `0 <= start,
destination < n`, `0 <= distance[i] <= 10^4`.

The arms are `fn distance_between_bus_stops(distance: Vec[i64], start: i64,
destination: i64) -> i64`. The two Rust arms keep the method LeetCode gives
Rust users, over `Vec<i32>` and `i32`, inside `impl Solution`, and a
one-line `distance_between_bus_stops` converts the values and calls it.

## Approaches

The two stops cut the ring into two arcs, and the answer is the shorter.
One arc is the legs from the lower stop up to the higher, and the other is
the rest of the ring.

| file | mechanism |
|---|---|
| `distance_between_bus_stops.kara` ★ | the stops ordered with `min` / `max`, the arc between them summed over the slice `distance[from..to]`, and the other arc the whole ring less it. O(n) |
| `distance_between_bus_stops_walk.kara` | the bus ridden stop by stop, clockwise and then counterclockwise, with the stop index taken modulo `n`, and the shorter ride kept. O(n) |
| `distance_between_bus_stops_prefix.kara` | prefix sums, `reach[i]` the ride from stop 0 to stop `i`; the arc is `\|reach[destination] - reach[start]\|` and the ring `reach[n]`. O(n) time and space |
| `distance_between_bus_stops_solution.kara` | a Rust solution as LeetCode's Rust users write it (the stops ordered with `min` / `max` and cast to `usize`, the ring and the arc summed with `iter().sum()` into annotated `i32`s), carried to Kāra by `karac fix` |
| `distance_between_bus_stops_chain.kara` | another Rust solution, one iterator chain (`iter().enumerate().fold((0, 0), ..)` splitting the legs between the two arcs by `(s..d).contains(&i)`, and the smaller taken from the tuple), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; one stop,
from itself to itself (`small 1: 0`); two stops asked the other way round
(`small 2: 5`); legs of length 0, where the shorter way costs nothing
(`small 3: 0`); stops asked from the higher to the lower on a ring of eight
(`small 4: 17`); 3000 random rings of 1 to 12 stops with legs 0 to 20
(`3000 random rings: checksum 556953161`); and a ring of 10000 stops, the
constraints' most, with legs 0 to 10000 (`10000 stops: 11288491`).
`distance_between_bus_stops.py` mirrors the ★ arm and its output is
byte-identical; it also asserts that every answer equals a ride around the
ring each way, stop by stop, as the statement reads. Every arm gives the
same output under `karac run` and `karac build`.

The Mend loop: the ★, walk and prefix arms take no fixes. The solution arm
takes one round of 6 (`struct Solution;` to `struct Solution {}`,
`Vec<i32>` to `Vec[i32]`, `Solution::` to `Solution.`, the `&` in `|&v|`
dropped, the casts back to `i64` dropped) and its output matches. The chain
arm takes 12 in its first round, among them its `usize` casts to `i64` and
the `&` of `&x`, `contains(&i)` and `|&v|`, and was then refused with no fix (the gap below); with the fix, one more round
of 2 writes the seed as `(0i32, 0i32)` and its output matches.

## Gap

**A name bound from a fold's result got no reason and no fix.** The chain
arm's `let (inside, outside) = distance.iter().enumerate().fold((0, 0),
|(a, b), (i, x)| ..)` over `i32` legs, then `inside.min(outside)` returned
as an `i32`, was refused with "implicit coercion from 'i64' to 'i32' would
narrow or change sign" and the advice to write `as i32`. The refusal is
right: the seed's literals meet the `i32` legs only through `+`, so they
keep the `i64` default (design.md §8 Literals). But `let (inside, outside)
= (0, 0)` gets the reason and a suffix fix, and the fold's result has the
seed's type. Now a name bound from a fold's result is bound to the seed's
literal, so the refusal says "`inside` is an 'i64' because the literal it
is bound to took the default (design.md §8 Literals); write that literal
`0i32`", and `karac fix` writes it. kara B-2026-11-17-98.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the bus ridden from `start` one stop at a time, clockwise and
then counterclockwise, adding each leg, and the shorter ride kept. 600
random rings of 1 to 12 stops with legs 0 to `span`, the span 0 to 20; the
first ten have one stop and the next ten ask from a stop to itself.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the way back (`start` and `destination` swapped) is as long |
| P3 | the ring renumbered from another stop has the same answer |
| P4 | the shorter way is at most half the ring |
| P5 | every leg doubled doubles the answer |
| P6 | the ★ arm's answer |

All 18,000 checks pass on every arm: `600 rings: checksum 502574578, 18000
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac run` and
`karac build`.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: one way round only | P1 122, P3 155, P4 122, P6 488 |
| A2 | ★: the ring's first leg left out | P1 141, P3 179, P6 564 |
| W1 | walk: counterclockwise rides the leg ahead | P1 197, P2 356, P4 39, P6 197 |
| W2 | walk: the longer ride taken | P1 398, P4 398, P6 398 |
| P1 | prefix: the arc's sign kept | P1 188, P2 388, P3 157, P6 188 |
| P2 | prefix: the ring stops a leg short | P1 140, P3 143, P6 140 |
| X1 | solution: the arc's first leg skipped | P1 338, P3 137, P6 338 |
| X2 | solution: the stops not ordered | P1 181, P2 378, P3 149, P6 181 |
| R1 | chain: an inside leg counted both ways | P1 122, P3 155, P4 122, P6 122 |
| R2 | chain: the inside arc taken | P1 122, P3 155, P4 122, P6 122 |

A mutation of the ★ arm fails P6 on every arm. P4 catches the faults that
can answer with the longer way (A1, W2, R1, R2) and W1, whose
counterclockwise ride is off by a leg; P2 the faults that depend on which
stop is asked first (W1, P1, X2). R1 and R2 fail the same checks: counting
an inside leg both ways makes the outside arc the whole ring, so the
minimum is the inside arc, which is what R2 returns. P5 catches none,
since every fault here scales with the legs.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 50 rings of 10000 stops, the constraints' most, with legs 0 to
10000, and 200 pairs of stops a ring, built once; then 10 rounds asking
every pair, each answer folded into a checksum. Every program prints `10
rounds of 10000 queries over 50 rings: checksum 77512623`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `2a5724c2d4`
and kata 1186's two fixes, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.529 to 0.577 s | 0.551 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.528 to 0.648 s | 0.564 s |
| Rust (`rustc -O`) | 0.153 to 0.187 s | 0.163 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.438 to 0.473 s | 0.453 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.422 to 0.537 s | 0.447 s |
| C (`clang -O3`) | 0.150 to 0.205 s | 0.162 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.122 to 0.154 s | 0.129 s |
| Go | 0.713 to 0.873 s | 0.764 s |
| Python | 6.85 to 6.86 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 5% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 1.24x the time of
overflow-checked Rust, the equal-safety comparison, 3.5x C's and 0.74x
Go's; Python takes about 12x Kāra's. The work is summing `i64`s, about
13,000 a query (the whole ring, then the arc), and Rust's checked build takes 2.8x its plain one, so most of C's lead is the
overflow check on each add; where Kāra's time over checked Rust's goes was
not profiled.
