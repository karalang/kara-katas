# 1259. Handshakes That Don't Cross

You are given an **even** number of people `numPeople` that stand around
a circle and each person shakes hands with someone else so that there
are `numPeople / 2` handshakes total.

Return *the number of ways these handshakes could occur such that none
of the handshakes cross*.

Since the answer could be very large, return it **modulo** `10^9 + 7`.

```
numPeople = 4  ->  2
numPeople = 6  ->  5
```

**Constraints:** `2 <= numPeople <= 1000`; `numPeople` is even.

The arms are `fn number_of_ways(num_people: i64) -> i64`.

## Approaches

Person 0's handshake splits the others into the people on its two
sides, an even number each, who shake hands only among themselves. The
counts are the Catalan numbers.

| file | mechanism |
|---|---|
| `handshakes_that_dont_cross.kara` ★ | by pairs: `ways[k]`, the count for `k` pairs, summed over how many pairs sit on one side of person 0's handshake, in a `Vec.filled` |
| `handshakes_that_dont_cross_memo.kara` | top down: the count for `n` people asked recursively over person 0's partner, two seats at a time, each count kept in a `Map` |
| `handshakes_that_dont_cross_formula.kara` | by formula: the Catalan number `C(2k, k) / (k + 1)` modulo the prime, with factorials and Fermat's inverse by repeated squaring |
| `handshakes_that_dont_cross_paths.kara` | as paths: round the table, a person who starts a handshake steps up and one who ends it steps down, and the handshakes that don't cross are the paths that never go below the start; a row of counts per height, moved one person at a time |
| `handshakes_that_dont_cross_solution.kara` | a Rust solution as LeetCode's Rust users write it (`const MOD: i64`, `vec![0i64; n + 1]`, `as usize`, an `i32` signature), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples; the total
and a checksum of the counts for every even number of people from 2 to
1000 (`total 165682182, checksum 156855159`); and the counts for 2 to 20
people, exact (`1, 2, 5, 14, 42, ...`), and for 1000 people
(`591137401`). `handshakes_that_dont_cross.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the four Kāra arms checked clean as first written. The
solution arm takes one round of fixes, 5 by `karac fix`'s count:
`struct Solution;` to `struct Solution {}`, `(num_people / 2) as usize`
to `as i64`, `vec![0i64; n + 1]` to `Vec.filled(n + 1, 0)`, and the harness's
`as i64` on the `i32` result dropped, since an `i32` widens to `i64` by
itself. All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to pair the people, the lowest unpaired person with
each later unpaired one in turn, counted when no two handshakes `(a, b)`
and `(c, d)` have `a < c < b < d`. That is exponential, so it is asked
only up to 12 people; the other properties cover every even number from
2 to 400.

| | property |
|---|---|
| P1 | the statement read literally, up to 12 people |
| P2 | the sum over person 0's partner, from the arm's own answers for fewer people |
| P3 | `(k + 1)` times the count for `k` pairs is `2(2k - 1)` times the count for `k - 1`, modulo the prime |
| P4 | the count is within 0 and `10^9 + 6` |
| P5 | the exact Catalan number, up to 36 people, where it is below the modulus |
| P6 | the ★ arm's count |

All 6,000 checks pass on every arm: `2 to 400 people: checksum
433558174, 6000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and the AddressSanitizer build.
Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the sum starts from one pair on the left, not none | P1 6, P2 1, P3 1, P5 18, P6 800 |
| S2 | ★: `ways[k - 1]` in place of `ways[k - 1 - left]` | P1 4, P2 198, P3 198, P5 16, P6 792 |
| M1 | memo: one too many people on the far side | P1 6, P2 1, P3 1, P5 18, P6 200 |
| M2 | memo: each count kept under the next count's key | P1 4, P2 198, P3 198, P5 16, P6 198 |
| F1 | formula: `(k + 1)!` taken for `k!` | P1 6, P2 200, P3 200, P5 18, P6 200 |
| F2 | formula: the inverse raised to `p - 1`, which is 1 | P1 6, P2 200, P3 200, P5 18, P6 200 |
| P1 | paths: the highest step never taken | P1 6, P2 200, P3 200, P5 18, P6 200 |
| P2 | paths: two people fewer walked | P1 5, P2 198, P3 199, P5 17, P6 199 |
| L1 | solution: `dp[0] = 2` | P1 6, P2 200, P3 200, P5 18, P6 200 |
| L2 | solution: the `% MOD` left out of the sum | runtime error: integer overflow |

All ten are caught: nine by P1, the statement read literally, P5, the
exact Catalan numbers, and P6, the ★ arm's count, and L2 by Kāra's
overflow check, since without the modulus the counts pass `i64` near
70 people. P2 and P3, the two recurrences, catch every mutation that
gives a wrong but nonzero count, and only once those, S1 and M1, whose
counts are all 0 past 0 people: a row of zeros satisfies both
recurrences from its second count on, so only the step from the 1 for
no people shows. P4, the count within the modulus, catches none: every
arm still reduces modulo the prime, or overflows first.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (ways[k] for k pairs, summed over where person 0's partner sits,
modulo 10^9 + 7) for every even count of people from 2 to 1000, 4
rounds; each count folded into a checksum. Every program prints `4
rounds of 2 to 1000 people: checksum 47328625`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.542 to 0.583 s | 0.547 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.542 to 0.578 s | 0.547 s |
| Rust (`rustc -O`) | 0.379 to 0.408 s | 0.385 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.387 to 0.417 s | 0.391 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.386 to 0.400 s | 0.392 s |
| C (`clang -O3`) | 0.378 to 0.400 s | 0.385 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.380 to 0.412 s | 0.387 s |
| Go | 0.516 to 0.536 s | 0.526 s |
| Python | 8.628 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 29% ahead of Kāra (0.391 s
against 0.547 s). C is about 30% ahead of Kāra (0.385 s against 0.547
s); Go runs level with Kāra (0.526 s against 0.547 s). Python takes
about 16x Kāra's time. No profile was taken.
