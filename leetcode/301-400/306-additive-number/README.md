# 306. Additive Number

A string of digits is **additive** if its digits can be cut into a sequence of
at least three numbers where every number after the first two is the sum of the
two before it. No number may carry a leading zero, so `1, 02, 3` is not a valid
cut even though `1 + 2 == 3`.

```
"112358"     ->  true    1, 1, 2, 3, 5, 8
"199100199"  ->  true    1, 99, 100, 199
"1023"       ->  false
```

## Approaches

| file | mechanism | arithmetic |
|---|---|---|
| `additive_number.kara` ★ | search the two prefix lengths, verify in place | digit lists — exact at any length |
| `additive_number_recursive.kara` | same search, verification by recursion | digit lists |
| `additive_number_concat.kara` | same search, generate and compare whole | digit lists |
| `additive_number_i64.kara` | same search over machine integers | i64, **declines past 18 digits** |
| `additive_number_allsplits.kara` | enumerate **every** cut — the definition | digit lists |
| `differential.kara` | 8,896 cases, five arms, seven properties | — |
| `bench/additive.kara` | 220 candidates × 18 digits × 90 passes | — |

## The mechanism: the first two numbers determine everything

The naive reading of the statement is "find a cut of the string into three or
more parts", which is a search over subsets of the 34 possible cut positions —
`2^34`. But the additive rule leaves nothing to choose after the second number:
once `a` and `b` are fixed, the third number **must** be `a + b`, which fixes
its digits, which fixes where it ends, which fixes the fourth, and so on to the
end of the string. The whole sequence is a function of its first two elements.

So the search space is not the cuts, it is the two prefix lengths — `O(n^2)`
pairs, each verified in `O(n)` — and the exponential collapses to `O(n^3)`.
That is the entire algorithmic content of the problem, and
`additive_number_allsplits.kara` enumerates the cuts anyway, which is what makes
the argument a **checked claim** rather than a plausible one.

## Arithmetic is the other half, and it is why this kata is worth writing

The input is up to 35 digits. Split it as evenly as the rule allows and the two
leading numbers run to ~17 digits each, so their sum needs 18 — and the sums
compound from there. `i64` tops out at 19 digits, so a straightforward integer
implementation does not merely lose precision on the extremes, it **overflows on
inputs the problem explicitly admits**. Kāra checks arithmetic by default, so
that overflow is a panic rather than a silently wrong answer.

The star arm therefore never converts a number to an integer: it holds each
number as its decimal **digits** and adds them by hand, which is exact at any
length. This case is in the demo set and it is not decorative —

```
"999999999999999999991100000000000000000000"  ->  true
```

— that is `(10^20 - 1)`, then `1`, then `10^20`. All three numbers exceed `i64`.

`additive_number_i64.kara` is the same search over machine integers, and it is
the answer to the problem's own follow-up question ("how would you handle
overflow for very large input integers?"). It **refuses rather than guesses**:
`is_additive_i64` returns `Option[bool]`, `None` exactly when the input exceeds
18 digits. The bound is what makes the `Some` answers sound, and the argument is
worth stating because it is not obvious:

- With `n <= 18` every span of the input is at most 18 digits, so every number
  **parsed** from it is at most `10^18 - 1`.
- A sum is only ever formed from two numbers already in the sequence, and the
  sequence only advances when the sum **matched** a stretch of the input — which
  bounds it by `10^18 - 1` as well.
- So every value added is at most `10^18 - 1` and every sum at most
  `2 * 10^18 - 2`, comfortably inside `i64`'s `9.22 * 10^18`.

The Fibonacci-style compounding that would break the bound cannot happen,
because a sum that does not match ends the verification before it is ever added
to anything.

## Testing a boolean is the hard part here

Almost every digit string is **not** additive. A case set drawn from random
strings is ~99% false, so an arm that ignored its input and returned `false`
would pass it — and agreement between arms does not help, because five arms that
all return `false` agree. That shapes the whole case space:

| part | what it is | why |
|---|---|---|
| exhaustive | every string of length 3–6 over `{0,1,2,9}` — 5,440 cases | small enough for arm E to reach all of them; the `9` keeps carries in play |
| constructed | sequences built forward from `(a, b)` and concatenated | additive **by construction** — the only guaranteed positives |
| perturbed | a constructed positive with one digit changed | negatives one edit from a positive, where offset slips show up |

```
cases 8896
  of which additive 1820
  arm E (all cuts) run on 8896
  arm D (i64) answered 8896
P1..P7 all 0
DIFFERENTIAL OK
```

**The true-rate is reported on purpose.** A property set for a boolean predicate
is worth nothing if the cases are all one answer, and 1,820 of 8,896 (20.5%) is
the only way to see that this one is not.

