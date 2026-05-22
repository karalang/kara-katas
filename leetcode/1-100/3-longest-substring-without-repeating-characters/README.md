# 3. Longest Substring Without Repeating Characters

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Hash Map, Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-substring-without-repeating-characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

Given a string `s`, find the length of the longest substring without duplicate characters.

**Constraints:** `0 ≤ s.length ≤ 5 × 10⁴`, `s` consists of English letters, digits, symbols, and spaces.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sliding window with last-index map | O(n) time, O(min(n, σ)) space | [`sliding_window.kara`](sliding_window.kara) ✓ via `karac run` / `karac build` | [`sliding_window.py`](sliding_window.py) ✓ |

`✓` runs end-to-end today. `σ` is the alphabet size; for ASCII input the space bound is O(min(n, 128)).

### Why one map jump is enough

The naive sliding window shrinks `left` one step at a time on a duplicate — O(n) amortized but with a real factor-of-two penalty. The last-index variant turns each contraction into a single pointer jump: when character `c`'s previously-recorded index `prev` lies inside the current window (`prev >= left`), set `left = prev + 1` directly.

The `prev >= left` guard is the key invariant: a previous occurrence outside the current window is irrelevant and must not shrink the window. Without that guard, the second `a` in `"abba"` shrinks too aggressively and returns 2 instead of 3 (`"bba"`).

## Kāra features exercised

- **`ref String` + `s.chars()`** — read-only string borrow, iterated per Unicode scalar value via an inline byte-offset loop with a runtime UTF-8 decode helper.
- **`Map[char, i64]`** — `char` works as a hash key through the typechecker and the (now monomorphized) runtime Map; the whole algorithm is one Map.
- **`match Option[i64]` on `Map.get()`** — canonical "lookup and act on present/absent" idiom; `None => {}` is the no-op arm.
- **Mutable local accumulators** — `let mut left`, `let mut best`, `let mut right` updated by guarded `if` / `match`.

No `Vec`, no slices, no shared structs.

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   sliding_window.kara
karac build sliding_window.kara && ./sliding_window

# Python
python3 sliding_window.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 3 --runs 10` across the three binaries. Input is the 26-character lowercase alphabet repeated 4000 times (104_000 chars total). `K = 20` outer iterations; each call answers `26` (the longest non-repeating run is exactly one full alphabet cycle).
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact.

| File | What it does |
|---|---|
| [`bench/sliding_window.kara`](bench/sliding_window.kara) | 26-char alphabet × 4000 = 104K chars, K=20 outer iterations, `Map[char, i64]` last-index map |
| [`bench/sliding_window.py`](bench/sliding_window.py) | Algorithmic mirror — same input, same K, `dict[str, int]` |
| [`bench/sliding_window.rs`](bench/sliding_window.rs) | Algorithmic mirror; `HashMap<char, i64>`; compiled with `rustc -O` |

All three print the same sum-of-results sink (`K × 26 = 520`) so the algorithm's output participates in I/O and can't be elided.

### Runtime

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 3 --runs 20 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Run | Mean ± σ |
|---|---|
| `kara sliding_window` (codegen) | 7.0 ± 0.4 ms |
| `py sliding_window` | 113.6 ± 2.8 ms |
| `rust sliding_window` | 17.1 ± 0.2 ms |

Kāra runs **2.45× faster than Rust** and **16.3× faster than Python** here. The pre-monomorphization snapshot (2026-05-15, M1) read kara 1620 ms — 98× *slower* than Rust; the gap reversed by ~240× over the next three days. Two karac strands account for the swing:

- **Monomorphized `Map[char, i64]`** (phase-7 line 362, slices 1+2, commits `537e5d2` through `48e4963`, 2026-05-15). Replaces the type-erased C runtime's function-pointer hash/eq dispatch + byte-blob key/value storage with a per-`{K, V}` LLVM family (`karac_map_i32_i64_*` covers both `char` and `i32`; `linkonce_odr` linkage dedupes across crates). The mono `get` body inlines the FxHash+linear-probe loop at the call site so the hot path becomes "hash key → index → load i64" — no extern call, no indirect dispatch, no widening shim. The `1b.4` microbench (1M `Map[i64, i64]` insert+get) measured this strand at 1.32× faster than `std::HashMap` on its own.
- **Codegen body cleanup post-Slice 2.** Slice 2's bench-day snapshot (2026-05-15 PM, doc commit `a1aa01b`) still read 95.7× of Rust — only a ~2% delta from the type-erased baseline, with `karac_string_decode_char` per-char FFI fingered as the residual bottleneck. The remaining ~230× evaporated over the next three days of codegen work on adjacent surfaces (per-iter Vec/String leak close on auto-par + slot paths in `daaf2cc`, the cluster of RC-discipline fixes around the Map / shared-struct drop walks in `9d878ae` / `8b13048` / `d329023`, branch-tail fresh-ref detection in `919cfe0`). None of those targeted kata 3, but the cumulative effect on the inner-loop codegen quality is the only thing the gap reversal can be charged to.

**Where the time goes.** The body of `length_of_longest_substring` is ~2M Map operations: 104K chars × 20 outer iterations × (one `Map.get`, one `Map.insert`) per char. At 7.0 ms total, that's ~3.4 ns per Map op — consistent with a hash compute + inline probe hitting L1 on a 26-entry table.

**Where Kāra now beats Rust.** Rust's `HashMap<char, i64>` is fully monomorphized, but its `RandomState` SipHash13 hasher pays a DoS-resistance tax (per-instance seed + 13-round mixing) that dominates on tiny-table workloads. Kāra's hash is FxHash (rotate-5 + XOR + multiply; multiplier `0x517c_c1b7_2722_0a95`), chosen by `karac-rust/bench/hash_quality/` (2026-05-15) as the fastest non-cryptographic option on the per-K matrix — 4-8× faster than FNV-1a, geometric mean 0.56× of FNV-1a baseline. DoS resistance is not in scope for v1 (no user-controlled keys in this kata anyway). With the function-pointer indirection now gone on Kāra's side, FxHash-vs-SipHash13 is the headline asymmetry, and it lands in Kāra's favor on this shape.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build sliding_window.kara` | 63.0 ± 0.9 ms | 294.9 KiB |
| `rustc -O sliding_window.rs` | 122.7 ± 1.3 ms | 457.1 KiB |

Kāra compiles this kata **1.95× faster** than `rustc -O` and produces a binary **~35% smaller**. Consistent with the other katas — the cross-archive LTO + DCE work landed 2026-05-12 keeps the runtime contribution to binary size tight when downstream features (HTTP, JSON, tokio subgraph) aren't reached.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara sliding_window` (codegen) | 1.4 MiB |
| `rust sliding_window` | 1.3 MiB |
| `py sliding_window` | 7.0 MiB |

The 104K-char String is ~104 KB; the Map holds at most 26 entries; neither dominates allocation. Kāra now sits within 0.1 MiB of Rust — the type-erased Map's per-call buffer churn that drove the previous 0.5 MiB headroom went away with monomorphization (one allocator per `{K, V}` instantiation, same shape as Rust's `HashMap<char, i64>`).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil. This kata used to be the worst codegen-vs-Rust gap in the suite (98× *slower*) and so the most concrete justification for monomorphized collections; with Slice 1+2 of that work shipped, it's now 2.45× *faster* than Rust on the same input — the gap reversed, and the bench earned its keep as the natural-pull validation workload that originally motivated the strand.
