# 288. Unique Word Abbreviation

Abbreviate a word as **first letter + middle length + last letter**, so `deer`
becomes `d2r` and `internationalization` becomes `i18n`. A word of two
characters or fewer has no middle to shrink and abbreviates to *itself* — the
encoding would otherwise be longer than the word.

Build a dictionary once, then answer `is_unique(word)` many times. The word is
unique when **no** dictionary word shares its abbreviation, **or** when every
dictionary word that shares it *is that same word*.

```
dictionary = ["deer", "door", "cake", "card"]

is_unique("dear")  ->  false    "d2r" is also "deer", and "deer" != "dear"
is_unique("cart")  ->  true     "c2t" belongs to nobody
is_unique("cane")  ->  false    "c2e" is "cake"
is_unique("cake")  ->  true     "c2e" is "cake" — which IS the word asked about
```

## Approaches

| file | index | build | query |
|---|---|---|---|
| `unique_word_abbr.kara` ★ | `Map[String, Bucket]` — `Sole(word)` \| `Conflicted` | O(n·w) | O(w) |
| `unique_word_abbr_buckets.kara` | `Map[String, Vec[String]]` — every distinct colliding word | O(n·w·c) | O(w) |
| `unique_word_abbr_counts.kara` | `Map[String, i64]` + `Set[String]` | O(n·w) | O(w) |
| `unique_word_abbr_brute.kara` | none — the predicate, transcribed | — | O(n·w) |
| `differential.kara` | 3600 queries, four solvers, three density axes | — | — |

`n` is the dictionary size, `w` the word length, `c` a bucket's width.

## The index is a three-way choice

Per abbreviation the dictionary is in exactly one of three states: nothing has
it, exactly one distinct word has it, or two or more do. Only the middle state
needs to remember anything, so the ★ file writes:

```kara
enum Bucket {
    Sole(String),
    Conflicted,
}
```

with "nothing has it" left to the map's own absence. Once two distinct words
collide, *which* words they were stops mattering — no later query can be
answered differently by knowing them — so `Conflicted` carries no payload and
the strings are dropped. `unique_word_abbr_buckets.kara` keeps every colliding
word alive to support an answer that was already decided; that is the honest
cost of the obvious first index.

The bucket-list file earns its place elsewhere: it is the only one that can
still answer **which** words collide, so `collisions_of` there is a real
function rather than one needing a re-scan.

## The trap is duplicates

The dictionary is a **multiset on input** and a **set in meaning**. Given
`["deer", "deer"]`, `is_unique("deer")` is **true** — the only word abbreviating
to `d2r` is `deer` itself. An index that counts *occurrences* rather than
*distinct words* reads 2 and answers false.

Each file pays for this differently, and each payment is a place to get it
wrong:

- ★ compares `prev != w` before promoting `Sole` to `Conflicted`.
- buckets guards its push with `contains` — the bucket is a *set* that happens
  to be stored as a list.
- counts bumps only on a word its `Set` had not yet seen, so the guard **is**
  the set insert and there is no separate check to forget.
- brute force cannot get it wrong at all: it excludes `d == word` on every
  occurrence, so a repeat behaves like a single entry without anything having
  to deduplicate it.

That last property is why the brute-force file is the differential's reference.
It has no representation to be wrong about — the other three pre-compute an
index and then *argue* the index preserves the predicate.

## Verifying it

`differential.kara` runs all four against 3600 queries over three axes —
alphabet size, dictionary size, and word length — and reports its own coverage
rather than just a pass:

```
cases 3600
mismatches 0
dictionaries 360, of which with a repeated word 140
answers true 3202, false 398
```

The coverage lines are the point. A differential that reports zero mismatches
while never building a dictionary with a repeat, or while every answer comes
back the same, has proved nothing. Word **length** is the axis that controls how
hard the abbreviation squeezes: a 1–2 character word abbreviates to itself and
can only collide by being equal, while a 5-character word over a 2-letter
alphabet has just four possible abbreviations. Both regimes are generated,
because the short one is the only thing that exercises the `n <= 2` branch.

It is also mutation-tested. Breaking the duplicate guard in any one of the three
indexes — `contains` in buckets, `prev != w` in ★, the `Set` insert in counts —
produces **582 mismatches**, with the differential naming the broken solver
while the other three agree.

## What this kata found

`Set.contains(w)` with `w: ref String` was rejected by the typechecker:
*expected 'String', found 'ref String'* — against a spec (design.md § Set) that
reads `fn contains(ref self, val: ref T) -> bool`.

