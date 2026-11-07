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

**Seq-only kata** (BENCH.md two-lane discipline): the hash sink is a **loop-carried dependency** (each `acc` needs the previous one), so the K-loop is not a reduction karac's auto-par pass can split — verified in the emitted IR (`KARAC_MIR_LL`): the default build carries no call of `karac_mir_task_spawn`, and the default `karac build` stays single-threaded (99.7% CPU). The kāra row is therefore directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core codegen-quality basis.

### Runtime — seq lane

M5 Pro, karac g6697158fa (v2/MIR backend), 2026-10-31 (`measured_at` 2026-11-01T02:25Z UTC), hyperfine `--warmup 5 --runs 30 --shell=none`. All single-threaded (kāra CPU 99.7%).

| Implementation | Wall time | User | vs kāra |
|---|---|---|---|
| c    unique_paths (clang -O3)       | 116.1 ± 3.2 ms | 114.6 ms | kāra 2.30× behind |
| rust unique_paths (rustc -O)        | 117.3 ± 3.6 ms | 115.8 ms | kāra 2.27× behind |
| rust unique_paths (`-C overflow-checks=on`) | 227.9 ± 3.5 ms | 225.8 ms | kāra 1.17× behind |
| go   unique_paths                   | 247.8 ± 1.9 ms | 245.5 ms | kāra 1.08× behind |
| **kāra unique_paths**               | **266.6 ± 2.8 ms** | **264.0 ms** | — |

