# 166. Fraction to Recurring Decimal

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table · Math · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/fraction-to-recurring-decimal](https://leetcode.com/problems/fraction-to-recurring-decimal/)

Given `numerator` and `denominator`, return the fraction as a decimal string. If the fractional part **repeats**, wrap the repeating block in parentheses.

```
1/2   ->  "0.5"        2/1   ->  "2"
2/3   ->  "0.(6)"      4/333 ->  "0.(012)"
1/6   ->  "0.1(6)"     22/7  ->  "3.(142857)"
-50/8 ->  "-6.25"      1/-3  ->  "-0.(3)"
```

**Constraints:** `-2³¹ ≤ numerator, denominator ≤ 2³¹-1`, `denominator ≠ 0`. (This kata uses `i64` throughout so the intermediate `rem*10` never overflows.)

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **long division + remainder map** ★ | [`fraction_decimal.kara`](fraction_decimal.kara) ✓ | [`fraction_decimal.py`](fraction_decimal.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Emit the sign and integer part, then do **long division** on the fractional part: repeatedly multiply the remainder by 10, the quotient digit is `rem*10 / d`, and the new remainder is `rem*10 % d`. The trick for the repeating block: a remainder that **recurs** means every digit from its first appearance onward repeats forever. So record each remainder's digit position in a `Map[i64, i64]`; when a remainder repeats, the recorded position is where the parenthesis opens. Termination is guaranteed — there are only `d` possible remainders.

## Kāra features exercised

- **`Map[i64, i64]` remainder → digit-position** with `.get` → `Option` matched by `match`, and the `insert` return discarded via `let _ = …`.
- **`Vec[i64]` digit accumulation** then a second pass to assemble the string with the parenthesised cycle.
- **Sign logic** via boolean `and`/`or` (`(num < 0 and den > 0) or (num > 0 and den < 0)`), and `f"{d}"` digit interpolation.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`215566009`). Workload: 500K PRNG numerator/denominator pairs (den 2..1024) through long-division digit generation (variable-divisor idiv/mod + seen-remainder Map, non-vectorizing); sink = checksum of fractional digits. NOTE: C hand-rolls an epoch-stamped table in place of the Map (identical digit stream).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 436.9 ms | 0.17× |
| **Kāra (codegen)** | 2.53 s | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 2.75 s | 1.09× |
| Rust `-O` | 2.81 s | 1.11× |
| Go | 4.93 s | 1.95× |
| Python (scale lane) | 9.19 s | 3.63× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   fraction_decimal.kara
karac build fraction_decimal.kara && ./fraction_decimal
python3 fraction_decimal.py
diff <(karac run fraction_decimal.kara) <(python3 fraction_decimal.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
