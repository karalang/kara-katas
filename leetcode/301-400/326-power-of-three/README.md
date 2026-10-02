# 326. Power of Three

Given an integer `n` (any 32-bit value), return `true` if `n == 3^x` for some
integer `x >= 0`. Follow-up: can you do it without loops or recursion?

```
n = 27  ->  true     (3^3)
n = 0   ->  false
n = -1  ->  false
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `power_of_three.kara` ★ | divide out every factor of 3, then check the rest is 1 | `O(log n)` time, `O(1)` space |
| `power_of_three_divisor.kara` | `n > 0 and 3^19 % n == 0` | `O(1)` time and space |
| `power_of_three_log.kara` | guess the exponent as `round(ln n / ln 3)`, then check it exactly | `O(log n)` time, `O(1)` space |
| `power_of_three_table.kara` | membership in a `Set` of all twenty powers `3^0 .. 3^19` | `O(1)` expected per query |
| `differential.kara` | the four arms on 220,203 inputs, six properties | — |
| `bench/power_of_three.kara` | 40 re-classifications of 300,000 values by the ★ arm | — |

Every arm prints the same 18 lines: the three examples, eight more single
values, the largest 32-bit power `3^19 = 1162261467` with its two neighbours,
both ends of the 32-bit range, a pass over every power `3^0 .. 3^19` and the
values one either side of it, and a sweep over `[-1000, 1000000]` (13
powers, sum 797161). The four arms' output is byte-identical, and
`power_of_three.py` mirrors both the ★ arm and, with `--divisor`, the
divisor arm.

## Why the logarithm is only a guess

The shortcut everyone reaches for is "`log3(n)` is a whole number", spelled
`ln(n) / ln(3)`. It is wrong for five of the twenty powers, on both Kāra
backends and in Python alike, because the quotient lands just under the
integer:

| `n` | `ln(n) / ln(3)` |
|---|---|
| `3^5 = 243` | `4.999999999999999` |
| `3^10` | `9.999999999999998` |
| `3^13` | `12.999999999999998` |
| `3^15` | `14.999999999999998` |
| `3^17` | `16.999999999999996` |

The `log10` spelling happens to be exact for all twenty, which is why it is
the one usually quoted. Relying on it is relying on rounding luck in a
particular libm. `power_of_three_log.kara` uses the logarithm only to GUESS
the exponent, rounds the guess to the nearest integer, and then rebuilds
`3^k` with exact integer multiplication and compares. A float error smaller
than one half cannot change the answer, so the arm is correct for any libm
that gets the logarithm to within a quarter.

The divisor arm answers the follow-up. 3 is prime, so the divisors of `3^19`
are exactly `3^0 .. 3^19`, and `3^19` is the largest power of three that fits
in 32 bits; a positive `n` is a power of three exactly when it divides
`1162261467`. The same trick works for any prime base and for no composite
one: `6^k` could not be tested by dividing `6^big`, since 2 and 3 divide it
too.

The table arm builds its `Set` once in `main` and passes it by `ref`, since
Kāra has no runtime-initialised globals. Nothing walks the set, so its
per-process iteration order never shows in the output.

## Differential

`differential.kara` runs all four arms on every `n` in `[-100, 200000]`,
every `3^k + d` for `k` in `0..19` and `d` in `-2..2`, both 32-bit extremes,
and 20,000 pseudo-random 32-bit values.

| | property |
|---|---|
| P1 | all four arms agree |
| P2 | nothing at or below 0 is accepted |
| P3 | for `0 < n <= 3^18`, `n` is accepted exactly when `3n` is |
| P4 | an accepted `n` other than 1 is divisible by 3 |
| P5 | the exhaustive range holds exactly the powers a multiplication loop finds in it, by count and by sum |
| P6 | every `3^k` is accepted, and no `3^k + d` with `d != 0` and `3^k > 3` is |

`checked 220203, accepted 34, failures 0`, and all properties hold, on every
surface.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | divide arm: `n < 0` instead of `n <= 0` | **killed** | hangs at `n = 0`, since `0 % 3 == 0` forever |
| M2 | divisor arm: `n >= 0` instead of `n > 0` | **killed** | panics, division by zero |
| M3 | divisor arm divides `3^18` instead of `3^19` | **killed** | P1 at `1162261467` |
| M4 | log arm truncates the guess instead of rounding it | **killed** | P1 at `243` and `59049` |
| M5 | table arm stops at `3^18` | **killed** | P1 at `1162261467` |
| M6 | divide arm: `m <= 1` instead of `m == 1` | silent (equivalent) | — |
| M7 | divide arm stops dividing at 3 | **killed** | P1, P3 at `n = 1` and `n = 3` |
| M8 | log arm accepts `3^k >= n` instead of `==` | **killed** | P1 on 112,342 inputs |

M6 is equivalent: dividing a positive `n` by 3 can never reach 0, so the
remainder `m` is at least 1 and `m <= 1` means `m == 1`. M3 and M5 are the
kind of mistake the boundary values are there for: they agree with the other
arms on every input except the single largest power, which only the extremes
and the `3^k + d` pass reach.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. All five programs are
valgrind-clean at `-O0`. The four arms' output is byte-identical to
`power_of_three.py` and `power_of_three.py --divisor`.

`scripts/surface-sweep.py --filter 326- --timeout 400` reports `5 programs ·
5 clean · 0 DIVERGENCES`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 295379457`), and `karac run --interp` prints the same sink.