The rule had already been established: `B-2026-08-15-22` fixed exactly this for
`Vec`/`VecDeque`, on the grounds that *a probe scans for its needle and never
keeps it, so a borrowed needle is exactly as usable as an owned one*. That fix
was inlined at the two arms it was reported against and never swept sideways, so
four more probes — `Set.contains`, `SortedSet.contains`, both `remove`s, and
both `binary_search`es — kept comparing raw types and rejecting a `ref`, each
against its own written signature.

The cause was structural: the set arms grouped `"contains" | "insert" | "remove"`
into one match arm, so the probes inherited `insert`'s ownership requirement —
and `insert` genuinely does store its argument (`val: T`), so the grouping had
to be split rather than patched. Filed and fixed as `B-2026-08-19-21`.

I also filed a second row, `B-2026-08-19-22`, claiming `String` had no indexed
character access. **That was wrong and the row was closed as invalid.**
`s.char_at(i) -> Option[char]` exists — specced, implemented across typechecker,
interpreter and codegen, and named in the help text of the `s[0]` compile error.
I had read a single per-type API table and concluded the capability was absent
without grepping either design.md or the compiler.

The correction is worth keeping because it cuts the other way too: design.md
§ Character access explicitly *sanctions* the phrasing these solvers use —
"when repeated indexed access is genuinely needed, convert first:
`let chars: Vec[char] = s.chars().collect()` — then `chars[i]` is O(1) on a type
where that is honest." So `abbrev`'s `collect()` is the recommended spelling,
not a workaround for a missing feature.

One measurement from that row survives, reframed as an ordinary cost of
phrasing rather than evidence of a gap: replacing the `collect()` in `abbrev`
with a single `chars()` walk that tracks first and last in flight is worth
**1.30× ± 0.18** (274.6 ms → 212.0 ms) on the bench below. It buys that because
it makes *one* pass; a `char_count()` + two `char_at()` rewrite makes three, and
was measured at no gain at all. The solvers keep `collect()` — readable, and
what the spec recommends.

None of this accounts for the whole gap: Kāra is 2.76× slower than Go here, and
the allocation closes only part of it. The rest is undiagnosed — plausibly
String hashing and the per-query abbreviation construction, but that has not
been measured and is not claimed.

## The par lane, and the two bugs it took to get one

The punch loop is 1M independent queries over an immutable index — textbook
order-free fan-out, and `karac build --concurrency-report` said so from the
start, reporting `parallel_reduction { op: +, accumulator: unique_count }`.

For two days it delivered **1.01×, at 0.96 cores busy**. Getting the lane took
two compiler fixes, and the first diagnosis was mine and wrong.

**`B-2026-08-20-3`** — I blamed the fan-out and proposed either declining the
loop or lowering it differently. Both would have been harmful: the loop wanted
to parallelize and would have won by 2.4×. The real cause was the grow chain.
`chars().collect()` lowered to `Vec.new()` plus push-per-char, ~1.5 reallocs per
collect, and every realloc takes the one glibc arena lock all workers share.
Presizing removed the contention.

**`B-2026-08-20-14`** — this loop still didn't move, and bisecting landed on a
single token. `preceding_stmt_init` matched only `let mut i = 0` and had no
assignment arm, so reusing the `i` that already served the build loops declined
as `WhileCounterInitNotFound`. Worth **3.69×**, with the concurrency report
claiming a reduction either way. Widening that gate then exposed a *correctness*
bug — the counter left at its init value after a fanned-out loop — which was
split out and fixed first, rather than trading a perf bug for a wrong answer.

With both in, the lane is real. Container x86_64, 4 cores, sink 573650 across
all seven binaries:

| lane | implementation | mean |
|---|---|---|
| par | c (pthreads) | 31.5 ms |
| par | go (goroutines) | 29.6 ms |
| par | **kāra (auto-par)** | **59.3 ms** |
| seq | c | 92.9 ms |
| seq | go | 86.4 ms |
| seq | rust (overflow-checks=on) | 95.8 ms |
| seq | **kāra (single-threaded)** | **181.2 ms** |

Auto-par is worth **3.06×** (181.2 → 59.3), and the fan-out is real — User time
183 ms against 54 ms wall in the raw hyperfine output.

The honest reading of the cross-language rows: kāra is ~1.9× off C in **both**
lanes (1.88× par, 1.95× seq). Auto-par is therefore carrying its weight —
it delivers about what hand-written threads deliver, and the remaining gap is
the same sequential gap, not something parallelism introduced or hid. That
sequential gap is undiagnosed; plausibly String hashing and the per-query
abbreviation build, but that has not been measured and is not claimed.

