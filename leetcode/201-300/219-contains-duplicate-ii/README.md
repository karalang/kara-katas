# 219. Contains Duplicate II

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Hash Table · Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/contains-duplicate-ii](https://leetcode.com/problems/contains-duplicate-ii/)

Return `true` if there are two **distinct** indices `i, j` with `nums[i] == nums[j]` and `|i - j| ≤ k` — i.e. does any value repeat within a window of width `k`?

```
[1,2,3,1],     k=3  ->  true    (indices 0, 3 — gap 3)
[1,0,1,1],     k=1  ->  true    (indices 2, 3 — gap 1)
[1,2,3,1,2,3], k=2  ->  false   (nearest repeat is gap 3)
```

**Constraints:** `1 ≤ nums.length ≤ 10⁵`, `-10⁹ ≤ nums[i] ≤ 10⁹`, `0 ≤ k ≤ 10⁵`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **last-index hash map** ★ | [`contains_duplicate_ii.kara`](contains_duplicate_ii.kara) | [`contains_duplicate_ii.py`](contains_duplicate_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Keep a `Map[i64, i64]` from each value to the **most recent** index where it appeared. Walk left to right; at position `i`, if the current value is already in the map and `i - last[x] ≤ k`, a qualifying pair exists — return `true`. Otherwise overwrite `last[x] = i` and move on.

Storing only the latest index (rather than all of them) is sufficient: for a future match, the nearest previous occurrence is always the newest one, so an older index could never satisfy the gap when the newest one doesn't. O(n) time, O(n) space.

## Kāra features exercised

- **`Map[i64, i64]` value → index** with `get(x) → Option` (matched) and an overwriting `insert` whose `Option` result is discarded (`let _ = last.insert(x, i)`).
- **Early-exit scan over `Slice[i64]`** — returns on the first in-window repeat.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`16323`). Workload: value->last-index hash map counting nearby duplicates over a 1M PRNG array, swept for k in 1..40; sum of hits.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 465.2 ms | 0.62× |
| **Kāra (codegen)** | 753.5 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 1.68 s | 2.23× |
| Rust `-O` | 1.71 s | 2.27× |
| Go | 2.20 s | 2.92× |
| Python (scale lane) | 13.54 s | 17.97× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   contains_duplicate_ii.kara
karac build contains_duplicate_ii.kara && ./contains_duplicate_ii
python3 contains_duplicate_ii.py
diff <(karac run contains_duplicate_ii.kara) <(python3 contains_duplicate_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
