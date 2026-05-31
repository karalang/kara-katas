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

- **`i32` arithmetic end-to-end** — typed literals like `7i32` and `-8i32` keep every variable in `i32`, honoring the "no 64-bit storage" constraint.
- **Truncated `%` and `/`** — sign-of-dividend modulo is what the algorithm needs; the Python mirror has to emulate this via `c_div` / `c_mod`.
- **Compound boolean guards** — `result > max_div or (result == max_div and digit > 7i32)` short-circuits both `or` and `and` arms.
- **Early `return` with typed literal** — `return 0i32` inside a `-> i32` function; the suffix avoids an `i64`-inference codegen mismatch.
- **`println(r)` on a narrow signed int** — codegen renders signed decimals correctly via sign-extension into `%lld` (fix landed 2026-05-19).

No `Vec`, no `String`, no `Map`, no shared structs — pure scalar arithmetic.

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

Per [`../../../BENCH.md`](../../../BENCH.md), the K = 50M outer loop reduces via `sum += reverse(inputs[k % N]) as i64` — karac's auto-par-on-reduction recognizes the shape and emits a `karac_par_reduce` dispatch by default (`nm -gU bench/target/reverse_kara | grep karac_par_reduce` confirms). The bench ships two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`reverse_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`reverse_kara`** — default `karac build` output. Picks up auto-par dispatch (~14 cores active on this workload). Reported separately so the production-default Kara behavior stays visible — **not** headlined cross-lane against the single-threaded comparators.

| File | What it does |
|---|---|
| [`bench/reverse.kara`](bench/reverse.kara) | N = 1024 LCG-fill i32 inputs, K = 50,000,000 outer iters, sink = Σ reverse(inputs[k % N]) as i64 |
| [`bench/reverse.rs`](bench/reverse.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/reverse.c`](bench/reverse.c) | Algorithmic mirror; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |
| [`bench/reverse.py`](bench/reverse.py) | Algorithmic mirror — same N, same LCG fill, same sink formula (sampled at K = 1M, projected ×50) |

All compiled mirrors print the same sink (`-292_465_958_482_676`) so the algorithm's output participates in I/O and can't be elided; `bench.sh` asserts agreement across kara/kara_seq/rust/c/go before timing. Python is sampled at K = 1M (a full K = 50M python run is ~88 s) and projected ×50 — console-only, since its K differs from the compiled mirrors.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0`), `rustc -O`, `clang -O3`, `go build`. Kara seq binary verified single-threaded: `nm -gU bench/target/reverse_kara_seq | grep karac_par` finds no auto-par symbols.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| **kāra reverse** (`KARAC_AUTO_PAR=0`) | **462.0 ms ± 35.9 ms** | 456.7 ms | **1.00×** (baseline) |
| rust reverse                          | 461.4 ms ± 7.8 ms      | 458.2 ms | 1.00× of Kāra |
| c    reverse (clang -O3)               | 473.1 ms ± 5.9 ms      | 469.4 ms | 1.02× of Kāra |
| go   reverse                           | 529.8 ms ± 27.3 ms     | 523.4 ms | 1.15× of Kāra |

Pure scalar i32 arithmetic — a tight `while x != 0` digit loop with two overflow rails, no allocations. **Kāra's seq lane is at parity with Rust** (462 vs 461 ms, inside run-to-run variance — kara's σ was elevated by outliers this run, but its min of 437.8 ms edged below Rust's 451.4 ms), a hair ahead of clang-O3, and 1.15× ahead of Go. This is the honest per-core codegen comparison: on a scalar kernel that all four lower to near-identical inner loops, Kāra lands in the pack. The parity here is held by three karac perf commits that tuned this shape (2026-05-20): [`a9e51c8`](../../../../karac-rust/) const-prop of top-level let-init captures (`n = 1024` arrives constant, not a per-iter heap load), [`1712d51`](../../../../karac-rust/) `llvm.assume` non-negative loop var (ARM64 signed-mod-pow2 collapses from 4 instr to 1), [`28d76af`](../../../../karac-rust/) vec-bounds-check hoist via modulo (per-iter `cmp + b.hs` moves to function entry).

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output, hyperfine `--warmup 10 --runs 50`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra reverse** (auto-par on reduction) | **41.6 ms ± 2.5 ms** | 568.9 ms | ~1368% (~14 cores) |

The K = 50M outer loop is shaped `let mut sum = 0i64; while k < k_iters { sum = sum + (reverse(inputs[k % n]) as i64); k = k + 1i64; }` — a textbook reduction over `sum`. The slice-1 concurrency analyzer recognizes it (`karac build --concurrency-report bench/reverse.kara` prints `reduction { op: +, accumulator: sum }`); slice-3b codegen lowers it to a `karac_par_reduce` call that fans the iteration space across cores, each thread accumulating a private partial, then a serial combine folds them. The op is associative + commutative, so the sink (`-292_465_958_482_676`) is identical regardless of how the work splits. **No source-level changes** express the parallelism — the analyzer recognizes the shape from the natural serial source. The inputs Vec fits in L1 (1024 × 4 B = 4 KiB), so workers reading the shared buffer don't contend on cache lines.

