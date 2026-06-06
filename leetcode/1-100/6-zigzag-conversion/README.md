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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`row_buffers.{kara,rs,c}`, `go-seq/main.go`). The Python mirror [`bench/row_buffers.py`](bench/row_buffers.py) is gated behind `KARA_BENCH_INCLUDE_PY=1` — at K=10K calls it lands at ~3.3s and would block the bench by default.

Per [`../../../BENCH.md`](../../../BENCH.md), the workload's per-call `convert_off` work (one push per input char + one flatten copy = 2N ops, ~20 µs at N=10K) is large enough that the K=10K outer loop's reduction (`sum += result[0] + result[N-1]`) amortizes par-dispatch overhead cleanly — karac's auto-par-on-reduction recognizes the shape and emits a `karac_par_reduce` dispatch by default. The bench ships two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`row_buffers_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`row_buffers_kara`** — default `karac build` output. Picks up auto-par dispatch (~14 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** N = 10,000 ASCII chars from a repeating `"PAYPALISHIRING"` pattern, num_rows = 4, R = 1,000 rotation period, K = 10,000 outer iterations. Per-iter rotation `off = k % R` defeats the cross-iteration CSE that would otherwise hoist the pure `convert_off` call out of the loop. Sink is the sum of (first + last codepoint) across all iterations. All five mirrors agree on `1514240` before any timing runs — `bench.sh` fails loudly on mismatch.

| File | What it does |
|---|---|
| [`bench/row_buffers.kara`](bench/row_buffers.kara) | N = 10K, num_rows = 4, R = 1K, K = 10K, rotated 14-char ASCII pattern |
| [`bench/row_buffers.rs`](bench/row_buffers.rs) | Algorithmic mirror; `Vec<char>` per-row buffers; compiled with `rustc -O` |
| [`bench/row_buffers.c`](bench/row_buffers.c) | Algorithmic mirror; raw `int32_t*` per-row buffers; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `[][]rune` per-row buffers; compiled with `go build` |
| [`bench/row_buffers.py`](bench/row_buffers.py) | Algorithmic mirror — same N, num_rows, R, K, sink |

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| **kāra row_buffers** (`KARAC_AUTO_PAR=0`) | **99.2 ms ± 5.4 ms** | 96.8 ms | **1.00×** (baseline) |
| rust row_buffers (rustc -O)  | **100.0 ms ± 0.7 ms** | 98.2 ms | 1.01× of Kāra |
| c    row_buffers (clang -O3) | **102.0 ms ± 7.5 ms** | 98.6 ms | 1.03× of Kāra |
| go   row_buffers             | 248.4 ms ± 4.9 ms      | 287.2 ms | 2.50× of Kāra |

Inner-loop-bound shape: per-iter allocates a `Vec[Vec[char]]` outer + 4 inner `Vec[char]` row buffers, walks N=10K chars distributing into the rails, then flattens via 4 `extend_from_slice` calls into an output `Vec[char]`. **Kāra, Rust and C are at dead-even parity** (all three means within ~3 ms and overlapping σ), and Kāra is 2.5× faster than Go. The 2026-05-31 snapshot had C/Rust ~6% ahead (Kāra 105.7 ms, user-CPU 104.2 ms); the gap closed in the 2026-05-31 → `a3acedaf` karac window, *not* via the `Vec.filled` source rewrite — an A/B of the old manual-push-loop shape rebuilt with current karac measures the two shapes statistically indistinguishable, and the rust/c comparator binaries are byte-identical (not rebuilt) across both snapshots, so the −7 ms Kāra user-CPU move is a karac/runtime codegen improvement from that window.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra row_buffers** (auto-par on reduction) | **23.3 ms ± 1.0 ms** | 302.0 ms | ~1296% (~13 cores) |

Karac's auto-par-on-reduction recognizes the `sum +=` reduction in `main`'s K=10K loop and emits a `karac_par_reduce` dispatch — binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~13 cores active during the run. The wall-time win over the seq-lane Kāra row is **4.3×** (99.2 / 23.3); total CPU time goes up 3.1× (96.8 → 302.0 ms user) as the cost of dispatch + per-worker fixed overhead.

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 4× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq lane above is the within-lane comparison; this row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline.

### Two karac fixes landed for this kata (2026-05-24)

When this kata's bench was first built (2026-05-24) it wouldn't compile, and the auto-par regime would have read 474 MiB peak RSS without intervention. Both surfaced building / running this bench, both shipped before the snapshots here:

1. **Typecheck check-mode propagation for `Vec.with_capacity`** (karac [`092180e`](../../../../karac-rust/), 2026-05-24). `let mut out: Vec[char] = Vec.with_capacity(len);` was rejected at typecheck with "expected Vec&lt;char&gt;, found Vec&lt;?T0&gt;": the synth-mode arm returned `Vec[?T]` (fresh typevar) so untyped-let `let v = Vec.with_capacity(8); v.push(x);` could pin from the downstream push, but at an annotated check-mode position the typevar wasn't unified against the declared element type. Latent since the `with_capacity` arm landed; surfaced when the CLI typecheck-error gate added at `db573a4` stopped letting CLI builds proceed past the typechecker. Fix: parallel check-mode arm in `check_expr` adopts the expected type directly, same shape as the existing `Vec.new()` short-circuit.
2. **Per-iteration cleanup frame in `emit_reduce_worker_fn`** (karac [`0567170`](../../../../karac-rust/), 2026-05-24). The first auto-par run of this kata read **498 MiB** peak RSS (322× the seq-lane Kāra row, 333× Rust). Root cause: `emit_reduce_worker_fn` was calling `compile_block(body)` for the loop body without wrapping it in a per-iteration scope frame. Body-local lets like `let result = convert_off(...)` (returning `Vec[char]`) registered drop cleanup against the worker's top frame — pushed once at the start of the worker fn, drained once at `exit_bb` after the loop fully iterated. Effect: only the LAST iteration's `result` ever got freed; every earlier iteration's heap allocation leaked. The seq path correctly pushes a per-iteration frame in `compile_while` / `compile_loop` / `compile_for_range` and drains it via `drain_top_frame_with_emit` before the back-edge; the par_reduce worker now mirrors that discipline. Validated: kata 6 auto-par peak RSS **498 MiB → 5.2 MiB** (~95× reduction); wall time also dropped from 30.7 ms → 23.0 ms because drops now distribute across worker threads instead of serializing at worker exit.

