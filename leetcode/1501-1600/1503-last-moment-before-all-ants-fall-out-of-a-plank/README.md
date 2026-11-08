# 1503. Last Moment Before All Ants Fall Out of a Plank

A wooden plank is `n` units long. Some ants walk on it at one unit per
second, some to the left and some to the right. When two ants walking in
opposite directions meet, they both turn round and keep walking; turning
takes no time. An ant that reaches either end of the plank falls off at
that moment. Given `n` and the positions of the ants walking left (`left`)
and right (`right`), return the moment when the last ant falls off.

```
n = 4, left = [4, 3], right = [0, 1]          ->  4
n = 7, left = [], right = [0, 1, 2, 3, 4, 5, 6, 7]  ->  7
n = 7, left = [0, 1, 2, 3, 4, 5, 6, 7], right = []  ->  7
```

**Constraints:** `1 <= n <= 10^4`; `0 <= left.length, right.length <= n + 1`;
positions lie in `0..=n`; all positions in both lists are distinct.

## Approaches

| file | mechanism |
|---|---|
| `ants.kara` ★ | two ants that meet and turn round look, with their labels taken off, like two that pass through each other, so the last fall is the longest walk: a left ant's `p`, a right ant's `n - p`. O(ants) |
| `ants_iter.kara` | the same walks with iterators: the left positions `chain`ed with the right ones' `n - p`, then `max` |
| `ants_sort.kara` | by the order of the falls: ants never pass, so each end's falls come in the order of its walks, sorted; the answer is the later of the two last |
| `ants_sim.kara` | the statement simulated: positions doubled so two ants always meet on a point, time in half units; each tick the ants at an end walking off it fall, two ants on one point turn round, every ant steps. O(n * ants) |
| `ants_solution.kara` | LeetCode's Rust template (`left.iter().max().copied()`, `map(\|&p\| n - p)`, `Solution::`), carried by `karac fix` in two rounds (10 edits, then 1) to Kāra that checks |
| `differential.kara` | the four closed-form arms, the Rust one among them, against the simulation, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's three
examples and five more, then the sum and a checksum of the answers for
3000 planks of 1 to 12 units, 300 of 1 to 100, and 5 of 1 to 600. Each
position of a plank holds a left ant, a right ant or none, at a fill drawn
per plank. `ants.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the ★, iterator, sort and Rust arms,
and the simulation as the statement read literally. It checks 3000
problems of planks of 1 to 10 units. Every random choice of a problem (the
plank, its ants, the ant to take off) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement simulated |
| P2 | the plank mirrored (each ant at `n - p`, walking the other way) leaves the answer |
| P3 | one ant taken off never makes the answer later |
| P4 | one more unit at the right end makes the answer later by 0 or 1 |
| P5 | the answer lies in `0..=n`, and is `n` exactly when an ant starts at an end walking toward the other |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 794504890, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept, three to
each arm. All twenty are killed and each fails the same way under both
backends, none by a crash. No two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each left walk one short | P1 984, P2 1914, P5 513, P6 984 |
| M2 | ★: a right ant's walk read as its position | P1 1014, P2 1320, P5 695, P6 1014 |
| M3 | ★: the answer starting at 1 | P1 662, P5 197, P6 662 |
| M4 | iter: `min` for `max` | P1 1952, P3 459, P5 1100, P6 1952 |
| M5 | iter: the first left ant skipped | P1 282, P2 1212, P5 114, P6 282 |
| M6 | iter: only the first right ant's walk | P2 702 |
| M7 | sort: the left walks not sorted | P2 685 |
| M8 | sort: the right walks not sorted | P1 685, P2 685, P3 126, P5 400, P6 685 |
| M9 | sort: the answer starting at `n / 2` | P1 592, P6 592 |
| M10 | Rust: the shortest left walk | P1 702, P2 1387, P3 149, P5 399, P6 702 |
| M11 | Rust: the smaller of the two ends | P1 1914, P5 991, P6 1914 |
| M12 | Rust: the wrapper passing the left ants as the right | P1 1437, P2 1932, P5 1025, P6 1437 |

P1 and P6 kill ten of the twelve, P5 nine, P2 eight, P3 three, and P4
none. M6 and M7 are seen by P2 alone: the arms' input lists come
ascending, so the first right ant has the longest walk and the last left
ant does, and taking the first or skipping the sort is right on every
problem as drawn. Mirroring hands the lists over descending, and both
edits fail there. P4 is blind to every edit here: each edited arm still
reads the right ants' walks as `n - p` or not at all, and both move with
`n` the way P4 asks.

The other eight fail as a kept one does. The ★ arm without its left loop
fails as M1; the ★ arm's right walk one short, the sort arm's, and the
Rust arm's (`n - p - 1`) fail alike; the iterator arm's right walk read as
its position fails as M2, and the sort arm reading its first left walk for
its last fails as M10. The iterator arm's `unwrap_or(n)` (P1 481, P3 355,
P5 481, P6 481) and the Rust arm's `l + r - min(l, r) - 1` (P1 3000, P5
1913, P6 3000) fail with signatures of their own but add no property.

## Rust template

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` carries it in two rounds, 10 edits and then 1:
`Vec<i32>` to `Vec[i32]`, `Solution::` to `Solution.`, the `&p` closure
pattern to `p`, and `copied()` to `cloned()`. It then checks and prints the
★ arm's output, and it is the fourth arm of the differential.

## Benchmarks

The ★ arm is one pass for a maximum, too little to time, so the bench
runs the simulation: 300 planks of 1 to 1000 units built once, then each
simulated, in all five languages with the same structure (positions and
directions in arrays, a doubled-position table of which ant stands where).
Every implementation prints `300 planks of 1 to 1000 units simulated: sum
150334, checksum 478791513`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `83c2a5580` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.234 to 0.246 s | 0.238 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.253 to 0.302 s | 0.256 s |
| Rust (`rustc -O`) | 0.252 to 0.306 s | 0.256 s |
| Go | 0.283 to 0.349 s | 0.314 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.296 to 0.347 s | 0.317 s |
| Kāra (`karac build`) | 0.281 to 0.354 s | 0.330 s |
| Python | 11.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.341 s) is below its real time (0.346 s).

Kāra is 1.24x Rust under overflow checks by median. The work is three
passes over the ants per half-unit tick, each reading `on[i]` and two
`i64` arrays and indexing the position table by `pos[i]`; why Kāra's loops
are slower was not measured.

## Verification

Every arm prints the same output as `ants.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the closed-form arms take 0.2 to 0.3 s, the
simulation 1.3 s, and the differential 1.0 s.

## Writing it

The four Kāra arms were written in Kāra and checked with no diagnostic;
`karac fix` made two edits to the differential.