**Not headlined against the rust / c / go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 11× faster than rust" would conflate per-core codegen quality (where kara is at *parity* with Rust, above) with whether the comparator opted into parallelism. Rust at 461 ms is single-threaded; `rustc -O` won't auto-parallelize without a manual `rayon::par_iter()` rewrite, whereas kara's compiler does it automatically from the natural serial source. So the auto-par win is reported as an **intra-Kāra 11.1× speedup** (462.0 / 41.6, User 568.9 / wall 41.6 ≈ 14× CPU across the M5 Pro's 6 P + 12 E cores) — the same number that anchors this kata's point on the repo's [auto-parallel speedup chart](../../../BENCHMARKS.md#auto-parallel-speedup-kāra).

### Codegen vs Python

Python (sampled at K = 1M: 1.769 s ± 0.011 s, projected ×50 to ~88.5 s at K = 50M) runs the same algorithm **~191× slower than Kāra's seq lane** (88.5 s / 462 ms) — the honest serial-vs-serial gap. The `reverse()` body is dominated by CPython's per-bytecode dispatch; `c_mod` / `c_div` are pure-python helpers, since Python's floor-division `%` gives the wrong sign for negatives and the mirror has to emulate truncated division. The auto-par regime widens the *wall* gap further (~2,130×), but that's a cross-lane figure — the ~191× seq-vs-seq number is the codegen-quality comparison.

### Runtime memory (peak, RSS)

Same snapshot:

| Implementation | Peak RSS |
|---|---|
| c    reverse | 1.1 MiB |
| **kāra reverse (seq)** | **1.1 MiB** |
| rust reverse | 1.1 MiB |
| kāra reverse (auto-par) | 1.4 MiB |
| go   reverse | 3.0 MiB |

The seq lane is at **three-way parity with C and Rust** (1.1 MiB each) — pure scalar arithmetic with no heap. The auto-par variant lands at 1.4 MiB: +0.3 MiB for the worker-thread stacks `karac_par_reduce` dispatches onto the long-lived `karac_par_run` pool (slice 3b.7), which reserves N = `available_parallelism()` OS-thread stacks on first auto-par call regardless of how many reductions fire. Acceptable cost for the 11.1× speedup; the residual would close only by tuning the pool's default thread count downward (a separate knob for memory-constrained targets). Go's 3.0 MiB carries its GC roots + scheduler arena.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 1 --runs 10` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `reverse` | **64.2 ± 1.9 ms** | 78.5 ± 1.3 ms | 41.6 ± 0.9 ms |

`karac build` is **1.22× faster than `rustc -O`** on this file, sitting between clang (the LLVM single-file floor) and rustc. Go is omitted per BENCH.md — `go build`'s first invocation mixes module resolution + link.

### Binary size

| Implementation | Size |
|---|---|
| c    reverse | 32.7 KiB |
| **kāra reverse (seq)** | **32.9 KiB** |
| kāra reverse (auto-par) | 295.8 KiB |
| rust reverse | 455.6 KiB |
| go   reverse | 2434.1 KiB |

The seq-lane Kāra binary is at parity with clang's (~33 KiB). The auto-par variant grows +263 KiB to carry the `karac_par_reduce` machinery (thread-pool init + worker-dispatch + reduction-combine globals) — the same +263 KiB ballast katas [#6](../6-zigzag-conversion/#binary-size) and [#8](../8-string-to-integer-atoi/) carry for the same mechanism, and still smaller than Rust's 455.6 KiB thanks to cross-archive LTO + DCE.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 reverse.c | 2.6 MiB |
| karac build reverse.kara | 10.0 MiB |
| rustc -O reverse.rs | 26.9 MiB |

`karac` compiles this file in **~10 MiB peak** — between clang and rustc, ~2.7× lower than rustc.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the load-bearing headline for v1 is the **seq-lane codegen-vs-Rust comparison — and there Kāra is at parity** (462 vs 461 ms, within σ), a hair ahead of C and Go. On top of that per-core baseline, Kāra's auto-concurrency machinery delivers a **language-level 11.1× intra-Kāra speedup** by parallelizing the reduction with no source change — reported separately (above) rather than as a cross-lane "ahead of Rust" number, because `rustc -O` stays single-threaded without a manual `rayon` rewrite and conflating the two lanes would overstate the codegen story. This is the first kata where that auto-par machinery lights up; the honest framing is *parity on codegen, plus free safe parallelism where the shape allows*.
