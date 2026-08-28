# 296. Smallest Rectangle Enclosing Black Pixels

A binary image: `1` is a black pixel, `0` is white. **Every black pixel is
connected** to every other, and you are given the coordinates of one of them.
Return the area of the smallest axis-aligned rectangle enclosing all the black
pixels.

```
0 0 1 0        black spans rows 0..2 and cols 1..2,
0 1 1 0        so the rectangle is 3 x 2 and the area is 6
0 1 0 0
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `smallest_rectangle.kara` ★ | binary search on the row/col projections | O(m log n + n log m) |
| `smallest_rectangle_scan.kara` | look at every pixel, track min/max | O(m·n) |
| `smallest_rectangle_flood.kara` | flood fill the component from the seed | O(k), k = black pixels |
| `differential.kara` | 1400 images, three arms, five properties | — |
| `bench/blackpixels.kara` | 4096² frame, 1200 queries | benchmark lane |

## The precondition is the algorithm

Project the black pixels onto the row axis and ask, per row, "any black here?"
Because the pixels form **one connected region**, the rows answering yes are an
unbroken **interval** — you cannot have a black row, a white row, and another
black row, because the region would have to jump the gap. Same for columns.

```
rows:  . . # # # . . .        contiguous, so binary-searchable
             ↑ seed
