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

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`4314388048384`). Workload: triple-reversal in-place rotate of a 30000-element PRNG array x 4000 fresh-PRNG-amount passes, loop-carried polynomial checksum folded each pass.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 237.9 ms | 0.83× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 275.4 ms | 0.96× |
| **Kāra (codegen)** | 287.2 ms | 1.00× |
| C `clang -O3` | 309.1 ms | 1.08× |
| Go | 317.0 ms | 1.10× |
| Python (scale lane) | 23.41 s | 81.50× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   rotate_array.kara
karac build rotate_array.kara && ./rotate_array
python3 rotate_array.py
diff <(karac run rotate_array.kara) <(python3 rotate_array.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
