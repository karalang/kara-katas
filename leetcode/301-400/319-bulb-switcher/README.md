# 319. Bulb Switcher

`n` bulbs start off. Round 1 toggles every bulb, round 2 every second bulb,
round `i` every `i`-th bulb, up to round `n`. How many are on at the end?

```
n = 3      off off off  ->  on on on  ->  on off on  ->  on off off   ->  1
n = 0  ->  0        n = 4  ->  2        n = 99 ->  9        n = 100 -> 10
```

The answer is `floor(sqrt(n))`, and the reason is short: bulb `b` is toggled
once per **divisor** of `b`, so it ends on exactly when `b` has an odd number
of divisors. Divisors come in pairs `(d, b/d)`, and the only way a pair fails
to be two distinct numbers is `d == b/d` — that is, `b` is a perfect square.
The bulbs left on are the squares `1, 4, 9, …` up to `n`, and there are
`floor(sqrt(n))` of them.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `bulb_switcher.kara` ★ | Newton's **integer** square root | `O(log log n)` |
| `bulb_switcher_count.kara` | count `k` with `k*k <= n`; no square root at all | `O(sqrt n)` |
| `bulb_switcher_simulate.kara` | run every round literally, then count | `O(n log n)` |
| `bulb_switcher_divisors.kara` | count each bulb's divisors, keep the odd ones | `O(n sqrt n)` |
| `differential.kara` | four arms, twelve properties | — |
| `bench/bulb_switcher.kara` | 10 passes of the **simulation** over 6 M bulbs | — |

## Four ways to count the squares

**★ Newton, on integers.** Once you believe the answer is `floor(sqrt(n))`,
one real problem is left: computing an integer square root without touching a
float. `(i64) sqrt((double) n)` is wrong near the top of the range, because a
double has 53 bits of mantissa and an i64 has 63 — beyond `2^53` the
conversion rounds, and the result can land one off.

That is not hypothetical, and this kata carries the witness as a demo case.
At `n = 4503599761588224`:

```
(long long) sqrt((double) n)  in C       ->  67108865      wrong
int(math.sqrt(n))             in Python  ->  67108865      wrong
67108865 * 67108865                      =   4503599761588225  =  n + 1
answer                                   ->  67108864
```

Newton's iteration `x -> (x + n/x) / 2` has no such window. In integer
arithmetic it converges downward from any overestimate and settles exactly on
`floor(sqrt(n))`; the loop stops on the first step that fails to decrease. The
largest intermediate it ever forms is `n + n/n = n + 1`, on the first
iteration, so every `n` below `i64::MAX` is safe from overflow — which matters
in a language that traps on overflow rather than wrapping.

**Count them instead.** Same conclusion, none of the machinery: walk
`k = 1, 2, 3, …` and stop when `k*k` passes `n`. No division, no convergence
argument, no iteration to get wrong — just the definition of "how many squares
are there". It is `O(sqrt n)` against `O(log log n)`, about 31,600 iterations
against six for `n` near a billion, and that gap is exactly what the ★ arm
buys. It also makes a good cross-check: an isqrt that is one off on some
awkward `n` cannot hide behind an arm that never computes a square root.

**Simulate it.** This arm does what the statement says and nothing else:
allocate `n + 1` bulbs, run round `i` for every `i` flipping every `i`-th bulb,
count what is left on. No divisors, no squares, no square root — none of the
reasoning above appears here at all, which is what makes it the oracle. The
cost is the harmonic sum, `n * (1 + 1/2 + … + 1/n) ≈ n ln n`: about fourteen
million toggles for `n` of a million, against six Newton iterations for the
same number. Index 0 is allocated and never touched so that bulb `b` lives at
slot `b` — one wasted slot to avoid an off-by-one everywhere else is a good
trade in an arm whose whole job is to be obviously correct.

**Count divisors.** This one takes the divisor half of the argument and stops
there: bulb `b` ends on when `b` has an odd number of divisors, so count
divisors and test the parity. It never notices that "odd divisor count" and
"perfect square" are the same predicate, which makes it a *second* independent
oracle — the ★ arm's answer is a square root and this arm's is a parity tally,
with no shared step to be wrong in together. Divisors are counted by trial
division, adding two per hit (`d` and `b/d`) except when `d * d == b`, where
the pair collapses to one. That collapse is the perfect-square story arriving
from the other side, and it is the one line worth staring at: drop its guard
and every square's count turns even and the answer is identically zero.

## Differential

`karac run differential.kara` sweeps every `n` from 0 to 520 through all four
arms, checks every bulb's state and divisor parity individually, replays the
rounds in three different orders, walks the state after every prefix of rounds
for `n` up to 70, sweeps a 20,000-wide band of perfect squares, and finishes on
409 large `n` — nine hand-picked around `2^52`, `2^53` and `floor(sqrt(i64max))²`,
plus 400 random 60-bit draws, which is the range where a double-backed sqrt
starts rounding.

