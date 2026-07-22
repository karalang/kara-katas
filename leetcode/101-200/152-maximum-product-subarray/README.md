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

> **Machine.** Container-only reference run so far — a shared **x86-64 Linux cloud container** ([`bench/results.container-x86.json`](bench/results.container-x86.json)); canonical Apple-M5 numbers (`bench/results.json`) are pending a maintainer run. Absolute times are noisy on the shared host; **within-run cross-language ratios are the signal.**

Seq-only kata — the `cur_max`/`cur_min` carry is a cross-iteration dependency chain, so the scan does **not** auto-parallelize. `N = 2·10⁶` deterministic values in `{-2,-1,0,1,2}` (an LCG; only `±2` grows the product magnitude and the frequent `0`s reset it, so the longest run reaches only `~2³¹` — no overflow, so the checked-arithmetic lanes agree with wrapping C/Go **and** Python's bignum). `K = 10` outer iterations; all five mirrors print the same sink (`21474836480`).

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Codegen at equal-safety parity — and ahead of `rust_ovf`

Container snapshot, hyperfine `--warmup 5 --runs 30`:

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
