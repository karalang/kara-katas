# 52. N-Queens II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/n-queens-ii](https://leetcode.com/problems/n-queens-ii/)

Return **how many** distinct ways `n` queens can be placed on an `n × n` board so that no two
attack each other — no shared row, column, or diagonal. This is [#51 N-Queens](../51-n-queens/)
stripped to a single number: the boards are never materialized, only counted.

```
n = 4  →  2          n = 8  →  92

counts for n = 1 … 11:
  1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680      (n = 2 and n = 3 have none)
```

**Constraints:** `1 ≤ n ≤ 9`. The solvers here sweep to `n = 11` to exercise deeper trees.

## Why this kata — the search is #51's; the *answer* is a number, and that changes everything

The engine is identical to [#51](../51-n-queens/): place exactly one queen per row, descend row by
row, and prune with the column-and-both-diagonals test (cells share a ↘ diagonal iff `row + col`
matches, a ↙ diagonal iff `row − col` matches). What changes is that #52 wants only the **count** —
and that single change dissolves the entire solution-materialization apparatus of #51. There is no
board to render, no `queens` path to snapshot, no `out` vector to grow. What remains is the bare
tree, and the kata is about the two axes that opens up:

**Axis 1 — how do you tally a search?** Two idiomatic answers, and the kata pins both:

| Lens | Occupancy state | How the count accumulates |
|---|---|---|
| **Bitmask, return-value** ★ | three `i64` bit-sets, by value | `count(...) -> i64` — the recursion **returns** the number and each level sums its children (`return 1` at a full board) |
| **Marker arrays, accumulator** | three `Vec[bool]` | `count(...)` returns nothing and bumps a `total: mut ref i64` **accumulator** threaded through the DFS |

The ★ solver is pure: with no `mut ref`, the search state is *exactly* its arguments, and the answer
flows back up the return edges. The marker solver is its mirror image — the occupancy lives in
mutable side-arrays flipped set/recurse/clear, and the tally rides a mutable out-parameter (the same
`mut ref i64` out-param shape the #51 benchmark's counting kernel used). Same number, two opposite
disciplines for producing it.

**Axis 2 — can you search *less*?** Yes — and only because we're counting. Reflecting a solved board
left↔right (`col ↦ n−1−col`) maps a valid placement to another valid placement, so if `f(c)` counts
solutions whose first-row queen sits in column `c`, then `f(c) = f(n−1−c)`. Therefore

```
total  =  Σ_c f(c)  =  2 · Σ_{c < n/2} f(c)   [ + f(n/2) when n is odd ]
```

Search the first-row queen across only the **left half** of the board, double it, and for odd `n`
add the exact-center column's count once (its mirror is itself, so it isn't doubled). That visits
~half the tree.

| Lens | Trick |
|---|---|
| **Symmetry-folded bitmask** | fix the first-row queen outside the recursion, count left-half columns, `2 ·` them, `+` the center for odd `n` |

Crucially, **#51 could not use this.** Listing every board in canonical column order means you cannot
skip the right half and fabricate the mirrored boards for free — you'd have to reconstruct and
re-sort them. #52 wants only the tally, so the right half is recovered by arithmetic (`2 ·`) instead
of by search. The optimization is a property of *counting*, not of the puzzle.

### The diagonal keys, and the `+(n−1)` bias

`row + col` ranges over `0 … 2n−2` — already a valid array/bit index. `row − col` ranges over
`−(n−1) … n−1`, so the marker-array and bitmask solvers add `(n−1)` to shift it into `0 … 2n−2`
before indexing. Every solver descends columns `0..n` low-to-high, so all three walk the same DFS
tree and reach the identical count for every `n`.

## Approaches

| Approach | File | Count via | Tree searched |
|---|---|---|---|
| **Bitmask, return-value** ★ | [`bitmask_count.kara`](bitmask_count.kara) | `-> i64` return value | full |
| **Marker arrays, accumulator** | [`marker_arrays.kara`](marker_arrays.kara) | `mut ref i64` out-parameter | full |
| **Symmetry-folded bitmask** | [`symmetry.kara`](symmetry.kara) | `-> i64`, first row halved & doubled | ~half |
| Oracle | [`n_queens_ii.py`](n_queens_ii.py) | mirrors the ★ solver + identical output format | full |

All three `.kara` files share a line-for-line-identical test harness (`n = 1..11`, one count per line
plus a `counts:` summary) and diff byte-for-byte against the Python oracle under `karac run`,
`karac build`, and the default auto-par build.

## What this kata surfaced

Unlike [#51](../51-n-queens/) — a clean pass — #52's two new mechanisms (a `mut ref i64` accumulator
threaded down a recursion, and a return-value reduction) each turned up a **real, distinct compiler
bug**. Both are fixed; both now A/B-verify green across all three surfaces.

**[B-2026-07-03-13](../../../../kara/docs/bug-ledger.md) — interpreter: `mut ref` scalar write-back
lost through forwarded calls.** The marker-array solver counted **all zeros** under `karac run` while
being correct under `karac build`. The tree-walk interpreter's copy-in-copy-out write-back for a
`mut ref` parameter keyed only on the *call-site* `mut` marker — but per
[design.md § Call-site mutation markers](../../../../kara/docs/design.md), an already-in-scope
`mut ref` binding **forwards without a marker**. So the innermost `total = total + 1` updated a local
copy that no intermediate frame ever propagated back, and the accumulator stayed 0. The fix keys the
write-back on the callee's **declared param mode** (`mut ref` / `mut Slice`) as well, matching the
full aliasing codegen already had. Minimal repro:

```kara
fn inc(x: mut ref i64) { x = x + 1i64; }
fn wrap(x: mut ref i64) { inc(x); }          // forwards x unmarked
fn main() { let mut t: i64 = 0; wrap(mut t); println(t); }   // was 0, now 1
```

**[B-2026-07-03-14](../../../../kara/docs/bug-ledger.md) — auto-par: parallelizing a reduction whose
delta recurses.** Both return-value solvers **crashed with a bus error** (`exit 138`) under the
default auto-par build at `n ≳ 9`, while `karac run` and `KARAC_AUTO_PAR=0 karac build` were correct.
The reduction analyzer recognized `if legal { total = total + count(...deeper...) }` as a valid `+`
reduction and parallelized the loop — but the delta *recurses into the same function*, so every
recursion level opened a fresh nested parallel region and the fan-out compounded into runaway task
nesting that exhausted the stack (correct output survived only for tiny `n ≤ 6`). The fix declines
reduction recognition when the loop body directly recurses into its enclosing function, keeping the
correct sequential lowering. Direct self-recursion — the backtracking-counter shape — is the common
case; transitive recursion through a helper is a tracked residual.

The marker-array solver, by contrast, is a `mut ref` accumulator (not a return-value reduction), so
auto-par never treated its loop as a reduction — it was correct under auto-par once B-2026-07-03-13
was fixed.

## Kāra features exercised

- **Return-value recursion** summing a search tree (`count(...) -> i64`, `return 1` at the leaf) —
  the ★ and symmetry solvers' purely functional tally, no mutable state beyond the arguments.
- **`mut ref i64` accumulator threaded through recursion** — the marker solver's out-parameter tally,
  the exact shape B-2026-07-03-13 was hiding in.
- **`Vec[bool]` marker arrays** flipped set/recurse/clear in lockstep (three axes).
- **Integer bitmasks** (`1 << c`, `mask & bit == 0`, by-value copy = free backtracking).
- **Mirror-symmetry pruning** — `f(c) = f(n−1−c)`, left-half search doubled with an odd-`n` center
  special case.

## Benchmarks

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh          # KARA_BENCH_INCLUDE_PY=1 to include the Python row
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file
with `karac build` (`KARAC_AUTO_PAR=0`), and the Go module with `go build` (all cached in
`bench/target/`, gitignored), then times them with `hyperfine` per the
[BENCH.md protocol](../../../BENCH.md) and writes [`bench/results.json`](bench/results.json).

| File | What it does |
|---|---|
| [`bench/nqueens2_bench.kara`](bench/nqueens2_bench.kara) | **return-value** counting kernel over `n = 9..13`, one `i64` sink |
| [`bench/nqueens2_bench.rs`](bench/nqueens2_bench.rs) | mirror; `-> i64` return; `rustc -O` |
| [`bench/nqueens2_bench.c`](bench/nqueens2_bench.c) | mirror; `int64_t` return; `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | mirror; `int64` return; `go build` |
| [`bench/nqueens2_bench.py`](bench/nqueens2_bench.py) | mirror; CPython |

**Workload.** The bench drops the count/board distinction and runs the **return-value counting
kernel** — the ★ solver's kernel, but each leaf returns `1 + partial` where
`partial = Σ_r queens[r]·(r+1)` is a placement-dependent checksum accumulated as columns are chosen.
So the sink depends on the actual queen positions, not merely the solution count, and no shortcut can
skip the descent. Swept over `n = 9..13` (which enumerate `352 + 724 + 2680 + 14200 + 73712 = 91_760`
solutions, dominated by `n = 13`), the kernel folds to one `i64` that every language prints
identically (`47557170`) — a **bit-exact, cross-language-diffable sink**. Magnitudes stay far inside
`i64`, so the fold never overflows.

This kernel is exactly the return-value reduction that tripped B-2026-07-03-14; the Kāra binary is
built `KARAC_AUTO_PAR=0` (the counting DFS is one deep recursive chain with no cross-branch parallel
structure worth engaging), and — post-fix — the default auto-par build now produces the *same* sink
sequentially rather than crashing.

### Runtime

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 5 --runs 30`, means:

| Implementation | Wall time | User-CPU |
|---|---|---|
| `c    nqueens2_bench` (clang -O3) | **80.2 ms ± 2.3 ms** | 78.6 ms |
| `rust nqueens2_bench` (rustc -O) | **80.6 ms ± 1.0 ms** | 79.1 ms |
| **`kara nqueens2_bench`** (codegen, seq) | **166.4 ms ± 2.5 ms** | 165.0 ms |
| `rust nqueens2_bench` (`-C overflow-checks=on`) | **177.5 ms ± 3.2 ms** | 174.6 ms |
| `go   nqueens2_bench` (go build) | **181.2 ms ± 4.4 ms** | 178.8 ms |
| `py   nqueens2_bench` (CPython) | **4702 ms** | — |

**Read the two Rust rows together — that's the apples-to-apples story.** The hot kernel is pure
integer arithmetic: three shifts, three masks, and a `c·(row+1)` checksum per candidate across a
91_760-leaf tree. Kāra **traps on integer overflow by default**
([design.md § Arithmetic Overflow](../../../../kara/docs/design.md): "defined behavior, never
undefined"); `rustc -O` **silently wraps**. So the equal-safety build — Rust with
`-C overflow-checks=on` — is the comparison that holds safety constant, and against it **Kāra is
faster**: 166.4 ms vs 177.5 ms, a **1.07× win**, while also edging out Go (0.92×, 166.4 vs 181.2). The
wider **2.06×** against `rustc -O`'s default is exactly the silent-wraparound the checks buy back —
this kernel never actually overflows, but Kāra checks every `row + c` and `c · (row + 1)` like the
language guarantees, and so does the checked-Rust row. C and Go wrap too; they are the unsafe-but-fast
floor (`clang -O3` at 80.2 ms), not safety peers. Kāra is **~28× faster than CPython**.

So on a pure branchy-recursion integer kernel, Kāra's default-safe output lands **ahead of both
safety-matched Rust and Go** — the same result [#51](../51-n-queens/) reached with the out-parameter
kernel, here reproduced with the pure return-value one — and the only gap left is the ~2× the
wrapping compilers get by opting out of the overflow checks Kāra refuses to ship without.

### Compile time, binary size, memory

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 1 --runs 10` (compile, cold via `--prepare`);
size and peak RSS are single deterministic samples.

| Compiler | Compile (cold) | Binary | Peak RSS |
|---|---|---|---|
| `clang -O3` | 39.2 ms | 32.7 KiB | 1.00 MiB |
| `rustc -O` | 72.4 ms | 455.4 KiB | 1.05 MiB |
| **`karac build`** | **75.1 ms** | **33.0 KiB** | **1.00 MiB** |
| `go build` | — (excluded; mixes module + std-lib link) | 2434.1 KiB | 2.66 MiB |

Kāra emits a binary **~14× smaller than Rust** and line-ball with C (33.0 vs 32.7 KiB), and ties C for
the **lowest peak RSS** (1.00 MiB, a hair under Rust and ~2.7× under Go, ~6.7× under CPython). Its cold
compile is on par with `rustc -O` (75.1 vs 72.4 ms) and ~1.9× behind `clang`. Every figure lands
within noise of [#51](../51-n-queens/)'s — the two katas compile the same shape of kernel.
