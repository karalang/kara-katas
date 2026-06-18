# 37. Sudoku Solver

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array, Backtracking, Hash Table, Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/sudoku-solver](https://leetcode.com/problems/sudoku-solver/)

Given a partially filled **9×9 board** (`0` marks an empty cell, `1`–`9` a placed digit),
**fill every empty cell** so the completed board obeys the three Sudoku rules: no digit
repeats within any **row**, any **column**, or any of the nine **3×3 sub-boxes**. The
input is guaranteed to have exactly one completion.

```
5 3 . | . 7 . | . . .            5 3 4 | 6 7 8 | 9 1 2
6 . . | 1 9 5 | . . .            6 7 2 | 1 9 5 | 3 4 8
. 9 8 | . . . | . 6 .            1 9 8 | 3 4 2 | 5 6 7
------+-------+------             ------+-------+------
8 . . | . 6 . | . . 3    solve   8 5 9 | 7 6 1 | 4 2 3
4 . . | 8 . 3 | . . 1   ----->   4 2 6 | 8 5 3 | 7 9 1
7 . . | . 2 . | . . 6            7 1 3 | 9 2 4 | 8 5 6
------+-------+------             ------+-------+------
. 6 . | . . . | 2 8 .            9 6 1 | 5 3 7 | 2 8 4
. . . | 4 1 9 | . . 5            2 8 7 | 4 1 9 | 6 3 5
. . . | . 8 . | . 7 9            3 4 5 | 2 8 6 | 1 7 9
```

**Constraints:** board is `9×9`; each cell is a digit `1–9` or empty; the puzzle is
valid and has a single solution.

This is the **dual** of [#36 Valid Sudoku](../36-valid-sudoku/): where #36 *validates* a
board, #37 *completes* one — and the example above solves to **exactly the board #36's
example 1 validated**. The candidate test at the heart of the solver is #36's
membership test run in reverse: "which digits are NOT yet seen in this row / column /
box?"

## Why this kata — search, with the validity test from #36 as the pruner

The skeleton is backtracking: walk the cells, and at the first empty one try each legal
digit, recurse, and undo on failure. The whole performance question is making **"legal
digit"** cheap, asked once per branch of a tree that — on a hard puzzle — has millions of
nodes. The answer is #36's bitmask, carried as *state*: three nine-element arrays of
masks (rows / cols / boxes), where bit `d` set means "digit `d` is present in this unit".
A cell `(r, c)`'s legal digits are exactly those whose bit is **clear** in
`rows[r] | cols[c] | boxes[b]`, with `b = (r/3)*3 + c/3` — an O(1) test. Placing a digit
sets its bit in all three masks; undoing **clears** it (one XOR per unit, since the bit
was just set). No per-placement re-scan of the grid: the masks are the incremental
witness of what each unit holds, updated in O(1) on the way down and O(1) on the way back
up.

Two axes vary across the three styles: **how legality is tested** (carried masks vs a
fresh row/column/box scan) and **which empty cell is expanded next** (linear order vs the
fewest-candidates cell). Everything else — DFS, place/recurse/undo, ascending digit
order — is shared.

| Lens | Idea |
|---|---|
| **Bitmask backtracking** ★ | three nine-element masks carried through the recursion; legal digits of `(r,c)` are the clear bits of `rows[r] \| cols[c] \| boxes[b]`; place sets three bits, undo XORs them off — O(1) per branch |
| **Plain backtracking** | no carried state — at each empty cell `is_safe` scans the row, column, and box for the candidate digit right then; O(27) per test, but the purest "place what doesn't conflict, recurse, undo" reading |
| **MRV (fewest candidates first)** | same masks, but expand the empty cell with the **minimum remaining values**; a one-candidate cell is forced, so taking forced cells first collapses the tree on hard puzzles |

## Approaches

Three styles, all agreeing with the Python oracle across all five cases (the LeetCode
example / AI Escargot / the world's-hardest Inkala puzzle / an already-solved board / a
valid-but-unsolvable board), under `karac run` **and** `karac build`. The oracle
additionally proves by brute force that each solvable test puzzle has **exactly one**
completion — which is what makes "the solution" well defined and the three cell-orders
interchangeable.

| Approach | File | Shape |
|---|---|---|
| **Bitmask backtracking** ★ | [`sudoku_solver.kara`](sudoku_solver.kara) | seed three `Vec[i64]` masks from the givens, then DFS in linear cell order; at an empty cell try each `1<<d` clear in `rows[r]\|cols[c]\|boxes[b]`, set/recurse/XOR-undo |
| Plain backtracking | [`sudoku_solver_plain.kara`](sudoku_solver_plain.kara) | no masks; `is_safe(board,r,c,d)` scans the nine row cells, nine column cells, and nine box cells for `d` before each placement |
| MRV ordering | [`sudoku_solver_mrv.kara`](sudoku_solver_mrv.kara) | same masks, but each step picks the empty cell minimising `candidate_count(rows[r]\|cols[c]\|boxes[b])` — forced cells first |

The bitmask form is the one the bench measures: O(1) legality, O(1) undo, all scratch on
the stack. The plain form trades a 27-cell re-scan per candidate for zero carried state —
the clearest statement of *what* backtracking is, with the conflict test spelled out
where the placement is considered. MRV keeps the bitmask machinery but changes only
**which** empty cell is expanded next; on a unique-solution board it finds the same grid,
just by visiting far fewer nodes (a one-candidate cell is never a guess). All three are
exponential in the worst case and agree on every puzzle.

## What this kata surfaced

Two `karac` findings, both reproduced minimally and tracked in the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl):

**1. A `mut ref` argument wouldn't downgrade to a `ref` parameter under `karac build`**
([`B-2026-06-17-4`](../../../../kara/docs/bug-ledger.jsonl), `kata:37`, typecheck, **fixed
in [`3ab709a2`](../../../../kara/docs/bug-ledger.jsonl)**). The plain solver's read-only
`is_safe(board)` is naturally called from the mutating search
`go(board: mut ref Vec[Vec[i64]])`. Passing that `mut ref` binding to a `ref` parameter
*was* a **`karac run` warning** (the interpreter accepted it and the program ran) but a
**`karac build` hard error** — *"expected ref …, found mut ref …"* at the call argument.
A program that runs should build, so the run/build divergence was the defect. The fix
adds the missing subtyping arm: a `mut ref T` reborrows down to a read-only `ref T` (the
`&mut T → &T` reborrow), sound and covariant in the pointee exactly like the `ref → ref`
rule because the destination borrow cannot write through it; the reverse direction
(`ref → mut ref`) stays rejected. Minimal repro that now builds and prints `9`:
`fn peek(xs: ref Vec[i64]) -> i64 { xs[0] }` called from
`fn poke(xs: mut ref Vec[i64]) -> i64 { xs[0] = 9i64; peek(xs) }`. With the fix landed,
[`sudoku_solver_plain.kara`](sudoku_solver_plain.kara) uses the **natural `ref`** on
`is_safe` (the earlier `mut ref` sidestep is gone).

**2. `mut` array-view parameters aren't lowered to LLVM `noalias`**
([`B-2026-06-17-5`](../../../../kara/docs/bug-ledger.jsonl), `kata:37`, codegen, open) —
the source of the benchmark gap to Rust below. The recursive solver threads **four
independent mutable array views** — the board plus the three masks — through `go()`.
Rust's `&mut` guarantees non-aliasing, which LLVM turns into `noalias` and exploits
heavily; Kāra's `mut Slice` params (like plain C's `int64_t *`) carry no such attribute,
so LLVM must assume any two of the four might alias and holds back. The result is a clean
three-way split (see the benchmark): Rust 190 ms, **Kāra ties plain C at 260 ms**, and
adding C `restrict` reproduces Rust's time exactly — proving the gap *is* the aliasing
attribute, not Kāra codegen quality.

