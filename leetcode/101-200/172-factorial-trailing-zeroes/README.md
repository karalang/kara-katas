# 172. Factorial Trailing Zeroes

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/factorial-trailing-zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/)

Return the number of trailing zeros in `n!`.

```
3     ->  0    (3! = 6)
5     ->  1    (5! = 120)
100   ->  24
10000 ->  2499
```

**Constraints:** `0 ≤ n ≤ 10⁴`. Follow-up: do it in **logarithmic** time.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **count factors of 5** ★ | [`trailing_zeroes.kara`](trailing_zeroes.kara) | [`trailing_zeroes.py`](trailing_zeroes.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A trailing zero is a factor of `10 = 2·5`. In `n!` the factors of 2 vastly outnumber the factors of 5, so the number of trailing zeros equals the number of times **5** divides `n!`: `⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …` (every multiple of 5 contributes one 5, every multiple of 25 an extra one, etc.). Summing via `m = n/5, m/5, …` keeps each intermediate **smaller than `n`**, so it's O(log₅ n) and — importantly under Kāra's checked arithmetic — never overflows, unlike accumulating the powers `5, 25, 125, …` directly.

## Kāra features exercised

- **Integer division truncation** (`n / 5` floors toward zero for non-negative `n`) driving the divide-down loop.
- **Overflow-safe formulation** — the shrink-`m` loop sidesteps the overflow that the power-accumulation variant would trip under Kāra's default-checked arithmetic.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`153124810625000`). Workload: trailing_zeroes summed over n in 0..35M (repeated /5 factor-count loop; scalar, non-vectorizing).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 282.8 ms | 0.85× |
| Rust `-O` | 311.9 ms | 0.94× |
| **Kāra (codegen)** | 331.5 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 342.4 ms | 1.03× |
| Go | 395.4 ms | 1.19× |
| Python (scale lane) | 21.54 s | 64.96× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   trailing_zeroes.kara
karac build trailing_zeroes.kara && ./trailing_zeroes
python3 trailing_zeroes.py
diff <(karac run trailing_zeroes.kara) <(python3 trailing_zeroes.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
