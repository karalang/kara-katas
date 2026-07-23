# 220. Contains Duplicate III

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Sliding Window · Bucketing · Ordered Set &nbsp;·&nbsp; **Source:** [leetcode.com/problems/contains-duplicate-iii](https://leetcode.com/problems/contains-duplicate-iii/)

Return `true` if there are two **distinct** indices `i, j` with `|i - j| ≤ indexDiff` **and** `|nums[i] - nums[j]| ≤ valueDiff`.

```
[1,2,3,1],       k=3, t=0  ->  true    (the two 1s, gap 3, value diff 0)
[1,5,9,1,5,9],   k=2, t=3  ->  false
[-3,3,0,10],     k=3, t=3  ->  true    (-3 and 0, value diff 3)
```

**Constraints:** `2 ≤ nums.length ≤ 10⁵`, `-10⁹ ≤ nums[i] ≤ 10⁹`, `1 ≤ indexDiff ≤ nums.length`, `0 ≤ valueDiff ≤ 10⁹`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **bucketing sliding window** ★ | [`contains_duplicate_iii.kara`](contains_duplicate_iii.kara) | [`contains_duplicate_iii.py`](contains_duplicate_iii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Partition the number line into buckets of width `t+1`. Two numbers in the **same** bucket differ by at most `t` — an instant hit. Two numbers within `t` of each other can otherwise only straddle a bucket boundary, so they live in **adjacent** buckets; those two neighbours are checked directly.

Slide a window of the last `k` indices, keeping one representative per occupied bucket in a `Map[i64, i64]` (bucket id → value; a bucket can hold at most one live value, else we'd already have returned). For each `x`: check its own bucket, then the two neighbours; record `x`; then evict the value that just left the window (`nums[i-k]`). Bucket ids use **floor** division so negative numbers bucket consistently — Kāra's `/` truncates toward zero, so negatives are shifted (`(x+1)/w - 1`) to recover the true floor. O(n) time, O(min(n,k)) space.

## Kāra features exercised

- **`Map[i64, i64]` as a bucket table** — `get → Option`, overwriting `insert`, and `remove` (both discarded via `let _ = …`) to add and evict window members.
- **Floor division from truncating `/`** — the negative-number shift `(x + 1) / w - 1`, a portable idiom the mirror replicates exactly so both agree on bucket assignment.
- **Helper-driven bucket probing** — `near_value` folds the `Option`-match + `abs` comparison so the three bucket checks read cleanly.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`235`). Workload: bucketed sliding-window check over one PRNG array across many (k,t) pairs (map-heavy, data-dependent early exit).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 505.8 ms | 0.42× |
| **Kāra (codegen)** | 1.20 s | 1.00× |
| Rust `-O` | 1.37 s | 1.15× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 1.45 s | 1.21× |
| Go | 1.72 s | 1.44× |
| Python (scale lane) | 8.70 s | 7.26× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   contains_duplicate_iii.kara
karac build contains_duplicate_iii.kara && ./contains_duplicate_iii
python3 contains_duplicate_iii.py
diff <(karac run contains_duplicate_iii.kara) <(python3 contains_duplicate_iii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
