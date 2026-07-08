# 63. Unique Paths II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/unique-paths-ii](https://leetcode.com/problems/unique-paths-ii/)

The obstacle sequel to kata [#62](../62-unique-paths/). A robot starts at the top-left of an `m × n` grid and may move only **right** or **down**, but some cells hold **obstacles** (marked `1`) it may not stand on (free cells are `0`). How many distinct paths reach the bottom-right corner?

```
[[0,0,0],          →  2     the center obstacle leaves exactly two routes:
 [0,1,0],                    right-right-down-down  and  down-down-right-right
 [0,0,0]]

[[0,1],            →  1     the only route is down-then-right
 [0,0]]

[[1,0],            →  0     the start cell is blocked — no path exists at all
 [0,0]]
```

**Constraints:** `1 ≤ m, n ≤ 100`; each cell is `0` or `1`; the answer is guaranteed to be `≤ 2·10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Rolling 1-D DP** ★ — one array spanning the columns, `dp[c] += dp[c-1]`, forced to `0` at an obstacle | O(m·n) time, O(n) space | [`unique_paths_ii.kara`](unique_paths_ii.kara) ✓ via `karac run` / `karac build` | [`unique_paths_ii.py`](unique_paths_ii.py) ✓ |
| **Full 2-D DP table** — materialise every cell, `paths[i][j] = paths[i-1][j] + paths[i][j-1]` (or `0` at an obstacle) | O(m·n) time, O(m·n) space | [`unique_paths_ii_2d.kara`](unique_paths_ii_2d.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all thirteen test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The recurrence — #62's, plus one rule

Every cell still has exactly two in-neighbours — the robot arrives only from **above** or from the **left** — so the count is their sum, with one addition: a cell holding an obstacle has **zero** paths through it.

```
paths[i][j] = 0                              if grid[i][j] is an obstacle
paths[i][j] = paths[i-1][j] + paths[i][j-1]  otherwise
```

with `paths[0][0] = 1` when the start is clear (and `0` when it is blocked — then there are no paths at all). The change from kata #62 is small but it removes two things #62 relied on:

- **The top row and left column are no longer a blanket line of `1`s.** A straight run along the top row survives only up to the first obstacle; everything past it is cut off. The additive recurrence gets this for free — an obstacle zeroes `paths` there, and that `0` propagates rightward through the row-sum and downward through the column-sum, walling off exactly the unreachable region.
- **The axis symmetry `paths(m,n) == paths(n,m)` is gone.** Obstacles are not symmetric under transposition, so — unlike #62 — you cannot roll onto the *smaller* dimension; the array must span the real column count `n`. That is the one structural difference between this kata's ★ and #62's.

**Rolling 1-D DP** ([`unique_paths_ii.kara`](unique_paths_ii.kara)) is the ★. As in #62, the recurrence only ever reads the row directly above, so a **single array** updated in place, left to right, suffices:

```
dp[c]  currently holds  paths[i-1][c]   (the row above)
dp[c] += dp[c-1]        ->  paths[i-1][c] + paths[i][c-1] = paths[i][c]
```

At the instant `dp[c]` is read on the right it still holds the value from the row above (not yet overwritten this pass), while `dp[c-1]` was already advanced to the current row — exactly the two neighbours the recurrence wants. An obstacle overrides the sum with `dp[c] = 0`. The left-column cell `dp[0]` is seeded once to `1` (the single virtual path entering the corner) and thereafter is only touched to zero it at an obstacle — otherwise it carries straight down (the all-downs path). This is #62's read-before-overwrite left-to-right sweep with an obstacle guard threaded through it.

**Full 2-D table** ([`unique_paths_ii_2d.kara`](unique_paths_ii_2d.kara)) is the textbook form: keep the whole `Vec[Vec[i64]]` grid of path counts. It has **no aliasing subtlety at all** — every cell is written once, and the two cells it reads (`paths[i-1][j]` in the finished previous row, `paths[i][j-1]` earlier in this row) are final before it is reached. Absent neighbours (the top row's `i-1`, the left column's `j-1`) simply contribute `0`, so the single additive rule covers the borders too — no separate "seed the first row/column" pass, precisely because past the first obstacle those borders are *not* all-`1`s. Its cost is the O(m·n) grid the rolling form trades away for O(n); keeping it here shows the space optimisation as a diff and cross-checks the recurrence independently.

### Why there is no third (closed-form) approach

Kata #62 had a third solver — the closed-form binomial `C(m+n-2, m-1)` — that dropped the DP entirely. **That option is gone here, and its absence is the point.** With arbitrary obstacles there is no product formula for the count: which routes survive depends on *where* the obstacles sit, not just how many steps there are. This is exactly what #62's own closing note predicted — "add obstacles (#63) and there is no closed form — the recurrence becomes mandatory." So #63 is the kata that justifies why #62's ★ was the DP and not the one-line binomial: the DP is the form that *scales* to this variant, and the binomial is the form that does not.

## Kāra features exercised

- **`Vec[i64]` rolling buffer** — `Vec.new()` + `push` to seed the columns, then in-place `dp[c] = dp[c] + dp[c - 1]` read-modify-write indexing, with an `dp[c] = 0` obstacle override. The same rolling-DP shape as kata [#62](../62-unique-paths/) and the `Vec[bool]` reachability table of kata [#55](../55-jump-game/).
- **`ref Vec[Vec[i64]]` grid parameter + double-index reads** — the solver borrows the obstacle grid (`grid: ref Vec[Vec[i64]]`) and reads it with `grid[i][c]`, the 2-D borrow-and-index idiom shared with katas [#54](../54-spiral-matrix/) and [#48](../48-rotate-image/); the 2-D solver additionally *builds* a `Vec[Vec[i64]]` with nested `Vec.new()`/`push`.
- **Nested array literals as test input** — `report([[0, 0, 0], [0, 1, 0], [0, 0, 0]], mut s)` constructs the `Vec[Vec[i64]]` obstacle grids inline, the same literal-grid harness shape as kata [#54](../54-spiral-matrix/).
- **Obstacle guard threaded through the recurrence** — `if grid[i][c] == 1 { dp[c] = 0 } else if c > 0 { dp[c] += dp[c-1] }` is the whole delta from #62; the border-`0` propagation falls out of it with no special-casing.
- **Shared `report`/`sums:` harness** — one answer per line plus a folded `sums:` checksum, the byte-for-byte diff anchor used across katas [#53](../53-maximum-subarray/), [#54](../54-spiral-matrix/), and [#62](../62-unique-paths/); both solvers and the Python mirror print it identically.

**v1 note.** LeetCode guarantees the answer `≤ 2·10⁹` (it fits i32); the arithmetic is i64 for uniformity with the rest of the corpus. Every `dp[c]`/`paths[i][j]` is a partial path count and so is itself `≤` the final answer, so no intermediate overflows. Obstacle cells short-circuit to `0` before any addition, so a blocked start or a fully walled row collapses the whole count to `0` without special-case branches.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   unique_paths_ii.kara
karac build unique_paths_ii.kara && ./unique_paths_ii

# The full 2-D approach (identical output):
karac run unique_paths_ii_2d.kara

# Python
python3 unique_paths_ii.py

# Verify they all agree
diff <(karac run unique_paths_ii.kara) <(python3 unique_paths_ii.py)         && echo OK
diff <(karac run unique_paths_ii.kara) <(karac run unique_paths_ii_2d.kara)  && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`unique_paths_ii.{kara,rs,c,py}`, `go-seq/main.go`).

> ⚠️ **Machine caveat — read before comparing.** Unlike the rest of the corpus (whose tables are **Apple M5 Pro** snapshots), the numbers below were measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.10 GHz, 4 vCPU, Linux 6.18.5), the environment this kata was authored in. So:
> - **Do NOT compare these absolute times/sizes/RSS against sibling katas' M5 tables** — different ISA (x86-64 vs ARM64), different toolchains (clang 18 / rustc 1.94 / go 1.24 vs the M5's clang 21 / rustc 1.95 / go 1.26), and a noisier shared host. `bench/results.json` records the real host in `env.host`/`env.note` so the consolidated feed can keep them apart.
> - **What IS load-bearing is the within-kata cross-language ratio** — every mirror here ran on the *same* box back-to-back, so kāra-vs-C-vs-Rust-vs-Go is an honest per-core codegen comparison. That ratio, not the millisecond count, is the result.
> - Re-run `bench/bench.sh` on the M5 reference machine to fold M5 numbers into the corpus tables (the harness auto-detects and tags the host).

**Workload.** K = 1,000,000 iterations of the rolling obstacle-DP ★. Each iteration sweeps the grid shape — `m = 2 + k%32`, `n = 2 + (k/32)%32`, both in `[2, 33]` — and threads `k` through an inline obstacle predicate `((i*7 + c*3 + k) % 13) == 0` (~31 % of cells), so both the shape *and* the obstacle pattern change every iteration (nothing to hoist). Using a predicate rather than a materialised `Vec[Vec[i64]]` grid is deliberate: it keeps the one `Vec[i64]` dp buffer the only per-call allocation, so the measured body is the **obstacle-guarded RMW scan itself** — exactly what #63 adds over #62 — rather than grid-allocation traffic (the alloc-domination pitfall BENCHMARKS.md warns against). Every count stays inside i64 (ceiling is the unobstructed 33×33 count `C(64,32) ≈ 1.8·10¹⁸`). The sink is a rolling polynomial hash `acc = (acc*131 + ans) % 1_000_000_007`, the same order-sensitive checksum kata [#55](../55-jump-game/) and [#62](../62-unique-paths/) use. All four compiled mirrors must agree on `583461340` before timing.

**Seq-only kata** (BENCHMARKS.md two-lane discipline): the hash sink is a **loop-carried dependency**, so the K-loop is not a reduction karac's auto-par pass can split — the default `karac build` stays single-threaded (CPU ≈ 99 %). The kāra row is therefore directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core codegen-quality basis.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All four single-threaded. **Cloud-container numbers — ratios, not absolutes** (see caveat above).

| Implementation | Wall time |
|---|---|
| c    unique_paths_ii (clang -O3)   | 310.5 ± 9.5 ms |
| **kāra unique_paths_ii**           | **323.7 ± 4.4 ms** |
| rust unique_paths_ii (rustc -O)    | 341.1 ± 6.2 ms |
| go   unique_paths_ii               | 448.1 ± 7.7 ms |

**Kāra sits dead even with C and a hair ahead of Rust** on this obstacle-guarded RMW scan — **1.04× C** (≈4 % behind), **0.95× Rust** (≈5 % *ahead*), and ~1.44× ahead of Go. That is the whole point of the entry: the per-cell obstacle branch #63 adds over #62 costs kāra **essentially nothing**, so the C/Rust parity #62 fought to reach (its `bce_length_pin` codegen fix, ledger `B-2026-07-04-6`) carries straight over to the obstacle variant. The bounds checks on `dp[c] += dp[c-1]` are still elided — the extra obstacle guard folds into the scan without reintroducing the per-cell checks. (Container variance is real — note C's ±9.5 ms spread; the kāra/C/Rust cluster is within noise of each other, which is itself the finding: no measurable obstacle-branch penalty.)

> **⚠️ M5 re-bench (2026-07-08) — the container parity above is stale; see ledger `B-2026-07-08-3` (FIXED) + `B-2026-07-08-7` (open).** On the corpus's Apple M5 Pro reference machine (arm64, clang 21 / rustc 1.95) the container's `0.95× Rust` did **not** hold: kāra started **1.36× behind on instructions** (5.75B vs 4.24B/4.21B), root-caused to a codegen strength-reduction miss — kāra rebuilt the obstacle-predicate dividend `i*7+c*3+k` with overflow checks every cell instead of letting LLVM carry it as one induction variable. **That miss is now fixed** (`B-2026-07-08-3`, karac commit `ac06b64b`: monotone non-negativity `llvm.assume`s are now emitted for every loop counter, not just array-index ones). The obstacle-predicate inner loop now matches `rustc -O -C overflow-checks=on` exactly (one plain `add nuw nsw` + `urem`); instructions **5.75B → 5.19B**, wall **190.4 → 178.8 ms** (**1.11× Rust**, from 1.18×), and σ collapsed 10.9 → 1.1 ms. The residual 1.11× is a **separate** Vec-fill/alloc idiom gap (the kata's `Vec.new()` + push-loop vs Rust's `vec![0; n]` single `alloc_zeroed`), tracked as `B-2026-07-08-7`. The table above is the stale x86 container snapshot pending a full M5 rewrite.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py unique_paths_ii` (K=100k) | 2965 ± 113 ms |

Python at K=100k is ~2.97 s; projecting to the compiled mirrors' K=1M (~29.6 s) puts it **~91× slower than kāra seq** — an even wider Python gap than #62's ~16.7×, because this workload is dominated by the DP's integer additions *plus* the per-cell `% 13` obstacle test, both of which CPython runs bytecode-by-bytecode.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 unique_paths_ii.c          | **79.5 ± 1.6 ms** |
| rustc -O unique_paths_ii.rs          | 119.3 ± 1.9 ms |
| **karac build unique_paths_ii.kara** | **183.0 ± 5.6 ms** |

On this container karac compiles at ~2.30× clang and ~1.53× rustc — slower than both, the reverse of #62's M5 snapshot (where karac edged rustc). Small-single-file compile time is dominated by process/LLVM-init overhead that differs sharply across the two toolchain sets; this is exactly the kind of number the machine caveat says not to read across katas.

### Binary size

| Implementation | Size |
|---|---|
| c    unique_paths_ii                | 15.7 KiB |
| **kāra unique_paths_ii**            | **324.5 KiB** |
| go   unique_paths_ii                | 2.11 MiB |
| rust unique_paths_ii                | 3.77 MiB |

Kāra's seq binary is **far below Rust's 3.8 MiB and Go's 2.1 MiB**, above C's 15.7 KiB. The 324.5 KiB is a property of this toolchain's link, **not** a #63 regression: kata #62's bench binary rebuilt on the *same* container is byte-for-byte the same 332,320 bytes, and the M5 build strips it much further (#62's M5 table shows 33.4 KiB). So the honest same-machine read is "kāra ≈ #62, orders of magnitude below the Rust/Go runtimes."

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| rust unique_paths_ii                | 5.56 MiB |
| c    unique_paths_ii                | 5.56 MiB |
| **kāra unique_paths_ii**            | **5.62 MiB** |
| go   unique_paths_ii                | 7.25 MiB |

Kāra's peak RSS is **within 1 % of C and Rust** (the per-call dp buffer is allocated and freed inside the loop, so steady state stays flat across all 1,000,000 iterations); Go's 7.25 MiB carries its GC arena + scheduler. (Absolute RSS runs higher here than the M5 tables' ~1.2 MiB — page size and dynamic-linking differences — but the kāra/C/Rust tie is the machine-independent signal.)

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build unique_paths_ii.kara** | **83.9 MiB** |
| clang -O3 unique_paths_ii.c          | 96.6 MiB |
| rustc -O unique_paths_ii.rs          | 110.4 MiB |

On this container karac has the **lowest** compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. This kata is the obstacle sibling of [#62](../62-unique-paths/): #62 established that kāra reaches C/Rust parity on the rolling-DP RMW scan (after a codegen fix); #63 confirms that adding the per-cell obstacle branch **keeps** that parity — kāra stays in the C/Rust cluster (within ±5 %), the obstacle guard folding into the scan for free. The within-kata cross-language ratio is the load-bearing number; the absolute container times are not (see the machine caveat).
