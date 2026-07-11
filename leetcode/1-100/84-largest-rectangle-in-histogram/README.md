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

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E = 18 logical cores; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. The seq lane tightens — kāra **ties equal-safety Rust** and slips just behind wrapping `rustc -O`; the par-lane auto-par (zero parallel source) lands **within 1.14× of hand-tuned rayon** and 5.3× ahead of Go, a 10.2× self-speedup on 18 cores. `bench/results.json` records the M5 host.

**Two lanes over one workload.** A batch of **K = 108,000 independent** largest-rectangle computations: each iteration builds a **fresh sawtooth histogram** whose phase depends on the iteration index — `heights[j] = (j + iter) % 50`, **N = 2000**, so no call hoists — runs `largest_rectangle` (the ★), and the K areas are combined through a plain **associative sum** (order-independent, so parallel and sequential produce the same total). The short sawtooth period means many pops per pass; the per-iteration build and per-call stack allocation are part of the measured work, alongside the double-indexed `heights[stack[..]]` chase. All nine seq + par mirrors must agree on `67500000` before timing.

- **Seq lane** — the batch run single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code**, raced against hand-tuned C-pthreads, rayon, and goroutines (kata [#75](../75-sort-colors/)'s framing).

**Equal data structure.** Every mirror uses **1D heap arrays** — kāra `Vec[i64]`, Rust `Vec<i64>`, C `malloc`'d `int64_t*`, Go `[]int64` — for both the histogram and the stack, so the comparison is codegen-vs-codegen.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So the seq lane includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`)

| Implementation | Wall time |
|---|---|
| c    largest_rectangle (clang -O3)                    | **243.0 ± 4.0 ms** |
| rust largest_rectangle (rustc -O)                     | 392.2 ± 6.0 ms |
| **kāra largest_rectangle (`KARAC_AUTO_PAR=0`)**       | **409.7 ± 6.0 ms** |
| rust largest_rectangle (rustc -O, overflow-checks=on) | 412.9 ± 6.0 ms |
| go   largest_rectangle                                | 430.9 ± 8.0 ms |

Single-threaded, kāra **ties equal-safety Rust** (409.7 vs `overflow-checks=on` 412.9 ms — within noise) and slips just behind wrapping `rustc -O` (392.2, 1.04×). C's unchecked pointer stack is the floor at 1.69× under kāra — but that is the *cost of safety* both kāra and Rust pay (overflow-checked Rust is itself 1.70× C), on this double-indexed `heights[stack[..]]` chase. Go trails at 430.9 ms. Python is timed separately.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`)

| Implementation | Wall time | Cores used |
|---|---|---|
| c    largest_rectangle (pthreads — metal floor)         | **22.0 ± 1.0 ms** | 14.4 |
| rust largest_rectangle (rayon `into_par_iter`)          | 35.3 ± 2.0 ms | 16.6 |
| **kāra largest_rectangle (auto-par, NO parallel code)** | **40.2 ± 3.0 ms** | 15.4 |
| go   largest_rectangle (goroutines + WaitGroup)         | 212.2 ± 6.0 ms | 5.6 |

The headline: **kāra's default build parallelises the batch with zero parallel source** — no threads, no rayon, no annotations, just `for k in 0..K { sum += … }` — and lands **within 1.14× of hand-tuned rayon** (40.2 vs 35.3 ms) and **5.3× ahead of the goroutine version** (212.2 ms — per-iteration allocation punishes Go's GC under parallelism). The raw-pthreads floor pulls further ahead on the M5's 18 cores (22.0 ms, 1.83×) than on the 4-vCPU container. Against its own single-threaded seq lane (409.7 ms) that is a **10.2× self-speedup**, for free. See [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — single-threaded kāra edges ahead of `rustc -O` on this stack-driven pass, and in the par lane kāra's zero-code auto-par matches hand-tuned rayon (`into_par_iter`). C calibrates the metal floor in both lanes, Go is the other native data point (its per-iteration slice churn shows in GC time, badly so under parallelism), Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
