# 90. Subsets II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Backtracking · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/subsets-ii](https://leetcode.com/problems/subsets-ii/)

Given an integer array `nums` that **may contain duplicates**, return **all possible subsets** (the power set). The solution set must **not** contain duplicate subsets. This is kata [#78](../78-subsets/) with duplicates allowed.

```
nums = [1,2,2]  ->  [[],[1],[1,2],[1,2,2],[2],[2,2]]
nums = [0]      ->  [[],[0]]
```

**Constraints:** `1 ≤ nums.length ≤ 10`; `-10 ≤ nums[i] ≤ 10`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Sorted backtracking, skip-duplicates-at-level** ★ | [`subsets_ii.kara`](subsets_ii.kara) ✓ via `karac run` / `karac build` | [`subsets_ii.py`](subsets_ii.py) ✓ |
| **Iterative cascade with duplicate handling** | [`subsets_ii_iterative.kara`](subsets_ii_iterative.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all nine test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other, with the Python mirror, **and with a brute-force ground truth** (the deduplicated power set of the multiset — every solver produces exactly it, with no duplicate subset). Both compile with **zero diagnostics**.

## One rule kills every duplicate subset

The only difference from #78 is avoiding duplicate *subsets* when `nums` has duplicate *values*. **Sorting** `nums` first brings equal values together, and then one rule does it: at each tree level, take `nums[i]` only when it is the **first choice at that level or differs from its predecessor** — `i == start OR nums[i] != nums[i-1]`.

**Sorted backtracking** ([`subsets_ii.kara`](subsets_ii.kara), the ★) is #78's emit-at-every-node DFS with that one guard added:

```
sort(nums)
backtrack(start):
    snapshot path                              # every node is a subset
    for i in start..n:
        if i == start or nums[i] != nums[i-1]:  # skip a duplicate started at this level
            path.push(nums[i]); backtrack(i+1); path.pop()
```

A run of equal values can be *extended* (`nums[i]` with `i > start`, following its own duplicate down the tree) but never *started twice at the same level* — so `[2,2]` is built once, not once per equal `2`. Because `nums` is sorted and each node is emitted before its extensions, the natural order is lexicographic.

**Iterative cascade** ([`subsets_ii_iterative.kara`](subsets_ii_iterative.kara)) builds the same set bottom-up with no recursion: start with `[[]]` and double the collection per value — but when a value equals its predecessor, extend **only the subsets the previous element just added** (`out[start..size]`), not all of them:

```
out = [[]]; start = 0
for each nums[i]:
    begin = (i > 0 and nums[i] == nums[i-1]) ? start : 0
    size  = out.len()
    for j in begin..size: out.push(out[j] + nums[i])
    start = size
```

Extending everything would rebuild `[2]` from both `2`s; restricting to the previous element's fresh subsets makes the run `[2],[2,2]` appear once. `start` is set to the length *before* this element's additions, so the next element (if a duplicate) sees exactly this element's new subsets. The cascade order differs from the ★'s DFS order, so the result is sorted (the same `subset_less` + selection sort as [#78](../78-subsets/)) to line up byte-for-byte — a distinct surface (`Vec` clone-and-extend in a doubling loop, plus the `Vec[Vec[i64]]` element swap).

## Kāra features exercised

- **Skip-duplicates-at-level guard** — the `i == start or nums[i] != nums[i-1]` test (on a `nums[i-1]` look-back into the sorted array) is the whole deduplication mechanism; both solvers hinge on it.
- **In-place selection sort with parallel-assignment swap** — `sort_nums` orders the input and the iterative variant's `sort_subsets` canonicalises the collection, both using `a[i], a[j] = a[j], a[i]` (over `i64` and over `Vec[i64]` rows).
- **`mut ref` recursion threading `Vec[i64]` + `Vec[Vec[i64]]`** — the ★ snapshots `path.clone()` at every node into the accumulator; the call-site-marker rule (`mut path`, `mut out` at the root; unmarked forwarding inside) shared with [#39](../39-combination-sum/)/[#78](../78-subsets/).
- **`Vec.clone()` + extend cascade** — the iterative variant copies each existing subset and appends the new value, a growing `Vec[Vec[i64]]`.
- **Prefix-aware subset comparator** — `subset_less` compares two variable-length subsets element-wise, shorter-is-prefix-smaller (`[] < [1] < [1,2]`).

**v1 note.** `nums.length ≤ 10` so the deduplicated power set stays small; the per-case sink is `count:hash` with a per-subset length marker, both count- and content-sensitive. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both match the deduplicated-power-set ground truth on every case.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   subsets_ii.kara
karac build subsets_ii.kara && ./subsets_ii

# The iterative-cascade variant (identical output):
karac run subsets_ii_iterative.kara

# Python
python3 subsets_ii.py

# Verify they all agree
diff <(karac run subsets_ii.kara) <(python3 subsets_ii.py)                  && echo OK
diff <(karac run subsets_ii.kara) <(karac run subsets_ii_iterative.kara)    && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`subsets_ii.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **The win holds:** kāra is fastest of five (tied with equal-safety Rust), ahead of C, wrapping Rust, and Go on this latency-bound dedup backtracking. `bench/results.json` records the M5 host.

**Workload.** The emit-at-every-node dedup backtracking (the ★) run as an **enumerate-and-fold** (kata [#78](../78-subsets/)'s shape): the recursion visits every **unique** subset node of a sorted multiset — **8 distinct values each repeated twice** (`[0,0,1,1,…,7,7]`), so the `i == start or nums[i] != nums[i-1]` skip rule fires throughout and the tree has **3⁸ = 6561** unique subsets (not 2¹⁶) — and folds each node's path into a threaded accumulator (no `Vec`-of-`Vec` storage, so the measured work is the **DFS recursion + the dedup test**, not allocation). Enumerated **K = 2700** times, the acc seeded with the loop index so nothing hoists. All five compiled mirrors must agree on `96157880` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99 % CPU (verified equal to `KARAC_AUTO_PAR=0`; `karac build --concurrency-report` finds no parallelizable region). **M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| **kāra subsets_ii**                            | **500.2 ± 4.0 ms** |
| rust subsets_ii (rustc -O, overflow-checks=on) | 500.4 ± 4.0 ms |
| rust subsets_ii (rustc -O)                      | 532.5 ± 5.0 ms |
| c    subsets_ii (clang -O3)                     | 536.9 ± 6.0 ms |
| go   subsets_ii                                 | 604.0 ± 6.0 ms |

Kāra is **fastest of five** — a dead heat with equal-safety Rust for the lead (500.2 vs 500.4 ms, within noise) and **ahead of C (1.07×), plain `rustc -O` (1.06×), and Go (1.21×)**. This recursion-bound dedup backtracking is **latency-bound** (call/return + the reused path's push/pop memory traffic stall the pipeline — C runs at IPC 1.06 here), and kāra actually pipelines it *better* (IPC 1.42): it retires 1.26× C's instructions (3.23 G vs 2.55 G) yet finishes ahead of C, because the higher IPC more than covers the extra bounds/overflow-check work — and it matches equal-safety Rust exactly (3.23 G ≈ rust_ovf 3.21 G, same IPC). Same favorable regime as siblings [#77](../77-combinations/)/[#78](../78-subsets/). Python is timed separately.

Binary 33.1 KiB (C parity), RSS ~C. See [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this recursion-bound dedup backtracking the mirrors land close (it is call/return latency-bound, so kāra's instruction density hides — the same regime as siblings [#77](../77-combinations/)/[#78](../78-subsets/)). C calibrates the metal floor, Go is the other native data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
