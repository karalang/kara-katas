# 168. Excel Sheet Column Title

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/excel-sheet-column-title](https://leetcode.com/problems/excel-sheet-column-title/)

Convert a 1-based column number to its Excel column title.

```
1  ->  "A"       26 ->  "Z"        27 ->  "AA"
28 ->  "AB"      701 -> "ZY"       2147483647 -> "FXSHRXW"
```

**Constraints:** `1 ≤ columnNumber ≤ 2³¹-1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **bijective base-26** ★ | [`column_title.kara`](column_title.kara) ✓ | [`column_title.py`](column_title.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

This looks like base-26 but there is **no zero digit** — `A` is 1, not 0, and `Z` is 26. That makes it *bijective* base-26. The fix is a single `-1` per digit: subtract one to shift the range `1..26` down to `0..25` (so `0→A … 25→Z`), take `x % 26` as the digit, then `x /= 26`. Digits come out least-significant first, so collect them and reverse. The `2147483647 → FXSHRXW` case confirms the `i64` arithmetic carries all 32 bits cleanly.

## Kāra features exercised

- **`char.try_from(u8)` → `Result[char, _]`** — Kāra forbids a bare `u8 as char` cast (not every integer is a valid scalar), so the digit-to-letter step goes through the checked conversion and a `match Ok/Err`.
- **`String.push(char)`** to assemble the reversed title, and **`Vec[char]`** to buffer the least-significant-first digits.
- **Bijective base-26 loop** — the `x -= 1` before `% 26` / `/= 26` is the whole trick.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`21802156690`). Workload: bijective base-26 column_title conversion over the range 1..50M (subtract-1/mod-26/div-26 with data-dependent trip count and loop-carried remainder, non-vectorizing); sink = checksum of produced letter byte values.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Go | 406.2 ms | 0.88× |
| Rust `-O` | 444.8 ms | 0.96× |
| **Kāra (codegen)** | 461.1 ms | 1.00× |
| C `clang -O3` | 463.8 ms | 1.01× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 487.7 ms | 1.06× |
| Python (scale lane) | 32.54 s | 70.56× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   column_title.kara
karac build column_title.kara && ./column_title
python3 column_title.py
diff <(karac run column_title.kara) <(python3 column_title.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
