# 313. Super Ugly Number

A **super ugly number** is a positive integer all of whose prime factors are
drawn from a given list `primes`. The first one is `1` — it has no prime
factors at all, so the condition holds vacuously. Given `n` and `primes`,
return the `n`th super ugly number.

```
n = 12, primes = [2, 7, 13, 19]  ->  32

1, 2, 4, 7, 8, 13, 14, 16, 19, 26, 28, 32
                                      ^^ the 12th
```

## Approaches

| file | mechanism | how it handles the tie |
|---|---|---|
| `super_ugly.kara` ★ | k-way merge, one pointer per prime | advances **every** stream that matched |
| `super_ugly_canonical.kara` | same merge, canonical factorisation | the tie **cannot arise** |
| `super_ugly_heap.kara` | same merge through a binary heap | discards the duplicate **on the way out** |
| `super_ugly_frontier.kara` | closure of `{1}` under multiplication | the **set** absorbs it |
| `super_ugly_brute.kara` | trial division on every integer | — *(nothing to merge)* |
| `differential.kara` | 2,711 cases, five arms, seven properties | — |
| `bench/ugly.kara` | 100,000 terms × 40 primes × 30 passes | — |

## The mechanism: a k-way merge whose streams are defined over its own output

The super ugly numbers are the closure of `{1}` under multiplication by the
primes. So every super ugly number `x > 1` is `p * u` for some `p` in `primes`
and some **smaller** super ugly `u` — smaller because every prime is at least
2. That single observation says the answer is a merge:

```
stream i  =  primes[i] * u[0],  primes[i] * u[1],  primes[i] * u[2], ...
```

Each stream is sorted, because `u` is sorted and multiplying by a positive
constant preserves order. The union of the `k` streams is exactly the super
ugly numbers greater than 1. Merging `k` sorted streams is routine.

**What is not routine is that the streams are defined over `u`, which is the
output of the merge.** That self-reference is well founded rather than
circular: producing `u[m]` consumes some `u[j]` with `primes[i] * u[j] = u[m]`,
and since `primes[i] >= 2` we have `u[j] < u[m]`, so `j < m`. Every element the
merge reads was already written. The merge feeds on its own prefix and never
needs a value it has not yet produced.

## The tie is the crux, and there are three ways out of it

Two streams can offer the same value: `6` is both `2 * 3` and `3 * 2`, so with
`primes = [2, 3]` both streams offer it at once. Emit it once but advance only
the stream that "won" and the other stream still holds `6`, offers it again
next round, and `6` is emitted twice. Every arm has to answer this, and the
four generating arms answer it four different ways — which is most of what
makes them worth having as separate arms rather than as one.

**★ advance every matching pointer.** Two passes: one to find the minimum, one
to advance every stream that offered it. Collapsing them into a single pass —
advancing as you scan — is subtly wrong, because a pointer advanced early
changes the candidate a later comparison sees.

**`_canonical` makes the tie impossible.** Every super ugly number has a unique
multiset of prime factors; order those factors by their **index in `primes`**
and single out the lowest-indexed one. Peeling one copy of it off leaves a
smaller super ugly number, so each `x > 1` has exactly one parent and exactly
one stream that may produce it:

```kara
x = ugly[j] * primes[i]   is emitted by stream i   only if   i <= spf[j]
```

where `spf[j]` is the index of the lowest-indexed prime factor of `ugly[j]`,
and `spf[0] = k` for the number 1. For `6` with `primes = [2, 3]`: stream 0 may
form it from `3` (`spf = 1 >= 0`), stream 1 may not form it from `2`
(`spf = 0 < 1`). One producer, no tie, no tie-handling code.

Note what the ordering is for: `spf` is the lowest **index**, not the smallest
**value**. Nothing in the argument needs `primes` sorted — any fixed total
order canonicalises a factorisation just as well, because all it has to do is
name one prime. That is a claim, so the differential checks it (P6).

**`_heap` discards on the way out.** A heap's `k` entries are not addressable,
so it can do neither of the above — there is no way to reach in and advance
"every stream that matched". It lets duplicates enter and drops a popped value
equal to the last emitted, **while still advancing that stream**. Dropping it
without advancing re-offers the same value forever and hangs.

