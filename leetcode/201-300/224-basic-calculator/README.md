# 224. Basic Calculator

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String · Stack · Math · Parsing &nbsp;·&nbsp; **Source:** [leetcode.com/problems/basic-calculator](https://leetcode.com/problems/basic-calculator/)

Evaluate a string expression made of non-negative integers, `+`, `-`, `(`, `)`, and spaces. There is **no** multiplication or division — only addition, subtraction, and parenthesised grouping (including unary minus, e.g. `-(3+4)`).

```
"1 + 1"                  ->  2
"(1+(4+5+2)-3)+(6+8)"    ->  23
"- (3 + (4 + 5))"        ->  -12
```

**Constraints:** `1 ≤ |s| ≤ 3·10⁵`; the expression is always valid.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **sign-stack byte scan** ★ | [`basic_calculator.kara`](basic_calculator.kara) | [`basic_calculator.py`](basic_calculator.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Scan the bytes left to right holding a running `result` and the `sign` (+1 / −1) that applies to the next term. A digit run parses into a number and folds in as `result += sign * num`. Because there's no precedence to juggle, that's the entire arithmetic core.

Parentheses are the only twist, and a stack handles them: `(` starts a fresh sub-expression, so the current `result` and `sign` are **pushed** and both reset; `)` finishes the group and folds the sub-result back with the sign that preceded it — `result = saved_result + saved_sign * result`. Because `sign` resets to +1 inside each new group, a unary minus like `-(…)` is just a `-` sign applied to a group that starts from 0. O(n), one pass.

## Kāra features exercised

- **`s.bytes()` ASCII scan** — O(1) byte indexing, digit classification with `b'0'..b'9'` byte literals, and `bytes[i] as i64 - b'0' as i64` to accumulate a number.
- **`Vec[i64]` as a stack** — `push` a `(result, sign)` pair and `pop` (→ `Option`, matched) on `)`.
- **Inner digit-run loop** that advances the shared cursor `i`, so the outer loop deliberately skips its own increment on the digit branch.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`659731447`). Workload: calculate() over one big PRNG +/-/paren expression run K times (byte-scan + stack, data-dependent branch).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 579.8 ms | 0.89× |
| Go | 636.7 ms | 0.98× |
| **Kāra (codegen)** | 652.1 ms | 1.00× |
| Rust `-O` | 659.2 ms | 1.01× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 660.6 ms | 1.01× |
| Python (scale lane) | 18.80 s | 28.82× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   basic_calculator.kara
karac build basic_calculator.kara && ./basic_calculator
python3 basic_calculator.py
diff <(karac run basic_calculator.kara) <(python3 basic_calculator.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
