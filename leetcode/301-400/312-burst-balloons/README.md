# 312. Burst Balloons

`n` balloons in a row, each with a number on it. Burst them all, one at a time.
Bursting balloon `i` pays

```
nums[left] * nums[i] * nums[right]
```

where `left` and `right` are the nearest balloons **still unburst** on either
side; past the ends of the row, treat the missing balloon as a `1`. Maximise the
total.

```
nums = [3, 1, 5, 8]  ->  167

[3,1,5,8]  burst 1  ->  3*1*5  =  15
[3,5,8]    burst 5  ->  3*5*8  = 120
[3,8]      burst 3  ->  1*3*8  =  24
[8]        burst 8  ->  1*8*1  =   8
                                 ---
                                 167
```

## Approaches

| file | mechanism | assumes the reframing |
|---|---|---|
| `burst_balloons.kara` ★ | interval DP, nested table, shortest interval first | ✅ |
| `burst_balloons_flat.kara` | same recurrence, flat table + stride | ✅ |
| `burst_balloons_memo.kara` | same recurrence, top-down, `Option[i64]` memo | ✅ |
| `burst_balloons_generic.kara` | same recurrence, generic bounded `Table[T]` | ✅ |
| `burst_balloons_brute.kara` | exhaustive search over burst orders | — |
| `differential.kara` | 3,024 cases, five arms, seven properties | — |
| `bench/burst.kara` | one 300-balloon row × 88 full solves | — |

## The mechanism: ask which balloon is burst *last*

This is the whole problem, and it is worth being precise about why the obvious
framing fails before showing the one that works.

**The obvious framing is "which balloon do I burst first?"** Pick `i`, collect
`nums[i-1] * nums[i] * nums[i+1]`, recurse on what is left. But what is left is
not two independent rows — removing balloon `i` makes `i-1` and `i+1`
**adjacent**, so a later burst in the left part can be paid a value that lives
in the right part. The two halves talk to each other. There is nothing to
memoise on, because "the left part" is not a subproblem: its answer depends on
what the right part still contains.

**Now ask which balloon is burst last** within the open interval `(i, j)` — that
is, among the balloons strictly between the surviving boundary balloons `i` and
`j`. Say it is `k`. Two things follow, and both are exact:

1. When `k` is finally burst, every other balloon in `(i, j)` is already gone,
   so `k`'s neighbours are precisely `i` and `j`. That burst pays
   `a[i] * a[k] * a[j]` — known outright, with no dependence on order.
2. Every balloon in `(i, k)` is burst while `k` is still standing. So `k` walls
   that group off from everything to its right, exactly as `i` walls it off to
   the left. Its world is bounded by `i` and `k` and nothing else — which is
   the subproblem `(i, k)`, unchanged. Symmetrically for `(k, j)`.

So the halves are independent, and:

```kara
dp[i][j] = max over k in (i, j) of dp[i][k] + dp[k][j] + a[i] * a[k] * a[j]
```

The reframing did not simplify the recurrence — it is the same shape either way.
What it bought is **independence**, which is the thing that makes the recurrence
true at all.

**The padding is not a convenience, it is what lets the boundary be stated in
the same language as the interior.** Prepending and appending a `1` turns "off
the end of the row counts as 1" into an ordinary array read, so `dp[0][n+1]` —
the interval bounded by the two sentinels, i.e. all `n` real balloons — is the
answer with no special case anywhere.

## The loop order is not free to choose

`dp[i][j]` reads `dp[i][k]` and `dp[k][j]`, both **strictly shorter** intervals
(`i < k < j`). So intervals must be filled shortest-first:

```kara
for len in 2..w {                    // len is j - i
    for i in 0..(w - len) {
        let j = i + len;
        let mut best = 0;
        for k in (i + 1)..j {
            let coins = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j];
            if coins > best { best = coins; }
        }
        dp[i][j] = best;
    }
}
```