(Note: this is structurally the *same* leak shape as the 2026-05-17 leak in `emit_par_branch_fn` fixed at `daaf2cc` — that one closed a per-iter leak in the `karac_par_run` codegen path; today's fix closes the per-iter leak in the `karac_par_reduce` codegen path. Two codegen paths, same per-iteration-frame discipline.)

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py row_buffers` | 3.313 s ± 142 ms |

Python is **33.4× slower** than Kāra codegen on the seq lane (and **142× slower** than the auto-par regime). CPython's per-iter overhead (function-call + `list.append` + per-char bytecode dispatch) dominates, even though Python's underlying `list` is C-implemented.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `row_buffers` | **75.6 ms ± 0.9 ms** | 106.0 ms ± 1.2 ms | 44.3 ms ± 1.1 ms |

`karac build` is **1.40× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). The mid-day `a3acedaf` install had karac at 79.8 ms; the evening `3f3b34a9` install reads 75.6 — both inside the recurring reinstall-day band (~75–86 ms across the corpus; binaries unaffected, see the drift-watch close-out in the karac trackers), with rustc/clang drifting −4/−2.5 ms on byte-identical inputs across the same window. Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    row_buffers | 33.0 KiB |
| **kāra row_buffers (seq)** | **33.0 KiB** |
| kāra row_buffers (auto-par) | 295.9 KiB |
| rust row_buffers | 455.8 KiB |
| go   row_buffers | 2434.1 KiB |

**Within 24 bytes of clang (33,832 B vs 33,808 B).** The seq-lane binary spent part of 2026-06-05 at 49.3 KiB: karac's phase-9 contract-fault categorization (`8183f6c7`) made every panic site (including bounds checks) reference `karac_runtime_panic_prefix`, whose thread-local data dragged one page-aligned writable 16 KiB `__DATA` segment into every binary — even contract-free ones. This kata's re-bench was the *first* instance measured (bisected via the pre-`a3acedaf` backup karac: 33,872 B old vs 50,496 B regressed, same source); katas [#88](../88-merge-sorted-array/README.md) and [#5](../5-longest-palindromic-substring/README.md) confirmed it the same day, and kata #5 showed the same panic-site change also cost **runtime** on bounds-check-hot loops. The same-day karac fix (`3f3b34a9`) folds the fault prefix static for contract-free programs (the page dead-strips) and outlines panic bodies (kata #5's 1.34× restored); this evening's rebuild reads **33,832 B** — the lean floor, back. The auto-par variant is unchanged at 295.9 KiB — it grows +246 KiB over seq to carry the par_reduce machinery (per-branch trampolines + reduction-combine globals + worker-pool registration), the same ballast kata [#4](../4-median-of-two-sorted-arrays/#binary-size) carries for the same auto-par mechanism. Here the ballast is paid for in a real 4.3× wall-time win, so it stays in.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    row_buffers | 1.3 MiB |
| **kāra row_buffers (seq)** | **1.5 MiB** |
| rust row_buffers | 1.5 MiB |
| kāra row_buffers (auto-par) | 5.3 MiB |
| py   row_buffers | 7.5 MiB |
| go   row_buffers | 10.7 MiB |

Kāra-seq is at C/Rust parity (within 0.2 MiB). The auto-par variant lands at 5.3 MiB — the cost of per-worker stack + per-worker partial accumulator slot + worker-pool initialization, against a workload that allocates K=10K per-call `Vec[Vec[char]]` chains that the per-iteration cleanup frame fix at `0567170` now drops correctly each iteration. Pre-fix this read 498 MiB. Go's 10.7 MiB carries its GC roots + scheduler arena. Python's 7.5 MiB is the CPython interpreter base + the per-char allocations the algorithm builds.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 row_buffers.c | 2.5 MiB |
| karac build row_buffers.kara | 12.3 MiB |
| rustc -O row_buffers.rs | 31.6 MiB |

`karac` compiles this file in **~12 MiB peak** — between clang and rustc, with no algorithmic blowup signature. The +1.7 MiB vs the 2026-05-31 snapshot (10.6 MiB) is the same karac-only fixed-floor growth band every reinstall day shows (rustc/clang flat on unchanged sources; emitted code unaffected — probe-confirmed pattern, see the corpus drift-watch close-out). Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Zigzag Conversion is the "nested-vec allocator pressure + amortizable parallel reduction" entry: each `convert_off` call builds a `Vec[Vec[char]]` outer + 4 inner `Vec[char]` rails + an output `Vec[char]`, then drops all of them at end of call; the K=10K outer loop runs that allocate-walk-flatten-drop cycle 10K times and sums two codepoints out of each result. This is where the seq lane measures per-call allocator + Vec discipline (kara at dead-even parity with C/Rust as of the 2026-06-05 snapshot, ahead of Go by 2.5×) and the auto-par lane measures whether the reduction recognizer can absorb that whole nested-alloc shape cleanly across worker threads without leaking per-iteration heap (5.3 MiB steady-state post-`0567170` — at parity with the per-iter allocate-then-drop steady-state footprint the algorithm requires).
