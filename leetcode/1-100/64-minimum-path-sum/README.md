# 64. Minimum Path Sum

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-path-sum](https://leetcode.com/problems/minimum-path-sum/)

The per-cell-cost sequel to katas [#62](../62-unique-paths/) (count paths) and [#63](../63-unique-paths-ii/) (count paths around obstacles). Same `m × n` grid, same **right**/**down** moves — but now every cell carries a non-negative **cost**, and instead of *counting* paths we want the single path whose costs sum to the **least**.

```
[[1,3,1],          →  7     the route 1 → 3 → 1 → 1 → 1  (right, right, down, down)
 [1,5,1],                    sums to 7 — no other right/down path is cheaper
 [4,2,1]]

[[1,2,3],          →  12    1 → 2 → 3 → 6
 [4,5,6]]
```

**Constraints:** `1 ≤ m, n ≤ 200`; `0 ≤ grid[i][j] ≤ 200`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Rolling 1-D DP** ★ — one array spanning the columns, `dp[c] = grid[i][c] + min(dp[c], dp[c-1])` | O(m·n) time, O(n) space | [`minimum_path_sum.kara`](minimum_path_sum.kara) ✓ via `karac run` / `karac build` | [`minimum_path_sum.py`](minimum_path_sum.py) ✓ |
| **Full 2-D DP table** — materialise every cell, `best[i][j] = grid[i][j] + min(best[i-1][j], best[i][j-1])` | O(m·n) time, O(m·n) space | [`minimum_path_sum_2d.kara`](minimum_path_sum_2d.kara) ✓ | — |
| **In place** — reuse the grid itself as the DP table, `grid[i][j] += min(grid[i-1][j], grid[i][j-1])` | O(m·n) time, **O(1) extra** space | [`minimum_path_sum_inplace.kara`](minimum_path_sum_inplace.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all twelve test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## The recurrence — swap `+` for `cost + min`

Katas #62 and #63 *summed* over both in-neighbours (count every way to arrive). Minimum Path Sum instead *chooses* the cheaper in-neighbour and pays the current cell's cost:

```
best[i][j] = grid[i][j] + min(best[i-1][j], best[i][j-1])
```

with the borders forced, since a border cell has only **one** in-neighbour:

```
best[0][0] = grid[0][0]
best[0][j] = best[0][j-1] + grid[0][j]     top row: only reachable from the left
best[i][0] = best[i-1][0] + grid[i][0]     left column: only reachable from above
```

This is exactly the generalisation #62's README flagged as forcing the DP: *"add per-cell costs (#64) and there is no closed form — the recurrence becomes mandatory."* There is no binomial and no axis symmetry to exploit; the `min` turns the problem into a shortest-path over a DAG that a single row-by-row scan solves, because every edge points right or down (so a fixed scan order always visits a cell's predecessors first).

**Rolling 1-D DP** ([`minimum_path_sum.kara`](minimum_path_sum.kara)) is the ★. As in #62/#63 the recurrence only reads the row directly above, so a **single array**, updated in place left to right, suffices:

```
dp[c]  currently holds  best[i-1][c]   (the cell above, this column)
dp[c] = grid[i][c] + min(dp[c], dp[c-1])
                         ^^^^^  ^^^^^^^
                         above   left (already advanced to this row)
```

At the instant `dp[c]` is read it still holds the row-above value (not yet overwritten this pass), while `dp[c-1]` was already advanced to the current row — the two in-neighbours the `min` chooses between. The left column has no left neighbour, so `dp[0]` just accumulates downward (`dp[0] += grid[i][0]`). Like #63, obstacles/costs break any symmetry, so the buffer spans the real column count `n` — **O(n) space**.

**Full 2-D table** ([`minimum_path_sum_2d.kara`](minimum_path_sum_2d.kara)) is the textbook form: keep the whole `Vec[Vec[i64]]` best-cost grid. It has **no aliasing subtlety** — every cell is written once, and the two it reads (`best[i-1][j]` in the finished previous row, `best[i][j-1]` earlier in this row) are final before it is reached; the borders are explicit single-in-neighbour branches. Its cost is the O(m·n) grid the rolling form trades away.

**In place** ([`minimum_path_sum_inplace.kara`](minimum_path_sum_inplace.kara)) drops the extra buffer entirely: it overwrites the **grid itself**, since a cell's predecessors (above, left) are always converted to best-costs before the cell is reached in a top-to-bottom, left-to-right scan. After the scan `grid[i][j]` holds `best[i][j]` and `grid[m-1][n-1]` is the answer — **O(1) extra** space. It is the only solver here that *writes* a `Vec[Vec[i64]]` in place (nested index-assignment `grid[i][j] = …`, the write-side counterpart to the read-only double-indexing the 2-D form uses), so it exercises a distinct codegen surface; the shared `report` harness hands each solver an owned grid, so consuming it is free.

## Kāra features exercised

- **`Vec[i64]` rolling buffer with `min`** — `Vec.new()` + `push` to seed the top row, then in-place `dp[c] = grid[i][c] + min(dp[c], dp[c - 1])` read-modify-write indexing. The `cost + min` body is the delta from #62/#63's pure-sum RMW scan; `min` is the `std.cmp` free function (see the note below).
- **`ref Vec[Vec[i64]]` read vs owned-grid *write*** — the rolling and 2-D solvers borrow the grid (`grid: ref Vec[Vec[i64]]`) and read `grid[i][c]`; the in-place solver takes the grid **by value**, rebinds it `let mut g = grid`, and mutates nested elements `g[r][c] = …`. Read-side double-indexing is shared with katas [#54](../54-spiral-matrix/)/[#48](../48-rotate-image/); the write-side nested index-assignment is the surface #64 adds.
- **Nested array literals as test input** — `report([[1, 3, 1], [1, 5, 1], [4, 2, 1]], mut s)` builds the `Vec[Vec[i64]]` cost grids inline, the same literal-grid harness shape as katas [#54](../54-spiral-matrix/) and [#63](../63-unique-paths-ii/).
- **Shared `report`/`sums:` harness** — one answer per line plus a folded `sums:` checksum, the byte-for-byte diff anchor used across katas [#53](../53-maximum-subarray/), [#62](../62-unique-paths/), and [#63](../63-unique-paths-ii/); all three solvers and the Python mirror print it identically. The call site `min_path_sum(grid)` is verbatim across all three — an owned argument passed to a `ref` param borrows implicitly, and passed to an owned param moves, so the same call compiles against both signatures.

**A found-gap-then-fixed note — `min` / `max` / `clamp` now ship.** This kata was first written when Kāra had **no** `min` in the stdlib: `a.min(b)` and `min(a, b)` were both rejected (`no method 'min' on type 'i64'` / `undefined name 'min'`), so the corpus hand-rolled a local `imin` helper (still visible in kata [#42](../42-trapping-rain-water/)). That gap was tracked as a roadmap item (`kara/docs/roadmap.md` § `std.cmp`) and has since **landed** — `min[T: Ord]` / `max[T: Ord]` / `clamp[T: Ord]` are ordinary generic stdlib free functions in `runtime/stdlib/ordering.kara` — so all three solvers here now use the natural `min(above, left)` directly, the helper deleted. This is the corpus loop working as intended: a kata surfaces the gap, the *compiler* is fixed (not the kata worked around), and the kata is rewritten to the natural form. `min`/`max`/`clamp` are correct in the interpreter for every `Ord` type and in compiled output for **Copy** types (`i64` here, plus `f64`/`usize`/`bool`/`char`); a compiled-output leak for **heap-owning** `Ord` types (`String`, heap structs) is tracked separately as `B-2026-07-08-6` and does not touch this kata's i64 use. (Costs ≤ 200 with m, n ≤ 200 bound the answer to ≤ 80,000, so i64 never approaches overflow.)

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   minimum_path_sum.kara
karac build minimum_path_sum.kara && ./minimum_path_sum

# The alternative approaches (identical output):
karac run minimum_path_sum_2d.kara
karac run minimum_path_sum_inplace.kara

# Python
python3 minimum_path_sum.py

# Verify they all agree
diff <(karac run minimum_path_sum.kara) <(python3 minimum_path_sum.py)             && echo OK
diff <(karac run minimum_path_sum.kara) <(karac run minimum_path_sum_2d.kara)      && echo OK
diff <(karac run minimum_path_sum.kara) <(karac run minimum_path_sum_inplace.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`minimum_path_sum.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-08).** The numbers below were measured on the corpus's **Apple M5 Pro reference machine** (arm64, clang 21 / rustc 1.95 / go 1.26), replacing the earlier provisional x86-64 cloud-container snapshot. **The surprising first-pass result — kāra *ahead* of both C and Rust on the `cost + min` scan — reproduces on the M5:** kāra 222.4 ms vs rust 251.1 / c 250.6 ms (**~1.13× faster than both**), so the kāra-ahead finding is now a confirmed codegen win, not a container artifact. The run used current karac, which includes the `B-2026-07-08-3` strength-reduction fix — #64's cost predicate `((i*7+c*3+k)%13)+1` is the *same* counter-arithmetic shape that fix targets in #63, so #64 carries that improvement too — but note the lead already held on the pre-fix container run (kāra 1.20× ahead there), so the win is fundamentally the `min`-DP codegen, not the fix.

**Workload.** K = 1,000,000 iterations of the rolling min-path-sum ★. Each iteration sweeps the grid shape — `m = 2 + k%32`, `n = 2 + (k/32)%32`, both in `[2, 33]` — and threads `k` through an inline **cost** predicate `((i*7 + c*3 + k) % 13) + 1` (in `[1, 13]`), so both the shape and the cost field change every iteration (nothing to hoist). Using a predicate rather than a materialised `Vec[Vec[i64]]` grid keeps the one `Vec[i64]` dp buffer the only per-call allocation, so the measured body is the **`cost + min` RMW scan itself** — the one thing #64 adds over #62's pure sum and #63's obstacle branch (the alloc-domination pitfall BENCHMARKS.md warns against is avoided). Because `min` here is the `std.cmp` generic free function, the run also probes whether generic-stdlib `min` lowers as tightly as C's `a < b ? a : b` / Rust's `.min()`. The answer is tiny (≤ ~300), far inside i64. The sink is a rolling polynomial hash `acc = (acc*131 + ans) % 1_000_000_007`; all four compiled mirrors must agree on `355333129` before timing.

**Seq-only kata** (BENCHMARKS.md two-lane discipline): the hash sink is a **loop-carried dependency**, so the K-loop is not a reduction karac's auto-par pass can split — the default `karac build` stays single-threaded. The kāra row is directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core basis.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All four single-threaded. **M5 Pro numbers (see the confirmation note above).**

| Implementation | Wall time |
|---|---|
| **kāra minimum_path_sum**            | **222.4 ± 5.5 ms** |
| go   minimum_path_sum                | 234.0 ± 4.5 ms |
| c    minimum_path_sum (clang -O3)    | 250.6 ± 3.3 ms |
| rust minimum_path_sum (rustc -O)     | 251.1 ± 4.6 ms |

On the M5 kāra is **~1.13× faster than Rust and ~1.13× faster than C**, and ~1.05× ahead of Go — **kāra leads the pack**, confirming the container first pass (which had it 1.20× ahead; Rust/C gain more from the M5's newer cores, so the lead narrows but holds). The result is doubly notable because kāra pays default integer-overflow checks that `rustc -O` / `clang -O3` skip, yet still wins — the lead is the `std.cmp` generic `min` lowering to a branchless `csel` on the rolling `dp` scan (no misprediction tax that a `a < b ? a : b` ternary can incur on this data), combined with the #62 `bce_length_pin` bounds-check elision and the #63 `B-2026-07-08-3` strength-reduction of the cost predicate. This is the first grid-DP kata where kāra *leads* rather than reaches parity.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py minimum_path_sum` (K=100k) | 4569 ± 259 ms |

Python at K=100k is ~4.57 s; projecting to the compiled mirrors' K=1M (~45.7 s) puts it **~108× slower than kāra seq** — a wider Python gap than #62's ~16.7× or #63's ~91×, because the per-cell body now does a `min` and a `% 13` on top of the additions, all of which CPython runs bytecode-by-bytecode.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 minimum_path_sum.c          | **41.7 ms** |
| **karac build minimum_path_sum.kara** | **81.2 ms** |
| rustc -O minimum_path_sum.rs          | 83.5 ms |

On the M5 karac compiles at ~1.95× clang but **edges rustc** (81.2 vs 83.5 ms). Small-single-file compile time is dominated by process/LLVM-init overhead.

### Binary size

| Implementation | Size |
|---|---|
| c    minimum_path_sum                | 32.7 KiB |
| **kāra minimum_path_sum**            | **33.3 KiB** |
| go   minimum_path_sum                | 2.38 MiB |
| rust minimum_path_sum                | 455.4 KiB |

Kāra's seq binary is **33.3 KiB — within ~0.6 KiB of C**, and far below Rust's 455 KiB and Go's 2.4 MiB. Adding the `std.cmp` `min` dependency did **not** grow the binary (essentially the same floor as #62/#63 on the M5).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra minimum_path_sum**            | **1.09 MiB** |
| c    minimum_path_sum                | 1.22 MiB |
| rust minimum_path_sum                | 1.22 MiB |
| go   minimum_path_sum                | 9.00 MiB |

Kāra's peak RSS is the **lowest of the four** (~0.13 MiB below C and Rust; the per-call dp buffer is freed inside the loop, so steady state is flat across all 1,000,000 iterations); Go's is ~8× higher for its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 minimum_path_sum.c          | **2.6 MiB** |
| **karac build minimum_path_sum.kara** | **19.6 MiB** |
| rustc -O minimum_path_sum.rs          | 28.2 MiB |

On the M5 karac's compile-memory footprint sits between clang (lowest) and rustc — well under rustc's.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. This kata completes the grid-DP triple — #62 (pure-sum scan, C/Rust parity after a codegen fix), #63 (sum + obstacle branch, parity after the `B-2026-07-08-3` strength-reduction fix), #64 (`cost + min` scan, the `min` a real `std.cmp` call). **#64 is where the family finally *leads*:** the M5 re-bench confirms kāra ~1.13× ahead of both Rust and C (see the confirmation note), driven by the branchless generic-`min` lowering on top of the #62/#63 check-elision work — kāra wins despite paying default overflow checks the native mirrors skip. It also carries the lowest peak RSS of the four.
