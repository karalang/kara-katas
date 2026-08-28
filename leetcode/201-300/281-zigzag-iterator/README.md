# 281. Zigzag Iterator

Return two lists' elements alternately. `[1,2]` and `[3,4,5,6]` gives
`1 3 2 4 5 6` — once a list runs out, the rest of the other follows in order.

**The follow-up is the real problem:** *what if you are given k lists?* A solution
written around `v1`/`v2` with a boolean toggle answers the example and collapses
at k=3, so this kata is written for k from the start and treats k=2 as one case
among many.

## Approaches

| file | mechanism | state |
|---|---|---|
| `zigzag_iterator.kara` ★ | cursor per list, turn pointer that skips | `cursor[]`, `turn` |
| `zigzag_iterator_queue.kara` | queue of lists that still have elements | `cursor[]`, queue |
| `zigzag_iterator_eager.kara` | the definition, materialized by rounds | **none** |
| `differential.kara` | 1500 list-sets, 13273 elements | — |
| `bench/zigzag.kara` | 64 unequal lists, drained 2200 times | benchmark lane |

## "Next" is not `turn + 1`

That one line is the whole problem. `next()` hands back
`lists[turn][cursor[turn]]`, bumps the cursor, then advances `turn` to the next
**non-exhausted** list, wrapping. A plain `turn = (turn + 1) % k` is wrong rather
than merely inelegant: on `[[1],[],[2]]` it hands back 1, moves to the empty list
and reads past its end.

So the advance has to *skip*, and it has to terminate when nothing is live —
which is what `settle` and its `tried < k` bound are for.

## The queue makes the skip disappear rather than solving it

Exhausted lists are never in the queue, so there is nothing to skip past and no
wrap-around to get wrong — the ★ solver's `settle` loop, where its bugs live, has
no counterpart. Empty lists are handled at *construction*: `[[1],[],[2,3]]`
starts with two queue entries, not three.

That's the trade — a queue's memory traffic buys away a class of state bug.

## Why the eager version is the oracle

Both iterators carry state between calls, and **every bug in this problem is a
state bug** — a turn that fails to wrap, a cursor bumped twice, a queue entry
pushed back when it shouldn't be. Different bookkeeping, same *kind* of thing.

The eager version has no state between elements at all:

```
for r = 0, 1, 2, ...:  for each list i in order:
    if list i has an element at index r, emit it
```

That's the specification, transcribed. A state bug and a transcription of the
definition have no way to agree.

```
cases 1500, elements interleaved 13273
cases containing at least one EMPTY list 567
cases where every list is empty 57
digest 213337647
cursor vs the definition 0
queue  vs the definition 0
```

The generator leans on the shapes that break iterators, not on size: empty lists
anywhere, wildly unequal lengths so lists drop out at different rounds, and k
from 1 to 5. **567 of 1500 cases contain an empty list and 57 are entirely
empty.** Equal-length non-empty lists would exercise none of the skipping logic —
the entire difficulty — and every solver would pass.

The sink is the full sequence, position-weighted, because interleaving is an
*ordering* problem: a multiset check would accept any permutation.

## What the injected bugs did

| injection | result |
|---|---|
| cursor: advance without skipping exhausted lists | **traps** — index 5 out of bounds (len 5) |
| cursor: don't settle the seed turn | **traps** — index 0 out of bounds (len 0) |
| cursor: settle scans forward but never wraps | **traps** — index 2 out of bounds (len 2) |
| queue: push back unconditionally | **traps** — index 6 out of bounds (len 6) |
| queue: admit empty lists at construction | **traps** — index 0 out of bounds (len 0) |
| **eager oracle: emit whole lists in turn, not by round** | cursor **1025**, queue **1025** |

