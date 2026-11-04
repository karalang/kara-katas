# 1665. Minimum Initial Energy to Finish Tasks

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array, Greedy, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-initial-energy-to-finish-tasks](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/)

You are given a list of tasks where `tasks[i] = (actual_i, minimum_i)`:

- `actual_i` is the energy spent finishing the i-th task.
- `minimum_i` is the energy required to *start* the i-th task (≥ `actual_i`).

You may finish the tasks in any order. Return the minimum initial energy needed to finish them all.

**Constraints:** `1 ≤ tasks.length ≤ 10⁵`, `1 ≤ actual_i ≤ minimum_i ≤ 10⁴`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sort by `minimum - actual` descending, then one-pass running max | O(n log n) time, O(n) space | [`greedy.kara`](greedy.kara) ✓ via `karac run` | [`greedy.py`](greedy.py) ✓ |

`✓` runs end-to-end today.

### Why sort by `minimum - actual` descending?

Let `E` be the chosen initial energy and let `S_k = sum_{i<k} actual_i` be the energy spent strictly before task k in the chosen order. The constraint at task k is `E - S_k ≥ minimum_k`, i.e. `E ≥ S_k + minimum_k`. So:

$$E^* = \max_k (S_k + minimum_k)$$

Exchange argument over an adjacent pair `(i, j)`: swapping them changes only the two terms involving them. With prefix `P = S_k` at the start of the pair, the relevant terms are

- order `i, j`: `max(P + minimum_i, P + actual_i + minimum_j)`
- order `j, i`: `max(P + minimum_j, P + actual_j + minimum_i)`

The cross-terms dominate (since `actual + minimum > minimum`), so order `i, j` wins iff `actual_i + minimum_j ≤ actual_j + minimum_i`, i.e. `minimum_j - actual_j ≤ minimum_i - actual_i`. So put the task with the larger `minimum - actual` *first* — it needs the largest "buffer" beyond its own cost, and that buffer is cheapest to provide when no other task has eaten into the reserve yet.

## Kāra features exercised

- **Tuple element type** — `Slice[(i64, i64)]` parameter, `Array[(i64, i64), N]` literal, coercion between the two.
- **Tuple field access inside a closure** — `(b.1 - b.0).cmp(a.1 - a.0)` as the `Vec.sort_by` comparator.
- **Tuple destructuring** — `let (actual, minimum) = t;` inside the running-max loop.
- **`Vec[T]` with closure-taking sort** — `ordered.sort_by(|a, b| ...)` mutates in place.

No `Map`, no strings, no shared structs.

## Running

```bash
# Kāra
karac run greedy.kara

# Python (3.10+ for PEP 604 union syntax)
python3 greedy.py
```

## Benchmarks
### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go mirror with `go build`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then measures runtime (`hyperfine --warmup 5 --runs 30` on `N = 50_000` deterministic `(actual, minimum)` tasks, `K = 5` outer iterations so algorithm time dominates per-process startup), cold-compile time and memory (via a `--prepare` delete step), binary size, and peak RSS.