| # | property | what it pins down |
|---|---|---|
| P1 | five arms, one answer | the algorithm, from five directions |
| P2 | a constructed positive is accepted | **no arm computes this** — the anti-`false` net |
| P3 | length < 3 ⇒ false | closed form |
| P4 | all zeros, length ≥ 3 ⇒ true | closed form |
| P5 | truncating a positive to ≥3 terms keeps it true | **no arm computes this** |
| P6 | extending a positive by its next term keeps it true | **no arm computes this** |
| P7 | the i64 arm agrees wherever it answers | the follow-up, made testable |

**P2, P5 and P6 run in the opposite direction to every arm.** The arms *search*
for a cut; the harness already *knows* one, and asks the arms about the string.
P2 is the entire defence against an arm biased toward `false` — the failure mode
that agreement is blind to. P5 and P6 are sound rather than heuristic: dropping
the last term of a valid cut leaves the remaining terms still satisfying "each is
the sum of the two before", and appending the next term does too.

P7's count is reported because `None` is not a pass — an arm that declined
everything would look identical to one that agreed, and 8,896 answered is what
distinguishes them.

## Mutation-tested, and two of the mutations were mine

Anchored by content **within a named function body**; the harness asserts each
anchor is unique and refuses to run otherwise.

| # | mutation | caught by |
|---|---|---|
| M1 | first number may carry a leading zero | P1, P7 |
| M2 | second number may carry a leading zero | P1, P7 |
| M3 | a two-number cut counts as a sequence | *survives — see below* |
| M4 | a prefix match is accepted, not just a full one | *survives — see below* |
| M5 | the carry is dropped in `add_digits` | P1, **P2**, P5, P6, P7 |
| M6 | the offset advances one digit, not the sum's width | P1, **P2**, P5, P6, P7 |
| M7 | the window does not slide (`a` never advances) | P1, **P2**, P5, P6, P7 |
| M8 | `matches_at` allows an out-of-range match | *bounds panic* |
| — | **control** — `hi == lo + 1` for `hi - lo == 1` | *(correctly survives)* |
| — | **control** — `steps != 0` for `steps > 0` | *(correctly survives)* |

**M3 and M4 survive because they are equivalent mutations, not because the
properties missed them** — and that is a finding about the star arm, not about
the battery. Both guards are provably dead under the arm's own loop bounds:

- `for len2 in 1..(n - len1)` makes `len1 + len2 <= n - 1`, so the verification
  loop always runs at least once and `steps` is never 0. The `steps > 0` test
  can never be false.
- `matches_at` refuses a match that would run past the end, so `pos <= n` always
  holds; combined with the loop's exit condition, `pos == n` and `pos <= n` are
  the same test.

Proven rather than argued. Widening the `len2` bound by one — so `len1 + len2`
can reach `n` — makes `steps > 0` load-bearing, and **M3 then fires on 13,370
cases**, while the widening alone and M3 alone both survive. M4 stays inert even
widened, because the range check is what pins `pos`.

The guards are kept anyway: they cost nothing, they state the postcondition the
loop bounds happen to imply, and they would become load-bearing again the moment
someone changes a bound. But they are **not** doing work today, and a battery
that reported "8 of 8 caught" would have been claiming otherwise.

P3 and P4 fired on nothing. They are narrow closed forms over a handful of
inputs, and they are recorded here as weak rather than listed as equals.

## Benchmarks

