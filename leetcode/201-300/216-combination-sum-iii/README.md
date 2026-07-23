# 216. Combination Sum III

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Backtracking · Combinations &nbsp;·&nbsp; **Source:** [leetcode.com/problems/combination-sum-iii](https://leetcode.com/problems/combination-sum-iii/)

Find **all** combinations of exactly `k` distinct digits from `1..9` that sum to `n`. Each digit is used at most once; each combination is listed in ascending order.

```
k=3, n=7   ->  [[1,2,4]]
k=3, n=9   ->  [[1,2,6],[1,3,5],[2,3,4]]
k=4, n=1   ->  []
```

**Constraints:** `2 ≤ k ≤ 9`, `1 ≤ n ≤ 60`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **backtracking with pruning** ★ | [`combination_sum_iii.kara`](combination_sum_iii.kara) | [`combination_sum_iii.py`](combination_sum_iii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Depth-first search over **ascending** digits. The state is the next digit to consider (`start`), how many digits remain to place (`k`), and the remaining sum. At each level try each digit `d` from `start` to `9`, append it to the running path, and recurse with `start = d+1`, `k-1`, `remaining-d`; undo the append (`pop`) before trying the next digit. A leaf with `k == 0` **and** `remaining == 0` is a valid combination.

Two prunes keep it tight: digits strictly increase (so `start = d+1` avoids duplicates and enforces ascending order), and once `d` exceeds the remaining sum every later digit is too big as well, so the level stops early. Emitting digits in order makes the whole result set come out lexicographically sorted for free.

## Kāra features exercised

- **Backtracking with `Vec.push` / `Vec.pop`** — one shared `path` buffer grown and shrunk in place across the recursion (`let _ = path.pop()` discards the returned `Option`).
- **Two `mut ref` parameters through recursion** — `path: mut ref Vec[i64]` and `results: mut ref Vec[Vec[i64]]`; the top-level call marks the fresh owned bindings (`backtrack(1, k, n, mut path, mut results)`) while the recursive calls forward the already-`mut ref` bindings unmarked.
- **Snapshot-on-hit** — a valid path is copied into a fresh owned `Vec[i64]` before being pushed into `results`, so the still-mutating shared buffer is never aliased into the output (`Vec[Vec[i64]]` ownership, valgrind-verified).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`2298771`). Workload: ascending-digit backtracking count over digits 1..36, summed across a k in 1..6 x n in 1..150 grid.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 442.5 ms | 0.97× |
| C `clang -O3` | 443.5 ms | 0.97× |
| **Kāra (codegen)** | 457.7 ms | 1.00× |
| Go | 496.6 ms | 1.09× |
| Rust `-O` | 516.3 ms | 1.13× |
| Python (scale lane) | 17.77 s | 38.83× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   combination_sum_iii.kara
karac build combination_sum_iii.kara && ./combination_sum_iii
python3 combination_sum_iii.py
diff <(karac run combination_sum_iii.kara) <(python3 combination_sum_iii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