**A note on the lane's construction.** Every other par kata carries a
`<stem>_seq.kara` differing from its par twin by a `#[par_order_free]`
attribute. This loop is picked up by the automatic path unaided, so the two
kāra rows here are **the same file built twice** and the only difference is the
compiler's own decision — a byte-identical `_seq.kara` would be a duplicate
asserting nothing. Building the par row with `KARAC_AUTO_PAR=0` would silently
measure the seq binary, so `bench.sh` says so where someone might be tempted.

### The M5 lane, and the `snprintf` bug this kata found — `B-2026-09-05-23`

Everything above was measured on the shared 4-core x86-64 container. Measuring
the canonical Apple M5 Pro (6P+12E) lane found auto-par returning **1.08×** —
15.7 cores burned to gain 8%, at 3.15× the sequential lane's total CPU. That was
filed as `B-2026-08-28-76`, blaming a static equal-count split meeting 12
efficiency cores.

**That diagnosis was wrong, and this kata is what disproved it.** A uniform
reduction that does not allocate scales **9.58×** at 18 workers on the same host
with flat CPU, so the partition was never the problem. What this kata actually
found is that `abbrev` formats — `out.push_str(f"{n - 2}")`, once per call over
1M punches — and f-string interpolation lowered to libc **`snprintf`**, which
serializes on locale and lock state. At 18 workers the program spent **1301 ms
in the kernel** to produce a 107 ms wall.

Fixed in `kara@7542b0f28` by formatting integers through a lock-free,
allocation-free runtime helper instead:

| | seq | par | auto-par worth | sys @ 18 workers |
|---|---:|---:|---:|---:|
| container x86-64, 4 cores | 181.2 ms | 59.3 ms | **3.06×** | — |
| M5, before the fix | 114.5 ms | 106.1 ms | **1.08×** | 1301 ms |
| M5, after the fix | 92.5 ms | 26.8 ms | **3.45×** | 2.5 ms |

The sequential lane got 1.24× faster too, because `snprintf` was the slower path
single-threaded as well — so this was never purely a parallelism defect.

The par lane also **inverts against the hand-written pthreads floor**: C's
mirror, which spawns one thread per logical core and collapses on this host
(72.0 ms, *slower* than its own 57.5 ms sequential build), is now **2.68×**
behind kāra's auto-par. Go still leads the lane at 7.1 ms.

Two findings this kata surfaced went on from here: `B-2026-08-28-76` for
whatever gap was left once formatting was accounted for, and `B-2026-09-05-22` —
**N=2 is pathological here** (179.8 ms against 91.6 at N=1), because that one is
allocation under two workers, not formatting, and the fix above does not touch
it. `B-2026-09-05-22` closed `wontfix`: the N=2 cliff is macOS libmalloc's, not
kāra's. `B-2026-08-28-76` is answered, below.

### What the remaining gap was: one allocation per lookup — `B-2026-09-12-28`

After the `snprintf` fix, kāra's auto-par still returned about **three fifths**
of what a hand-written C pthreads mirror got on the same host and the same
workload, and nothing moved it. Region length did not (stretching the 3 ms
region 10× doubled *both* languages' speedups and left the ratio alone), nor did
working-set size (shrinking the table 16× to an L1-resident 40 KB made it
slightly worse), nor the machine's ceiling (pure-arithmetic C reaches 14.90× at
18 threads, so the cores are real). Auto-par's own dispatch did not either: the
par binary at **one** worker is 1.02× its own seq binary, so the parallel
lowering costs nothing per iteration.

The answer was in the disassembly. `___karac_reduce_worker_0`'s loop body holds
two dyld stubs that resolve to `_malloc` and `_free`. The punch loop is

```kara
let u = match idx.get(a) {
    None => true,
    Some(Bucket.Sole(w)) => w == word,   // reads w, keeps nothing
    Some(Bucket.Conflicted) => false,
};
```

and `Bucket` is an enum with a `String` payload, so it is 32 bytes — tag plus
`String{ptr,len,cap}`. `_karac_map_get` has *already* written those four words
into a stack out-slot; codegen then mallocs 32 bytes, copies the same four words
onto the heap with two `stp`s, runs the arm, and frees the box before the next
iteration. No arm keeps anything.

The control is one edit: `Bucket.Sole` carries an `i64` index into `dict`
instead of an owned `String`, so the matched value has nothing to drop. Worker
malloc/free callsites go 2 → 0 and the sink is unchanged at `unique 5736500`.
10M punches, dual binaries, hyperfine 7 runs:

| lane | seq | par | speedup | user CPU par/seq | vs C |
|---|---:|---:|---:|---:|---:|
| kāra, `Sole(String)` | 319.29 ms | 54.81 ms | 5.83× | 2.37× | 0.56 |
| kāra, `Sole(i64)` | 193.30 ms | 19.96 ms | **9.68×** | **1.32×** | **0.93** |
| C mirror | 150.32 ms | 14.37 ms | 10.46× | 1.34× | — |

