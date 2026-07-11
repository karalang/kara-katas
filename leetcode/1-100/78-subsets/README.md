# 78. Subsets

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Backtracking · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/subsets](https://leetcode.com/problems/subsets/)

Given an integer array `nums` of **distinct** elements, return **all possible subsets** (the power set). The solution set must not contain duplicate subsets; order doesn't matter.

```
nums = [1,2,3]  ->  [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
nums = [0]      ->  [[],[0]]
```

**Constraints:** `1 ≤ nums.length ≤ 10`; elements distinct.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Emit-at-every-node backtracking** ★ | [`subsets.kara`](subsets.kara) ✓ via `karac run` / `karac build` | [`subsets.py`](subsets.py) ✓ |
| **Iterative cascade** — double the collection per element | [`subsets_iterative.kara`](subsets_iterative.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all six test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## Two ways to build a power set

**Emit-at-every-node backtracking** ([`subsets.kara`](subsets.kara)) is the ★ — the same start-indexed DFS as kata [#77](../77-combinations/), with one change: a subset isn't only recorded at a fixed depth, **every node of the tree is a subset**, so the current `path` is snapshotted at the *top* of each call, before extending:

```
backtrack(start):
    snapshot path                      # this node is a subset
    for i in start..n:
        path.push(nums[i]); backtrack(i+1); path.pop()
```

Recursing at `i + 1` visits each subset once; emitting before the loop puts the empty set first and each prefix before its extensions, so the natural order is lexicographic (`[] < [1] < [1,2] < [1,2,3] < [1,3] < …`). One mutable `path`, `push`/recurse/`pop`, and a `path.clone()` snapshot per node.

**Iterative cascade** ([`subsets_iterative.kara`](subsets_iterative.kara)) builds the same power set bottom-up with **no recursion**: start with `[[]]`, and for each `num` extend every subset seen *so far* with a copy that also contains `num` — each element doubles the collection, giving `2ⁿ`:

```
out = [[]]
for num in nums:
    for each existing subset s (present BEFORE this num):
        out.push(s.clone() + num)
```

The `cur = out.len()` snapshot taken before the inner loop is load-bearing: only the subsets present at the round's start are extended. This visits the same subsets in **cascade order**, not lexicographic — so the result is sorted (a small selection sort over `Vec[Vec[i64]]`) to line up byte-for-byte with the ★. It's the recursion-free cross-check and a distinct surface — `Vec` `clone`-and-extend in a doubling loop, plus the `Vec[Vec[i64]]` element swap in the sort.

## Kāra features exercised

- **Recursion threading `mut ref Vec[i64]` + `mut ref Vec[Vec[i64]]`** — the ★ snapshots `path.clone()` at every node into the `Vec[Vec[i64]]` accumulator; the call-site-marker rule (`mut path`, `mut out` at the root; unmarked forwarding inside) shared with katas [#39](../39-combination-sum/)/[#77](../77-combinations/).
- **`Vec.clone()` + `push` cascade** — the iterative variant copies each existing subset and extends it (`out[j].clone()` then `extended.push(num)`), a growing `Vec[Vec[i64]]` that doubles per element.
- **`Vec[Vec[i64]]` element swap** — `out[i], out[min_idx] = out[min_idx], out[i]` swaps two subset rows in place inside the selection sort (the same parallel-assignment swap kata [#77](../77-combinations/)'s bitmask variant uses).
- **Prefix-aware subset comparator** — `subset_less` compares two variable-length subsets element-wise and makes the shorter a prefix smaller (`[] < [1] < [1,2]`).
- **Empty subset via typed `Vec.new()`** — the empty set is `let empty: Vec[i64] = Vec.new()` (the element-type annotation an empty literal in `push`-argument position currently needs — kāra ledger `B-2026-07-11-10`).

**v1 note.** `2ⁿ ≤ 1024` subsets and all values fit i64; the per-case sink is `count:hash` with a per-subset length marker so it's both count- and content-sensitive. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   subsets.kara
karac build subsets.kara && ./subsets

# The iterative-cascade variant (identical output):
karac run subsets_iterative.kara

# Python
python3 subsets.py

# Verify they all agree
diff <(karac run subsets.kara) <(python3 subsets.py)               && echo OK
diff <(karac run subsets.kara) <(karac run subsets_iterative.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`subsets.{kara,rs,c,py}`, `go-seq/main.go`).

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Workload.** The emit-at-every-node backtracking (the ★) run as an **enumerate-and-fold**: the recursion visits all **2¹⁶ = 65,536** subsets of `[1..16]` and folds each node's path into a threaded accumulator (no `Vec`-of-`Vec` storage — so the measured work is the **DFS recursion itself**, not allocation), for **K = 300** iterations seeded by the loop index so nothing hoists. All five compiled mirrors must agree on `12611223` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried sum is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Cloud-container numbers.**

| Implementation | Wall time |
|---|---|
| **kāra subsets**                            | **836.7 ± 14.5 ms** |
| rust subsets (rustc -O, overflow-checks=on) | 837.4 ± 10.7 ms |
| c    subsets (clang -O3)                     | 838.5 ± 7.6 ms |
| rust subsets (rustc -O)                      | 843.5 ± 5.2 ms |
| go   subsets                                 | 955.9 ± 6.5 ms |

A **dead heat** — kāra, `rustc -O -C overflow-checks=on`, and C land within **~2 ms** of each other (well inside the run-to-run noise), with kāra nominally first. On this recursion-bound backtracking kāra sits right **on the C floor**, and at equal safety it matches overflow-checked Rust (the workload is call/branch-bound, so overflow checks cost nothing — plain `rustc -O` is no faster). Go trails ~14%. Python at 1/10 the iteration count is ~2.33 s.

Compile-cold (clang 99 ms < rustc 163 ms < karac 312 ms) and binary size (c 15.7 KiB, **kāra 324.5 KiB**, go 2.11 MiB, rust 3.77 MiB — kāra links the runtime floor but stays far under Rust/Go); peak RSS c 1.53 / go 1.65 / rust 1.99 / kāra 2.22 MiB. See [`bench/results.container-x86.json`](bench/results.container-x86.json) for exact records.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this recursion-bound backtracking the four native/codegen languages land within a couple percent of each other. C calibrates the metal floor, Go is the other native data point, Python (run at 1/10 the iteration count, timed separately) the ergonomic foil.
