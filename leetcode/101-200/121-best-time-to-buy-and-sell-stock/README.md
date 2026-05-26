# 121. Best Time to Buy and Sell Stock

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/best-time-to-buy-and-sell-stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

You are given an array `prices` where `prices[i]` is the price of a given stock on the i-th day. Choose a single buy day and a strictly later sell day to maximize profit. Return that maximum profit, or `0` if no profitable trade exists.

**Constraints:** `1 ≤ prices.length ≤ 10⁵`, `0 ≤ prices[i] ≤ 10⁴`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| One-pass: track running min, update running max profit | O(n) time, O(1) space | [`one_pass.kara`](one_pass.kara) ✓ via `karac run` | [`one_pass.py`](one_pass.py) ✓ |

`✓` runs end-to-end today.

### Why one pass is enough

The best profit ending on day `k` is `prices[k] - min(prices[0..=k])`. Walking left to right while maintaining `min_so_far` makes that an O(1) update per step, and the overall answer is the running maximum of those daily candidates. No DP table, no sort.

## Kāra features exercised

- **`Slice[i64]` parameter** — read-only slice; LeetCode driver passes `Array[i64, N]` literals, bench passes `Vec[i64].as_slice()`.
- **Indexed slice access** with `for i in 1..n` half-open range.
- **Mutable local accumulators** — `let mut min_price`, `let mut best`, updated by guarded `if`.

No `Map`, no strings, no shared structs.

## Running

```bash
# Kāra
karac run one_pass.kara

# Python
python3 one_pass.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 5 --runs 30` across the three binaries on `N = 2_000_000` deterministic LCG-generated prices, `K = 10` outer iterations so the O(n) scan dominates per-process startup.
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact (`bench/target/one_pass_kara` and `bench/target/one_pass`).

| File | What it does |
|---|---|
| [`bench/one_pass.kara`](bench/one_pass.kara) | N=2_000_000 LCG-generated prices in `[1, 4096]`, K=10 outer iterations, one-pass running min + running max profit |
| [`bench/one_pass.py`](bench/one_pass.py) | Algorithmic mirror — same N, K, generator |
| [`bench/one_pass.rs`](bench/one_pass.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sum-of-results sink (`K × max_profit = 40_950`) so the algorithm's output participates in I/O and can't be elided.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `one_pass` | 14.7 ± 0.2 ms | 15.0 ± 0.6 ms | **1.02× faster than Rust** |

The O(n) scan is essentially a tight loop with two compares, a subtraction, and two conditional stores — a regime where modern LLVM produces near-optimal machine code for either frontend. The May-14 snapshot read kara at 1.09× *of* Rust on M1; the gap has closed with the cross-archive LTO + DCE work and the karac drop-pathway fix that also showed up in kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak)'s memory profile. The 0.3 ms wall difference is inside startup-and-page-fault variance for a 16 MiB `Vec[i64]` allocation (see runtime-memory section below), not algorithm time.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara one_pass` (codegen) | 14.7 ± 0.2 ms |
| `rust one_pass` | 15.0 ± 0.6 ms |
| `py one_pass` | 539.6 ± 11.5 ms |

Python is **~37× slower** than Kāra codegen on this workload — the per-iteration overhead of CPython bytecode dispatch dominates everything else when the body is two integer compares.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build one_pass.kara` | 56.4 ± 1.2 ms | 32.8 KiB |
| `rustc -O one_pass.rs` | 82.0 ± 1.5 ms | 455.6 KiB |

Kāra compiles this kata **1.45× faster** than `rustc -O` and produces a binary **~93% smaller** (14× the size disparity, vs the ~35% disparity measured against the same source on 2026-05-14). The much smaller binary tracks the cross-archive LTO + DCE work landed 2026-05-12, which strips the unreachable runtime surface (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs) when downstream features aren't used. Same shape as kata [#4](../../1-100/4-median-of-two-sorted-arrays/#compile-time-and-binary-size) and kata [#88](../../1-100/88-merge-sorted-array/#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara one_pass` (codegen) | 16.4 MiB |
| `rust one_pass` | 16.4 MiB |
| `py one_pass` | 81.7 MiB |

**Parity with Rust on memory**, byte-for-byte. The bench's `Vec.filled(N, 0)` for a 2M-element `Vec[i64]` allocates exactly the 16 MiB working set, then the one-pass scan walks it. The May-14 snapshot measured kara at 32.8 MiB against the same source; the 16 MiB headroom traced to a karac drop / allocator pathway that has since been fixed, and the current build matches Rust's `vec![0; N]` allocation profile exactly. Same story as kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
