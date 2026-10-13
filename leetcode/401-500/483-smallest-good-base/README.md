# 483. Smallest Good Base

Given an integer `n` represented as a string, return the smallest good
base of `n`.

We call `k >= 2` a good base of `n` if all digits of `n` base `k` are
1s.

```
n = "13"                   ->  "3"                    (13 is 111 in base 3)
n = "4681"                 ->  "8"                    (4681 is 11111 in base 8)
n = "1000000000000000000"  ->  "999999999999999999"   (11 in that base)
```

**Constraints:** `n` is an integer in the range `[3, 10^18]`, with no
leading zeros.

## Approaches

Every arm is `fn smallest_good_base(n: String) -> String`, the
problem's own signature: it borrows the text, reads it with `i64.parse`
and returns the base as text. `n` is `m` 1s in base `k` when `n = 1 + k
+ ... + k^(m-1)`. Two 1s always work, with `k = n - 1`, and more 1s
mean a smaller base, so each arm looks for the most 1s that work.

| file | mechanism |
|---|---|
| `smallest_good_base.kara` ★ | `n` lies between `k^(m-1)` and `(k+1)^(m-1)`, so `k` can only be the integer `(m-1)`-th root of `n`: for `m` from 63 down to 3 the root comes from `f64.pow`, and it and the integer above it are checked exactly, with a sum that stops before it can pass `n` |
| `smallest_good_base_binary.kara` | for each `m` from 62 down, a binary search over `k` from 2 to `n - 1`; the sum is taken with `checked_mul` and `checked_add`, and an overflow counts as larger than `n` |
| `smallest_good_base_newton.kara` | the same roots as the ★ arm, but in integers: Newton's method from a power of two above the root, with `n / x^(d-1)` taken one division at a time so nothing overflows; then `n`'s digits in that base are read |
| `smallest_good_base_scan.kara` | four or more 1s need `k^3 < n`, so every such base is at most `10^6`: try them in order, reading `n`'s digits. Past that, three 1s can only be in base `isqrt(n)` (`k^2 < k^2 + k + 1 < (k+1)^2`), and otherwise the answer is `n - 1` |
| `differential.kara` | the four arms on every `n` from 3 to 1,000 and 1,000 random values, three properties |

