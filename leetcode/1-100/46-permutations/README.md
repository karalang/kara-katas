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

**No compiler change was needed — all three solvers typechecked, ran, and built correctly on the
first pass,** and all three agree with the Python oracle under both `karac run` and `karac build`,
including the `Vec[bool]` used-marker that exercises the recently-fixed sub-word element-store
path ([#44](../44-wildcard-matching/)'s `B-2026-06-19-5`). The benchmark, though, *characterizes*
a sharply-localized **allocation gap**, run down with a `malloc` interposer and a sampling
profiler:

- The workload is **allocator-bound** — a profile of the Kāra binary spends almost all of its
  self-time in `malloc`/`_xzm_free`, while the C mirror spends most of its time in `backtrack`
  compute. So whatever the allocation difference is, it *is* the runtime difference.
- A `malloc`-counting interposer shows Kāra issues **exactly 2× the allocations of C** — 10,080
  per solve vs C's 5,040 (one per permutation leaf). The 2× runtime gap *is* the 2× allocation
  count.
- The extra allocation is **one redundant `malloc`+`free` per element when a heap-owning value is
  appended to a `Vec[Vec]`**. Cloning a small `Vec[i64]` without appending it costs 1 `malloc`;
  `out.push(v.clone())` into a `Vec[Vec[i64]]` whose contents are read costs **2** — verified
  per-element (scales 1:1 with element count, not with capacity growth), and present whether the
  clone is written inline or `let`-bound first. The C/Rust mirrors do the identical append in a
  single allocation. Minimal repro: a 6-line loop of `out.push(v.clone())` with the contents read
  → 2× the `malloc`s of the C equivalent.

Crucially the gap is **not a safety tax**: `rustc -C overflow-checks=on` (37.2 ms) ties plain
`rustc -O` (36.7 ms) to within noise, so the checked integer math is free here. And it is **not**
the v1 allocator baseline being "just slow" — Kāra's runtime peak RSS is in fact the *lowest* of
all four native mirrors (1.69 MiB, under even C) and its binary ties C at 33 KiB. It is one
specific redundant per-element copy on `Vec[Vec]` append: eliminating it (a move where the codegen
currently copies the element buffer) would roughly **halve allocation traffic and bring this
kernel to ~parity with C**, since the workload is allocator-bound. That is squarely the roadmap's
stated #1 optimization lever ("allocation reduction on hot paths"); the ~2× sits *at* Kāra's
documented v1 bar (`design.md`: "within ~2× apples-to-apples"), with parity deferred to the
Phase 11 codegen pass.

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

| | Rust (`-O`) | Rust (`overflow-checks=on`) | C | Go | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 36.7 ms | 37.2 ms | 39.1 ms | 50.5 ms | **73.4 ms** | 741.6 ms |
| vs Kāra | 2.00× faster | 1.97× faster (= safety) | 1.88× faster | 1.45× faster | — | 10.1× slower |

This is an **allocation-bound** workload — 5040 leaf `Vec[i64]` clones per solve into a growing
`Vec[Vec[i64]]` — and Kāra trails native by ~2×, which a `malloc` interposer pins to Kāra issuing
**exactly 2× C's allocations** (one redundant `malloc`+`free` per `Vec[Vec]` append; see *What this
kata surfaced*). The safety-matched comparator rules out arithmetic: at **equal safety** Rust is
still 1.97× faster, and `rustc -C overflow-checks=on` (37.2 ms) ties plain `rustc -O` (36.7 ms), so
the checked integer math costs nothing here. Go's GC'd allocator lands between (1.45×). Python runs
the identical algorithm interpreted, 10× behind.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.69 MiB** | 1.77 MiB | 1.78 MiB | 9.1 MiB |
| binary size (seq) | 33.4 KiB | 455.9 KiB | **33.0 KiB** | 2434.1 KiB |
| compile elapsed | 84.2 ms | 114.0 ms | **54.4 ms** |
| compile peak RSS | 14.0 MiB | 31.3 MiB | **2.6 MiB** |

Despite being slower per op, Kāra holds the **lowest runtime peak RSS of the four — 1.69 MiB,
under even C's 1.78 MiB** — the small-object churn pool stays tighter than malloc's footprint here,
while Go's runtime pays 9.1 MiB and Python's interpreter 8.9 MiB. The seq compute binary references
no par-scheduler runtime, so LTO + `-dead_strip` carve it to **33.4 KiB**, within a rounding of C's
33.0 KiB and 13.6× under Rust. Compile favours Kāra over `rustc -O` on both elapsed (84.2 vs
114.0 ms) and peak compiler RSS (14.0 vs 31.3 MiB); clang's 54.4 ms / 2.6 MiB is the floor.

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
  overflow-checks=on`; the seq-lane gap here is allocation, not arithmetic.

---

**Bug ledger:** no *correctness* bug — all three solvers typechecked, ran, and built correctly on
the first pass and agree with the oracle under both `karac run` and `karac build`. The benchmark
contributes a precisely-localized **performance characterization** (a candidate optimization, not a
miscompile): appending a heap-owning value to a `Vec[Vec]` (`out.push(v.clone())`) emits **one
redundant per-element `malloc`+`free`** — Kāra issues exactly 2× the allocations of the C/Rust
mirrors (10,080 vs 5,040 per solve), confirmed with a `malloc` interposer and a sampling profile
showing the workload is allocator-bound. The append currently *copies* the element buffer where a
*move* would do; eliminating the copy would roughly halve allocation traffic and bring this
allocator-bound kernel to ~parity with C. The ~2× sits *at* the documented v1 bar (`design.md`:
"within ~2× apples-to-apples") and the fix is the roadmap's #1 lever ("allocation reduction on hot
paths"), with parity deferred to the Phase 11 codegen pass. Minimal repro: a loop of
`out.push(v.clone())` into a `Vec[Vec[i64]]` whose contents are read → 2× the `malloc`s of the C
equivalent. See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the cross-kata
history.
