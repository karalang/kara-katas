# 123. Best Time to Buy and Sell Stock III

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/best-time-to-buy-and-sell-stock-iii](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

You may complete **at most two** transactions (buy one share, sell it, repeat — holding at most one share at a time). Given the daily `prices`, return the maximum profit. Where [#121](../121-best-time-to-buy-and-sell-stock/) allowed one transaction and [#122](../122-best-time-to-buy-and-sell-stock-ii/) allowed unlimited, this one caps you at two — the interesting middle.

```
prices = [3, 3, 5, 0, 0, 3, 1, 4]  ->  6   (buy 0 sell 3 = +3, buy 1 sell 4 = +3)
prices = [1, 2, 3, 4, 5]           ->  4   (one transaction is enough)
prices = [7, 6, 4, 3, 1]           ->  0   (prices only fall)
```

**Constraints:** `1 ≤ prices.length ≤ 10⁵`, `0 ≤ prices[i] ≤ 10⁵` — every profit fits a signed 64-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Four-state one-pass DP** ★ | [`max_profit.kara`](max_profit.kara) ✓ | [`max_profit.py`](max_profit.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the four-state relaxation equals the general at-most-`k` DP (specialised to `k=2`) *and* a brute-force search over all ≤2-transaction schedules, on many random series. Zero disagreements. The solver compiles with zero diagnostics and is valgrind-clean.

## The mechanism

**Four-state DP** ([`max_profit.kara`](max_profit.kara), the ★): carry four running values through a single pass and relax each every day —

- `buy1 = max(buy1, -price)` — best balance after opening the **1st** position
- `sell1 = max(sell1, buy1 + price)` — best profit after closing the **1st**
- `buy2 = max(buy2, sell1 - price)` — best balance after opening the **2nd**, funded by `sell1`
- `sell2 = max(sell2, buy2 + price)` — best profit after closing the **2nd** — the answer

The chained order (each state feeds the next) means a single left-to-right sweep captures the best two non-overlapping transactions. O(n) time, O(1) space — no `k`-sized table, just four scalars.

## Kāra features exercised

- **Chained scalar-state relaxations** — four interdependent `if new > state { state = new }` updates per element, each lowering to a **branchless conditional-move** (`cmovg`), so the hot loop is four cmovs with no data-dependent branches.
- **Per-op overflow checks** — the four negate/add/subtract operations each carry kāra's default overflow trap (`jo`); this is the honest cost the equal-safety Rust row also pays.
- **Forward-index BCE** — `prices[i]` on the hot path drops its bounds check (the `for i in 1..n` guard proves `i < n`); the whole binary carries a single panic site, the shared overflow trap.

**v1 note.** Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; agrees with the Python mirror and the general-`k` DP + brute-force ground truth, and is valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   max_profit.kara
karac build max_profit.kara && ./max_profit

# Python
python3 max_profit.py

# Verify they agree
diff <(karac run max_profit.kara) <(python3 max_profit.py) && echo OK

# Ground truth: four-state == general-k DP == brute force
python3 ground_truth.py
```

## Benchmarks

Wall-clock comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`max_profit.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). Absolute times/sizes/RSS are **not** comparable across hosts; only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to fold a canonical `results.json`.

**Workload.** `N = 2,000,000` deterministic LCG-generated prices in `[1, 4096]`, the four-state DP run **K = 10** times, folding a sum-of-results sink. Dominated by the O(n) four-relaxation pass.

**Single-threaded, by design.** The K=10 outer loop is a **serial dependency chain** — each rep perturbs the opening price by the previous rep's result. A naive `sum += max_profit(data)` reduction would auto-parallelize under kāra's default build (the four-state body is "heavy" enough to trip the cost model), raising CPU to ~200% and adding scheduling variance — an unfair comparison against the single-threaded C/Rust/Go mirrors. The serial loop keeps every mirror on one core, so the numbers measure the *algorithm*, not the harness.

**Equal safety.** Kāra checks integer overflow (and array bounds) by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow.

`--warmup 12 --runs 60`. All single-threaded. **x86-64 container numbers**:

| Implementation | Wall time | Store |
|---|---|---|
| c    max_profit (clang -O3)                    | 42 ± 1 ms | `long[]` |
| rust max_profit (rustc -O)                     | 43 ± 2 ms | `Vec<i64>` |
| go   max_profit (`[]int64`)                    | 47 ± 14 ms | `[]int64` |
| rust max_profit (rustc -O, overflow-checks=on) | 48 ± 1 ms | `Vec<i64>` |
| **kāra max_profit**                            | **49 ± 2 ms** | **`Vec[i64]`** |

**Kāra is at equal-safety parity with Rust — kāra 49 ms reads level with `rustc -O -C overflow-checks=on` at 48 ms.** The ~1.15× gap to wrapping `rust -O` / C (42–43 ms) is the **overflow-check tax**, and it is larger here than in [#121](../121-best-time-to-buy-and-sell-stock/)/[#122](../122-best-time-to-buy-and-sell-stock-ii/) precisely because the four-state DP does four overflow-checked ops per element instead of one. kāra's inner loop is four branchless `cmovg` relaxations plus four `jo` overflow checks, with `prices[i]` bounds-check-elided — the same instruction budget `overflow-checks=on` Rust carries, hence the tie. Verified correct (all compiled mirrors agree on the sink) and valgrind-clean. Python (pure-Python, timed separately) is omitted.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched four-state scalar DP (`Slice[i64]` vs `&[i64]`). Like its siblings #121/#122, this is a *clean-parity* kata: the equal-safety comparison ties (both carry the four overflow checks and the elided bounds check), and the only separation from wrapping `-O` Rust is the safety tax kāra pays by default — here amplified 4× by the four-op body. C's `long[]` is the metal floor, Go the GC data point, Python (timed separately, not cross-checked) the ergonomic foil.
