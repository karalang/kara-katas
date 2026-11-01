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
> **Machine.** The canonical numbers below are an **Apple M5 Pro** run ([`bench/results.json`](bench/results.json)) — karac g6697158fa (v2/MIR backend), measured 2026-11-01. A shared **x86-64 Linux cloud-container** reference run is folded in separately ([`bench/results.container-x86.json`](bench/results.container-x86.json)); absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal. The container run reproduced the headline — **kāra at equal-safety parity with `rustc -O -C overflow-checks=on`** (both ~32 ms there, ~1.3× behind wrapping `rust -O`, the overflow-check tax) — though its short ~30 ms workload is noisier, so the M5 run is the stable reference.

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

M5 Pro, 2026-11-01, karac g6697158fa (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded (seq-only kata — the running-min/max-profit pair is a cross-iteration dependency chain; bench.sh builds Kāra with `KARAC_AUTO_PAR=0`, because the default build auto-parallelises the K=10 outer `sum` loop — one `karac_mir_task_spawn` call in its emitted IR (`KARAC_MIR_LL`), none in the seq build):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    one_pass (clang -O3) | 14.9 ± 0.3 ms | 1.08× ahead of kāra |
| rust one_pass (`-O`, wrapping) | 15.6 ± 0.3 ms | 1.03× ahead of kāra |
| go   one_pass | 15.9 ± 0.3 ms | 1.01× ahead of kāra |
| **kāra one_pass (codegen)** | **16.1 ± 0.3 ms** | — |
| rust one_pass (`overflow-checks=on`) | 16.2 ± 0.8 ms | **1.00× — equal-safety parity** |

The honest comparison is at equal safety. Kāra checks integer overflow by default; `rustc -O` *wraps* — its 15.6 ms is a no-overflow-check binary. Matching Kāra's default safety with `-C overflow-checks=on` moves Rust to **16.2 ms**, and against that lane Kāra reads **1.00×** (16.1 vs 16.2, both ~14.7 ms User, well inside the noise band). The small gap to wrapping `-O` Rust is the overflow-check safety tax, and it vanishes once Rust opts into the same checks. The O(n) scan is essentially a tight loop with two compares, a subtraction, and two conditional stores — a regime where modern LLVM produces near-optimal machine code for either frontend. Every comparator ran 8–14% slower in this session than in the previous feed (legacy karac, 2026-06-16), so the ratios carry the comparison: Kāra/Rust 1.04× → 1.03×, Kāra/C 1.09× → 1.08×, Kāra/Go 0.97× → 1.01× — flat on all three. The May-14 snapshot read kara at 1.09× *of* Rust on M1; the gap closed with the cross-archive LTO + DCE work and the karac drop-pathway fix that also showed up in kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak)'s memory profile. C's 1.08× lead is the no-bounds-check, no-overflow-check floor.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara one_pass` (codegen) | 16.1 ± 0.3 ms |
| `rust one_pass` (`-O`, wraps) | 15.6 ± 0.3 ms |
| `py one_pass` (last measured 2026-06-16, not re-run) | 524.7 ± 3.1 ms |

Python was **~37× slower** than Kāra codegen in its last measured session (524.7 vs 14.3 ms, 2026-06-16; this run did not set `KARA_BENCH_INCLUDE_PY`) — the per-iteration overhead of CPython bytecode dispatch dominates everything else when the body is two integer compares.

### Compile time and binary size

M5 Pro, 2026-11-01, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build one_pass.kara` | 110.6 ± 2.0 ms | 295.8 KiB |
| `rustc -O one_pass.rs` | 89.1 ± 1.1 ms | 455.6 KiB |
| `clang -O3 one_pass.c` | 46.9 ± 1.0 ms | 32.7 KiB |

`karac build` is now **1.24× slower** than `rustc -O` on this kata (the 2026-06-16 legacy feed had it 1.33× faster, 71.0 vs 94.7 ms). The Kāra binary is 302,920 B — **~35% smaller** than Rust's, but ~9× C's 33,512 B: every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (legacy built this kata to 34,056 B), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). (History: the legacy binary's near-C size tracked the cross-archive LTO + DCE work landed 2026-05-12, which strips the unreachable runtime surface (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs) when downstream features aren't used. Same shape as kata [#4](../../1-100/4-median-of-two-sorted-arrays/#compile-time-and-binary-size) and kata [#88](../../1-100/88-merge-sorted-array/#compile-time-and-binary-size).)

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara one_pass` (codegen) | 16.3 MiB |
| `c    one_pass` | 16.3 MiB |
| `rust one_pass` | 16.4 MiB |
| `go   one_pass` | 18.8 MiB |
| `py one_pass` (last measured 2026-06-16, not re-run) | 81.8 MiB |

**Parity with C and Rust on memory** — the 2026-11-01 single-shot readings put kara (17,138,024 B) between C (17,105,232 B) and Rust (17,154,384 B), all within 48 KiB of each other. Page-level jitter aside, all three sit on the same working set: the bench's `Vec.filled(N, 0)` for a 2M-element `Vec[i64]` allocates exactly the 16 MiB, then the one-pass scan walks it. The May-14 snapshot measured kara at 32.8 MiB against the same source; the 16 MiB headroom traced to a karac drop / allocator pathway that has since been fixed, and the current build matches Rust's `vec![0; N]` allocation profile. Same story as kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (1.08× ahead — the no-bounds-check loop), Go is the cross-runtime data point (1.01× ahead of kāra, a tie), and Python is the ergonomic foil.
