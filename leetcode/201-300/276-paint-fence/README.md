# 276. Paint Fence

`n` posts, `k` colours. **No three consecutive posts may share a colour** — two
in a row is fine. Return how many ways the fence can be painted.

```
n=1 k=5  ->  5
n=2 k=2  ->  4        every two-post painting is legal
n=3 k=2  ->  6        the two all-same paintings are out
n=4 k=3  ->  66
n=10 k=3 ->  27408
n=20 k=2 ->  21892    at k=2 the sequence is Fibonacci doubled
```

**Constraints:** `1 ≤ n ≤ 50`, `1 ≤ k ≤ 10⁵`, and — the part LeetCode states and
this kata does not paper over — the testcases are chosen so the answer fits in 32
bits.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `paint_fence.kara` ★ | two rolling states, `same` and `diff` | O(n), O(1) space |
| `paint_fence_recurrence.kara` | the same recurrence with a variable eliminated | O(n), O(1) space |
| `paint_fence_brute.kara` | enumerate every painting, reject three-in-a-row | O(k·kⁿ) |
| `differential.kara` | 474 `(n, k)` pairs, 75 checked against the definition | — |
| `bench/paint_enum.kara` | the enumerator at n=13, k=4, split 16 ways | benchmark lane |

## One bit of history is enough

The rule looks at a window of three, but carrying the last two colours is
unnecessary — all that matters about the previous post is **whether it matched
the one before it**. That bit splits every valid painting into two classes:

```kara
same[i] = diff[i-1]                          // repeating is only legal after a change
diff[i] = (same[i-1] + diff[i-1]) * (k - 1)  // any painting, extended differently
```

and the three-in-a-row rule is never re-checked — it is enforced entirely by
`same[i] = diff[i-1]` refusing to chain.

**The base cases are where this goes wrong.** `same[2] = k` and
`diff[2] = k·(k−1)`, which sum to `k²`: every painting of two posts is legal,
because the rule needs three. A solver that starts the roll at 2, or seeds
`same[1] = k`, is right for `n = 1` and wrong from `n = 3` on.

## Eliminating the states moves the mistakes

Add the two classes together once and they disappear:

```
total[i] = diff[i-1] + total[i-1]·(k-1)
         = (total[i-1] + total[i-2])·(k-1)
```

A two-term linear recurrence — Fibonacci's shape, scaled by `k−1`. The second
solver is not a rewrite of the first; it is the first with a variable eliminated,
and **eliminating it moves where the mistakes live**. The ★ version can seed
`same` and `diff` wrongly while the loop is right; this one has no states to
seed but must get `total[2] = k²` — not `k·(k−1)` — and must start at 3. Two
different off-by-one surfaces, one answer.

## Which is exactly why the third solver is the definition

Both DP solvers are the same derivation at different stages. They share the
`total[2] = k²` fact and the "the rule needs three posts" reading, so a
misunderstanding of the **rule** — as opposed to an off-by-one in a loop — would
leave them agreeing confidently on a wrong count.

`paint_fence_brute.kara` walks all `kⁿ` assignments and rejects three-in-a-row.
Hopeless past a dozen posts, and that is fine: it is the problem statement,
compiled.

## What the injected bugs did

| injection | mismatches | brute-force disagreements |
|---|---:|---:|
| two-state: `same[i] = same[i-1]` (lets three chain) | 431 | 51 |
| recurrence: `total[2] = k(k−1)` instead of `k²` | 255 | 0 |
| two-state: swap the `same`/`diff` seeds | 139 | 42 |
| two-state: start the roll at 2 | *overflow trap* | — |
| recurrence: multiply by `k` instead of `k−1` | *overflow trap* | — |
| brute force: reject only **four** in a row | 0 | 52 |
| **both DP solvers misread the rule** | **0** | **63** |

