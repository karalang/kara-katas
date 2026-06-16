# 33. Search in Rotated Sorted Array

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/search-in-rotated-sorted-array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

A sorted ascending array of **distinct** values has been rotated at an unknown
pivot — e.g. `[0,1,2,4,5,6,7]` becomes `[4,5,6,7,0,1,2]`. Given the rotated array
and a `target`, return its index, or `-1`. The catch: it must run in **O(log n)**.

```
[4,5,6,7,0,1,2], target = 0  →  4
[4,5,6,7,0,1,2], target = 3  →  -1
[1],            target = 0  →  -1
```

**Constraints:** `1 ≤ nums.length ≤ 5000`; all values distinct; `-10⁴ ≤ nums[i], target ≤ 10⁴`.

## Why this kata — binary search where half the invariant is broken

Plain binary search needs a fully sorted array; rotation breaks that globally but
**not locally** — at any midpoint, the rotation pivot can fall in only one of the
two halves, so the *other* half is still perfectly sorted. Every approach here
turns on that one fact; they differ in how they exploit it:

| Lens | Idea |
|---|---|
| **One-pass** | at each `mid`, decide which half is sorted, range-test the target against that (sorted) half, recurse into the half that must contain it |
| **Find-pivot + search** | binary-search the rotation point first, then run a textbook binary search on the one sorted segment the target can be in |
| **Find-pivot + remap** | find the rotation `rot`, then binary-search the *logical* sorted view, reading each probe through `(mid + rot) % n` |

The pedagogical arc: the one-pass form folds the rotation into the search logic
(harder to get right, no second pass); the two pivot-based forms *separate* the
rotation from the search (a clean find-then-search, at the cost of a second
O(log n) pass). All three are O(log n).

## Approaches

