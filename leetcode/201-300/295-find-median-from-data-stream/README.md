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
| `median_finder_stdlib.kara` | the ★ algorithm on the stdlib `PriorityQueue` | O(log n) | O(1) |
| `differential.kara` | 900 streams, **four** arms, five properties | — | — |
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
| **P1** | all **four** arms agree after **every** add, not just at the end |
| **P2** | the median depends only on the multiset — reordering cannot move it |
| **P3** | A's heap invariant holds: `max(lo) <= min(hi)`, sizes balanced |
| **P4** | `min <= median <= max`, and for an odd count the median is a member |
| **P5** | `i64.MIN` and `i64.MAX` survive — the negation max-heap would trap |

900 streams, 18,250 adds, every prefix of every stream compared three ways.
Streams alternate between a wide value spread and a deliberately repeat-heavy
one, so C's distinct-key path and its within-run median both get hit.

**Bands are sized by the tree-walk interpreter**, the slowest of the four
surfaces every kata must agree on. The durable fact is the RATIO — the
interpreter runs this file **~1500-1900x** slower than the compiled build — and
that is what sizes it: the compiled build could afford a hundred times the
streams, and the interpreter is the whole of the constraint.

> The absolutes are machine-dependent and should not be read as fixed. First
> recorded as 19s interpreted with three arms; re-measured at 46.2s once a fourth
> arm joined and on a slower container,
> where the C benchmark binary — unchanged, same compiler — also ran 33% slower,
> which is how you can tell that is the machine and not a regression. The
> compiled side is **23.7ms ± 3.0** with four arms (18.2ms ± 0.4 with three); an earlier "0.01s" here was an artifact of
> `/usr/bin/time`'s 10ms resolution rather than a measurement.

### The differential was checked for its ability to fail

A differential that cannot fail proves nothing, so this one was mutation-tested
— four deliberate bugs introduced one at a time, each of which it must catch:

| mutation | caught |
|---|---|
| A averages nothing: even counts return `lo`'s root alone | ✅ |
| the sift-down forgets the right child | ✅ |
| C reads only the second rank (the run-straddling bug named above) | ✅ |
| `lower_bound` starts at 1, so B inserts out of range | **found `B-2026-08-24-15`** |

## The fourth mutation: `B-2026-08-24-15`, found here and now fixed

The broken `lower_bound` made arm B call `Vec.insert(1, v)` on an empty vec.
design.md says `insert` "panics if out of bounds" and `karac run --interp`
did — but **neither compiled backend checked at all**, so instead of a panic
the mutation produced a glibc `free(): invalid pointer` abort.

Reduced away from the kata, on a `Vec[i64]` holding two elements. The right
column is what this kata found; the fix landed in `114a9d2` and the fourth
column is the same probe re-run after it:

| op | `--interp` | compiled, when filed | compiled, now |
|---|---|---|---|
| `v.insert(7, 9)` | panic | `free(): invalid pointer`, exit 134 | panic, exit 101 |
| `v.remove(7)` | panic | `free(): invalid pointer`, exit 134 | panic, exit 101 |
| `v.swap_remove(7)` | panic | **no error, exit 0** | panic, exit 101 |
| `v[7]` | panic | panic, exit 101 | panic, exit 101 |

The last row was the control, and it is what made this a bug rather than a
policy: plain indexing **was** checked in codegen, so the split was
inconsistent inside one type. `swap_remove` was the worst of the three because
it did not crash — the AOT build returned `0`, set `len` to 1 and dropped an
element with a clean exit; under the JIT the same call returned
`94405721258608`, a live heap pointer handed back as an `i64`.

The cause was in `insert`'s lowering: `move_count` is computed as `len - idx`,
so `idx > len` made it negative and it reached `memmove` as a huge unsigned
byte count. The fix is one `icmp` + branch per call site, and the one subtle
part is that the predicate is not the same for all three — `insert` compares
UGT because `insert(len, v)` is a legal **append**, while `remove` and
`swap_remove` compare UGE. Using UGE for `insert` would have traded a
memory-safety hole for a broken `push`.

The mutation itself is the shortest proof the fix works. It used to die with
`exit 139`, SIGSEGV, no diagnostic. Now:

```
panic at m4.kara:168:23 in ss_add: Vec.insert index out of bounds
```

**The kata never depended on the bug and was unaffected by it or by the fix.**
It surfaced only because the differential was being checked for its ability to
fail, which is the one test that finds a compiler bug instead of a kata bug.

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

> These numbers were taken before `B-2026-08-24-15`'s bounds-check fix and
> **still stand**, which is a structural fact rather than a hope: the fix adds
> a compare to `insert` / `remove` / `swap_remove`, and the benched path calls
> none of them — the heap is `push` and `pop` only. (`Vec.insert` appears in
> arm B, which is not a bench lane.) Re-running on the fixed compiler gives the
> identical sink and 373.1 ms ± 39.6 against the recorded 382.6 ± 24.0, well
> inside this container's ~10% variance.

