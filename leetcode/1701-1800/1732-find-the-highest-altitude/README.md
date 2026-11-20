# 1732. Find the Highest Altitude

There is a biker going on a road trip. The road trip consists of `n + 1`
points at different altitudes. The biker starts the trip on point `0`
with altitude equal `0`.

You are given an integer array `gain` of length `n` where `gain[i]` is
the **net gain in altitude** between points `i` and `i + 1` for all
(`0 <= i < n`). Return *the **highest altitude** of a point.*

```
gain = [-5,1,5,0,-7]           ->  1    (altitudes 0,-5,-4,1,1,-6)
gain = [-4,-3,-2,-1,4,3,2]     ->  0    (altitudes 0,-4,-7,-9,-10,-6,-3,-1)
```

**Constraints:** `n == gain.length`; `1 <= n <= 100`;
`-100 <= gain[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `altitude.kara` ★ | every altitude pushed onto a list, the start's 0 first and each next one the last plus its gain, and the largest taken with `iter().max()`. O(n) |
| `altitude_fold.kara` | a `fold` over the gains whose state is the pair (altitude now, highest so far), both starting at the start's 0. O(n) |
| `altitude_scan.kara` | `scan` carries the altitude through the gains and yields each point's; `max` over them, with the start's 0 as the floor, is the answer. Nothing is stored. O(n) |
| `altitude_solution.kara` | a Rust solution as LeetCode's Rust users write it, `alt += g` over `for g in gain` and the answer kept with `ans = ans.max(alt)`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 6 lines: LeetCode's two examples, a single
loss, and a hundred climbs of 100; then the highest points summed and a
checksum for 3000 random trips of up to 8 gains from -3 to 3 and 3000 of
up to 100 gains from -100 to 100, LeetCode's limits. `altitude.py`
mirrors the ★ arm and its output is byte-identical.

```
1
0
0
10000
3000 trips of up to 8 gains up to 3: highest points sum to 7114, checksum 620056322
3000 trips of up to 100 gains up to 100: highest points sum to 850896, checksum 761266509
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the altitude of point `i` is the sum of the first `i` gains,
added up anew for each point, point 0 the start at 0, and the answer
the largest of the `n + 1`. It checks 3000 random trips of 1 to 8 gains
from -5 to 5. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a loss of 1000 put at the end gives the same answer |
| P3 | every gain doubled doubles the answer |
| P4 | the trip run backwards, each gain negated, gives the answer less the total gain |
| P5 | each arm agrees with at least two of the other three |

P4 holds because the backward trip's altitudes are the trip's own, each
less the last one. The differential prints `3000 problems: checksum
220522352, 60000 checks over 4 arms: 0 failures` under every lane in
Verification, and a Python reading of the statement, the largest of `0`
and `itertools.accumulate` of the gains, gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Four of them, M1, M4, M5 and M8, each
turn the answer into the largest single gain or 0, and fail the very
same checks; M6 and M9 both drop the start's 0, and M7 and M10 both
miss the last point. No edit fails P3: each of these answers is still a
sum of gains, which doubles with them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each altitude the gain alone, not the last altitude plus it | P1 1907, P4 2238, P5 1907 |
| M2 | ★: the answer the last altitude, not the largest | P1 1977, P2 3000, P4 2817, P5 1977 |
| M3 | ★: the start at the first gain, not 0 | P1 2742, P4 2723, P5 2742 |
| M4 | fold: the highest compared with the gain, not the altitude | P1 1907, P4 2238, P5 1907 |
| M5 | fold: the altitude never moved | P1 1907, P4 2238, P5 1907 |
| M6 | scan: the start's 0 not taken as a floor | P1 777, P4 1579, P5 777 |
| M7 | scan: each point yields the altitude before its gain | P1 802, P2 802, P4 1579, P5 802 |
| M8 | solution: the answer kept from the gains, not the altitudes | P1 1907, P4 2238, P5 1907 |
| M9 | solution: the answer starting at `i32.MIN`, not 0 | P1 777, P4 1579, P5 777 |
| M10 | solution: the answer taken before the gain is added | P1 802, P2 802, P4 1579, P5 802 |

## Benchmarks

The bench draws 1000 random trips of 100 gains from -100 to 100,
LeetCode's largest, all of them first, then answers each 2000 times by
the ★ arm in all five languages. Every implementation prints `1000 trips
of 100 gains, 2000 rounds: highest points sum to 838452000, checksum
575703251`. Each answer builds its list of 101 altitudes anew: Kāra,
Rust and Go push onto a growable list from one element, and C writes a
`malloc`'d array of `n + 1`, which never grows. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.120 s |
| Rust (`rustc -O`) | 0.449 s |
| Kāra (`karac build`) | 0.575 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.591 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.668 s |
| Go | 1.260 s |
| Python | 11 s |

The sequential Kāra build takes 1.32x Rust's time and 0.88x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.120 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.727 s and 0.731 s on one
run).

## Verification

All four arms print the same output as `altitude.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm checked clean as first written.

The fold arm was written `fold((0, 0), |(altitude, highest), g| ...)`
and then `let (_, highest) = ...; highest` as the `i32` answer. `karac
check` named the narrowing at the return, and its fix reached back
through the `fold` and the tuple pattern to the seed and wrote `(0,
0i32)`.

The scan arm was written as Rust writes it, `scan(0, |altitude, g| {
*altitude += g; Some(*altitude) })`. Kāra's `scan` closure takes its
state by value and returns `Some((state, item))`, and `karac fix`
rewrote the closure to `{ let altitude = altitude + g; Some((altitude,
altitude)) }`. The seed `0` kept the default `i64`, since `+` with an
`i32` gain does not fix a literal's type, so every altitude was an
`i64` and `max(0, highest)` an `i64` returned as the `i32` answer.
`karac check` named the narrowing but offered no fix; since kara
`93fd9b2078` (B-2026-11-20-47) the narrowing reaches back through the `let` and
the `max` to the seed of a `scan` whose item is its state, and `karac
fix` wrote `scan(0i32, ..)`.

LeetCode's Rust template took one `karac fix` of 5 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, and `let mut
alt = 0` and `let mut ans = 0` declared `alt: i32` and `ans: i32`.
`for g in gain` and `ans.max(alt)` carried over as written.

The differential took one `karac fix` of 2 edits: the statement's
reading summed its gains into `let mut altitude = 0` and kept the
largest in `let mut highest = 0`, and both were declared `: i32`.
`arm_name` in it indexes a list of string literals for a `Str`, as
#1662's does (B-2026-11-19-131).
