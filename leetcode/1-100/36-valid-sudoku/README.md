# 36. Valid Sudoku

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Hash Table, Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/valid-sudoku](https://leetcode.com/problems/valid-sudoku/)

A partially filled **9×9 board** (`0` marks an empty cell, `1`–`9` a placed digit).
Decide whether it is valid **so far**: no digit repeats within any **row**, any
**column**, or any of the nine **3×3 sub-boxes**. Empty cells impose nothing, and the
board need not be solvable — only the three no-duplicate rules matter.

```
5 3 . | . 7 . | . . .      valid: no row, column, or box repeats a digit
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+------
8 . . | . 6 . | . . 3      change the top-left 5 → 8 and it becomes invalid:
4 . . | 8 . 3 | . . 1      that 8 now repeats in column 0 (row 3) AND in the
7 . . | . 2 . | . . 6      top-left box (cell (2,2) is 8)
```

**Constraints:** board is `9×9`; each cell is a digit `1–9` or empty; only the placed
digits are checked (a valid-so-far board may have no solution).

## Why this kata — three constraints, one membership test

The whole problem is one question — *"have I seen this digit in this row / column /
box already?"* — asked 81 times. With nine distinct digits a unit's seen-set fits in a
single integer used as a **bitmask** (`bit d = 1 << d`), so the entire state is three
nine-element arrays of masks: 27 integers, O(1) per cell, one pass over the grid. The
crux is that **all three constraints must be tested at the same cell**: a digit can be
unique in its row and its column yet still collide inside its box, so row-and-column
checking alone is wrong — the box-only duplicate case is the witness.

The cell-to-box map is the one piece of arithmetic: cell `(r, c)` lives in box
`(r/3)*3 + c/3` — integer division folds the 9×9 grid into a 3×3 grid of boxes, then
back to a flat `0..9` box index. After that it is three membership tests and an early
return on the first collision (what makes the common invalid case cheap).

| Lens | Idea |
|---|---|
| **Single-pass bitmask** ★ | three nine-element `Array` masks; per cell test `(rows[r] & 1<<d) \| (cols[c] & …) \| (boxes[b] & …)`, early-return on a hit, else set all three |
| **Single-pass boolean** | the same pass, but the seen-set is a `9×10` boolean grid `seen[unit][digit]` — no shift/mask, just a 2-D lookup; the clearest reading of *what a bitmask encodes* |
| **Three separate passes** | check the rules **independently** — scan the nine rows, then the nine columns, then the nine boxes, each with one reused local mask; `O(3·81)` work, but textually orthogonal rules |

## Approaches

Three styles, all agreeing with the Python oracle across all seven cases (empty /
solved / the two LeetCode examples / row-only / column-only / box-only duplicates),
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Single-pass bitmask** ★ | [`valid_sudoku.kara`](valid_sudoku.kara) | three `Vec[i64]` masks; `bit = 1<<d`, `b = (r/3)*3 + c/3`; if `bit` already in `rows[r] \| cols[c] \| boxes[b]` → invalid, else OR it into all three |
| Single-pass boolean | [`valid_sudoku_bool.kara`](valid_sudoku_bool.kara) | three `9×10` `Vec[Vec[bool]]` seen-grids indexed by the digit value itself; `seen_row[r][d]` direct lookup, no bit tricks — 243 bools vs 27 ints |
| Three separate passes | [`valid_sudoku_passes.kara`](valid_sudoku_passes.kara) | one reused integer mask, reset per unit; rows pass, then columns pass, then boxes pass (top-left corner `((b/3)*3, (b%3)*3)`); every cell read three times, rules independent |

The bitmask form is the tightest (27 ints of scratch, one OR-and-test per filled
cell); the boolean form trades a little space for zero bit arithmetic and is the
clearest mental model; the three-pass form spends a 3× constant factor to keep the
row / column / box rules textually independent — you can read or edit the box rule
with no row logic in view. All three are O(1) in the (fixed 9×9) board size and agree
on every board.

## What this kata surfaced

**`ref Array[T, N]` parameters failed codegen** ([`B-2026-06-17-1`](../../../../kara/docs/bug-ledger.jsonl),
`kata:36`, **fixed `2cdbbac4`**). The natural way to pass a fixed-size board by borrow —
`fn is_valid(board: ref Array[i64, 81])` — *built*-failed with *"Index operator applied
to non-array type"*. A `ref`/`mut ref Array` param's slot LLVM type is `ptr` (the
borrow), not `[N x T]`, and the param sat in no name-keyed index registry, so
`compile_index` (`src/codegen/collections.rs`) fell past the tensor/slice/map/soa/vec
routes to the generic tail, whose `ArrayType` branch can't match a `ptr`. The
`ref Vec[T]` form is handled precisely because it has an explicit `vec_elem_types`
name-keyed route (its ref slot is also `ptr`); `ref Array` had no analogue. **The fix
mirrors that route** (`ref_array_index_target`): detect a `ref`/`mut-ref Array` param
from its recorded inner `[N x T]` type, load the data pointer from the slot and GEP
through `[N x T]`, for both index-read and index-store — exactly as predicted here, now
landed in `2cdbbac4`. (Note: `run_program` bypassed codegen, so the form always *ran*
fine — only `karac build` tripped.)

