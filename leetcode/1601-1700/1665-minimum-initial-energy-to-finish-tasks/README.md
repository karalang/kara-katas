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

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 2 --runs 10` across the three binaries on `N = 50_000` deterministic `(actual, minimum)` tasks, `K = 5` outer iterations so algorithm time dominates per-process startup.
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact (`bench/target/greedy_kara` and `bench/target/greedy`).

| File | What it does |
|---|---|
| [`bench/greedy.kara`](bench/greedy.kara) | N=50_000 deterministic generator, K=5 outer iterations, sort-by-`(minimum - actual)`-descending via `Vec.sort_by` with an inline closure comparator |
| [`bench/greedy.py`](bench/greedy.py) | Algorithmic mirror — same N, K, generator |
| [`bench/greedy.rs`](bench/greedy.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sum-of-results sink so the algorithm's output participates in I/O and can't be elided.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `greedy` | 3.2 ± 0.1 ms | 2.7 ± 0.0 ms | **1.19× of Rust** |

This kata is **sort-dominated** — pdqsort over 50,000 `(i64, i64)` pairs is ~850k comparisons per call × K=5 ≈ 4M comparator invocations. The remaining gap is the FFI hop on each comparison: `karac_vec_sort_by` lives in a precompiled runtime crate and calls the user comparator via an `extern "C" fn` pointer that LLVM in the runtime crate sees as opaque and cannot inline through. Codegen already does the cheapest fix on its own side — `emit_sort_by_inline_thunk` fuses the closure body into the bridge thunk so the function pointer points directly at the comparator code rather than going through a fat-pointer indirect call. The 2026-05-12 → 2026-05-25 gap-tightening from 1.37× → 1.19× tracks the cumulative effect of cross-archive LTO + DCE, the `__TEXT,__jittmpl` segment re-scope (`e76f42b`), and platform shift from M1 → M5 Pro. Closing the remaining FFI-boundary cost is tracked in [`deferred.md` § *Vec.sort_by FFI-Boundary Comparator Inlining*](../../../../karac-rust/docs/deferred.md); promotion gate fires once ≥2 distinct non-synthetic workloads show >1.3× perf gap from this specific cause.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara greedy` (codegen) | 3.2 ± 0.1 ms |
| `rust greedy` | 2.7 ± 0.0 ms |
| `py greedy` | 38.3 ± 0.6 ms |

Python is **~12× slower** than Kāra codegen here — the algorithm-dominated regime at N=50k where compiled-with-codegen languages put the same lap on CPython they do on every other O(n log n) workload at this size.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build greedy.kara` | 58.9 ± 0.9 ms | 294.7 KiB |
| `rustc -O greedy.rs` | 119.7 ± 1.1 ms | 472.1 KiB |

Kāra compiles this kata **~2× faster** than `rustc -O` and produces a binary **~38% smaller** — the cumulative effect of the 2026-05-12 fat-LTO runtime rebuild that exposed dead `Vec.sort_by` / `Map` plumbing to `-Wl,-dead_strip` (shaving ~17%), plus the 2026-05-25 `__TEXT,__jittmpl` segment re-scope (`karac-rust e76f42b`) that reclaimed an additional 16 KiB per Mach-O binary (311.9 KiB → 294.7 KiB on this kata).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
