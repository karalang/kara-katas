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

> ⚠️ **Machine caveat — read before comparing.** Like kata [#63](../63-unique-paths-ii/#benchmarks)'s first pass (and unlike the M5 Pro tables elsewhere in the corpus), the numbers below were measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.10 GHz, 4 vCPU, Linux 6.18.5). So:
> - **Do NOT compare these absolute times/sizes/RSS against sibling katas' M5 tables** — different ISA, different toolchains (clang 18 / rustc 1.94 / go 1.24), and a noisier shared host. `bench/results.json` records the real host in `env.host`/`env.note`.
> - **The within-kata cross-language ratio is the signal** — every mirror ran on the same box back-to-back — but on this run it is **unusually noisy** (hyperfine flagged statistical outliers on the C runtime) and, more importantly, it **inverts** #62/#63's near-parity: kāra came out *ahead* of C and Rust here (see below), which is surprising enough that it **must be reproduced on the M5 before being treated as a real codegen win.** Re-run `bench/bench.sh` on the reference machine to settle it.

**Workload.** K = 1,000,000 iterations of the rolling min-path-sum ★. Each iteration sweeps the grid shape — `m = 2 + k%32`, `n = 2 + (k/32)%32`, both in `[2, 33]` — and threads `k` through an inline **cost** predicate `((i*7 + c*3 + k) % 13) + 1` (in `[1, 13]`), so both the shape and the cost field change every iteration (nothing to hoist). Using a predicate rather than a materialised `Vec[Vec[i64]]` grid keeps the one `Vec[i64]` dp buffer the only per-call allocation, so the measured body is the **`cost + min` RMW scan itself** — the one thing #64 adds over #62's pure sum and #63's obstacle branch (the alloc-domination pitfall BENCHMARKS.md warns against is avoided). Because `min` here is the `std.cmp` generic free function, the run also probes whether generic-stdlib `min` lowers as tightly as C's `a < b ? a : b` / Rust's `.min()`. The answer is tiny (≤ ~300), far inside i64. The sink is a rolling polynomial hash `acc = (acc*131 + ans) % 1_000_000_007`; all four compiled mirrors must agree on `355333129` before timing.

**Seq-only kata** (BENCHMARKS.md two-lane discipline): the hash sink is a **loop-carried dependency**, so the K-loop is not a reduction karac's auto-par pass can split — the default `karac build` stays single-threaded. The kāra row is directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core basis.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All four single-threaded. **Cloud-container numbers — see the caveat; the kāra-ahead result needs M5 confirmation.**

| Implementation | Wall time |
|---|---|
| **kāra minimum_path_sum**            | **422.8 ± 5.6 ms** |
| rust minimum_path_sum (rustc -O)     | 506.0 ± 10.6 ms |
| c    minimum_path_sum (clang -O3)    | 514.8 ± 20.0 ms |
| go   minimum_path_sum                | 668.1 ± 15.0 ms |

On this container kāra measured **~1.20× faster than Rust and ~1.22× faster than C**, with the tightest variance of the four (±5.6 ms; C showed ±20 ms and drew hyperfine's outlier warning), and ~1.58× ahead of Go. Kāra's fastest sample (415.8 ms) sits below C's and Rust's fastest (499/490 ms), so it is not merely the mean being dragged by C's noise. **This is a genuinely surprising result and is treated as provisional:** it inverts the near-parity #62/#63 measured on the same idiom family, kāra pays for default overflow checks that `rustc -O`/`clang -O3` skip (so a *lead* is doubly unexpected), and the host is a shared 4-vCPU box. A plausible mechanism — the `std.cmp` `min` lowering to a well-predicted branch/cmov combined with the #62 `bce_length_pin` check-elision on the `dp` scan — would explain a *parity*, not a 1.2× lead. **Do not quote "kāra beats C on min-path" until `bench/bench.sh` reproduces it on the M5 Pro.** The load-bearing claim today is only the sink agreement and that the `cost + min` scan is not *slower* than the native mirrors here.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py minimum_path_sum` (K=100k) | 4569 ± 259 ms |

Python at K=100k is ~4.57 s; projecting to the compiled mirrors' K=1M (~45.7 s) puts it **~108× slower than kāra seq** — a wider Python gap than #62's ~16.7× or #63's ~91×, because the per-cell body now does a `min` and a `% 13` on top of the additions, all of which CPython runs bytecode-by-bytecode.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 minimum_path_sum.c          | **97.2 ± 9.8 ms** |
| rustc -O minimum_path_sum.rs          | 126.7 ± 4.0 ms |
| **karac build minimum_path_sum.kara** | **184.4 ± 9.6 ms** |

On this container karac compiles at ~1.90× clang and ~1.45× rustc — slower than both, consistent with #63's container run (and the reverse of #62's M5 snapshot). Small-single-file compile time is dominated by process/LLVM-init overhead that differs across the toolchain sets.

### Binary size

| Implementation | Size |
|---|---|
| c    minimum_path_sum                | 15.7 KiB |
| **kāra minimum_path_sum**            | **324.5 KiB** |
| go   minimum_path_sum                | 2.11 MiB |
| rust minimum_path_sum                | 3.77 MiB |

Kāra's seq binary is **far below Rust's 3.8 MiB and Go's 2.1 MiB**, above C's 15.7 KiB — and byte-for-byte the same 332,304 B as #62/#63 built on this toolchain (the M5 build strips further; see #63's note). Adding the `std.cmp` `min` dependency did **not** grow the binary.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra minimum_path_sum**            | **7.07 MiB** |
| c    minimum_path_sum                | 7.07 MiB |
| rust minimum_path_sum                | 7.07 MiB |
| go   minimum_path_sum                | 7.29 MiB |

Kāra's peak RSS is identical to C's and Rust's (the per-call dp buffer is freed inside the loop, so steady state is flat across all 1,000,000 iterations); Go's is a touch higher for its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build minimum_path_sum.kara** | **84.7 MiB** |
| clang -O3 minimum_path_sum.c          | 96.8 MiB |
| rustc -O minimum_path_sum.rs          | 112.2 MiB |

On this container karac has the lowest compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. This kata completes the grid-DP triple — #62 (pure-sum scan, C/Rust parity after a codegen fix), #63 (sum + obstacle branch, parity held), #64 (`cost + min` scan, the `min` now a real `std.cmp` call). The first-pass container numbers put kāra *ahead* on #64, but that inverts the family's established parity and is held as provisional pending the M5 re-bench (see the machine caveat); the durable, machine-independent facts are the five-language sink agreement and that the generic-stdlib `min` lowers without a size or memory penalty.
