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

Four `karac` findings, **all four fixed**, each reproduced minimally and tracked in the
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

**2. The Rust gap was *loop unrolling* — found after three wrong guesses, then *fixed*;
Kāra now leads the field.** The solver opened ~1.34× behind Rust. Three hypotheses for
that gap were tested and *all three were wrong*; the corrections are kept because the
kata's job is to *find* the truth, not to look clean. IR/asm-level isolation of `go`
finally pinned the real cause, and it is now closed
([`B-2026-06-17-7`](../../../../kara/docs/bug-ledger.jsonl), `kata:37`, codegen, **fixed
[`1de4eb1e`](../../../../kara/docs/bug-ledger.jsonl)**).

- **First hypothesis (wrong): the gap is `noalias`.** The solver threads four mutable
  array views — board + three masks — through `go()`; Rust's `&mut` carries LLVM
  `noalias`, and adding C `restrict` to the bench's pointers reproduced Rust's time, so it
  *looked* like the whole gap was the aliasing attribute
  ([`B-2026-06-17-5`](../../../../kara/docs/bug-ledger.jsonl), **fixed**). The detour
  surfaced a *real soundness bug*: emitting `noalias` is sound only if `mut ref` params are
  *guaranteed* non-aliasing, but the checker didn't enforce exclusivity at call sites —
  `f(mut v, mut v)` compiled and codegen diverged from the interpreter
  ([`B-2026-06-17-6`](../../../../kara/docs/bug-ledger.jsonl), **fixed `1e0fe5ea`**, now a
  hard error). But measuring it, switching *to* the `noalias`-carrying form recovered only
  ~1.5% — so `noalias` was never the gap.
- **Second & third hypotheses (wrong): the gap is bounds checks.** The next guesses were
  that Rust elides per-access checks on a known-length `[i64; N]` while Kāra doesn't.
  **Direct measurement refuted it:** `get_unchecked` on the hot reads made Kāra *slower*
  (279 vs 253 ms); a `Vec`-with-elision vs `Array`-without-elision micro-bench ran
  byte-for-byte the same; the recursive hot indices aren't loop-bounded so nothing could
  elide them; and Rust's `&mut [i64]` bench bounds-checks too. No speculative (and
  potentially out-of-bounds) elision was shipped.
- **The real cause, found by disassembly: Rust *fully unrolled* the candidate loop; Kāra
  and C did not.** Comparing `go`'s machine code across all three compilers showed Kāra's
  inner loop `while d <= 9 { … if go(…) …; d = d + 1 }` was **byte-for-byte at the C floor**
  (Kāra 254 ms vs C 254 ms — actually a hair *ahead* of clang), while Rust emitted the same
  loop **fully unrolled** into nine straight-line digit blocks. That single difference *was*
  the whole gap: forcing the unroll on the C mirror with `#pragma clang loop unroll(full)`
  lands C *exactly* on Rust (190 ms), and disabling rustc's unroller drops Rust back onto
  Kāra/C (~255 ms). clang's cost model *declines* this unroll (the recursive call + early
  exit look expensive) even at `-O3 -funroll-loops` — rustc's LLVM config takes it.
