# 495. Teemo Attacking

Our hero Teemo is attacking an enemy Ashe with poison attacks! When
Teemo attacks Ashe, Ashe gets poisoned for exactly `duration` seconds.
More formally, an attack at second `t` will mean Ashe is poisoned
during the inclusive time interval `[t, t + duration - 1]`. If Teemo
attacks again before the poison effect ends, the timer for it is reset,
and the poison effect will end `duration` seconds after the new attack.

You are given a non-decreasing integer array `timeSeries`, where
`timeSeries[i]` denotes that Teemo attacks Ashe at second
`timeSeries[i]`, and an integer `duration`.

Return the total number of seconds that Ashe is poisoned.

```
timeSeries = [1,4], duration = 2  ->  4
timeSeries = [1,2], duration = 2  ->  3
```

**Constraints:** `1 <= timeSeries.length <= 10^4`;
`0 <= timeSeries[i], duration <= 10^7`; `timeSeries` is sorted in
non-decreasing order.

## Approaches

Every arm is `fn find_poisoned_duration(time_series: Vec[i64],
duration: i64) -> i64`.

| file | mechanism |
|---|---|
| `teemo_attacking.kara` ★ | each gap, capped: an attack poisons until the next one or for the full duration, whichever is shorter; the last gets the full duration |
| `teemo_attacking_merge.kara` | merging the poisoned intervals: an attack that starts before the current interval ends stretches it, one that starts after closes it and adds its length |
| `teemo_attacking_fold.kara` | a `fold` over `iter()` carrying the total and the moment the poison wears off; each attack adds only the poisoned time it brings past that moment |
| `teemo_attacking_zip.kara` | `iter().zip(iter().skip(1))` pairs each attack with the next; `map` caps each gap and `sum` adds them, plus the last duration |
| `differential.kara` | the four arms on 1,500 random series, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
attack, a zero duration, attacks back to back, intervals exactly
touching, two attacks at the same moment, the problem's largest
values, and for 300 random series (1 to 30 attacks, gaps of 0 to 9, a
duration of 0 to 9) the total and a checksum. `teemo_attacking.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random series `a` and `b` of 1 to 25 attacks, with gaps of 0 to
2, 0 to 9 or 0 to 40 in turn, a duration of 0 to 12 and a shift of 0
to 999. The reference puts every poisoned second in a `Set` and counts
them.

| | property |
|---|---|
| P1 | the total is the reference's |
| P2 | every attack shifted by the same amount gives the same total |
| P3 | the total is at least one duration and at most one duration per attack |
| P4 | an attack repeated at the same moment adds nothing |
| P5 | `b` placed after `a`'s poison wears off adds `b`'s own total |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 2.4 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a gap is not capped at the duration | P1 855, P3 712, P5 1409 |
| M2 | ★: the last attack adds nothing | P1 1366, P3 169, P5 1366 |
| M3 | merge: an interval ends a duration after it starts, not after its last attack | P1 1162, P5 33 |
| M4 | merge: the first interval is taken to start at 0 | P1 1500, P3 186, P5 1500 |
| M5 | fold: each attack counts from where the poison wore off | P1 1393, P2 1499, P3 779, P5 1000 |
| M6 | fold: the end of the poison never passes the duration | P1 1147, P2 579, P4 1330, P5 573 |
| M7 | zip: each attack is paired with the one two on | P1 1199, P4 801, P5 1275 |
| M8 | zip: the last attack adds nothing | P1 1366, P3 169, P5 1366 |

M2 and M8 are the same mistake in two arms and fail with the same
counts. One first draft was equivalent and was replaced: closing the
merge arm's interval when the next attack lands exactly at its end,
rather than stretching it, adds the same seconds either way.

## Verification

All four arms print the same output as `teemo_attacking.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included.
The differential prints `30000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on the ★ and merge arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output. They refuse the other two. On the fold and zip
arms they refuse `*t` and `*b - *a` at type checking ("unary '*'
requires 'ref T' ... found 'i64'"), reading the items as values where
v2 reads them as borrows; the differential carries copies of those arms
and is refused the same way. (Before the zip arm went back to `*b -
*a`, `karac run --interp` printed its right output, and LLJIT and legacy
`karac build` failed in codegen: "no handler for method 'sum' on
non-identifier receiver".) Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 200 series of 10,000
attacks (the problem's most) with gaps of 0 to 99, once, then solves
each for every duration from 0 to 49. Every implementation prints
`200 series of 10000, 50 durations each: 2032416568 poisoned in all,
checksum 790462376`, the Kāra program under `karac __mir-run` included
(in 68 s).

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.09 to 0.12 s |
| Rust (`rustc -O`) | 0.07 to 0.11 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.10 to 0.12 s |
| Go | 0.10 to 0.12 s |
| Python | 16.5 to 18.2 s |
| Kāra (legacy `karac build`) | 0.10 to 0.12 s |
| Kāra (`karac build --mir`) | 0.40 to 0.44 s |

Legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build; the
`--mir` row is timed by hand at kara `d9a7136c58`. The v2 compiled
backend is 3.6 times slower here, and kara B-2026-10-13-15 has the
measurements: the x86 code takes a branch for `.min(duration)` where
rustc keeps a conditional move, and with gaps of 0 to 99 against
durations of 0 to 49 that branch is close to a coin flip (28 million
mispredicts under cachegrind, against 21 thousand for the
overflow-checked Rust). Under `karac __mir-llvm-run` the program prints
the same line in 2.0 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-13-15 (perf, open): `karac build --mir` runs the bench
3.6 times slower than C, Rust and legacy `karac build`; see Benchmarks.

The zip arm was first written `(*b - *a)`, since the items of `iter()`
are borrows. That form ran right on `karac __mir-run` and passed `karac
check` with `KARAC_CHECK_LIBRARY=1`, but default `karac check` refused
it ("unary '*' requires 'ref T' ... found 'i64'"), so the arm used `(b
- a)` for a while. Kata 643 filed the same refusal as kara
B-2026-10-15-1 (`check` typed the items of a `zip` by value), fixed in
kara `078a101ad6`. The arm and the differential are back to `(*b -
*a)`, which default `karac check` passes at kara `f75dd289bc`.
