# 343. Integer Break

Given an integer `n` (`2 <= n <= 58`), break it into the sum of at least two
positive integers and return the largest product of those integers.

```
n = 2   ->  1     (1 + 1)
n = 10  ->  36    (3 + 3 + 4)
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `integer_break.kara` ★ | `best[i]` over every first part `j`, keeping the rest whole or breaking it further | `O(n^2)` time, `O(n)` space |
| `integer_break_greedy.kara` | take threes while more than four is left | `O(n)` time, `O(1)` space |
| `integer_break_pow.kara` | the closed form `3^q`, `3^(q-1) * 4` or `3^q * 2` by `n mod 3` | `O(log n)` time, `O(1)` space |
| `integer_break_memo.kara` | top-down recursion over "what a total is worth as a part", with a memo | `O(n^2)` time, `O(n)` space |
| `integer_break_23.kara` | a table over sums of 2s and 3s only | `O(n)` time and space |
| `differential.kara` | the five arms and a brute force on every `n` in `2..119`, seven properties | — |
| `bench/integer_break.kara` | 20 re-solves of 20,000 random `n` by the ★ arm | — |

Every arm prints the same 62 lines: the two examples, every `n` the problem
allows with its answer, their sum (5230176595), and two values past the
bound, `100` and `119`. 119 is the largest `n` whose answer, `2 * 3^39 =
8105110306037952534`, fits in an `i64`; at 120 the answer is `3^40`, and
Kāra's checked arithmetic would trap rather than wrap. The five arms' output
is byte-identical, and `integer_break.py` mirrors both the ★ arm and, with
`--greedy`, the greedy arm.

## Why only 2s and 3s

A best break never needs a part other than 2 or 3, once `n >= 4`:

- a part `p >= 5` is worth less than the two parts `2` and `p - 2`, since
  `2(p - 2) > p` exactly when `p > 4`;
- a 4 is worth the same as `2 + 2`;
- a 1 adds to the sum and nothing to the product.

Three 2s (product 8) lose to two 3s (product 9), so a best break has at most
two 2s, which leaves one shape per remainder of `n mod 3`. The greedy, power
and 2-and-3 arms all lean on this; the DP and memo arms do not, and the
differential checks the argument by comparing them, and all five against a
brute force over every partition up to `n = 40`.

`n = 2` and `n = 3` are the exceptions every shortcut has to special-case.
The break must have at least two parts, so the answers are `1 * 1` and
`1 * 2`, below `n` itself. The ★ arm handles this without a special case by
keeping the two meanings apart: `best[i]` is the best product of a real
break of `i`, while a part of a larger break can also be kept whole, which
is why each step compares `j * (i - j)` as well as `j * best[i - j]`. The
memo arm draws the same line differently: `value(i)` is what a total is
worth as a part (at least `i`), and only the top level is forced to split.

In the DP no intermediate value can overflow before the answer does: every
candidate a step compares is the product of a real break of `i`, so none
exceeds `best[i]`. That is why the arm runs unchanged up to 119.

## Differential

`differential.kara` runs all five arms on every `n` in `2..119` and a brute
force over all partitions for `n <= 40`.

| | property |
|---|---|
| P1 | all five arms agree |
| P2 | they equal the brute force, for `n <= 40` |
| P3 | the answer grows strictly with `n` |
| P4 | `f(n + 3) == 3 * f(n)` for `n >= 4` |
| P5 | `f(n) >= n - 1`, and `f(n) >= n` for `n >= 4` |
| P6 | `f(a + b) >= f(a) * f(b)` for `a, b >= 2`: two breaks side by side are a break of the sum (3,422 pairs) |
| P7 | for `n >= 4`, `f(n)` is `2^e * 3^k` with `e <= 2` |

`failures 0` and all properties hold, on every surface, with the answers
summing to 35232087804 mod `1e9+7`, the same as a Python closed form.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run under
`--interp`.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | DP: drop the "keep the rest whole" candidate | **killed** | P1 at `n = 2`, 392 failures |
| M2 | DP: drop the "break the rest further" candidate | **killed** | P1 at `n = 8` (16 for 18) |
| M3 | greedy: `while rest > 3` | **killed** | P1 at `n = 4` |
| M4 | greedy: special-case `n <= 4` instead of `n <= 3` | **killed** | P1 at `n = 4` only |
| M5 | power: `3^q + 1` for `n = 3q + 1` | **killed** | P1 at `n = 7` |
| M6 | memo: a total is worth 0 kept whole, not itself | **killed** | P1 at `n = 2` |
| M7 | memo: never store a solved total | silent on values | runs past the 300 s limit |
| M8 | 2-and-3 table: `f[0] = 0` | **killed** | P1 at `n = 4` |
| M9 | 2-and-3 table: `i > 3` instead of `i >= 3` for the 3 option | **killed** | P1 at `n = 6` (8 for 9) |
| M10 | brute force: a single part counts as a break | **killed** | P2 at `n = 2` and `n = 3` |
| M11 | brute force: the last part may not take all that is left | **killed** | P2 at `n = 2` |
| M12 | DP: start the table at 3 | **killed** | P1 at `n = 2` |

M7 is the only survivor, and it is value-equivalent: without the memo the
recursion still returns the right answers, but it re-solves every total and
takes exponential time, so the run never reaches the end. M4 is the
boundary case: only `n = 4` tells it apart.

M1 and M12 at first did not report cleanly. With every DP answer 0, P7's
factoring loop spun forever on 0 and P6 divided by 0; both properties now
skip a non-positive answer, which P1 and P5 already report.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, after the auto-par fix below.
All six programs are valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0` and
`KARAC_BUF_CACHE=0` (`All heap blocks were freed`, `0 errors`). The five arms' output is byte-identical to `integer_break.py`
and `integer_break.py --greedy`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 445830989`). `karac run --interp` was not run on the kernel: at
about 240 million inner steps it would take tens of minutes.

## Benchmarks

`bench/integer_break.kara` and its four mirrors time the ★ arm as written.
20,000 values of `n` are drawn once, uniformly from `[2, 58]`. Each of 20
punches replaces one value at a random position and solves every value
again, so a punch runs the `O(n^2)` table 20,000 times and allocates a
fresh table each time, as the arm does. The sum of the answers is folded
into a rolling hash, which is the sink.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10448+g76727438c`, measured 2026-10-05. The timed lane is built
with `KARAC_AUTO_PAR=0`, so B-2026-10-05-30's auto-par fix, which landed
after this build, does not touch it. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 265.1 ms ± 10.9 | 1.00× |
| c `clang -O3` | 327.7 ms ± 8.8 | 1.24× |
| rust `-O -C overflow-checks=on` (equal-safety) | 329.8 ms ± 11.2 | 1.24× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 333.4 ms ± 13.6 | 1.26× |
| go `go build` | 368.0 ms ± 19.8 | 1.39× |
| **kāra `karac build`** | **370.7 ms ± 8.6** | **1.40×** |
| rust `-O` | 392.5 ms ± 9.4 | 1.48× |
| python 3 | 18947 ms ± 77 | 71.5× |