**`_frontier` lets the container absorb it.** An ordered set does not hold the
same value twice, so no arm-level dedup code exists at all. This is why it is
the arm that proves the least about the other three, and it is here for
mechanism diversity rather than to double-check pointer arithmetic.

## Arm E assumes nothing, and that is why it earns its cost

The four generating arms rest on **one** premise — that every super ugly number
is `p * u` for a smaller super ugly `u`, so the sequence can be generated from
its own prefix. If that premise were wrong all four would be wrong together and
would agree with each other perfectly. Their individual bugs are tie-handling
and pointer bugs; none of them is the premise.

So `super_ugly_brute.kara` never generates anything. It **tests membership**
one integer at a time, by the literal reading of the statement: divide out
every listed prime as often as it goes, and see whether what is left is 1.
Unique factorisation makes that decisive — a prime factor not in the list
survives every division, so the residue exceeds 1. And `1` needs no special
case: the residue starts at 1 and no division changes it.

Its cost is roughly `O(answer * k)` against the star arm's `O(n * k)`, and
`answer` grows far faster than `n`. That is the point, and it is also the
constraint the property set exists to work around.

## Properties, and being honest about what they are for

```
cases 2711
tier2 beyond-oracle cases 575
P1..P7 all 0
DIFFERENTIAL OK
```

| # | property | what it pins down |
|---|---|---|
| P1 | five arms, one answer | the algorithm, from five directions |
| P2 | strictly increasing, first term 1 | the dedup — the failure mode this problem is about |
| P3 | the answer is super ugly, by factoring it | **no arm computes this** *(see below)* |
| P4 | nothing valid skipped between consecutive answers | **no arm computes this** |
| P5 | one prime ⇒ the nth term is `p^(n-1)` | **no arm computes this** |
| P6 | permuting `primes` cannot change the answer | **no arm computes this** |
| P7 | adding a prime cannot raise the answer | **no arm computes this** |

**Why have any properties at all, when arm E is a complete and independent
oracle?** This decides how much the set is actually worth, so it is worth
stating plainly rather than listing seven properties as if each were a
detector.

Wherever E runs, it settles the case outright. Any property that is a function
of **the answer alone** is then implied by P1: if arm A returned exactly what E
returned, and E is right, then A's answer is super ugly, is larger than the
previous one, and matches every closed form — necessarily, with nothing left to
catch. **Inside E's range the properties are localisers, not detectors.** They
say how an arm is wrong, not that it is.

E's range is the whole constraint. It is bounded by the **answer's magnitude**
while the other four are bounded by `n`, and the two diverge fast: with
`primes = [13]` the 12th super ugly number is `13^11`, which E needs ~1.8e12
iterations to reach and the star arm produces in eleven steps. So the case
space is built deliberately to run past E:

- **Tier 1** — answer ≤ 3000. All five arms; E is complete; P2–P7 localise.
- **Tier 2** — beyond that, up to 1e15. Four arms and the properties, which are
  now the only thing between a wrong merge and a green run. **575 of 2,711
  cases.**

That number is reported by the differential itself, because a property set
whose entire coverage sits inside an oracle's range has not been tested for the
job it is actually there to do.

**The properties test arm A** (P6 also tests arm B). Arms C and D are covered
by P1 alone. That is a real limitation of the set and not a claim about their
quality — it is why M8 and M10 below are caught by exactly one property.

## Mutation-tested, because a differential that cannot fail is decoration

Anchored by content **within a named function body**, so drift cannot silently
point a mutation at the wrong arm; the harness asserts each anchor is unique
and refuses to run otherwise.

The first battery produced a result about the *language* rather than about the
property set:

