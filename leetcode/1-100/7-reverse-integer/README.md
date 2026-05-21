# 7. Reverse Integer

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-integer](https://leetcode.com/problems/reverse-integer/)

Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing causes the value to fall outside the signed 32-bit range `[-2³¹, 2³¹ − 1]`, return `0`. The problem statement forbids storing 64-bit intermediates — the overflow check has to live inside the 32-bit world.

```
123          →  321
-123         →  -321
120          →  21          (trailing zeros drop)
1534236469   →  0           (reversed = 9_646_324_351 > INT_MAX)
```

**Constraints:** `-2³¹ ≤ x ≤ 2³¹ − 1`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Pop-and-push with pre-multiply overflow check | O(log₁₀ \|x\|) time, O(1) space | [`reverse.kara`](reverse.kara) ✓ via `karac run` / `karac build` | [`reverse.py`](reverse.py) ✓ | [`bench/reverse.rs`](bench/reverse.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 14 test cases.

## Why pop-and-push

The textbook formulation walks digits least-significant first:

```
digit  = x % 10
result = result * 10 + digit
x      = x / 10
```

Three operations per digit, all in registers, no allocation. The interesting part is the overflow check, not the digit walk.

### The overflow rails

Doing the multiply first and checking after won't work — the multiply itself is the overflow event. The check has to fire *before* the multiply, against `INT_MAX / 10` and `INT_MIN / 10`:

```
if result >  INT_MAX / 10                                       { return 0; }
if result == INT_MAX / 10 and digit > 7                         { return 0; }
if result <  INT_MIN / 10                                       { return 0; }
if result == INT_MIN / 10 and digit < -8                        { return 0; }
```

The boundary digits (`7` and `-8`) are the last digits of `INT_MAX = 2_147_483_647` and `INT_MIN = -2_147_483_648`. Any input whose reverse fits in i32 cleanly skips both rails; any input that overflows trips one of them before the offending multiply runs.

### Why one loop covers both signs

Kāra's `%` follows C/Rust semantics — the sign of the result matches the *dividend*:

```
(-123) % 10 == -3       (not 7, as Python would give)
(-123) /  10 == -12     (truncated toward zero)
```

So a single `while x != 0` loop walks negatives correctly without a sign flip — `digit` carries the sign of `x`, and `result * 10 + digit` accumulates a negative reversed value. Python's `%` floors instead, so [`reverse.py`](reverse.py) defines `c_div` / `c_mod` helpers to mirror the truncated-division shape. Without that mirror the Python output would diverge on every negative input.

## Kāra features exercised

- **`i32` arithmetic end-to-end** — `let result: i32 = 0i32`, `let digit: i32 = x % 10i32`, comparisons against typed constants like `7i32` and `-8i32`. The LeetCode constraint ("the environment does not allow 64-bit integers") maps directly to keeping every variable in `i32`; the kata refuses to widen to `i64` even for the check.
- **Truncated `%` and `/`** — Kāra inherits Rust's sign-of-dividend modulo, which is what the algorithm needs. The Python mirror has to emulate this with `c_div` / `c_mod` because Python's operators floor instead.
- **Compound boolean guards** — `result > max_div or (result == max_div and digit > 7i32)`. Mixed `or`/`and` with parens parses as expected; the lowering short-circuits both `or` and `and` arms.
- **Early `return` with typed literal** — `return 0i32` inside a function declared `-> i32`. The literal suffix is load-bearing here — bare `0` would be inferred as `i64` and trip a codegen type-mismatch.
- **`println(r)` on a narrow signed int** — direct print of an `i32` renders the signed decimal in both the interpreter and the codegen path. Pre-fix, codegen formatted the value as unsigned (e.g. `-123` printed as `4_294_967_173`) because the printf arm passed the raw `i32` to `%lld` and LLVM zero-padded the varargs slot. The 2026-05-19 codegen fix routes narrow ints through `sext + %lld` (signed) or `zext + %llu` (unsigned) based on the source-level type — surfaced while writing this kata, landed alongside it.

No `Vec`, no `String`, no `Map`, no shared structs — pure scalar arithmetic.

## Edge cases worth exercising

| Input | Expected | Why it's interesting |
|---|---|---|
| `0` | `0` | The `while x != 0` loop body never runs; `result` stays at its `0` init. |
| `1` / `-1` | `1` / `-1` | Single iteration; tests the negative path skips no rail. |
| `10` / `-10` | `1` / `-1` | Trailing-zero drop — `10 % 10 == 0` so the first iter contributes `0`, second iter contributes `1`. |
| `120` | `21` | Trailing-zero drop on a multi-digit input. |
| `1463847412` | `2147483641` | Just under `INT_MAX` — exercises the boundary without tripping it. |
| `1463847413` | `0` | Same shape, last digit increments — should trip the `digit > 7` rail at the boundary. |
| `1534236469` | `0` | Overflows comfortably — trips the `result > max_div` rail before the boundary check. |
| `2147483647` | `0` | `INT_MAX` itself — reversed is `7463847412`, overflows. |
| `-2147483648` | `0` | `INT_MIN` — reversed is `-8463847412`, trips the `min_div` rail. |
| `-1463847412` | `-2147483641` | Mirror of the just-under-INT_MAX case, against the negative rail. |

All 14 cases run in `main` and the output is diffed against [`reverse.py`](reverse.py).

## API shape

`reverse(x: i32) -> i32` is the algorithm; `report(x: i32)` prints the result; `main` calls `report` per test case. Logic is separated from I/O so the function would slot into a future test harness unchanged. The Python file mirrors this with `reverse(x: int) -> int` and the same `report` / `main` shape.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   reverse.kara
karac build reverse.kara && ./reverse

# Python
python3 reverse.py

# Verify they agree
diff <(./reverse) <(python3 reverse.py) && echo OK
diff <(karac run reverse.kara) <(python3 reverse.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs hyperfine for runtime + cold-compile, plus straight `wc` / `time -l` reads for binary size + memory. Python is timed in a separate stanza at K = 1M and projected to K = 50M (a full python sample at K = 50M is ~80 s, too slow for the iterative dev loop).

| File | What it does |
|---|---|
| [`bench/reverse.kara`](bench/reverse.kara) | N = 1024 LCG-fill i32 inputs, K = 50,000,000 outer iters, sink = Σ reverse(inputs[k % N]) as i64 |
| [`bench/reverse.py`](bench/reverse.py) | Algorithmic mirror — same N, K, same LCG fill, same sink formula |
| [`bench/reverse.rs`](bench/reverse.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sink (`-292_465_958_482_676` at the default parameters) so the algorithm's output participates in I/O and can't be elided. The bench's `bench.sh` asserts the kara and rust sinks match before timing; the python stanza prints its own sink (different K, expectedly different value).

### Runtime — 11.18× ahead of Rust via auto-par reduction

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`. Requires karac at commit [`28d76af`](../../../../karac-rust/) or later — picks up the original auto-par reduction lowering (slice 3b.4 + 3b.6, `415508c`) plus the three par-reduce single-thread perf commits landed 2026-05-20: [`a9e51c8`](../../../../karac-rust/) const-prop top-level let-init captures into the worker (`n = 1024` arrives as a constant, not a heap load per iter), [`1712d51`](../../../../karac-rust/) `llvm.assume` non-negative loop var (ARM64 signed-mod-pow2 collapses from 4 instr to 1), [`28d76af`](../../../../karac-rust/) vec-bounds-check hoist via modulo (per-iter cmp+b.hs moves to function entry).

| Run | Mean ± σ |
|---|---|
| `kara reverse` (codegen) | 38.7 ± 1.9 ms |
| `rust reverse` | 433.1 ± 2.7 ms |
| `py   reverse` (K = 1M, ×50 projection) | 85,946 ms (~86 s projected) |

The K = 50M outer loop is shaped `let mut sum = 0i64; let mut k = 0i64; while k < k_iters { sum = sum + (reverse(inputs[k % n]) as i64); k = k + 1i64; }` — a textbook reduction over the `sum` accumulator. The slice-1 concurrency analyzer recognizes this pattern (`karac build --concurrency-report bench/reverse.kara` prints `reduction { op: +, accumulator: sum, line: 64 }`); the slice-3b codegen lowers it to a `karac_par_reduce` call that fans the iteration space across the available cores, each thread accumulating into a private partial slot, then a final serial combine pass folds the partials into the parent's `sum`. The reduction op is associative + commutative (the slice-1 allow-list constraint), so the combine order doesn't affect the result — every run produces the same sink (`-292_465_958_482_676`) regardless of how the work was split. **No source-level changes** to express the parallelism: the analyzer recognizes the shape from the natural serial source.

CPU utilization tells the parallelism story: hyperfine's reading is **User 569.9 ms / wall 38.7 ms ≈ 14.7× CPU usage** — close to perfect parallel scaling across the M5 Pro's 6 P-cores + 12 E-cores. Per-iter work is enough (~10 inner iters of i32 mod/compare/mul-add per outer iter) to amortize the thread-spawn overhead; the inputs Vec fits comfortably in L1 cache (1024 × 4 bytes = 4 KiB), so workers reading the shared buffer don't contend on cache lines.

Rust stays single-threaded at 433 ms — the Rust mirror's `for k in 0..k_iters { sum += reverse(inputs[(k % n) as usize]) as i64; }` is the same shape, but `rustc -O` doesn't auto-parallelize without explicit `rayon::par_iter()` or similar annotation. Adding rayon to the Rust source would close most of the gap, but that's a manual user step — kara's compiler does it automatically based on the source shape the slice-1 analyzer recognizes. **Previous readings:** 2026-05-19 (pre-auto-par): kara 418.8 ms vs rust 427.6 ms — at parity. 2026-05-20 (initial auto-par, pre-perf-commits): kara 45.0 ms vs rust 444.0 ms — 9.87× ahead. The current 11.18× is the auto-par lowering plus the three single-thread perf commits, which dropped per-worker user time from 648.9 ms → 569.9 ms.

### Codegen vs Python

Python is **~2,220× slower than Kāra codegen** at the same K (extrapolated from the K = 1M sample at 1718.9 ms; the projection to K = 50M is 85,946 ms vs kara's 38.7 ms). The reverse() body is dominated by CPython's per-bytecode dispatch — `c_mod` / `c_div` are pure-python helpers (no `divmod` shortcut for negatives gives the right answer here) so each loop iter spends ~5–10 µs in interpreter overhead vs a handful of nanoseconds in the codegen path. The gap is wider than kata [#6](../6-zigzag-conversion/#codegen-vs-python)'s ~32× because (a) there's no C-implemented `list.append` doing the heavy lifting — every operation is at the bytecode level — and (b) kara fans the outer loop across cores via auto-par reduction while CPython runs the GIL-locked single-threaded loop. The serial-vs-serial gap (kara's 569.9 ms user time vs python's 85,946 ms) is **~151×**; the auto-par lowering widens that to 2,220× on wall.

### Runtime memory — slightly above Rust (worker thread overhead)

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara reverse` (codegen) | 1.5 MiB |
| `rust reverse` | 1.1 MiB |

Kara is ~0.4 MiB above Rust (was at parity pre-auto-par). The delta is the worker thread stacks — `karac_par_reduce` dispatches onto the long-lived `karac_par_run` pool (slice 3b.7), which holds N OS-thread stack reservations regardless of how many reductions actually fire. The pool's lazy-init creates N = `available_parallelism()` threads on the first auto-par call; each stack reservation adds to peak RSS even when most of the stack is never touched. Acceptable cost for the 11× speedup; the residual delta lives at the runtime-pool layer and would close (or reverse) only by tuning the pool's default thread count downward (separate slice — needs a knob for users running on memory-constrained targets). Pool sizing is currently `max(2, available_parallelism)`, which is the standard pool-API default; trimming to (say) the P-core count would cut the reservation in half on big.LITTLE hardware like the M5 Pro, at the cost of leaving E-cores unused under heavy load.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build reverse.kara` | 57.7 ± 0.5 ms | 311.9 KiB |
| `rustc -O reverse.rs` | 79.6 ± 0.6 ms | 455.6 KiB |

Kāra compiles this kata **1.38× faster** than `rustc -O` and produces a binary **1.46× smaller**. The kara binary grew from 49 KiB (pre-auto-par) to 311.9 KiB because the par_reduce lowering links in the karac-runtime's thread-pool + worker-dispatch code; rust's binary is unchanged because it doesn't pull in `std::sync::mpsc` / `std::thread::scope` for a single-threaded loop. Even with the new runtime weight, kara stays smaller than rust thanks to the cross-archive LTO + DCE work (landed 2026-05-12). The three perf commits added negligible compile overhead — the const-prop, assume, and BCE-hoist passes are bounded constant work per recognized site.

Compile memory: karac peaks at **8.8 MiB** vs rustc's **26.9 MiB** — ~3× lower compile-time RAM, essentially unchanged from the pre-auto-par snapshot (the reduction lowering is bounded constant work per recognized site).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. The current result — **11.18× ahead of Rust on runtime via auto-par reduction, 1.46× smaller binary, 1.38× faster compile, ~3× lower compile RAM, +0.4 MiB peak RSS for the worker thread pool** — is the first kata where kara's auto-concurrency machinery lights up against a serial Rust baseline. The slice-1 analyzer recognizes the source shape; the slice-3 codegen lowers it without any user annotation. The three par-reduce single-thread perf commits (const-prop captures, assume non-neg loop var, BCE-hoist via modulo) widened the original 9.87× gap to 11.18× by cutting per-worker user time from 648.9 ms → 569.9 ms. Adding `rayon::par_iter()` to the Rust source would close most of the gap, but the comparison is meaningful exactly because that step is a manual rewrite on the Rust side and automatic on the kara side.
