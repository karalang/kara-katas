# 198. House Robber

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/house-robber](https://leetcode.com/problems/house-robber/)

Rob the maximum total from a row of houses **without robbing two adjacent ones** (adjacent break-ins trip the alarm).

```
[1,2,3,1]     ->  4    (1 + 3)
[2,7,9,3,1]   ->  12   (2 + 9 + 1)
[100,1,100]   ->  200
```

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ nums[i] ≤ 400`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **rolling two-variable DP** ★ | [`house_robber.kara`](house_robber.kara) | [`house_robber.py`](house_robber.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

At each house there are two choices: **skip** it (keep the best total up to the previous house, `prev`) or **rob** it (its value plus the best from two houses back, `prev2`, since the immediate neighbour must be skipped). So `cur = max(prev, prev2 + nums[i])`, then slide the window (`prev2 = prev; prev = cur`). Only the two trailing maxima matter, so it runs in O(n) time and **O(1) space** — no DP array. The final `prev` is the answer.

## Kāra features exercised

- **O(1)-space rolling DP** — two scalar carries (`prev`, `prev2`) across a single `Slice[i64]` scan, the canonical linear-DP compression.
- **`max` helper** lowering to a branchless select.
- **Empty-input edge** — `Array[i64, 0]` yields `0` (the loop never runs, `prev` stays 0).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`130976291209`). Workload: O(1)-space rob() DP over a 5000-house PRNG array x 90000 punched passes (loop-carried max recurrence, one house flipped per pass).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 309.7 ms | 0.76× |
| C `clang -O3` | 311.9 ms | 0.77× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 340.8 ms | 0.84× |
| Go | 375.9 ms | 0.93× |
| **Kāra (codegen)** | 404.9 ms | 1.00× |
| Python (scale lane) | 29.90 s | 73.85× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   house_robber.kara
karac build house_robber.kara && ./house_robber
python3 house_robber.py
diff <(karac run house_robber.kara) <(python3 house_robber.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