**Five of six injections trap rather than answering wrongly**, which is unlike
[#276](../276-paint-fence/), [#278](../278-alien-dictionary/) and
[#280](../280-wiggle-sort/), where the same exercise produced confident wrong
answers. State bugs in this problem read off the end of a list, and Kāra's bounds
checking turns them into located runtime errors instead of silent garbage. The
differential's job here is correspondingly narrower — it earns its place on the
last row, where breaking the *oracle* is caught by both iterators at once, and on
the ordinary case of a bug that stays in bounds.

That is worth saying plainly rather than dressing the table up: for this problem
the language catches most of what a harness would, and the harness catches what
the language cannot.

## A compiler bug this kata found

`B-2026-08-17-30` — **E0218 tells you the exact text to insert and `karac fix`
still declines it.** The diagnostic ends with ``Write `mut <expr>`.`` but carries
no `replacement`, while its exact inverse does:

| code | message | `replacement` | `karac fix` |
|---|---|---|---|
| E0218 | *"…requires a `mut` marker… Write `mut <expr>`"* | **no** | declines |
| E0219 | *"…already a mut-ref; drop the `mut` marker"* | yes | applies |

Adjacent codes, the same call-site marker, opposite directions — the one that
*removes* text is machine-applicable, the one that *adds* it isn't. Unlike
[`B-2026-08-17-11`](../278-alien-dictionary/), there's no hazard justifying the
gap: E0218 has exactly one correct repair, with no direction to choose. Filed
low; two of this session's katas hit it.

## Kāra features exercised

- **A struct with `mut` fields** carrying iterator state, mutated through
  `mut ref` free functions — the shape LeetCode's class would have, minus the
  ceremony.
- **`Vec[Vec[i64]]` with ragged and empty rows**, including all-empty.
- **Modular wrap-around with a visit bound** (`tried < k`) — the termination
  guarantee is the interesting part, not the arithmetic.

## Running

```bash
karac run zigzag_iterator.kara
karac run zigzag_iterator_queue.kara
karac run zigzag_iterator_eager.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in zigzag_iterator zigzag_iterator_queue zigzag_iterator_eager differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-08-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

> **Host:** the tables below are a shared **x86-64 Linux cloud container**
> snapshot, kept as [`bench/results.container-x86.json`](bench/results.container-x86.json).
> The canonical Apple M5 Pro lane is [`bench/results.json`](bench/results.json) —
> that is the file `scripts/consolidate-bench.sh` feeds into the top-level chart,
> and it is current as of the date stamped above. Absolute milliseconds are NOT
> comparable between the two hosts; only the **within-file cross-language
> ratios** are.

**k matters more than n here**, which is what makes this worth benching. Both
iterators are O(1) amortized per element, but the cursor version's skip scan
walks past exhausted lists — bounded by k, and only cheap while few lists are
dead. As lists drop out at different rounds that scan lengthens, so the
interesting axis is *many lists of unequal length*, not one long list.

64 lists with lengths spread over three orders of magnitude, drained end to end,
2200 rounds. Every lane prints `864303988`.

| lane | time | vs equal-safety Rust |
|---|---:|---:|
| `rustc -O` | 646.8 ms ± 19.6 | 0.89× |
| **`karac build`** | **729.3 ms ± 25.6** | **1.00×** |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **730.0 ms ± 25.2** | **1.00×** |
| `go build` | 767.5 ms ± 21.9 | 1.05× |
| `clang -O3 -march=x86-64-v3` | 811.4 ms ± 15.4 | 1.11× |
| `clang -O3` | 837.3 ms ± 39.3 | 1.15× |

Kāra and equal-safety Rust are **within 0.7 ms of each other** — the closest
match in this corpus, and comfortably inside one σ, so the honest claim is a tie
rather than a win either way.

C being the *slowest* lane is unusual and worth flagging rather than quietly
publishing: each list is a separate `malloc`, so `lists[t][cursor[t]]` chases a
pointer into scattered allocations, while Rust's and Kāra's `Vec<Vec<…>>` land
their headers contiguously. That's a data-layout difference between the mirrors,
not a codegen result — the algorithm is identical in all four.

### No parallel lane

A drain is inherently sequential: which list is read next depends on which
cursors the previous step advanced. The rounds could be fanned out, but they all
re-drain the *same* lists and would measure the harness rather than the
iterator. [#276](../276-paint-fence/) and [#277](../277-find-the-celebrity/) fan
out because they have genuinely independent instances.

### A note on the kernel's shape

The bench does **not** use the kata's `Zigzag` struct. A struct field is *owned*,
so a `Zigzag` holding the lists would take them by value and every round would
copy 64 lists before iterating — the bench would measure copying. The kernel
keeps the same three pieces of state as locals over a borrowed
`ref Vec[Vec[i64]]`: same algorithm, ownership arranged for repetition rather
than for the API the problem describes.
