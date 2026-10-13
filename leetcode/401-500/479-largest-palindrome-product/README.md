# 479. Largest Palindrome Product

Given an integer `n`, return the largest palindromic integer that can
be represented as the product of two `n`-digit integers. Since the
answer can be very large, return it modulo `1337`.

```
n = 2  ->  987     (99 x 91 = 9009, 9009 % 1337 = 987)
n = 1  ->  9
```

**Constraints:** `1 <= n <= 8`.

## Approaches

Every arm is `fn largest_palindrome(n: i64) -> i64`. For `n >= 2` the
largest product has `2n` digits and so does the palindrome; for
`n = 1` the answer is the one-digit 9 (3 × 3), and every arm returns it
directly.

| file | mechanism |
|---|---|
| `largest_palindrome_product.kara` ★ | the `2n`-digit palindromes from the largest down, each built from its left half; for each, a factor from `10^n - 1` down while its square still reaches the palindrome, and the first that divides it wins |
| `largest_palindrome_product_sqrt.kara` | write the factors as `10^n - x` and `10^n - y`, with `a = x + y`: the product is `(10^n - a) × 10^n + x y`, so for `a = 1, 2, ...` the left half is `10^n - a`, the right half must be its mirror `lo`, and `x + y = a`, `x y = lo` have whole solutions exactly when `a² - 4 lo` is a perfect square; no division search at all |
| `largest_palindrome_product_eleven.kara` | as the ★ arm, but a palindrome with an even number of digits is a multiple of 11, and 11 is prime, so only multiples of 11 are tried as the factor |
| `largest_palindrome_product_text.kara` | each palindrome spelled out (`f"{half}"` and its reversed chars) and read back with `i64.from_str_radix`; any factorization will do, so the factor is searched upward, from the smallest that leaves an `n`-digit cofactor |
| `differential.kara` | the four arms on every `n`, two properties |

Every arm prints the answer for each `n` from 1 to 8, the problem's
whole domain: `9, 987, 123, 597, 677, 1218, 877, 475`.
`largest_palindrome_product.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

With eight inputs there is nothing to draw at random, so
`differential.kara` holds copies of the four arms and checks every one
on every `n`.

| | property |
|---|---|
| P1 | the answer is the largest palindrome over every pair of `n`-digit numbers, by brute force (from the top, until no product can beat the best found), modulo 1337; `n` = 1 to 6 |
| P2 | the answer is LeetCode's, for every `n` from 1 to 8 |

From `n = 7` the brute force passes the MIR interpreter's step limit
(`step limit exceeded` after about 400 s), so P1 stops at 6 and P2,
whose table is the problem's published answers, covers 7 and 8. It
prints `n = 1 to 8, 4 arms, 56 checks, 0 failures` under
`karac __mir-run`, in 14 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no special case for `n = 1` | P1 1, P2 1 |
| M2 | ★: the factor search starts at `10^n - 2` | P1 3, P2 4 |
| M3 | sqrt: the discriminant is `a² - 2 lo` | P1 5, P2 7 |
| M4 | sqrt: any `a` with `a² >= 4 lo` is taken, square or not | P1 5, P2 7 |
| M5 | eleven: the largest multiple of 11 is skipped | P1 3, P2 4 |
| M6 | eleven: only every other multiple of 11 is tried | the run stops: step limit |
| M7 | text: the mirrored half drops its first digit | P1 5, P2 7 |
| M8 | text: the factor goes up by two | P1 2, P2 3 |

M6 skips the multiple of 11 that divides the right palindrome for at
least one `n` (which one is not known, since the run never finishes)
and goes on through so many smaller palindromes that the run passes the
interpreter's step limit before it can print a count. Six first drafts
were replaced: five survived on every `n`, and say something about the
problem, and one did not run.

- ★, the cofactor not checked to have `n` digits: a `2n`-digit
  palindrome divided by an `n`-digit factor always leaves at least
  `10^(n-1)`, so the check never fails.
- ★, only every other factor tried (`factor -= 2`): the largest
  palindromes all end in 9, so they are odd and both factors are odd,
  and the search starts at the odd `10^n - 1`.
- sqrt, either of the integer square root's correction loops changed
  (two drafts): the discriminants stay below 2^52, where `f64`'s square
  root of a perfect square is exact, so the loops never run.
- text, the factor search started at `palindrome / upper` rounded down
  rather than up: on these eight inputs the one extra factor it can try
  never changes the answer.
- text, collecting the left half's chars unreversed did not run when
  the kata was written: `let right: String = left.chars().collect();`
  was refused by both MIR backends, which was B-2026-10-13-10, below.

## Verification

All four arms print the same output as `largest_palindrome_product.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file, the
bench program included. The differential prints `56 checks, 0
failures` on both. The four arms and the differential also run clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak.

On the frozen legacy backends, `karac run --interp` prints the same
output on every arm and `0 failures` on the differential. LLJIT and
legacy `karac build` agree on the ★, sqrt and eleven arms (a
`KARAC_AUTO_PAR=1` build too), but refuse the text arm and the
differential: "`Iterator.rev()` is not yet supported under `karac
build`/`karac run` (codegen) for this chain shape", on
`left.chars().rev().collect()`. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm on every `n` from 1 to 8, ten times
over. Every implementation prints `10 rounds of n = 1 to 8: answers add
up to 49630, checksum 765645361`, the Kāra program under `karac __mir-
run` included (in 47 s). A single round takes 0.10 to 0.11 s in C,
Rust, Go and both Kāra builds, a tenth of ten, so none of them hoists
the repeated calls out of the loop.

Every mirror is the same loops over 64-bit integers, which is likely
why the compiled rows land together: the inner loop is a 64-bit
`palindrome % factor` per step, and no language can avoid that division
(inferred, not profiled). Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.95 to 0.97 s |
| Rust (`rustc -O`) | 0.98 to 0.99 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.98 to 1.02 s |
| Go | 0.98 to 1.00 s |
| Python | 18.2 to 18.4 s |
| Kāra (`karac build`) | 0.94 to 1.02 s |
| Kāra (`karac build --mir`) | 0.97 to 1.04 s |

The legacy `karac build` builds and runs this program correctly, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
that build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `b0b1557b39`. Under
`karac __mir-llvm-run` the program prints the same line in 1.8 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-10** (fixed in kara `5a562a4b64`): on the MIR backends,
  `let s: String = text.chars().collect();` stopped with "collecting
  chars into this type is not lowered yet", while `karac check` and the
  legacy interpreter accepted it, and the same collect after `.rev()`,
  `.filter(..)`, `.skip(..)`, `.take(..)` or `.map(..)` ran. The MIR
  builder special-cased a bare `chars().collect()` and handled only a
  `Vec[char]` destination. Met in a draft of mutant M7; the text arm
  itself collects after `.rev()` and runs.
