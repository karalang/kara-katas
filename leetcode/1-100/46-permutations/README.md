# 46. Permutations

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/permutations](https://leetcode.com/problems/permutations/)

Given an array `nums` of **distinct** integers, return **all** the possible orderings of its
elements. There are exactly `n!` of them, and they may be returned in any order.

```
[1,2,3]  →  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
[0,1]    →  [[0,1],[1,0]]
[1]      →  [[1]]
```

**Constraints:** `1 ≤ n ≤ 6`, `-10 ≤ nums[i] ≤ 10`, all integers distinct. Since `n ≤ 6`,
`n! ≤ 720` and every value fits trivially inside `i64`. This is the ordering counterpart of the
combination katas [#39](../39-combination-sum/) and [#40](../40-combination-sum-ii/): there the
index-monotone DFS collapsed each multiset's permutations to one canonical visit; **here the
permutations *are* the answer**, so that shortcut is exactly what we must give up.

## Why this kata — every level may pick any unused element

Because order matters, a permutation DFS has no "never look left of `i`" discipline to lean on:
at each level it may place **any element not yet used on the current branch**, not just elements
to the right of the last pick. The whole problem reduces to *tracking what's still available* and
*undoing each choice on the way back up*. The three canonical solvers are three factorings of
that single fact — they differ only in how availability is tracked and how the path is carried:

| Lens | Idea |
|---|---|
| **Used-array + mutable path** ★ | a parallel `Vec[bool]` marks taken indices; one mutable `path` with push/pop and a lock-step `used[i]` flip/unflip — O(1) availability test, O(n) marker space |
| **In-path membership scan** | no side array — an element is available iff it is not already in `path` (linear scan); distinctness makes "value in path" ⟺ "index used" — O(depth) test, zero marker space |
| **Immutable-snapshot DFS** | carry the path as an owned `Vec` snapshot; each descent builds a fresh child path (`clone` + `push`) and never undoes; the leaf snapshot already *is* the answer |

All three scan the indices `0..n` in order and pick the first available index first, so all three
emit the **identical** "lexicographic by original index" listing — for `[1,2,3]`, exactly
LeetCode's order. The ★ file pays O(n) marker space for an O(1) lookup; the scan file pays an
O(depth) lookup for zero marker space (the classic space-for-time swap); the snapshot file drops
the mutable buffer entirely and pays a per-node clone, the functional shape of
[#40](../40-combination-sum-ii/)'s snapshot solver. It is the same `Vec[Vec]`-allocation footing
as #39/#40, here over an `n!` enumeration rather than a sum-bounded one.

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Used-array + mutable path** ★ | [`permutations.kara`](permutations.kara) | `Vec[bool]` marker + one mutable `path` (push/pop + flag flip), leaf `path.clone()` into `Vec[Vec[i64]]` |
| In-path membership scan | [`permutations_scan.kara`](permutations_scan.kara) | no side array; `contains(path, x)` linear scan as the availability test, same mutable path |
| Immutable-snapshot DFS | [`permutations_snapshot.kara`](permutations_snapshot.kara) | owned `Vec[i64]` snapshot carried by move; fresh child = `clone` + `push`, no undo |

The ★ and scan forms share the mutable-path/push-pop spine and differ only in the availability
test (`Vec[bool]` lookup vs in-path scan); the snapshot form trades the shared buffer and all
pop bookkeeping for a per-node clone. The ★ `Vec[bool]` marker is the sub-word-element collection
that kata [#44](../44-wildcard-matching/) stressed — see that kata's ledger for the
element-store-width fix this relies on.

## What this kata surfaced

All three solvers typechecked, ran, and built correctly on the first pass and agree with the
Python oracle under both `karac run` and `karac build`, including the `Vec[bool]` used-marker that
exercises [#44](../44-wildcard-matching/)'s sub-word element-store fix (`B-2026-06-19-5`). But the
benchmark drove **two compiler fixes**, run down with a `malloc` interposer and a sampling
profiler:

- The workload is **allocator-bound** — a profile of the Kāra binary spent almost all of its
  self-time in `malloc`/`_xzm_free`, while the C mirror spent most of its in `backtrack` compute.
  So the allocation difference *was* the runtime difference.
- A `malloc`-counting interposer showed Kāra issuing **exactly 2× the allocations of C** — 10,080
  per solve vs C's 5,040. IR + per-element counting localized the extra one: **not** the append
  (`out.push(path.clone())` is already a single-alloc move) but the signature loop's
  `let perm = perms[j]`, which **deep-cloned the heap element even though `perm` is only read**.
  Reading via the bare `perms[j][i]` (no element binding) already allocated 1×.
- **Fix 1 — `B-2026-06-19-6` (clone-elision):** a conservative whitelist pass now binds a read-only,
  non-escaping `let r = v[i]` as a *borrow* of the element (no clone, no scope-exit free) when the
  container isn't mutated in scope — anything unproven falls back to the clone, so it can only ever
  *over*-clone, never alias unsafely. The read loop drops from 2 → 1 malloc/elem.
- **Fix 2 — `B-2026-06-19-7` (index-store drop):** writing the negative regression tests surfaced a
  *separate* pre-existing crash — `out[j] = nb` (index-assigning a heap `Vec`/`String` element)
  SIGTRAPped in AOT binaries (double-free of the moved source + leak of the old element). The
  index-store now drops the old element and suppresses the moved source's cleanup, mirroring
  `Vec.push`'s move discipline.

The gap was never a safety tax — `rustc -C overflow-checks=on` (36.8 ms) ties plain `rustc -O`
(36.0 ms) — and it was never the v1 allocator being "just slow": it was one redundant per-element
clone. **With Fix 1, Kāra goes from ~2× behind to ~1.2–1.3× of C/Rust — and now runs *faster than
Go* on this kernel** (§ Benchmarks). The residual ~1.25× is the genuine per-clone cost of the
remaining 5040 leaf snapshots (element-wise copy vs `memcpy`) plus allocator differences — well
inside Kāra's documented v1 bar (`design.md`: "within ~2× apples-to-apples").

## Benchmarks

Workload: a fixed-size `n=7` array `nums` (5040 permutations) is permuted **`TOTAL = 300`** times.
Because the ★ backtracker permutes by **index** (the `Vec[bool]` marker), the element *values* are
free to vary without changing the `n!` count, so each iteration punches one slot
(`nums[k%n] = 1 + k%9`, **not reverted**, so the array state carries forward) before solving. Every
permutation's position-weighted signature plus the count is folded into a rolling checksum (sink
`75196912`). The punched values vary with the loop index (no hoisting of the otherwise-constant
permutation set) and the checksum carries a loop-borne dependency, so this is a single-lane (seq)
bench by construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded used-array backtracking)

Measured with the clone-elision fix (`B-2026-06-19-6`) landed:

| | Rust (`-O`) | Rust (`overflow-checks=on`) | C | **Kāra** | Go | Python |
|---|---|---|---|---|---|---|
| time | 36.0 ms | 36.8 ms | 38.4 ms | **47.0 ms** | 49.0 ms | 725.9 ms |
| vs Kāra | 1.30× faster | 1.28× faster (= safety) | 1.22× faster | — | 1.04× slower | 15.4× slower |

This is an **allocation-bound** workload — 5040 leaf `Vec[i64]` snapshots per solve into a growing
`Vec[Vec[i64]]`. Before the fix Kāra trailed native by ~2× (73.4 ms), which a `malloc` interposer
pinned to Kāra issuing exactly 2× C's allocations — the signature loop's `let perm = perms[j]`
deep-cloned each element it only read. With that clone elided (`B-2026-06-19-6`) Kāra drops to
**47.0 ms — ~1.2–1.3× of C/Rust, and now faster than Go**. The safety-matched comparator confirms
the residual isn't arithmetic: at **equal safety** `rustc -C overflow-checks=on` (36.8 ms) ties
plain `rustc -O` (36.0 ms). What's left is the genuine cost of the 5040 remaining leaf clones
(element-wise copy vs `memcpy`) plus allocator differences. Python runs the identical algorithm
interpreted, 15× behind.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.67 MiB | 1.72 MiB | **1.64 MiB** | 9.1 MiB |
| binary size (seq) | 33.4 KiB | 455.9 KiB | **33.0 KiB** | 2434.1 KiB |
| compile elapsed | 79.2 ms | 105.4 ms | **49.7 ms** |
| compile peak RSS | 13.9 MiB | 31.3 MiB | **2.5 MiB** |

Runtime peak RSS is a three-way tie among the native mirrors — Kāra **1.67 MiB**, C 1.64 MiB, Rust
1.72 MiB, all within noise — while Go's runtime pays 9.1 MiB and Python's interpreter 8.9 MiB. The
seq compute binary references no par-scheduler runtime, so LTO + `-dead_strip` carve it to
**33.4 KiB**, within a rounding of C's 33.0 KiB and 13.6× under Rust. Compile favours Kāra over
`rustc -O` on both elapsed (79.2 vs 105.4 ms) and peak compiler RSS (13.9 vs 31.3 MiB); clang's
49.7 ms / 2.5 MiB is the floor.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par pass does not fire: the default and
`KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded — same as
[#45](../45-jump-game-ii/).

## Kāra features exercised

- **`Vec[bool]` used-marker** — the ★ solver allocates a `Vec[bool]` of length n and flips
  `used[i]` in lock step with the path, exercising the sub-word element store/load that kata
  [#44](../44-wildcard-matching/) stressed (its `B-2026-06-19-5` element-store-width fix); it
  typechecks, runs, and builds clean here.
- **`Vec[Vec[i64]]` accumulation with leaf `path.clone()`** — the shared backtracking spine of
  #39/#40, here driving an `n!` enumeration: per-node push/pop on the mutable path plus a snapshot
  clone at each of the 5040 leaves into a growing nested Vec — the allocation-churn workload the
  benchmark characterizes.
- **Owned-snapshot recursion (functional carriage)** — the snapshot solver carries the path as an
  owned `Vec[i64]` moved into the recursive call, building a fresh `clone`+`push` child per descent
  with no undo, the immutable-snapshot contrast to the two mutable-path forms.
- **`mut ref` threading + call-site markers** — `used`, `path`, and the accumulator thread through
  the recursion as `mut ref` bindings; the root call writes the `mut` markers (fresh owned
  bindings) and interior calls forward them unmarked, per the call-site-marker rule.
- **Checked integer arithmetic at zero cost** — the index math and the position-weighted checksum
  fold run under Kāra's default overflow checking and land dead-even with `rustc -C
  overflow-checks=on`; the seq-lane residual here is allocation, not arithmetic.

---

**Bug ledger:** no *correctness* bug in the solvers — all three typechecked, ran, and built
correctly on the first pass and agree with the oracle under both `karac run` and `karac build`. The
benchmark drove **two `karac` codegen fixes**, both landed:

- **`B-2026-06-19-6` (clone-elision, fixed):** a read-only `let perm = perms[j]` over a `Vec[Vec]`
  deep-cloned the heap element it only read — Kāra issued exactly 2× the C/Rust allocations (10,080
  vs 5,040 per solve), confirmed with a `malloc` interposer and an allocator-bound profile. A
  conservative whitelist pass now binds such a read-only, non-escaping index element as a *borrow*
  (no clone, no scope-exit free) when the container isn't mutated in scope. Seq lane: **73.4 → 47.0
  ms**, from ~2× behind to ~1.2–1.3× of C/Rust and ahead of Go.
- **`B-2026-06-19-7` (index-store drop, fixed):** found while writing the negative regression
  tests — `out[j] = nb` (index-assigning a heap `Vec`/`String` element) SIGTRAPped in AOT binaries
  (double-free of the moved source + leak of the old element). The index-store now drops the old
  element and suppresses the moved source's cleanup.

The residual ~1.25× is the genuine per-clone cost of the 5040 remaining leaf snapshots
(element-wise copy vs `memcpy`), well inside the documented v1 bar (`design.md`: "within ~2×
apples-to-apples"). See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the
cross-kata history.
