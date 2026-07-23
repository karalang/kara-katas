# 201. Bitwise AND of Numbers Range

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/bitwise-and-of-numbers-range](https://leetcode.com/problems/bitwise-and-of-numbers-range/)

Return the bitwise **AND** of all integers in the inclusive range `[left, right]`.

```
5, 7            ->  4     (5 & 6 & 7)
12, 15          ->  12
1, 2147483647   ->  0
```

**Constraints:** `0 ≤ left ≤ right ≤ 2³¹-1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **common binary prefix** ★ | [`range_and.kara`](range_and.kara) | [`range_and.py`](range_and.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

ANDing the whole range one number at a time is O(range) — but the answer is just the **common binary prefix** of `left` and `right`. At any bit position where they differ, the lower bits sweep through every combination as you count from `left` to `right`, so that bit is `0` for at least one value and ANDs away. Shift both numbers right until they agree (stripping the differing low bits, counting the shifts), then shift the shared prefix back into place. O(log) — at most 31 shifts.

## Kāra features exercised

- **Bitwise shifts on `i64`** — `>>` to strip low bits, `<<` to restore the prefix — the whole kernel, no arithmetic that could overflow under Kāra's checked defaults.
- **Convergence loop** on `lo < hi` counting a shift amount.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`7162597134924416`). Workload: range_and over 20M PRNG [lo,hi] pairs (data-dependent bit-shift kernel).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 477.5 ms | 0.86× |
| Rust `-O` | 479.8 ms | 0.86× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 500.7 ms | 0.90× |
| **Kāra (codegen)** | 556.1 ms | 1.00× |
| Go | 614.8 ms | 1.11× |
| Python (scale lane) | 54.70 s | 98.36× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   range_and.kara
karac build range_and.kara && ./range_and
python3 range_and.py
diff <(karac run range_and.kara) <(python3 range_and.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