But emitting `noalias` is **not** a quick win, and chasing it surfaced a deeper gap.
`noalias` is sound only if `mut ref` / `mut Slice` params are *guaranteed* non-aliasing —
exactly what Rust's borrow checker enforces for `&mut`. Kāra's design says the same
(`mut ref T` is an *exclusive* borrow, "allowed only when no other borrow of `T` is
active"), **but the checker doesn't enforce it at call sites**: `f(mut v, mut v)` — two
exclusive borrows of the same binding — compiles
([`B-2026-06-17-6`](../../../../kara/docs/bug-ledger.jsonl), `kata:37`, ownership, open).
Worse, codegen already *diverges* from the interpreter on that aliased call (it passes the
Vec header by value per borrow), so a blanket `noalias` would turn a latent bug into broad
miscompiles. The correct sequence is therefore: **enforce mut-borrow exclusivity first**
(B-2026-06-17-6), *then* emit `noalias` on the now-provably-disjoint params. (An earlier
draft of this README claimed Kāra's ownership "already proves" non-aliasing — that was
wrong; `f(mut v, mut v)` is the counterexample, and finding it is exactly what this
bug-finder kata is for.)

## Benchmarks

Workload: the template is **Arto Inkala's 2012 "world's hardest sudoku"** — the puzzle
engineered to force maximal backtracking. **`TOTAL = 500`** times, copy the template into
a fresh working board, **clear cell `k % 81`** (removing a clue can never make the puzzle
unsolvable, so every iteration completes), **solve** it with the single-pass bitmask
backtracker, and fold a **position-weighted** signature of the solved grid —
`sum board[i]*(i+1)` — into a rolling checksum (sink `667470979`). The weight is
load-bearing: an *unweighted* cell sum is `405` for any complete board, so it would not
detect a misplaced digit; the weighted sum depends on *where* each digit lands. The
cleared cell varies with the loop index, so no comparator can hoist the solve out of the
loop. Recursion + branchy mask arithmetic over a fixed-size grid, **no heap allocation in
the hot path** (board + the three masks are all stack storage), so this measures
backtracking-search codegen, not the allocator. The accumulator carries a loop-borne
dependency, so this is a single-lane (seq) bench by construction. Apple M5 Pro;
`bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded bitmask-backtracking solve)

| | Rust (`-O`) | Rust (`overflow-checks=on`) | C | **Kāra** | Go | Python |
|---|---|---|---|---|---|---|
| time | 190.4 ms | 190.5 ms | 260.2 ms | **260.2 ms** | 297.9 ms | 19091 ms |
| vs Kāra | 1.37× faster | **1.37× faster (= safety)** | 1.00× (tie) | — | 1.14× slower | 73× slower |

**Kāra ties C exactly and beats Go by 1.14×; the 1.37× behind Rust is entirely a
`noalias` effect, not a Kāra-vs-native gap.** Two things make this run read differently
from #36 (where C was the floor and Rust ≈ C):

- **Rust beats C here, and the reason is provable.** The hot loop threads four mutable
  array views through a recursion. Rust's `&mut` non-aliasing becomes LLVM `noalias`;
  plain C's pointers might alias, so the optimizer is conservative. Adding `restrict` to
  the C pointers — asserting the same non-aliasing — **closes the gap exactly**: plain C
  259 ms → `restrict` C **187 ms**, dead level with Rust's 189 ms (`hyperfine`, 15 runs).
  So the whole Rust-over-C lead is the aliasing attribute, and **Kāra sits precisely at
  the aliasing-conservative native floor** (= plain C). This is [`B-2026-06-17-5`](../../../../kara/docs/bug-ledger.jsonl):
  Kāra's ownership analysis already proves the four views don't alias, so emitting
  `noalias` would move it onto the Rust/`restrict`-C line — a measured ~1.37× left on the
  table, recoverable without weakening any safety guarantee.
- **The overflow tax is ~zero on this kernel.** `rustc -O` (190.4 ms) and
  `-C overflow-checks=on` (190.5 ms) are within noise, because the hot path is array
  indexing + bitwise mask ops, with the single multiply living only in the once-per-solve
  signature fold — almost no checked arithmetic to tax. So equal-safety Rust is also
  1.37×; the distance is the aliasing attribute, full stop.

**No par lane — by construction.** The solve is pure per iteration, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par-on-reduction pass does not
fire: the default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run
single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.02 MiB | 1.05 MiB | **1.02 MiB** | 2.58 MiB |
| binary size (seq) | 33.1 KiB | 455.4 KiB | **32.8 KiB** | 2434.1 KiB |
| compile elapsed | 75.9 ms | 79.6 ms | **41.3 ms** |
| compile peak RSS | 15.1 MiB | 26.4 MiB | **2.5 MiB** |

The board and masks are all stack storage with no hot-path allocation, so runtime RSS
ties C **to the byte** (both 1.02 MiB) and undercuts Rust's 1.05 MiB; Go's runtime pays
2.58 MiB and Python's interpreter 7.25 MiB. The seq compute binary references no
`String`/par-scheduler runtime, so LTO + `-dead_strip` carve it to **33.1 KiB** — 13.8×
under Rust and within a rounding of C's 32.8 KiB (Go's static runtime is 2.4 MiB).
Compile favours Kāra over `rustc -O` on both elapsed (75.9 vs 79.6 ms) and peak compiler
RSS (15.1 vs 26.4 MiB); clang's 41.3 ms / 2.5 MiB is the toolchain floor.

## Kāra features exercised

- **Recursive backtracking that mutates a borrowed board in place** — `go` takes the
  board (and the three masks) as `mut Slice[i64]` in the bench / `mut ref Vec[Vec[i64]]`
  in the pedagogical files, writes a cell, recurses, and on failure clears it; the search
  state lives entirely in the borrowed views, no per-node heap.
- **`Slice[i64]` borrowed view of a fixed array** — the bench's `solve`/`go` take
  `mut Slice[i64]` and `main` passes its `Array[i64, 81]` board by coercion, the same
  borrowed-`nums` form as [#34](../34-find-first-and-last-position/) /
  [#35](../35-search-insert-position/) / [#36](../36-valid-sudoku/), here on the *mutable*
  path (the solver writes through the slice).
- **Stack `Array[i64, 9]` masks reset per solve** — the three nine-element masks are
  rebuilt each `solve` call, no heap in the hot path — the property that lets the bench
  isolate search codegen from the allocator.
- **Bitmask membership as the search pruner** — `1 << d`, `mask & bit` to test, `mask | bit`
  to place, `mask ^ bit` to undo, with the integer-division box fold `(r/3)*3 + c/3`; the
  plain style re-expresses the same legality as a 27-cell scan, MRV as a candidate count.
- **Three orderings of one search** — carried-mask linear DFS, fresh-scan linear DFS, and
  fewest-candidates-first, all agreeing across the five oracle cases (including a
  no-solution board) under both `karac run` and `karac build`.

---

**Bug ledger:** [`B-2026-06-17-4`](../../../../kara/docs/bug-ledger.jsonl) (`kata:37`,
typecheck, **fixed `3ab709a2`**) — a `mut ref` argument failed to downgrade to a `ref`
parameter under `karac build` (a `karac run` warning became a build error); fixed by
adding the `mut ref T → ref T` reborrow subtyping arm, so the plain solver now uses the
natural `ref`; [`B-2026-06-17-5`](../../../../kara/docs/bug-ledger.jsonl)
(`kata:37`, codegen, open) — `mut` array-view parameters aren't emitted as LLVM `noalias`,
the *provable* (C `restrict` closes it) source of the 1.37× gap to equal-safety Rust; and
its newly-found blocker [`B-2026-06-17-6`](../../../../kara/docs/bug-ledger.jsonl)
(`kata:37`, ownership, open) — Kāra's **exclusive-borrow rule isn't enforced at call
sites** (`f(mut v, mut v)` compiles, and codegen then diverges from the interpreter on the
aliased call), so mut-param `noalias` can't be made sound until exclusivity is enforced
first. See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
