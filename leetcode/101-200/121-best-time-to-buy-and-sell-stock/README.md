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

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go mirror with `go build`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then runs runtime (`hyperfine --warmup 5 --runs 30`, `N = 2_000_000` deterministic LCG-generated prices, `K = 10` outer iterations so the O(n) scan dominates per-process startup), compile-cost (cold, via a `--prepare` delete step), binary-size, and peak-RSS passes.

| File | What it does |
|---|---|
| [`bench/one_pass.kara`](bench/one_pass.kara) | N=2_000_000 LCG-generated prices in `[1, 4096]`, K=10 outer iterations, one-pass running min + running max profit |
| [`bench/one_pass.py`](bench/one_pass.py) | Algorithmic mirror — same N, K, generator |
| [`bench/one_pass.rs`](bench/one_pass.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/one_pass.c`](bench/one_pass.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |

All mirrors print the same sum-of-results sink (`K × max_profit = 40_950`) so the algorithm's output participates in I/O and can't be elided; bench.sh fails loudly on mismatch.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded (seq-only kata — the running-min/max-profit pair is a cross-iteration dependency chain):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    one_pass (clang -O3) | 13.2 ± 0.1 ms | 1.07× ahead of kāra |
| **kāra one_pass (codegen)** | **14.3 ± 0.1 ms** | — |
| rust one_pass (`-O`, wrapping) | 13.7 ± 0.1 ms | 1.04× ahead of kāra |
| rust one_pass (`overflow-checks=on`) | 14.1 ± 0.1 ms | **1.01× — equal-safety parity** |
| go   one_pass | 15.1 ± 1.2 ms | kāra 1.06× ahead of Go |

The honest comparison is at equal safety. Kāra checks integer overflow by default; `rustc -O` *wraps* — its 13.7 ms is a no-overflow-check binary. Matching Kāra's default safety with `-C overflow-checks=on` moves Rust to **14.1 ms**, and against that lane Kāra and Rust read **identical to the tenth of a millisecond** — a **1.01× tie** (14.3 vs 14.1, both ~12.5 ms User, well inside the noise band). The small gap to wrapping `-O` Rust is the overflow-check safety tax, and it vanishes once Rust opts into the same checks. The O(n) scan is essentially a tight loop with two compares, a subtraction, and two conditional stores — a regime where modern LLVM produces near-optimal machine code for either frontend. The May-14 snapshot read kara at 1.09× *of* Rust on M1; the gap closed with the cross-archive LTO + DCE work and the karac drop-pathway fix that also showed up in kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak)'s memory profile. C's 1.07× lead is the no-bounds-check, no-overflow-check floor.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara one_pass` (codegen) | 14.3 ± 0.1 ms |
| `rust one_pass` | 14.3 ± 1.8 ms |
| `py one_pass` | 520.3 ± 2.0 ms |

Python is **~36× slower** than Kāra codegen on this workload — the per-iteration overhead of CPython bytecode dispatch dominates everything else when the body is two integer compares.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build one_pass.kara` | 74.8 ± 0.4 ms | 33.3 KiB |
| `rustc -O one_pass.rs` | 94.5 ± 1.7 ms | 455.6 KiB |
| `clang -O3 one_pass.c` | 46.1 ± 0.4 ms | 32.7 KiB |

Kāra compiles this kata **1.26× faster** than `rustc -O` and produces a binary **~93% smaller** — within 615 bytes of C's (34,099 vs 33,484 B). (The 2026-05-18 snapshot read `karac build` at 56.4 ± 1.2 ms against the karac installed at the time; the May-30 karac reinstall plus the 06-05 environment band account for today's 74.8 — the emitted binary is byte-identical across the two compilers. rustc 82.0 → 94.5.) The much smaller binary tracks the cross-archive LTO + DCE work landed 2026-05-12, which strips the unreachable runtime surface (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs) when downstream features aren't used. Same shape as kata [#4](../../1-100/4-median-of-two-sorted-arrays/#compile-time-and-binary-size) and kata [#88](../../1-100/88-merge-sorted-array/#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara one_pass` (codegen) | 16.3 MiB |
| `c    one_pass` | 16.3 MiB |
| `rust one_pass` | 16.3 MiB |
| `go   one_pass` | 19.0 MiB |
| `py one_pass` | 81.7 MiB |

**Parity with C and Rust on memory** — today's single-shot readings put kara and Rust byte-identical (17,137,664 B) with C one 32 KiB page below; the 2026-05-18 sample read kara/Rust byte-identical instead. Page-level jitter aside, all three sit on the same working set: the bench's `Vec.filled(N, 0)` for a 2M-element `Vec[i64]` allocates exactly the 16 MiB, then the one-pass scan walks it. The May-14 snapshot measured kara at 32.8 MiB against the same source; the 16 MiB headroom traced to a karac drop / allocator pathway that has since been fixed, and the current build matches Rust's `vec![0; N]` allocation profile exactly. Same story as kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (1.07× ahead — the no-bounds-check loop), Go is the cross-runtime data point (1.06× behind kāra), and Python is the ergonomic foil.
