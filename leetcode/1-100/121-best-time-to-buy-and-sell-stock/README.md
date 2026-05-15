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

```
min_price = prices[0]
best      = 0
for p in prices[1..]:
    min_price = min(min_price, p)
    best      = max(best, p - min_price)
return best
```

## Kāra features exercised

- **`Slice[i64]` parameter** — function takes an immutable slice; the LeetCode case-driver passes `Array[i64, N]` literals, the bench passes `Vec[i64].as_slice()`.
- **Indexed slice access** — `prices[0]` for the seed, `prices[i]` inside the for-by-index loop.
- **`for i in 1..n`** — half-open integer range.
- **Mutable local accumulators** — `let mut min_price`, `let mut best`, updated by guarded `if`.

No `Map`, no strings, no shared structs.

## API shape

Each solution exposes a pure `max_profit(prices) -> i64` (Python: `-> int`) and a thin `report` that prints. `main` calls `report` per test case. Logic is separate from I/O so the function is testable once a harness exists.

## Output format

One integer per line — the maximum profit for each test case. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
5
0
0
```

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

Snapshot — M1, 2026-05-14, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `one_pass` | 15.5 ± 0.2 ms | 14.2 ± 0.9 ms | **1.09× of Rust** |

The O(n) scan is essentially a tight loop with two compares, a subtraction, and two conditional stores — a regime where modern LLVM produces near-optimal machine code for either frontend. The ~1.3 ms residual gap is within startup-and-page-fault variance for a 16 MB `Vec[i64]` allocation (see runtime-memory section below), not algorithm time.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara one_pass` (codegen) | 15.5 ± 0.2 ms |
| `rust one_pass` | 14.2 ± 0.9 ms |
| `py one_pass` | 514.9 ± 3.6 ms |

Python is **~36× slower** than Kāra codegen on this workload — the per-iteration overhead of CPython bytecode dispatch dominates everything else when the body is two integer compares.

### Compile time and binary size

Snapshot — M1, 2026-05-14, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build one_pass.kara` | 54.1 ± 0.3 ms | 295.7 KiB |
| `rustc -O one_pass.rs` | 77.9 ± 0.8 ms | 455.6 KiB |

Kāra compiles this kata **1.44× faster** than `rustc -O` and produces a binary **~35% smaller**.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara one_pass` (codegen) | 32.8 MiB |
| `rust one_pass` | 16.4 MiB |
| `py one_pass` | 81.8 MiB |

Kāra's peak is ~2× Rust's because `Vec[i64].push` doubles capacity on each grow — the final 2M-element Vec is 16 MiB (i64 × 2M), and the doubling pass before it allocates an additional 16 MiB transient buffer that sits at peak. Rust's `Vec::with_capacity(N)` short-circuits the doubling. Equivalent capacity-hint support in Kāra (e.g., `Vec.with_capacity(n)`) would close this gap.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
