# 34. Find First and Last Position of Element in Sorted Array

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

A non-decreasing array (duplicates allowed) and a `target`. Return `[first, last]`
— the smallest and largest index where `nums[i] == target` — or `[-1, -1]` if the
target is absent. The catch: it must run in **O(log n)**.

```
[5,7,7,8,8,10], target = 8  →  [3, 4]
[5,7,7,8,8,10], target = 6  →  [-1, -1]
[],            target = 0  →  [-1, -1]
```

**Constraints:** `0 ≤ nums.length ≤ 10⁵`; `nums` non-decreasing; `-10⁹ ≤ nums[i], target ≤ 10⁹`.

## Why this kata — both ends of a run, without scanning it

The equal values form a contiguous run; the whole problem is "find the two ends of
that run without walking it." A single binary search finds *some* occurrence in
O(log n), but the run can be O(n) long (a whole array of one value), so expanding
outward from a hit to the ends is O(n) — exactly what the constraint forbids. Each
approach here finds the two ends *directly*, in O(log n), differing in how they
factor the search:

| Lens | Idea |
|---|---|
| **Two bounds** | `lower_bound` (first index `>= target`) and `upper_bound` (first index `> target`) — two equality-free half-open searches; the run is `[lower, upper)` |
| **Biased edge-finder** | one search that, on a hit, records the index and keeps going toward the chosen end (a `find_first` flag picks the side) |
| **Find-then-bound** | a textbook search proves presence and finds one hit, then two *inward* bounded searches pin each end |

The pedagogical arc: the two-bounds form never tests equality (presence is
reconstructed afterward); the edge-finder tests equality and biases inline; the
find-then-bound form separates "is it here?" from "where are its ends?" cleanly.
All three are O(log n).

## Approaches

