# 774. Minimize Max Distance to Gas Station

Gas stations stand at the strictly increasing positions `stations` on a
line. Add `k` new stations anywhere, not necessarily at whole positions,
so that the longest distance between neighbouring stations is as small
as it can be, and return that distance. Answers within 10^-6 are
accepted.

```
stations = [1,2,3,4,5,6,7,8,9,10], k = 9         ->  0.50000
stations = [23,24,36,39,46,56,57,65,84,98], k = 1 ->  14.00000
```

**Constraints:** from 10 to 2,000 stations at positions from 0 to
10^8, and k from 1 to 10^6.

## Approaches

The best way to put m - 1 stations in a gap g cuts it into m equal
pieces, so the answer is always some gap divided by a whole number. The
arms find that number for each gap.

| file | mechanism |
|---|---|
| `minimize_max_distance_to_gas_station.kara` ★ | bisection on the distance d, a hundred halvings from just over the longest gap, counting floor(g / d) stations for gap g; then each gap cut into the fewest pieces shorter than the bound found, whose longest piece is the exact answer |
| `minimize_max_distance_to_gas_station_closed.kara` | bisection counting ceil(g / d) - 1 stations, from the longest gap down until the midpoint equals an end, so the bound is the least reachable double; then each gap cut into ceil(g / d) pieces |
| `minimize_max_distance_to_gas_station_heap.kara` | a heap of gaps, longest pieces first, compared exactly by cross-multiplying, each of the k stations going to the top gap |
| `minimize_max_distance_to_gas_station_share.kara` | each gap first given its proportional share of the k stations; the longest piece that leaves bounds the answer from above, so every gap can start at the pieces that bound forces, and a heap hands out the stations left |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: LeetCode's two examples; one gap cut
in four; two equal longest gaps and one station, which cannot shorten
both; one gap cut into 32 and into 64 pieces, the second exactly halfway
between two values at five decimals, 0.015625, which prints as
0.01562; a long gap and a million stations; a road of mixed gaps; then
300 random roads of 10 to 60 stations, with gaps up to 1,000 or a
quarter of the time up to 10^6 and k up to 2,000, with the sum of the
answers and a checksum of them to six decimals.
`minimize_max_distance_to_gas_station.py` mirrors the ★ arm and its
output is byte-identical. The bisecting arms end by computing the exact
quotient, so all four return the same double, not merely values within
10^-6, and print alike.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the least a / b, over every gap a and every count b from 1 to k +
1, such that cutting every gap g into ceil(g * b / a) pieces, none
longer than a / b, takes at most k stations, all in integers. The
definition is cheap only for small roads, so of the 1,400 random cases
1,200 have from 2 to 8 stations with gaps up to 20 and k up to 30, and
200 have from 10 to 200 stations with gaps as in the harness and k up to
2,000; P1 runs on the small ones and P4 proves every answer best on all
of them.

| | property |
|---|---|
| P1 | on the small cases the answer is the definition's, bit for bit |
| P2 | one more station never makes the answer longer |
| P3 | the stations mirrored and shifted give the same answer |
| P4 | the answer is some gap g over some count m, bit for bit, where k stations can cut every piece to g / m or less but not every piece to less than g / m, which proves it best |

It prints `1400 cases (answers sum to 148887.85175), 4 arms,
21600 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error; the sum is the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bound not raised past the longest gap | P1 5, P4 5 |
| M2 | ★: the bound returned without the final cut | P1 1186, P4 1384 |
| M3 | ★: a count of exactly k stations taken as too many | P1 987, P4 1173 |
| M4 | closed: pieces counted, not stations | P1 1195, P4 1395 |
| M5 | closed: the final cut into pieces shorter than the bound | P1 1168, P4 1359 |
| M6 | closed: the search begun at half the longest gap | P1 114, P3 173, P4 126 |
| M7 | heap: the shortest pieces first | P1 1021, P4 1221 |
| M8 | heap: one station fewer | P1 987, P4 1173 |
| M9 | heap: gaps ordered by length, not by their pieces | P1 988, P4 1188 |
| M10 | share: each share one station too many | P1 914, P4 1081 |
| M11 | share: a start of p pieces charged p stations | P1 922, P4 1122 |
| M12 | share: the stations left given to the shortest pieces | P1 1018, P2 292, P3 85, P4 1218 |

P1 and P4 kill all twelve, and they agree: an answer the definition
rejects on a small case is one the proof in P4 rejects, and P4 also
covers the large cases. M1 starts the ★ bisection at the longest gap
itself, which the count of shorter pieces never accepts, so when two
longest gaps share too few stations it reports half of one; only 5 small
cases have that shape. M6 halves each gap as it takes the running
maximum, so the closed bisection starts at half of some gap, which loses
whenever the answer is longer; which gap depends on their order, so
P3, which reverses it, sees M6 more often than P1 does. M12 hands the
stations left after the shares to the shortest pieces, which makes the
answer depend on which stations remain, so P2 and P3 see it too. Two
first choices did nothing: twenty halvings instead of a hundred, and
stopping the closed bisection once the bound is within 10^-6. Both
bisecting arms end by cutting every gap at the bound found, which lands
on the exact answer from any bound short of the next quotient above it,
so their precision barely matters; M2 and M6 replace them.

## Verification

Every arm prints the same output as
`minimize_max_distance_to_gas_station.py` under `karac __mir-run` (the
v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer) with no error; the differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the release
build that runs `check` and `__mir-run` are both at kara `4f079681eb`,
whose last compiler change is `ecb1a0322e`. The runtime archives were
built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, heap and share arms and,
through a copy, the bench. The three print the same output under the
legacy JIT (`karac run`), `karac build` and an auto-par build, and the ★
and share arms under the legacy interpreter as well; the heap arm's
million stations ran past the interpreter's 60 s limit there. Legacy
refuses the closed arm and so the differential at `*g` on the element of
a `for` over a `Vec[f64]`, which it gives by value, and the bench at
`minmax_gas_dist(roads[round % 64], ks[round % 64])`, as a move out of
an index; the timing below is of a copy whose parameter is `ref
Vec[i64]`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Sixty-four
random roads of 2,000 stations, LeetCode's limit, with gaps up to
50,000 and so spread over up to 10^8, each with k from 1 to 10^6, are
built once; each of 2,000 rounds solves the next of them, and the
answers are added up. Every implementation prints `2000 roads of
2000 stations: answers sum to 450144.43446`, the Kāra program under
`karac __mir-run` included (in 164 s). The work is 100 halvings, each a
pass of floating-point divisions over the 1,999 gaps.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.51 to 0.73 s |
| Rust (`rustc -O`) | 0.59 to 0.73 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.74 to 0.83 s |
| Go | 0.57 to 0.61 s |
| Python | 46.8 to 47.8 s |
| Kāra (`karac build --mir`) | 0.71 to 0.82 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
4.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.78 s,
against C's 0.56, Rust's 0.66 (0.80 under overflow checks) and Go's
0.58, and Python takes 47 s. Under valgrind's cachegrind v2 runs
7.3 billion instructions and 1.6 billion branches, Rust 7.1 billion and
1.0 billion, and C 4.0 billion and 106 million. The legacy build of the
copy ran 0.71 to 1.01 s, a median of 0.74 s in the interleaved runs, so
v2 takes 1.05 times legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

Nothing new.