Every arm prints the same 11 lines: the three LeetCode examples, the
smallest `n` (3, base 2), 15 (1111 in base 2), 21 (111 in base 4), `10^6`
(only `n - 1`), `2^51 - 1` (51 1s in base 2), `10^18 - 1`, 919818571896748567
(seven 1s in base 986), and for 300 random cases (two in three built as
3 to 8 1s in a base from 2 to 2,001, the rest random up to `10^12`, or
`10^18` one time in ten) the sum of the bases and a checksum.
`smallest_good_base.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on 1,000
random values, one in three from 3 to 5,000, one in three built as 3 to
12 1s in a random base (from 2 to 2,000, or to 1,000,000 one time in
twenty, the value at most `10^18`), and one in three random up to
`10^12` (to `10^18` one time in forty), and then on every `n` from 3 to
1,000.

| | property |
|---|---|
| P1 | `n` is all 1s in the base returned, which is from 2 to `n - 1` |
| P2 | for `n` up to 5,000, it is the smallest such base, found by trying every base from 2 up |
| P3 | for `n` built as three or more 1s in base `k`, the base returned is at most `k` |

It prints `n = 3 to 1000 and 1000 random cases, 4 arms, 14656 checks, 0
failures` under `karac __mir-run`, in 33 s, and a count for each
property when anything fails.

The sweep of every small `n` was added after the first round of
mutants: two of them (M4 and M7 below) are wrong on exactly one input
each, 31 and 3, which 500 random draws from 3 to 5,000 had missed. The
first version (1,500 random values, a sweep to 2,000, and more of the
largest values) took 71 s, past the corpus runner's 60 s limit, and was
cut down to this one; the mutants were run again on it.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: three 1s are never tried | P2 35, P3 41 |
| M2 | ★: the counts start at 8 1s, not 63 | P2 1, P3 12 |
| M3 | binary: a sum too small moves the low end two past the middle | P2 20, P3 135 |
| M4 | binary: the counts are tried from 3 up | P2 1 |
| M5 | newton: Newton's method may start below the root | P2 16, P3 227 |
| M6 | newton: the step divides by `x` one time too few | P2 48, P3 332 |
| M7 | scan: base 1 is allowed for three 1s | P1 1, P2 1 |
| M8 | scan: a digit 0 is taken as a 1 | P1 1986, P2 1321 |

M4 finds the largest base with three or more 1s rather than the
smallest, which differs only when `n` has two such bases. Up to 5,000
that is 31 alone (11111 in base 2, 111 in base 5), the one failure. M7
is wrong only for `n = 3`, where `isqrt(3) = 1` and `1 + 1 + 1 = 3`.

Five first drafts survived and were replaced:

- ★, the integer above the float root not tried: `f64.pow` never fell
  short of the true root. Checked separately with Python's float power
  (the C library's `pow`): for four or more 1s, every base whose value
  is at most `10^18`, over a million in all, and for three 1s, about
  700,000 bases from 2 to `10^9`; the root was never below the base.
- ★, the early stop comparing the term with `n / k` instead of `(n -
  sum) / k`: the sum can then pass `n` by one term, which `sum == n`
  rejects, and `term * k` still stays below `n`.
- ★, the early stop comparing the term with `n - sum`, not divided by
  `k`: survived every case too. The product it lets through can be up
  to `k` times larger; whether it can ever overflow for `n <= 10^18`
  was not worked out.
- ★, `sum >= n` instead of `sum == n`: the early stop never lets the
  sum pass `n`, so the two are the same test.
- newton, the digit count not checked against `m`: on every case, a
  base that is the integer `(m-1)`-th root and has all digits 1 had `m`
  digits.

## Verification

All four arms print the same output as `smallest_good_base.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `14656 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on every arm: LLJIT, legacy `karac
build` and a `KARAC_AUTO_PAR=1` build print the same output, and so
does the differential's legacy build. `karac run --interp` agrees on
the ★, binary and newton arms; on the scan arm it prints the ten fixed
lines and does not reach the random cases within 300 s, and the
first, larger version of the differential did not finish on it within
900 s (the tree-walking interpreter is slow on the scan arm's
million-step loops; the final version was not run there). The
`KARAC_AUTO_PAR=1` build of the binary arm also writes "Error return
trace: unavailable — the `?` chain was split across parallel tasks" to
stderr, though nothing fails: its `?` only turns an overflow into
`None`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on 50,000 values, each passed in and
out as text the way the problem's signature has it: two in three count
down from `10^18` by 7, and every third is 3 to 8 1s in base `k`, for
`k` from 2 up. Every implementation prints `50000 values: bases add up
to 24865112 (mod 1000 each), checksum 46384329`, the Kāra program under
`karac __mir-run` included (in 36 s).

Every mirror takes the same float root with the C library's `pow` (Rust
`f64::powf`, Go `math.Pow`, Python `**`) and the same exact check, and
converts the number to text and back with the language's own routines
(`snprintf` and `strtoll` in C). Most of the time is the up to 61 calls
to `pow` per value, which is likely why the compiled rows land together
(inferred, not profiled). Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.64 s |
| Rust (`rustc -O`) | 0.54 to 0.60 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.58 to 0.60 s |
| Go | 0.72 to 0.74 s |
| Python | 17.5 to 18.6 s |
| Kāra (`karac build`) | 0.58 to 0.61 s |
| Kāra (`karac build --mir`) | 0.56 to 0.58 s |

The legacy `karac build` builds and runs this program correctly, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
that build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `b0b1557b39`. Under
`karac __mir-llvm-run` the program prints the same line in 1.5 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

None on the v2 backends. `f64` raises to a power with `pow`, not
Rust's `powf`; the first draft's `powf` was refused with "no method
'powf' on type 'f64'", which is the language's name for it, not a
finding.
