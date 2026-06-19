# 47. Permutations II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/permutations-ii](https://leetcode.com/problems/permutations-ii/)

Given an array `nums` that **may contain duplicates**, return **all the unique** orderings of its
elements, in any order.

```
[1,1,2]    →  [[1,1,2],[1,2,1],[2,1,1]]
[1,2,3]    →  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
[3,3,0,3]  →  [[0,3,3,3],[3,0,3,3],[3,3,0,3],[3,3,3,0]]
```

**Constraints:** `1 ≤ n ≤ 8`, `-10 ≤ nums[i] ≤ 10`. The `n! ≤ 40320` upper bound on the listing
and every value fit trivially inside `i64`. This is the **duplicate-input twin** of kata
[#46](../46-permutations/) exactly as [#40](../40-combination-sum-ii/) is the duplicate-input twin
of [#39](../39-combination-sum/): #46 had *distinct* integers, so its any-unused-element DFS already
emitted each ordering once; **the moment the input repeats a value, that same DFS emits each
ordering once per arrangement of the equal copies** — two `1`s in `[1,1,2]` would print `[1,1,2]`
twice. The whole kata is *suppressing those duplicate siblings*.

## Why this kata — suppress the duplicate siblings, three ways

A run of equal values may be **consumed down a single branch** (a permutation like `[1,1,2]` really
does place both `1`s) but may not be **started more than once at the same tree level** — the second
start would re-enumerate a subtree the first already covered. The four canonical solvers are four
factorings of that single fact; they differ only in *how a level decides a value is a repeat sibling*
and *how the path is carried*:

| Lens | Idea |
|---|---|
| **Sorted + used-array, adjacent skip** ★ | sort so equals are adjacent; a `Vec[bool]` `used` marker + mutable path; skip index `i` when `nums[i] == nums[i-1] and not used[i-1]` — one backward look, the permutation analog of #40's `i > start` guard |
| **Counted multiset DFS** | collapse the sorted input into distinct `(value, count)` groups; fill each position by offering each distinct value once (count `> 0`), decrement/recurse/increment — dedup is *structural*, no `used` array, no adjacency test |
| **Immutable-snapshot, shrinking remaining** | carry both the chosen prefix **and** the sorted still-available multiset as owned `Vec` snapshots; descend by removing one element and appending one, never undoing; an *unconditional* adjacent skip suffices because consumed elements are already gone from `remaining` |
| **In-place swap + per-level seen-`Set`** | no separate path and no sort: permute the array in place — swap each distinct value into position `start`, recurse, swap back; dedup via a per-level `Set[i64]` of values already fixed. The swap is a **parallel assignment** (`nums[start], nums[i] = nums[i], nums[start]`); output is canonicalized by sorting |

Because all three sort first and always take the smallest eligible value at each level, all three
emit the **identical** "lexicographic **by value**" listing — for `[1,1,2]`, exactly
`[1,1,2],[1,2,1],[2,1,1]`. That is the visible contrast with #46, whose distinct, *unsorted* input
came out "lexicographic **by original index**": adding duplicates forces the sort, and the sort
reorders the output. The ★ file pays an `O(n)` marker plus a one-line adjacency check; the counted
file pays an `O(distinct)` per-level scan for zero marker and no adjacency logic; the snapshot file
drops every mutable buffer and pays a per-node `clone` of *two* shrinking vectors — the functional
shape of [#40](../40-combination-sum-ii/)'s and [#46](../46-permutations/)'s snapshot solvers.

## Approaches

Four styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Sorted + used-array, adjacent skip** ★ | [`permutations_ii.kara`](permutations_ii.kara) | sort, `Vec[bool]` marker + mutable `path` (push/pop + flag flip), skip `nums[i]==nums[i-1] and not used[i-1]`, leaf `path.clone()` into `Vec[Vec[i64]]` |
| Counted multiset DFS | [`permutations_ii_counted.kara`](permutations_ii_counted.kara) | run-group into `vals`/`cnts`; offer each distinct value once per position, count as availability + undo ledger |
| Immutable-snapshot DFS | [`permutations_ii_snapshot.kara`](permutations_ii_snapshot.kara) | owned `(remaining, path)` snapshots carried by move; child = `remaining` minus index `i` and `path.clone()+push`, unconditional adjacent skip |
| In-place swap + seen-`Set` | [`permutations_ii_swap.kara`](permutations_ii_swap.kara) | permute in place via **parallel assignment** swap `nums[start], nums[i] = nums[i], nums[start]`; per-level `Set[i64]` dedup; output canonicalized by an insertion sort (rows swapped by parallel assignment too) |

The ★ and counted forms share the mutable-path/push-pop spine and differ only in *what proves a
value is a repeat sibling* (`not used[i-1]` after the adjacent value vs each distinct value being
offered at most once); the snapshot form trades both the shared buffer and the `used` marker for a
per-node clone of the shrinking available-set; the swap form drops the auxiliary path entirely and
mutates the array itself, deduping with a real hash `Set`. The ★ `Vec[bool]` marker is the
sub-word-element collection that kata [#44](../44-wildcard-matching/) stressed — see that kata's
ledger for the element-store-width fix this relies on.

## What this kata surfaced

**A real language gap — now fixed in `karac`.** The first three solvers typechecked, ran, and built
correctly on the first pass, but they all reuse idioms already proven by #46/#40/#44 — a regression
test, not a bug-find. Probing the *fourth* canonical approach (the in-place **swap** DFS) is what
surfaced the gap: the natural swap `nums[start], nums[i] = nums[i], nums[start]` did not parse —
Kāra had **no parallel/destructuring assignment**. That is exactly the construct swap-based sorts
and permutation enumerators reach for, so it blocked a whole family of natural solvers, not just this
one. Rather than route around it (a manual three-line temp swap), the compiler was fixed: parallel
assignment `t1, …, tn = v1, …, vn;` now parses and lowers (evaluate every RHS into a temporary before
writing any target, so it is a true swap), with parser + codegen tests. The swap solver above is
written in its natural form on top of that fix.

One *false* alarm is worth recording: the same probe first reported "no hash set." That was a naming
error — Kāra's hash containers are **`Set[T]` / `Map[K,V]`** (not the Rust `HashSet`/`HashMap`), and
they work under both `karac run` and `karac build`. The swap solver's per-level dedup uses the real
`Set[i64]`; nothing was missing there.

Beyond the new feature, the kata remains a clean *regression exercise* of three prior fixes it
depends on to stay native-competitive:

- the ★ solver's `Vec[bool]` `used` marker is the sub-word element store/load that kata
  [#44](../44-wildcard-matching/) hardened (`B-2026-06-19-5`, element-store-width);
- the benchmark's signature loop reads each permutation with `let perm = perms[j]` over a
  `Vec[Vec[i64]]`, the exact read-only index binding that kata [#46](../46-permutations/) taught the
  compiler to bind as a *borrow* rather than deep-clone (`B-2026-06-19-6`, clone-elision) — without
  it this kernel would issue 2× the allocations, as #46 did before the fix;
- the shared backtracking spine (`out.push(path.clone())` into a growing nested `Vec`) is the
  move-disciplined append that #46's `B-2026-06-19-7` work also touched.

The headline result is that **Kāra lands dead-even with C and ahead of both Rust and Go** on this
kernel (§ Benchmarks) — *stronger* than #46, where it trailed native by ~1.25×. The reason is
structural: #47's kernel **sorts every iteration** (allocation-free compute) and the duplicate skip
**prunes the leaf-snapshot count**, so the `Vec[Vec]`-allocation fraction that cost #46 is diluted
by more pointer-chasing compute — and at that mix Kāra's codegen closes the gap to parity. The
safety-matched comparator confirms the residual isn't arithmetic: `rustc -C overflow-checks=on`
(51.2 ms) is actually *slower* than Kāra (48.9 ms) here.

## Benchmarks

Workload: a fixed-size `n=8` multiset `nums` drawn from `{1,2,3,4}` (so always duplicate-heavy) is
permuted **`TOTAL = 600`** times. Each iteration punches one slot (`nums[k%n] = 1 + k%4`, **not
reverted**, so the multiset state carries forward), then `permute_unique` sorts its **own working
copy** (the caller's array stays in punch order) and enumerates the unique permutations. Every
permutation's position-weighted signature plus the count is folded into a rolling checksum (sink
`863540794`). The punched values vary with the loop index (no hoisting of an otherwise-constant
result) and the checksum carries a loop-borne dependency, so this is a single-lane (seq) bench by
construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded sorted adjacent-skip backtracking)

| | C | **Kāra** | Rust (`-O`) | Rust (`overflow-checks=on`) | Go | Python |
|---|---|---|---|---|---|---|
| time | 48.2 ms | **48.9 ms** | 49.8 ms | 51.2 ms | 58.2 ms | 1049.5 ms |
| vs Kāra | 1.02× faster | — | 1.02× slower | 1.05× slower (= safety) | 1.19× slower | 21.5× slower |

This is the same **allocation-bound** `Vec[Vec]` enumeration as #46 — per-iteration leaf
`Vec[i64]` snapshots into a growing `Vec[Vec[i64]]` — but with two compute additions that dilute the
allocation fraction: a per-iteration `sort_by` and the adjacent-duplicate skip (which also *reduces*
the number of leaves). At that mix Kāra is **dead-even with C** (48.9 vs 48.2 ms, a 1.5% gap inside
run-to-run noise) and **faster than both `rustc -O` and the safety-matched
`rustc -C overflow-checks=on`** — a stronger showing than #46's ~1.25×-behind, for the same codegen.
The clone-elision fix from #46 (`B-2026-06-19-6`) is load-bearing here: the signature loop's
`let perm = perms[j]` borrows rather than deep-clones each permutation it only reads, keeping Kāra
at C's allocation count. Go's mean carries a large outlier (σ = 22 ms; median 52.7 ms, so ~1.1×
slower than Kāra by median); Python runs the identical algorithm interpreted, ~21× behind.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.55 MiB | 1.52 MiB | **1.41 MiB** | 9.8 MiB |
| binary size (seq) | 33.4 KiB | 456.0 KiB | **33.0 KiB** | 2452.2 KiB |
| compile elapsed | 91.8 ms | 146.5 ms | **53.3 ms** |
| compile peak RSS | 14.7 MiB | 39.4 MiB | **2.6 MiB** |

Runtime peak RSS is a three-way tie among the native mirrors — Kāra **1.55 MiB**, C 1.41 MiB, Rust
1.52 MiB, all within noise — while Go's runtime pays 9.8 MiB and Python's interpreter 14.0 MiB. The
seq compute binary references no par-scheduler runtime, so LTO + `-dead_strip` carve it to
**33.4 KiB**, within a rounding of C's 33.0 KiB and 13.7× under Rust. Compile favours Kāra over
`rustc -O` on both elapsed (91.8 vs 146.5 ms, 1.6× faster) and peak compiler RSS (14.7 vs 39.4 MiB,
2.7× lighter); clang's 53.3 ms / 2.6 MiB is the floor.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par pass does not fire: the default and
`KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded — same as
[#45](../45-jump-game-ii/) and [#46](../46-permutations/).

## Kāra features exercised

- **Per-iteration `sort_by` in the hot kernel** — `xs.sort_by(|a, b| a.cmp(b))` runs every solve
  before the DFS (equals must be adjacent for the skip), the closure-comparator sort of #15/#40 now
  inside an allocation-bound loop; it is the compute that dilutes the `Vec[Vec]`-allocation fraction
  and lets Kāra close to C parity.
- **`Vec[bool]` used-marker** — the ★ solver flips `used[i]` in lock step with the path, exercising
  the sub-word element store/load that kata [#44](../44-wildcard-matching/) stressed
  (`B-2026-06-19-5`); it typechecks, runs, and builds clean here.
- **`Vec[Vec[i64]]` accumulation with leaf `path.clone()`** — the shared backtracking spine of
  #39/#40/#46, here driving a duplicate-suppressed `n!` enumeration: per-node push/pop on the
  mutable path plus a snapshot clone at each leaf into a growing nested Vec, and the read-only
  `let perm = perms[j]` index-borrow (#46's `B-2026-06-19-6`) on the way back out.
- **Run-length grouping + counter ledger** — the counted solver run-groups the sorted multiset into
  parallel `vals`/`cnts` (the #38 indexed run read) and uses the counters as both the availability
  test and the undo ledger (`cnts[i] -= 1` / recurse / `+= 1`), the count-based replacement for the
  `used` flip.
- **Two-snapshot functional recursion** — the snapshot solver carries `(remaining, path)` as owned
  `Vec[i64]` values moved into each call, rebuilding a shrunk `remaining` and an extended `path` per
  descent with no undo — the immutable-snapshot contrast to the two mutable-path forms, carrying the
  *available set* by value rather than via a marker.
- **Parallel/destructuring assignment (new)** — the swap solver's `nums[start], nums[i] =
  nums[i], nums[start]` (and its row swap `out[b], out[b-1] = out[b-1], out[b]`) use the
  parallel-assignment construct this kata drove into `karac`: every RHS is read before any target is
  written, so it is a genuine two-slot swap with no manual temp — over both plain `i64` slots and
  heap `Vec[i64]` rows.
- **`Set[i64]` hash set** — the swap solver's per-level duplicate suppression keeps a `Set[i64]` of
  values already fixed into the current position (`seen.contains` / `seen.insert`), the no-sort
  alternative to the adjacent skip; it typechecks, runs, and builds clean.
- **Checked integer arithmetic at zero cost** — the index math and the position-weighted checksum
  fold run under Kāra's default overflow checking and come in *ahead* of `rustc -C
  overflow-checks=on`; the seq-lane result here is set by allocation/compute mix, not arithmetic.

---

**Bug ledger:** one language gap, fixed. Probing the swap-based solver surfaced that Kāra had **no
parallel/destructuring assignment** — `nums[start], nums[i] = nums[i], nums[start]` failed to parse,
blocking the natural in-place swap that swap-sorts and permutation enumerators rely on. Fixed in
`karac` (parser-level desugaring of `t1, …, tn = v1, …, vn;` into a temp-block that evaluates every
RHS before writing any target, so it swaps; parser + codegen E2E tests, full suites green). A *false*
gap was also recorded and corrected: hash containers exist as `Set[T]` / `Map[K,V]` (not the Rust
`HashSet`/`HashMap`), so no stdlib work was needed — the swap solver's dedup uses the real `Set[i64]`.

The four solvers otherwise remain a clean regression exercise of three prior `karac` fixes — the
`Vec[bool]` element-store-width fix (`B-2026-06-19-5`, kata [#44](../44-wildcard-matching/)), the
read-only index-binding clone-elision (`B-2026-06-19-6`, kata [#46](../46-permutations/)) that keeps
this allocation-bound kernel at C's allocation count, and the move-disciplined nested-`Vec` append
(`B-2026-06-19-7`, kata [#46](../46-permutations/)). With those in place Kāra lands **dead-even with
C and ahead of Rust and Go** on this kernel — well inside the documented v1 bar (`design.md`: "within
~2× apples-to-apples"). See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the
cross-kata history.