Three styles, all byte-identical to the Python oracle across all 21 cases, under
`karac run` **and** `karac build` (the oracle additionally cross-checks the three
algorithms against each other and a brute-force scan of the run's true endpoints).

| Approach | File | Shape |
|---|---|---|
| **Two bounds** ★ | [`search_range.kara`](search_range.kara) | `lower_bound` + `upper_bound`, two half-open binary searches; `<` vs `<=` is the only difference between the two ends |
| Biased edge-finder | [`search_range_edge.kara`](search_range_edge.kara) | one `search_edge(.., find_first)`; equality records the best-so-far and biases toward the wanted end |
| Find-then-bound | [`search_range_split.kara`](search_range_split.kara) | `find_any` proves presence + one hit, then `bound_left`/`bound_right` shrink inward from it |

The two-bounds is the tightest pair of loops (one comparator flipped); the
edge-finder is the mirror image (equality drives the bias instead of bounds
reconstructing presence); the find-then-bound does the least total probing when
the target sits near the middle (each inward search spans at most half the array).

## What this kata uncovered

**A real codegen perf gap — and its fix ([`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md)).**
This kata posted the *widest* equal-safety gap of the recent binary-search katas,
and tracing it led to a genuine missed optimization on the canonical binary-search
loop — now closed in `karac`.

The ★ two-bounds search is the tight loop

```kara
while lo < hi {
    let mid = lo + (hi - lo) / 2i64;
    if nums[mid] < target { lo = mid + 1i64; } else { hi = mid; }
}
```

The `nums[mid]` access carries a bounds check. Rust's `&[i64]` indexing carries
one too — yet `rustc` folds it away, while `karac` kept it, and on a loop body this
tight the per-iteration check dominated: the seq lane ran **298 ms vs equal-safety
Rust's 189 ms (1.58×)**, the widest gap of the [#31](../31-next-permutation/) /
[#32](../32-longest-valid-parentheses/) / [#33](../33-search-in-rotated-sorted-array/)
through-line. Crucially the overflow tax was *zero* here (`rustc -O` and `rustc -C
overflow-checks=on` were identical at 189 ms), so unlike #33 this was **not** the
checked-arithmetic tax — it was pure codegen. A `get_unchecked` variant (no check)
ran 205 ms, pinning the bounds check as ~85 % of the gap.

**Root cause (LLVM 18 IR).** Folding `mid < len` needs the *relational* invariant
`mid < hi` — and `mid = lo + (hi - lo) / 2` correlates `lo` and `hi` *inside* the
index. LLVM's CVP/LVI is **interval-based**: it bounds `mid` componentwise as
`[lo_min + div_min, lo_max + div_max]`, which cannot prove `mid < hi`. Worse,
`karac` lowers checked arithmetic through `llvm.sadd.with.overflow`, and `mid` is
the `extractvalue` of that intrinsic — **opaque** to the range pass. So the check
survived `-O2`.

**Fix.** `karac` now recognizes the midpoint idiom (`lo + (hi-lo)/2` or `(lo+hi)/2`
under a strict `while lo < hi`) and emits two `llvm.assume`s at the binding —
`assume(mid >= lo)` and `assume(mid < hi)` — the relational facts the optimizer
can't synthesize. Both are *locally* sound from the midpoint form plus the
dominating guard (signed floor `(hi-lo)/2 ∈ [0, d-1]`, so `lo <= mid <= hi-1 < hi`),
and AOT overflow trapping makes the no-wrap precondition hold on every defined
execution — no whole-loop analysis required. With the facts present, CVP folds the
check. (A phase-ordering wrinkle — the assumes only fold once co-resident with the
check post-inline — is handled by one extra `default<O1>` pass *gated on emission*,
so non-binary-search programs pay nothing; the baked prelude has no midpoint search.)

**Result: the ★ search dropped 298 → 208 ms, closing the gap to equal-safety Rust
from 1.58× to 1.11×** (and 2.21× → 1.55× vs C). This is the kata-as-bug-finder loop
working as intended: a tight, mundane binary search flushed a latent codegen gap
that every `nums[mid]` in every Kāra binary search would have paid. Landed
`9b36be5d` with three regression tests (emission, a negative gate, and a soundness
E2E) and the full mechanism written up in
[`docs/investigations/bce_monotonic_assume.md` § midpoint idiom](../../../../kara/docs/investigations/bce_monotonic_assume.md).

## Benchmarks

Workload: build one fixed sorted array of length `N = 4096` once (`nums[p] =
2·(p/4)` — non-decreasing, each even value repeated 4×, odd values absent), then
run the full first+last query (`lower_bound` + `upper_bound`) **`TOTAL = 14M`**
times for targets cycling through `[0, 2N)` so all four control-flow paths (hit /
odd-miss / over-miss / boundary) fire, folding both endpoints into a checksum
(sink `421417033`). The target varies with the loop index, so no comparator can
hoist the query out of the loop; the accumulator carries a loop-borne dependency,
so it does not auto-parallelize. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded two-bounds binary search)

| | C | Go | Rust (`-O`) | **Kāra** | Rust (`overflow-checks=on`) | Python |
|---|---|---|---|---|---|---|
| time | 134.6 ms | 139.2 ms | 187.8 ms | **208.4 ms** | 187.8 ms | 7025 ms |
| vs Kāra | 1.55× faster | 1.50× faster | 1.11× faster | — | **1.11× faster (= safety)** | 34× slower |

**The bounds-check fix is the whole story.** Before [`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md),
Kāra ran **298 ms — 1.58× behind equal-safety Rust**, the widest gap of the
binary-search katas, entirely from the un-folded `nums[mid]` check (the overflow
tax is *zero* here: `rustc -O` and `-C overflow-checks=on` both land at 187.8 ms).
Teaching `karac` to assert the midpoint's `lo <= mid < hi` lets LLVM fold the
check, dropping Kāra to **208 ms — within 1.11× of equal-safety Rust**, the same
band as the rest of the through-line. The residual gap is one `nums[lo]` check in
`main` (a guard-proven index against a decoupled length, a separate issue) plus the
genuine ~11 % a branchy, allocation-light search leaves between Kāra and the
systems-language floor (C's no-overhead `1.55×`).

**No par lane — by construction.** Each query is independent, but karac's
auto-par-on-reduction pass does not fire on this loop (per-call function + checksum
reduction): the default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and
both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.06 MiB | 1.11 MiB | **1.05 MiB** | 3.0 MiB |
| binary size (seq) | **33.4 KiB** | 455.7 KiB | 32.7 KiB | 2434.1 KiB |
| compile elapsed | **74.3 ms** | 93.9 ms | 46.8 ms |
| compile peak RSS | **13.2 MiB** | 26.8 MiB | 2.5 MiB |

The single 4096-element array is the only heap allocation, so runtime RSS ties C
and Rust to within rounding (1.06 / 1.05 / 1.11 MiB). The seq compute binary
references no `String`/par-scheduler runtime, so LTO + `-dead_strip` carve it to
**33.4 KiB** — 13.6× under Rust. Compile favors Kāra over `rustc -O` on both
elapsed (74.3 vs 93.9 ms) and peak compiler RSS (13.2 vs 26.8 MiB) — and the gated
second optimization pass the fix adds is invisible in the numbers (it runs only for
binary-search modules, where it pays for itself many times over at runtime).

## Kāra features exercised

- **`Vec[i64]` read params from a `ref` borrow** — the bound searches take
  `ref Vec[i64]`; `main` builds the array once and forwards it without a call-site
  marker (immutable read borrow).
- **The binary-search midpoint idiom** — `let mid = lo + (hi - lo) / 2` under a
  strict `while lo < hi`, the pattern that now emits `assume(lo <= mid < hi)` and
  folds the `nums[mid]` bounds check (the fix this kata surfaced,
  [`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md)).
- **Half-open vs closed binary search** — the two-bounds style's `while lo < hi`
  (half-open, the form the fix optimizes) alongside the edge-finder/find-then-bound
  styles' `while lo <= hi` (closed interval, deliberately out of the fix's scope:
  `lo == hi` would make `mid == hi`).
- **Empty-array boundary** — `let a2: Array[i64, 0] = []` to a `Slice` param, the
  case that regression-guards [#33](../33-search-in-rotated-sorted-array/)'s
  [`B-2026-06-14-30`](../../../../kara/docs/bug-ledger.md).

---

**Bug ledger:** surfaced **`B-2026-06-16-1`** (canonical binary-search `nums[mid]`
bounds check not folded — relational `mid < hi` invariant opaque to interval CVP;
1.58× → 1.11× vs equal-safety Rust), fixed `9b36be5d` with midpoint `llvm.assume`
emission and three regression tests. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md) and
[`docs/investigations/bce_monotonic_assume.md`](../../../../kara/docs/investigations/bce_monotonic_assume.md).