Iterating `i` and `j` in row-major order instead reads cells that have not been
written yet and silently returns a too-small answer. That is mutation **M6**
below, and it is caught.

The flat arm has to honour the same constraint through arithmetic that hides
which row it is touching: `dp[k * w + j]` sits in a **later** row than the cell
being written, so flattening buys the cheaper indexing and none of the locality
that usually motivates it. The `_generic` arm is the same recurrence again
behind a bounded `Table[T]`, present for **compiler coverage** rather than
algorithmic coverage — it cannot disagree with the flat arm for a reason about
burst balloons, only for a reason about monomorphisation.

## Arm E assumes nothing, and that is why it earns `O(n!)`

Four of the five arms are schedulings of **one** recurrence, and they share its
whole premise. If the last-burst argument above were wrong, all four would be
wrong *together* and agree perfectly. Their individual bugs are scheduling bugs;
none of them is the premise.

So `burst_balloons_brute.kara` implements the statement and nothing more:
maintain the row of surviving balloons, pick one, pay against the balloons
*actually adjacent right now*, remove it, recurse. The neighbour lookup is a
live scan of the surviving row rather than an index computation, so the coupling
that breaks the forward framing happens **by construction** instead of being
reasoned about.

It agrees with all four DP arms on every input up to `n = 7` in the
differential, and on `[9,76,64,21,97,60]` — all 720 burst orders — in the
statement cases. That is what promotes the reframing from a plausible argument
to a checked one.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | five arms, one answer | the algorithm, from five directions |
| P2 | `solve(nums) == solve(reverse(nums))` | **reversal — no arm computes this** |
| P3 | `[x] -> x` | the lone-balloon closed form |
| P4 | `[a,b] -> a*b + max(a,b)` | the two-balloon closed form |
| P5 | raising one value cannot lower the answer | *(a shape check — see below)* |
| P6 | answer ≥ any feasible order's total | **the maximum — no arm computes this** |
| P7 | answer ≤ `M² · sum(nums)` | no balloon is paid twice |

```
cases 3024
P1..P7 all 0
DIFFERENTIAL OK
```

**P2 and P6 are the ones no arm computes.** Each relates *separate invocations*
to one another, so each catches a fault symmetric across every arm — the failure
mode all-arms agreement is blind to. P2 holds because a balloon's pay depends on
its two neighbours and not on which side they are on, and every arm walks the
row in one fixed direction knowing nothing of it. P6 holds because the answer is
a **maximum** over orders, so it is at least the total paid by any particular
one; the harness bursts left-to-right, simulating the statement directly. P6 is
the only property that specifically catches **under**-maximisation, which is
exactly what a too-early table read produces.

### P5 looks like the strongest property here and is very nearly a tautology

Monotonicity — with non-negative values, raising one balloon's number cannot
lower the answer — reads like it should be the best test in the set. It
constrains how the answer must **move** under a perturbation, which no arm
computes even implicitly.

It is also unfalsifiable by any plausible single mutation, for a structural
reason. The computed answer is a maximum over sums of products of non-negative
values, and **any** expression of that shape is monotone in each of its inputs —
the maximum of monotone functions is monotone. So monotonicity follows from the
*shape* of the computation, not from its correctness, and every single-line
mutation preserves the shape: swapping indices, truncating the candidate loop,
reading an unwritten cell, duplicating a boundary factor. All of them stay
monotone while being wrong.

Measured: **P5 fired on none of the six single-line mutations**, including M5,
which was written specifically to be antitone. M5 fails to break it because
`best` starts at `0` and only ever moves up, so negative terms are clamped away
and the answer collapses to `0` — which is monotone. Breaking P5 took **two
simultaneous** mutations, subtracting the boundary product *and* lowering the
initial `best` past `0` so negatives propagate; then it fires on 1751 of 3024
cases.

