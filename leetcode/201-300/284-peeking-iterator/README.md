# 284. Peeking Iterator

You're given an iterator supporting `has_next()` and `next()`. Wrap it so it also
supports `peek()` — return the next element **without advancing**.

## Approaches

| file | mechanism | pulls at construction | `peek` takes |
|---|---|---:|---|
| `peeking_iterator.kara` ★ | one-slot buffer, filled eagerly | 1 | `ref` |
| `peeking_iterator_lazy.kara` | same slot, filled on demand | 0 | **`mut ref`** |
| `peeking_iterator_materialized.kara` | drain into a `Vec`, index it | n | `ref` |
| `differential.kara` | 840 random operation sequences | — | — |
| `bench/peekiter.kara` | 320 rounds, two peeks per next | — | — |

## You cannot see inside, so you must have already asked

The underlying iterator offers exactly two operations, and `next()` is
destructive — once called the element is gone and there's no way to put it back.
So `peek()` can't be implemented by asking. It can only be implemented by having
**already asked** and kept the answer.

```
peek()      -> slot
next()      -> slot, then refill
has_next()  -> the SLOT is full   (not: the underlying has more)
```

**That last line is where it goes wrong.** After the final element has been
pulled into the slot, the underlying iterator reports empty while the wrapper
still has one element to hand out. A `has_next` that forwards to the underlying
iterator drops the last element — right for the first n−1, wrong for the nth,
which is the easiest possible bug to miss on a short example. It's 3123
disagreements in the table below.

## The lazy variant pays for its thrift in the signature

Filling only on demand means construction costs **zero** pulls, and a caller that
only ever calls `next()` never looks ahead at all — which matters when the
underlying iterator is expensive or effectful.

But `peek()` may now have to pull, so it *mutates*: `peek(p: mut ref Peeking)`
against the eager version's `peek(p: ref Peeking)`. **A caller holding a shared
reference can peek an eagerly-filled iterator and cannot peek a lazy one.** That's
the real trade, and it's invisible in a language that doesn't declare parameter
modes — there, the two differ only in when a side effect happens.

`has_next` gets harder too: it must consider both the slot and the underlying
iterator, where the eager version only asks about the slot. Two states instead of
one is exactly where bugs go — 5870 disagreements when it consults only the slot.

## The object is stateful, so the harness drives it

Every other kata in this stretch maps one input to one output. That shape can't
test this problem: the bugs live in the **transitions** — a slot left full after
the last element, a `has_next` consulting the wrong state, a `peek` that quietly
advances. None is visible from a single drain.

So the harness generates random interleavings of `peek` / `next` / `has_next`,
replays each against all three implementations, and compares **every response at
every step**.

```
sequences 840, operations executed 4253
underlying pulls: eager 2105, lazy 1919, materialized 2520
digest 651902548
has_next disagreements 0
peek disagreements 0
next disagreements 0
peek that advanced 0
```