**Kāra is 12% behind Rust with overflow checks** and level with Go. The gap
was not investigated; both checked languages bounds-check `best[i - j]` and
`best[i]`, and both allocate the table per call. Rust without overflow
checks came out slower than Rust with them, by more than the noise, so the
ordering among the scalar rows says more about code layout than about
safety checks. C built for AVX2 is 24% ahead of baseline C; where that
comes from was not investigated either.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 88.2 ms ± 1.6 | 15.8 KiB | 1.8 MiB |
| rust | 143.0 ms ± 4.7 | 3863.5 KiB | 2.3 MiB |
| kāra | 315.3 ms ± 10.2 | 341.6 KiB | 2.5 MiB |
| go | — | 2178.7 KiB | 7.5 MiB |
| python | — | — | 8.0 MiB |

`karac build` is 3.6× clang's cold compile and 2.2× rustc's. Its binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

- **B-2026-10-05-30 (run-vs-build, high): auto-par fanned out a summing loop
  whose body also printed, and the lines came out in a different order on
  every run.** `main` sums the answers while printing them, `for n in 2..59
  { let p = integer_break(n); println(..); sum += p; }`. Under the default
  `karac build` and under `karac run` (LLJIT), the DP and memo arms printed
  2 to 32 in order and then interleaved 33 onward with 47 onward, a
  different permutation on each run of one binary. Auto-par had recognised
  `sum += p` as a reduction and run the iterations on workers that print
  straight to the console. Its other lane, for loops that write disjoint
  array slots, already declined a printing body; the reduction lane never
  asked. The greedy, power and 2-and-3 arms looked fine only because their
  bodies are too cheap for the cost model to fan out. Fixed in the kara
  repo: the reduction lane now declines a body that prints, directly or
  through a call, or performs an ordered resource effect.

`karac check` reported one error while writing the memo arm: forwarding the
`memo` parameter, already a `mut ref`, as `mut memo`. The call-site `mut`
marker belongs only on a fresh owned binding, and `karac fix` removed it.
The author already knows the language, so this does not count toward the
machine-fix rate.
