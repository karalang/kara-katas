# 231. Power of Two

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/power-of-two](https://leetcode.com/problems/power-of-two/)

Return `true` iff `n` is a power of two (`n == 2^x` for some `x ≥ 0`).

```
1  ->  true    (2^0)
16 ->  true
3  ->  false
0  ->  false
```

**Constraints:** `-2³¹ ≤ n ≤ 2³¹−1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **`n & (n-1)` bit trick** ★ | [`power_of_two.kara`](power_of_two.kara) | [`power_of_two.py`](power_of_two.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A positive power of two has exactly **one** set bit. Subtracting 1 flips that bit off and turns every lower bit on — `1000 → 0111` — so the two share no bits and `n & (n - 1) == 0`. Any other positive number has at least two set bits, and clearing the lowest one with `n & (n - 1)` leaves something non-zero. Non-positive `n` is never a power of two, so it's rejected up front. O(1), no loop.

## Kāra features exercised

- **Bitwise AND and subtraction on `i64`** — `n & (n - 1)`, the single-expression test, including the `2^31` / `2^30` cases well within `i64` range.
- **Guard-then-return** — the `n <= 0` early return keeps the bit test on the domain where it's meaningful.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`1269530`). Workload: is_power_of_two over a 130M-step LCG stream, masked to 0..1024 (loop-carried PRNG, count of powers).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 177.5 ms | 0.81× |
| Rust `-O` | 188.3 ms | 0.86× |
| **Kāra (codegen)** | 218.3 ms | 1.00× |
| C `clang -O3` | 232.2 ms | 1.06× |
| Go | 241.5 ms | 1.11× |
| Python (scale lane) | 32.86 s | 150.49× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   power_of_two.kara
karac build power_of_two.kara && ./power_of_two
python3 power_of_two.py
diff <(karac run power_of_two.kara) <(python3 power_of_two.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
