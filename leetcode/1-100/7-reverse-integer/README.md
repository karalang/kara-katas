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

Snapshot for every table below unless marked otherwise: Apple M5 Pro (6P+12E), karac `0.9.0-dev.14057+g6697158fa` (the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, go 1.26.3, hyperfine 1.20.0, measured 2026-10-31 (feed `measured_at` 2026-11-01T00:45Z UTC). Source of truth: [`bench/results.json`](bench/results.json).

> **Re-bench 2026-10-31 — what moved.** Quoted as language ratios, because every comparator ran 6–16% slower in absolute terms this session (machine state).
>
> - **Seq lane: near flat.** Kāra/Rust 1.18× → 1.23×, Kāra/C 1.13× → 1.18×, Kāra/Go 1.02× → 1.06× (previous feed: 2026-07-28, legacy backend) — every move under the 10% noise line.
> - **Par lane: worse.** Kāra/rayon 1.15× → 1.36×, Kāra/C-pthreads 1.12× → 1.33×, Kāra/Go 1.00× → 1.17× — a ~1.19× relative loss against every comparator.
> - **Binary size: 33.4 → 295.8 KiB (seq)** — see [Binary size](#binary-size).

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

Per [`../../../BENCH.md`](../../../BENCH.md), the K = 50M outer loop reduces via `sum += reverse(inputs[k % N]) as i64` — karac's auto-par recognizes the shape and parallelizes the reduction by default (the par build's IR carries a call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`)). The bench ships two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`reverse_kara_seq`** — built with `KARAC_AUTO_PAR=0` (the documented mechanism for side-by-side seq-vs-par benchmarking). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
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

M5 Pro, 2026-10-31, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0`), `rustc -O`, `clang -O3`, `go build`. Kara seq binary verified single-threaded: its IR carries no call of `karac_mir_task_spawn` (verified in the emitted IR (`KARAC_MIR_LL`)), and it runs at 99.9% CPU.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| rust reverse (`-O`, wrapping)          | 491.8 ms ± 6.7 ms      | 490.2 ms | 0.81× of Kāra |
| rust reverse (`overflow-checks=on`)    | 512.2 ms ± 22.4 ms     | 510.5 ms | 0.85× of Kāra |
| c    reverse (clang -O3)               | 513.5 ms ± 7.4 ms      | 511.9 ms | 0.85× of Kāra |
| go   reverse                           | 569.4 ms ± 15.6 ms     | 567.2 ms | 0.94× of Kāra |
| **kāra reverse** (`KARAC_AUTO_PAR=0`) | **606.0 ms ± 6.8 ms** | 604.1 ms | **1.00×** (baseline) |

Pure scalar i32 arithmetic — a tight `while x != 0` digit loop with two overflow rails, no allocations. **The apples-to-apples comparison is against equal-safety Rust.** Kāra checks integer overflow by default (the algorithm's whole point is the pre-multiply overflow rails); `rustc -O` *wraps* silently, so the 491.8 ms `-O` row is a no-overflow-check binary. Adding `-C overflow-checks=on` to Rust — matching Kāra's default safety — moves Rust to **512.2 ms ± 22.4 ms**, and against that lane Kāra is **1.18×** (606.0 vs 512.2 ms; it was 1.15× on the legacy backend). Part of the apparent gap to wrapping Rust is the overflow-check safety tax; a genuine residual survives at equal safety. On this kata that residual lives in the digit-decompose / reverse path — the per-iteration `% 10`, `/ 10`, and `result * 10 + digit` accumulation. Kāra runs 1.18× of clang-O3 (which checks nothing) and now trails Go by 1.06× (Go's ±15.6 ms band covers most of that gap). The standing here was set by three karac perf commits that tuned this shape on the legacy backend (2026-05-20): [`a9e51c8`](../../../../karac-rust/) const-prop of top-level let-init captures (`n = 1024` arrives constant, not a per-iter heap load), [`1712d51`](../../../../karac-rust/) `llvm.assume` non-negative loop var (ARM64 signed-mod-pow2 collapses from 4 instr to 1), [`28d76af`](../../../../karac-rust/) vec-bounds-check hoist via modulo (per-iter `cmp + b.hs` moves to function entry).

**Surfaced [`B-2026-11-07-1`](../../../../kara/docs/bugs-v2.md)** (perf, low, open). Raising SimplifyCFG's phi-fold threshold from 4 to 6 (kara `a723c25762`, for kata 342) costs this kata 1.11× the cycles on the M5 (kara 6e709e5fdd): the digit loop's rare `result == min_div and digit < -8` rail is now computed every digit as a select instead of a well-predicted branch.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output, hyperfine `--warmup 10 --runs 50`. All four languages parallelize the same K = 50M reduction; the difference is what the programmer wrote.

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust reverse (rayon) | **42.4 ms ± 0.8 ms** | 676.7 ms | ~1628% |
| c    reverse (pthreads) | 43.4 ms ± 2.9 ms | 638.1 ms | ~1473% |
| go   reverse (goroutines) | 49.4 ms ± 3.6 ms | 704.5 ms | ~1433% |
| **kāra reverse** (auto-par on reduction) | **57.7 ms ± 1.7 ms** | 818.1 ms | ~1427% (~14 cores) |

The K = 50M outer loop is shaped `let mut sum = 0i64; while k < k_iters { sum = sum + (reverse(inputs[k % n]) as i64); k = k + 1i64; }` — a textbook reduction over `sum`. The concurrency analyzer recognizes it (`karac build --concurrency-report bench/reverse.kara` prints `reduction { op: +, accumulator: sum }`); codegen fans the iteration space across cores, each thread accumulating a private partial, then a serial combine folds them. The op is associative + commutative, so the sink (`-292_465_958_482_676`) is identical regardless of how the work splits. **No source-level changes** express the parallelism — the analyzer recognizes the shape from the natural serial source. The inputs Vec fits in L1 (1024 × 4 B = 4 KiB), so workers reading the shared buffer don't contend on cache lines.

**Kāra with zero parallel source trails rayon 1.36×, C+pthreads 1.33× and Go 1.17×** (legacy backend: 1.15× / 1.12× / 1.00×). The seq-lane residual accounts for 1.23× of the rayon gap; the rest is the par lane losing ~1.19× relative to every comparator since the legacy feed. Kāra burns more user-CPU than any comparator (818 ms vs rayon's 677 ms) at a similar core count.

**Not headlined against the seq rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 8× faster than rust" would conflate per-core codegen quality with whether the comparator opted into parallelism. So the auto-par win is reported as an **intra-Kāra 10.5× speedup** (606.0 / 57.7, user 818.1 / wall 57.7 ≈ 14.2× CPU across the M5 Pro's 6 P + 12 E cores) — the same number that anchors this kata's point on the repo's [auto-parallel speedup chart](../../../BENCHMARKS.md#auto-parallel-speedup-kāra).

### Codegen vs Python

Last measured 2026-05-31, not re-run (this run did not set `KARA_BENCH_INCLUDE_PY`). Python (sampled at K = 1M: 1.769 s ± 0.011 s, projected ×50 to ~88.5 s at K = 50M) ran the same algorithm **~177× slower than Kāra's seq lane** of that snapshot (88.5 s / 500.7 ms) — the honest serial-vs-serial gap. The `reverse()` body is dominated by CPython's per-bytecode dispatch; `c_mod` / `c_div` are pure-python helpers, since Python's floor-division `%` gives the wrong sign for negatives and the mirror has to emulate truncated division. The auto-par regime widens the *wall* gap further (~1,860× at that snapshot), but that's a cross-lane figure — the seq-vs-seq number is the codegen-quality comparison.

### Runtime memory (peak, RSS)

Same snapshot:

| Implementation | Peak RSS |
|---|---|
| c    reverse | 1.0 MiB |
| **kāra reverse (seq)** | **1.0 MiB** |
| rust reverse | 1.1 MiB |
| c    reverse (pthreads) | 1.3 MiB |
| kāra reverse (auto-par) | 1.5 MiB |
| rust reverse (rayon) | 2.0 MiB |
| go   reverse | 2.7 MiB |
| go   reverse (goroutines) | 4.1 MiB |

The seq lane is at **three-way parity with C and Rust** (1.0–1.1 MiB) — pure scalar arithmetic with no heap. The auto-par variant lands at 1.5 MiB: +0.5 MiB for the worker-thread stacks of the long-lived worker pool, which reserves N = `available_parallelism()` OS-thread stacks on first auto-par call regardless of how many reductions fire — still under rayon's 2.0 MiB. Go's 2.7 MiB carries its GC roots + scheduler arena.

### Compile elapsed (cold)

M5 Pro, 2026-10-31, hyperfine `--warmup 1 --runs 10` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `reverse` | **149.3 ± 1.7 ms** | 87.1 ± 2.7 ms | 47.2 ± 0.8 ms |

`karac build` is now **1.71× slower than `rustc -O`** on this file and 3.16× slower than clang; on the legacy backend (2026-07-28 feed) it was 1.25× of rustc's time, and faster than rustc in the 2026-05-31 snapshot. Go is omitted per BENCH.md — `go build`'s first invocation mixes module resolution + link.

### Binary size

| Implementation | Size |
|---|---|
| c    reverse | 32.7 KiB |
| **kāra reverse (seq)** | **295.8 KiB** |
| kāra reverse (auto-par) | 377.1 KiB |
| rust reverse | 455.6 KiB |
| go   reverse | 2434.1 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); this one is 302,872 B seq (legacy: 34,200 B, at parity with clang) and 386,152 B auto-par. The seq binary is 1.54× under Rust's 455.6 KiB. The auto-par variant carries +81 KiB over seq for the parallel-dispatch machinery.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 reverse.c | 2.6 MiB |
| rustc -O reverse.rs | 26.8 MiB |
| karac build reverse.kara | 57.6 MiB |

`karac` now compiles this file in **~58 MiB peak** — 2.15× rustc's, where the legacy backend sat at 23.8 MiB (2026-07-28 feed), under rustc.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the load-bearing headline for v1 is the **seq-lane codegen-vs-Rust comparison at equal safety — and on the 2026-10-31 re-bench Kāra trails overflow-checked Rust 1.18×** (606.0 vs 512.2 ms; 1.23× against wrapping `-O` Rust, where Kāra pays a safety tax Rust opts out of), with C level with equal-safety Rust and Go 1.06× ahead of Kāra. The residual at equal safety is real — it lives in the per-iteration digit-decompose/reverse path. On top of that per-core baseline, Kāra's auto-concurrency machinery delivers a **language-level 10.5× intra-Kāra speedup** by parallelizing the reduction with no source change — reported separately (above) rather than as a cross-lane "ahead of Rust" number, because `rustc -O` stays single-threaded without a manual `rayon` rewrite and conflating the two lanes would overstate the codegen story; against hand-written rayon the auto-par build trails 1.36×. This is the first kata where that auto-par machinery lights up; the honest framing is *behind the pack on codegen — trailing equal-safety Rust 1.18× this run — plus free safe parallelism where the shape allows*.

## Bug ledger

**Surfaced [`B-2026-10-31-39`](../../../../kara/docs/bugs-v2.md)** (perf, open; filed on kata 9, this kata is its second instance). The default (auto-par) build runs a constant +1.85G instructions over its one-worker count as soon as it has two or more workers (14.02G at 1, 15.88G at 2 to 18), which is why the par lane lost ground on every comparator (1.15× → 1.36× rayon). Measured 31 Oct 2026 with karac g6697158fa.
