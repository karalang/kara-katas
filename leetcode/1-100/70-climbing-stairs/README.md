# 70. Climbing Stairs

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · Dynamic Programming · Memoization &nbsp;·&nbsp; **Source:** [leetcode.com/problems/climbing-stairs](https://leetcode.com/problems/climbing-stairs/)

You climb a staircase of `n` steps, taking **1 or 2** steps at a time. How many distinct ways reach the top?

```
n = 2  →  2      (1+1),  (2)
n = 3  →  3      (1+1+1),  (1+2),  (2+1)
n = 5  →  8
```

**Constraints:** `1 ≤ n ≤ 45`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Two rolling counters** ★ — carry `ways(i-1)`, `ways(i-2)`, roll forward | O(n) time, O(1) space | [`climbing_stairs.kara`](climbing_stairs.kara) ✓ via `karac run` / `karac build` | [`climbing_stairs.py`](climbing_stairs.py) ✓ |
| **Full DP table** — materialise every `ways(i)` in a `Vec[i64]` | O(n) time, O(n) space | [`climbing_stairs_dp.kara`](climbing_stairs_dp.kara) ✓ | — |
| **Matrix exponentiation** — `Mⁿ` by repeated squaring, `(Mⁿ)[0][0] = ways(n)` | O(log n) time, O(1) space | [`climbing_stairs_matrix.kara`](climbing_stairs_matrix.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all eleven test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## It's Fibonacci

The last move onto step `n` is either a single step (from `n-1`) or a double step (from `n-2`), and those two families of paths are disjoint — so

```
ways(n) = ways(n-1) + ways(n-2),   ways(1) = 1,  ways(2) = 2
```

which is the Fibonacci recurrence (`ways(n) = fib(n+1)`). It is the same "sum the two ways in" move the grid katas [#62](../62-unique-paths/)–[#63](../63-unique-paths-ii/) make, collapsed to a single dimension.

**Two rolling counters** ([`climbing_stairs.kara`](climbing_stairs.kara)) is the ★. The recurrence only ever looks back two terms, so no array is needed — hold `ways(i-1)` and `ways(i-2)` in a pair of scalars and roll them forward each step. O(1) space, the scalar-accumulator analogue of the grid DP's rolling row (kata [#53](../53-maximum-subarray/)'s Kadane is the same shape).

**Full DP table** ([`climbing_stairs_dp.kara`](climbing_stairs_dp.kara)) keeps every `ways(i)` in a `Vec[i64]` — the textbook 1-D DP, identical to kata [#62](../62-unique-paths/)'s rolling row before it is collapsed to a scalar pair. It carries no information the two scalars don't (each `dp[i]` is dead once `dp[i+2]` is computed), so it is here as the space optimisation shown as a diff.

**Matrix exponentiation** ([`climbing_stairs_matrix.kara`](climbing_stairs_matrix.kara)) is the outlier: it reaches the answer in **O(log n)**. One Fibonacci step is the linear map `M = [[1,1],[1,0]]`, so `(Mⁿ)[0][0] = fib(n+1) = ways(n)`, and `Mⁿ` is computed by exponentiation-by-squaring — square the base each step, fold it into the result on every set bit of `n`. It is the same fast-power as kata [#50](../50-powx-n/)'s `pow`, lifted from scalars to 2×2 matrices (carried as four scalars, no `Vec`). For `n ≤ 45` it is overkill, but it is a genuinely different algorithm that must still land on the same counts — the strongest cross-check of the three.

## Kāra features exercised

- **Scalar rolling recurrence** — the ★'s `next = a + b; a = b; b = next`, an O(1) two-variable state machine, plus the `n <= 2` base-case `return`; the same scalar-accumulator idiom as kata [#53](../53-maximum-subarray/).
- **`Vec[i64]` DP table** — `Vec.new()` + `push` to size the array, then `dp[j] = dp[j-1] + dp[j-2]` read-modify indexing, the 1-D DP shape shared with katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/).
- **2×2 matrix fast-power in scalars** — the matrix solver carries `[[a,b],[c,d]]` as four i64 locals and walks the exponent with `p % 2` (low bit) and `p / 2` (shift); exponentiation-by-squaring over matrices, the same halving loop as kata [#50](../50-powx-n/).
- **Shared `report`/`sums:` harness** — one `climb(n) = ways` per line plus the folded `sums:` checksum, the byte-for-byte diff anchor shared with the numeric katas [#50](../50-powx-n/) and [#69](../69-sqrtx/); all three solvers and the Python mirror print it identically.

**v1 note.** LeetCode caps `n` at 45, so `ways(45) = 1_836_311_903` fits i64 with enormous room (it fits i32). The matrix solver's largest intermediate is about `M⁶⁴`, whose entries are `fib(65) ≈ 1.7·10¹³`, and its biggest product stays far under i64::MAX — so Kāra's default overflow checks never trip on any of the three approaches. All arithmetic is i64 for corpus uniformity.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   climbing_stairs.kara
karac build climbing_stairs.kara && ./climbing_stairs

# The alternative approaches (identical output):
karac run climbing_stairs_dp.kara
karac run climbing_stairs_matrix.kara

# Python
python3 climbing_stairs.py

# Verify they all agree
diff <(karac run climbing_stairs.kara) <(python3 climbing_stairs.py)              && echo OK
diff <(karac run climbing_stairs.kara) <(karac run climbing_stairs_dp.kara)       && echo OK
diff <(karac run climbing_stairs.kara) <(karac run climbing_stairs_matrix.kara)   && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`climbing_stairs.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-08); the unroll gap is now FIXED (`B-2026-07-08-24`).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, clang 21 / rustc 1.95 / go 1.26). The equal-safety row pinpointed the gap as **loop unrolling**: `rustc` runtime-unrolls the two-counter fib loop 4×, and kāra's stock `default<O2>` pipeline did not. karac now emits `!llvm.loop.unroll.count` on pure-scalar counted loops (the Fibonacci shape) — see the ledger entry. Effect: kāra dropped from 210.3 ms to **136.3 ms (1.54× faster)**, which now **beats all three wrapping native builds** (rust `-O` 171.3, clang -O3 172.4, go 188.4 ms) and closes the equal-safety gap to **1.23× behind checked Rust** (`-C overflow-checks=on`, 111.1 ms) — down from 1.89×. The gate is scalar-recurrence-only, so it carries **zero binary-size cost and no regression** on memory-bound katas (an earlier blunt global unroll was rejected for exactly that; the ledger has the full story).

**Workload.** A single `climb(n)` is O(n) with `n ≤ 45` — cheap — so the bench runs the rolling-counter ★ **K = 30,000,000** times over a sweep of `n = 1 + k%45` (every step count in `[1, 45]`), folding each result into a rolling hash `acc = (acc*131 + climb(n)) % 1_000_000_007`. Sweeping `n` re-runs the recurrence to a different depth each iteration (nothing hoistable), and the loop-carried sink keeps it seq. No allocation — the whole body is the two-counter integer-add loop. All four compiled mirrors must agree on `522887212` before timing.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **M5 Pro numbers.**

| Implementation | Wall time | Integer overflow |
|---|---|---|
| rust climbing_stairs (`-C overflow-checks=on`) | 111.1 ± 3.1 ms | **checked (panics)** |
| **kāra climbing_stairs**            | **136.3 ± 3.3 ms** | **checked (traps)** |
| rust climbing_stairs (rustc -O)     | 171.3 ± 2.9 ms | **wraps silently** |
| c    climbing_stairs (clang -O3)    | 172.4 ± 2.9 ms | **wraps silently** |
| go   climbing_stairs                | 188.4 ± 2.8 ms | **wraps silently** |

Read this in two halves. Against the **wrapping** natives (rust `-O` 171, clang 172, go 188 ms) kāra now **leads** — ~1.26× ahead of C and Rust, ~1.38× ahead of Go — *despite* paying default overflow checks on `a + b` / `acc*131 + …` that they skip. That lead is new: it comes from karac now partial-unrolling the scalar fib loop 4× (`B-2026-07-08-24`), which cut kāra from 210.3 → 136.3 ms (−19 % instructions). The **load-bearing row is the equal-safety one**: `rustc -O -C overflow-checks=on` at **111.1 ms is 1.23× faster than kāra** — a real but modest residual (was 1.89× before the fix). Both are now checked *and* 4×-unrolled; the remaining gap is a smaller codegen difference (rust's native unroller schedules the checked recurrence a touch tighter than kāra's forced count). The equal-safety row is why overflow-checks-on Rust is the *fastest* build here: enabling the checks hands LLVM the nsw facts that trip its unroller — the same unroll kāra now performs directly. What was the corpus's clearest single-kata loss is now a win over every wrapping build and a narrow, tracked residual against checked Rust.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py climbing_stairs` (K=3M) | 807.1 ± 11.1 ms |

Python at K=3M is ~0.81 s; projecting to the compiled mirrors' K=30M (~8.1 s) puts it **~59× slower than kāra seq** — the recurrence's per-iteration integer adds run bytecode-by-bytecode, CPython's worst case.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 climbing_stairs.c          | **35.8 ms** |
| rustc -O climbing_stairs.rs          | 71.4 ms |
| **karac build climbing_stairs.kara** | **79.9 ms** |

On the M5 karac compiles at ~2.08× clang and just ~1.10× rustc — a near-tie with rustc on this small scalar program.

### Binary size

| Implementation | Size |
|---|---|
| c    climbing_stairs                | 32.7 KiB |
| **kāra climbing_stairs**            | **33.1 KiB** |
| go   climbing_stairs                | 2.38 MiB |
| rust climbing_stairs                | 455.4 KiB |

Kāra's seq binary is **33.1 KiB — within ~0.4 KiB of C's 32.7 KiB** (same lean M5 floor as [#69](../69-sqrtx/)), and orders of magnitude below Rust's 455 KiB and Go's 2.4 MiB.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra climbing_stairs**            | **1.00 MiB** |
| c    climbing_stairs                | 1.02 MiB |
| rust climbing_stairs                | 1.05 MiB |
| go   climbing_stairs                | 2.67 MiB |

Kāra's peak RSS is the **lowest of the four** — the working set is a handful of scalars, so peak is the process/runtime base; kāra's edges under C and Rust, with Go carrying its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 climbing_stairs.c          | **2.5 MiB** |
| **karac build climbing_stairs.kara** | **18.6 MiB** |
| rustc -O climbing_stairs.rs          | 24.8 MiB |

On the M5 karac's compile-memory footprint sits between clang (lowest) and rustc — under rustc's.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap. This kata started as the corpus's clearest *loss* (kāra trailed checked Rust 1.89× because Rust runtime-unrolls the fib loop and kāra didn't) — and it drove a karac fix: partial-unrolling pure-scalar counted loops (`B-2026-07-08-24`). After it, kāra **leads all three wrapping builds** and the equal-safety residual against checked Rust narrowed to 1.23×. C calibrates the (wrapping) LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. The load-bearing facts are the five-language sink agreement, the found-and-fixed unroll gap, kāra's lead over every wrapping build at a stricter safety posture, and that it still holds a near-C binary (no unroll bloat) and the lowest peak RSS of the four. Same pattern as sibling katas [#62](../62-unique-paths/)/[#63](../63-unique-paths-ii/): found a gap, fixed the compiler, kept the natural code.
