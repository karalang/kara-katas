# 51. N-Queens

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/n-queens](https://leetcode.com/problems/n-queens/)

Place `n` queens on an `n × n` chessboard so that no two attack each other — no shared row,
column, or diagonal — and return **every** distinct placement. Each solution is a list of board
rows, `'Q'` for a queen and `'.'` for an empty square.

```
n = 4  →  2 solutions

  .Q..        ..Q.
  ...Q        Q...
  Q...        ...Q
  ..Q.        .Q..
```

**Constraints:** `1 ≤ n ≤ 9`. The number of solutions is the (in)famous sequence
`1, 0, 0, 2, 10, 4, 40, 92, 352` for `n = 1 … 9` — note `n = 2` and `n = 3` have **none**.

## Why this kata — one search, three ways to say "is this square safe?"

The move that makes N-Queens tractable is to place **exactly one queen per row** and descend row by
row. That discharges the "no two on a row" rule by construction and turns the search into "for each
row, which column?" — an `n`-way branch at each of `n` levels, pruned hard by the attack test. Two
queens at `(r1, c1)` and `(r2, c2)` attack iff they share a column (`c1 == c2`) or a diagonal, and
the diagonal test is the elegant part:

```
cells on the same ↘ diagonal share   row + col
cells on the same ↙ diagonal share   row − col
```

So a queen at `(row, col)` is legal iff its **column** and **both diagonal keys** are still free.
Every solver here walks the *same* DFS tree in the *same* column order (`0..n` ascending), so they
emit the **identical** solution listing — LeetCode's canonical order. The only axis that changes is
how "is this square safe?" is answered:

| Lens | Occupancy state | Legality test | Undo |
|---|---|---|---|
| **Marker arrays** ★ | three `Vec[bool]` (`cols`, `diag1[row+col]`, `diag2[row−col+n−1]`) | O(1) array reads | clear three flags + `pop` |
| **Conflict scan** | none — just `queens[r]` | O(row) scan of placed queens, `|Δrow| == |Δcol|` | `pop` only |
| **Bitmask** | three `i64` bit-sets, passed **by value** | O(1) `mask & bit == 0` | **automatic** (parent keeps its copy) |

This is the same space-for-time spectrum the permutation katas ([#46](../46-permutations/),
[#47](../47-permutations-ii/)) laid out — an O(n) side-array with O(1) lookup at one end, a
side-array-free O(depth) rescan at the other — with a third, sharper option the bitset makes
possible: encode all three occupancy sets in the bits of three integers and let by-value copying do
the backtracking for free.

### The diagonal keys, and the `+(n−1)` bias

`row + col` ranges over `0 … 2n−2` — already a valid array/bit index. `row − col` ranges over
`−(n−1) … n−1`, so the marker-array and bitmask solvers add `(n−1)` to shift it into `0 … 2n−2`
before indexing. The conflict-scan solver sidesteps keys entirely: two queens are on a common
diagonal exactly when the vertical and horizontal gaps between them are equal, `|row−pr| == |col−pc|`
— one `.abs()` comparison, no arrays at all.

### Why the bitmask needs no cleanup

The marker-array solver brackets every choice with *set three flags → recurse → clear three flags*;
the scan solver only has the `queens` path entry to `pop`. The bitmask solver has **nothing** to
undo on the occupancy side: `i64` is a plain copied scalar, so `place(…, cols | bit_c, …)` hands the
child an updated copy while the parent's masks stay exactly as they were. "Undo" is implicit — the
same trick [#46](../46-permutations/)'s immutable-snapshot solver uses, here on three integers
instead of a path vector.

## Approaches

| Approach | File | Occupancy representation |
|---|---|---|
| **Marker arrays** ★ | [`marker_arrays.kara`](marker_arrays.kara) | three `Vec[bool]`, flipped in lockstep, O(1) test |
| **Conflict scan** | [`conflict_scan.kara`](conflict_scan.kara) | none — rescans placed queens, `|Δrow| == |Δcol|` |
| **Bitmask** | [`bitmask.kara`](bitmask.kara) | three `i64` bit-sets, by-value copy = free undo |
| Oracle | [`n_queens.py`](n_queens.py) | mirrors the ★ solver + identical output format |

Everything below the legality test — the row-by-row recursion, the `queens` path, the
`build_board` renderer, and the test harness — is line-for-line identical across the three `.kara`
files. The kata's point is that the search is one algorithm; only the safety test differs.

## What this kata surfaced

**A clean pass — no compiler gap.** All three solvers compiled and ran correctly the first time
under **both** `karac run` and `karac build`, and the benchmark's scalar `mut ref i64` out-parameters
(the counting kernel threads `acc` and `sink` by mutable reference) lowered cleanly on both surfaces
too. Every configuration — `karac run`, `karac build`, and default auto-par — is byte-identical to
the Python oracle and to each other, for the full board listings **and** the `n = 1..9` count sweep.
Not every kata turns up a bug; probing three canonical backtracking mechanisms and confirming they
all typecheck, run, and codegen identically is itself the coverage this corpus is for.

The one thing worth flagging is a **call-site-marker** subtlety the ★ solver exercises: the four
mutable references (`cols`, `diag1`, `diag2`, `queens`, `out`) get their `mut` markers at the **root**
call in `solve` (where they are fresh owned bindings), and the **interior** recursive call forwards
the already-`mut ref` bindings **unmarked**. Re-marking them at the recursive call is a hard error
under `karac build` (a warning under `karac run`) — the same rule the permutation katas document.

## Kāra features exercised

- **Recursive backtracking** with `mut ref` accumulators threaded through the DFS.
- **`Vec[bool]` marker arrays** — the sub-word-element collection the wildcard/permutation katas
  stressed; here three of them flipped in lockstep.
- **`Vec[String]` / `Vec[Vec[String]]`** — boards built char-by-char (`row.push('Q')`) and collected.
- **`i64` bit ops** — `1 << c`, `mask & bit`, `mask | bit` for the bitmask occupancy sets.
- **`i64.abs()`** — the symmetric diagonal test in the conflict-scan solver.
- **Scalar `mut ref i64` out-parameters** — the benchmark's `acc` / `sink` accumulators.

## Running

```bash
# Kāra — interpreter and codegen produce the same output.
karac run   marker_arrays.kara
karac build marker_arrays.kara && ./marker_arrays

# Python oracle
python3 n_queens.py

# Verify all four agree, byte-for-byte
diff <(karac run marker_arrays.kara) <(python3 n_queens.py)     && echo OK
diff <(karac run marker_arrays.kara) <(karac run conflict_scan.kara) && echo OK
diff <(karac run marker_arrays.kara) <(karac run bitmask.kara)  && echo OK
```

All three solvers are byte-identical to the oracle under `karac run`, `karac build` (default
auto-par), and `KARAC_AUTO_PAR=0`.

## Benchmarks

### How to run

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
| [`bench/nqueens_bench.kara`](bench/nqueens_bench.kara) | bitmask solution-**counter** (no board build) over `n = 8..13`, weighted-checksum sink |
| [`bench/nqueens_bench.rs`](bench/nqueens_bench.rs) | mirror; `&mut i64` out-params; `rustc -O` |
| [`bench/nqueens_bench.c`](bench/nqueens_bench.c) | mirror; pointer out-params; `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | mirror; `*int64` out-params; `go build` |
| [`bench/nqueens_bench.py`](bench/nqueens_bench.py) | mirror; list-boxed accumulators; CPython |

**Workload.** The bench drops the board rendering and runs the **pure counting kernel** (the
bitmask solver's core) over board sizes `n = 8..13`. Those six searches enumerate
`92 + 352 + 724 + 2680 + 14200 + 73712 = 91_760` solutions between them, dominated by `n = 13`. Each
leaf folds a placement-dependent checksum `Σ_r queens[r]·(r+1)` so the sink depends on the actual
queen positions, not merely their count; every language accumulates `acc·100003 + sink` per `n` into
one `i64` that all five print identically — a **bit-exact, cross-language-diffable sink**
(`9223752374`). The magnitudes stay far inside `i64`, so the fold never overflows.

**Seq-only kata.** The counting DFS is one deep recursive chain with no cross-branch parallel
structure the auto-par cost model engages, so the Kāra binary is built `KARAC_AUTO_PAR=0` and the seq
row is the apples-to-apples comparator against the native single-file compilers.

### Runtime

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 5 --runs 30`, means:

| Implementation | Wall time | User-CPU |
|---|---|---|
| `rust nqueens_bench` (rustc -O) | **80.0 ms ± 1.3 ms** | 78.3 ms |
| `c    nqueens_bench` (clang -O3) | **82.9 ms ± 0.2 ms** | 81.3 ms |
| **`kara nqueens_bench`** (codegen, seq) | **155.6 ms ± 1.2 ms** | 153.6 ms |
| `rust nqueens_bench` (`-C overflow-checks=on`) | **167.6 ms ± 1.3 ms** | 165.4 ms |
| `go   nqueens_bench` (go build) | **172.7 ms ± 2.7 ms** | 170.2 ms |
| `py   nqueens_bench` (CPython) | **4683 ms** | — |

**Read the two Rust rows together — that's the apples-to-apples story.** The hot kernel is nothing
but integer arithmetic: three shifts, three masks, and a `c·(row+1)` checksum per candidate, run
across a 91_760-leaf search tree. Kāra **traps on integer overflow by default**
([design.md § Arithmetic Overflow](../../../../kara/docs/design.md): "defined behavior, never
undefined"); `rustc -O` **silently wraps**. So the equal-safety build — Rust with
`-C overflow-checks=on` — is the comparison that holds safety constant, and against it **Kāra is
actually faster**: 155.6 ms vs 167.6 ms, a **1.08× win**, while *also* edging out Go (0.90×). The
wider **1.95×** against `rustc -O`'s default is the silent-wraparound the checks buy back — this
kernel never actually overflows, but Kāra checks every `row + c` and `c · (row + 1)` like the
language guarantees, and so does the checked-Rust row. C and Go wrap too; they are the unsafe-but-fast
floor (`clang -O3` at 82.9 ms), not safety peers. Kāra is **30× faster than CPython**.

So on a pure branchy-recursion integer kernel, Kāra's default-safe output lands **ahead of both
safety-matched Rust and Go**, and the only gap that remains is the ~1.9× the wrapping compilers get
by opting out of the overflow checks Kāra refuses to ship without.

### Compile time, binary size, memory

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 1 --runs 10` (compile, cold via `--prepare`);
size and peak RSS are single deterministic samples.

| Compiler | Compile (cold) | Binary | Peak RSS |
|---|---|---|---|
| `clang -O3` | 40.0 ms | 32.7 KiB | 1.02 MiB |
| `rustc -O` | 73.5 ms | 455.4 KiB | 1.05 MiB |
| **`karac build`** | **77.0 ms** | **33.0 KiB** | **1.00 MiB** |
| `go build` | — (excluded; mixes module + std-lib link) | 2434.1 KiB | 2.73 MiB |

Kāra emits a binary **~14× smaller than Rust** and line-ball with C (33.0 vs 32.7 KiB), and actually
posts the **lowest peak RSS of the four** (1.00 MiB, a hair under C and Rust, ~2.7× under Go and ~6.8×
under CPython). Its cold compile is on par with `rustc -O` (77.0 vs 73.5 ms) and ~1.9× behind
`clang`.
