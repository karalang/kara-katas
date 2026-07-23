# 213. House Robber II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/house-robber-ii](https://leetcode.com/problems/house-robber-ii/)

Houses are arranged in a **circle**. Robbing two adjacent houses trips the alarm, and because the layout is circular the **first and last houses are also adjacent**. Return the maximum amount that can be robbed without alerting the police.

```
[2,3,2]    ->  3    (rob house 1; can't take both ends)
[1,2,3,1]  ->  4    (houses 0 and 2)
[5]        ->  5
```

**Constraints:** `1 ≤ nums.length ≤ 100`, `0 ≤ nums[i] ≤ 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two linear DP runs** ★ | [`house_robber_ii.kara`](house_robber_ii.kara) | [`house_robber_ii.py`](house_robber_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The only new wrinkle over [#198](../../101-200/198-house-robber/) is that the ends touch. Since you can never rob both the first and last house, split into two ordinary (non-circular) House Robber problems: one that **excludes the last house** (rob within `[0, n-1)`) and one that **excludes the first** (rob within `[1, n)`). The circular optimum is whichever linear run pays more.

Each linear run is the O(1)-space rolling DP: sweep left to right holding the best total up to the previous two houses; at each house choose to **skip** it (carry the running best) or **take** it (best from two houses back plus this house). Single-house and empty inputs short-circuit before the split. O(n) time, O(1) space.

## Kāra features exercised

- **`Slice[i64]` with an explicit `[lo, hi)` window** — the two runs reuse one `rob_linear` over index ranges instead of allocating sub-slices, so no copying and no slice-of-slice.
- **`if`-expression in value position** — `let next = if take > cur { take } else { cur }` folds the max inline.
- **Rolling two-variable DP** — `prev` / `cur` advance in lockstep; overflow-checked `i64` accumulation.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`76367382296`). Workload: one 100k positive-value array built once; run the circular House Robber DP over 130k sliding windows (loop-carried max recurrence); sink = sum of takes.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 361.8 ms | 0.57× |
| Rust `-O` | 398.4 ms | 0.63× |
| Go | 460.9 ms | 0.72× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 592.6 ms | 0.93× |
| **Kāra (codegen)** | 636.5 ms | 1.00× |
| Python (scale lane) | 33.20 s | 52.15× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   house_robber_ii.kara
karac build house_robber_ii.kara && ./house_robber_ii
python3 house_robber_ii.py
diff <(karac run house_robber_ii.kara) <(python3 house_robber_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
