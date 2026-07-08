# 69. Sqrt(x)

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/sqrtx](https://leetcode.com/problems/sqrtx/)

Return **⌊√x⌋** — the integer part of the square root of a non-negative integer `x` — computed **without** any floating point or a built-in `sqrt`.

```
x = 4   →  2      exact
x = 8   →  2      ⌊2.828…⌋ = 2   (LeetCode example)
x = 2147483647 → 46340         i32 max, just below 46341² = 2147488281
```

**Constraints:** `0 ≤ x ≤ 2³¹ − 1` (2,147,483,647).

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Binary search** ★ — largest `r` with `r*r ≤ x`, on the monotone predicate | O(log x) | [`sqrtx.kara`](sqrtx.kara) ✓ via `karac run` / `karac build` | [`sqrtx.py`](sqrtx.py) ✓ |
| **Newton's method** — integer `r ← (r + x/r) / 2` until it stops shrinking | O(log log x) iters | [`sqrtx_newton.kara`](sqrtx_newton.kara) ✓ | — |
| **Bit-by-bit** — long-division √ over powers of four; **no multiplication** | O(log x), shift/add only | [`sqrtx_bits.kara`](sqrtx_bits.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all twenty-seven test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## Three routes to the floor

The answer is defined by a monotone predicate — `r*r ≤ x` is true for every `r` up to ⌊√x⌋ and false after — so this is a search for a boundary, and the three solvers are three ways to reach it.

**Binary search** ([`sqrtx.kara`](sqrtx.kara)) is the ★: it reads "largest `r` with `r*r ≤ x`" directly. Halve the interval each step, keep the best `r` whose square fits, and it lands on the floor in ~31 steps for x near 2³¹. It is the same monotone-predicate search template as katas [#35](../35-search-insert-position/) and [#34](../34-find-first-and-last-position/), specialised to the predicate `mid*mid ≤ x`, with `lo + (hi - lo) / 2` avoiding a `lo + hi` overflow.

**Newton's method** ([`sqrtx_newton.kara`](sqrtx_newton.kara)) converges far faster — a handful of steps even at 2³¹. Starting from an overestimate `r = x`, the truncating average `r ← (r + x/r) / 2` monotonically descends to exactly ⌊√x⌋; integer `/` rounding toward zero is precisely what makes it settle on the floor instead of oscillating. `x = 0` is special-cased to avoid the `x / r` division by zero.

**Bit-by-bit** ([`sqrtx_bits.kara`](sqrtx_bits.kara)) is the outlier: it builds the result one binary digit at a time, high to low, using only shifts, adds, and compares — **never a multiplication**. A probe walks down the powers of four (`4ᵏ = (2ᵏ)²`); at each, `res + bit` is the candidate square of "the answer so far with this bit set," accepted (subtract, set the bit, `res = res/2 + bit`) iff the remainder still covers it, else rejected (`res = res/2`). The `res/2` rescales the partial root as the place value drops ×4. It is the method a fixed-point or no-multiplier context reaches for.

## The overflow angle — where Kāra's checks matter

The natural predicate is `mid*mid ≤ x`, and `mid` ranges up to ~`x ≤ 2.1·10⁹` — so `mid*mid` overflows a **32-bit** integer. In C/Java the usual fixes are to compute the product in a wider type or to rewrite it as the division `mid ≤ x / mid` to dodge the overflow. **Kāra checks integer overflow by default**, so a 32-bit `mid*mid` would *trap* rather than silently wrap — surfacing the bug instead of hiding it. Computing in **i64** keeps the honest `mid*mid ≤ x` comparison (largest product on the path ≈ 4.6·10¹⁸ < i64::MAX ≈ 9.2·10¹⁸) with no division-based rewrite. The bit-by-bit method sidesteps the question entirely — it has no product term at all.

## Kāra features exercised

- **`i64` binary search with an overflow-safe midpoint** — `lo + (hi - lo) / 2` and the monotone `mid*mid <= x` predicate, the search template shared with katas [#35](../35-search-insert-position/)/[#34](../34-find-first-and-last-position/), here in i64 so the squaring test never trips Kāra's default overflow trap.
- **Integer Newton iteration** — `r = (r + x / r) / 2` with truncating `/`, plus the `x == 0` guard and a mid-function `return`; the convergence-loop idiom.
- **Pure shift/add bit-twiddling** — the bit-by-bit solver's `bit / 4` power-of-four walk and `res / 2` rescale (all `/` by constant powers of two, i.e. shifts), a multiplication-free numeric kernel — a distinct codegen surface from the squaring solvers.
- **Scalar `report`/`sums:` harness** — one `sqrt(x) = r` per line plus the folded `sums:` checksum, the byte-for-byte diff anchor shared with the numeric katas [#50](../50-powx-n/) and [#29](../29-divide-two-integers/); all three solvers and the Python mirror print it identically.

**v1 note.** All arithmetic is i64. The binary-search and Newton solvers rely on i64 headroom for `mid*mid` / `r*r` (≤ ~4.6·10¹⁸ at x = 2³¹) staying under i64::MAX; the bit-by-bit solver has no product and stays trivially in range. Newton special-cases `x == 0` (its loop would divide by `r = 0`); binary search and bit-by-bit handle 0 with no special case (the search collapses to `ans = 0`, the probe loop leaves `res = 0`).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   sqrtx.kara
karac build sqrtx.kara && ./sqrtx

# The alternative approaches (identical output):
karac run sqrtx_newton.kara
karac run sqrtx_bits.kara

# Python
python3 sqrtx.py

# Verify they all agree
diff <(karac run sqrtx.kara) <(python3 sqrtx.py)         && echo OK
diff <(karac run sqrtx.kara) <(karac run sqrtx_newton.kara) && echo OK
diff <(karac run sqrtx.kara) <(karac run sqrtx_bits.kara)   && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`sqrtx.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-08).** The numbers below were measured on the corpus's **Apple M5 Pro reference machine** (arm64, clang 21 / rustc 1.95 / go 1.26), replacing the earlier x86-64 cloud-container snapshot. **The equal-safety headline holds:** kāra 235.8 ms ties `rustc -O -C overflow-checks=on` at 234.6 ms (within noise), while the wrapping native builds (c 134.4, rust 167.8, go 177.7 ms) are faster only because they skip the overflow checks. Kāra's checked-multiply codegen is at parity with Rust's checked-multiply codegen on the M5, same as the container pass showed.

**Workload.** A single ⌊√x⌋ is O(log x) — cheap — so the bench runs the binary-search ★ **K = 3,000,000** times over a **Knuth-multiplicative sweep** `x = (k·2654435761) % 2³¹`, scattering `x` across the full `[0, 2³¹)` range so every iteration searches a different value (nothing hoistable) and the search runs its full ~31-step depth. No allocation — the whole body is the search loop (an integer `mid*mid ≤ x` compare per step). The sink is a rolling polynomial hash `acc = (acc*131 + r) % 1_000_000_007` over the results; all four compiled mirrors must agree on `759234816` before timing.

### The equal-safety comparison is the headline

This kata is the corpus's clean illustration of the BENCHMARKS.md **equal-safety** rule. The hot `mid*mid` is a **checked** multiply in Kāra (overflow trap by default) but a **wrapping** one under `rustc -O`/`clang -O3` — and `mid*mid` *genuinely* overflows i32 here, so the checks are load-bearing, not hypothetical. Comparing checked-Kāra against unchecked-Rust is apples-to-oranges; the honest comparison adds a `rustc -O -C overflow-checks=on` row.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **M5 Pro numbers.**

| Implementation | Wall time | Integer overflow |
|---|---|---|
| c    sqrtx (clang -O3)                | 134.4 ± 1.8 ms | **wraps silently** |
| rust sqrtx (rustc -O)                 | 167.8 ± 0.7 ms | **wraps silently** |
| go   sqrtx                            | 177.7 ± 1.3 ms | **wraps silently** |
| rust sqrtx (`-C overflow-checks=on`)  | 234.6 ± 4.3 ms | **checked (panics)** |
| **kāra sqrtx**                        | **235.8 ± 5.4 ms** | **checked (traps)** |

Read the table in two halves. Against the **default** (wrapping) native builds kāra is ~1.40× behind Rust and ~1.75× behind C — but that gap is almost entirely the **cost of the overflow checks kāra runs and they don't**. The load-bearing pair is the last two rows: at **equal safety**, kāra's 235.8 ms **ties `rustc -O -C overflow-checks=on` at 234.6 ms** — a 0.5 % gap, inside the run-to-run noise (kāra ±5.4, rust-ofl ±4.3 ms). So Kāra's checked-multiply codegen is on par with Rust's checked-multiply codegen; the apparent "slowness" is the price of not silently wrapping `mid*mid`, a price Rust pays identically when you ask it to. This is exactly the case the corpus discipline exists to frame honestly — quoting only the kāra-vs-default-Rust ratio would misrepresent a *safety* difference as a *codegen* one.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py sqrtx` (K=300k) | 408.6 ± 3.0 ms |

Python at K=300k is ~0.41 s; projecting to the compiled mirrors' K=3M (~4.1 s) puts it **~17× slower than kāra seq** — the per-iteration body is the whole ~31-step binary search, run in bytecode.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 sqrtx.c          | **35.8 ms** |
| rustc -O sqrtx.rs          | 67.9 ms |
| **karac build sqrtx.kara** | **76.3 ms** |

On the M5 karac compiles at ~2.1× clang and just ~1.12× rustc — a near-tie with rustc, on this small scalar single-file program.

### Binary size

| Implementation | Size |
|---|---|
| c    sqrtx                | 32.6 KiB |
| **kāra sqrtx**            | **33.1 KiB** |
| go   sqrtx                | 2.38 MiB |
| rust sqrtx                | 455.3 KiB |

Kāra's seq binary is **33.1 KiB — within ~0.5 KiB of C's 32.6 KiB**, and orders of magnitude below Rust's 455 KiB and Go's 2.4 MiB. This all-scalar, zero-allocation workload sits at the same lean M5 floor as the other single-file katas.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra sqrtx**            | **1.00 MiB** |
| c    sqrtx                | 1.02 MiB |
| rust sqrtx                | 1.06 MiB |
| go   sqrtx                | 2.64 MiB |

Kāra's peak RSS is the **lowest of the four** — the working set is a handful of scalars, so peak is the process/runtime base; kāra's is a hair under C and Rust, with Go carrying its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 sqrtx.c          | **2.5 MiB** |
| **karac build sqrtx.kara** | **18.8 MiB** |
| rustc -O sqrtx.rs          | 24.7 MiB |

On the M5 karac's compile-memory footprint sits between clang (lowest) and rustc — under rustc's.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap. Here that gap is entirely a **safety** gap: at equal overflow safety kāra matches Rust, and the only reason kāra trails the default `rustc -O` is that kāra refuses to silently wrap `mid*mid`. C calibrates the (wrapping) LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. The load-bearing claims are the five-language sink agreement, the equal-safety parity with checked Rust, a near-C binary, and the lowest peak RSS of the four.
