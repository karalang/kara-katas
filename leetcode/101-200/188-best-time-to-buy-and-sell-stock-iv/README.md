# 188. Best Time to Buy and Sell Stock IV

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/best-time-to-buy-and-sell-stock-iv](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

Maximum profit from **at most `k`** buy/sell transactions (buy before sell, one position held at a time).

```
k=2, [2,4,1]        ->  2
k=2, [3,2,6,5,0,3]  ->  7
k=3, [1,4,2,8,3,9,1,7] -> 19
```

**Constraints:** `1 ≤ k ≤ 100`, `1 ≤ n ≤ 1000`, `0 ≤ prices[i] ≤ 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **rolling buy/sell DP (+ greedy shortcut)** ★ | [`stock_iv.kara`](stock_iv.kara) | [`stock_iv.py`](stock_iv.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Two regimes. When `k ≥ n/2` the cap is not binding — you can take every upward move — so greedily sum all positive day-to-day deltas. Otherwise an **O(n·k) DP** over two rolling arrays: `buy[j]` = best profit while **holding** after at most `j` buys, `sell[j]` = best profit while **flat** after at most `j` sells. For each price, `buy[j] = max(buy[j], sell[j-1] - price)` (open the j-th position) and `sell[j] = max(sell[j], buy[j] + price)` (close it). The answer is `sell[k]`. `buy` starts at a large negative sentinel (never having held is impossible profit); `sell` starts at 0.

## Kāra features exercised

- **Two rolling `Vec[i64]` DP arrays** (`buy`, `sell`) sized `k+1`, updated in a nested `for price × for j` sweep with in-place `buy[t]`/`sell[t]` index-assign.
- **Branch on regime** — the `k ≥ n/2` greedy shortcut vs the full DP — and a large-negative sentinel that stays overflow-safe under Kāra's checked arithmetic (`neg + price` never wraps).
- **`Slice[i64]`** input from fixed-size `Array` literals.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`121941975`). Workload: O(n*k) two-array transaction DP over a 2000-price PRNG array x 5000 rounds, fresh PRNG k (<n/2) + one price punch per round (loop-carried max recurrence).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (0.9.0-dev.14057, v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 251.1 ± 2.9 ms | 0.46× |
| Rust `-O` | 252.0 ± 3.3 ms | 0.46× |
| Go | 452.6 ± 5.9 ms | 0.82× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 545.4 ± 5.2 ms | 0.99× |
| **Kāra (codegen)** | 549.4 ± 5.8 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Kāra is last: **2.18×** behind `rustc -O`, **2.19×** behind C and **1.21×** behind Go, but at parity with equal-safety Rust (**1.01×**, 549.4 vs 545.4 ms). Against the previous feed (2026-07-28, legacy backend `karac 0.1.0`: 2.16× Rust, 2.19× C, 1.20× Go, 1.00× equal-safety Rust) every ratio is within 1%, so flat. Every comparator ran 15–16% slower this session (machine state), so compare the ratios, not the milliseconds.

Binary size: C 32.8 KiB, **kāra 295.8 KiB** (302,872 B), Rust 455.6 KiB, Go 2.38 MiB; every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's was 34,312 B on 2026-07-28), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: **kāra 1.23 MiB**, C 1.48 MiB, Rust 1.52 MiB, Go 4.94 MiB. Compile-cold: clang 47.7 ms < rustc 95.3 ms < **karac 124.4 ms** (2.61× clang, 1.31× rustc); compile peak RSS clang 2.6 MiB, rustc 29.0 MiB, **karac 59.0 MiB**.

## Running

```bash
karac run   stock_iv.kara
karac build stock_iv.kara && ./stock_iv
python3 stock_iv.py
diff <(karac run stock_iv.kara) <(python3 stock_iv.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