| # | mutation | caught by |
|---|---|---|
| M1 | A: tie advances only the winning stream — **the duplicate bug** | P1, P2, P6 |
| M2 | A: advanced pointer skips a term (+2) | *bounds panic* |
| M3 | A: merge takes the max of the heads, not the min | *overflow panic* |
| M4 | A: every stream multiplies stream 0's position | *overflow panic* |
| M5 | A: sequence seeded with 2 instead of 1 | P1, P2, P3, P4, P5, P6 |
| M6 | A: the min scan skips stream 1 | *overflow panic* |
| M7 | B: canonical guard off by one, squares vanish | *bounds panic* |
| M8 | C: heap admits the duplicate it should discard | P1 |
| M9 | B: 1's canonical sentinel is 0 | *bounds panic* |
| M10 | D: closure expands by every prime but the last | *overflow panic* |
| — | **control** — min scan `<=` instead of `<` | *(correctly survives)* |
| — | **control** — tie test `<=` instead of `==` | *(correctly survives)* |
| — | **control** — reordered declarations in B's scan | *(correctly survives)* |

**Seven of ten died on a runtime check before the differential could report.**
That is Kāra's default-checked arithmetic and bounds checking doing the
detecting, not the properties. It is a real property of this problem: the
answer is exponential in `n`, so any mutation that lets the merge run ahead of
itself blows past `i64` inside the 45 terms the case space asks for.

It also means the first battery says almost nothing about the property set, so
the same mutations were re-run with the case space capped (`NMAX` 45 → 11,
`CEIL` 1e15 → 1e5) so that no answer can overflow:

| # | caught by, capped case space |
|---|---|
| M1 | P1, P2, P6 |
| M2 | *still a bounds panic* |
| M3 | P1, P4, P6, **P7** |
| M4 | P1, P4, P6 |
| M5 | P1, P2, P3, P4, P5, P6 |
| M6 | P1, P4, P6 |
| M7 | *still a bounds panic* |
| M8 | P1 |
| M9 | *still a bounds panic* |
| M10 | P1 |

Seven of ten now fall to the properties. The three that remain are all
pointer-runs-off-the-array, which capping `n` cannot prevent.

**P6 is the strongest property here**, firing on five of the seven, and there
is a reason rather than an accident: nearly every way to break a k-way merge is
**position-dependent** — which stream is scanned first, which is skipped, which
advances — and permuting `primes` is precisely the transformation that varies
position while leaving the answer fixed. P4 is next at four.

### P3 looks like the strongest property here and is structurally near-inert

Membership — the returned value is super ugly, established by **factoring** it,
which no generating arm does — reads like it should be the best test in the
set. It fired on **one** of the seven.

