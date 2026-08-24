# 295. Find Median from Data Stream

Numbers arrive one at a time. After any of them, `median()` must report the
median of everything seen so far — the middle element when the count is odd,
the mean of the two middle elements when it is even.

```
add 1     median 1
add 3     median 2      (1 3)      -> (1+3)/2
add 2     median 2      (1 2 3)
add 4     median 2.5    (1 2 3 4)  -> (2+3)/2
```

## Approaches

| file | mechanism | insert | query |
|---|---|---|---|
| `median_finder.kara` ★ | two heaps meeting at the middle | O(log n) | O(1) |
| `median_finder_sorted.kara` | binary search + insert into one sorted vec | O(n) | O(1) |
| `median_finder_multiset.kara` | `SortedMap` value→count, walked by rank | O(log d) | O(d) |
| `differential.kara` | 900 streams, three arms, five properties | — | — |
| `bench/medianfinder.kara` | 2M streamed adds, median after every one | benchmark lane | |

## The median is a position, so hold the positions either side of it

The whole problem is that the median moves. Sorting per query is O(n log n)
and keeping one sorted vec pays O(n) per insert to open a slot.

The ★ arm splits the multiset in half: `lo` is a **max**-heap over the smaller
half, `hi` is a **min**-heap over the larger half. Then the two elements
adjacent to the median are exactly the two roots, and a root is O(1) to read.

```
… 1 2 3 │ 4 5 6 …          lo = max-heap{1,2,3}   hi = min-heap{4,5,6}
      ↑   ↑                 lo root = 3            hi root = 4
```

Hold `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`, and an odd count puts
the median at `lo`'s root while an even count averages the two.

### The insert is a shuffle, not a comparison

The tempting insert compares the new value against a root and picks a side.
That works, but it needs a case for the empty heap and another for the tie.
Pushing through `lo` unconditionally has no special cases at all, because each
step restores one invariant and disturbs only the next:

```
lo.push(v)                  lo may now hold a value that belongs in hi
hi.push(lo.pop())           sides are correct; sizes may be off by one
if len(hi) > len(lo):       restore the size invariant
    lo.push(hi.pop())
```

### One heap type, two directions, and why not negation

The usual way to get a max-heap out of a min-heap is to store negated values.
It is one line, and it breaks at exactly one input: `-i64.MIN` overflows, and
**Kāra traps integer overflow by default**, so that version does not return a
wrong answer — it dies. A `max: bool` that flips the comparison costs the same
line and has no such edge.

That is a claim about a design decision, so the differential tests it (P5)
rather than asserting it. The Python mirror negates freely and is *correct* to
do so — its ints are unbounded. The difference is a property of the languages,
not of the algorithm, which is why it lives in the mirror's header rather than
being smoothed away.

## The board is not one game — but the multiset is not one shape either

Arms A and B are both **positional**: they store elements and the median is
wherever the middle lands. A misreading of "median" for even counts would sit
in both and the diff would stay silent.

**C is why the differential is worth running.** It stores no positions — only
a count per distinct value in a `SortedMap`, walked by rank. It cannot share a
positional bug because it has no positions. It is also the only arm whose cost
depends on the number of *distinct* values rather than the total: a thousand
copies of one number cost one key here and a thousand slots in both others.

`SortedMap` has no order-statistic operation, so C walks keys from the smallest
accumulating counts — O(d) per query, the slowest of the three. It picks up
**both** middle ranks in that one walk, because for an even count they may be
the same key (a run covering both) or adjacent keys. Taking only the second and
looking backwards is the version that gets the run case wrong.

## Five properties

| | property |
|---|---|
| **P1** | all three arms agree after **every** add, not just at the end |
| **P2** | the median depends only on the multiset — reordering cannot move it |
| **P3** | A's heap invariant holds: `max(lo) <= min(hi)`, sizes balanced |
| **P4** | `min <= median <= max`, and for an odd count the median is a member |
| **P5** | `i64.MIN` and `i64.MAX` survive — the negation max-heap would trap |

900 streams, 18,250 adds, every prefix of every stream compared three ways.
Streams alternate between a wide value spread and a deliberately repeat-heavy
one, so C's distinct-key path and its within-run median both get hit.

**Bands are sized by the tree-walk interpreter**, the slowest of the four
surfaces every kata must agree on: **19s** under `karac run --interp` against
**0.01s** compiled. That ~1900x ratio is what sizes this file — the compiled
build could afford a hundred times the streams, and the interpreter is the
whole of the constraint.

### The differential was checked for its ability to fail

A differential that cannot fail proves nothing, so this one was mutation-tested
— four deliberate bugs introduced one at a time, each of which it must catch:

| mutation | caught |
|---|---|
| A averages nothing: even counts return `lo`'s root alone | ✅ |
| the sift-down forgets the right child | ✅ |
| C reads only the second rank (the run-straddling bug named above) | ✅ |
| `lower_bound` starts at 1, so B inserts out of range | **found a compiler bug** |

## The fourth mutation: `B-2026-08-24-15`

