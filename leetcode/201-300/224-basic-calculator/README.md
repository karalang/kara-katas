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

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-27 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 196.6 ms | 0.92× |
| **Kāra (codegen)** | 213.5 ms | 1.00× |
| Rust `-O` | 213.9 ms | 1.00× |
| Go | 223.9 ms | 1.05× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 229.4 ms | 1.07× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   basic_calculator.kara
karac build basic_calculator.kara && ./basic_calculator
python3 basic_calculator.py
diff <(karac run basic_calculator.kara) <(python3 basic_calculator.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
