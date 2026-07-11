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

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Two lanes over one workload.** A batch of **K = 108,000 independent** largest-rectangle computations: each iteration builds a **fresh sawtooth histogram** whose phase depends on the iteration index — `heights[j] = (j + iter) % 50`, **N = 2000**, so no call hoists — runs `largest_rectangle` (the ★), and the K areas are combined through a plain **associative sum** (order-independent, so parallel and sequential produce the same total). The short sawtooth period means many pops per pass; the per-iteration build and per-call stack allocation are part of the measured work, alongside the double-indexed `heights[stack[..]]` chase. All nine seq + par mirrors must agree on `67500000` before timing.

- **Seq lane** — the batch run single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code**, raced against hand-tuned C-pthreads, rayon, and goroutines (kata [#75](../75-sort-colors/)'s framing).

**Equal data structure.** Every mirror uses **1D heap arrays** — kāra `Vec[i64]`, Rust `Vec<i64>`, C `malloc`'d `int64_t*`, Go `[]int64` — for both the histogram and the stack, so the comparison is codegen-vs-codegen.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So the seq lane includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`)

| Implementation | Wall time |
|---|---|
| c    largest_rectangle (clang -O3)                    | 539.6 ± 20.7 ms |
| **kāra largest_rectangle (`KARAC_AUTO_PAR=0`)**       | **823.2 ± 17.5 ms** |
| rust largest_rectangle (rustc -O)                     | 885.9 ± 34.8 ms |
| rust largest_rectangle (rustc -O, overflow-checks=on) | 895.3 ± 23.8 ms |
| go   largest_rectangle                                | 1677.7 ± 64.6 ms |

Single-threaded, kāra is **ahead of both Rust builds** (823.2 vs 885.9 / 895.3 ms) — and the equal-safety comparison (`overflow-checks=on`, 895.3) is the widest gap in kāra's favour. C's unchecked pointer stack is the floor at ~1.53× under kāra; Go trails ~2× (per-iteration slice churn on the GC). Python at K=4000 is ~2.0 s, timed separately.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`)

| Implementation | Wall time |
|---|---|
| c    largest_rectangle (pthreads — metal floor)         | 166.3 ± 23.5 ms |
| rust largest_rectangle (rayon `into_par_iter`)          | 235.1 ± 6.9 ms |
| **kāra largest_rectangle (auto-par, NO parallel code)** | **244.7 ± 16.2 ms** |
| go   largest_rectangle (goroutines + WaitGroup)         | 928.6 ± 24.1 ms |

The headline: **kāra's default build parallelises the batch with zero parallel source** — no threads, no rayon, no annotations, just `for k in 0..K { sum += … }` — and lands **within ~4% of hand-tuned rayon** (244.7 vs 235.1 ms), a step behind the raw-pthreads floor (~1.47×), and **3.8× ahead of the goroutine version** (928.6 ms — its per-iteration slice allocation punishes Go's GC hard under parallelism). Against its own single-threaded seq lane (823.2 ms) that is a **3.36× self-speedup** on 4 vCPU, for free. Records in [`results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — single-threaded kāra edges ahead of `rustc -O` on this stack-driven pass, and in the par lane kāra's zero-code auto-par matches hand-tuned rayon (`into_par_iter`). C calibrates the metal floor in both lanes, Go is the other native data point (its per-iteration slice churn shows in GC time, badly so under parallelism), Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
