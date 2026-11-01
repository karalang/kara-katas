# 6. Zigzag Conversion

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/zigzag-conversion](https://leetcode.com/problems/zigzag-conversion/)

Given a string `s` and an integer `numRows`, write `s` in a zigzag pattern across `numRows` lines and return the string read row-by-row.

```
P   A   H   N
A P L S I I G       "PAYPALISHIRING", numRows = 3   →   "PAHNAPLSIIGYIR"
Y   I   R
```

**Constraints:** `1 ≤ s.length ≤ 1000`, `s` is ASCII (English letters, `','`, `'.'`), `1 ≤ numRows ≤ 1000`. (The kata also exercises `s.length == 0` because the algorithm is well-defined there.)

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Row buffers (visit-by-row) | O(n) time, O(n) space | [`row_buffers.kara`](row_buffers.kara) ✓ via `karac run` / `karac build` | [`row_buffers.py`](row_buffers.py) ✓ |

`✓` runs end-to-end today. Both interpreter and codegen render `println(c)` for a `char` as the UTF-8 glyph; Python mirrors with `print(c)`.

### Why row buffers

Two textbook approaches exist:

1. **Row buffers (this kata).** Walk the input left-to-right, tracking a `cur` row index that bounces between `0` and `numRows - 1`. Each character is appended to its row's `Vec[char]`. After the walk, concatenating the rows row-major yields the answer. O(n) time, O(n) extra space.
2. **Direct math/stride.** For each row `r`, characters in that row sit at positions `r, r + 2(numRows−1), r + 2(numRows−1) − 2r, r + 2(numRows−1), ...` — a two-stride alternating pattern. O(n) time, O(1) extra space (you can write the result directly).

The math/stride form is *constant-factor* better on memory but requires reasoning about two interleaved arithmetic progressions per row, including the special-case handling for the top and bottom rows (which have only one stride, not two). Row buffers express the same algorithm as a one-pass walk with a single direction flag, which is easier to read, easier to test, and matches LeetCode's canonical "Approach 1" almost line for line.

### Why flip direction *before* the step

Flipping before stepping makes the seed state `(cur = 0, going_down = false)` work: on the first iteration we hit `cur == 0`, flip `going_down` to `true`, and step down to row 1. The alternative ("seed `going_down = true`, flip after the step") leaves a subtle off-by-one on the very first step when `numRows == 2`. With the pre-flip ordering the same loop body works for every `numRows ≥ 2` without a special case.

## Kāra features exercised

- **`Vec[Vec[char]]` via `Vec.filled`** — per-row buffers built with `Vec.filled(num_rows, Vec.new())`, which deep-clones the empty inner Vec into each slot; nested-vec indexed access `rows[cur].push(...)` survives the typechecker's element-type pinning. (Until 2026-06-05 this was a manual `Vec.new()` + `push` loop written around a since-fixed `Vec[Vec[T]]` init coercion gap — rewritten during the corpus-wide workaround audit; outputs verified identical under both `karac run` and `karac build`.)
- **`ref String` + `for c in s.chars()`** — read-only string borrow, iterated per Unicode scalar value. Same backbone as katas [#3](../3-longest-substring-without-repeating-characters/) and [#5](../5-longest-palindromic-substring/).
- **`Vec.with_capacity` + `Vec.extend_from_slice`** — the pre-allocated push form mirrors rust's `Vec::with_capacity` + `extend_from_slice` line-for-line. The check-mode short-circuit for `let mut out: Vec[char] = Vec.with_capacity(len)` landed in karac [`092180e`](../../../../karac-rust/) (the synth-mode arm returned `Vec[?T0]` which didn't unify against the declared element type; the new check-mode arm adopts the expected type directly).
- **`if cond or cond` short-circuit** — used in the early-return guard and the rail check.
- **`Vec[char]` indexed read + push** — per-row buffer fills and the flatten loop; bounds checks fire on each indexed read.
- **`println(c)` glyph print** — the char-display arm in `compile_print` routes the i32 codepoint through `karac_string_encode_char` and prints the 1–4 byte UTF-8 sequence.

No `Map`, no `Set`, no shared structs.

## Running

```bash
# Kāra — codegen and interpreter both print glyphs.
karac run   row_buffers.kara
karac build row_buffers.kara && ./row_buffers

# Python
python3 row_buffers.py

# Verify they agree
diff <(./row_buffers) <(python3 row_buffers.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`row_buffers.{kara,rs,c}`, `go-seq/main.go`, plus the par-lane mirrors `row_buffers_par.c`, `go-par/`, `rayon/`). The Python mirror [`bench/row_buffers.py`](bench/row_buffers.py) is gated behind `KARA_BENCH_INCLUDE_PY=1` — at K=10K calls it lands at ~3.2s and would block the bench by default.

Snapshot for every table below unless marked otherwise: Apple M5 Pro (6P+12E), karac `0.9.0-dev.14057+g6697158fa` (the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, go 1.26.3, hyperfine 1.20.0, measured 2026-10-31 (feed `measured_at` 2026-11-01T00:40Z UTC). Source of truth: [`bench/results.json`](bench/results.json).

> **Re-bench 2026-10-31 — what moved.** Quoted as language ratios, because every comparator ran 8–58% slower in absolute terms this session (machine state), so raw milliseconds overstate any Kāra move.
>
> - **Seq lane: Kāra/Rust 1.05× → 1.69×, Kāra/C 1.04× → 1.67×** (previous feed: 2026-07-28, legacy backend). A real MIR-backend regression: MIR executes *fewer* instructions than legacy (2.93 G vs 3.28 G) but takes 1.70× its cycles (731 M vs 431 M). That is the signature filed as [`B-2026-10-31-38`](../../../../kara/docs/bugs-v2.md) — see [Bug ledger](#bug-ledger).
> - **Par lane: Kāra/rayon 0.87× → 1.05×, Kāra/C-pthreads 1.56× → 1.73×** — Kāra no longer beats rayon; the two are now inside each other's error bars.
> - **Binary size: 33.6 → 295.8 KiB (seq)** — see [Binary size](#binary-size).

Per [`../../../BENCH.md`](../../../BENCH.md), the workload's per-call `convert_off` work (one push per input char + one flatten copy = 2N ops, ~20 µs at N=10K) is large enough that the K=10K outer loop's reduction (`sum += result[0] + result[N-1]`) amortizes par-dispatch overhead cleanly — karac's auto-par recognizes the shape and parallelizes the reduction by default. The bench ships two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`row_buffers_kara_seq`** — built with `KARAC_AUTO_PAR=0` (the documented mechanism for side-by-side seq-vs-par benchmarking). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`row_buffers_kara`** — default `karac build` output. Picks up auto-par dispatch (~14 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

Lane verification: the par build's IR carries a call of `karac_mir_task_spawn` and the seq twin's does not, verified in the emitted IR (`KARAC_MIR_LL`).

**Workload.** N = 10,000 ASCII chars from a repeating `"PAYPALISHIRING"` pattern, num_rows = 4, R = 1,000 rotation period, K = 10,000 outer iterations. Per-iter rotation `off = k % R` defeats the cross-iteration CSE that would otherwise hoist the pure `convert_off` call out of the loop. Sink is the sum of (first + last codepoint) across all iterations. All mirrors agree on `1514240` before any timing runs — `bench.sh` fails loudly on mismatch.

| File | What it does |
|---|---|
| [`bench/row_buffers.kara`](bench/row_buffers.kara) | N = 10K, num_rows = 4, R = 1K, K = 10K, rotated 14-char ASCII pattern |
| [`bench/row_buffers.rs`](bench/row_buffers.rs) | Algorithmic mirror; `Vec<char>` per-row buffers; compiled with `rustc -O` and, for the equal-safety row, `rustc -O -C overflow-checks=on` |
| [`bench/row_buffers.c`](bench/row_buffers.c) | Algorithmic mirror; raw `int32_t*` per-row buffers; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `[][]rune` per-row buffers; compiled with `go build` |
| [`bench/row_buffers.py`](bench/row_buffers.py) | Algorithmic mirror — same N, num_rows, R, K, sink |

### Runtime — seq lane

M5 Pro, 2026-10-31, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| rust row_buffers (rustc -O)  | **109.3 ms ± 2.8 ms** | 108.2 ms | 0.59× of Kāra |
| c    row_buffers (clang -O3) | **110.4 ms ± 2.0 ms** | 109.3 ms | 0.60× of Kāra |
| rust row_buffers (rustc -O -C overflow-checks=on, equal-safety) | 115.8 ms ± 3.2 ms | 114.7 ms | 0.63× of Kāra |
| **kāra row_buffers** (`KARAC_AUTO_PAR=0`) | **184.4 ms ± 2.5 ms** | 183.0 ms | **1.00×** (baseline) |
| go   row_buffers             | 337.7 ms ± 2.9 ms      | 342.3 ms | 1.83× of Kāra |

Inner-loop-bound shape: per-iter allocates a `Vec[Vec[char]]` outer + 4 inner `Vec[char]` row buffers, walks N=10K chars distributing into the rails, then flattens via 4 `extend_from_slice` calls into an output `Vec[char]`. **Kāra is 1.69× behind `rustc -O`, 1.67× behind C and 1.59× behind equal-safety Rust**, and still 1.83× ahead of Go. On the legacy backend (2026-07-28 feed) Kāra sat at 1.05× Rust / 1.04× C — near parity, and at dead-even parity in the 2026-06-05 snapshot this section used to quote. The loss is not more work: MIR runs 2.93 G instructions against legacy's 3.28 G, but 731 M cycles against 431 M (1.70×), the instructions-down/cycles-up signature of [`B-2026-10-31-38`](../../../../kara/docs/bugs-v2.md).

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot. All four languages parallelize the same K=10K reduction; the difference is what the programmer wrote. Per BENCH.md's two-lane discipline these rows are not comparable to the seq rows above.

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| c row_buffers (pthreads) | **14.2 ms ± 1.9 ms** | 170.2 ms | ~1218% |
| rust row_buffers (rayon `par_iter`) | 23.3 ms ± 1.9 ms | 323.1 ms | ~1511% |
| **kāra row_buffers** (auto-par on reduction) | **24.5 ms ± 2.2 ms** | 338.7 ms | ~1429% (~14 cores) |
| go row_buffers (goroutines + WaitGroup) | 317.0 ms ± 9.8 ms | 636.6 ms | ~451% |

Karac's auto-par recognizes the `sum +=` reduction in `main`'s K=10K loop and dispatches it across workers, ~14 cores active during the run. **Kāra with zero parallel source is 1.05× rayon — a tie inside both error bars — and 1.73× behind the hand-written C+pthreads mirror**; it was 0.87× rayon on the legacy backend. The wall-time win over the seq-lane Kāra row is **7.5×** (184.4 / 24.5); total CPU time goes up 1.85× (183.0 → 338.7 ms user) as the cost of dispatch + per-worker fixed overhead.

**Not headlined against the seq rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 4× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq lane above is the within-lane comparison; this table is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline.

### Two karac fixes landed for this kata (2026-05-24)

When this kata's bench was first built (2026-05-24) it wouldn't compile, and the auto-par regime would have read 474 MiB peak RSS without intervention. Both surfaced building / running this bench, both shipped before the snapshots here:
When this kata's bench was first built (2026-05-24) it wouldn't compile, and the auto-par regime would have read 474 MiB peak RSS without intervention. Both surfaced building / running this bench, both shipped before the snapshots here:

1. **Typecheck check-mode propagation for `Vec.with_capacity`** (karac [`092180e`](../../../../karac-rust/), 2026-05-24). `let mut out: Vec[char] = Vec.with_capacity(len);` was rejected at typecheck with "expected Vec&lt;char&gt;, found Vec&lt;?T0&gt;": the synth-mode arm returned `Vec[?T]` (fresh typevar) so untyped-let `let v = Vec.with_capacity(8); v.push(x);` could pin from the downstream push, but at an annotated check-mode position the typevar wasn't unified against the declared element type. Latent since the `with_capacity` arm landed; surfaced when the CLI typecheck-error gate added at `db573a4` stopped letting CLI builds proceed past the typechecker. Fix: parallel check-mode arm in `check_expr` adopts the expected type directly, same shape as the existing `Vec.new()` short-circuit.
2. **Per-iteration cleanup frame in `emit_reduce_worker_fn`** (karac [`0567170`](../../../../karac-rust/), 2026-05-24). The first auto-par run of this kata read **498 MiB** peak RSS (322× the seq-lane Kāra row, 333× Rust). Root cause: `emit_reduce_worker_fn` was calling `compile_block(body)` for the loop body without wrapping it in a per-iteration scope frame. Body-local lets like `let result = convert_off(...)` (returning `Vec[char]`) registered drop cleanup against the worker's top frame — pushed once at the start of the worker fn, drained once at `exit_bb` after the loop fully iterated. Effect: only the LAST iteration's `result` ever got freed; every earlier iteration's heap allocation leaked. The seq path correctly pushes a per-iteration frame in `compile_while` / `compile_loop` / `compile_for_range` and drains it via `drain_top_frame_with_emit` before the back-edge; the par_reduce worker now mirrors that discipline. Validated: kata 6 auto-par peak RSS **498 MiB → 5.2 MiB** (~95× reduction); wall time also dropped from 30.7 ms → 23.0 ms because drops now distribute across worker threads instead of serializing at worker exit.

(Note: this is structurally the *same* leak shape as the 2026-05-17 leak in `emit_par_branch_fn` fixed at `daaf2cc` — that one closed a per-iter leak in the `karac_par_run` codegen path; today's fix closes the per-iter leak in the `karac_par_reduce` codegen path. Two codegen paths, same per-iteration-frame discipline.)

### Runtime — long workloads (Python)

Last measured 2026-06-05, not re-run (this run did not set `KARA_BENCH_INCLUDE_PY`); hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py row_buffers` | 3.191 s ± 89 ms |

At that snapshot Python was **31.8× slower** than Kāra codegen on the seq lane (and **141× slower** than the auto-par regime). CPython's per-iter overhead (function-call + `list.append` + per-char bytecode dispatch) dominates, even though Python's underlying `list` is C-implemented.

### Compile elapsed (cold)

M5 Pro, 2026-10-31, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `row_buffers` | **175.1 ms ± 2.4 ms** | 117.9 ms ± 1.8 ms | 47.7 ms ± 1.4 ms |

`karac build` is now **1.48× slower than `rustc -O`** on this file and 3.67× slower than clang; on the legacy backend (2026-07-28 feed) it was 0.94× of rustc's time. Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    row_buffers | 33.0 KiB |
| **kāra row_buffers (seq)** | **295.8 KiB** |
| kāra row_buffers (auto-par) | 377.1 KiB |
| rust row_buffers | 455.8 KiB |
| go   row_buffers | 2434.1 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); this one is 302,920 B seq (legacy: 34,360 B, within ~550 B of clang) and 386,152 B auto-par. The seq binary is 1.54× under Rust's and 9.0× over C's. The auto-par variant carries +81 KiB over seq for the parallel-dispatch machinery.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    row_buffers | 1.2 MiB |
| **kāra row_buffers (seq)** | **1.4 MiB** |
| rust row_buffers | 1.4 MiB |
| c    row_buffers (pthreads) | 2.9 MiB |
| kāra row_buffers (auto-par) | 4.2 MiB |
| rust row_buffers (rayon) | 4.5 MiB |
| py   row_buffers (last measured 2026-06-05, not re-run) | 7.8 MiB |
| go   row_buffers | 10.0 MiB |
| go   row_buffers (goroutines) | 29.1 MiB |