The reason is structural, and it is the same shape of finding as
[#312](../312-burst-balloons/)'s unfalsifiable monotonicity reached from a
different direction. Every value the merge emits is `primes[i] * ugly[j]` for
some already-emitted `ugly[j]`; by induction from `ugly[0] = 1`, **everything
it emits is a product of listed primes, hence super ugly — whether or not the
merge is correct.** Membership follows from the algebraic *shape* of the
computation, not from its correctness, and every mutation confined to the merge
preserves that shape. Only M5, which changes the **seed**, escapes it — and
only for prime sets not containing 2.

Measured rather than argued, with two mutations written to separate the two
explanations:

| probe | emits | P3 |
|---|---|---|
| X1 | `best + 1` — *outside* the shape | **fires** (444 cases) |
| X2b | `best * primes[0]` — wrong, but *inside* the shape | **silent** (P1, P4, P5, P6 all fire) |

X2b is the decisive one: a plainly wrong answer that stays inside the merge's
algebra is caught by four other properties and **not** by P3. So P3 is
falsifiable in principle and inert against the entire class of faults it was
added to catch. It is kept because it costs one factorisation and does pin the
seed, but it is **not** counted as an independent check.

P7 is the other weak one — one of seven. It relates two runs of the *same*
mutated arm over different prime sets, so a fault symmetric in the prime set
moves both answers together and survives it.

## Benchmarks

Allocate the 100,000-term sequence array and the 40 stream pointers **once**,
then punch 30 complete merge generations through them, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 24228156`.

**Each pass swaps one prime**, at an index and to a value both derived from the
running checksum — the generation is a pure function of `(n, primes)`, so 30
identical generations are exactly what an optimiser may hoist and run once. The
swap is drawn from a pool of primes, so every pass runs on a legitimate prime
list rather than on an arbitrary integer list that happens to type-check.

**No re-zeroing is needed between passes**, and that is a property of the
algorithm rather than a shortcut: every one of the 100,000 slots is written by
the pass that reads it before any read of it can occur, and the pointers are
reset explicitly. So a single allocation is correct for every pass in all five
languages, which keeps the measured work in the `O(n * k)` merge rather than in
the allocator.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 183.5 ms ± 15.3 | 0.39× |
| c (`-O3`) | 322.8 ms ± 12.1 | 0.69× |
| go | 345.0 ms ± 11.4 | 0.74× |
| rust (`-O`) | 368.1 ms ± 21.7 | 0.79× |
| rust (`-O -C overflow-checks=on`, equal safety) | 410.9 ms ± 7.4 | 0.88× |
| rust (equal safety + matched ISA) | 418.3 ms ± 13.4 | 0.90× |
| **kara** (codegen, seq) | **464.7 ms ± 23.8** | **1.00×** |
| python | 15.5 s | 33.4× |

Python is a correctness oracle here rather than a timed lane (it is gated behind
`KARA_BENCH_INCLUDE_PY=1` and absent from the JSON); the 15.5 s is one direct
run, not a hyperfine mean.

**Kāra is last among the compiled lanes**, trailing equal-safety Rust by 1.13×
and plain `rustc -O` by 1.26×. That is a weaker result than
[#312](../312-burst-balloons/), where kāra tied equal-safety Rust exactly
(553.2 ms against 554.0 ms), and it is worth recording as a gap rather than
rounding to a tie: 464.7 against 410.9 is well outside the two σ.

### The ISA column, for the second kata running

| | baseline | matched ISA (v3) | gain |
|---|---:|---:|---:|
| c (unchecked) | 322.8 ms | 183.5 ms | **1.76×** |
| rust (checked) | 410.9 ms | 418.3 ms | **none** (−1.8%, inside σ) |

This reproduces [#312](../312-burst-balloons/)'s controlled comparison with a
larger effect on the unchecked side: the same compiler (rustc/LLVM) on the same
loop gains **nothing** from `-C target-cpu=x86-64-v3` with overflow checks on,
while clang with no checks at all gains **1.76×** (against 1.27× on #312's
loop). Kāra, which checks by default, again sits in the checked group.

**It stays a suspect, not a finding**, for the reason #312 already gave: the
comparison does not isolate *which* check blocks the gain — checked Rust carries
overflow **and** bounds checks, clang carries neither — and kāra has no ISA
variant of its own in this lane. What this kata adds is that the pattern is not
specific to an interval DP: a k-way merge with a stride-1 scan and a
data-dependent gather (`ugly[idx[i]]`) shows it too, and more strongly.

### Auto-par is a 2.2× loss on this workload

Not a lane in the table (this is a seq-only kata) but measured, because #312
found a defect exactly here:

| | time |
|---|---:|
| `KARAC_AUTO_PAR=0` (sequential) | 0.44 s |
| default auto-par | 0.95 s |

The [`B-2026-09-03-18`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)
cliff is gone — system time is 0.00 s where it used to be 51.8 s. What is left
is 0.29 s of per-dispatch environment lookups, which is a second defect filed
below, plus ordinary task-framework overhead for regions this fine. The merge's
inner scan is 40 elements; there is not enough work in one to pay for a
dispatch, and no amount of worker tuning changes that — the sweep is flat at
0.73–0.80 s for every explicit worker count from 1 to 16.


## Compiler findings

The arms are clean — zero `karac check` diagnostics across all seven sources,
all byte-identical under `karac run`, `karac build` and the default
auto-parallelising build.

### One defect found: the use-after-move hint denies a `.clone()` that exists

[kara `B-2026-09-03-26`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)
— filed from this kata. The `_frontier` arm needs `SortedSet` for its minimum,
and probing that surface for the methods it required turned up a diagnostic
that gives confidently wrong advice:

```
warning E0500  value 'q' moved here, used again here
  HINT: declare the callee parameter `ref` if it only reads, or restructure to
        avoid reuse ('q' has no `.clone()` — that exists only on `String`, the
        built-in heap collections and RC types)
```

`SortedSet` **is** a built-in heap collection, and `q.clone()` compiles with
zero diagnostics, runs identically on all three backends, and is a genuine deep
copy. The hint names the one fix that works and says it does not exist — and
because the same predicate gates the machine-applicable edit, `karac fix`
reports *"no fixable diagnostics"* where the `Set` spelling of the same program
is repaired automatically.

Five categories are affected, all of which have a working `.clone()`:
`Option[T]`, `Result[T, E]`, `SortedSet[T]`, `SortedMap[K, V]`, and **any user
type carrying `#[derive(Clone)]`** — where the diagnostic contradicts the user's
own annotation. `Vec`, `Map`, `Set`, `VecDeque` and `String` get the correct
hint; `PriorityQueue`, which genuinely has no `clone`, is correctly told so.

The root cause is a third copy of a predicate that was already reconciled twice.
`moved_type_supports_clone` (`src/ownership.rs`) keeps its own list —
`["Vec", "Map", "Set", "VecDeque"]` — while the typechecker's authoritative
`type_supports_clone` (`src/typechecker/derives.rs`) lists `Option`, `Result`,
`SortedMap` and `SortedSet` too and consults `#[derive(Clone)]`. The ownership
copy's doc comment states, as fact, that `Option`/`Result` have no callable
clone, and cites `B-2026-07-29-31` — the row whose *fix* gave `Option` one
(`Result` followed in `B-2026-07-30-10`). It is a fossil of the world before the
rows it cites.

**To be exact about provenance:** the shipped `_frontier` arm does not itself
move a `SortedSet`, so it does not trigger this. The diagnostic surfaced while
probing the collection's API — set algebra returns a new set and takes its
argument by value, so `p.union(q)` followed by `p.difference(q)` moves `q`
twice, which is the ordinary shape that draws E0500.

### A second defect: an environment lookup per parallel dispatch

[kara `B-2026-09-03-27`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)
— the follow-on to `B-2026-09-03-18`, filed from #312. That fix cached the
expensive *auto-detect* tier of `resolve_pool_workers()` and deliberately left
the `std::env::var("KARAC_PAR_WORKERS")` in front of it per-call, on the
reasoning that it is "cheap libc getenv" at 111 ns against the probe's 15.2 µs.

The per-call figure is right. The aggregate is not, because the same doc comment
establishes that the function runs **once per parallel-region entry**, so the
cost scales with the workload rather than with the program. Counted with an
`LD_PRELOAD` interposer on this benchmark:

```
[getenv] total=2999972 KARAC_PAR_WORKERS=2999970
```

**2,999,970** — exactly 30 passes × 99,999 merge steps, one lookup per step.
The sequential build of the same program makes **one** getenv call in total.

Two corrections to the reasoning that left it in place:

1. **It is not a constant-cost getenv.** `std::env::var` scans the environment
   block, so the cost is linear in how many variables the process was started
   with. Measured on the same binary: **0.66 s** under `env -i`, **0.95 s** with
   a normal environment, **1.53 s** with 300 extra variables — 98 ns and 292 ns
   per call respectively. The program's runtime is a function of its environment
   size.

2. **The documented escape hatch no longer escapes.** Under `B-2026-09-03-18`,
   setting `KARAC_PAR_WORKERS` explicitly was a 45× speedup because it returned
   before the cgroup probe. Now that the probe is cached, both paths pay the
   lookup — `KARAC_PAR_WORKERS=4` makes the same 2,999,970 calls and is not
   faster (1.60 s vs 1.53 s under a padded environment).

0.29 s of the 0.95 s auto-par run is environment scanning — **66% of the entire
0.44 s sequential runtime**, spent re-asking a question whose answer cannot
change. Correctness is unaffected: every arm is byte-identical in all three
modes and the benchmark prints `checksum 24228156` everywhere. As with its
predecessor, the clock is the only detector.

