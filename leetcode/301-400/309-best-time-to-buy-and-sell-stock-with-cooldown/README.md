# 309. Best Time to Buy and Sell Stock with Cooldown

Unlimited transactions over a price series, with one rule added to
[#122](../../101-200/122-best-time-to-buy-and-sell-stock-ii/): **the day after
a sale you may not buy.**

```
prices = [1, 2, 3, 0, 2]

buy 1 → sell 2 → cooldown → buy 0 → sell 2   ->  3
```

That single constraint is what turns a greedy problem into a state machine.
#122's answer is "pocket every positive one-day gain"; here that is merely an
**upper bound**, because the cooldown can force you to skip a rise you would
otherwise have taken. After six range-query katas, this is the first in the run
whose difficulty is in the *shape of the state*, not the shape of the index.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `best_time_cooldown.kara` ★ | three-state rolling DP — `hold` / `sold` / `rest` | O(n) | O(1) |
| `best_time_cooldown_twostate.kara` | two states, cooldown as a `sell[i-2]` lookback | O(n) | O(n) |
| `best_time_cooldown_tabulated.kara` | arm ★'s recurrence, fully materialised | O(n) | O(n) |
| `best_time_cooldown_recursive.kara` | memoised recursion over (day, state), backward | O(n) | O(n) |
| `differential.kara` | 3,800 series, 2,000 against an exhaustive oracle, seven properties | — | — |
| `bench/cooldown.kara` | 200,000-day series × 1,900 passes (380M day-steps) | — | — |

## The mechanism

```
hold[i] = max(hold[i-1], rest[i-1] - price[i])   buy only from `rest`
sold[i] =     hold[i-1] + price[i]               selling is forced-from-hold
rest[i] = max(rest[i-1], sold[i-1])              yesterday's sale frees today
```

The cooldown lives **entirely** in `rest[i] = … sold[i-1]`: a sale on day `i-1`
reaches `rest` only on day `i`, so a buy cannot see it until day `i+1`. There is
no cooldown counter anywhere — the delay is a consequence of the state graph's
shape. The answer is `max(sold, rest)` and never `hold`: ending the series
holding stock means the last purchase was never realised.

### The update-order bug is not on the line you would guess

All three lines read yesterday's values, so the obvious hazard is forgetting to
snapshot before overwriting. Do it on the **`sold`** line — let it read today's
`hold` — and **nothing breaks**. Today's hold is `max(prev_hold, prev_rest −
price)`, so the slip computes `max(true_sold, prev_rest)`; since `rest` is
already at least `prev_rest`, both the rest-chain and the final `max(sold,
rest)` absorb it. Checked over **32,000 random series against the correct form:
zero disagreements.**

The line the snapshot actually protects is **`rest`**. If it reads *today's*
`sold`, the cooldown vanishes outright — a sale reaches `rest` the same day, so
the next day's purchase can see it. That fires four properties.

This kata's first draft asserted the opposite in its own source comment. The
mutation battery is what corrected it, which is the entire reason the battery
carries mutations that must *not* fire.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | four arms, one answer | the algorithm, from four directions |
| P2 | profit is never negative | doing nothing is always allowed |
| P3 | adding a constant to every price changes nothing | **no arm computes this** |
| P4 | scaling every price by `c > 0` scales the answer by `c` | linearity |
| P5 | at most [#122](../../101-200/122-best-time-to-buy-and-sell-stock-ii/)'s no-cooldown answer | the cooldown can only cost |
| P6 | at least [#121](../../101-200/121-best-time-to-buy-and-sell-stock/)'s best single transaction | one trade is always schedulable |
| P7 | equals an **exhaustive enumeration of transaction pairs** | ground truth |

```
series 3800
oracle-checked 2000
P1..P7 all 0
DIFFERENTIAL OK
```

**P7 is the one that audits what every arm assumes.** All four arms take it for
granted that the optimum at a day depends only on a bounded summary of the days
before it. That is true — but it is exactly the assumption four-way agreement
cannot check, because if the state set were insufficient all four would be wrong
together. The oracle enumerates transaction *pairs* directly, with no state
machine anywhere:

```
brute(start) = max over b in [start, n), s in (b, n) of
               price[s] − price[b] + brute(s + 2)
```

The `s + 2` is the cooldown stated as arithmetic on days rather than as a
transition. Exponential, so it runs for `n ≤ 9` — 2,000 of the 3,800 series.

**P3 is the property no arm computes.** Profit is a sum of differences, so a
constant shift cancels in every one. No arm has any notion of that invariance,
which is what makes it able to catch a whole-series fault symmetric across all
four.

**P5 and P6 bracket the answer using other katas' problems** — both already in
the corpus, neither computed by any arm here.

## Mutation-tested, because a differential that cannot fail is decoration

| # | mutation | caught by |
|---|---|---|
| M2 | buying allowed from `sold`, ignoring the cooldown | P1 · · P6 P7 |
| M3 | two-state arm's lookback shortened to `sell[i-1]` | P1 |
| M5 | recursive arm may end while still **holding** | P1 |
| M7 | `rest` reads **today's** `sold` — the cooldown deleted | P1 P2 · P6 P7 |
| M8 | tabulated arm: `rest[i]` reads `sold[i]`, not `sold[i-1]` | P1 |
| M1 | **control** — `sold` reads today's `hold` | *(correctly survives — measurably equivalent)* |
| M4 | **control** — same slip in the tabulated arm | *(correctly survives)* |
| M6 | **control** — redundant `+ 0` on a snapshot read | *(correctly survives)* |

Three of the eight are controls. M1 and M4 are the two that matter: they are the
mutation this kata's source originally *called* the characteristic bug, and they
are semantically equivalent to the correct code — proven by the 32,000-series
check above, not merely unobserved by the differential.

## Benchmarks

Generate a 200,000-day price series once; then punch 1,900 three-state DP
passes — 380M day-steps, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 293297968`.

