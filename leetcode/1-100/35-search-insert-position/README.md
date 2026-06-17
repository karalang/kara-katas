# 35. Search Insert Position

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/search-insert-position](https://leetcode.com/problems/search-insert-position/)

A **sorted array of distinct integers** and a `target`. Return the index of the
target if it is present; otherwise return the index where it would be inserted to
keep the array sorted. Must run in **O(log n)**.

```
[1,3,5,6], target = 5  →  2   (found)
[1,3,5,6], target = 2  →  1   (insert between 1 and 3)
[1,3,5,6], target = 7  →  4   (append)
[1,3,5,6], target = 0  →  0   (prepend)
```

**Constraints:** `1 ≤ nums.length ≤ 10⁴`; `nums` strictly increasing (distinct); `-10⁴ ≤ nums[i], target ≤ 10⁴`.

## Why this kata — "found" and "insert" are the same number

The whole problem collapses to one observation: the found index and the insert
index are **the same value** — the first index `i` with `nums[i] >= target`. If the
target is present, distinct values mean that `i` lands exactly on it (no run to
disambiguate, unlike [#34](../34-find-first-and-last-position/)); if it is absent,
`i` is precisely where it belongs. So this is `lower_bound` verbatim, with **no
found-vs-absent branch at all** — the search's terminal index is the entire answer.

That makes #35 the **single-search core** of #34: where #34 ran *two* bound
searches to pin both ends of a duplicate run, #35 runs *one* and returns it
directly. Each approach here computes that one index, differing only in how it
walks the array:

| Lens | Idea |
|---|---|
| **Half-open `lower_bound`** | `while lo < hi`, `hi = mid` on `>=` — the live window is `[lo, hi)`; terminal `lo` is the answer, append case (`lo == len`) included for free |
| **Closed + candidate** | `while lo <= hi` over real indices; record the leftmost `mid` with `nums[mid] >= target` and keep biasing left |
| **Binary lifting** | build the index bottom-up from power-of-two strides — a *fixed* iteration count regardless of the data |

## Approaches

Three styles, all byte-identical to the Python oracle across all 24 cases, under
`karac run` **and** `karac build` (the oracle additionally cross-checks the three
algorithms against each other and a brute-force scan for the first index `>= target`).

| Approach | File | Shape |
|---|---|---|
| **Half-open `lower_bound`** ★ | [`search_insert.kara`](search_insert.kara) | `while lo < hi`; `nums[mid] < target ? lo = mid+1 : hi = mid`; return `lo`. Never tests equality — the terminal point *is* the insert index |
| Closed + candidate | [`search_insert_closed.kara`](search_insert_closed.kara) | `while lo <= hi`, `ans` defaults to `len`; on `nums[mid] >= target` record `ans = mid` and search left |
| Binary lifting | [`search_insert_stride.kara`](search_insert_stride.kara) | `pos = -1`, halve `step` from the largest power of two `<= len`; jump `pos += step` while `nums[pos+step] < target`; return `pos + 1` |

The half-open form is the tightest (one comparator, no answer register, append case
free); the closed form is the mirror of [#34](../34-find-first-and-last-position/)'s
biased edge-finder (record-and-bias-left, but on `>=` rather than equality); the
binary-lifting form runs an identical instruction trace for every query of a given
length — only the taken/not-taken bit of each `pos += step` varies — the shape a
branch predictor and a loop-unroller like best. All three are O(log n).

## What this kata confirmed

**The midpoint bounds-check fix generalizes to the single-search canonical loop.**
[#34](../34-find-first-and-last-position/) surfaced
[`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md): `karac` was not folding the
`nums[mid]` bounds check on the binary-search midpoint idiom, because the relational
invariant `mid < hi` is opaque to LLVM's interval-based CVP (and `mid` is the
`extractvalue` of a `llvm.sadd.with.overflow`). The fix teaches `karac` to emit
`assume(lo <= mid < hi)` at the midpoint binding, restoring the fold. #35 is the
**most common binary search there is** — the bare `lower_bound`/insert-position loop

```kara
while lo < hi {
    let mid = lo + (hi - lo) / 2i64;
    if nums[mid] < target { lo = mid + 1i64; } else { hi = mid; }
}
```

— so it is the cleanest possible regression witness that the fix holds on the
single-search case, not just on #34's paired bound searches. With the assume in
place, the seq lane lands **189.6 ms — within 1.11× of equal-safety Rust**, the same
band as the rest of the [#31](../31-next-permutation/) /
[#32](../32-longest-valid-parentheses/) / [#33](../33-search-in-rotated-sorted-array/)
/ [#34](../34-find-first-and-last-position/) through-line. As on #34, the overflow
tax is **zero** here (`rustc -O` 169.5 ms vs `-C overflow-checks=on` 171.4 ms — within
noise), so the residual gap is pure codegen, not checked arithmetic.

**And here Kāra beats Go.** Unlike #34 (where Go edged Kāra at 137 ms), on the
single-search insert loop Kāra's folded `nums[mid]` access pulls **1.60× ahead of
Go** (189.6 ms vs 303.4 ms) — Go's bounds-check elision does not fold the midpoint
access, and `searchInsert` does not inline into the hot loop. No new bug surfaced;
this kata is the fix from #34 paying off on the most-used binary search in the set.

## Benchmarks

Workload: build one fixed strictly-increasing array of length `N = 4096` once
(`nums[p] = 2·p` — distinct, so found and insert positions never collide), then run
the insert query (`lower_bound`) **`TOTAL = 14M`** times for targets cycling through
`[0, 2N)` so all control-flow paths fire (even = exact hit / odd = insert between
neighbours / largest odd = append at `N`), folding each index into a checksum (sink
`862973806`). The target varies with the loop index, so no comparator can hoist the
query out of the loop; the accumulator carries a loop-borne dependency, so it does
not auto-parallelize. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded half-open `lower_bound`)

| | C | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Go | Python |
|---|---|---|---|---|---|---|
| time | 120.2 ms | 169.5 ms | 171.4 ms | **189.6 ms** | 303.4 ms | 5629 ms |
| vs Kāra | 1.58× faster | 1.12× faster | **1.11× faster (= safety)** | — | 1.60× slower | 29.7× slower |

**Within 1.11× of equal-safety Rust, and 1.60× ahead of Go.** The midpoint
`llvm.assume` fix ([`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md), surfaced
by [#34](../34-find-first-and-last-position/)) folds the `nums[mid]` bounds check on
this exact loop, so Kāra sits in the binary-search through-line's band rather than
paying a per-iteration check. The overflow tax is zero (`-O` and
`-C overflow-checks=on` differ by < 1.2%, inside noise), so the residual ~11 % gap
to equal-safety Rust is the genuine distance a branchy, allocation-light search
leaves between Kāra and the systems-language floor (C's no-overhead 1.58×). Go,
whose BCE leaves the midpoint check in, runs the same algorithm 1.60× slower.

**No par lane — by construction.** The query is pure and independent, but karac's
auto-par-on-reduction pass does not fire on this loop (per-call function + checksum
reduction): the default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and
both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.06 MiB | 1.11 MiB | **1.05 MiB** | 2.97 MiB |
| binary size (seq) | **33.4 KiB** | 455.7 KiB | 32.7 KiB | 2434.1 KiB |
| compile elapsed | 73.4 ms | 91.2 ms | **45.7 ms** |
| compile peak RSS | **13.0 MiB** | 26.5 MiB | 2.5 MiB |

The single 4096-element array is the only heap allocation, so runtime RSS ties C and
Rust to within rounding (1.06 / 1.05 / 1.11 MiB). The seq compute binary references
no `String`/par-scheduler runtime, so LTO + `-dead_strip` carve it to **33.4 KiB** —
13.6× under Rust and within a rounding of C's 32.7 KiB. Compile favours Kāra over
`rustc -O` on both elapsed (73.4 vs 91.2 ms) and peak compiler RSS (13.0 vs 26.5
MiB); clang's 45.7 ms is the toolchain floor.

## Kāra features exercised

- **`Vec[i64]` read param from a `ref` borrow** — `search_insert` takes
  `ref Vec[i64]`; `main` builds the array once and forwards it without a call-site
  marker (immutable read borrow). Unlike [#34](../34-find-first-and-last-position/)'s
  bench, `main` does no post-search `nums[lo]` access — the answer is `lo` itself, so
  the search loop is isolated even more cleanly.
- **The binary-search midpoint idiom** — `let mid = lo + (hi - lo) / 2` under a
  strict `while lo < hi`, the pattern that emits `assume(lo <= mid < hi)` and folds
  the `nums[mid]` bounds check ([`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md),
  here on the single-search `lower_bound`, the most common shape of that loop).
- **Half-open vs closed binary search** — the ★ style's `while lo < hi` (half-open,
  the form the fix optimizes) alongside the closed `while lo <= hi` candidate-tracking
  style, plus a fixed-iteration **binary-lifting** form (`pos += step` over
  power-of-two strides) — three distinct factorings of the same `lower_bound`.
- **Empty-/single-element boundaries** — `let a2: Array[i64, 0] = []` and a
  single-element array exercise the append (`lo == len`) and degenerate-window edges
  that regression-guard the binary-search family.

---

**Bug ledger:** no new defect — this kata is the regression witness that
[#34](../34-find-first-and-last-position/)'s midpoint bounds-check fix
([`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md), folds `assume(lo <= mid <
hi)`) generalizes to the single-search canonical `lower_bound`/insert-position loop.
See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md) and
[`docs/investigations/bce_monotonic_assume.md`](../../../../kara/docs/investigations/bce_monotonic_assume.md).
