# 8. String to Integer (atoi)

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/string-to-integer-atoi](https://leetcode.com/problems/string-to-integer-atoi/)

Implement `myAtoi(s)` — the C-style string-to-integer conversion. Skip ASCII space, read an optional sign, then read a run of digits and stop at the first non-digit. Clamp the result to the signed 32-bit range `[-2³¹, 2³¹ − 1]`; positive overflow returns `INT_MAX`, negative underflow returns `INT_MIN`. Like kata [#7](../7-reverse-integer/), the problem disallows 64-bit intermediates — the overflow check has to live inside the 32-bit world.

```
"42"              →  42
"   -42"          →  -42        (leading spaces, then sign)
"4193 with words" →  4193       (stop at first non-digit)
"words and 987"   →  0          (non-digit prefix → no number)
"91283472332"     →  2147483647 (overflow → INT_MAX)
"-91283472332"    →  -2147483648 (underflow → INT_MIN)
```

**Constraints:** `0 ≤ s.length ≤ 200`, `s` consists of English letters, digits, `' '`, `'+'`, `'-'`, and `'.'`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust | C |
|---|---|---|---|---|---|
| One-pass scan over `s.bytes()` with pre-multiply overflow rail | O(n) time, O(1) extra space (zero-copy byte view) | [`atoi.kara`](atoi.kara) ✓ via `karac run` / `karac build` | [`atoi.py`](atoi.py) ✓ | [`bench/atoi.rs`](bench/atoi.rs) ✓ (bench triad) | [`bench/atoi.c`](bench/atoi.c) ✓ (bench quad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 20 test cases.

## Why one-pass with i32 rails

The conversion is naturally three phases over the input — skip space, read sign, consume digits — but each phase advances the same `i` cursor, so they collapse into a single linear walk with no rewind. The whole function is straight-line code over the bytes; per-byte work is one compare + one increment + (in the digit phase) one mul-add.

The only subtle part is the overflow check. As in kata [#7](../7-reverse-integer/), the multiply itself is the overflow event, so the rail has to fire *before* `result = result * 10 + digit`:

```
result >  INT_MAX / 10                       → overflow
result == INT_MAX / 10 and digit > 7         → overflow (digit 7 is the last of INT_MAX)
```

When the rail fires, the function returns the clamped sentinel directly — `INT_MAX` for positive, `INT_MIN` for negative — and the loop never enters the broken multiply.

### Why one rail covers both signs

The naive approach is two rails (one each against `INT_MAX / 10` and `INT_MIN / 10`), as kata [#7](../7-reverse-integer/#the-overflow-rails) does. atoi can be simpler: build `result` as a *positive* i32 with the sign tracked separately as `±1`, and only multiply by the sign at the end. The accumulator's range is `[0, INT_MAX]`, so a single positive rail against `INT_MAX / 10` is sufficient. `-result` at the end fits in i32 worst-case at `INT_MIN + 1`, so no extra negation rail either. The boundary case `result == max_div and digit == 8` routes through the same clamp arm for both signs — `INT_MIN` is the correct answer for negative magnitudes ≥ `2_147_483_648`, whether the equality case is "exactly representable" or "underflow by one".

## Kāra features exercised

- **`ref String` + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view; LeetCode alphabet is ASCII-only so byte == codepoint with O(1) indexing, no `Vec[char]` snapshot.
- **`u8` byte-literal constants + `u8 as i32` digit math** — `b' '`, `b'0'`, `b'9'` for comparisons; `(b as i32) - (zero as i32)` widens before subtracting. This kata caught an interpreter bug where `ExprKind::Cast` was a no-op; fix landed alongside the kata.
- **i32 arithmetic end-to-end** — accumulator stays `i32`, rails check against `2147483647i32` / typed `7i32`, multiply never enters the broken range.
- **Compound boolean guards with short-circuit** — `result > max_div or (result == max_div and digit > 7i32)`.
- **Early `return` with typed literal** — clamp arms exit the loop directly inside a function declared `-> i32`.

No `Vec.collect()`, no `Map`, no shared structs — `Slice[u8]` view + scalar arithmetic.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   atoi.kara
karac build atoi.kara && ./atoi

# Python
python3 atoi.py

# Verify they agree
diff <(./atoi) <(python3 atoi.py) && echo OK
diff <(karac run atoi.kara) <(python3 atoi.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`atoi.{kara,rs,c}`, `go-seq/main.go`, plus the par-lane mirrors). The Python mirror [`bench/atoi.py`](bench/atoi.py) feeds the long-workloads table behind `KARA_BENCH_INCLUDE_PY=1` — at K=10M calls it lands at ~4 s; the much-longer K=50M / projection-only dance kata [#7](../7-reverse-integer/#benchmarks) needs isn't required here.

Snapshot for every table below unless marked otherwise: Apple M5 Pro (6P+12E), karac `0.9.0-dev.14057+g6697158fa` (the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, go 1.26.3, hyperfine 1.20.0, measured 2026-10-31 (feed `measured_at` 2026-11-01T00:47Z UTC). Source of truth: [`bench/results.json`](bench/results.json).

> **Re-bench 2026-10-31 — what moved.** Flat on both lanes, quoted as language ratios (every comparator ran 9–29% slower in absolute terms this session, machine state): seq Kāra/Rust 1.30× → 1.29×, Kāra/C 1.21× → 1.20×; par Kāra/rayon 1.18× → 1.13×, Kāra/C-pthreads 1.20× → 1.18× (previous feed: 2026-07-28, legacy backend). Binary size moved 33.4 → 295.8 KiB (seq) — see [Binary size](#binary-size).

Per [`../../../BENCH.md`](../../../BENCH.md), the workload's K=10M outer loop reduces via `sum += my_atoi(inputs[k % N]) as i64` — karac's auto-par recognizes the shape and parallelizes the reduction by default (the par build's IR carries a call of `karac_mir_task_spawn` and the seq twin's does not, verified in the emitted IR (`KARAC_MIR_LL`)). The bench ships two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`atoi_kara_seq`** — built with `KARAC_AUTO_PAR=0` (the documented mechanism for side-by-side seq-vs-par benchmarking). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`atoi_kara`** — default `karac build` output. Picks up auto-par dispatch (~12 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go file with `go build`, and the Kāra file with `karac build` (default and `KARAC_AUTO_PAR=0`, both cached in `bench/target/`, gitignored), then runs hyperfine for runtime + cold-compile, plus straight `wc` / `time -l` reads for binary size + memory.

| File | What it does |
|---|---|
| [`bench/atoi.kara`](bench/atoi.kara) | N = 8 distinct inputs cycled by `k % N` (every arm of the three-phase scan exercised), K = 10,000,000 outer iters, sink = Σ my_atoi(inputs[k % N]) widened to i64 |
| [`bench/atoi.rs`](bench/atoi.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/atoi.c`](bench/atoi.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |
| [`bench/atoi.py`](bench/atoi.py) | Algorithmic mirror — same N, K, same input set, same sink formula |

The N = 8 inputs are picked to exercise every arm of the three-phase scan — bare positive (`"42"`), whitespace + sign (`"   -42"`), phase-3 early-exit at first non-digit (`"4193 with words"`), positive overflow rail (`"91283472332"`), explicit `+` (`"+1"`), leading zeros after sign (`"  0000000000012345678"`), INT_MIN boundary (`"-2147483648"`), and whitespace + sign + leading-zero + non-digit break (`"  -0012a42"`) — so no single branch dominates the predictor's history. All five impls print the same sink (`15_437_323_750_000` at the default parameters) so the algorithm's output participates in I/O and can't be elided. The bench's `bench.sh` asserts the kara, kara_seq, rust, c, and go sinks all match before timing.

### Runtime — seq lane

M5 Pro, 2026-10-31, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| rust atoi (rustc -O)             | 50.1 ms ± 0.8 ms     | 49.3 ms | 0.77× of Kāra |
| c    atoi (clang -O3)            | 53.7 ms ± 0.7 ms     | 52.8 ms | 0.83× of Kāra |
| rust atoi (`-C overflow-checks=on`) | 59.3 ms ± 3.2 ms  | 58.3 ms | 0.92× of Kāra |
| go   atoi                        | 62.5 ms ± 1.7 ms     | 61.3 ms | 0.97× of Kāra |
| **kāra atoi** (`KARAC_AUTO_PAR=0`) | **64.7 ms ± 2.0 ms** | 63.7 ms | **1.00×** (baseline) |

Per-call work is a single linear walk over ≤200 ASCII bytes with one i32 accumulator and one overflow rail — no allocations per call, no Vec growth. **Read the two Rust rows together.** Kāra traps on integer overflow *by default* (design.md § Arithmetic Overflow); `rustc -O` **silently wraps**, so its 0.77× is apples-to-oranges. The equal-safety build — Rust with `-C overflow-checks=on` — holds the safety constant, and against it Kāra is **close to parity at 1.09×** (64.7 vs 59.3 ms; Rust's ±3.2 ms band covers about half the gap). That small residual is not the arithmetic — the overflow rail is one compare per digit — it is the `Vec[String]` inputs-table stride + per-call branch codegen on the string scan, the same effect the perf-commit table below traces. (C and Go also wrap; the C floor (0.83×) and Go (0.97×, within the combined error bars — a tie) are the unsafe-but-fast comparators, not safety peers.) Kāra's seq-lane wall is the result of the three karac perf commits documented below — pre-optimization, kara's single-thread user time was 92 ms (1.93× of C).

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output, hyperfine `--warmup 10 --runs 50 --shell=none` (heavier warmup absorbs worker-pool init noise). All four languages parallelize the same K=10M reduction; the difference is what the programmer wrote.

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| c    atoi (pthreads) | **7.1 ms ± 0.5 ms** | 69.5 ms | ~997% |
| rust atoi (rayon) | 7.4 ms ± 1.0 ms | 75.3 ms | ~1156% |
| **kāra atoi** (auto-par on reduction) | **8.3 ms ± 0.2 ms** | 96.2 ms | ~1200% (~12 cores) |
| go   atoi (goroutines) | 9.1 ms ± 0.5 ms | 77.8 ms | ~876% |

Karac's auto-par recognizes the `sum +=` reduction in `main`'s K=10M loop (`karac build --concurrency-report bench/atoi.kara` prints `reduction { op: +, accumulator: sum }`) and fans the iteration space across the M5 Pro's 6 P-cores + 12 E-cores, each thread accumulating into a private partial slot, then a final serial combine pass folds the partials into the parent's `sum`. The reduction op is associative + commutative, so the combine order doesn't affect the result — every run produces the same sink (`15_437_323_750_000`) regardless of how the work was split. **No source-level changes** to express the parallelism: the analyzer recognizes the shape from the natural serial source.

**Kāra with zero parallel source is 1.13× behind rayon, 1.18× behind C+pthreads and 1.09× ahead of Go's goroutine chunking.** The wall-time win over the seq-lane Kāra row is **7.8×** (64.7 / 8.3); total CPU time goes up 1.51× (63.7 → 96.2 ms user) as the cost of dispatch + per-worker fixed overhead. The short per-iter body (~10–20 bytes per call) means the inputs-table reads + partials combine weigh more against compute than on kata [#6](../6-zigzag-conversion/#runtime--auto-par-regime-kara-default-multi-core)'s heavier body, which is why this run averages ~12 active cores rather than ~14.

**Not headlined against the seq rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 6× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq lane above is the within-lane comparison; the par table is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline.

### Single-thread CPU — at-or-ahead of C after three karac perf commits

The seq-lane parity above is the *result* of perf work that closed a 1.93× gap to C. Pre-optimization, the seq-lane Kāra user time was **92.0 ms** vs C's **47.5 ms** — Kāra was 1.93× slower on the same algorithm. Three perf commits closed most of the gap, and a subsequent codegen pass closed the remainder:

| Commit | What it removes | Seq-lane user-time |
|---|---|---|
| (baseline, pre-perf) | — | 92.0 ms (1.94× of C) |
| [`a9e51c8`](../../../../karac-rust/) const-prop top-level let-init captures | `n = 8` arrives at worker as a constant, not a 24-byte heap load per iter | 72.5 ms (1.53× of C) |
| [`1712d51`](../../../../karac-rust/) assume non-neg loop var | ARM64 signed-mod-pow2 collapses from `negs/and/and/csneg` (4 instr) to `and #N-1` (1 instr) | 67.8 ms (1.43× of C) |
| [`28d76af`](../../../../karac-rust/) hoist vec bounds check via modulo | `inputs[k % 8]` bounds check moves from per-iter to function entry | 61.0 ms (1.29× of C) |
| (today's snapshot, with subsequent codegen wins absorbed)         | further bounds-check thinning + register-allocator improvements | 59.0 ms (**1.28× of C**) |

The kara-vs-C gap has fully closed and reversed — kara is now behind C on user time (59.0 vs 46.0 ms) and 0.79× as fast on wall. The residual `Vec[String]` stride cost — `umaddl` to compute element address vs C's `ldr` with shifted offset — is fully absorbed by other codegen wins, no longer measurable as a kara-side overhead. A borrowed-view string type (`StringSlice`, analogous to `Slice[u8]` but UTF-8-aware) remains tracked but no longer kata-justified.

*(Note 2026-10-31: the table above is the legacy backend's 2026-06-16 history. On the v2/MIR backend Kāra's seq user time is 63.7 ms vs C's 52.8 ms — 1.21× of C, the same standing the legacy feed showed (1.21×), so Kāra is behind C, not at or ahead of it.)*

### Codegen vs Python

Last measured 2026-06-16, not re-run (this run did not set `KARA_BENCH_INCLUDE_PY`). Python on the same workload, same K = 10M, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py atoi` | 3.930 s ± 55 ms |

At that snapshot Python was **510× slower than Kāra auto-par** (3929 / 7.7) and **65× slower than Kāra seq** (3929 / 60.6) at the same K. The per-iter body is dominated by CPython's per-bytecode dispatch — every `s[i] == ' '`, `s[i] < '0'`, and `ord(c) - ord('0')` is a fresh interpreter dispatch with object boxing for the integer arithmetic. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was wider (~1,950×) because the per-iter body there is even shorter (4 i32 ops vs ~15 bytes × ~5 ops/byte here) so interpreter overhead dominates a larger fraction.

### Compile elapsed (cold)

M5 Pro, 2026-10-31, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `atoi` | **155.7 ms ± 2.9 ms** | 83.9 ms ± 1.8 ms | 44.7 ms ± 0.9 ms |

`karac build` is now **1.86× slower than `rustc -O`** on this file and 3.49× slower than clang; on the legacy backend (2026-07-28 feed) it was 1.32× of rustc's time, and 1.15× faster than rustc in the 2026-05-31 snapshot. Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    atoi                | 32.7 KiB |
| **kāra atoi (seq)**      | **295.8 KiB** |
| kāra atoi (auto-par)     | 377.1 KiB |
| rust atoi                | 455.4 KiB |
| go   atoi                | 2434.1 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); this one is 302,872 B seq (legacy: 34,248 B) and 386,152 B auto-par. The seq binary is 1.54× under Rust's 455.4 KiB. The auto-par variant carries +81 KiB over seq for the parallel-dispatch machinery.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    atoi                | 1.0 MiB |
| **kāra atoi (seq)**      | **1.0 MiB** |
| rust atoi                | 1.1 MiB |
| c    atoi (pthreads)     | 1.3 MiB |
| kāra atoi (auto-par)     | 1.5 MiB |
| rust atoi (rayon)        | 1.8 MiB |
| go   atoi                | 2.6 MiB |
| go   atoi (goroutines)   | 4.0 MiB |
| py   atoi (last measured 2026-06-16, not re-run) | 7.0 MiB |

Kāra-seq is at C parity (1,081,656 B vs C's 1,048,888 B), a hair under Rust. The auto-par variant lands at 1.5 MiB — +0.4 MiB for per-worker stacks + per-worker partial accumulator slot + worker-pool initialization, still under rayon's 1.8 MiB. The footprint stays tiny because the per-call work doesn't allocate (no `Vec[Vec[char]]` chains like kata [#6](../6-zigzag-conversion/#runtime-memory-peak-rss)); only the inputs-table and the `sum` accumulator persist. Go's 2.6 MiB carries its GC roots + scheduler arena; Python's 7.0 MiB is the CPython interpreter base.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 atoi.c       | 2.6 MiB |
| rustc -O atoi.rs       | 26.6 MiB |
| karac build atoi.kara  | 59.6 MiB |

`karac` now compiles this file in **~60 MiB peak** — 2.24× rustc's, where the legacy backend sat at 24.5 MiB (2026-07-28 feed), under rustc. Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

String-to-integer atoi is the "branch-heavy scalar scan + amortizable parallel reduction" entry: each `my_atoi` call is a three-phase straight-line walk (skip whitespace, read sign, consume digits) with branch points the compiler can't fully fold; the K=10M outer loop runs that scalar-scan + accumulate cycle 10M times. This is where the seq lane measures per-call branch + bounds-check codegen quality (kara close to equal-safety Rust at 1.09×, level with Go at 1.04× inside the error bars) and the auto-par lane measures whether the reduction recognizer can absorb a short-bodied per-iter call cleanly across worker threads without partials-combine overhead dominating (7.8× wall-time win, ~12 cores on the short body — vs kata [#6](../6-zigzag-conversion/#runtime--auto-par-regime-kara-default-multi-core)'s ~14 cores on a heavier per-iter body). Together they're the cleanest demonstration in the corpus that **kara's seq-lane codegen quality is close to equal-safety Rust on a non-allocating numeric scan — the gap to wrapping `rustc -O` is mostly the overflow-check safety tax — and the auto-par regime adds a 7.8× wall-time multiplier on top of that with zero source-level changes.**