Build 220 candidate strings of 18 digits once as one flat digit array — every
25th a **planted additive positive**, so the verification loop runs to
completion rather than bailing on the first mismatch every time — then punch 90
full `O(n^3)` scans over them, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 370052193`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. The bracketed column is an independent repeat of the whole suite;
every ratio below reproduces within 5%, which is the precision these numbers are
quoted to.

| | mean | repeat | vs kara |
|---|---:|---:|---:|
| c (`-O3`) | 138.9 ms ± 3.3 | 139.8 | 0.47× |
| c (`-O3 -march=x86-64-v3`) | 144.1 ms ± 11.9 | 142.4 | 0.49× |
| **kara** (codegen, seq) | **294.6 ms ± 6.8** | **307.6** | **1.00×** |
| go | 339.9 ms ± 8.5 | 343.6 | 1.15× |
| rust (`-O`) | 413.8 ms ± 8.6 | 417.0 | 1.40× |
| rust (equal safety + matched ISA) | 430.0 ms ± 11.0 | 430.5 | 1.46× |
| rust (`-O -C overflow-checks=on`) | 434.3 ms ± 11.5 | 432.1 | 1.47× |
| python | 3.65 s | — | 12.4× |

**Kāra beats equal-safety Rust by 1.47×, plain `rustc -O` by 1.40× and Go by
1.15×**, and trails `clang -O3` by 2.12×. Against the equal-safety comparator
BENCHMARKS.md treats as the fair one, this is the corpus's widest Kāra win in
the 300s.

### The first version of these mirrors was wrong, in both directions

This table replaces one where C was 71.4 ms and Rust 556.0 ms — C looking 4.1×
faster than kāra and Rust 1.9× slower. Both were artifacts of my own mirrors,
not of the compilers, and they leaned in **opposite** directions, which is why
the shape of the table looked plausible enough to nearly ship:

- **Rust cloned where Kāra moves.** The window advance was
  `a = b.clone(); b = c.clone();`, two heap allocations per verification step
  that have no counterpart in `additive.kara`'s `a = b; b = c;`. Removing them:
  556.0 ms → 413.8 ms, a **1.34×** penalty that was purely mine.
- **C never allocated at all.** `add_digits` wrote into a caller-supplied stack
  buffer and the window advanced by `memcpy`, where the Kāra arm returns a fresh
  `Vec[i64]` per addition. Allocation is part of the algorithm here, not an
  implementation detail to hoist away. Making C allocate and free per addition,
  exactly as the Kāra arm does: 71.4 ms → 138.9 ms, **1.93×**.

The stack-buffer C is still worth knowing as a number rather than hiding: 72.6 ms
against 140.1 ms for the matching version, measured head-to-head. That 1.93× is
the price of this algorithm's allocation strategy in a language with no runtime
at all, which puts kāra's 2.12× gap to matching C in useful perspective — most of
what separates them is *not* allocation, since C pays that too now.

### The ISA column: nothing gains here

| | baseline | matched ISA (v3) | gain |
|---|---:|---:|---:|
| c (unchecked) | 138.9 ms | 144.1 ms | **none** |
| rust (checked) | 434.3 ms | 430.0 ms | **none** (1.01×) |

Both are inside σ, and this is the interesting departure from
[#312](../312-burst-balloons/) and [#313](../313-super-ugly-number/), where
unchecked C gained 1.27× and 1.93× from `-march=x86-64-v3` while checked Rust
gained nothing. Here **neither** gains. The loop is a branchy, allocation-bound
digit walk with data-dependent exits — there is no vector work to find, so the
wider ISA has nothing to do regardless of what the checks allow. That is a
useful control on the earlier two katas' suspect: it shows the "checks block
vectorisation" story only applies where vectorisable work exists.

### Auto-par is a 7× loss here, and that is a filed defect

| | time | system time |
|---|---:|---:|
| `KARAC_AUTO_PAR=0` (sequential) | **0.29 s** | 0.00 s |
| default auto-par | **2.05 s** | 1.42 s |

The published table is the sequential lane. The default build is 7.1× slower —
see [`B-2026-09-03-40`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)
below.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all seven sources,
all byte-identical under `karac run`, `karac build` and the default
auto-parallelising build.

### One defect found: the auto-par cost gate is defeated by an implausible estimate

[kara `B-2026-09-03-40`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)
— filed from this kata. The **default** build fans out a region entered on the
order of a million times:

| workload | sequential | default auto-par | |
|---|---:|---:|---|
| `bench/additive.kara` | 0.29 s | 2.05 s | **7.1×** |
| `differential.kara` | 0.069 s | 27.5 s | **398×** |

`KARAC_COST_DEBUG=1` reports `per_iter_cost=3578073120 floor=64
substantial=true`. That cannot be a per-**iteration** cost: the whole benchmark
executes on the order of 3e8 operations, so one iteration cannot cost 3.6e9
units. Whatever the estimator is measuring, it clears the floor by **eight
orders of magnitude**, so the gate that exists to decline unprofitable fan-outs
cannot fire. The accumulation is `saturating_*` on `u64`, so this is not a
wraparound.

`strace -c` attributes 100% of syscall time to `futex`: **1,843,996** calls at
four workers and **1,963,832** at *one*. The volume is driven by dispatch count,
not by contention between workers — the region is entered about a million times
and each entry pays a pool round trip. Worker count then adds contention on top,
monotonically: 1 → 0.68 s, 2 → 1.69 s, 4 → 1.99 s.

Ruled out by measurement rather than inspection, because this has the same
*look* as [`B-2026-09-03-18`](../313-super-ugly-number/) and is a different
defect: not the per-dispatch environment read (a `getenv` interposer counts five
calls in the whole run), not nested fan-out (`KARAC_PAR_MAX_FORK_DEPTH=0/1`
unchanged), not atomic promotion (`KARAC_PAR_ATOMIC_PROMOTION=0` unchanged), not
worker contention as the root.

The likely missing question is separate from the bad number: every gate asks
*"is this body substantial?"* and none asks *"how often is this region
**entered**?"*. A region entered a million times loses on dispatch cost no matter
how substantial its body, because the amortisation has to happen across entries.

**Correctness is unaffected**, which is why no A/B test in the corpus catches it:
all five arms are byte-identical in every mode, the benchmark prints
`checksum 370052193` everywhere and the differential prints `DIFFERENTIAL OK`
everywhere. The clock is the only detector, for the third time in this class.

### Nothing was phrased around a gap

The i64 arm's `Option[bool]` is not a workaround for a compiler limitation — it
is the honest answer to the problem's follow-up, and the exact arms answer the
same inputs. The one construct this kata needed and did not have on the first
try was the call-site `mut` marker on `explore(bytes, 0, mut nums)`, which
`karac check` diagnosed precisely and `karac fix` applied.
