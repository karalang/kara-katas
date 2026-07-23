# 136. Single Number

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Bit Manipulation · Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/single-number](https://leetcode.com/problems/single-number/)

Every element appears **exactly twice** except for one, which appears once. Find that one — in `O(n)` time and `O(1)` extra space.

```
[4,1,2,1,2]  ->  4
[2,2,1]      ->  1
[-7]         -> -7
```

**Constraints:** `1 ≤ n ≤ 3·10⁴`, `-3·10⁴ ≤ nums[i] ≤ 3·10⁴`, every element appears twice except one which appears once.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **XOR-fold** ★ | [`single_number.kara`](single_number.kara) ✓ | [`single_number.py`](single_number.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. Zero diagnostics, valgrind-clean.

## The mechanism

XOR is associative, commutative, self-inverse (`a ^ a == 0`), and has `0` as identity (`x ^ 0 == x`). Fold `^` across the whole array and every value that appears twice cancels to `0`, leaving only the lone element. Correct for negative values too (two's-complement bit patterns XOR identically).

## Kāra features exercised

- **`ref Vec[i64]` read-only parameter** — the solver borrows `nums` without taking ownership (the idiomatic read-only-function form; sibling of #137's helpers).
- **`^` on `i64`** — the sequential bitwise-XOR fold, interp == build == Python.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`27831520`). Workload: XOR-fold of a 280001-element pairs+unique array x 3400 passes (build-once + punch); sink=fold total.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 298.1 ms | 0.99× |
| **Kāra (codegen)** | 299.8 ms | 1.00× |
| Rust `-O` | 301.5 ms | 1.01× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 310.4 ms | 1.04× |
| Go | 645.2 ms | 2.15× |
| Python (scale lane) | 42.24 s | 140.91× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   single_number.kara
karac build single_number.kara && ./single_number
python3 single_number.py
diff <(karac run single_number.kara) <(python3 single_number.py) && echo OK
```

## Notes

The Easy predecessor of [#137 Single Number II](../137-single-number-ii/). Where #137 needs a per-bit mod-3 counter, #136 is the pure XOR-cancellation trick — a clean one-operator fold over `ref Vec[i64]`.
