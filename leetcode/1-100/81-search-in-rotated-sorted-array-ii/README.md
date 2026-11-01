# 81. Search in Rotated Sorted Array II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/search-in-rotated-sorted-array-ii](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)

A sorted-ascending array that **may contain duplicates** has been rotated at an unknown pivot (e.g. `[0,0,1,2,2,5,6]` → `[2,5,6,0,0,1,2]`). Given a `target`, return **true** if it is present, **false** otherwise. This is kata [#33](../33-search-in-rotated-sorted-array/) with duplicates allowed — which, as the twist below shows, defeats the O(log n) guarantee.

```
nums = [2,5,6,0,0,1,2]  target = 0  ->  true
nums = [2,5,6,0,0,1,2]  target = 3  ->  false
```

**Constraints:** `1 ≤ nums.length ≤ 5000`; `nums` is a sorted array rotated at some pivot; duplicates allowed.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Shrink-both on `nums[lo]==nums[mid]==nums[hi]`** ★ | [`search_rotated_ii.kara`](search_rotated_ii.kara) ✓ via `karac run` / `karac build` | [`search_rotated_ii.py`](search_rotated_ii.py) ✓ |
| **Single-sided skip on `nums[lo]==nums[mid]`** | [`search_rotated_ii_skiplow.kara`](search_rotated_ii_skiplow.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all nineteen queries, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike; both approaches agree with each other, with the Python mirror, **and with a linear-scan ground truth** (each query's `true`/`false` matches actual membership). Both compile with **zero diagnostics**.

## Why duplicates break #33 — and the two ways to patch it

Kata #33's rotated binary search decides *which half is sorted* by comparing the two ends of the window to the midpoint: `nums[lo] <= nums[mid]` means the left half is sorted, so a simple range test picks the direction and the window halves. Duplicates break exactly this test. When `nums[lo] == nums[mid]`, the comparison is uninformative — the pivot could be on either side. The worst case, an all-equal array like `[1,1,1,2,1,1,1]`, forces the search to give up halving and walk linearly: **#81 is O(n) worst case** where #33 is strictly O(log n). The two solvers differ only in *how* they resolve that tie:

**Shrink both ends** ([`search_rotated_ii.kara`](search_rotated_ii.kara), the ★) adds one branch to #33's logic:

```
if nums[lo] == nums[mid] == nums[hi]:   lo += 1; hi -= 1     # ambiguous — drop one from each end
elif nums[lo] <= nums[mid]:             ... left half sorted (as in #33)
else:                                   ... right half sorted (as in #33)
```

The ambiguous case is precisely when all three window ends are equal; then one indistinguishable element is dropped from *each* end and the search retries. Whenever the three ends are not all equal, `#33`'s `nums[lo] <= nums[mid]` split is still valid, so the average case stays logarithmic.

**Single-sided skip** ([`search_rotated_ii_skiplow.kara`](search_rotated_ii_skiplow.kara)) splits on strict inequalities and folds the ambiguity into the low end alone:

```
if   nums[lo] <  nums[mid]:   ... left half strictly sorted
elif nums[lo] >  nums[mid]:   ... right half sorted
else:                          lo += 1        # nums[lo] == nums[mid] != target, so drop it
```

It's safe to skip `nums[lo]` on the tie because this branch is reached only after `nums[mid] != target`, and `nums[lo] == nums[mid]`, so `nums[lo]` can't be the target either. A distinct control-flow shape — a three-way strict split with a single-sided shrink instead of the ★'s all-three-equal test — that must land byte-identical to the ★ and the linear ground truth on every query.

## Kāra features exercised

- **Duplicate-ambiguity binary search** — the ★'s three-way `nums[lo] == nums[mid] and nums[mid] == nums[hi]` guard and the variant's strict `<`/`>` split are the branch-heavy heart of the kata; both chain comparisons with `and` (kāra's short-circuit conjunction, not `&&`).
- **`Slice[i64]` read-only view + `Array[i64, N]` literals** — every case is a stack `Array[i64, N]` literal passed straight into a `Slice[i64]` parameter (the same read-only borrow form kata [#33](../33-search-in-rotated-sorted-array/) uses), sliced to a `len`.
- **Signed midpoint `lo + (hi - lo) / 2`** — the overflow-safe midpoint on `i64` cursors, with `hi` walking down to `mid - 1` (including to `-1` on an empty window, which the `lo <= hi` guard rejects before any read).
- **`bool` return threaded to a hash sink** — `search` returns a `bool`; `report` folds it (as `1`/`0`) together with the target into a running polynomial hash, so the sink is both target- and outcome-sensitive across the nineteen queries.
- **`String` building via `push_str` + interpolation** — `fmt` renders each array with `f"{nums[i]}"` fragments and `", "` separators (shared with #33's formatter).

**v1 note.** Arrays are short (`len ≤ 5000` in the spec; the test cases are tiny) and all values fit i64. Every test array is a genuine rotation of a sorted-with-duplicates array, so the binary search's answer is verified against true membership, not just against the Python port of the same algorithm. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   search_rotated_ii.kara
karac build search_rotated_ii.kara && ./search_rotated_ii

# The single-sided-skip variant (identical output):
karac run search_rotated_ii_skiplow.kara

# Python
python3 search_rotated_ii.py

# Verify they all agree
diff <(karac run search_rotated_ii.kara) <(python3 search_rotated_ii.py)                  && echo OK
diff <(karac run search_rotated_ii.kara) <(karac run search_rotated_ii_skiplow.kara)      && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`search_rotated_ii.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `measured_at` 2026-11-01. The first M5 snapshot (2026-07-10/11, legacy backend) replaced an earlier x86-64 cloud-container one and corrected that snapshot's claim of kāra *ahead* of overflow-checked Rust. **Against Rust the MIR re-bench is flat; kāra is still last of five:** Kāra/Rust 1.31× → 1.32×, Kāra/equal-safety-Rust 1.08× → 1.09×, Kāra/Go 1.49× → 1.51×, Kāra/C 1.60× → 1.32×. The C move is almost all C-side — the C row ran 1.36× slower than in July, against 1.11–1.13× for Rust, Go and kāra — so it is not a kāra gain. `bench/results.json` records the M5 host.

**Workload.** A single rotated binary search is O(log n), so the bench is a **build-once + punch**: one rotated sorted array with duplicates (each value `0..1000` appears **twice**, then rotated — **N = 2000**) is built once, then searched **K = 17,000,000** times for targets sweeping present and absent values (`target = iter % 1050`), folding each `true`/`false` outcome through a **rolling polynomial hash**. The loop-carried hash serialises the punch loop and keeps every search's result observable so nothing hoists; the measured work is the search's comparison/branch loop over cache-resident reads. All five compiled mirrors must agree on `700567695` before timing.

**Equal data structure.** Every mirror uses a **1D heap array** — kāra `Vec[i64]`, Rust `Vec<i64>`, C `malloc`'d `int64_t*`, Go `[]int64` — the same layout, so the comparison is codegen-vs-codegen.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. **Lane note (2026-11-01):** the kāra row is the seq lane — `bench/bench.sh` builds it with `KARAC_AUTO_PAR=0` (harness fixed 2026-11-01; an earlier run that day had accidentally timed the auto-parallel default build) — and it runs at 99.7 % CPU like every other mirror. The default `karac build` does auto-parallelize this kata: under MIR the auto-par pass fires on the one-off array build in `build()`, verified in the emitted IR (`KARAC_MIR_LL`: the default build contains a call of `@karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` build none). That is a real but small wall-time gain — default build **228.9 ± 2.6 ms** vs in-order build **246.7 ± 3.4 ms**, **1.08×** (hyperfine, same machine, 2026-11-01) — and it is not in the table below, which compares single-threaded code. **M5 Pro numbers, karac g6697158fa, measured_at 2026-11-01.**

| Implementation | Wall time |
|---|---|
| go   search_rotated_ii                                | **163.6 ± 4.0 ms** |
| c    search_rotated_ii (clang -O3)                    | 187.0 ± 3.2 ms |
| rust search_rotated_ii (rustc -O)                     | 187.5 ± 1.6 ms |
| rust search_rotated_ii (rustc -O, overflow-checks=on) | 228.1 ± 2.8 ms |
| **kāra search_rotated_ii**                            | **247.7 ± 3.0 ms** |

On the M5 kāra is **last of five** — 1.51× behind Go (now the fastest; C led in July), 1.32× behind C, 1.32× behind wrapping `rustc -O` (C and Rust tie inside σ), and **1.09× behind equal-safety `rustc -O -C overflow-checks=on`** (228.1 ms). Two things make this kata unusual. First, **overflow checks actually cost here** (~22 %: Rust goes 187.5 → 228.1 ms with `overflow-checks=on`) — the midpoint arithmetic and rolling-hash fold sit on the hot path — so equal-safety Rust is the fair peer, and the gap to it is unchanged from July (1.08× → 1.09×). Second, the July gap to it was **not** extra work: the July legacy build retired **3.554 G instructions to rust_ovf's 3.540 G** — essentially identical — but at a **lower IPC (3.55 vs 3.89)** (counts not re-taken on MIR). That was the *instruction-scheduling* flavor of the diffuse codegen-quality gap (`B-2026-07-10-5`), distinct from the instruction-*density* flavor of [#76](../76-minimum-window-substring/)/[#79](../79-word-search/). Most of the 1.32× gap vs **C** is the safety cost both kāra and Rust pay (rust_ovf is itself 1.22× C). Python was last measured 2026-07-11 and not re-run: at K=300000 (1/56 the native iteration count) it took ~0.17 s.

Compile-cold on the M5: clang 49.0 ms < rustc 91.6 ms < **karac 158.9 ms** — karac is now 1.73× slower than rustc (~1.02× faster in July) and 3.24× the clang floor. Binary size: c 32.7 KiB, **kāra 295.8 KiB**, rust 455.7 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: c 1.05 MiB, **kāra 1.08 MiB**, rust 1.06 MiB, go 2.61 MiB. Full records in [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here it was an honest **loss** in July (1.08× behind equal-safety `rustc -O -C overflow-checks=on`, from ~10 % worse instruction scheduling at matched instruction counts) and is still one on MIR (1.09×, measured 2026-11-01), with kāra 1.32× behind wrapping `rustc -O`. C calibrates the metal floor, Go is the other native data point, Python (run at a fraction of the iteration count, timed separately; last measured 2026-07-11) the ergonomic foil. Another case where measuring on the reference machine turned the container's rosy "kāra ahead of Rust" reading into a precise, honest gap — exactly why Rust stays in the harness.
