# 634. Find the Derangement of An Array

A derangement is a permutation of the elements of a set in which no
element appears in its original position. Given an integer `n`, for the
array of the integers 1 to `n` in ascending order, return the number of
derangements it can generate, modulo 10^9 + 7.

```
n = 3  ->  2    ([2,3,1] and [3,1,2])
n = 2  ->  1
```

**Constraints:** `n` from 1 to 10^6.

## Approaches

Every arm is `fn find_derangement(n: i64) -> i64` and works modulo
10^9 + 7 throughout, so no product of two reduced numbers passes
63 bits.

| file | mechanism |
|---|---|
| `find_derangement.kara` ★ | D(n) = (n - 1) * (D(n - 1) + D(n - 2)), kept in two variables from D(0) = 1 and D(1) = 0; O(n) time, O(1) space |
| `find_derangement_table.kara` | the same recurrence filled into a `Vec` of every D(i); O(n) time and space |
| `find_derangement_alternating.kara` | D(n) = n * D(n - 1) + (-1)^n, kept in one variable from D(0) = 1; O(n) time, O(1) space |
| `find_derangement_series.kara` | inclusion-exclusion, D(n) = n! times the sum of (-1)^k / k! for k from 0 to n, the inverse of n! taken by one modular power and the smaller inverses by multiplying back down; O(n + log p) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; eleven
more values of `n` (1, 4, 5, 6 and 10; 12 and 13, whose answers fall
either side of the modulus; 20, 1,000, 99,999 and the largest,
10^6); and a total and checksum over every `n` from 1 to
2,000. `find_derangement.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the permutations of 1 to `n` with nothing in its own place, counted one
at a time by a depth-first search, for `n` from 1 to 8. Each of
1,000 cases draws four sizes: `n` from 1 to 8 for the definition, `m`
from 3 to 500 for the two recurrences, `q` from 1 to 40 for the sum over
fixed places, and `r` from 1 to 15 for the closed form.

| | property |
|---|---|
| P1 | D(n) is the definition's count |
| P2 | D(m) = (m - 1) * (D(m - 1) + D(m - 2)), all three from the arm |
| P3 | D(m) = m * D(m - 1) + (-1)^m |
| P4 | the sum over k of C(q, k) * D(q - k) is q!, since every permutation fixes some k places and deranges the rest |
| P5 | D(r) is r! / e rounded to the nearest integer, taken modulo 10^9 + 7 |

It prints `1000 cases (D(8) = 14833), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the factor `n` taken for `n - 1` | P1 879, P2 1000, P3 1000, P4 969, P5 936 |
| M2 | ★: D(0) taken as 0 | P1 879, P3 1000, P4 969, P5 936 |
| M3 | table: D(n - 1) used twice | P1 879, P3 1000, P4 969, P5 936 |
| M4 | table: D(1) set to 1 instead of D(0) | P1 887, P3 1000, P4 1000, P5 932 |
| M5 | alternating: the signs swapped | P1 1000, P3 1000, P4 1000, P5 1000 |
| M6 | alternating: D(0) taken as 0 | P1 1000, P4 1000, P5 1000 |
| M7 | series: each inverse factorial multiplied by `k + 1` | P1 1000, P2 1000, P3 1000, P4 1000, P5 1000 |
| M8 | series: the power taken to p - 1, not p - 2 | P1 879, P2 1000, P3 1000, P4 969, P5 936 |
| E1 | ★: the sum of the two terms not reduced first | 0 |
| E2 | table: one place more than needed | 0 |
| E3 | alternating: the product reduced before taking off 1 | 0 |
| E4 | series: the base of the power not reduced | 0 |

P1, P4 and P5 each kill all eight. P2 misses six: M2 and M3 make every
answer 0, which satisfies the two-term recurrence, and M4, M5 and
M6 still satisfy it, since any sequence in which D(n) - n * D(n - 1) is
a fixed multiple of (-1)^n does, whatever it starts from. P3 misses only
M6, which is the one-term recurrence itself started from 0. The four
survivors cannot change an answer: the unreduced sum stays below 2 *
10^9 + 14, so its product with `n - 1` stays well inside 63 bits for
every `n` up to 10^6 and reduces to the same value; the extra place is
never read; reducing `i * d` first changes only what is reduced at the
end, not the result; and the base passed to the power is already below
the modulus.

## Verification

Every arm prints the same output as `find_derangement.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `cfcdff46d8` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends run every arm under the JIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`, all with identical output. Under the
legacy interpreter three arms match, and the series arm printed its
first 13 lines identically and then ran past the 60 s budget. The legacy
backends refuse the differential: they still hold the old rule that an
argument which is already a `mut ref`, as `used` is inside the
definition's search, drops its call-site `mut` marker. Legacy is frozen,
so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 random values of `n` from
1 to 10^6 once, then answers each in turn, adding up the answers and
putting each into a checksum. Every implementation prints `100 values of
n: total 204858146, checksum 793936056`, the Kāra program under `karac
__mir-run` included (in 11 s).

Each implementation is the same loop over 64-bit integers, one multiply
and two reductions modulo the constant 10^9 + 7 per step. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
values:

| | time |
|---|---|
| C (`clang -O3`) | 0.46 to 0.47 s |
| Rust (`rustc -O`) | 0.46 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.46 to 0.47 s |
| Go | 0.45 s |
| Python | 4.39 to 4.54 s |
| Kāra (`karac build --mir`) | 0.46 to 0.47 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it types the items of a `Vec`'s `iter()` by value, so `*n` is
an error. That edit is by hand, on top of the `scripts/new-bench.sh`
output. A copy outside the kata without the `*` builds under legacy and
takes 0.47 to 0.48 s, so the v2 build is level with legacy. Under `karac
__mir-llvm-run` the program prints the same line in 1.8 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

Every compiled build takes the same time, within a hundredth of a
second. Each step's multiply and two reductions modulo 10^9 + 7 depend
on the step before, so the loop is likely bound by that chain, which no
compiler can shorten. That is inferred from the timings, not profiled.

## Compiler findings

None. The legacy refusal of the bench program is not filed because
legacy is frozen.
