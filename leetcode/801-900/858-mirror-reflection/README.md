# 858. Mirror Reflection

A square room has mirrors on all four walls, each wall of length `p`.
Three corners hold receptors: receptor `0` in the south-east corner, `1`
in the north-east and `2` in the north-west; the south-west corner has
none. A laser ray leaves the south-west corner and first meets the east
wall at a distance `q` from receptor `0`. Return the number of the
receptor the ray meets first; it is guaranteed to meet one.

```
p = 2, q = 1  ->  2
p = 3, q = 1  ->  1
```

**Constraints:** `1 <= q <= p <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `mirror_reflection.kara` ★ | unfold the room: a reflection is the ray going straight on into a mirrored copy, so the ray is the line of slope `q / p` from the origin, and it first meets a corner of the tiling after `k = p / g` rooms across and `m = q / g` rooms up, for `g = gcd(p, q)`. An odd `m` ends on the north wall, an even one on the south; an odd `k` on the east wall, an even one on the west. Only the parities of `k` and `m` matter, so both lengths are halved while both are even, and then an even `p` gives `2`, an even `q` gives `0`, and two odd ones give `1`. O(log p) |
| `mirror_reflection_unfold.kara` | the unfolded room walked a room across at a time: the first `k` whose rise `k * q` is a multiple of `p`, and `m = k * q / p`. O(p / g) |
| `mirror_reflection_gcd.kara` | the rooms across and up directly, as `p / g` and `q / g` with `g` from Euclid's algorithm. O(log p) |
| `mirror_reflection_trace.kara` | the ray traced from wall to wall: between the west and east walls it rises or falls `q`, and its height on each side wall is kept exactly, reflected off the north or south wall when the rise would carry it past one, until it reaches a side wall at height `0` or `p`, a corner. O(p / g) |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples; eleven more
(a room of one, rooms with a common factor, `q` equal to `p`, and rooms
of side 999 and 1000); the count of each receptor over all 5,050 rooms
of side up to 100; and 300 random rooms of side up to 1000, with the sum
of their receptors and a checksum. `mirror_reflection.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the room drawn to scale, every length multiplied by `q` along
the x-axis and by `p` along the y-axis, so that the ray moves one unit
across for each unit up and stays on whole coordinates. It goes straight
to the next wall, turns back off each wall it meets, and stops at a
corner. Its 1,600 rooms are all 820 of side up to 40 and 780 random
rooms of side up to 1000, and their receptors sum to 1,650.

| | property |
|---|---|
| P1 | the statement's receptor |
| P2 | the room and `q` scaled by the same factor, 2 to 5, give the same receptor |
| P3 | with `q < p`, `p - q` in place of `q` keeps receptor `2` and exchanges `0` and `1` |
| P4 | with `q` odd, a room of side `2p` gives receptor `2` |
| P5 | a room of side `p + q` keeps receptor `0` and exchanges `1` and `2` |
| P6 | the answer is a receptor, `0`, `1` or `2` |

P3 to P5 follow from the parities: `p - q` keeps `p / g` and changes the
parity of `q / g` exactly when `p / g` is odd, and `p + q` changes the
parity of `p / g` exactly when `q / g` is odd. P3 is checked on the
1,551 rooms with `q < p` and P4 on the 826 with `q` odd.

It prints `1600 rooms, receptors sum to 1650, 35108 checks over 4 arms:
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only `p` halved | P1 273, P2 407, P3 385 |
| M2 | ★: an even `p` read as receptor `0` | P1 551, P3 551, P4 826, P5 1099 |
| M3 | ★: `q`'s parity read off its second bit | P1 262, P3 525, P5 262 |
| M4 | unfold: the count of rooms across starting at two | P1 49, P5 49 |
| M5 | unfold: the east wall read off the rooms up | P1 551, P3 551, P4 826, P5 1099 |
| M6 | unfold: the rooms up counted as `k * p / q` | P1 640, P3 895, P4 461, P5 1230 |
| M7 | gcd: Euclid returning the larger number a step early | P1 1186, P3 175, P4 521, P5 553 |
| M8 | gcd: the rooms across counted from `q` | P1 1052, P3 1551, P4 826, P5 1600 |
| M9 | gcd: the common divisor left in | P1 270, P2 408, P5 407 |
| M10 | trace: a reflection off the north wall leaving the ray at `p` | P1 944, P3 936, P4 452 |
| M11 | trace: the north corners exchanged | P1 1099, P3 1551, P4 826 |
| M12 | trace: the ray always on the east wall | P1 551, P3 551, P4 826, P5 1099 |

P1 kills all twelve. P2 kills only M1 and M9, the two that do not divide
the common factor out of both lengths: scaling the room changes nothing
for an arm that does. M2, M5 and M12 fail the same cases: each never
answers `2`, so each fails every room whose receptor is `2`, and P4
fails on all 826 rooms with `q` odd. M4 fails the 49 rooms where `q`
equals `p`, the only ones whose ray meets a receptor after one room
across. P6 kills nothing: every mutant still answers a receptor.

## Verification

Every arm prints the same output as `mirror_reflection.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds and the runtime archives are all at kara `d42264fd85`. Under
`karac __mir-run` the arms take 0.13 to 0.21 s and the differential 0.9
s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run all four arms through `karac run
--interp`, `karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build
with the same output, and build the bench program. They refuse the
differential at `let (p, q) = *room` and `*f`, over `iter()` of a vector
of pairs and of an array of integers, saying the element is copied,
where v2 yields a reference to each element. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the trace arm, the one with work to measure, in
all five languages: it traces the ray in every room LeetCode allows, all
500,500 with `1 <= q <= p <= 1000`, 243,908,332 crossings in all. Every
implementation prints `500500 rooms: receptor 0 166198 times, 1 167198,
2 167104, checksum 402739244`, the ★ arm's counts over the same rooms,
the Kāra program under `karac __mir-run` included, in 32 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.42 s |
| Rust (`rustc -O`) | 0.33 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.46 s |
| Go | 0.42 to 0.52 s |
| Python | 12.1 to 14.0 s |
| Kāra, legacy (`karac build`) | 0.44 to 0.54 s |
| Kāra (`karac build --mir`) | 0.35 to 0.44 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.38 s, against Rust's
0.34 (0.41 under overflow checks), C's 0.34, Go's 0.46 and legacy's
0.46: 0.93 times Rust's time under overflow checks, 1.12 times C's, 0.83
times Go's and 0.83 times legacy's. Under valgrind's cachegrind C runs
3.43 billion instructions and 0.73 billion branches, with 41 million
mispredicted, and Rust 3.18 billion, 0.73 billion and 41 million; v2
runs 3.49 billion instructions but 1.34 billion branches, with 41
million mispredicted. The mispredictions are the ray's turns off the
north and south walls, which no compiler can predict, and they cost
about the same in all three. Built for `x86-64-v3`, the target `karac
build` uses, C takes 0.33 to 0.39 s and Rust with overflow checks 0.40
to 0.50 s, against v2's 0.37 to 0.47 s in the same five interleaved
runs. Python takes 13 s, about 38 times C's time. The comparison with C
and Rust waits until after M4.