```

A contiguous interval with a known interior point is exactly what binary search
wants, and the seed pixel is that point. Four searches give the four edges:

```
top    = first r in [0, x]  with a black pixel
bottom = first r in (x, h]  with NO black pixel
left   = first c in [0, y]  with a black pixel
right  = first c in (y, w]  with NO black pixel
```

Each probe costs one row or column scan and there are log-many probes.

## Three arms that need the hypothesis differently

This is why the differential is worth running rather than being one algorithm
written three times:

| arm | what it needs connectivity for |
|---|---|
| **A** binary search | the **projections** must be hole-free, or bisection steps over a black row |
| **C** flood fill | every black pixel must be **reachable** from the seed |
| **B** full scan | **nothing** — correct on any binary image whatsoever |

So B is the oracle, and an oracle with teeth: it can catch A and C *together*,
and it is the only arm that survives P5.

The three also occupy different corners of the cost space. B is O(m·n) however
little ink there is. A is O(m log n + n log m) regardless too. **C is the only
arm that gets cheaper as the image gets sparser** — one black pixel in a
million-pixel frame costs it a single iteration — and the only one that gets
worse as the ink gets dense, since it pays a visited-write and four neighbour
pushes per pixel.

## Five properties

| | property |
|---|---|
| **P1** | all three arms agree on every connected image |
| **P2** | the reported rectangle matches B's explicit min/max bounds |
| **P3** | A and C are **seed-independent** — same answer from any black pixel |
| **P4** | transposing the image leaves the area unchanged |
| **P5** | on a **disconnected** image, A and C go wrong and B stays right |

1400 images, 3924 black pixels, every arm run from **every** black pixel as
seed. Images are grown by a random walk from the middle, so connectivity holds
by construction rather than by hope.

**P5 is not a bug report.** It is the hypothesis of the theorem shown to be
necessary. Withdraw connectivity — two black corners with a gap between them —
and the measured result is:

```
P5 disconnected: B wrong 0, A wrong 200, C wrong 200, overcounts 0
```

Both clever arms fail **every single time**, and always by *undercounting*:
they lose pixels, they never invent them. The test asserts that failure count
is exactly the number of disconnected images, because a P5 that found zero
disagreements would mean the generator never produced a disconnected image —
i.e. the test had gone vacuous.

**Bands are sized by the tree-walk interpreter**, the slowest of the four
surfaces every kata must agree on: 7.1s interpreted against 22ms compiled.

### The differential was checked for its ability to fail

Four deliberate bugs, introduced one at a time:

| mutation | caught |
|---|---|
| scan forgets to widen `right` | ✅ |
| flood fill pushes only three of four neighbours | ✅ |
| transpose writes the wrong index | ✅ (as a bounds panic) |
| bisection direction inverted in `first_black_row` | ✅ |

A fifth mutation — starting the `bottom` search at the seed row instead of one
past it — was **not** caught, and that is correct: it is an **equivalent
mutant**. `first_white_row` looks for the first row with *no* black, and the
seed row is black by precondition, so including it cannot change the answer.
Confirmed by diffing the two binaries' output rather than by argument.

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

One 4096² frame built **once**, then 1200 min-area queries from varying seeds —
build-once-and-punch, so the measurement is the query and not a 16.7M-pixel
memset. The bisection is a chain of dependent branches whose next index comes
from the previous probe, so there is nothing to vectorise and nothing to hoist.

Sparse on purpose: this is the regime where binary search is supposed to beat
the O(m·n) scan. All four compiled lanes produce `checksum 312731232`.

Container, x86-64, 4 cores; full numbers in
[`bench/results.container-x86.json`](bench/results.container-x86.json). See
[BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| lang | mean | vs C | notes |
|---|---:|---:|---|
| Go | 568.9 ms ± 16.8 | 0.88× | 2178 KiB binary |
| **Kāra** | **614.1 ms ± 13.2** | **0.95×** | sequential lane, 341 KiB binary |
| Rust (`-O`, overflow-checks=on) | 618.6 ms ± 10.7 | 0.95× | equal-safety twin |
| Rust (`-O`) | 623.8 ms ± 15.0 | 0.96× | |
| Rust (`-O`, target-cpu=v3) | 630.3 ms ± 8.3 | 0.97× | |
| C | 648.2 ms ± 10.7 | 1.00× | 16 KiB binary |

**C is last here, and that is not a typo.** It is the first kata in this series
where C is not the baseline winner, so the obvious suspicion is a handicapped C
mirror — the C version passes the image through file-scope globals while the
other three pass it explicitly. That was tested and rejected: a param-passing C
rewrite measures 570.0 ms against the globals version's 573.8 ms, a 1.01×
difference, i.e. noise. **Why C trails Go by 1.43× on this workload is
unattributed**; ruling out the mirror's shape is what has been established, not
the cause.

Kāra beats both Rust configurations and trails only Go, which is a better
showing than [#295](../295-find-median-from-data-stream/)'s tie against
equal-safety Rust — different bottleneck, different ordering.

### The par lane — Kāra writes no parallel code and still wins it

The seq table above is single-threaded on every row: `bench.sh` builds the Kāra
lane with `KARAC_AUTO_PAR=0`, because timing an auto-parallelised binary against
single-threaded C, Rust and Go would credit code generation with free
parallelism. BENCHMARKS.md records an earlier incident where exactly that
happened, and `scripts/lint-par-lane.py` exists to catch it.

The par lane is where the parallelism belongs. **All four rows do the same
four-way fan-out** — the difference is who wrote it:

| lang | mean | who wrote the parallelism |
|---|---:|---|
| Go | 393.9 ms ± 7.0 | 3 goroutines + `WaitGroup`, by hand |
| **Kāra** | **406.2 ms ± 16.7** | **nobody — `karac` inferred it** |
| C | 525.8 ms ± 24.5 | 3 raw `pthread_create` per call, by hand |
| Rust | 574.9 ms ± 15.1 | two nested `rayon::join`, by hand |

Kāra ties Go (1.03× ± 0.05 — inside the noise) and beats hand-written C and
Rust, **from source containing no concurrency construct at all**. Against its
own sequential build it is 614.1 → 406.2 ms, a **1.51×** self-speedup.

Why not 4× on four branches: the branches are unequal. The two **column**
searches stride by `w` and miss cache on nearly every probe while the two
**row** searches walk contiguous bytes, so the critical path is the slowest
branch, not the average.

Why C and Rust trail: both pay per-call. C creates three OS threads on every
one of the 1200 calls — that is the "metal floor", raw pthreads with no pool,
and its `System` time (224 ms, the highest of the four) is where it shows.
Rayon's `join` submits to a work-stealing pool rather than spawning, but at
this granularity the submit-and-steal overhead still costs more than the fan-out
returns. Go's goroutines multiplex onto an existing M:N scheduler, which is why
it is the one hand-written mirror that keeps up.

**This lane is not comparable to the seq rows above.** Those are all
single-threaded; these are all using four cores.

#### What exactly got parallelised, and how to ask

Not a guess — `karac query concurrency` reports it. For `min_area`:

```json
"parallel_groups": [{"statements": [0,1,2,3],
                     "reason": "no data or effect dependencies"}]
```

Statements 0–3 are exactly `top`, `bottom`, `left`, `right`. They read the same
immutable image and write nothing, so the pass fans all four out, and the
binary carries four `__par_branch_0_0…_0_3` symbols the sequential build lacks.

> Worth recording because it cost an hour: an earlier draft of this section
> claimed the mechanism was *unattributed* and listed the four-searches
> explanation as DISPROVED. That was a bad experiment, not a finding. The test
> replaced two of the four searches with **constants**, which leaves `min_area`
> with four dependency-free statements either way — so the group stays four
> wide and the branch count cannot move. Cutting the *statement count* is the
> discriminating test. The real lesson is smaller and more useful: `karac query
> concurrency` answers this directly, and reaching for it first would have
> skipped six probes and one wrong conclusion.

### Every mirror hand-rolls the search, except Python's scale

C, Rust and Go all write the same plain index loops rather than reaching for
`sort.Search`, iterator `any()` chains, or equivalents — those would measure a
closure-per-probe indirection instead of the algorithm.

Python runs the same algorithm but at **120 queries against the compiled lanes'
1200**, because its row and column probes are per-pixel interpreter loops over
a 4096-wide frame, which is precisely what CPython is worst at. Its sink
therefore does not match the other four, by construction, and is comparable
only to itself.