**Kāra trails C and Rust ~2.3×** on this tight read-modify-write array scan, and Go by 1.08×; against Rust at equal safety (`-C overflow-checks=on`) the gap is 1.17×. Against the previous feed (2026-07-28, legacy backend) that is an improvement in every ratio: Kāra/Rust **3.11× → 2.27×**, Kāra/C 3.12× → 2.30×, Kāra/Go 1.48× → 1.08×. The v2/MIR build also beats the last legacy build on this kata directly — 0.93× its instructions and 0.72× its cycles. A *possible* cause of the remaining gap, **not verified for this kata**: the kernel `dp[c] = dp[c] + dp[c - 1]` reads back the value the previous iteration just stored, the loop shape of [`B-2026-10-31-38`](../../../../kara/docs/bugs-v2.md) (MIR reloads that value from memory where legacy kept it in a register; measured on sibling kata [#64](../64-minimum-path-sum/)).

Note (2026-11-07, karac g97681763d, seq lane re-benched with `KARAC_AUTO_PAR=0`): Kāra now reads 1.05× C and `rustc -O`, 0.53× equal-safety Rust and 0.49× Go, so the gaps above are history.

> **Note (2026-10-31):** the C/Rust parity described in the next paragraphs was measured on 2026-07-04 and did not survive into the 2026-07-28 feed (Kāra/Rust 3.11× there), nor today's (2.27×). The paragraphs below are kept as the history of the original gap and its fix.

The kata was written as the corpus's honest counter-case: kāra trailed C/Rust by **~3.10×** here (316 ms vs 102 ms), the widest per-core gap in the neighbourhood — and the gap it exposed drove a karac codegen fix (`src/codegen/bce_length_pin.rs`, commit `b5d18320`, ledger `B-2026-07-04-6`) that closed it. It is the counterpart to sibling kata [#61](../61-rotate-list/), where kāra *led* Rust by 1.36× on a linked-list workload: found a gap, fixed the compiler, kept the natural code.

**What the gap was.** The natural rolling-DP scan `dp[c] = dp[c] + dp[c-1]` compiled to **three bounds-checked array accesses per cell** (read `dp[c]`, read `dp[c-1]`, write `dp[c]`), and those checks blocked LLVM from forwarding the just-written `dp[c-1]` into a register. Rebuilding the kāra mirror one change at a time isolates the cause:

| kāra variant (pre-fix diagnostic) | Wall time | isolates |
|---|---|---|
| natural kata (`dp[c] = dp[c] + dp[c-1]`, `Vec.new()` per call) | ~316 ms | the gap |
| **no-op every per-cell bounds check** (allocation untouched) | **~105 ms** | **bounds checks ≈ 210 ms — the *entire* gap** |
| also hoist the alloc + hand-carry `dp[c-1]` in a scalar | ~80 ms | (removes the reads outright too) |

The load-bearing row is the middle one: with the per-cell checks off but the per-call `Vec.new()` **kept**, the identical DP already runs at C's ~105 ms. So the whole ~210 ms was the bounds checks — once they clear, LLVM performs the `dp[c-1]` store-to-load forwarding *itself* and the per-call allocation stops mattering (it optimises the fill loop too). An earlier "≈96 ms allocation + ≈140 ms RMW" split was a red herring from hoisting the alloc and the scalar-carry together; one mechanism accounts for all of it.

**How it closed.** The fix teaches the compiler to prove `c < dp.len()` for the *natural* guard `while c < cols`, where `cols` is not spelled `dp.len()` but equals it — `dp` is filled to exactly `cols` elements by the counted `while j < cols` loop and never resized. A fail-closed whole-function analysis pins `cols == dp.len()`, and the existing split-check elision then drops the upper-half checks on `dp[c]` and `dp[c-1]` (`i ± k` indices included); the residual `< 0` checks fold against the loop's monotone `assume(c >= 1)`. The kata keeps its natural `dp[c] = dp[c] + dp[c-1]` form throughout — the recurrence is how the algorithm is taught, and per the corpus discipline the compiler was fixed rather than the kata hand-carried around it. Kata [#53](../53-maximum-subarray/)'s Kadane (a scalar-accumulator scan with one bounds-checked read per cell) was already at C parity (154.4 ms vs 155.0 ms) and never had the gap, confirming it was specific to the RMW multi-access idiom — now closed.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py unique_paths` (K=100k) — last measured 2026-07-04, not re-run | 527.2 ± 2.3 ms |

The Python row was not re-run in the 2026-10-31 pass (no `KARAC_BENCH_INCLUDE_PY`). As of 2026-07-04, Python at K=100k was 527 ms; projecting to the compiled mirrors' K=1M (~5.27 s) put it **~16.7× slower than that session's kāra seq** — a much wider Python gap than the linked-list kata [#61](../61-rotate-list/)'s ~5.4×, because this workload is dominated by the DP's integer additions, which CPython runs bytecode-by-bytecode, rather than by allocation and pointer-chasing (which CPython does in C).

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 unique_paths.c           | **46.7 ± 0.8 ms** |
| rustc -O unique_paths.rs           | 89.1 ± 1.0 ms |
| **karac build unique_paths.kara**  | **118.2 ± 5.5 ms** |

Kāra compiles at **2.53× clang -O3** and **1.33× `rustc -O`** (118.2 vs 89.1 ms) on this small single-file program.

### Binary size

| Implementation | Size |
|---|---|
| c    unique_paths                   | 32.8 KiB |
| **kāra unique_paths**               | **295.8 KiB** |
| rust unique_paths                   | 455.4 KiB |
| go   unique_paths                   | 2434.1 KiB |

Kāra's seq binary is **295.8 KiB** (302,880 B) — ~9× C's 32.8 KiB, and below Rust's 455 KiB. Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (this kata's was 34,320 B); that floor is tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra unique_paths**               | **1.08 MiB** |
| c    unique_paths                   | 1.22 MiB |
| rust unique_paths                   | 1.23 MiB |
| go   unique_paths                   | 9.27 MiB |

Kāra's peak RSS (1,130,832 B) is the **lowest of the four**, below C (1,278,264 B) and Rust (1,294,648 B). The per-call DP buffer is allocated and freed inside the loop, so steady state stays flat across all 1,000,000 iterations with no growth. Go's 9.27 MiB carries its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 unique_paths.c          | 2.5 MiB |
| rustc -O unique_paths.rs          | 28.3 MiB |
| **karac build unique_paths.kara** | **57.4 MiB** |

Kāra's compile-memory footprint is ~22.7× clang's and ~2.0× rustc's on this kata.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this array-scan DP **Kāra currently trails Rust 2.27×** (2026-10-31, v2/MIR; 3.11× in the 2026-07-28 legacy feed), and that is why the kata earns its place. It matched Rust once (2026-07-04): it first trailed Rust by **~3.10×** here, the isolation above pinned the cause to one optimiser gap (per-cell bounds checks on the RMW scan, *not* the backend — the same DP with checks off already runs at C's speed), and closing it was a compiler fix, not a kata rewrite. It is the complement to kata #61's headline win: there kāra *led* Rust because Rust paid `Rc<RefCell>`; here kāra reached parity by teaching its own backend to elide the checks Rust and C already dropped. On the idiom kāra optimises well (scalar-carried scans, kata #53) it always matched C; the RMW array scan is the one it had to *learn*, learned on 2026-07-04, and has since lost again (2.27× behind Rust today). All of these numbers are load-bearing.
