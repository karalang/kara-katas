# 48. Rotate Image

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Math, Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/rotate-image](https://leetcode.com/problems/rotate-image/)

Given an `n x n` matrix, rotate it **90 degrees clockwise, in place** — the follow-up forbids
allocating a second matrix.

```
[[1,2,3],            [[7,4,1],
 [4,5,6],     →       [8,5,2],
 [7,8,9]]             [9,6,3]]

[[5, 1, 9,11],       [[15,13, 2, 5],
 [2, 4, 8,10],   →    [14, 3, 4, 1],
 [13,3, 6, 7],        [12, 6, 8, 9],
 [15,14,12,16]]       [16, 7,10,11]]
```

**Constraints:** `1 ≤ n ≤ 20`, `-1000 ≤ matrix[i][j] ≤ 1000`. Every value fits trivially inside
`i64`.

## Why this kata — one index map, four factorings

Every clockwise rotation is the same index map, stated two equivalent ways:

```
new[i][j] = old[n-1-j][i]          old[i][j] lands at new[j][n-1-i]
```

The four canonical solvers differ only in *how they realise that map* and *whether they touch a
second buffer*:

| Lens | Idea |
|---|---|
| **Layer four-way cyclic swap** ★ | walk concentric rings; rotate each ring a quarter-turn by cycling four cells at a time — `top, right, bottom, left = left, top, right, bottom`, a **four-target parallel assignment**, no temporary. `O(1)` extra space |
| **Transpose + reverse rows** | two in-place passes: transpose across the main diagonal (`m[i][j] ↔ m[j][i]`), then reverse each row. Transpose-then-row-reverse = a clockwise quarter-turn. `O(1)` extra space |
| **Reverse row-order + transpose** | the dual identity: flip the matrix top-to-bottom (reverse the *order* of the rows — a whole-row swap), then transpose. `O(1)` extra space |
| **Out-of-place index map** | the straight-line statement: allocate a fresh grid and scatter `dst[j][n-1-i] = src[i][j]`. `O(n²)` extra space — fails the in-place follow-up, kept as the explicit-mapping contrast |

The first three never allocate (the matrix is its own scratch); the fourth names the arithmetic the
other three encode implicitly. All four emit the **identical** rotated matrix on every case.

This is the **multi-target-parallel-assignment twin** of kata [#47](../47-permutations-ii/): #47
introduced parallel assignment into `karac` and exercised the *two-target* swap
(`nums[start], nums[i] = nums[i], nums[start]`); the ★ ring rotation here is the natural
generalization to a **four-target** swap over nested `Vec[Vec[i64]]` index targets, and the
flip-and-transpose solver reuses #47's *whole-row* swap (`m[a], m[b] = m[b], m[a]`).

## Approaches

Four styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Layer four-way cyclic swap** ★ | [`rotate_image.kara`](rotate_image.kara) | rings `i ∈ 0..n/2`, offsets `j ∈ i..n-1-i`; one four-target parallel assignment per cell-cycle, in place |
| Transpose + reverse rows | [`rotate_image_transpose.kara`](rotate_image_transpose.kara) | transpose (`m[i][j], m[j][i] = m[j][i], m[i][j]`), then two-pointer row reverse |
| Reverse row-order + transpose | [`rotate_image_flip.kara`](rotate_image_flip.kara) | whole-row swap `m[a], m[b] = m[b], m[a]` to flip vertically, then transpose |
| Out-of-place index map | [`rotate_image_fresh.kara`](rotate_image_fresh.kara) | build a fresh zero grid, scatter `dst[j][n-1-i] = src[i][j]`, return it |

The ★, transpose, and flip forms share the in-place / `O(1)`-space spine and differ only in *which
index identity* they exploit; the fresh form trades the in-place constraint for an explicit
`dst[j][n-1-i] = src[i][j]` scatter. Because all three in-place forms realise the same clockwise
map, the rotated matrix is byte-for-byte identical to the fresh form's output and to the oracle.

## What this kata surfaced

**A real language gap — now fixed in `karac`.** The four solvers were straightforward to write on
top of #47's parallel assignment (the four-target form and the nested-index reads/writes all
compiled the first time). The gap surfaced in the part every solver shares: the **matrix display**.
Printing a `Vec[Vec[i64]]` passed by `ref` means iterating its rows, and the natural idiom is

```
fn print_grid(m: ref Vec[Vec[i64]]) {
    let row = m[i];        // bind one row out of the borrowed matrix
    ... row.len() ... row[j] ...
}
```

That `let row = m[i]` **typechecked, ran correctly under `karac run`, but failed `karac build`** with

```
codegen: no handler for method 'len' on variable 'row'
```

The root cause was in the type-checker's index inference, not codegen: integer-indexing a
**borrowed** collection (`m[i]` where `m: ref Vec[Vec[i64]]`) fell through to `Type::Error`. The
range-index path (`m[a..b]`) and the Tensor/Column index paths already peeled `ref`/`mut ref`
before extracting the element type, but the **scalar integer-index** path did not — so a borrowed
container had no element-type arm and silently inferred `Error`. The `Error` propagated with no
diagnostic, the binding recorded no surface/element type, and method dispatch then fell through in
codegen. Tellingly, the *direct* double-index forms `m[i][j]` (reads and the nested-index parallel
assignment swap) and an *explicitly annotated* `let row: Vec[i64] = m[i]` both worked — only the
**inferred let-bound row** broke, which is exactly the idiom matrix-display code reaches for.

Rather than route around it (annotate every row binding, or inline `m[i][j]` everywhere), the
compiler was fixed: `infer_expr`'s scalar-index arm now peels `Type::Ref`/`Type::MutRef` and
extracts the inner `Array`/`Slice`/`Vector`/`Vec` element, bringing scalar indexing of a borrowed
collection in line with the range and Tensor/Column paths. Two E2E regression tests pin the `ref`
and `mut ref` forms. Full suites green (typecheck 1040, interpreter 1824, codegen 1909, ASAN 408).
See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) entry **B-2026-06-29-2** and the
print-grid helper in every solver, which is written in its natural `let row = m[i]` form on top of
the fix.

