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

## Running

```bash
karac run   contains_duplicate_iii.kara
karac build contains_duplicate_iii.kara && ./contains_duplicate_iii
python3 contains_duplicate_iii.py
diff <(karac run contains_duplicate_iii.kara) <(python3 contains_duplicate_iii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