| File | What it does |
|---|---|
| [`bench/greedy.kara`](bench/greedy.kara) | N=50_000 deterministic generator, K=5 outer iterations, sort-by-`(minimum - actual)`-descending via `Vec.sort_by` with an inline closure comparator |
| [`bench/greedy.py`](bench/greedy.py) | Algorithmic mirror — same N, K, generator |
| [`bench/greedy.rs`](bench/greedy.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/greedy.c`](bench/greedy.c) / [`bench/go-seq/`](bench/go-seq/) | Algorithmic mirrors; `clang -O3` (`qsort`) / `go build` (`sort.Slice`) |

All mirrors print the same sum-of-results sink so the algorithm's output participates in I/O and can't be elided; bench.sh fails loudly on mismatch.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-11-04, karac gd33cb285d (the v2/MIR backend), sequential lane (`KARAC_AUTO_PAR=0`), hyperfine `--warmup 5 --runs 30 --shell=none`:

| Workload | Kāra (codegen) | Rust | Rust (checked) | C (clang -O3) | Go | Kāra : Rust |
|---|---|---|---|---|---|---|
| `greedy` | 3.13 ± 0.14 ms | 2.45 ± 0.04 ms | 2.49 ± 0.05 ms | 2.87 ± 0.08 ms | 9.60 ± 0.22 ms | **1.28× of Rust** |

Kāra reads 1.28× `rustc -O`, 1.26× equal-safety Rust, 1.09× C and 0.33× Go, against 2.83×, 2.36× C and 0.77× Go on the 2026-06-16 feed. This is a 3 ms kernel. Against legacy dd86e3955 (`KARAC_AUTO_PAR=0`) it runs 1.20× the instructions and 1.16× the cycles; see [`B-2026-11-04-33`](#bug-ledger).

(The 2026-05-29 snapshot read kāra 3.4 ± 0.2 / rust 3.0 ± 0.3 — both moved down together within ~1σ, batch movement; C and Go rows are benched here for the first time.)

**This gap is not an overflow-comparison artifact.** Kāra checks integer overflow by default; `rustc -O` silently wraps. Elsewhere in the corpus that asymmetry can flatter Kāra's ratio against wrapping Rust, so the harness also benches an equal-safety Rust lane (`rustc -O -C overflow-checks=on`, the "Rust (checked)" column). Here it reads **2.49 ms — statistically indistinguishable from wrapping Rust's 2.45 ms**, inside σ. Overflow checking costs nothing measurable on this workload, so it explains none of the gap. The 2.71× gap of the 2026-06-05 snapshot was the lean-sort runtime tradeoff (`B-2026-06-13-2`).

This kata is **sort-dominated** — a sort over 50,000 `(i64, i64)` pairs is ~850k comparisons per call × K=5 ≈ 4M comparator invocations. **On the v2/MIR backend the FFI hop is gone:** the emitted IR defines the merge and partition sort bodies for this closure in the module (`merge_sort.by.closure…`, `part_sort.by.closure…`) and has no call to `karac_vec_sort_by`. On the legacy backend, `karac_vec_sort_by` lived in a precompiled runtime crate and called the user comparator via an `extern "C" fn` pointer that LLVM in the runtime crate saw as opaque and could not inline through. The 2026-05-12 → 2026-05-25 gap-tightening from 1.37× → 1.19× tracked the cumulative effect of cross-archive LTO + DCE, the `__TEXT,__jittmpl` segment re-scope (`e76f42b`), and platform shift from M1 → M5 Pro.

The comparator rows: `qsort` (C, 2.87 ms) still carries the cannot-inline-the-comparator handicap, on top of its element-swap-by-`memcpy` generality, and Kāra now sits just behind it at 1.09×, where the 2026-06-05 snapshot read 2.24×. Rust's monomorphized `sort_by` leads everyone. Go's `sort.Slice` trails Rust 3.91× — interface-based comparator dispatch plus bounds checks in the swap path.

**Slice 6.1 + 6.4 (Vec[T].sort_by monomorphization) shipped 2026-05-29.** The original deferred-entry promotion gate ("≥2 distinct non-synthetic workloads show >1.3× perf gap") fired via katas [#16 (3Sum Closest)](../../1-100/16-3sum-closest/) at 1.55× and [#56 (Merge Intervals)](../../1-100/56-merge-intervals/) at 1.50×; karac shipped per-call-site `__vec_<elem>_sort_by_mono_<id>` insertion-sort bodies with the comparator inlined, plus a runtime length dispatch `if len > 64 { runtime } else { mono }`. **This kata routes to the runtime path at N=50000** because insertion sort's O(N²) loses hard above the threshold; the runtime length check at the call site picks the safe path per call. The pre-Slice-6.4 codegen behavior (FFI hop through `karac_vec_sort_by`) is preserved unchanged for kata 1665's workload; the kāra-vs-rust gap widened with the lean-sort tradeoff (3.4 vs 3.0 then, 7.6 vs 2.8 on 2026-06-05). Kata 16 / 56's much smaller N=16 workloads benefit from the mono path; kata 1665's N=50000 workload would have *regressed* under a pure-mono dispatch (a strawman first attempt during the Slice 6.4 work showed 3.2 ms → 1.1 s before the length dispatch was added), so the safe runtime fallback is the load-bearing piece here. Cross-ref: [`phase-7-codegen.md` Slice 6 trigger entry](https://github.com/karalang/kara/blob/main/docs/implementation_checklist/phase-7-codegen.md).

*2026-11-04: that dispatch describes the legacy backend. The v2/MIR backend emits the sort in the module at this N, as above.*

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara greedy` (codegen) | 3.13 ± 0.14 ms |
| `rust greedy` | 2.45 ± 0.04 ms |
| `py greedy` | 35.65 ± 0.21 ms *(last measured 2026-06-16, not re-run)* |

Python's last reading is **~11× slower** than Kāra codegen, across sessions since it was not re-run — the algorithm-dominated regime at N=50k where compiled-with-codegen languages put a lap on CPython. (CPython's `list.sort` with a key tuple is actually a *good* showing — Timsort's C core keeps the multiplier an order of magnitude below the pure-bytecode katas' ~35–540×.)