## Benchmarks

Workload: a fixed `n=20` matrix (the max LeetCode size) is rotated **`TOTAL = 40000`** times **in
place**, the state carrying forward across iterations. Each iteration punches one cell
(`m[k%n][(k*7)%n] = k%97`, **not reverted**, so the matrix state evolves) before rotating, then folds
a position-weighted signature of every cell into a rolling checksum (sink `320060006`). The punched
cell varies with the loop index (no hoisting of an otherwise-constant result) and the checksum
carries a loop-borne dependency, so this is a single-lane (seq) bench by construction. Unlike kata
[#46](../46-permutations/)/[#47](../47-permutations-ii/), **the rotation kernel allocates nothing
per solve** — the matrix is its own scratch — so this measures pure compute: nested-`Vec[Vec[i64]]`
index arithmetic, bounds checks, and in-place swaps. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded in-place ring rotation)

| | C | **Kāra** | Rust (`-O`) | Rust (`overflow-checks=on`) | Go | Python |
|---|---|---|---|---|---|---|
| time | 45.3 ms | **52.6 ms** | 47.6 ms | 51.0 ms | 53.6 ms | 1138.7 ms |
| vs Kāra | 1.16× faster | — | 1.11× faster | 1.03× faster (= safety) | 1.02× slower | 21.6× slower |

This is an **allocation-free, index-bound** kernel — every iteration is `O(n²)` double-indexed
reads/writes into a `Vec[Vec[i64]]` plus an `O(n²)` checksum fold, with no heap traffic. At that mix
Kāra lands at **52.6 ms: ahead of Go, within ~3% of the safety-matched `rustc -C overflow-checks=on`
(51.0 ms), ~1.11× behind `rustc -O`, and ~1.16× behind C** — comfortably inside the documented v1
bar (`design.md`: "within ~2× apples-to-apples"). The residual gap to C is codegen quality on the
doubly-indirect `m[i][j]` inner loop (two pointer-chases + two bounds checks per cell under Kāra's
checked-by-default indexing), not arithmetic: the safety-matched Rust comparator
(`overflow-checks=on`, 51.0 ms) is the right yardstick, and Kāra sits ~3% off it. Python runs the
identical algorithm interpreted, ~21.6× behind.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.02 MiB | 1.06 MiB | **1.00 MiB** | 2.64 MiB |
| binary size (seq) | 33.4 KiB | 455.4 KiB | **32.8 KiB** | 2434.1 KiB |
| compile elapsed | **82.2 ms** | 124.4 ms | 86.4 ms |
| compile peak RSS | 19.7 MiB | 31.5 MiB | **2.5 MiB** |

Runtime peak RSS is a three-way tie among the native mirrors — Kāra **1.02 MiB**, C 1.00 MiB, Rust
1.06 MiB, all within noise — while Go's runtime pays 2.64 MiB and Python's interpreter 6.8 MiB. The
seq compute binary references no par-scheduler runtime, so LTO + `-dead_strip` carve it to
**33.4 KiB**, within a rounding of C's 32.8 KiB and 13.6× under Rust. Compile is the clean win here:
Kāra is the **fastest** of the three AOT toolchains end to end — **82.2 ms**, 1.05× faster than
`clang -O3` (86.4 ms) and 1.51× faster than `rustc -O` (124.4 ms) — at 1.6× lighter peak compiler
RSS than `rustc` (19.7 vs 31.5 MiB); clang's 2.5 MiB is the floor.

