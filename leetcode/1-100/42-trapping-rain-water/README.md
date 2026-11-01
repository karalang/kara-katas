# 42. Trapping Rain Water

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/trapping-rain-water](https://leetcode.com/problems/trapping-rain-water/)

Given `n` non-negative bar heights, each of unit width, return the total water trapped between
them after rain.

```
[0,1,0,2,1,0,1,3,2,1,2,1]  →  6
[4,2,0,3,2,5]              →  9
```

**Constraints:** `n == height.length`, `1 ≤ n ≤ 2·10⁴`, `0 ≤ height[i] ≤ 10⁵`. The water
standing over column `i` is `min(maxLeft[i], maxRight[i]) - height[i]` (clamped at 0): a
column holds water up to the shorter of the tallest wall to its left and the tallest to its
right. Sum that over every column. Heights and widths are small enough that the total stays
far inside `i64`.

## Why this kata — one invariant, three ways to spend space

The water over a column is fixed by the same quantity in every solution —
`min(left_max, right_max) - height` — and the three canonical solvers are exactly three
*space/structure* factorings of how you get `left_max` and `right_max` to each column. That
makes #42 the natural Hard companion to [#11](../11-container-with-most-water/) (Container With
Most Water): both are converging-two-pointer problems, but #11's two pointers chase a single
*global* maximum while #42's accumulate a *running* one and settle each column on the way past.
It is also the in-place sibling of [#41](../41-first-missing-positive/) — an
allocation-free O(1)-space scan over a `mut`/borrowed array — extended with two O(n)-space
contrasts that exercise `Vec` differently.

| Lens | Idea |
|---|---|
| **Two pointers** ★ | advance the shorter outer wall; that side's running max is the binding constraint (the far side is provably taller), so the column settles with one scalar — O(1) space |
| **Prefix/suffix maxima** | materialize `left_max[i]` and `right_max[i]` as arrays, then sum `min(left_max, right_max) - height` — the formula made literal, O(n) space |
| **Monotonic stack** | keep a stack of indices with non-increasing heights; a taller incoming bar closes a basin, and water is added as the rectangular slab between the two walls — O(n) space |

The two-pointer file removes the arrays entirely by noticing you never need the *exact*
far-side maximum, only that it is at least as tall as the near side — which the
"advance the shorter wall" rule guarantees. The array file is the version that makes the
invariant obvious. The stack fills water in horizontal slabs rather than columns, settling each
basin the moment its bounding right wall appears.

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Two pointers** ★ | [`trapping_rain_water.kara`](trapping_rain_water.kara) | `Slice[i64]`, two converging indices + two running-max scalars, one linear pass, no allocation |
| Prefix/suffix maxima | [`trapping_rain_water_arrays.kara`](trapping_rain_water_arrays.kara) | two `Vec[i64]` of length n (forward + backward scans), then sum `min(L,R) - h` |
| Monotonic stack | [`trapping_rain_water_stack.kara`](trapping_rain_water_stack.kara) | `Vec[i64]` driven as a stack — `push`/`pop`/`is_empty` + top-peek via `stack[stack.len()-1]` |

The two-pointer form is allocation-free (a read-only `Slice[i64]` view + scalars); the array
form allocates two `Vec[i64]` and indexes them; the stack form allocates one `Vec[i64]` and
drives it with stack operations. Each bar is pushed and popped at most once in the stack
solver, so all three are O(n) time.

## What this kata surfaced

**No compiler change was needed — all three solvers typechecked, ran, and built correctly on
the first pass.** What the kata surfaced is on the *codegen-quality* side, in the benchmark: the
converging two-pointer's lone data-dependent branch (`height[left] < height[right]`) is a
clean case where **the mainstream `-O` backends pessimize and Kāra does not.**

`clang -O3` and `rustc -O` both lower that branch **branchlessly**, as a `csel` chain (9 `csel`
in each `trap` lowering). On a converging-pointer loop that is the wrong call: the `csel`
makes each iteration's `left`/`right` update *data-depend* on the previous one, so the loop
becomes **latency-bound on its own carried dependency** — ~341 ms (C) / ~353 ms (Rust),
**terrain-independent** (a scrambled, genuinely-unpredictable height profile measures the same,
because there is no branch left to mispredict). Kāra and the safety-matched
`rustc -C overflow-checks=on` keep the comparison as a **predicted branch**, which the Apple M5
predictor pipelines, letting independent iterations overlap — ~112–120 ms, **~3× faster**. The
two land in a dead heat (Kāra 119.9 ms vs checked Rust 112.4 ms, within 7%), so this is a
*codegen choice on this loop shape*, not a Kāra-specific trick: when Rust is compiled to the
same branchy code, it ties Kāra. (Those figures are the legacy snapshot. On the 31 Oct 2026 v2/MIR re-bench the two are 1.12× apart on means and within 4% on medians, see § Benchmarks; the shape of the argument stands.)

The honest reading is the corpus's usual one — **the apples-to-apples (equal-safety) comparator
ties Kāra** — with the added note that `clang`/`rustc -O`'s `csel` transform happens to be a
latency-bound de-optimization for the converging-pointer kernel on Apple Silicon. The kata ships
the idiomatic two-pointer in every language (no hand-tuning to force or forbid `csel`); the
gap is what the stock toolchains emit.

## Benchmarks

Workload: a jagged length-`N=1000` terrain (`(i*37)%100`) is built **once**, then **`TOTAL =
200000`** times a single slot is punched (`height[k%n] = (k*19)%100`, an O(1) tweak that shifts
the basins so the answer changes with `k`), the ★ two-pointer solve runs, and each answer is
folded into a rolling checksum (sink `111821755`). The per-iteration cost is therefore the
**non-vectorizable converging scan itself**, not an O(n) refill loop whose vectorization would
diverge across compilers and drown out the algorithm. The terrain is built once and only one
slot changes per iteration — the hot loop **allocates nothing** — so this is allocation-free
integer compute, the in-place-scan counterpart to [#41](../41-first-missing-positive/). The
punch location and the checksum carry a loop-borne dependency (no hoisting), so it is a
single-lane (seq) bench by construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).
Measured 2026-10-31 (`measured_at` 2026-11-01T02:04Z) with karac `g6697158fa` (v2/MIR
backend).

### Seq lane — runtime (single-threaded converging two-pointer)

| | Rust (`overflow-checks=on`) | Go | **Kāra** | C | Rust (`-O`) | Python |
|---|---|---|---|---|---|---|
| time | 120.6 ± 5.4 ms | 124.0 ± 4.1 ms | **135.4 ± 18.7 ms** | 375.6 ± 7.7 ms | 387.5 ± 6.5 ms | 5358 ms (last measured 2026-06-19, not re-run) |
| vs Kāra | 1.12× faster (= safety) | 1.09× faster | — | 2.77× slower | 2.86× slower | 44.7× slower (2026-06-19 ratio) |

**Kāra sits with the equal-safety comparator and Go, and is ~2.8× ahead of stock C and Rust —
because of the `csel` story above, not raw throughput.** This is the rare kata where reading
the *shape* matters more than usual. Against the previous (2026-06-19, legacy-backend) run the
picture is flat: Kāra/Rust 0.34× → 0.35×, Kāra/C 0.35× → 0.36×, Kāra/Go 1.06× → 1.09×.

- **Equal safety is a near-tie.** Kāra checks arithmetic by default; the apples-to-apples
  comparator is `rustc -C overflow-checks=on` (120.6 ms), 1.12× ahead of Kāra's mean
  (135.4 ms). Kāra's mean carries a wide ±18.7 ms σ from a few slow runs (max 166.8 ms); on
  medians the two are 123.8 vs 119.2 ms, within 4%. Go (124.0 ms) sits with them. All three
  keep the converging-pointer comparison as a predicted branch.
- **Don't over-read the ~2.8× over C/Rust.** `clang -O3` (375.6 ms) and `rustc -O` (387.5 ms) emit
  a branchless `csel` chain that serializes the loop-carried `left`/`right` update — a
  latency-bound de-optimization for *this* kernel on Apple Silicon (confirmed terrain-
  independent; see § What this kata surfaced). It is a real, reproducible gap, but it is a stock-
  toolchain codegen choice, not evidence Kāra's compute is ~3× faster in general. The honest
  headline is the equal-safety near-tie.
- **Python** runs the identical algorithm interpreted: 44.7× slower (2026-06-19 run, not re-run).

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.03 MiB | 1.06 MiB | **1.02 MiB** | 2.64 MiB |
| binary size (seq) | 295.8 KiB | 455.4 KiB | **32.7 KiB** | 2434.1 KiB |
| compile elapsed | 113.0 ms | 84.5 ms | **46.6 ms** |
| compile peak RSS | 57.6 MiB | 27.6 MiB | **2.6 MiB** |

A single 1000-element buffer means runtime RSS is tiny and allocator-bound: C peaks at
**1.02 MiB** (1 065 272 bytes), Kāra at 1.03 MiB (1 081 680 bytes, 16 KiB over C) and Rust at
1.06 MiB, while Go's runtime pays 2.64 MiB and Python's interpreter 6.8 MiB (last measured
2026-06-19, not re-run). The Kāra binary is **295.8 KiB** — 1.5× under Rust's 455.4 KiB but 9×
C's 32.7 KiB; every MIR-backend Kāra binary is ~300–390 KB where the legacy backend's were
~34 KB (tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Compile now favours
`rustc -O` over `karac` on both elapsed (84.5 vs 113.0 ms) and peak compiler RSS (27.6 vs
57.6 MiB); clang's 46.6 ms / 2.6 MiB is the floor.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par pass does not fire: neither the default
nor the `KARAC_AUTO_PAR=0` build's emitted IR (`KARAC_MIR_LL`) contains a call of
`karac_mir_task_spawn`, and the two binaries are **byte-identical** (re-checked with karac
`g6697158fa`); both run single-threaded.

## Kāra features exercised

- **Read-only `Slice[i64]` view** — the ★ two-pointer solver takes the input as a bare
  `Slice[i64]` (the idiomatic borrowed view) since it never writes, walking two converging
  indices with two running-max scalars and no allocation, the in-place-scan footing of
  [#41](../41-first-missing-positive/).
- **`Vec[i64]` index arrays** — the prefix/suffix solver allocates two `Vec[i64]` of length n,
  fills them with forward/backward scans, and reads them back by computed index, the allocating
  contrast to the scalar two-pointer.
- **`Vec[i64]` as a stack** — the monotonic-stack solver drives one `Vec[i64]` with `push`,
  `pop`, `is_empty`, and top-peek (`stack[stack.len()-1]`), plus `break` out of the inner
  basin-closing loop.
- **Checked integer arithmetic that ties C-class** — index math, the running-max compares, the
  width × depth slab products, and the checksum fold all run under Kāra's default overflow
  checking, within 1.12× of `rustc -C overflow-checks=on` (4% on medians) — and the predicted-branch
  lowering avoids the `csel` latency trap the stock `-O` backends fall into here.
- **Three factorings of one O(n) idea** — two-pointer, prefix/suffix maxima, and a monotonic
  stack, all agreeing across the LeetCode examples under both `karac run` and `karac build`.

---

**Bug ledger:** none — no compiler change was required for this kata (all three solvers
typechecked, ran, and built correctly on the first pass). The finding is a codegen
*characterization*: `clang -O3` / `rustc -O` lower the converging-pointer branch as a
latency-bound `csel` chain, while Kāra and safety-matched Rust keep the predicted branch and run
~3× faster (§ What this kata surfaced). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the cross-kata history.
