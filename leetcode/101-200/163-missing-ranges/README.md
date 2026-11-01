# 163. Missing Ranges

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/missing-ranges](https://leetcode.com/problems/missing-ranges/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given a **sorted** array `nums` of distinct integers all within the inclusive bounds `[lower, upper]`, return the smallest sorted list of ranges that cover **every number in `[lower, upper]` missing from `nums`**. A range prints as `"a"` for a single number, else `"a->b"`.

```
nums=[0,1,3,50,75], lower=0, upper=99  ->  2, 4->49, 51->74, 76->99
nums=[],            lower=1, upper=1   ->  1
nums=[-1,0,1,2],    lower=-1, upper=2  ->  (nothing missing)
```

**Constraints:** `nums` sorted ascending, distinct, all in `[lower, upper]`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **cursor sweep + upper sentinel** ★ | [`missing_ranges.kara`](missing_ranges.kara) ✓ | [`missing_ranges.py`](missing_ranges.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Track `prev` — the last number accounted for — initialised to `lower - 1`. Sweep each element, plus a virtual `upper + 1` sentinel at the end. Whenever the gap `cur - prev` is at least 2, the numbers strictly between them are missing, so emit the range `[prev+1, cur-1]`; then advance `prev = cur`. The sentinel makes the trailing gap up to `upper` fall out of the same rule with no special case. O(n) time.

## Kāra features exercised

- **`Vec[String]` accumulation** — each range is formatted and pushed; the caller joins them with `", "` via `String.push_str`. Exercises heap-`String`-element `Vec` growth and cleanup (the reassign/leak class this corpus stress-tests) — verified valgrind-clean.
- **`f"{lo}->{hi}"` interpolation** and the `"a"` single-number branch.
- **`if`-expression** for the sentinel: `let cur = if i < n { nums[i] } else { upper + 1 }`.
- **`Slice[i64]` parameter** fed from `Array[i64, N]` literals, including the empty-array `Array[i64, 0]` case.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`320331567536794`). Workload: build-once 1M-elem sorted PRNG array + 120K sliding-window missing-ranges sweeps (loop-carried prev, data-dependent gap>=2 branch, non-vectorizing); sink = ranges count + endpoint checksum.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 58.1 ms | 0.10× |
| Rust `-O` | 59.2 ms | 0.10× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 548.2 ms | 0.91× |
| Go | 552.1 ms | 0.91× |
| **Kāra (codegen)** | 604.7 ms | 1.00× |

The ~10× gap (10.21× behind `rustc -O`, 10.41× behind C) is to plain `rustc -O` and C, which vectorise this loop. Against equal-safety Rust (`-C overflow-checks=on`) Kāra is 1.10× behind, and Go is in the same range (1.10×). That is the in-loop overflow check blocking vectorisation (kara `B-2026-08-16-11`, legacy ledger, wontfix): the checked Rust build pays the same ~10×. Flat against the 2026-07-28 feed (9.49× behind `rustc -O`); the equal-safety and Go ratios slipped from Kāra marginally ahead (0.98× / 0.95×) to 1.10× behind. Binary size: the MIR Kāra binary is 302,880 bytes, where the legacy backend's was ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)).

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   missing_ranges.kara
karac build missing_ranges.kara && ./missing_ranges
python3 missing_ranges.py
diff <(karac run missing_ranges.kara) <(python3 missing_ranges.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
