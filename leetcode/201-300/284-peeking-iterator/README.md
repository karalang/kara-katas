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
