# 189. Rotate Array

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Math · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/rotate-array](https://leetcode.com/problems/rotate-array/)

Rotate an array to the **right** by `k` steps, **in place**, using O(1) extra space.

```
[1,2,3,4,5,6,7], k=3  ->  [5,6,7,1,2,3,4]
[-1,-100,3,99],  k=2  ->  [3,99,-1,-100]
[1,2,3],         k=4  ->  [3,1,2]   (k ≡ 1 mod n)
```

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ k ≤ 10⁵`. The O(1)-space in-place solution is the follow-up.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **triple reversal** ★ | [`rotate_array.kara`](rotate_array.kara) | [`rotate_array.py`](rotate_array.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Reversing the whole array moves the last `k` elements to the front — but backwards. Reversing each of the two blocks (`[0, k)` and `[k, n)`) restores their internal order:

```
[1,2,3,4,5,6,7]  reverse all →  [7,6,5,4,3,2,1]
                 reverse [0,3) → [5,6,7|4,3,2,1]
                 reverse [3,7) → [5,6,7|1,2,3,4]
```

Three linear passes, no auxiliary array, O(1) extra space. `k` is reduced mod `n` first (a full rotation is a no-op).

## Kāra features exercised

- **In-place `Vec[i64]` reversal** — `reverse_range` does converging two-pointer index swaps; `rotate` calls it three times, exercising **bounds-checked index-assign** on every write.
- **`k % n` normalization** with the `kk = 0` edge (a zero-width reverse-range is a clean no-op — `while i < j` with `hi = -1`).
- **`mut ref Vec[i64]` parameter** with the `mut` call-site marker on the fresh binding.

> Ships correctness-only (no benchmark): the triple reversal is **memory-bandwidth-bound** in-place data movement, so a sequential cross-language timing would be dominated by DRAM throughput rather than a codegen difference. The purely-ALU compute story lives in the bit-manipulation katas ([#191](../191-number-of-1-bits/)).
>
> **Note (2026-11-01):** this kata now does ship a benchmark (§ Benchmarks below); the bandwidth caveat above still applies to reading its numbers.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`4314388048384`). Workload: triple-reversal in-place rotate of a 30000-element PRNG array x 4000 fresh-PRNG-amount passes, loop-carried polynomial checksum folded each pass.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (0.9.0-dev.14057, v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 180.6 ± 1.2 ms | 0.95× |
| Rust `-O` | 183.5 ± 2.2 ms | 0.97× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 184.0 ± 2.9 ms | 0.97× |
| **Kāra (codegen)** | 189.9 ± 2.7 ms | 1.00× |
| Go | 191.0 ± 3.4 ms | 1.01× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Kāra is fourth of five, all within 6%: **1.03×** behind both Rust builds, **1.05×** behind C, and at parity with Go (**0.99×**). Against the previous feed (2026-07-27, legacy backend `karac 0.1.0`: 1.04× Rust, 1.04× C, 0.99× Go) every ratio moved by 1% or less, so flat. Every comparator ran 13–14% slower this session (machine state), so compare the ratios, not the milliseconds.

Binary size: C 32.7 KiB, **kāra 295.8 KiB** (302,880 B), Rust 455.7 KiB, Go 2.38 MiB; every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's was 34,208 B on 2026-07-27), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: C 1.25 MiB, **kāra 1.27 MiB**, Rust 1.28 MiB, Go 2.94 MiB. Compile-cold: clang 49.5 ms < rustc 93.3 ms < **karac 118.1 ms** (2.39× clang, 1.27× rustc); compile peak RSS clang 2.6 MiB, rustc 27.4 MiB, **karac 55.8 MiB**.

## Running

```bash
karac run   rotate_array.kara
karac build rotate_array.kara && ./rotate_array
python3 rotate_array.py
diff <(karac run rotate_array.kara) <(python3 rotate_array.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
