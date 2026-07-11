# 80. Remove Duplicates from Sorted Array II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-duplicates-from-sorted-array-ii](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)

Given a **sorted** integer array `nums`, remove duplicates **in place** so that each distinct value appears **at most twice**, preserving the relative order, and return the new length `k`. The first `k` slots of `nums` must hold the result; the rest may be anything.

```
nums = [1,1,1,2,2,3]        -> k=5, nums[:5] = [1,1,2,2,3]
nums = [0,0,1,1,1,1,2,3,3]  -> k=7, nums[:7] = [0,0,1,1,2,3,3]
```

**Constraints:** `1 ≤ nums.length ≤ 3·10⁴`; `nums` sorted non-decreasing.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Two-pointer, `nums[k-2]` look-back** ★ | [`remove_duplicates_ii.kara`](remove_duplicates_ii.kara) ✓ via `karac run` / `karac build` | [`remove_duplicates_ii.py`](remove_duplicates_ii.py) ✓ |
| **Generalized keep-at-most-`m` (run counter)** | [`remove_duplicates_ii_general.kara`](remove_duplicates_ii_general.kara) ✓ | — |
| **Two-pointer over a `mut Slice[i64]` view** | [`remove_duplicates_ii_slice.kara`](remove_duplicates_ii_slice.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all seven test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror. All three compile with **zero diagnostics**.

## Three ways to cap a run at two

**Two-pointer with a two-slot look-back** ([`remove_duplicates_ii.kara`](remove_duplicates_ii.kara), the ★) is the canonical O(1)-space sweep. A write cursor `k` trails the read cursor `i`; the value at `i` is kept only when it differs from the one **two positions back in the already-written prefix**:

```
k = 2
for i in 2..n:
    if nums[i] != nums[k-2]:     # sorted, so nums[k-2] is the value written 2 ago
        nums[k] = nums[i]; k += 1
return k
```

Because the array is sorted, `nums[k-2]` is exactly the value that would sit two slots before `i`'s landing spot — so a third identical copy always equals it and is skipped, while the first two always differ from whatever preceded them. The first two elements are kept unconditionally (`k` starts at 2), and `n ≤ 2` returns `n` directly. The write is an **in-place index assignment into the same `mut ref Vec[i64]` being read** — `nums[k] = nums[i]`.

**Generalized keep-at-most-`m`** ([`remove_duplicates_ii_general.kara`](remove_duplicates_ii_general.kara)) makes the cap explicit instead of implicit. It walks each **run** of equal values and copies at most `m` of them forward, using a run counter rather than a `nums[k-2]` peek:

```
for each run of equal value v:
    keep the first m copies, drop the rest
```

With `m = 2` the output is byte-identical to the ★; `m = 1` would be the plain "remove duplicates" of kata [#26](../26-remove-duplicates-from-sorted-array/). It's a distinct surface — an inner run-scan loop with a compound `while i < n and nums[i] == v` condition and an explicit counter — and the recursion-free cross-check that the look-back trick is correct.

**Two-pointer over a `mut Slice[i64]` view** ([`remove_duplicates_ii_slice.kara`](remove_duplicates_ii_slice.kara)) is the ★'s exact algorithm re-typed to the **most faithful encoding of the LeetCode contract**. Rather than owning a `mut ref Vec[i64]`, the dedup takes a `mut Slice[i64]` — a mutable *window* onto the caller's storage. It can overwrite within bounds and read its own `.len()`, but it cannot grow or shrink the backing `Vec`, which is exactly the "modify `nums` in place, return `k`" shape. At the call site `remove_dups(mut nums)` coerces the `ref mut Vec[i64]` to a `mut Slice[i64]` (design.md's `ref mut Vec[T] → mut Slice[T]` boundary coercion) — the same borrow form kata [#26](../26-remove-duplicates-from-sorted-array/) (the `m = 1` sibling), [#31](../31-next-permutation/), and [#88](../88-merge-sorted-array/) use. A separate ownership + codegen path from the owning ★, verified to land byte-identical.

## Kāra features exercised

- **In-place index-assignment reading another index** — `nums[k] = nums[i]` writes into the same `mut ref Vec[i64]` it reads from, with `k` trailing `i`; the whole dedup is this one converging-pointer write.
- **`nums[k - 2]` look-back into the written prefix** — the ★'s correctness hinges on indexing two slots back in the *result* being built, an index computed from the write cursor.
- **Compound loop condition with short-circuit `and`** — the generalized variant's inner `while i < n and nums[i] == v` relies on `and` short-circuiting so `nums[i]` is never read at `i == n` (kāra uses `and`/`or`, not `&&`/`||`).
- **`mut ref Vec[i64]` threading + call-site marker** — `remove_dups(mut nums)` marks the fresh owned `nums` at the call site; the callee mutates in place and returns the new length.
- **`mut Slice[i64]` view + boundary coercion** — the slice variant hands the dedup a mutable window; `remove_dups(mut nums)` coerces `ref mut Vec[i64]` → `mut Slice[i64]` at the call boundary, and the sweep is bounded by the slice's own `.len()` (a distinct ownership + codegen surface from the owning form; both compile clean).
- **Fixed-size `Array[i64, 9]` case tables** — each test case's values are a stack `Array[i64, 9]` sliced to a length by `make`, then copied into a fresh `Vec[i64]` so the in-place dedup doesn't clobber the source.

**v1 note.** Arrays are short and all values fit i64; the per-case sink folds `k` plus the surviving prefix into a running polynomial hash so it's both length- and content-sensitive across the seven cases. All three solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; all three compile with **zero diagnostics**.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   remove_duplicates_ii.kara
karac build remove_duplicates_ii.kara && ./remove_duplicates_ii

# The other two variants (identical output):
karac run remove_duplicates_ii_general.kara   # generalized keep-at-most-m
karac run remove_duplicates_ii_slice.kara     # mut Slice[i64] view

# Python
python3 remove_duplicates_ii.py

# Verify they all agree
diff <(karac run remove_duplicates_ii.kara) <(python3 remove_duplicates_ii.py)                    && echo OK
diff <(karac run remove_duplicates_ii.kara) <(karac run remove_duplicates_ii_general.kara)        && echo OK
diff <(karac run remove_duplicates_ii.kara) <(karac run remove_duplicates_ii_slice.kara)          && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`remove_duplicates_ii.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-10).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **The dead heat holds** — kāra ties both Rust builds to within a millisecond and sits 1.007× off the C floor, 1.21× ahead of Go. The honest nuance (see below): this is a *latency-bound* loop, so kāra's dead heat is genuine on the clock even though it retires **1.75× C's instructions** — the density is masked in the stall shadow (`B-2026-07-10-5`). `bench/results.json` records the M5 host.

**Workload — why not the in-place sweep itself.** The kata's two-pointer write is a **csel-on-converging-pointer**: the optimizer would vectorise the conditional store away, and mutating in place forces a per-iteration *copy* of the array (allocation domination) — both erase the work you meant to measure (`BENCHMARKS.md`'s pitfalls). So the bench times the **decision logic**: the generalized run-scan computes the at-most-2 dedup and folds each kept value through a **rolling polynomial hash**. The loop-carried hash serialises the scan (resisting vectorisation) over a fixed **N = 3000** sorted array (mixed run lengths 1, 2, 3, … so the cap actually drops elements) built **once**, for **K = 67,000** iterations seeded by the loop index so nothing hoists. All five compiled mirrors must agree on `103734817` before timing.

**Equal data structure.** Every mirror uses a **1D heap array** — kāra `Vec[i64]`, Rust `Vec<i64>`, C `malloc`'d `int64_t*`, Go `[]int64` — the same layout, so the comparison is codegen-vs-codegen.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99 % CPU (verified equal to `KARAC_AUTO_PAR=0`; `karac build --concurrency-report` finds no parallelizable region). **M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| c    remove_duplicates_ii (clang -O3)                    | **518.2 ± 1.7 ms** |
| **kāra remove_duplicates_ii**                            | **522.0 ± 3.3 ms** |
| rust remove_duplicates_ii (rustc -O)                     | 522.1 ± 3.3 ms |
| rust remove_duplicates_ii (rustc -O, overflow-checks=on) | 522.5 ± 4.5 ms |
| go   remove_duplicates_ii                                | 629.9 ± 2.1 ms |

A **dead heat** — kāra, `rustc -O`, and equal-safety Rust finish within **half a millisecond** of each other (522.0 / 522.1 / 522.5 ms), all 1.007× off the C floor and 1.21× ahead of Go. But the parity is **latency-masked, not codegen parity** — the honest read the reference machine makes visible. The loop is a tight dependent chain of multiply-add-mod over sequential reads, memory/latency-bound (every mirror's IPC is low — C 1.16, kāra 2.02), so the wall-clock is set by cycles-to-drain-the-chain, which are equal. Under the hood kāra retires **4.77 G instructions to C's 2.73 G (1.75×) and rust_ovf's 4.14 G (1.15×)** — its per-element bounds + overflow checks are real extra work that simply executes in the stall shadow for free here. On a *throughput*-bound loop the same density gap surfaces as a real loss (kata [#79](../79-word-search/); the general characterization is `B-2026-07-10-5`). Overflow checks cost nothing (latency-bound), so equal-safety and wrapping Rust are indistinguishable. Python (K=3000, ~0.49 s, a fraction of the native iteration count) is timed separately.

Compile-cold on the M5: clang 40.6 ms < rustc 81.8 ms < **karac 84.1 ms** (~1.03× rustc, ~2.07× clang). Binary 33.3 KiB (C parity), runtime RSS 1.08 MiB (~C). Full records in [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this serialised hash-fold scan the two land in a dead heat. C calibrates the metal floor, Go is the other native data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
