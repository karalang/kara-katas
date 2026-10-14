# 629. K Inverse Pairs Array

For an integer array `nums`, an inverse pair is a pair of indices `[i,
j]` with `0 <= i < j < nums.length` and `nums[i] > nums[j]`. Given two
integers `n` and `k`, return the number of arrays of the numbers 1 to
`n` with exactly `k` inverse pairs, modulo 1,000,000,007.

```
n = 3, k = 0  ->  1    ([1,2,3])
n = 3, k = 1  ->  2    ([1,3,2] and [2,1,3])
```

**Constraints:** `n` from 1 to 1,000; `k` from 0 to 1,000.

## Approaches

Every arm is `fn k_inverse_pairs(n: i64, k: i64) -> i64`. Putting the
largest value `n` into an arrangement of the other `n - 1` values adds
0 to `n - 1` inverse pairs, one for each value it lands in front of, so
the count for `n` and `k` is the sum of the counts for `n - 1` and `k -
t` over `t` from 0 to `n - 1`.

| file | mechanism |
|---|---|
| `k_inverse_pairs.kara` ★ | one row of counts at a time, each next row a sliding window sum over the previous one that adds one count and drops one as `k` grows; O(n * k) |
| `k_inverse_pairs_table.kara` | the whole (n + 1) by (k + 1) table, each count the one to its left, plus the one above, less the one above and `i` to the left; O(n * k) time and space |
| `k_inverse_pairs_memo.kara` | the same recurrence top down, recursing on `(n, k - 1)`, `(n - 1, k)` and `(n - 1, k - n)` with each pair stored once computed; O(n * k) |
| `k_inverse_pairs_series.kara` | the generating function: the product of (1 - x^i) for i up to `n`, multiplied out to x^k, against the coefficients of (1 - x)^(-n), which are binomials from factorials and their inverses mod 1,000,000,007; O(n * k) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 16 lines: the two LeetCode examples; twelve
more (one value with no pairs and with one, two values, every pair of
three inverted and one past it, small counts for four, five and ten
values, the most pairs for 20 values, and `n` = 1,000 with `k` =
0, 1 and 1,000); a total and checksum over 200 random cases with `n`
from 1 to 60 and `k` from 0 to 300; and the counts for 30 values over
every `k`, added up, which give 30! mod
1,000,000,007. `k_inverse_pairs.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
for `n` from 1 to 8, every arrangement of 1 to `n` listed one value at a
time, counting the inverse pairs of each. Each of 600 random cases has
an `n` from 1 to 8 with a `k` up to three past the most pairs, an `m`
from 9 to 16 with a `k2` within range, and a count past the most pairs
for `m`.

| | property |
|---|---|
| P1 | the count for (n, k) is the definition's, 0 past the most pairs |
| P2 | (m, k2) and (m, m(m - 1)/2 - k2) have the same count, since reversing an arrangement swaps them |
| P3 | the counts for n over every k add up to n! |
| P4 | m values never have more than m(m - 1)/2 pairs |
| P5 | the count for (m, k2) is the sum of the counts for (m - 1, k2 - t), t from 0 to m - 1 |

It prints `600 cases, 4 arms, 12000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window one count too wide | P1 438, P2 596, P3 463, P4 600, P5 493 |
| M2 | ★: the largest value never added | P1 355, P2 596, P3 529, P5 409 |
| M3 | table: the oldest count dropped one step late | P1 438, P2 596, P3 463, P4 600, P5 493 |
| M4 | table: no row starting at 1 past the first | P1 529, P2 596, P3 529, P4 600 |
| M5 | memo: the count dropped from one place too far right | P1 355, P2 596, P3 529, P5 409 |
| M6 | memo: n arrangements counted with no pairs | P1 529, P2 596, P3 529, P4 600, P5 600 |
| M7 | series: the factor 1 - x^k left out | P1 205, P2 226, P3 529, P5 179 |
| M8 | series: the binomial divided by n! instead of (n - 1)! | P1 401, P3 529, P5 600 |
| E1 | ★: the rows started at one value, which copies the first | 0 |
| E2 | table: one modulus step left out of a value already near range | 0 |
| E3 | memo: a stored count recognised as above -1 | 0 |
| E4 | series: no early stop once i passes k | 0 |

Every property but P4 sees most of them. M1 and M3 compute the same
wrong counts, a window one wider, and M2 and M5 the same, a window one
narrower, which counts arrangements of one value fewer; each pair fails
the same counts. P4 sees the mutants whose counts no longer reach 0 past
the most pairs, the wider windows and M4 and M6, whose rows start wrong.
P5 is blind to M4, which counts 0 everywhere past one value, so the sum
of its 0 counts is its 0 count, and P2 and P4 to M8, which divides every
count by the same `n`, so its counts stay symmetric and its zeros stay
zeros. P3 sees every mutant but M1 and M3 on all 529 cases with more
than one value; those two miss the cases with two values, where a window
one wider still sums to 2 over k = 0 and 1. The four survivors cannot
change an answer: a row started at one value is the window of width one,
which copies the first row; a count between minus the modulus and twice
the modulus is brought into range by one addition and one remainder; `>=
0` and `> -1` are the same test on integers; and once `i` passes `k` the
factor 1 - x^i changes nothing below x^(k+1), so the loop body does
nothing.

## Verification

Every arm prints the same output as `k_inverse_pairs.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `cdca55e210` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends run the ★, table and generating-function arms
under the JIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`, all
with identical output, and the generating-function arm under the
interpreter too; the interpreter printed the first 14 lines of the ★ and
table arms identically and then ran past the 60 s budget on the random
cases. They refuse the memo arm and the differential at type checking:
they still hold the old rule that an argument which is already a `mut
ref`, as `memo` is inside `count`, drops its call-site `mut` marker.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It counts 100 times, each with `n` and
`k` from 500 to 1,000, the problem's most, stepped by the round, putting
each count into a checksum. Every implementation prints `100 rounds:
checksum 324388798`, the Kāra program under `karac __mir-run` included
(in 22 s).

Each implementation is the same rows of window sums over a fresh array
of 64-bit integers per row, with up to two remainders by 1,000,000,007 a
step. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.41 s |
| Rust (`rustc -O`) | 0.41 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.43 s |
| Go | 0.49 to 0.53 s |
| Python | 5.7 to 5.8 s |
| Kāra (`karac build`, legacy) | 0.40 to 0.41 s |
| Kāra (`karac build --mir`) | 0.41 to 0.42 s |

`bench.sh` is the `scripts/new-bench.sh` output unchanged: the legacy
`karac build` builds this program, so it times legacy. The `--mir` row
is the v2 compiled backend, built by hand. Under `karac __mir-llvm-run`
the program prints the same line in 1.7 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

The compiled rows are within a few hundredths of a second of each other,
except Go a tenth behind. The program is not profiled.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
