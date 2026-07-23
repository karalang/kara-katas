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

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 302.4 ms | 0.46× |
| C `clang -O3` | 326.3 ms | 0.49× |
| Go | 640.9 ms | 0.97× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 642.1 ms | 0.97× |
| **Kāra (codegen)** | 660.9 ms | 1.00× |
| Python (scale lane) | 24.49 s | 37.06× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   stock_iv.kara
karac build stock_iv.kara && ./stock_iv
python3 stock_iv.py
diff <(karac run stock_iv.kara) <(python3 stock_iv.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
