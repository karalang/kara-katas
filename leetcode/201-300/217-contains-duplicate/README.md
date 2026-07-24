# 217. Contains Duplicate

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Hash Table · Set &nbsp;·&nbsp; **Source:** [leetcode.com/problems/contains-duplicate](https://leetcode.com/problems/contains-duplicate/)

Return `true` if any value appears **at least twice** in the array, and `false` if every element is distinct.

```
[1,2,3,1]              ->  true
[1,2,3,4]              ->  false
[1,1,1,3,3,4,3,2,4,2]  ->  true
```

**Constraints:** `1 ≤ nums.length ≤ 10⁵`, `-10⁹ ≤ nums[i] ≤ 10⁹`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **hash-set membership** ★ | [`contains_duplicate.kara`](contains_duplicate.kara) | [`contains_duplicate.py`](contains_duplicate.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Walk the array once, keeping a `Set[i64]` of the values seen so far. Before inserting each value, check whether it is already present — the first time that check succeeds you've found a repeat and can return `true` immediately. If the scan completes with every value inserted exactly once, there are no duplicates. O(n) time, O(n) space.

## Kāra features exercised

- **`Set[i64]`** — `Set.new()`, `contains(x) → bool` membership test, and `insert(x)`, the hash-set primitive (Set lowers to `Map[T, ()]` in the runtime).
- **Early-exit scan over a `Slice[i64]`** — returns on the first repeat rather than counting everything.


## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`27979`). Workload: hash-set contains_duplicate over 239200 sliding width-800 windows of a PRNG array; count of windows with a duplicate.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 228.5 ms | 0.03× |
| Rust `-O` | 7.79 s | 0.94× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 7.80 s | 0.95× |
| **Kāra (codegen)** | 8.25 s | 1.00× |
| Go | 12.03 s | 1.46× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   contains_duplicate.kara
karac build contains_duplicate.kara && ./contains_duplicate
python3 contains_duplicate.py
diff <(karac run contains_duplicate.kara) <(python3 contains_duplicate.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
