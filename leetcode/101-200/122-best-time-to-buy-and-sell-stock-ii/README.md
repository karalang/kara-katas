# 122. Best Time to Buy and Sell Stock II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Greedy &nbsp;·&nbsp; **Source:** [leetcode.com/problems/best-time-to-buy-and-sell-stock-ii](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

You may complete **as many transactions as you like** (buy one share, sell it, repeat) — but you may hold **at most one** share at a time. Given the daily `prices`, return the maximum profit. Where [#121](../121-best-time-to-buy-and-sell-stock/) allowed a *single* buy/sell, this one lets you ride every upswing.

```
prices = [7, 1, 5, 3, 6, 4]  ->  7    (buy 1 sell 5 = +4, buy 3 sell 6 = +3)
prices = [1, 2, 3, 4, 5]     ->  4    (one long upward run, 1 -> 5)
prices = [7, 6, 4, 3, 1]     ->  0    (prices only fall)
```

**Constraints:** `1 ≤ prices.length ≤ 3·10⁴`, `0 ≤ prices[i] ≤ 10⁴` — every profit fits a signed 64-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Greedy — sum every positive daily gain** ★ | [`max_profit.kara`](max_profit.kara) ✓ | [`max_profit.py`](max_profit.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the greedy sum equals an O(n) cash/hold **DP state machine** *and* a **brute-force** search over all buy/sell decisions, on many random series. Zero disagreements. The solver compiles with zero diagnostics and is valgrind-clean.

## The mechanism

**Greedy** ([`max_profit.kara`](max_profit.kara), the ★): the key insight is that any profitable multi-day rise `a → … → b` decomposes into the sum of its consecutive one-day gains, so you never need to look ahead — just **pocket every positive `prices[i] - prices[i-1]`**. Downward days contribute nothing (you simply don't hold). One pass, O(n) time, O(1) space. This proves optimal because the greedy sum is an upper bound (no schedule can capture more than every up-move) that the "buy-before-each-rise, sell-after" schedule achieves.

## Kāra features exercised

- **Offset-index read** — the loop reads both `prices[i]` and `prices[i-1]` on the hot path; kāra's bounds-check elision proves `i-1 ≥ 0` from the `for i in 1..n` lower bound and `i < n` from the upper, so **both** indices drop their checks (the compiled binary carries a single panic site — the shared overflow trap; see Benchmarks).
- **Conditional accumulation** — `if d > 0 { profit += d }` lowers to a compare-and-conditional-add with the overflow check on the subtraction, no branch mispredict penalty on the accumulate.

**v1 note.** Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; agrees with the Python mirror and the DP + brute-force ground truth, and is valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   max_profit.kara
karac build max_profit.kara && ./max_profit

# Python
python3 max_profit.py

# Verify they agree
diff <(karac run max_profit.kara) <(python3 max_profit.py) && echo OK

# Ground truth: greedy == DP state machine == brute force
python3 ground_truth.py
```

## Benchmarks

Wall-clock comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`max_profit.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). Absolute times/sizes/RSS are **not** comparable across hosts; only within-file cross-language ratios are the signal. This is a **short workload (~24–32 ms)**, so container noise is elevated — read the *ratios*. Re-run `bench.sh` on the M5 to fold a canonical `results.json`.

**Workload.** `N = 2,000,000` deterministic LCG-generated prices in `[1, 4096]`, the greedy scan run **K = 10** times, folding a sum-of-results sink. Dominated by the O(n) `profit += max(0, prices[i] - prices[i-1])` pass.

**Equal safety.** Kāra checks integer overflow (and array bounds) by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow.

`--warmup 12 --runs 60`. All single-threaded. **x86-64 container numbers**:

| Implementation | Wall time | Store |
|---|---|---|
| c    max_profit (clang -O3)                    | 24 ± 1 ms | `long[]` |
| rust max_profit (rustc -O)                     | 24 ± 1 ms | `Vec<i64>` |
| rust max_profit (rustc -O, overflow-checks=on) | 29 ± 2 ms | `Vec<i64>` |
| **kāra max_profit**                            | **29 ± 2 ms** | **`Vec[i64]`** |
| go   max_profit (`[]int64`)                    | 32 ± 1 ms | `[]int64` |

**Kāra is at equal-safety parity with Rust — kāra 29 ms reads identical to `rustc -O -C overflow-checks=on` at 29 ms.** The ~1.2× gap to wrapping `rust -O` / C (both 24 ms) is the **overflow-check tax**, not a codegen deficit: kāra's greedy loop is `sub prices[i]-prices[i-1]; jo <ovf>; jle <skip>; add`, with **both** the forward index `prices[i]` and the offset index `prices[i-1]` bounds-check-elided (the `for i in 1..n` guard proves `i-1 ≥ 0` and `i < n`) — the whole binary carries a single panic site, the shared overflow trap. That is the same instruction budget `overflow-checks=on` Rust carries, hence the tie. Verified correct (all compiled mirrors agree on the sink) and valgrind-clean. Python (pure-Python, ~30× slower per rep, timed separately) is omitted.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched greedy O(n) scan (`Slice[i64]` vs `&[i64]`). Like its sibling [#121](../121-best-time-to-buy-and-sell-stock/), this is a *clean-parity* kata: the equal-safety comparison ties (both carry overflow + the same elided bounds checks), and the only separation from wrapping `-O` Rust is the safety tax kāra pays by default. C's `long[]` is the metal floor, Go the GC data point, Python (timed separately, not cross-checked) the ergonomic foil.