| lang | mean | vs C | notes |
|---|---:|---:|---|
| C | 240.9 ms ± 21.9 | 1.00× | hand-rolled heap, 16 KiB binary |
| Rust (`-O`) | 317.7 ms ± 31.2 | 1.32× | hand-rolled heap |
| Rust (`-O`, overflow-checks=on) | 360.7 ms ± 25.3 | 1.50× | equal-safety twin |
| **Kāra** | **382.6 ms ± 24.0** | **1.59×** | hand-rolled heap, 337 KiB binary |
| Go | 604.8 ms ± 33.1 | 2.51× | hand-rolled heap |

> **Re-measured 2026-08-25 on a later compiler: Kāra's gap to C narrowed from
> 1.59x to 1.47x** (469.7ms ± 13.9 against C's 320.1ms ± 5.7, 20 runs). Both
> absolutes are higher than the table because that run was on a slower container
> — C moved too, on an unchanged binary — so only the ratio carries across, and
> it moved in Kāra's favour. The table below is the recorded run; the JSON keeps
> its environment stamp.

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

### The stdlib gained a `PriorityQueue`, and it now does this problem

When this kata was written there was no stdlib heap, and the section above named
that as a gap. **It has since landed**: `PriorityQueue[T: Ord]`, a `Vec`-backed
binary heap in `runtime/stdlib/priority_queue.kara`, smallest-first by default
with a `max_first()` sibling — exactly the two directions the two-heap median
wants.

It arrived without a `peek`, which is the one operation this algorithm needs on
every query: the median *is* the two roots. That was filed as
**`B-2026-08-25-32`** — together with a second defect it exposed, the stdlib
file's own header advertising `peek / len O(1)` for a method present in neither
the file nor design.md's table. **Both are now fixed.**

So the whole kata is expressible against the stdlib type, verified end to end:

```kara
let mut lo: PriorityQueue[i64] = PriorityQueue.max_first();
let mut hi: PriorityQueue[i64] = PriorityQueue.new();
…
lo.push(v);
match lo.pop() { Some(x) => { hi.push(x); } None => {} }
if hi.len() > lo.len() { match hi.pop() { Some(x) => { lo.push(x); } None => {} } }
```

— which builds and reproduces this kata's output exactly.

`peek` returns `Option[T]`, not the `Option[ref T]` the bug report proposed, and
the reason is worth knowing: `Option[ref T]` appears in this stdlib only on
`#[compiler_builtin]` stubs whose bodies are never evaluated, so a real Kāra
body cannot return one. The consequence is that `peek` **copies** the root —
free for a scalar, a clone for a heap-carrying `T`.

**So it is now a fourth arm**, `median_finder_stdlib.kara` — the ★ algorithm
with the hand-rolled `Heap` deleted and `PriorityQueue` called instead. It is in
the differential, so a collection that landed the same day is cross-checked
against three implementations sharing none of its code, and P5 pushes
`i64.MIN` / `i64.MAX` through it.

It also has no negation anywhere, which the ★ arm's header spends a paragraph
earning: `PriorityQueue` ships **both** directions as constructors
(`new()` smallest-first, `max_first()` largest-first), so there is no
`Reverse`-style wrapper and no `-i64.MIN` overflow hazard to avoid.

`peek` returns `Option[T]`, not the `Option[ref T]` the bug report proposed, so
it **copies** the root — free for the `i64` here, a clone for a heap-carrying
element. That is a stdlib-wide constraint rather than an oversight: the only
`Option[ref T]` returns in the stdlib are `#[compiler_builtin]` stubs whose
bodies are never evaluated, so a real Kāra body cannot return one.

**The ★ arm stays hand-rolled**, because writing the heap *is* the exercise for
#295 and because the C/Rust/Go mirrors must implement the same algorithm for
the benchmark to be honest. The two now sit side by side: what the exercise
asks for, and what you would actually write.

### A fourth mutation, and a symmetry worth knowing

Arm D was mutation-tested like the rest. Reading only `lo`'s root on an even
count, and dropping the rebalance, are both caught. **Swapping the two
constructors is not** — and that is correct, not a gap:

```kara
lo: PriorityQueue.new(), hi: PriorityQueue.max_first()   // both flipped
```

produces byte-identical output over all 18,250 adds. The algorithm is symmetric
under flipping *both* directions: `lo` then holds the upper half with its
minimum at the root and `hi` the lower half with its maximum, and those are the
same two middle elements, named in the other order. Confirmed by diffing the
binaries, not by argument.