**No par lane — by construction.** The per-iteration rotate is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par pass does not fire on the bench harness: the
default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded — same
as [#45](../45-jump-game-ii/)/[#46](../46-permutations/)/[#47](../47-permutations-ii/). Worth noting
the contrast the **solver** files draw out: their rotation loops *are* embarrassingly parallel (each
ring-cycle / transpose-swap / scatter touches disjoint cells), so auto-par safely transforms them —
the default and seq solver binaries differ yet produce identical output on every case. The
allocation-free, disjoint-write structure that makes ring rotation a clean auto-par target is the
same structure that keeps it competitive with C here.

## Kāra features exercised

- **Four-target parallel assignment over nested indices (new reach)** — the ★ solver's ring cycle
  `m[i][j], m[j][n-1-i], m[n-1-i][n-1-j], m[n-1-j][i] = m[n-1-j][i], m[i][j], m[j][n-1-i],
  m[n-1-i][n-1-j]` reads all four `Vec[Vec[i64]]` cells before writing any, so it is a genuine
  four-way rotate with no temporary — the four-target generalization of kata
  [#47](../47-permutations-ii/)'s two-target swap, and it typechecks, runs, and builds clean.
- **Whole-row parallel-assignment swap** — the flip solver's `m[a], m[b] = m[b], m[a]` swaps entire
  heap `Vec[i64]` rows, the same move-disciplined row swap #47 used to canonicalize its output.
- **Borrowed nested-collection row binding (`let row = m[i]`)** — every solver's `print_grid` binds
  a row out of a `ref Vec[Vec[i64]]` and reads it by `row.len()` / `row[j]`; this is the idiom the
  kata's compiler fix repaired (B-2026-06-29-2), now natural under both `karac run` and `karac build`.
- **In-place nested-index reads and writes** — transpose / row-reverse / scatter all index
  `m[i][j]` directly on a `mut ref Vec[Vec[i64]]` (and `dst[j][n-1-i] = …` on a fresh grid), the
  doubly-indirect access pattern the benchmark stresses.
- **`Vec[Vec[i64]]` construction from 2-D literals** — `report([[1,2,3],[4,5,6],[7,8,9]])` builds
  the matrix from a nested array literal moved into a `Vec[Vec[i64]]` binding, then a `let mut m`
  rebinding makes it mutable for the in-place rotate.
- **Checked integer arithmetic at zero cost** — the ring/transpose index math (`n-1-i`, `n-1-j`)
  and the position-weighted checksum fold run under Kāra's default overflow checking and land within
  ~3% of the safety-matched `rustc -C overflow-checks=on`; the seq-lane result here is set by
  index-codegen quality, not arithmetic.

---

**Bug ledger:** one language gap, fixed. Probing the four solvers' shared **matrix display** surfaced
that `karac` inferred `Type::Error` for a `let row = m[i]` binding when `m` is a **borrowed** nested
collection (`ref Vec[Vec[i64]]`) — the type-checker's scalar integer-index arm peeled `ref`/`mut ref`
nowhere, unlike the range-index and Tensor/Column paths, so a borrowed container had no element-type
arm. The `Error` propagated silently (no diagnostic) and codegen then failed with "no handler for
method 'len' on variable 'row'" — even though `karac run`, an explicit `let row: Vec[i64] = m[i]`
annotation, and the direct double-index `m[i][j]` (including the nested-index parallel-assignment
swap) all worked. Fixed in `karac` by adding a `Type::Ref`/`Type::MutRef` arm to `infer_expr`'s
scalar-index match that peels one borrow and extracts the inner `Array`/`Slice`/`Vector`/`Vec`
element. Parser/typecheck unchanged; two codegen E2E regressions added
(`ref_param`/`mut_ref_param` nested-vec row binding); full suites green (typecheck 1040, interpreter
1824, codegen 1909, ASAN 408; clippy + fmt clean). See **B-2026-06-29-2** in the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the cross-kata history.

Beyond the new fix the four solvers remain a clean **regression exercise** of kata
[#47](../47-permutations-ii/)'s parallel-assignment work — the four-target cell cycle and the
whole-row swap are the multi-target and row generalizations of #47's two-target swap, all written in
their natural form on top of that construct.
