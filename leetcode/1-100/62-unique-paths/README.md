# 62. Unique Paths

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math · Dynamic Programming · Combinatorics &nbsp;·&nbsp; **Source:** [leetcode.com/problems/unique-paths](https://leetcode.com/problems/unique-paths/)

A robot starts at the top-left of an `m × n` grid and may move only **right** or **down**. How many distinct paths reach the bottom-right corner?

```
m = 3, n = 7   →   28
m = 3, n = 2   →   3     (down-down-right, down-right-down, right-down-down)
```

**Constraints:** `1 ≤ m, n ≤ 100`; the answer is guaranteed to be `≤ 2·10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Rolling 1-D DP** ★ — one array spanning the smaller axis, `dp[c] += dp[c-1]` down the rows | O(m·n) time, O(min(m,n)) space | [`unique_paths.kara`](unique_paths.kara) ✓ via `karac run` / `karac build` | [`unique_paths.py`](unique_paths.py) ✓ |
| **Full 2-D DP table** — materialise every cell, `grid[i][j] = grid[i-1][j] + grid[i][j-1]` | O(m·n) time, O(m·n) space | [`unique_paths_2d.kara`](unique_paths_2d.kara) ✓ | — |
| **Closed-form binomial** — `C(m+n-2, m-1)`, built up multiplicatively | O(min(m,n)) time, O(1) space | [`unique_paths_math.kara`](unique_paths_math.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## The recurrence, and rolling it onto one row

Every cell has exactly two in-neighbours — the robot can only arrive from **above** or from the **left** — so the number of paths to a cell is the sum of the paths to those two:

```
paths[i][j] = paths[i-1][j] + paths[i][j-1]
```

with `paths = 1` along the top row and left column (a single straight run of rights, or of downs, reaches them). This is the same move kata [#53](../53-maximum-subarray/)'s Kadane and kata [#55](../55-jump-game/)'s reachability sweep make: a 2-D relation collapsed to a one-step recurrence you can fill in a fixed scan order.

**Rolling 1-D DP** ([`unique_paths.kara`](unique_paths.kara)) is the ★. The recurrence only ever reads the row directly above, so a **single array** suffices if it is updated in place, left to right:

```
dp[j]  currently holds  paths[i-1][j]   (the row above)
dp[j] += dp[j-1]        ->  paths[i-1][j] + paths[i][j-1] = paths[i][j]
```

At the instant `dp[j]` is read on the right it still holds the value from the row above (not yet overwritten this pass), while `dp[j-1]` was already advanced to the current row — exactly the two neighbours the recurrence wants. `dp[0]` is never touched after initialisation (the left column is always 1). This read-before-overwrite in a left-to-right sweep is the same discipline the linked-list katas turn on, here over an array index instead of a `next` field. Rows and columns are symmetric (`paths(m,n) == paths(n,m)`), so the array is sized to the smaller dimension — **O(min(m,n)) space**.

**Full 2-D table** ([`unique_paths_2d.kara`](unique_paths_2d.kara)) is the textbook form: keep the whole `Vec[Vec[i64]]` grid (same 2-D shape as kata [#54](../54-spiral-matrix/) and kata [#48](../48-rotate-image/)). It has **no aliasing subtlety at all** — every cell is written once, and the two cells it reads (`grid[i-1][j]` in the finished previous row, `grid[i][j-1]` earlier in this row) are final before it is reached. Its cost is the O(m·n) grid the rolling form trades away; keeping it here shows the space optimisation as a diff and cross-checks the recurrence independently.

**Closed-form binomial** ([`unique_paths_math.kara`](unique_paths_math.kara)) drops the DP entirely. Every path is a sequence of exactly `(m-1)` downs and `(n-1)` rights in some order, and *any* such sequence is a valid path — so counting paths is choosing which of the `(m-1)+(n-1)` steps are the downs:

```
C(m + n - 2, m - 1) = C(m + n - 2, n - 1)
```

Computed multiplicatively with the smaller index `k = min(m-1, n-1)`: `result = result * (total - k + i) / i` for `i` in `1..=k`, where `total = m+n-2`. After step `i`, `result` equals `C(total-k+i, i)` — always an integer, so every division is exact — and the partial results climb monotonically to the answer, so each stays `≤ 2·10⁹` and the largest transient (`result * (total-k+i)` before a divide) stays comfortably inside i64. O(1) space and the fewest operations, but it does **not** generalise: add obstacles (#63) or per-cell costs (#64) and there is no closed form — the recurrence becomes mandatory. That is why the DP is the ★ and the binomial is the "you didn't need the table" counterpoint.

## Kāra features exercised

- **`Vec[i64]` rolling buffer** — `Vec.new()` + `push` to seed the top row, then in-place `dp[c] = dp[c] + dp[c - 1]` read-modify-write indexing, sized to `min(m, n)`. The same `Vec[bool]` reachability-table shape as kata [#55](../55-jump-game/)'s DP solver.
- **`Vec[Vec[i64]]` grid** (2-D approach) — nested `Vec.new()`/`push` row construction and double-index reads `grid[i - 1][j]`, the 2-D idiom shared with katas [#54](../54-spiral-matrix/) and [#48](../48-rotate-image/).
- **Axis-swap for the smaller dimension** — `if cols > rows { let t = rows; rows = cols; cols = t; }` realises the `paths(m,n) == paths(n,m)` symmetry so the buffer spans `min(m,n)`.
- **Exact integer binomial** (math approach) — `result * (total - k + i) / i` relies on the multiply-then-divide order and the invariant that each partial product is itself a binomial coefficient, so integer `/` is always exact — no floats, no factorials, no overflow.
- **Shared `report`/`sums:` harness** — one answer per line plus a folded `sums:` checksum, the byte-for-byte diff anchor used across katas [#53](../53-maximum-subarray/) and [#54](../54-spiral-matrix/); all three solvers and the Python mirror print it identically.

**v1 note.** LeetCode guarantees the answer `≤ 2·10⁹` (it fits i32); the arithmetic is i64 for uniformity with the rest of the corpus. In the DP, every `dp[j]`/`grid[i][j]` is a partial path count `≤` the final answer, so no intermediate overflows; in the binomial, the partials are bounded by the answer and the largest transient by `answer · (m+n-2) ≤ 2·10⁹ · 198`, well inside i64.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   unique_paths.kara
karac build unique_paths.kara && ./unique_paths

# The alternative approaches (identical output):
karac run unique_paths_2d.kara
karac run unique_paths_math.kara

# Python
python3 unique_paths.py

# Verify they all agree
diff <(karac run unique_paths.kara) <(python3 unique_paths.py)          && echo OK
diff <(karac run unique_paths.kara) <(karac run unique_paths_2d.kara)   && echo OK
diff <(karac run unique_paths.kara) <(karac run unique_paths_math.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`unique_paths.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** K = 1,000,000 iterations of the rolling-DP ★. Each iteration sweeps the grid shape — `m = 2 + k%32`, `n = 2 + (k/32)%32`, both in `[2, 33]` — so the DP genuinely re-runs on a different table every iteration (no hoisting a constant answer) while every count stays inside i64: the largest case, 33×33, is `C(64,32) ≈ 1.8·10¹⁸`. The sink is a rolling polynomial hash `acc = (acc*131 + ans) % 1_000_000_007`, the same order-sensitive checksum kata [#55](../55-jump-game/) uses; the `% modulus` keeps it bounded no matter how large the counts get. All four compiled mirrors must agree on `583774682` before timing.

**Seq-only kata** (BENCH.md two-lane discipline): the hash sink is a **loop-carried dependency** (each `acc` needs the previous one), so the K-loop is not a reduction karac's auto-par pass can split — `nm -gU` on the binary shows no `karac_par_reduce`, and the default `karac build` stays single-threaded (99% CPU). The kāra row is therefore directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core codegen-quality basis.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-07-04, hyperfine `--warmup 5 --runs 30 --shell=none`. All four single-threaded (kāra CPU 99%).

| Implementation | Wall time |
|---|---|
| c    unique_paths (clang -O3)       | 102.2 ± 0.6 ms |
| rust unique_paths (rustc -O)        | 102.2 ± 0.8 ms |
| go   unique_paths                   | 221.5 ± 0.6 ms |
| **kāra unique_paths**               | **316.4 ± 4.9 ms** |

This is the corpus's honest counter-case: **Kāra trails C/Rust by ~3.10× and Go by ~1.43×** on a tight read-modify-write array scan — the widest per-core gap in the neighbourhood, and the opposite of its sibling linked-list kata [#61](../61-rotate-list/) (where Kāra *led* Rust by 1.36× because Rust paid `Rc<RefCell>` overhead). The gap is two specific optimiser headrooms on the *natural* rolling-DP idiom, both isolated by rebuilding the kāra mirror with one change at a time:

| kāra variant | Wall time | isolates |
|---|---|---|
| natural kata (`dp[c] = dp[c] + dp[c-1]`, `Vec.new()` per call) | ~316 ms | — |
| hoist the per-call `Vec` allocation (reuse one buffer) | ~220 ms | **allocation ≈ 96 ms** |
| also carry `dp[c-1]` in a scalar (1 read + 1 write / cell) | **~80 ms** | **RMW bounds-checked triple-access ≈ 140 ms** |

1. **Per-call `Vec` allocation (~30%).** One million `Vec[i64]` allocate/fill/drop cycles. C's `malloc`/`free` and Rust's `Vec` amortise this better; Kāra's per-call RC/allocator traffic is heavier.
2. **The RMW inner scan (~44%).** `dp[c] = dp[c] + dp[c-1]` compiles to **three bounds-checked array accesses per cell** (read `dp[c]`, read `dp[c-1]`, write `dp[c]`). `clang -O3` and `rustc -O` forward the just-written `dp[c-1]` into a register — turning it into a scalar running value — and drop the bounds checks entirely; Kāra does neither yet.

The load-bearing evidence is the last row: with the allocation hoisted **and** `dp[c-1]` carried in a scalar, the *identical* DP runs **~80 ms — faster than clang's 102 ms**. So Kāra's backend is competitive on the arithmetic itself; the 3.1× is optimiser headroom on one array idiom, not a fundamental codegen deficit. Kata [#53](../53-maximum-subarray/)'s Kadane corroborates this: a scalar-accumulator scan with a single bounds-checked read per element already sits at **dead parity with C** (154.4 ms vs 155.0 ms). The natural rolling-DP is kept as-written here — the recurrence `dp[c] = dp[c] + dp[c-1]` is how the algorithm is taught, and hand-carrying a scalar would obscure it — so the honest 3.1× stands, with the cause pinpointed. Closing it is a karac codegen opportunity (bounds-check elision + redundant-load forwarding on monotonic-index array scans), tracked as follow-up, not routed around in the kata.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py unique_paths` (K=100k) | 527.2 ± 2.3 ms |

Python at K=100k is 527 ms; projecting to the compiled mirrors' K=1M (~5.27 s) puts it **~16.7× slower than kāra seq** — a much wider Python gap than the linked-list kata [#61](../61-rotate-list/)'s ~5.4×, because this workload is dominated by the DP's integer additions, which CPython runs bytecode-by-bytecode, rather than by allocation and pointer-chasing (which CPython does in C).

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 unique_paths.c           | **37.8 ± 1.5 ms** |
| **karac build unique_paths.kara**  | **74.4 ± 0.5 ms** |
| rustc -O unique_paths.rs           | 77.2 ± 0.8 ms |

Kāra compiles at **1.97× clang -O3** and is a hair **ahead of `rustc -O`** (74.4 vs 77.2 ms) on this small single-file program.

### Binary size

| Implementation | Size |
|---|---|
| c    unique_paths                   | 32.8 KiB |
| **kāra unique_paths**               | **33.4 KiB** |
| rust unique_paths                   | 455.4 KiB |
| go   unique_paths                   | 2434.1 KiB |

Kāra's seq binary is **33.4 KiB — essentially identical to C's 32.8 KiB**, and far below Rust's 455 KiB. This kata calls no `sort_by` and triggers no auto-par dispatch, so it never links the runtime's libstd floor (panic infrastructure + DWARF symbolizer) that dominates the sort-using katas — see [kata 16 § Binary size](../16-3sum-closest/README.md).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra unique_paths**               | **1.2 MiB** |
| c    unique_paths                   | 1.2 MiB |
| rust unique_paths                   | 1.2 MiB |
| go   unique_paths                   | 9.1 MiB |

Kāra's peak RSS (1,278,264 B) is **identical to C's** (1,278,264 B) and a hair under Rust (1,294,648 B). The per-call DP buffer is allocated and freed inside the loop, so steady state stays flat across all 1,000,000 iterations with no growth. Go's 9.1 MiB carries its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 unique_paths.c          | 2.5 MiB |
| **karac build unique_paths.kara** | **18.8 MiB** |
| rustc -O unique_paths.rs          | 28.3 MiB |

Kāra's compile-memory footprint is ~7.4× clang's and ~1.5× lower than rustc's on this kata.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this array-scan DP **Kāra trails Rust by ~3.10×** — and the isolation table above pins the cause to two optimiser gaps (per-call allocation + bounds-check/redundant-load on the RMW scan), *not* the backend, since the same DP with those two idioms hand-lifted beats clang. It is the honest complement to kata #61's headline win: on the idiom Kāra optimises well (scalar-carried scans, kata #53) it matches C; on the one it does not yet (RMW array scans) it pays 3×. Both numbers are load-bearing.
