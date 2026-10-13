# 470. Implement Rand10() Using Rand7()

Given the API `rand7()` that generates a uniform random integer in the
range `[1, 7]`, write a function `rand10()` that generates a uniform
random integer in the range `[1, 10]`. You can only call the API
`rand7()`, and you shouldn't call any other API. Please do not use a
language's built-in random API.

**Follow up:** What is the expected value for the number of calls to
`rand7()` function? Could you minimize the number of calls to
`rand7()`?

## Approaches

Every arm is `fn rand10(rng: mut ref Rand7) -> i64`, where `Rand7`
offers `fn rand7(mut ref self) -> i64`. A uniform draw from 1 to 10
cannot come from a fixed number of calls, since 10 does not divide any
power of 7, so every arm throws something away and draws again.

| file | mechanism | calls of rand7 on average |
|---|---|---|
| `rand10.kara` ★ | two calls give 1 to 49; keep 1 to 40, four for each value, and start over on 41 to 49 | 2 × 49/40 = 2.45 |
| `rand10_reuse.kara` | as the ★ arm, but a rejected 41 to 49 is itself a uniform draw from 9, so one more call makes 1 to 63, of which 60 are kept; a rejected 61 to 63 and one more call make 1 to 21, of which 20 are kept | about 2.19 |
| `rand10_bits.kara` | a call that gives 1 to 6 is a fair bit by its parity (a 7 is thrown away); four bits make 0 to 15, of which 0 to 9 are kept | 4 × 7/6 × 16/10 ≈ 7.47 |
| `rand10_halves.kara` | a fair bit picks the half (1 to 5 or 6 to 10) and a call that gives 1 to 5 picks within it (6 and 7 are thrown away) | 7/6 + 7/5 ≈ 2.57 |
| `differential.kara` | each arm held to what a rand10 must do, five properties |

The arms draw differently, so the same `rand7` gives each of them
different values, and the harness prints only what every correct
`rand10` must make true. `Rand7` either draws from a seeded generator
or replays a script of draws. Every arm prints the same 9 lines:

- for every script of up to 2, 3, 4, 5 and 6 draws, enumerated in full,
  whether the ten values have equal total weight over the scripts the
  arm finishes on (a script of `L` draws weighs `7^(D - L)` out of
  `7^D`), and whether every value it returned was from 1 to 10;
- for 1,000,000 draws from a seeded `rand7`, whether all were from 1 to
  10, whether each value came up within 4 standard deviations of
  100,000 times, and whether, cut into 500,000 pairs, each of the 100
  pairs came up within 4 standard deviations of 5,000 times.

All nine read `true`. `rand10.py` mirrors the ★ arm and its output is
byte-identical; it draws the same values, so its counts match the ★
arm's exactly.

The exact lines are the strong ones: every arm here is exactly uniform
at every depth, not only in the limit, so the enumeration finds equal
weights at each one. A draw-by-draw interval method (read base-7 digits
until they fix a decimal digit) is uniform only in the limit, and would
fail them; it is not one of the arms.

## Differential

`differential.kara` holds copies of the four arms. Since they cannot be
compared with each other, each is held to the properties below, 3,026
checks an arm.

| | property |
|---|---|
| P1 | over every script of up to 6 draws, the scripts of exactly `L` draws that the arm finishes on give each value equally often, for each `L` from 1 to 6, and never anything outside 1 to 10 |
| P2 | on 1,500 random scripts of 200 draws, the draws the arm read decide its value: the same draws followed by other ones give the same value and read as many |
| P3 | every value on those scripts is from 1 to 10 |
| P4 | in 10 seeded runs of 30,000 draws, each value comes up within 5 standard deviations of 3,000 times |
| P5 | in the same runs, cut into 15,000 pairs, each of the 100 pairs comes up within 5 standard deviations of 150 times |

P1 is per length, which is stronger than the harness's running total:
it is the arm's distribution exactly, depth by depth. P4 and P5 use 5
standard deviations because they check 4,400 counts in all, and at 4 a
fair arm would fail one of them about one run in five; the first
version, at 4, did fail one P5 count on the ★ arm.

It prints `4 arms, 12104 checks, 0 failures` under `karac __mir-run`,
and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 41 and 42 are kept too | P1 3, P4 10, P5 10 |
| M2 | ★: 40 is thrown away too | P1 3, P4 10, P5 8 |
| M3 | reuse: all of 1 to 63 is kept | P1 1 |
| M4 | reuse: a rejected 41 to 49 counts from 1, not 0 | P1 1 |
| M5 | bits: a 7 counts as an odd bit | P1 1, P4 10, P5 10 |
| M6 | bits: 10 is kept, giving 11 | P1 3, P3 133, P4 10, P5 1 |
| M7 | halves: a 6 counts as one of five | P1 5, P3 104, P4 10, P5 10 |
| M8 | halves: the coin throws away 6 as well as 7 | P1 5, P4 10, P5 10 |

P1 sees all eight, and alone sees M3 and M4: their bias lives in the
third draw of the reuse arm, which comes into play once in 5.4 calls
(9/49), so 300,000 draws do not show it at 5 standard deviations but
the exact count at length 3 does. P2 sees none, as expected: every
mutant still reads its draws in order and keeps nothing between calls,
which is all P2 checks.

## Verification

All four arms print the same output as `rand10.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `12104 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

On the frozen legacy backends every arm matches under LLJIT,
`karac build`, and `KARAC_AUTO_PAR=1 karac build`, and the differential
prints the same line under `karac run --interp` and `karac build`.
Under `karac run --interp` the ★, reuse and halves arms match; the bits
arm, which reads about three times as many draws, prints its first four
lines correctly and does not finish the depth-6 enumeration within the
300 s limit. That is a timeout, not a divergence. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm over the same seeded `rand7` as the
harness: 20,000,000 calls of `rand10`, counting each value and folding
the values in order into a checksum. Every implementation prints
`20000000 draws: 1999985 ones, 1999343 tens, checksum 339701230`, the
Kāra program under `karac __mir-run` included (in 63 s).

The legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.29 s |
| Rust (`rustc -O`) | 0.14 to 0.17 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 s |
| Go | 0.29 to 0.32 s |
| Python | 12.3 to 13.1 s |
| Kāra (`karac build --mir`) | 0.28 to 0.30 s |
| Kāra (legacy `karac build`) | 0.27 to 0.29 s |

The Kāra rows are timed at kara `d2ffa9b440`. Kāra checks integer
overflow, so the like-for-like Rust row is the one with
`overflow-checks=on`. Under `karac __mir-llvm-run` the program prints
the same line in 1.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