One allocation per lookup is the difference between 56% and 93% of the C
mirror's speedup. The parallel run's CPU amplification does not shrink, it goes
away: 2.37× → 1.32×, against C's 1.34×. The sequential gap closes at the same
time, 2.12× → 1.29×.

It read as a *parallel* defect for so long because a malloc/free pair is cheap
on one thread, where libmalloc serves it from a per-thread cache, and expensive
on eighteen — `B-2026-09-05-22`'s ceiling again. A flat per-iteration cost
presents as a scaling loss. So the auto-par question this kata opened is
settled: on a loop that does not allocate, kāra returns 93% of a C pthreads
mirror's speedup with matching CPU efficiency. What is left is codegen, tracked
as `B-2026-09-12-28`.

One caveat on the table: `Sole(i64)` is a *control*, not a proposed rewrite of
the kata. It answers what the box costs; it is not the idiomatic spelling, and
the fix belongs in the compiler.

#### Fixed — the box moved to the stack (`kara@ef9a76f90`)

The compiler already knew the box's lifetime. `track_freshtemp_boxed_enum_
scrutinee` queues a **box-only** free at the enclosing construct's scope frame
for exactly this shape, which is a statement that the box cannot outlive the
`match`. A lifetime bounded by the construct is one an entry-block `alloca`
covers, so `coerce_to_payload_words` now takes an alloca instead of calling
`malloc`, and that registration declines to queue the free. The box pointer
cannot escape: an arm binds the payload through `reconstruct_payload_value`,
which `inttoptr`s word 0 and **loads** `T`, so the binding owns `T`'s inner heap
and the box was only ever a container.

Same 10M punches, dual binaries, hyperfine 7 runs, same lane. Identical sinks
and byte-identical binary sizes in all four:

| lane | seq | par | speedup | user CPU par/seq |
|---|---:|---:|---:|---:|
| baseline karac | 325.36 ms | 55.67 ms | 5.84× | 2.41× |
| stack-box karac | 211.73 ms | 19.91 ms | **10.63×** | **1.23×** |
| C pthreads mirror | 150.32 ms | 14.37 ms | 10.46× | 1.34× |

**1.54× sequentially and 2.80× in parallel**, from deleting one `malloc`/`free`
pair per lookup. kāra's auto-par speedup now edges past the C mirror's, and its
CPU amplification is *lower* than C's — so the auto-par question this kata
opened closes here, on the idiomatic `Sole(String)` spelling rather than on the
`i64` control.

The `Sole(i64)` file stays in `bench/` as the control that located the cost, not
as a recommendation. Write the enum the way the problem reads.

What is **not** covered: `Vec.pop()` / `first()` / `last()` and a
`-> Option[Wide]` return still heap-box per iteration in the same construct.
The mechanism transfers but the plumbing keys on the call's argument slice, and
those take no arguments — tracked as `B-2026-09-12-29`, unmeasured.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-09-07.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

> **Host:** the tables below are a shared **x86-64 Linux cloud container**
> snapshot, kept as [`bench/results.container-x86.json`](bench/results.container-x86.json).
> The canonical Apple M5 Pro lane is [`bench/results.json`](bench/results.json) —
> that is the file `scripts/consolidate-bench.sh` feeds into the top-level chart,
> and it is current as of the date stamped above. Absolute milliseconds are NOT
> comparable between the two hosts; only the **within-file cross-language
> ratios** are.

Container x86_64, 3000-word dictionary built once, then 1M `is_unique` punches
over a 20k-word pool. All five implementations agree on the sink (`unique
573650`). Numbers are from `bench/results.container-x86.json` — the canonical
`results.json` holds Apple-silicon figures and is deliberately not overwritten
from this host.

| | relative |
|---|---|
| go | 1.00 (fastest) |
| c | 1.04 ± 0.06 |
| c (`-march=x86-64-v3`) | 1.03 ± 0.07 |
| rust (`-C overflow-checks=on`, equal-safety) | 1.26 ± 0.11 |
| rust (`-O`) | 1.29 ± 0.11 |
| **kara** | **2.76 ± 0.21** |

The equal-safety row is the honest comparison: Kāra checks integer overflow by
default and `rustc -O` silently wraps, so the `overflow-checks=on` twin is the
like-for-like one. See `BENCHMARKS.md` for the full methodology.

Run-to-run variance in a shared container is real — an earlier run of this same
bench ranked C ahead of Go — so treat the sub-10% separations as noise and only
the Kāra gap as signal.