Three styles, all byte-identical to the Python oracle across all 22 cases, under
`karac run` **and** `karac build` (the oracle additionally cross-checks the three
algorithms against each other and against Python's own `index`).

| Approach | File | Shape |
|---|---|---|
| **One-pass modified binary search** ★ | [`search_rotated.kara`](search_rotated.kara) | one window; `nums[lo] <= nums[mid]` picks the sorted half, a single bound test picks the direction — no pivot pre-pass, no allocation |
| Find-pivot + binary search | [`search_rotated_pivot.kara`](search_rotated_pivot.kara) | binary-search the minimum's index, then a reusable textbook `bsearch` on the segment `nums[0]`'s range selects |
| Find-pivot + index remap | [`search_rotated_remap.kara`](search_rotated_remap.kara) | find `rot`, then one ordinary sorted-array binary search over the logical range, each probe read through `(mid + rot) % n` |

The one-pass is the tightest (one branchy loop); the pivot-split factors out the
exact `bsearch` [#704](https://leetcode.com/problems/binary-search/) would use
directly; the remap is the cleanest separation — the search never knows the array
was rotated, the rotation living entirely in one `%` per probe.

## What this kata uncovered

**A codegen bug — [`B-2026-06-14-30`](../../../../kara/docs/bug-ledger.md).** This
is the first of the binary-search/array katas to hit a real `karac` defect, and
the edge case that surfaced it is mundane: an **empty array** in the test battery.

```kara
let a7: Array[i64, 0] = [];
report(a7, 0, 5);              // -1 — the len==0 guard must be safe
```

`karac run` (interpreter) handled `a7` fine, but `karac build` **hard-failed**:

```
error: codegen failed: Module verification failed:
  "Call parameter type does not match function signature!
   %a737 = load i64, ptr %a7   { ptr, i64 } call void @report(i64 %a737, i64 0, i64 5)"
```

Root cause: `compile_array_literal([])` can't infer the element type from an empty
element list, so it returned a scalar `i64 0` sentinel — and the binding's slot
type was registered as `i64`, not `[0 x i64]`. At the call site, the Array → Slice
coercion (`coerce_to_slice`) keys on the slot being an LLVM `ArrayType`, so it
**skipped** the empty array; the raw `i64` then reached the `Slice[i64]` parameter
where a `{ptr, i64}` fat pointer was expected, failing LLVM module verification.
Only the codegen backend surfaced it — the interpreter does not lower to fat
pointers, so `karac run` accepted the same `[] → Slice` coercion silently.

**Fixed** (`36e9d82f`): a new `try_emit_empty_array_let` in the codegen
let-binding path recovers the element type from the `Array[T, N]` annotation and
allocates a real `[0 x T]` slot, so an empty array coerces to a zero-length slice
header `{ptr, 0}` like any other array (length 0, so the pointer is never
dereferenced). Non-empty bindings and the no-annotation empty literal are
unaffected. Regression-guarded by `tests/codegen.rs::test_e2e_empty_array_binding_to_slice_param`.
This is exactly the kata-as-bug-finder loop: the empty-array boundary case is not
part of the LeetCode problem (`len ≥ 1`), but exercising it is what flushed a
latent codegen gap that any future `Array[T, 0] = []` → `Slice` would have hit.

## Benchmarks

Workload: build one fixed rotated-sorted array of length `N = 4096` once (values
`2·((p+ROT)%N)` — even, so odd targets miss), then run the ★ one-pass `search`
**`TOTAL = 18M`** times for targets cycling through `[0, 2N)` so ~half hit and
~half miss (both control-flow paths), folding each result index into a checksum
(sink `455834850`). The target varies with the loop index, so no comparator can
hoist the pure call out of the loop; the accumulator carries a loop-borne
dependency, so it does not auto-parallelize. Apple M5 Pro; `bench/bench.sh`
(`hyperfine`).

### Seq lane — runtime (single-threaded rotated binary search)

| | C | Rust (`-O`) | Go | **Kāra** | Rust (`overflow-checks=on`) | Python |
|---|---|---|---|---|---|---|
| time | 211.3 ms | 283.8 ms | 289.9 ms | **309.5 ms** | 311.3 ms | 9827 ms |
| vs Kāra | 1.46× faster | 1.09× faster | 1.07× faster | — | **1.01× (tied at = safety)** | 32× slower |

**A branchy, data-dependent compute kernel — and the cleanest equal-safety read
yet.** Binary search's direction at each step depends on a comparison the branch
predictor can't pre-resolve, and the arithmetic is light (a `mid`, a `%` for the
checksum). That makes the overflow-check tax the dominant Kāra-vs-Rust variable:
`rustc -O` (wrap) runs 284 ms, but turning Rust's checks **on** to match Kāra's
checked-by-default semantics (design.md § Arithmetic Overflow) costs it 284 → 311
ms (+9.7 %). Kāra lands at **310 ms — dead even with equal-safety Rust** (a hair
ahead). The unchecked tier — wrapping `rustc -O` (284) and Go (290, no integer
overflow checking either) — is ~1.07–1.09× faster precisely because it skips the
checks this loop still pays per step; C's no-overhead floor is 1.46×. The honest
one-liner: **at equal overflow safety Kāra ties Rust on branchy search; the gap to
the headline `rustc -O` number is the overflow-check tax, not a codegen deficit.**

**No par lane — by construction.** Each search is independent, but karac's
auto-par-on-reduction pass does not fire on this loop (per-call function +
modulo reduction): verified, the default and `KARAC_AUTO_PAR=0` binaries are
**byte-identical** and both run single-threaded (cpu 99.6 %).

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.06 MiB | 1.11 MiB | **1.05 MiB** | 2.95 MiB |
| binary size (seq) | **33.4 KiB** | 455.7 KiB | 32.7 KiB | 2434.1 KiB |
| compile elapsed | **74.1 ms** | 90.9 ms | 46.6 ms |
| compile peak RSS | **13.0 MiB** | 26.7 MiB | 2.6 MiB |

The single 4096-element array is the only heap allocation, so runtime RSS ties C
and Rust to within rounding (1.06 / 1.05 / 1.11 MiB). The seq compute binary
references no `String`/par-scheduler runtime, so LTO + `-dead_strip` carve it to
**33.4 KiB** — 13.6× under Rust. Compile favors Kāra over `rustc -O` on both
elapsed (74.1 vs 90.9 ms) and peak compiler RSS (13.0 vs 26.7 MiB).

**Where this lands.** With [#31](../31-next-permutation/) (in-place compute,
tied), [#32](../32-longest-valid-parentheses/) (alloc-churn, Kāra ahead at equal
safety), and now #33 (branchy search, tied at equal safety), the through-line
holds: when a workload is compute-bound and allocation-light, Kāra sits on the
systems-language floor — and the only consistent gap to the *headline* Rust number
is the overflow safety Kāra never turns off.

## Kāra features exercised

- **`Slice[i64]` read params from arrays** — `search`/`fmt` take `Slice[i64]`;
  `main` passes owned `Array[i64, N]` bindings (and the empty `Array[i64, 0]`)
  without a call-site marker (immutable read borrow), `report` forwards them on.
- **Data-dependent branchy control flow** — the "which half is sorted" double
  branch + bound test, the upper/lower window updates, the `len == 0` guard.
- **Empty-array boundary** — `let a7: Array[i64, 0] = []` to a `Slice` param, the
  case that surfaced and now regression-guards [`B-2026-06-14-30`](../../../../kara/docs/bug-ledger.md).
- **Index-remap arithmetic** — the remap style's `(mid + rot) % len` logical→
  physical probe, and the pivot styles' reusable textbook `bsearch`.

---

**Bug ledger:** surfaced **`B-2026-06-14-30`** (empty `Array[T,0]` → `Slice`
codegen verification failure), fixed `36e9d82f` with a codegen regression test.
See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
