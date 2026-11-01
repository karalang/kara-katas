# 84. Largest Rectangle in Histogram

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Stack · Monotonic Stack · Divide and Conquer &nbsp;·&nbsp; **Source:** [leetcode.com/problems/largest-rectangle-in-histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)

Given an array of bar `heights` (each bar width 1), return the area of the **largest axis-aligned rectangle** that fits under the histogram. A rectangle spanning bars `[l, r]` has height `min(heights[l..r])` and width `r - l + 1`; the answer maximises `height · width` over all spans.

```
heights = [2,1,5,6,2,3]   ->   10   (bars 5,6 give 2·5 = 10)
heights = [2,4]           ->    4
```

**Constraints:** `1 ≤ heights.length ≤ 10⁵`; `0 ≤ heights[i] ≤ 10⁴`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Monotonic stack, fused pop-and-settle** ★ | [`largest_rectangle.kara`](largest_rectangle.kara) ✓ via `karac run` / `karac build` | [`largest_rectangle.py`](largest_rectangle.py) ✓ |
| **Two-pass nearest-smaller spans** | [`largest_rectangle_spans.kara`](largest_rectangle_spans.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other, with the Python mirror, **and with a brute-force O(n²) ground truth**. Both compile with **zero diagnostics**.

## Two monotonic-stack formulations

The key insight both share: bar `i`'s maximal rectangle is bounded on each side by the **nearest strictly-shorter bar** — it can extend left and right at its own height until it hits something shorter. The two solvers compute those boundaries differently.

**Fused pop-and-settle** ([`largest_rectangle.kara`](largest_rectangle.kara), the ★) keeps a stack of indices whose heights strictly increase. When the current bar is shorter than the stack top, that top bar can extend no further right, so it is popped and its rectangle settled immediately:

```
for i in 0..=n:                          # a virtual height-0 sentinel at i == n
    h = heights[i] if i < n else 0
    while stack and heights[stack.top] > h:
        top = stack.pop()
        width = i - stack.top - 1         # (or i, if the stack emptied)
        max_area = max(max_area, heights[top] * width)
    stack.push(i)
```

The popped bar's nearest-shorter-left is the new stack top and its nearest-shorter-right is the current bar `i`, so its width is `i - stack.top - 1`. Each index is pushed and popped once → **O(n)**. The height-0 sentinel at `i == n` flushes the still-increasing tail.

**Two-pass nearest-smaller spans** ([`largest_rectangle_spans.kara`](largest_rectangle_spans.kara)) precomputes the two boundaries explicitly instead of settling on the fly: one left-to-right stack sweep fills `nsl[i]` (nearest strictly-shorter bar to the left, or `-1`), one right-to-left sweep fills `nsr[i]` (to the right, or `n`), and then each area is `heights[i] · (nsr[i] - nsl[i] - 1)`. Popping with `>=` on **both** sides makes a run of equal bars attribute the full-width rectangle to a single representative, so no span is double-counted. It's the "compute the spans, then the areas" decomposition — a distinct surface with two stacks, an index-assigned `nsr` Vec, and a right-to-left `i64` loop walking down to `-1`.

## Kāra features exercised

- **`Vec[i64]` as a stack** — `push`/`pop` and `stack.len()` drive the monotonic stack; the ★ reads `stack[stack.len() - 1]` as the top and the spans variant runs two independent stacks.
- **Double-indexed array chase** — `heights[stack[stack.len() - 1]]` indexes the histogram *through* the stack, the inner-loop hot path of both solvers.
- **Index-assignment into a pre-filled Vec** — the spans variant fills `nsr` with the sentinel `n` then writes `nsr[r] = right` in the right-to-left pass (the same `Vec` index-assignment kata [#80](../80-remove-duplicates-from-sorted-array-ii/) uses).
- **Descending `i64` loop to `-1`** — `while r >= 0 { … r = r - 1 }` walks the right-to-left pass, with `heights[r]` read only while `r >= 0` (signed compare, no underflow read).
- **`if`-expression for the sentinel / width** — `let h = if i < n { heights[i] } else { 0 }` and the empty-stack width branch are value-position `if`s.

**v1 note.** Heights fit i64 and areas stay well within i64 (`≤ 10⁵ · 10⁴`); the per-case sink folds each area into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both agree with a brute-force O(n²) check on every case.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   largest_rectangle.kara
karac build largest_rectangle.kara && ./largest_rectangle

# The two-pass spans variant (identical output):
karac run largest_rectangle_spans.kara

# Python
python3 largest_rectangle.py

# Verify they all agree
diff <(karac run largest_rectangle.kara) <(python3 largest_rectangle.py)                    && echo OK
diff <(karac run largest_rectangle.kara) <(karac run largest_rectangle_spans.kara)          && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`largest_rectangle.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E = 18 logical cores; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23). The first M5 snapshot (2026-07-11, legacy backend) replaced an earlier x86-64 cloud-container one, and a 2026-07-28 re-measure (also legacy) had kāra leading both Rust builds single-threaded. **On MIR the seq lead is gone:** Kāra/Rust went 0.94× → 1.07× (Kāra/C 1.53× → 1.72×) — kāra now trails wrapping `rustc -O` by 1.07× and ties the overflow-checked twin (1.02×, inside σ). The MIR build runs **1.17× the October legacy build's instructions at 1.12× its cycles**, so this is a real codegen regression, not machine noise — borderline in size. The par-lane auto-par (zero parallel source) lands **1.22× behind hand-tuned rayon** (1.11× on 2026-07-28 — the seq gap carried into every worker) and **7.9× ahead of Go**, a 10.8× self-speedup on 18 cores. `bench/results.json` records the M5 host.

**Two lanes over one workload.** A batch of **K = 108,000 independent** largest-rectangle computations: each iteration builds a **fresh sawtooth histogram** whose phase depends on the iteration index — `heights[j] = (j + iter) % 50`, **N = 2000**, so no call hoists — runs `largest_rectangle` (the ★), and the K areas are combined through a plain **associative sum** (order-independent, so parallel and sequential produce the same total). The short sawtooth period means many pops per pass; the per-iteration build and per-call stack allocation are part of the measured work, alongside the double-indexed `heights[stack[..]]` chase. All nine seq + par mirrors must agree on `67500000` before timing.

- **Seq lane** — the batch run single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code**, raced against hand-tuned C-pthreads, rayon, and goroutines (kata [#75](../75-sort-colors/)'s framing). The default build emits a call of `karac_mir_task_spawn` and the `KARAC_AUTO_PAR=0` twin does not, verified in the emitted IR (`KARAC_MIR_LL`) on 2026-11-01.

**Equal data structure.** Every mirror uses **1D heap arrays** — kāra `Vec[i64]`, Rust `Vec<i64>`, C `malloc`'d `int64_t*`, Go `[]int64` — for both the histogram and the stack, so the comparison is codegen-vs-codegen.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So the seq lane includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`)

**M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time |
|---|---|
| c    largest_rectangle (clang -O3)                    | **281.4 ± 6.8 ms** |
| rust largest_rectangle (rustc -O)                     | 454.9 ± 5.5 ms |
| rust largest_rectangle (rustc -O, overflow-checks=on) | 476.7 ± 11.1 ms |
| **kāra largest_rectangle (`KARAC_AUTO_PAR=0`)**       | **484.9 ± 15.1 ms** |
| go   largest_rectangle                                | 522.2 ± 2.9 ms |

> **Update (2026-07-28) — Kāra now leads both Rust builds; the old text
> understated it.** Re-measured on the same M5 host:
>
> | Implementation | wall time | vs Kāra |
> |---|---|---|
> | c    largest_rectangle (clang -O3) | **239.1 ± 0.5 ms** | 0.65× |
> | **kāra largest_rectangle (`KARAC_AUTO_PAR=0`)** | **366.3 ± 5.4 ms** | **1.00×** |
> | rust largest_rectangle (rustc -O) | 389.2 ± 1.2 ms | 1.06× |
> | rust largest_rectangle (overflow-checks=on) | 406.1 ± 4.3 ms | 1.11× |
> | go   largest_rectangle | 425.4 ± 2.8 ms | 1.16× |
>
> The previous reading — "ties equal-safety Rust and slips just behind wrapping
> `rustc -O`" — is superseded in Kāra's favour: it is **1.11× ahead of the
> overflow-checked build and 1.06× ahead of wrapping `rustc -O`**. Kāra moved
> 409.7 → 366.3 ms (−11%) while the Rust rows moved little, so this is a
> Kāra-side gain rather than a comparator regression. C's lead narrowed from
> 1.69× to 1.53×.
>
> *Note (2026-11-01): this lead was a legacy-backend result and does not hold
> on MIR — see the table above.*

Single-threaded, kāra is **4th of five**: 1.07× behind wrapping `rustc -O` and 1.02× behind the `overflow-checks=on` twin (inside σ — the honest comparison since kāra checks by default, and a tie), 1.08× ahead of Go. The July-28 lead over both Rusts (legacy backend) is gone: the MIR build retires 1.17× the October legacy build's instructions at 1.12× its cycles. C's unchecked pointer stack remains the floor at 1.72× under kāra — mostly the *cost of safety* both kāra and Rust pay (overflow-checked Rust is itself 1.69× C), on this double-indexed `heights[stack[..]]` chase. Python is not in this run's feed.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`)

**M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time | Cores used |
|---|---|---|
| c    largest_rectangle (pthreads — metal floor)         | **25.3 ± 2.0 ms** | 12.7 |
| rust largest_rectangle (rayon `into_par_iter`)          | 36.8 ± 0.8 ms | 16.2 |
| **kāra largest_rectangle (auto-par, NO parallel code)** | **44.8 ± 1.3 ms** | 14.5 |
| go   largest_rectangle (goroutines + WaitGroup)         | 354.8 ± 9.3 ms | 5.2 |

The headline: **kāra's default build parallelises the batch with zero parallel source** — no threads, no rayon, no annotations, just `for k in 0..K { sum += … }` — and lands **1.22× behind hand-tuned rayon** (44.8 vs 36.8 ms; 1.11× on 2026-07-28, 1.14× on 2026-07-11 — the 1.07× seq gap is in every worker) and **7.9× ahead of the goroutine version** (354.8 ms — per-iteration allocation punishes Go's GC under parallelism; that gain is mostly Go-side, its row ran 1.71× slower than on 2026-07-28 against 1.08–1.22× for the others). The raw-pthreads floor is 1.77× ahead on the M5's 18 cores (1.83× on 2026-07-28). Against its own single-threaded seq lane (484.9 ms) that is a **10.8× self-speedup**, for free. See [`bench/results.json`](bench/results.json).

Compile-cold on the M5: clang 49.0 ms < rustc 92.8 ms < **karac 161.1 ms** (1.74× rustc, 3.29× clang). Binary size: c 32.7 KiB, **kāra 295.8 KiB** seq / 377.1 KiB par (the task runtime), rust 455.7 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS (seq): c 1.05 MiB, **kāra 1.14 MiB**, rust 1.16 MiB, go 9.47 MiB.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — single-threaded kāra now trails `rustc -O` by 1.07× on this stack-driven pass (2026-11-01; it edged ahead on the legacy backend), and in the par lane kāra's zero-code auto-par lands 1.22× behind hand-tuned rayon (`into_par_iter`). C calibrates the metal floor in both lanes, Go is the other native data point (its per-iteration slice churn shows in GC time, badly so under parallelism), Python (run at a fraction of the iteration count, timed separately; not in this run's feed) the ergonomic foil.
