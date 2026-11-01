# 152. Maximum Product Subarray

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximum-product-subarray](https://leetcode.com/problems/maximum-product-subarray/)

Find the contiguous subarray with the **largest product**.

```
[2,3,-2,4]         ->  6      (2·3)
[-2,0,-1]          ->  0
[-2,3,-4]          ->  24     (-2·3·-4)
[2,-5,-2,-4,3]     ->  24     (-2·-4·3)
[-2]               ->  -2
[0,2]              ->  2
```

**Constraints:** `1 ≤ n ≤ 2·10⁴`, `-10 ≤ nums[i] ≤ 10`; the product of any prefix/suffix is guaranteed to fit in a 32-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **running max/min product DP** ★ | [`max_product.kara`](max_product.kara) ✓ | [`max_product.py`](max_product.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A single O(n) pass. The subtlety is the **sign flip**: multiplying by a negative turns the largest running product into the smallest and vice-versa. So track **both** the maximum and minimum product ending at the current index. On a negative element, **swap** `cur_max`/`cur_min` first; then each becomes `max`/`min` of `{x, prev·x}` (the `x` term restarts the window at the current element). The answer is the running maximum of `cur_max`.

## Kāra features exercised

- **Two-accumulator DP scan** — `cur_max`/`cur_min` carried across a `for i in 1..n` loop, with the negative-element swap.
- **Overflow-checked arithmetic** — the products `cur_max * x` / `cur_min * x` are checked `i64` multiplies (Kāra's default safety); the constraint that products fit in 32 bits keeps them in range.
- **`max`/`min` helpers** lowering to branchless conditional selects.

## Benchmarks
> **Machine.** The canonical figures are the Apple M5 Pro run below ([`bench/results.json`](bench/results.json)). The container table further down is the original reference run on a shared **x86-64 Linux cloud container** (22 Jul 2026), kept as history — [`bench/results.container-x86.json`](bench/results.container-x86.json) has since been re-measured and no longer holds those figures; absolute times there are noisy, so **within-run cross-language ratios are the signal.**

The `cur_max`/`cur_min` carry is a cross-iteration dependency chain, so the scan itself does **not** auto-parallelize; the default build does parallelize the `K = 10` outer sum over `max_product` calls (verified in the emitted IR (`KARAC_MIR_LL`): the default build carries a call of `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` twin does not). `bench.sh` measures the seq lane only. `N = 2·10⁶` deterministic values in `{-2,-1,0,1,2}` (an LCG; only `±2` grows the product magnitude and the frequent `0`s reset it, so the longest run reaches only `~2³¹` — no overflow, so the checked-arithmetic lanes agree with wrapping C/Go **and** Python's bignum). `K = 10` outer iterations; all five mirrors print the same sink (`21474836480`).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine `--warmup 5 --runs 30`; `KARAC_AUTO_PAR=0`):

| Run | Mean ± σ | vs kāra |
|---|---|---|
| c `max_product` (`clang -O3`) | 36.5 ± 0.6 ms | 1.18× ahead |
| rust `max_product` (`-O`, wrapping) | 36.7 ± 0.5 ms | 1.17× ahead |
| go `max_product` | 37.7 ± 0.6 ms | 1.14× ahead |
| rust `max_product` (`overflow-checks=on`) | 42.3 ± 1.0 ms | 1.02× ahead |
| **kāra `max_product` (codegen)** | **43.0 ± 1.2 ms** | — |
| python `max_product` | 6349 ± 260 ms — last measured 22 Jul 2026 on the container, not re-run (scale only) | — |

On the M5 Kāra is at equal-safety parity with `rust_ovf` (1.02× behind, inside one σ of each other), 1.17× behind wrapping `rustc -O` and 1.18× behind C. Against the previous M5 measurement (karac 0.1.0, legacy backend, 2026-07-27) the ratios are flat: Kāra/Rust 1.15× → 1.17×, Kāra/C 1.16× → 1.18×, Kāra/Go 1.13× → 1.14×, Kāra/`rust_ovf` 1.01× → 1.02× (every comparator also ran ~12% slower in absolute terms this session, so compare ratios, not milliseconds).

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Codegen at equal-safety parity — and ahead of `rust_ovf`

> **Note (1 Nov 2026).** "Ahead of `rust_ovf`" and the Go ranking below are the container run's. On the M5 Pro (table above) Kāra is 1.02× *behind* `rust_ovf`, and Go is 1.14× ahead of Kāra.

Container snapshot (22 Jul 2026), hyperfine `--warmup 5 --runs 30`:

| Run | Mean ± σ | vs kāra |
|---|---|---|
| c `max_product` (`clang -O3`) | 62.1 ± 1.3 ms | 1.10× ahead |
| rust `max_product` (`-O`, wrapping) | 67.0 ± 3.0 ms | 1.03× ahead |
| **kāra `max_product` (codegen)** | **68.7 ± 2.2 ms** | — |
| rust `max_product` (`overflow-checks=on`) | 73.2 ± 11.3 ms | **kāra 1.07× ahead** |
| go `max_product` | 87.4 ± 65.5 ms | kāra 1.27× ahead (go noisy) |
| python `max_product` | 6349 ± 260 ms | (scale only) |

The honest comparison is at **equal safety**. Kāra checks integer overflow by default; `rustc -O` *wraps*. Matching Kāra's safety with `-C overflow-checks=on` moves Rust to **73.2 ms** — and against that lane **Kāra is ahead** (68.7 vs 73.2). Against wrapping `rust -O` (67.0 ms) Kāra is within **~3%**, and within **1.10×** of C. The kernel is a tight branch (`x < 0` swap) plus two checked multiplies and two compares per element — a regime where LLVM produces near-optimal code for either frontend and the overflow-check tax is small.

## Running

```bash
karac run   max_product.kara
karac build max_product.kara && ./max_product
python3 max_product.py
diff <(karac run max_product.kara) <(python3 max_product.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.
