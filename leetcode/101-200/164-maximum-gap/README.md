# 164. Maximum Gap

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Sorting · Bucket Sort · Radix Sort &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximum-gap](https://leetcode.com/problems/maximum-gap/)

Given an unsorted array, return the maximum difference between two **successive** elements in its sorted form (0 if fewer than two elements). Must run in **linear time and linear space**.

```
[3,6,9,1]  ->  3    (sorted 1,3,6,9 — gaps 2,3,3)
[10,1]     ->  9
[1]        ->  0
```

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ nums[i] ≤ 10⁹`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **pigeonhole (bucket) method** ★ | [`maximum_gap.kara`](maximum_gap.kara) ✓ | [`maximum_gap.py`](maximum_gap.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The linear-time constraint rules out comparison sorting. Key insight: if `n` values span `[lo, hi]`, the **average** gap after sorting is `(hi-lo)/(n-1)`, and the maximum gap is at least that. So choose a bucket width `bsize = max(1, (hi-lo)/(n-1))` — no gap can fall *entirely inside* one bucket, which means the maximum gap must **straddle a bucket boundary**. Drop each value into bucket `(x-lo)/bsize`, keeping only that bucket's running **min and max**; empty buckets are skipped. Sweep the non-empty buckets left to right, and the answer is the largest `curBucketMin - prevBucketMax`. O(n) time, O(n) buckets, no comparison sort.

## Kāra features exercised

- **Three parallel `Vec`s** (`used: Vec[bool]`, `bmin`/`bmax: Vec[i64]`) sized to the bucket count and filled with a `push` loop.
- **Data-dependent scatter** — `bmin[idx] = min_i64(bmin[idx], x)` with a computed index, the part that is *not* auto-vectorizable and drives the benchmark.
- **`Slice[i64]` from `Array[i64, N]`** including the empty-array `Array[i64, 0]` case (`n < 2` early-out).

## Benchmarks

> **Machine.** Container-only reference run — a shared **x86-64 Linux cloud container** ([`bench/results.container-x86.json`](bench/results.container-x86.json)); canonical Apple-M5 numbers (`bench/results.json`) are pending a maintainer run. Absolute times are noisy on the shared host; **within-run cross-language ratios are the signal.**

Compute-bound, seq-only kata. The workload is **build-once + punch**: fill `N = 1_000_000` deterministic LCG values, then run `maximum_gap` `K = 30` times, perturbing one element each round so the pure function can't be hoisted. All five mirrors print the same sink (`462870`). The dominant cost is the O(n) bucket allocation + data-dependent scatter, so this doubles as an **allocator + memory-scatter** benchmark.

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Codegen ahead of C/Rust/Go on the allocation-bound kernel

Container snapshot, hyperfine `--warmup 5 --runs 30`:

| Run | Mean ± σ | vs kāra |
|---|---|---|
| **kāra `maximum_gap` (codegen)** | **1.443 ± 0.156 s** | — |
| c `maximum_gap` (`clang -O3`) | 1.972 ± 0.171 s | kāra 1.37× ahead |
| rust `maximum_gap` (`-O`, wrapping) | 2.313 ± 1.19 s | kāra 1.60× ahead (rust noisy) |
| rust `maximum_gap` (`overflow-checks=on`) | 2.073 ± 0.166 s | kāra 1.44× ahead |
| go `maximum_gap` | 2.744 ± 0.649 s | kāra 1.90× ahead |
| python `maximum_gap` | 30.79 ± 0.82 s | (scale only; 3 runs) |

Here Kāra's codegen is **fastest** — ahead of `clang -O3`. The kernel repeatedly allocates three ~1M-element buckets and scatters into them; the measured cost is dominated by **allocation + memory traffic**, where Kāra's allocator (reused arenas across the K calls) edges out C's `malloc`/`calloc` (higher system time — note C's `System: 63 ms` vs Kāra's `18 ms`) and Go's GC. This is a workload-specific win, not a general claim: for the tight-arithmetic kernels elsewhere in this corpus (e.g. [#152](../152-maximum-product-subarray/)) C stays ahead. Python is a **scale reference only** (run 3× — it is ~20× slower here because the per-bucket work is pathological under CPython).

## Running

```bash
karac run   maximum_gap.kara
karac build maximum_gap.kara && ./maximum_gap
python3 maximum_gap.py
diff <(karac run maximum_gap.kara) <(python3 maximum_gap.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. (The full-scale bench kernel is too slow under the tree-walk interpreter to A/B at `N=1M`; the small correctness cases above cover the interpreter surface, and the JIT matches the compiled sink.)