```
cases 521 squares 22 bulbs 135460 prefix-rounds 2485 big-n 409
DIFFERENTIAL OK
```

| # | property |
|---|---|
| P1 | the Newton arm agrees with the simulation |
| P2 | the counting arm agrees with the simulation |
| P3 | the divisor arm agrees with the simulation |
| P4 | the answer is non-decreasing in `n` |
| P5 | `f(n) - f(n-1)` is 1 exactly at perfect squares and 0 everywhere else |
| P6 | `f(n)² <= n < (f(n)+1)²` — the defining bracket of an integer square root |
| P7 | `f(k*k) == k` and `f(k*k - 1) == k - 1`, swept over `k` |
| P8 | in the final simulated state, bulb `b` is on iff `b` is a perfect square |
| P9 | `b` has an odd number of divisors iff `b` is a perfect square |
| P10 | after `r` rounds, bulb `b` is on iff `b` has an odd number of divisors `<= r` |
| P11 | the final state does not depend on the ORDER the rounds run in — reversed, and a seeded shuffle |
| P12 | running the whole round set twice returns every bulb to off |

P10 is the one that watches the machine rather than the answer. Every other
property reads a final count; P10 pins the intermediate state after every
prefix of rounds, so an off-by-one in the round loop is caught at the round
where it happens instead of being absorbed into a total that comes out right
anyway. P11 and P12 are the same idea aimed at the toggle rather than the
count: toggles commute, so order cannot matter, and two full passes must
return every bulb to off.

P6's upper half has to be written carefully, and the reason is Kāra-specific.
`(r + 1) * (r + 1)` overflows i64 when `r` is `floor(sqrt(i64::MAX))`, and Kāra
traps on overflow rather than wrapping — so the unguarded bracket check panics
on `n = 3037000499²`, which is one of the hand-picked big cases. The guard is
sound rather than a dodge: at that `r` the claim `(r+1)² > n` holds for every
representable `n`, so there is nothing left to check.

## Mutation testing

Fifteen content-anchored edits to `differential.kara`, each run through the
full sweep. HANG, PANIC and BUILD-FAIL count as kills alongside
`DIFFERENTIAL FAILED` — M3 is a hang, and a harness that scored only the
property lines would have recorded it as silent.

| # | mutation | predicted | outcome | properties that fired |
|---|---|---|---|---|
| M1 | the isqrt guard weakened from `n < 2` to `n < 1` | kill | *silent* | — |
| M2 | Newton rounds the mean up: `(x + n/x + 1) / 2` | kill | **killed** | P1, P6, P7 |
| M3 | Newton's stop test `>=` weakened to `>` | kill | **killed** | hang |
| M4 | the counting arm tests `k*k <= n` instead of `(k+1)²` | kill | **killed** | P2, P7 |
| M5 | round `i` starts at bulb `2i`, skipping bulb `i` | kill | **killed** | P1, P2, P3, P5, P6, P8, P10 |
| M6 | the round loop runs `b < n`, never toggling the last bulb | kill | **killed** | P1, P2, P3, P5, P6, P8, P10 |
| M7 | the divisor pair at `d*d == b` is counted twice | kill | **killed** | P3, P9 |
| M8 | trial division stops at `d*d < b`, missing `d = sqrt(b)` | kill | **killed** | P3, P9 |
| M9 | `is_square` overshoots and reports false for every `b` | kill | **killed** | P5, P8, P9 |
| M10 | `count_on` starts at slot 0 | *silent* | silent | — |
| M11 | the square root comes back one too low | kill | **killed** | P1, P6, P7 |
| M12 | `divisors_upto` drops its `d <= b` clause | *silent* | silent | — |
| M13 | the reversed round order drops round 1 | kill | **killed** | P11 |
| M14 | Fisher–Yates stops one element early | *silent* | silent | — |
| M15 | rounds SET the bulb instead of toggling it | kill | **killed** | P1, P2, P3, P5, P6, P8, P10, P12 |

**11 killed, 4 silent, 1 prediction wrong — and the wrong one taught me
something about my own code.** I predicted M1 would die: weakening the ★ arm's
`if n < 2 { return n; }` to `if n < 1` looked like it would send `n = 1` into
the loop and `n = 0` into a division by zero. Only the second half of that is
true, and it is the half the weakened guard still catches. `n = 1` needs no
guard at all — the loop computes `y = (1 + 1) / 2 = 1`, fails to decrease, and
returns 1 unaided.

So only the `n == 0` case is load-bearing, and the `< 2` form is one wider
than it strictly has to be. Both arms now say so in a comment. The guard stays
as it is: `n < 2` states "0 and 1 are their own square roots", which is the
property a reader wants to see, and the mutation result is evidence about which
half does the work rather than an argument for trimming it.