The broken `lower_bound` made arm B call `Vec.insert(1, v)` on an empty vec.
design.md says `insert` "panics if out of bounds" and `karac run --interp`
does. **Neither compiled backend checks at all**, so instead of a panic the
mutation produced a glibc `free(): invalid pointer` abort.

Reduced away from the kata, on a `Vec[i64]` holding two elements:

| op | `--interp` | `karac run` / `karac build` |
|---|---|---|
| `v.insert(7, 9)` | panic | `free(): invalid pointer`, exit 134 |
| `v.remove(7)` | panic | `free(): invalid pointer`, exit 134 |
| `v.swap_remove(7)` | panic | **no error, exit 0** |
| `v[7]` | panic | panic, exit 101 |

The last row is the control, and it is what makes this a bug rather than a
policy: plain indexing **is** checked in codegen, so the split is inconsistent
inside one type. `swap_remove` is the worst of the three because it does not
crash — the AOT build returns `0`, sets `len` to 1 and drops an element with a
clean exit; under the JIT the same call returned `94405721258608`, a live heap
pointer handed back as an `i64`.

The cause is in `insert`'s lowering: `move_count` is computed as `len - idx`
and handed to `memmove`, so `idx > len` makes it negative and it arrives as a
huge unsigned byte count. `insert(len, v)` — appending at the end — is legal
and correct on both backends; the boundary is exactly `idx > len`.

**The kata does not depend on the bug and is unaffected.** It surfaced only
because the differential was being checked for its ability to fail, which is
the one test that finds a compiler bug instead of a kata bug.

## One deferred feature this kata hit

`heap_invariant_holds` first reached into the owner as `m.lo.data[i]` and was
rejected: **chained field receivers (`a.b.c`) are deferred in codegen**, and
the compiler says so with a fix-it rather than letting it check clean and fail
at build (that gate is `B-2026-08-13-12` / `B-2026-08-16-12`, both fixed). The
check now takes the heap itself, which is the better factoring anyway — a
heap's validity belongs to the heap, not to its owner.

## Benchmarks

2M streamed adds, median read after every one, so the measured work is 2M
inserts plus 2M queries against heaps that grow to 1M elements. A binary heap
resists the optimizer for a reason BENCHMARKS.md cares about: the sift path is
a chain of **dependent** loads — each level's index comes from the previous
level's comparison — so there is nothing to vectorise and nothing to reorder
across.

All five languages produce the identical sink, `checksum 831081041`, over the
identical 2M adds. The sink hashes **twice** the median, which is always a whole
number, so no float formatting enters the comparison.

Container, x86-64, 4 cores; full numbers in
[`bench/results.container-x86.json`](bench/results.container-x86.json). See
[BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| lang | mean | vs C | notes |
|---|---:|---:|---|
| C | 240.9 ms ± 21.9 | 1.00× | hand-rolled heap, 16 KiB binary |
| Rust (`-O`) | 317.7 ms ± 31.2 | 1.32× | hand-rolled heap |
| Rust (`-O`, overflow-checks=on) | 360.7 ms ± 25.3 | 1.50× | equal-safety twin |
| **Kāra** | **382.6 ms ± 24.0** | **1.59×** | hand-rolled heap, 337 KiB binary |
| Go | 604.8 ms ± 33.1 | 2.51× | hand-rolled heap |

**Kāra and equal-safety Rust are a tie here, and the σ is the reason to say so
rather than claim a winner.** The table's 382.6 vs 360.7 looks like a 1.06×
loss, but a focused 30-run rerun put them at 359.9 ± 36.1 and 348.0 ± 33.8 — a
gap of 12 ms against a spread of ~35 ms. This container's run-to-run variance
is ~10%, which is larger than the effect, so the honest reading is that the two
are indistinguishable on this workload and only C is clearly ahead.

That is a different result from [#294](../294-flip-game-ii/), where Kāra beat
equal-safety Rust outright on `Map`-heavy work. Nothing contradictory: that
workload was dominated by hashing, this one by dependent pointer-chasing
through a heap, and the two languages trade places with the bottleneck.

### Every mirror hand-rolls its heap, except Python

C, Rust and Go all implement the same sift loop by hand rather than calling
`std::collections::BinaryHeap`, `container/heap`, or an equivalent. That is
deliberate: **Kāra has no stdlib heap**, so calling a tuned library heap on the
other side would measure library maturity rather than code generation, and
`container/heap` would additionally measure Go's interface devirtualisation.

Python is the exception and uses `heapq`, because a Python-level sift loop
measures interpreter dispatch and nothing else. It still runs the full 2M adds
and lands at ~2.4s — no scale-down was needed, and its sink matches the other
four exactly.

The absence of a stdlib heap is worth naming as a gap rather than leaving
implicit: `Vec`, `Map`, `Set`, `VecDeque`, `SortedMap` and `SortedSet` all
ship, and a priority queue is the obvious missing member of that set. This
kata works fine without one — hand-rolling the heap **is** the exercise for
#295 — but a language that has `SortedSet.min` and no `BinaryHeap` will send
every scheduler, Dijkstra and top-k program through a hand-rolled sift loop.