**Each pass perturbs one price from the running checksum**, and that is
load-bearing rather than decorative. The DP is a pure function of the price
array, so 1,900 identical calls over an unchanging input are exactly the shape
an optimiser is entitled to hoist and run once. Making pass *p*'s input depend
on pass *p−1*'s output creates a serial dependency, so every pass must actually
run — and it is the realistic shape anyway.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3`) | 324.8 ms | 0.54× |
| rust (`-O`) | 339.3 ms | 0.56× |
| c (`-O3 -march=x86-64-v3`, matched ISA) | 345.3 ms | 0.57× |
| rust (`-O -C overflow-checks=on`, equal safety) | 437.8 ms | 0.72× |
| **kara** (codegen, seq) | **606.4 ms** | **1.00×** |
| rust (equal safety + matched ISA) | 612.3 ms | 1.01× |
| go | 1.477 s | 2.44× |
| python | 43.208 s | 71.3× |

Two results here are worth stating plainly rather than glossing.

**This is the first kata in this run where kāra loses to equal-safety Rust** —
1.39× behind `rustc -O -C overflow-checks=on`, where #303 through #308 all had
it ahead or level. The loop is unusually scalar-dense: six live values, three
of them snapshot copies, with checked arithmetic on every add and subtract and
one bounds-checked load per day. That is a plausible account and it is **not a
measurement** — separating the bounds-check cost from the checked-arithmetic
cost would need a build with one of them disabled, which this lane cannot do.
Recorded as an open question rather than an explanation, on the same principle
as [#304](../304-range-sum-query-2d-immutable/)'s refuted stride-multiply
hypothesis.

**Go is the slowest compiled language here by a wide margin**, 2.44× behind
kāra and 4.5× behind C — its first such showing in this range, having been
level with kāra on #305 and #307. Verified in a separate back-to-back hyperfine
run (1.471 s ± 0.015), so it is not a scheduling artefact. A tight scalar loop
with a single indexed load is precisely where Go's weaker bounds-check
elimination and absence of LLVM-grade loop optimisation show up.

Note also that `rust_v3` (612.3 ms) is *slower* than plain `rust_ovf`
(437.8 ms): on this loop the matched-ISA build is a pessimisation. Reported as
measured.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all five sources, all
byte-identical under `karac run`, `karac build` and the default
auto-parallelising build, matching the Python oracle.

**No compiler defect surfaced.** Probed before shipping, not after being asked:

- **An `enum` state machine with an exhaustive `match`** — the idiom this kata
  most obviously avoided, since it writes its three states as bare `i64` (they
  double as memo-table indices, `i * 3 + state`, which is the reason). Clean:
  `enum State { Free, Holding, Cooling }` with `match` over all three variants
  compiles, runs, and returns correctly.
- **A non-exhaustive `match`** is correctly rejected —
  `error[E0205]: non-exhaustive match: missing variants: Cooling`, naming the
  variant.
- **Tuple-returning step function** `-> (i64, i64, i64)` for the three rolling
  scalars — clean.
- **Recursion through `mut ref self`** with memo mutation (arm D) — clean on all
  three backends.
- **`Option[i64]` in a memo table** with `match` on `Some`/`None` — clean, and
  used in arm D in preference to an integer sentinel.

**One gotcha worth recording, which is correct behaviour and not a bug.** A
**field-less** enum is *not* `Copy` unless it says so: passing
`State.Free` to two functions warns `value 's' moved here, used again here`
(E0500) until the type carries `#[derive(Copy)]`, after which it is clean. This
is the documented rule — design.md makes every derivable trait opt-in, "cannot
be inferred from how the type is used elsewhere" — and it matches Rust. It is
worth flagging only because a state machine is exactly where one reaches for a
field-less enum and then threads it through a loop, which is the shape that
trips it.

## Running it

```bash
karac run best_time_cooldown.kara            # ★ three-state rolling DP
karac run best_time_cooldown_twostate.kara   # two states, i-2 lookback
karac run best_time_cooldown_tabulated.kara  # materialised arrays
karac run best_time_cooldown_recursive.kara  # memoised recursion, backward
karac run differential.kara                  # 3,800 series, 2,000 vs the oracle

bash bench/bench.sh                          # cross-language lane
```