**Three implementations agreeing on all 4253 responses while consuming
measurably differently** — that's the second property this kata measures, the way
[#277](../277-find-the-celebrity/) counted API calls and
[#283](../283-move-zeroes/) counted writes.

The sequence lengths **vary**, and short ones are the point: all three pull
exactly n times if you drain them, so a drain-only generator reports identical
counts and hides the difference entirely. My first version did exactly that —
2520 pulls across the board.

## What the injected bugs did

| injection | has_next | peek | next | peek advanced |
|---|---:|---:|---:|---:|
| eager: `has_next` forwards to the underlying | **3123** | 0 | 0 | 0 |
| eager: `next()` forgets to refill the slot | 1922 | 601 | 1225 | 0 |
| lazy: `has_next` only checks the slot | **5870** | 0 | 0 | 0 |
| **lazy: `peek` advances on a repeat peek** | 2535 | 298 | 801 | **880** |
| materialized: cursor off by one | 3232 | 271 | 557 | 0 |

Row four is why peek-idempotence is checked directly rather than inferred: a
wrapper that advances on peek still produces a plausible sequence when peeks and
nexts alternate one-for-one, which is how a hand-written test usually calls it.

## A harness bug this table found

The first version gated every operation on **eager's** `has_next` — the exact
thing the harness's own comment warns against. An injected implementation then
got driven past its end and **trapped** instead of being reported: three of the
five rows above crashed and produced no counts at all.

Requiring all three to agree before performing an operation turned every one of
them into a number. A harness that converts a reportable disagreement into a
crash has thrown away the information it exists to collect.

## Three keywords this kata walked into

`writes` (an effect verb), `stable` (the effect-group stability modifier) and
`own` (the closure capture-by-value mode, where Rust says `move`) are all
load-bearing keywords and cannot be identifiers. All three are ordinary English
words that a natural variable name reaches for — the counter here is `stores`,
the definitional solver is `by_definition`, and the copy buffer is `buf`. Each
gave a clear diagnostic naming the collision.

## Kāra features exercised

- **A struct holding another struct by value** (`Peeking` owns its `Source`),
  mutated through nested field paths — `src_next(p.src)` where `p` is `mut ref`.
- **Declared parameter modes making an API difference visible**: the same
  operation is `ref` in one implementation and `mut ref` in the other.
- **`karac fix` applying both marker directions in one pass** — 6 fixes covering
  E0218 insertions and E0219 deletions together.

## Benchmarks

> **Hosts.** The canonical numbers are Apple M5 Pro, in
> [`bench/results.json`](bench/results.json) (first table below) — the file
> `scripts/consolidate-bench.sh` feeds into the top-level chart. The analysis
> after it was done on a shared **x86-64 Linux cloud container**, kept as
> [`bench/results.container-x86.json`](bench/results.container-x86.json); those
> figures are history, and only their **within-file cross-language ratios** are
> comparable with anything.

**The wrapper is what's measured, not the source.** A drain that only calls
`next()` measures the underlying iterator — the slot bookkeeping is two field
accesses per element and vanishes into the cost of walking a `Vec`. So the mix is
peek-heavy: two peeks per next, the pattern the wrapper exists to support.

The operation mix is **deterministic**, not random, so every lane executes an
identical sequence — a randomly-driven bench would need the RNG mirrored exactly
across four languages just to be comparable, and any drift shows up as a
performance difference that is really a workload difference.

320 rounds over 200,000 elements. Every lane prints `434217027 64000000` — the
sink *and* the pull count.

**Apple M5 Pro (6P+12E), 2026-11-02**, `karac 0.9.0-dev.14057+g6697158fa`
(v2/MIR backend), hyperfine 30 runs, `KARAC_AUTO_PAR=0`:

| lane | time | vs C |
|---|---:|---:|
| `rustc -O` | 601.7 ms ± 3.1 | 1.00× |
| `clang -O3` | 602.4 ms ± 4.4 | 1.00× |
| `go build` | 642.3 ms ± 3.9 | 1.07× |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **645.2 ms ± 5.0** | **1.07×** |
| **`karac build`** | **654.6 ms ± 6.5** | **1.09×** |

**1.01× against the equal-safety comparator** (1.5%, about 1.5σ) — a tie with
the build that does what Kāra does, while C and `rustc -O` tie each other ~9%
ahead of Kāra; on this host the overflow checks cost Rust 7.2%. Against the previous M5
feed (2026-08-28, `karac g9b221e799`, legacy backend) the ratios are flat:
Kāra/Rust 1.08× → 1.09×, Kāra/C 1.08× → 1.09×, Kāra/Go 0.98× → 1.02×,
Kāra/equal-safety 1.00× → 1.01× (every comparator ran 12–16% slower in absolute
ms this session).

Kāra's binary is 295.8 KiB (302,872 B) against C's 32.8 KiB, Rust's 455.4 KiB
and Go's 2.38 MiB; every v2/MIR Kāra binary is ~300–390 KB where the legacy
backend's were ~34 KB (tracked as
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Peak RSS is 4.3 MiB for
Kāra, 4.2 MiB for Rust, 4.1 MiB for C and 11.8 MiB for Go. Cold compile:
`karac build` 120.0 ms ± 1.1 (57.8 MiB peak), `rustc -O` 89.4 ms (29.9 MiB),
`clang -O3` 49.0 ms (2.6 MiB).

Container x86 run (history, `bench/results.container-x86.json`):

| lane | time | vs C |
|---|---:|---:|
| **`rustc -O -C overflow-checks=on`** (equal safety) | **927.3 ms ± 5.6** | **0.98×** |
| **`karac build`** | **941.5 ms ± 12.9** | **0.99×** |
| `clang -O3` | 946.3 ms ± 5.8 | 1.00× |
| `rustc -O` | 961.6 ms ± 6.4 | 1.02× |
| `go build` | 1163 ms ± 56 | 1.23× |

**1.02× against the equal-safety comparator**, and the four compiled lanes span
under 4% — close enough that ordering between them is not a meaningful result.
Note that overflow-checked Rust came out *faster* than unchecked here (927 vs
962 ms), which is a clear sign the difference is noise and layout rather than
codegen: checks cannot make code faster.
*(2026-11-02: on the M5 feed above the ordering is the expected one — checked Rust is 1.07× unchecked — and Kāra is the slowest compiled lane, 1.09× C.)*

What the workload really exercises is struct-field access through a nested owned
struct — `p.src.pos` on every operation — so all four are doing the same handful
of loads and stores per element.

### No parallel lane

A wrapper is a sequential state machine: every operation depends on what the
previous one left in the slot. The rounds could be fanned out, but they drive an
identical sequence over identical data and would measure the harness.
[#282](../282-expression-add-operators/) is where a fan-out was genuinely
available and I had wrongly skipped it.

## Running

```bash
karac run peeking_iterator.kara
karac run peeking_iterator_lazy.kara
karac run peeking_iterator_materialized.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in peeking_iterator peeking_iterator_lazy peeking_iterator_materialized differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