The other three silents are genuine equivalents. M10 lets `count_on` include
slot 0, which exists only so that bulb `b` lives at index `b` and which no
round ever touches. M12 drops `d <= b` from `divisors_upto`, and a candidate
larger than `b` never divides `b` for `b >= 1`. M14 truncates the Fisher–Yates
shuffle by one step, which still produces a permutation — and P11 asserts that
order does not matter, not which order was used. M15 is the mutant that shows
P11 alone would not have been enough: setting instead of toggling is *also*
order-independent, so P11 stays green and eight other properties do the work.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` — the full A/B set the repo requires.

The benchmark mirror is verified on JIT, AOT-sequential and AOT-auto-par, and
against all four language twins, but not under `--interp`: it is ten passes of
a six-million-bulb simulation, which the tree-walk backend would take hours to
finish. The kata's semantics are covered by the arms and the differential,
which do run on every backend.

## Benchmarks

`bench/bulb_switcher.kara` and its four mirrors run ten passes, each
simulating **all `n` rounds** over an `n`-bulb byte array for a different `n`,
from 6,000,000 down to 5,189,901. The benchmark deliberately measures the arm
the closed form replaces: `floor(sqrt(n))` is six Newton iterations and not a
workload, while the simulation is a harmonic-sum number of writes — about
`n ln n`, roughly 97 million per pass — laid down at every stride from 1 to
`n`. Round 1 is a linear sweep of six megabytes; round 700,000 touches two
bulbs a megabyte apart. It is a cache-behaviour benchmark, not an arithmetic
one.

The `n` changes each pass so the answer moves (2449 down to 2278) rather than
being one constant, and the fold takes both the count of lit bulbs and the sum
of their indices, so the array has to be materialised and walked. Bulbs are
`u8` in every mirror so that all five measure the same six megabytes of
traffic and not their own choice of bit packing.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container. Python is its own
lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 1409.7 ms ± 22.9 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 1435.2 ms ± 36.7 | 1.02× |
| **kāra `karac build`** | **1437.4 ms ± 44.5** | **1.02×** |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1489.9 ms ± 26.6 | 1.06× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1521.1 ms ± 22.6 | 1.08× |
| rust `-O` | 1544.1 ms ± 43.1 | 1.10× |
| go `go build` | 1619.1 ms ± 28.0 | 1.15× |
| python 3.11 | 93519 ms ± 6943 | 66.3× |

Unlike kata 318 — where six of seven compiled legs finished inside 5% and the
benchmark discriminated nothing — this workload does separate the backends.
Kāra lands 2.0% behind clang and ahead of all three Rust legs.

**The Rust gap was investigated and the obvious explanation ruled out.** The
inner loop indexes a byte slice, so bounds checking is the natural suspect, and
the Rust binary does retain a `panic_bounds_check` path where the C mirror
(a raw pointer) has none. It is not the cause: a `get_unchecked_mut` variant,
timed against the checked one in the same hyperfine run, came out at
1.563 s ± 0.070 against 1.537 s ± 0.042 — no faster, and both still behind
C's 1.463 s in that run. So the 7% is real and its cause is *not* isolated
here; that variant is a scratch diagnostic and is deliberately not in the repo,
because shipping an `unsafe` mirror would break the equal-safety framing the
whole benchmark rests on.

Two comparisons that usually carry weight turn out to be non-events on this
kata, and saying so is more useful than quoting them:

- **Equal-safety is unmeasurable here.** `rustc -O -C overflow-checks=on`
  came in at 1521.1 ms against plain `-O`'s 1544.1 ms — nominally *faster*,
  which is not a real effect but noise (σ ≈ 23 and 43 ms). The inner loop is an
  XOR and a pointer bump; there is essentially no arithmetic to check, so
  Kāra's default-checked overflow costs it nothing measurable either.
- **`-march=x86-64-v3` does nothing.** It made C nominally slower (1435.2 vs
  1409.7 ms, ~1σ). A scattered read-modify-write over a strided array has
  nothing to vectorise.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 95.3 ms ± 1.8 | 15.8 KiB | 7.16 MiB |
| rust | 118.6 ms ± 3.5 | 3862.6 KiB | 7.62 MiB |
| kāra | 337.2 ms ± 6.0 | 337.4 KiB | 8.12 MiB |
| go | — | 2178.2 KiB | 7.64 MiB |
| python | — | — | 13.33 MiB |

`karac build` is 3.5× clang's cold compile and 2.8× rustc's; its binary is 21×
clang's and 11× smaller than rustc's. Every leg's resident set is dominated by
the six-megabyte bulb array, as it should be. Raw numbers in
`bench/results.container-x86.json`; methodology and caveats in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Nothing to file. Across five `.kara` files the only diagnostics were three
`E0218`s in the differential, where `next(seed)` needed the call-site `mut`
marker Kāra requires on a fresh binding; `karac fix` applied all three. No
workarounds, no contorted phrasing, no `KARAC_AUTO_PAR=0`-only pass.