Kāra-seq is at C/Rust parity (within 0.2 MiB). The auto-par variant lands at 4.2 MiB — under rayon's 4.5 MiB — the cost of per-worker stack + per-worker partial accumulator slot + worker-pool initialization, against a workload that allocates K=10K per-call `Vec[Vec[char]]` chains that the per-iteration cleanup frame fix at `0567170` made drop correctly each iteration. Pre-fix this read 498 MiB. Go's 10.0 MiB carries its GC roots + scheduler arena. Python's 7.8 MiB is the CPython interpreter base + the per-char allocations the algorithm builds.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 row_buffers.c | 2.6 MiB |
| rustc -O row_buffers.rs | 31.5 MiB |
| karac build row_buffers.kara | 58.9 MiB |

`karac` now compiles this file in **~59 MiB peak** — 1.87× rustc's 31.5 MiB, where the legacy backend sat at 24.9 MiB (2026-07-28 feed). Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Zigzag Conversion is the "nested-vec allocator pressure + amortizable parallel reduction" entry: each `convert_off` call builds a `Vec[Vec[char]]` outer + 4 inner `Vec[char]` rails + an output `Vec[char]`, then drops all of them at end of call; the K=10K outer loop runs that allocate-walk-flatten-drop cycle 10K times and sums two codepoints out of each result. This is where the seq lane measures per-call allocator + Vec discipline (kara 1.69× behind Rust and 1.67× behind C as of the 2026-10-31 re-bench, ahead of Go by 1.83×; at dead-even parity on the legacy backend) and the auto-par lane measures whether the reduction recognizer can absorb that whole nested-alloc shape cleanly across worker threads without leaking per-iteration heap (4.2 MiB steady-state — at parity with the per-iter allocate-then-drop steady-state footprint the algorithm requires).

## Bug ledger

**Surfaced [`B-2026-10-31-38`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the v2/MIR backend the seq lane went from 1.05× to 1.69× `rustc -O`. MIR runs fewer instructions than legacy here (2.93 G vs 3.28 G) but 1.70× its cycles (731 M vs 431 M): a value stored by the previous loop iteration is reloaded from memory where legacy carried it in a register. Same signature, mechanism verified on kata 64; not verified for this kata's loop.