The last row is the one this kata exists for. The two DP solvers agree
**perfectly** — cross-checking reports nothing — and the definition catches all
63. That is [#272](../272-closest-binary-search-tree-value-ii/)'s finding and
[#275](../275-h-index-ii/)'s in a third setting.

Row six is the same argument run backwards: break the *oracle* instead, and the
two DP solvers catch it. Neither side is privileged; they are independent.

**Two injections trap instead of answering**, which is worth its own note. Both
make the recurrence grow faster than the real one, so they leave `i64` inside an
envelope the generator computed for the *correct* recurrence — and Kāra's
default overflow checking turns what would be a silently wrapped wrong answer in
C or Rust into a located panic. A wrong algorithm caught by arithmetic rather
than by the oracle.

## The generator has to know where the arithmetic stops fitting

The answer grows like `(k−1)ⁿ`, so at `k = 100000` it leaves `i64` **before
n = 5**. Kāra traps; C and Rust wrap and print garbage without complaint.

So the harness computes its own envelope — `max_safe_n` walks the same recurrence
with a guard *before* each multiply, because checking afterwards is checking a
value that has already trapped — and draws every case inside it:

```
cases 474
of which checked against the DEFINITION (brute force) 75
largest n reached, all k (k=1 never grows, so it runs to the walk cap) 200
envelope at k=2 89, at k=100000 3
brute-force disagreements 0
digest 338090785
mismatches 0
```

`n = 89` at `k = 2` against `n = 3` at `k = 100000` is the whole story of this
problem's arithmetic in two numbers. LeetCode's `n ≤ 50` sits inside the envelope
for every `k` it allows, which is what its 32-bit promise is really saying.

The Python mirror cannot reproduce the envelope by overflowing — its integers are
arbitrary-precision — so it computes the same bound the same way, against the
same explicit limit. The envelope is arithmetic the harness performs, not a
property of the host's integer type, which is what lets the two agree exactly.

## Two compiler bugs this kata found

`B-2026-08-15-20` — **the interpreter blames an integer overflow on a
sub-expression that cannot overflow.** In `let c = (a + b) * m` with `a + b == 3`,
the trap is reported at the column of `a`; the compiled backends point elsewhere
on the same line. The message text is right everywhere and all four surfaces exit
1 — but `karac run` and `karac build` give two different answers to *where*, and
the interpreter's is provably not the culprit. Filed low: no wrong answer, and
the fault is detected. It still costs the first thing anyone does with a panic.

`B-2026-08-15-23` — **fixed** — *a `#[par_order_free]` collect-tabulate loop
dispatched four workers and gave all the work to one.* Found by this kata's par
lane measuring 1.02× against its own sequential twin, at 100% CPU, while
`karac query concurrency` reported `fanned_out: true`.

The report was telling the truth: the fan-out did happen. The order-free dynamic
chunker sized chunks `.max(MIN_DYNAMIC_CHUNK.min(iter_total))`, which for any
range under 1024 is `iter_total` itself — one chunk, one worker running the whole
loop, three exiting immediately. This kata's loop has **16** iterations.

My filed diagnosis ("the tabulate lowering does not dispatch", "`fanned_out` is
computed from classification") was wrong on both counts, and refuted by
instrumenting the dispatch. The six-shape table that found it was right; the
causal reading of it was not. `order_free` is set only by the tabulate lowering,
so the conditional-vs-unconditional split I measured was a *marker* for "took the
dynamic path", never the cause.

## Kāra features exercised

- **`Vec[Vec[i64]]` literals** as a case table, indexed twice (`cases[i][0i64]`).
- **Default integer-overflow checking**, as a load-bearing part of the kata
  rather than a footnote — see the two trapping injections.
- **A `while` odometer with carry** over base-`k` digits — the brute-force
  enumerator, mutating its array in place.
- **`i64` bounds arithmetic** — `9223372036854775807i64` as a literal, and
  division-before-multiply guards.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

## Running

```bash
karac run paint_fence.kara
karac run paint_fence_recurrence.kara
karac run paint_fence_brute.kara

diff <(karac run paint_fence.kara) <(python3 paint_fence.py) && echo OK

# 474 (n, k) pairs, 75 of them against brute-force enumeration
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in paint_fence paint_fence_recurrence paint_fence_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

## Benchmarks

The **DP is not the workload.** It is O(n) and `n` cannot exceed 89 before the
answer leaves `i64` — ninety iterations of four arithmetic ops. Benching it would
have meant inventing a modular variant, which is a different problem wearing this
kata's name.

The **enumerator** is a real one: `n = 13, k = 4` is 67 million paintings and
~800 million comparisons, branch-heavy and entirely data-dependent. And the sink
is the answer, so the bench verifies itself — every lane must print
`num_ways(13, 4) = 36884484`. A lane that optimized away half the search would
say so immediately.

4-core x86 container, hyperfine. Full caveats in
[BENCHMARKS.md](../../../BENCHMARKS.md).

### SEQ lane — single-threaded against single-threaded

| lane | time | vs C |
|---|---:|---:|
| `clang -O3 -march=x86-64-v3` | 360.7 ms ± 6.4 | 0.97× |
| `clang -O3` | 373.2 ms ± 13.0 | 1.00× |
| `rustc -O` | 391.2 ms ± 9.0 | 1.05× |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **409.0 ms ± 11.6** | **1.10×** |
| **`karac build`, `KARAC_AUTO_PAR=0`** | **474.8 ms ± 14.0** | **1.27×** |
| `go build` | 1043 ms ± 9 | 2.79× |

Against the equal-safety comparator — Rust with overflow checks on, matching
Kāra's default-checked arithmetic — Kāra is **1.16×**. Against Go, 2.2× faster.

### PAR lane — against mirrors that also reached for threads

The enumeration splits on the first two posts into 16 wholly independent
branches. Kāra opts in with one attribute; the mirrors are hand-threaded.

| lane | time | vs pthreads |
|---|---:|---:|
| `clang -O3` + pthreads (metal floor) | 115.7 ms ± 6.3 | 1.00× |
| **`karac build`, `#[par_order_free]`** | **124.8 ms ± 8.0** | **1.08×** |
| Go, goroutines + `WaitGroup` | 277.6 ms ± 6.7 | 2.40× |

**Within 8% of hand-written pthreads C, from a one-line attribute** — and 3.8×
its own sequential twin on 4 cores. The Kāra source is the sequential program
plus `#[par_order_free]`; the C mirror needs an explicit thread pool, a per-thread
argument struct, and a join loop.

These two tables are kept apart deliberately. A parallel Kāra number beside a
sequential C number would measure whether the comparator's author reached for
threads, not the compiler — see [#270](../270-closest-binary-search-tree-value/)'s
lane note.

### What this lane cost before it worked

The par lane originally measured **1.02×** — no speedup at all — which is how
`B-2026-08-15-23` was found. The fix (a one-line cap on the chunker's floor,
`c04bc65`) took it from 1.02× to 3.8× against the sequential twin with no source
change to the kata.

`bench/probe/paint_enum_guarded.kara` is what sized the gap at the time: the
identical push wrapped in an always-true guard, which fell out of the tabulate
shape and onto the working static-split path. It is kept as a **regression
witness** — it should now measure at or slightly *behind* the natural shape
(137.9 ms vs 121.1 ms when re-measured after the fix), and if it ever pulls
materially ahead again, the chunker floor has regressed.

The shipped lane was published at 1.02× for as long as that was the true number.
Adopting the guard to manufacture a good row would have routed around the
compiler gap instead of reporting it — and the row is what got it fixed.