### Compile time and binary size

Snapshot — M5 Pro, 2026-11-04, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size | Compile memory |
|---|---|---|---|
| `karac build greedy.kara` | 130.0 ± 12.2 ms | 66.9 KiB | 60.0 MiB |
| `rustc -O greedy.rs` | 116.0 ± 2.3 ms | 472.1 KiB | 38.0 MiB |
| `clang -O3 greedy.c` | 43.5 ± 1.5 ms | 32.9 KiB | 2.6 MiB |

`karac build` takes 1.12× `rustc -O`'s time at 1.58× its peak memory, and produces a binary ~86% smaller (66.9 KiB vs Rust's 472.1).

> **Binary-size note.** Kāra's seq binary is 68,504 B on the v2/MIR backend, and the default auto-par binary is 402,824 B. The legacy backend's 33.5 KiB (2026-06-05) sat in the same tier as C's 32.9 KiB; `B-2026-10-28-36` (fixed) brought the v2/MIR seq binaries down from ~300–390 KB. Go's binary (not in the cold-compile table — `go build` caching isn't comparable) weighs 2452.1 KiB, ~18 KiB above its usual 2434.2 corpus floor for the `sort` package.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `c    greedy` | 1.8 MiB |
| `rust greedy` | 3.4 MiB |
| `kara greedy` (codegen) | 3.4 MiB |
| `go   greedy` | 7.2 MiB |
| `py   greedy` | 11.6 MiB *(last measured 2026-06-16, not re-run)* |

Single-shot readings. The N=50,000 `(i64, i64)` working set is ~800 KiB ×2 (input + sorted copy); C's 1.8 MiB is that plus process baseline. Kāra sits at parity with Rust (3.4 MiB). Go's 7.2 MiB is GC arena + runtime; Python's 11.6 MiB is the interpreter baseline.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor here, and on this kata it also calibrates the *comparator-indirection penalty* — `qsort`'s function-pointer dispatch carries a cannot-inline handicap, yet still lands 1.09× ahead of kāra, with Rust's inlined `sort_by` the floor-setter. Go is the cross-runtime data point; Python is the ergonomic foil.

---

**Bug ledger:** this kata surfaced `B-2026-06-13-2` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).

## Bug ledger

**Surfaced [`B-2026-11-04-33`](../../../../kara/docs/bugs-v2.md)** (perf, low, open). On gd33cb285d (measured 2026-11-04) this 3 ms kernel runs 1.20× the instructions and 1.16× the cycles of legacy dd86e3955 (0.066G vs 0.055G instructions), though the seq lane improved against the 2026-06-16 feed, 2.83× → 1.28× Rust.