This was **not** a blocker for the kata: the idiomatic borrowed view of a fixed array is
**`Slice[i64]`** (an `Array` coerces to it), exactly how [#34](../34-find-first-and-last-position/)
/ [#35](../35-search-insert-position/) pass `nums`. The bench harness uses `Slice` and
hits the hot path with zero heap allocation; the pedagogical files use `ref Vec[Vec[i64]]`
(the 2-D jagged form). So `ref Array` was a genuine codegen gap the kata *found* and
*drove to a fix* — both forms build now; the bench stays on the idiomatic `Slice`.

## Benchmarks

Workload: build one fixed, fully-solved (valid) board once as a flat `Array[i64, 81]`,
then **`TOTAL = 5M`** times **perturb** cell `k % 81` to digit `(k % 9) + 1`, validate
the perturbed board, fold the boolean verdict into a checksum, and restore the cell
(sink `291807572`). The perturbation varies with the loop index, so no comparator can
hoist the validation out of the loop; ~half the perturbations introduce a duplicate
(early-return path) and ~half leave a valid board (full 81-cell scan). The accumulator
carries a loop-borne dependency, so this is a single-lane (seq) bench by construction.
Pure branchy integer compute over a fixed-size grid, **no heap allocation in the hot
path** (board + the three masks are all stack storage), so this measures validation
codegen, not the allocator. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded single-pass bitmask validation)

| | C | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Go | Python |
|---|---|---|---|---|---|---|
| time | 113.8 ms | 114.3 ms | 118.6 ms | **183.1 ms** | 246.5 ms | 27702 ms |
| vs Kāra | 1.61× faster | 1.60× faster | **1.54× faster (= safety)** | — | 1.35× slower | 151× slower |

**Within 1.54× of equal-safety Rust, and 1.35× ahead of Go.** This is a branchy,
index-heavy inner loop — 81 cells each doing a `Slice` read plus three bounds-checked
mask accesses — so the residual gap to Rust is the per-access bounds check Kāra does
not yet fully elide on stack `Array`/`Slice` indices, where Rust's known-length arrays
drop it. The overflow tax is small but real here (`rustc -O` 114.3 ms vs
`-C overflow-checks=on` 118.6 ms, +3.8 %), so equal-safety Rust is 1.54× rather than
1.60×; the remaining distance is codegen on a tight branchy loop, not checked
arithmetic. C (1.61×) marks the no-overhead floor, and Go — whose BCE also leaves the
mask-index checks in and does not inline `isValid` into the hot loop — runs the same
algorithm 1.35× slower than Kāra.

**No par lane — by construction.** The validation is pure and independent per
iteration, but the checksum reduction carries a loop-borne dependency, so karac's
auto-par-on-reduction pass does not fire: the default and `KARAC_AUTO_PAR=0` binaries
are **byte-identical** and both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.03 MiB | 1.08 MiB | **1.00 MiB** | 2.91 MiB |
| binary size (seq) | **33.0 KiB** | 455.4 KiB | 32.8 KiB | 2434.1 KiB |
| compile elapsed | 76.3 ms | 98.3 ms | **50.4 ms** |
| compile peak RSS | 14.1 MiB | 26.1 MiB | **2.5 MiB** |

The board and masks are all stack storage with no hot-path allocation, so runtime RSS
ties C and Rust to within rounding (1.03 / 1.00 / 1.08 MiB); Python's interpreter pays
7.1 MiB. The seq compute binary references no `String`/par-scheduler runtime, so LTO +
`-dead_strip` carve it to **33.0 KiB** — 13.8× under Rust and within a rounding of C's
32.8 KiB (Go's static runtime is 2.4 MiB). Compile favours Kāra over `rustc -O` on both
elapsed (76.3 vs 98.3 ms) and peak compiler RSS (14.1 vs 26.1 MiB); clang's 50.4 ms /
2.5 MiB is the toolchain floor.

## Kāra features exercised

- **`Slice[i64]` borrowed view of a fixed array** — the bench's `is_valid` takes
  `Slice[i64]` and `main` passes its `Array[i64, 81]` board by coercion, the same
  borrowed-`nums` form as [#34](../34-find-first-and-last-position/) /
  [#35](../35-search-insert-position/); the attempt to use `ref Array[i64, 81]` instead
  is what surfaced [`B-2026-06-17-1`](../../../../kara/docs/bug-ledger.jsonl) (since fixed
  in `2cdbbac4` — `ref Array` indexing builds now, though `Slice` stays the idiomatic view).
- **Stack `Array[i64, N]` locals reset per call** — the three nine-element masks are
  `let mut rows: Array[i64, 9] = [0, …]` rebuilt each validation, no heap in the hot
  path — the property that lets the bench isolate validation codegen from the allocator.
- **Bitmask membership over integers** — `1 << d`, `mask & bit`, `mask | bit` as the
  per-unit seen-set, with integer-division box folding `(r/3)*3 + c/3`; the boolean and
  three-pass styles re-express the same membership without bit tricks.
- **Three factorings of one invariant** — single-pass parallel seen-sets, a `Vec[Vec[bool]]`
  seen-grid, and three independent single-mask sweeps, all agreeing across the seven
  oracle cases under both `karac run` and `karac build`.

---

**Bug ledger:** [`B-2026-06-17-1`](../../../../kara/docs/bug-ledger.jsonl) (`kata:36`,
codegen, **fixed `2cdbbac4`**) — `ref`/`mut ref Array[T, N]` parameters failed codegen
(*"Index operator applied to non-array type"*) because the borrow slot is `ptr` with no
name-keyed index route; the fix mirrors the existing `ref Vec[T]` route
(`ref_array_index_target`), GEPing through the recorded `[N x T]` for index-read and
index-store. The bench keeps the idiomatic `Slice[i64]` borrowed view (same form as
#34/#35); `ref Array` now also builds.
See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