- **The fix: karac now emits the unroll hint that rustc effectively does.** `compile_while`
  attaches `llvm.loop.unroll.full` to the back-edge of small, constant-upper-bounded counted
  loops (`v < K` / `v <= K`, constant-step induction var, `K ≤ 32`), so LLVM's full unroller
  fires. It is **advisory-safe**: unrolling is semantics-preserving, and LLVM ignores the
  hint when it can't prove a small constant trip count, so a mis-detected loop costs nothing.
  Result: kata:37 drops **254 → 183 ms, now 1.03× *ahead* of Rust** (Kāra carries `noalias`
  *and* — on fixed `Array` — no bounds checks, where Rust's slices still check). The same
  optimization speeds [#36](../36-valid-sudoku/)'s 9-cell validator loops **2.88×**;
  variable-bounded loops (the binary-search katas) are untouched — the gate is narrow by
  design.

> **Note (2026-10-31):** the "Kāra now leads the field" result above is the June legacy
> build's. On the v2/MIR backend the unroll hint is no longer emitted on this loop and Kāra
> is 1.37× behind `rustc -O`, on the C floor — [`B-2026-10-31-44`](../../../../kara/docs/bugs-v2.md)
> (perf, open); see § Benchmarks.

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
`bench/bench.sh` (`hyperfine`). Figures below are the 2026-10-31 re-bench (results.json
`measured_at` 2026-11-01T02:00Z), measured with **karac 0.9.0-dev.14057+g6697158fa** — the
v2/MIR backend (the legacy backend was deleted 2026-10-23).

### Seq lane — runtime (single-threaded bitmask-backtracking solve)

| | Rust (`overflow-checks=on`) | Rust (`-O`) | **Kāra** | C | Go | Python |
|---|---|---|---|---|---|---|
| time | 211.5 ± 3.5 ms | 211.7 ± 3.4 ms | **289.5 ± 5.2 ms** | 295.7 ± 3.7 ms | 334.8 ± 3.6 ms | 19027 ms (last measured 2026-06-18, not re-run) |
| vs Kāra | **1.37× faster (= safety)** | 1.37× faster | — | 1.02× slower | 1.16× slower | 103× slower than the 2026-06-18 Kāra figure |

**Kāra no longer leads the field: it is back on the C floor (1.02× ahead of clang, 1.16×
ahead of Go) and 1.37× behind `rustc -O`.** In language ratios against the previous feed
(legacy karac 0.1.0, 2026-06-18): Kāra/Rust 0.97× → 1.37×, Kāra/C 0.71× → 0.98×,
Kāra/Go 0.62× → 0.86× — a ~1.4× relative regression, against comparators that ran only
11–13 % slower in absolute ms this session. The solver is still written in its natural
`mut ref Array[i64, 81]` / `mut ref Array[i64, 9]` form (board + masks), which lowers each
borrow to a single `ptr` carrying LLVM `noalias`; what it has lost is the unroll:

- **The candidate loop is no longer fully unrolled.** The hot inner loop
  `while d <= 9 { … }` carried Kāra's full-unroll hint on the June legacy build
  ([`B-2026-06-17-7`](../../../../kara/docs/bug-ledger.jsonl),
  **fixed [`1de4eb1e`](../../../../kara/docs/bug-ledger.jsonl)**), so LLVM expanded it into
  nine straight-line digit blocks — the single optimization that closed (and then crossed) a
  1.34× gap. This was the whole story: before the fix Kāra sat at the **C floor** (254 ms,
  rolled, a hair *ahead* of clang), and Rust's lead came *entirely* from unrolling the same
  loop (proven by forcing the unroll on the C mirror — it lands exactly on Rust — and by
  disabling rustc's unroller, which drops Rust back to ~255 ms). clang declines this unroll
  even at `-O3 -funroll-loops`; rustc takes it. The MIR backend never emits the hint on
  this loop (it calls `go` recursively and exits early, which its unroll gate rejects), so
  the loop runs rolled again and the measured gap, 1.37×, is the June rolled gap
  (~1.34×) back — filed as [`B-2026-10-31-44`](../../../../kara/docs/bugs-v2.md) (perf,
  open). The regression is against the June build, not the MIR switch: the October legacy
  build had lost the unroll too, and MIR runs 1.01× its instructions.
- **The `noalias` + no-bounds-check edge still shows against C.** Kāra carries `noalias`
  (from the exclusive `mut ref` borrow) *and*, on a fixed `Array[i64, N]`, drops bounds
  checks the type makes provable — which is what keeps the rolled loop a hair ahead of
  clang. In June the same edge put Kāra 1.03× ahead of an equally-unrolled Rust, whose
  bench indexes `&mut [i64]` slices that still bounds-check.
- **The overflow tax is ~zero on this kernel.** `rustc -O` (211.7 ms) and
  `-C overflow-checks=on` (211.5 ms) are within noise — the hot path is array indexing +
  bitwise mask ops, with the single multiply only in the once-per-solve signature fold — so
  equal-safety Rust is 1.37× ahead, the same as unchecked.

**No par lane — by construction.** The solve is pure per iteration, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par-on-reduction pass does not
fire: the default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** (re-checked on the
2026-10-31 MIR build: same 302,880 B, same sha) and both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.03 MiB | 1.08 MiB | **1.00 MiB** | 2.72 MiB |
| binary size (seq) | 295.8 KiB | 455.4 KiB | **32.8 KiB** | 2434.1 KiB |
| compile elapsed | 125.2 ms | 89.9 ms | **47.2 ms** |
| compile peak RSS | 59.8 MiB | 26.4 MiB | **2.6 MiB** |

The board and masks are all stack storage with no hot-path allocation, so runtime RSS sits
with the natives — 1.03 MiB, between C's 1.00 MiB and Rust's 1.08 MiB (single-shot
readings, a 16 KiB page or two apart); Go's runtime pays 2.72 MiB and Python's interpreter
paid 7.06 MiB (last measured 2026-06-18, not re-run). Every MIR Kāra binary is ~300–390 KB
where the legacy backend's were ~34 KB (kara ledger
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); this one is **295.8 KiB**
(302,880 B, was 33,904 B on legacy), 1.54× under Rust and 9.0× over C (Go's static runtime
is 2.4 MiB). On the MIR backend compile no longer favours Kāra: karac is 1.39× slower than
`rustc -O` (125.2 vs 89.9 ms) and peaks at 2.3× its compiler RSS (59.8 vs 26.4 MiB); the
legacy build was 80.2 ms / 15.5 MiB, ahead of rustc on both. clang's 47.2 ms / 2.6 MiB is
the toolchain floor.

## Kāra features exercised

- **Recursive backtracking that mutates a borrowed board in place** — `go` takes the
  board (and the three masks) as `mut ref Array[i64, N]` in the bench / `mut ref Vec[Vec[i64]]`
  in the pedagogical files, writes a cell, recurses, and on failure clears it; the search
  state lives entirely in the borrowed views, no per-node heap.
- **`mut ref Array[i64, N]` — a fixed-array exclusive borrow with `noalias`** — the bench's
  `solve`/`go` take the board and masks as `mut ref Array[i64, 81]` / `mut ref Array[i64, 9]`,
  the precise type for a fixed-size grid (length is in the type) and the closest analog to
  C's `int64_t *restrict` / Rust's `&mut [i64; 81]`. Each borrow lowers to a single `ptr`
  carrying LLVM `noalias` — sound because the exclusive-borrow rule is now enforced at call
  sites ([`B-2026-06-17-6`](../../../../kara/docs/bug-ledger.jsonl)) — and indexes correctly
  thanks to [`B-2026-06-17-1`](../../../../kara/docs/bug-ledger.jsonl). The four masks +
  board are declared mutually non-aliasing, the disjointness the search relies on.
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

**Bug ledger** — this kata surfaced four `karac` findings, **all four now fixed**:
[`B-2026-06-17-4`](../../../../kara/docs/bug-ledger.jsonl) (typecheck, **fixed `3ab709a2`**)
— a `mut ref` argument wouldn't downgrade to a `ref` parameter under `karac build`; fixed
with the `mut ref T → ref T` reborrow arm, so the plain solver uses the natural `ref`.
[`B-2026-06-17-6`](../../../../kara/docs/bug-ledger.jsonl) (ownership, **fixed `1e0fe5ea`**)
— the **exclusive-borrow rule wasn't enforced at call sites** (`f(mut v, mut v)` compiled
and codegen diverged from the interpreter on the aliased call); now a hard error, which
makes Kāra's `noalias`-on-`mut ref` sound. [`B-2026-06-17-5`](../../../../kara/docs/bug-ledger.jsonl)
(codegen, **fixed**) — the noalias question itself: `mut ref` noalias is emitted and (post
B-6) sound, and the kata's natural `mut ref Array` form gets it; the earlier claim that
noalias was the Rust gap was **wrong** (measured ~1.5%). And
[`B-2026-06-17-7`](../../../../kara/docs/bug-ledger.jsonl) (codegen, **fixed
`1de4eb1e`**) — the residual to Rust, which IR/asm isolation of `go` pinned to **loop
unrolling**: Rust fully unrolled the `while d <= 9` candidate loop while karac left it at
the (correct) C-floor rolled form. Both the bounds-check and noalias hypotheses were
measured and *refuted* first; the proof that unrolling was the whole gap is that the C
mirror with `#pragma clang loop unroll(full)` lands exactly on Rust and rustc with its
unroller off drops back onto Kāra/C. The fix emits `llvm.loop.unroll.full` on small
constant-trip counted loops, which takes Kāra **1.03× ahead of Rust** here (and 2.88× on
[#36](../36-valid-sudoku/)). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).

**Surfaced [`B-2026-10-31-44`](../../../../kara/docs/bugs-v2.md)** (perf, open). The MIR
backend never emits the full-unroll hint on the `while d <= 9` candidate loop (it recurses
and exits early) — the exact loop `B-2026-06-17-7` targeted — so the bench went from 0.97×
to 1.37× `rustc -O`. Shared with [#36](../36-valid-sudoku/).

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Gaps found, in the kara bug ledger:

- **B-2026-10-06-88** — `let bit: u16 = 1 << (d as u16);` and every operator tree of bare literals were refused in a narrow type context. A fix is in flight.
- **B-2026-10-06-89** — `.iter()` on an indexed element of a struct field (`g.rows[i].iter()`) is refused by `karac build`.
- **B-2026-10-06-90** — a repeat literal into a narrow `Array[u16, N]` field of a multi-field struct fails LLVM module verification.
- The kata-10 repeat-literal aliasing (B-2026-10-06-81) and the kata-3 chain row (B-2026-10-06-80) were hit again.