## Benchmarks

`bench/power_of_three.kara` and its four mirrors time the ★ arm as written.
300,000 values are built once, a third each of: a power of three `3^0 ..
3^19`, a power of three plus or minus one, and a random 32-bit value. The
powers run the divide loop to the end (up to 19 rounds). A neighbour of a
power is never divisible by 3, so it stops at the first remainder, and so do
two thirds of the random values. Each of 40 punches replaces one value at
a random position and classifies the whole array again. The count and sum of
accepted values are folded into a rolling hash, which is the sink.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10189+ga44377460` (plus B-2026-10-02-40's interpreter-only
change, which does not touch codegen), measured 2026-10-02. Python is its own
lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 206.4 ms ± 3.4 | 1.00× |
| c `clang -O3` | 208.1 ms ± 3.9 | 1.01× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 213.3 ms ± 4.3 | 1.03× |
| **kāra `karac build`** | **213.5 ms ± 5.1** | **1.03×** |
| rust `-O -C overflow-checks=on` (equal-safety) | 214.7 ms ± 3.1 | 1.04× |
| rust `-O` | 219.3 ms ± 3.6 | 1.06× |
| go `go build` | 238.1 ms ± 2.5 | 1.15× |
| python 3 | 3102 ms ± 24 | 15.0× |

**Kāra ties C and Rust.** The six C, Rust and Kāra rows sit within 6% of each
other. With standard deviations of 3 to 5 ms, the gaps of 3% or less between
Kāra, C and Rust with overflow checks are within noise. Go is 15% behind.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 94.9 ms ± 9.4 | 15.8 KiB | 3.7 MiB |
| rust | 132.1 ms ± 4.9 | 3864.3 KiB | 4.4 MiB |
| kāra | 461.8 ms ± 9.0 | 396.6 KiB | 4.7 MiB |
| go | — | 2179.1 KiB | 4.0 MiB |
| python | — | — | 17.7 MiB |

`karac build` is 4.9× clang's cold compile and 3.5× rustc's. Its binary is
25× clang's and 9.7× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No correctness gaps.** All five programs were byte-identical on every
surface from the first run. The interpreter was the problem: correct, but
slow. Two of the three findings are fixed.

- **B-2026-10-02-40 (perf, medium, fixed in kara `74d4fa7d2` and
  `c3ea28d83`): every call in `karac run --interp` re-walked the callee's
  whole body through a dozen ownership predicates**, so a call cost time in
  proportion to the callee's size: 4.6 ms a call for a forty-line function.
  A per-run memo of those walks, keyed by the function's address, took a
  2,000-call loop into a 40-line function from 9.32 s to 0.55 s.
- **B-2026-10-02-41 (perf, medium, fixed in kara `fcd99fa94`): the
  interpreter copied a function's entire body every time it looked up the
  function's name.** A function value held its `Block` by value and
  `Env::get` returns a clone; a profile of a loop calling a one-line
  function counted five copies per call, 40% of its instructions with their
  frees. The body is now shared.
- **B-2026-10-02-42 (missing-feature, low, open): `f"{d:+}"` is rejected**,
  as "unsupported type `+`". The format-spec grammar has no sign flag, which
  Rust and Python both have, and the message calls the flag a type. The
  differential spells that line `3^{k} + {d}` instead.

Together the two fixes take the ★ arm under `--interp` from 102 s to 9.7 s
and the differential from 60 s (with only the first fix) to 29 s. That is still far from
the JIT's 0.3 s for the differential; the remaining per-call cost is
recorded in B-2026-10-02-40's close.

`karac check` reported six E0218 diagnostics on the differential, all the
missing `mut` marker on a `mut ref` argument, and `karac fix` applied all
six. That says little about the diagnostics: the author already knows the
language, which is why authoring like this never counts toward the
machine-fix rate.