So P5 is falsifiable in principle and unfalsifiable by any plausible slip. It is
kept because it costs one call and does pin the non-negativity clamp, which is a
real invariant. It is **not** counted as an independent check. Same shape of
finding as [#304](../304-range-sum-query-2d-immutable/)'s unfalsifiable split
additivity, reached from a different direction.

## Mutation-tested, because a differential that cannot fail is decoration

Anchored by content inside `fn coins_a` rather than by line number, so drift
cannot silently point a mutation at the wrong arm.

| # | mutation | caught by |
|---|---|---|
| M1 | right half reads `dp[k+1][j]` (the forward-framing instinct) | P1, P2, P4 |
| M2 | boundary product duplicates `a[k]` | P1, P2, P3, P4 |
| M3 | `k` range includes the boundary balloon | P1, P2, P3, P4, **P7** |
| M4 | candidate loop truncated to one `k` | P1, P2, P4, **P6** |
| M5 | boundary product subtracted | P1, P3, P4, **P6** |
| M6 | shortest-first violated — row-major nest | P1, P2, P4 |
| — | **control** — `>=` instead of `>` for the tie-break | *(correctly survives)* |
| — | **control** — `best` initialised to `-1` | *(correctly survives)* |

Both controls are semantically equivalent to correct code and must **not** fire:
a tie broken the other way still yields the same maximum, and a `-1` seed is
unreachable for non-negative inputs. A battery that flagged either would be
flagging *edits*, not faults.

**M6 is the one worth noting.** Violating shortest-first is not an arithmetic
error — every term is right — it just reads cells before they are written. The
answer that comes out is a plausible, too-small number, and it is caught by
three properties.

## Benchmarks

Build one 300-balloon row and one 302×302 flat table once; then punch 88
complete interval-DP solves, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 289414141`.

**Each pass perturbs one balloon at an index derived from the running
checksum** — the solve is a pure function of its input, so 88 identical solves
of unchanging inputs are exactly what an optimiser may hoist and run once.

**The table needs no re-zeroing between passes**, and that is a property of the
recurrence rather than a shortcut: every cell with `j - i >= 2` is written by
the pass that reads it, and the `j - i < 2` band is the base case that must stay
`0` forever. So a single zeroing at allocation is correct for every pass, in all
five languages, which keeps the measured work in the `O(w³)` inner loop rather
than in allocation.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 271.0 ms ± 6.5 | 0.49× |
| c (`-O3`) | 344.7 ms ± 9.9 | 0.62× |
| rust (`-O`) | 418.8 ms ± 11.3 | 0.76× |
| rust (equal safety + matched ISA) | 551.9 ms ± 16.6 | 1.00× |
| **kara** (codegen, seq) | **553.2 ms ± 13.4** | **1.00×** |
| rust (`-O -C overflow-checks=on`, equal safety) | 554.0 ms ± 17.0 | 1.00× |
| go | 651.9 ms ± 30.5 | 1.18× |
| python | 51.2 s | 92.6× |

Python is a correctness oracle here rather than a timed lane (it is gated behind
`KARA_BENCH_INCLUDE_PY=1` and absent from the JSON); the 51.2 s is one direct
run, not a hyperfine mean.

**Kāra ties equal-safety Rust exactly** — 553.2 ms against 554.0 ms is a 0.1%
difference, and the matched-ISA equal-safety build lands at 551.9 ms. All three
are one number. Kāra beats Go by 1.18× and trails plain `rustc -O` by 1.32×.

That is a weaker showing than [#311](../311-sparse-matrix-multiplication/), where
kāra beat equal-safety Rust by 1.38×, and the reason is visible in the ISA
column.

### The ISA column: unchecked code gains 1.27×, checked code gains nothing

| | baseline | matched ISA (v3) | gain |
|---|---:|---:|---:|
| c (unchecked) | 344.7 ms | 271.0 ms | **1.27×** |
| rust (checked) | 554.0 ms | 551.9 ms | **none** (0.4%, inside σ) |

This is a better-controlled version of the observation
[#311](../311-sparse-matrix-multiplication/) could only record as a suspect.
There, kāra failed to gain from a wider ISA and the bounds checks were the
obvious candidate — but with no checked comparator, nothing separated "cannot
vectorise" from "vectorises but is limited elsewhere."

Here **the same compiler** (rustc/LLVM) is measured both ways on the same loop:
with overflow checks on, `-C target-cpu=x86-64-v3` buys **nothing**; clang with
no checks at all buys **1.27×**. Kāra, which checks by default, sits exactly at
checked-Rust's level.

**It is still a suspect, not a finding**, for two reasons worth stating:

1. The comparison does not isolate *which* check blocks the gain. Checked Rust
   carries overflow checks **and** bounds checks; clang carries neither. Nothing
   here attributes the 1.27× to one or the other, and kāra has no ISA variant of
   its own in this lane.
2. **This loop is not the vectorisable shape #311's was.** #311's inner loop was
   a unit-stride AXPY — the most vectorisable form a loop can have, which is why
   clang got 1.49× there. Here one of the two table reads is `dp[k * w + j]`, a
   **stride-`w` gather**, and the accumulator is a max-reduction. That the
   unchecked gain is smaller (1.27× vs 1.49×) is consistent with the harder
   shape, and it means the ceiling kāra is missing is lower here than #311's
   numbers would suggest.

Recorded as measured, on the same footing as
[#310](../310-minimum-height-trees/)'s unexplained *win* over clang.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all seven sources,
all byte-identical under `karac run`, `karac build` and the default
auto-parallelising build.

### One defect found: a user associated function on a primitive type

[kara `B-2026-09-03-13`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md).
Three lines reproduce it:

```kara
trait Zero { fn zero() -> Self; }
impl Zero for i64 { fn zero() -> i64 { return 0; } }
fn main() { let x: i64 = i64.zero(); println(x.to_string()); }
```

`karac check --output=json` reports **zero diagnostics**. Then every executor
refuses it: the interpreter errors `internal: name 'i64' resolved but has no
binding at run time. This is a compiler bug`, and the JIT and AOT build both
error `codegen: no handler for method 'zero' on variable 'i64'`. Two of the
three messages declare themselves compiler bugs. This is **not** a run/build
divergence — run and build agree, and both disagree with `check`.

**The discriminator is `self`, not primitives.** Scoped three ways:

- An **instance** method via a trait impl on a primitive **works** —
  `impl Dbl for i64 { fn dbl(ref self) -> i64 { self * 2 } }` then `x.dbl()`
  prints 42 on both backends. So `impl <trait> for <primitive>` is supported
  generally; only the no-`self` form is unreachable.
- The same associated function reached through a **generic type parameter
  works** — `fn make[T: Zero]() -> T { return T.zero(); }` prints 0, correctly
  monomorphising to the `i64` impl. So the impl *is* reachable and
  dispatchable; only the syntactic form `i64.zero()` has no resolution.
- It is **not trait-specific** — an inherent `impl i64 { fn two() -> i64 }` with
  `i64.two()` fails identically.

Uniform across `i32`, `i64`, `u8`, `bool` and `f64`. The same form on a user
struct works (`P.zero()` prints 7), and the built-in type-name receiver works
(`i64.MAX` prints `9223372036854775807`) — so a primitive type name *is*
resolvable as a receiver, just not for a user-defined associated function.

It is complementary to the already-fixed `B-2026-07-22-10`, which covered the
**unknown**-name half of this surface (`i64.max_value()`, a Rust-ism) and now
yields a clean `E0236 no associated function 'max_value' on type 'i64'`. That
fix taught the typechecker enough to *reject* unknown associated functions on
primitives; this row is the other half, where the name is legitimately
implemented so there is correctly nothing to diagnose — and yet no backend can
execute it.

**Nothing here is phrased around the gap.** The `_generic` arm seeds its table
with `T.zero()` through the bound, which is the form that works and the form one
would write; its local accumulator uses a literal `0`, likewise. The two
spellings sitting side by side is how the gap was found.

### A second defect: the default auto-par build is 123× slower here

[kara `B-2026-09-03-14`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md).
On this kata's benchmark workload:

| build | time | |
|---|---:|---|
| `KARAC_AUTO_PAR=0 karac build` (sequential) | **0.553 s** | |
| `karac build` (default, auto-par) | **67.8 s** | 123× slower |
| the *same* auto-par binary, `KARAC_PAR_WORKERS=4` | **1.51 s** | 45× faster than default |

The third row is the finding. Setting the worker count to *the value auto-detect
would have chosen anyway* (this container has 4 cores) is 45× faster than
leaving it unset. A worker sweep is flat and fast at every explicit value — 1:
1.55 s, 2: 3.85 s, 3: 1.64 s, 4: 1.50 s, 8: 1.46 s — so the pathology is not a
worker *count*, it is the variable being unset.

**Cause, confirmed by `strace` rather than inferred.** `resolve_pool_workers()`
is called once per parallel dispatch, which its own doc comment justifies as a
"cheap libc getenv". That holds only on the env-*set* path, which early-returns.
Unset — the default — it falls through to `thread::available_parallelism()`,
which on Linux probes the cgroup CPU quota through the **filesystem**. A 2-pass
run makes 90,301 such probes, opening exactly three paths 90,301 times each:

```
/proc/self/cgroup
/sys/fs/cgroup/cpu/cpu.cfs_quota_us
/sys/fs/cgroup/cpu/cpu.cfs_period_us
```

The count pins the granularity exactly: the DP has `sum(1..300) = 45,150`
`(i, j)` cells per pass, and `90,301 = 2 × 45,150 + 1` — **one cgroup probe per
parallel region entry**. Hence 51.8 s of the 67.8 s being *system* time.

Ruled out by measurement, not assumed: atomic promotion
(`KARAC_PAR_ATOMIC_PROMOTION=0` is still 67.6 s), worker contention (the same
binary at `KARAC_PAR_WORKERS=4` has *zero* sys time), and fine-grained regions
as such (a minimal repro with a small distinct-index-write inner loop costs
~50 µs per region, two orders of magnitude below this workload's ~2.5 ms — the
difference being the probe count).

**Correctness is unaffected, which is why nothing in the A/B posture catches
it.** All five arms are byte-identical in every mode and the bench workload
prints `checksum 289414141` everywhere. It is a pure perf cliff, invisible to
every test in this repo — the clock is again the only detector, as it was for
[#311](../311-sparse-matrix-multiplication/)'s zero-skip guard.

The published table above is the **sequential** lane and is unaffected.

### Probed clean

- **Descending interval schedule** (`i` from high to low instead of
  length-ordered) — a valid alternative fill order. Clean, agrees.
- **Tuple return tracking the argmax** — the natural way to also recover *which*
  balloon was burst last. Clean.
- **`Vec[Vec[Option[i64]]]`** as a choice table, assigned through a double index.
  Clean.
- **`Vec[(i64, i64)]` as an explicit work stack** with `let (lo, hi) = top;`
  destructuring — burst-order reconstruction. Clean.
- **Generic bounded `Table[T]`** with an associated constructor — shipped as the
  fifth arm.

## Running it

```bash
karac run burst_balloons.kara            # ★ interval DP, nested table
karac run burst_balloons_flat.kara       # same recurrence, flat table
karac run burst_balloons_memo.kara       # top-down, Option memo
karac run burst_balloons_generic.kara    # generic bounded table
karac run burst_balloons_brute.kara      # exhaustive over burst orders
karac run differential.kara              # 3,024 cases, seven properties

bash bench/bench.sh                      # cross-language lane
```
