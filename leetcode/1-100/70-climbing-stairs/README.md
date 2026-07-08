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

> ⚠️ **Machine caveat.** Like katas [#63](../63-unique-paths-ii/#benchmarks)–[#69](../69-sqrtx/#benchmarks)'s container passes (and unlike the M5 Pro tables elsewhere in the corpus), the numbers below were measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.10 GHz, 4 vCPU, Linux 6.18.5). Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; `bench/results.json` records the real host. Re-run `bench/bench.sh` on the M5 to fold comparable numbers in.

**Workload.** A single `climb(n)` is O(n) with `n ≤ 45` — cheap — so the bench runs the rolling-counter ★ **K = 30,000,000** times over a sweep of `n = 1 + k%45` (every step count in `[1, 45]`), folding each result into a rolling hash `acc = (acc*131 + climb(n)) % 1_000_000_007`. Sweeping `n` re-runs the recurrence to a different depth each iteration (nothing hoistable), and the loop-carried sink keeps it seq. No allocation — the whole body is the two-counter integer-add loop. All four compiled mirrors must agree on `522887212` before timing.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All four single-threaded. **Cloud-container numbers — ratios, not absolutes.**

| Implementation | Wall time |
|---|---|
| c    climbing_stairs (clang -O3)    | 239.5 ± 5.4 ms |
| go   climbing_stairs                | 323.1 ± 4.6 ms |
| **kāra climbing_stairs**            | **374.3 ± 6.7 ms** |
| rust climbing_stairs (rustc -O)     | 446.2 ± 11.5 ms |

**This one goes to C, and kāra lands mid-pack** — ~1.56× behind C, but ~1.19× *ahead* of Rust, with Go in between. Two things drive the spread on this trivial Fibonacci micro-loop, and both are honest to name: (1) **`clang -O3` optimises it exceptionally** — a tight `a, b = b, a+b` loop over `n ≤ 45` is exactly the shape LLVM unrolls and schedules to the metal with no barrier in its way; (2) the native mirrors **wrap** on overflow while kāra runs its **default overflow checks** on `a + b` and `acc*131 + …` (the values never overflow here, so it is pure branch-not-taken overhead, but it is real). Rust is *slowest* not because its codegen is worse but because the `black_box(climb(n))` barrier — needed so `rustc` doesn't fold the whole constant-bounded loop away — also blocks the unrolling clang does freely; it is the honest cost of forcing the work to happen. So the takeaway is narrow: on a micro-loop this optimiser-sensitive, C's freedom to transform it wins, and kāra sits reasonably in the middle rather than at C-parity — a contrast to the scan/search katas (#66/#68) where kāra matched C. No equal-safety row is added here (unlike [#69](../69-sqrtx/)) because overflow never triggers, so the check cost is a fixed overhead, not the load-bearing gap — the gap is clang's loop transformation.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py climbing_stairs` (K=3M) | 2055 ± 28 ms |

Python at K=3M is ~2.06 s; projecting to the compiled mirrors' K=30M (~20.6 s) puts it **~55× slower than kāra seq** — the recurrence's per-iteration integer adds run bytecode-by-bytecode, CPython's worst case.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 climbing_stairs.c          | **72.9 ± 4.1 ms** |
| rustc -O climbing_stairs.rs          | 86.0 ± 3.1 ms |
| **karac build climbing_stairs.kara** | **126.2 ± 21.9 ms** |

On this container karac compiles at ~1.73× clang and ~1.47× rustc on this small scalar program (high variance on the shared host).

### Binary size

| Implementation | Size |
|---|---|
| **kāra climbing_stairs**            | **15.4 KiB** |
| c    climbing_stairs                | 15.6 KiB |
| go   climbing_stairs                | 2.11 MiB |
| rust climbing_stairs                | 3.77 MiB |

Kāra's seq binary is **15.4 KiB — the smallest of the four, a hair under C's 15.6 KiB** (same as [#69](../69-sqrtx/)), and orders of magnitude below Rust's 3.8 MiB and Go's 2.1 MiB. This all-scalar, zero-allocation workload links no runtime floor — the binary is essentially the code.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra climbing_stairs**            | **6.86 MiB** |
| c    climbing_stairs                | 6.86 MiB |
| rust climbing_stairs                | 6.86 MiB |
| go   climbing_stairs                | 6.86 MiB |

All four sit at the same ~6.86 MiB process/runtime floor — the working set is a handful of scalars.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build climbing_stairs.kara** | **83.9 MiB** |
| clang -O3 climbing_stairs.c          | 95.8 MiB |
| rustc -O climbing_stairs.rs          | 99.7 MiB |

On this container karac has the lowest compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here kāra *leads* Rust (~1.19×), both trailing C's aggressively-optimised micro-loop. C calibrates the (wrapping) LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. This kata is an honest "kāra doesn't always match C" data point: on a trivial recurrence loop the optimiser's freedom (and C's lack of a `black_box`-style barrier or overflow checks) puts it ahead; the load-bearing facts are the five-language sink agreement, kāra's lead over Rust, and the smallest-of-four binary.
