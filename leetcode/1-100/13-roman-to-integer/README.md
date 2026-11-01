# 13. Roman to Integer

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table, Math, String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/roman-to-integer](https://leetcode.com/problems/roman-to-integer/)

Convert a Roman numeral in `[1, 3999]` back to its integer value. The seven base symbols are `I, V, X, L, C, D, M` for `1, 5, 10, 50, 100, 500, 1000`. The system encodes `4` and `9` in each place via subtractive pairs: `IV`, `IX`, `XL`, `XC`, `CD`, `CM` — when a smaller symbol precedes a larger one, the smaller value is subtracted.

```
"III"              → 3
"IV"               → 4
"IX"               → 9
"LVIII"            → 58       (50 + 5 + 3)
"MCMXCIV"          → 1994     (1000 + 900 + 90 + 4)
"MMMDCCCLXXXVIII"  → 3888     (15 chars — the longest valid input)
"MMMCMXCIX"        → 3999     (LeetCode upper bound)
```

**Constraints:** `1 ≤ s.length ≤ 15`, characters drawn from `{I, V, X, L, C, D, M}`, and `s` is a valid Roman numeral in `[1, 3999]`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Forward scan + lookahead | O(n) time, O(1) space | [`greedy.kara`](greedy.kara) ✓ via `karac run` / `karac build` | [`greedy.py`](greedy.py) ✓ | [`bench/greedy.rs`](bench/greedy.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 12 test cases.

## Why forward-scan with lookahead

The standard parse strategy walks the input left-to-right and decides at each position whether the current symbol *adds* or *subtracts*. The rule is one comparison against the next byte: if `value[s[i]] < value[s[i+1]]`, we're inside a subtractive pair and the current value is negated; otherwise it adds.

```
for i in 0..n:
    cur = value(s[i])
    if i + 1 < n and cur < value(s[i + 1]):
        total -= cur            ← subtractive prefix (IV, IX, XL, XC, CD, CM)
    else:
        total += cur            ← additive
```

This expresses the LeetCode subtractive-pair rule directly as a one-line predicate instead of branching on every possible two-character prefix (six explicit cases × seven additive cases = 42 patterns). The value lookup itself is unrolled into seven byte-equality checks against the fixed `{I, V, X, L, C, D, M}` alphabet — no hash map, no associative array.

Per-call worst case (LeetCode bound `n ≤ 15`): 15 × 7 = 105 byte comparisons, plus 15 lookahead checks. Per-call mean over the full `1..3999` sweep: ~9.5 chars and ~67 byte comparisons. No nested loops, no auxiliary buffers, no allocations beyond the input view.

This is the same shape LeetCode's "Approach 2" reference uses (the textbook "Approach 1" walks the input in reverse with a running max, which expresses the same rule less directly). Both compile to roughly the same straight-line code; the forward-scan form makes the subtractive-pair rule visible as a single predicate that the optimizer can hoist cheaply.

## Kāra features exercised

- **`s.bytes()` returning a `Slice[u8]`** — zero-copy view over the `String`'s storage with O(1) byte-positional access. Single-byte ASCII for all seven Roman symbols, so the byte view is exact and never needs a `Vec[char]` snapshot. Same primitive kata [#8](../8-string-to-integer-atoi/) (atoi) uses for its left-to-right digit scan.
- **`b'I'`-style byte literals + `b == b'I'` byte equality** — the seven-way value lookup is seven byte-equality checks; no `match` on chars, no string comparison, no hash. Same lowering as kata [#8](../8-string-to-integer-atoi/)'s sign-check and digit-range tests.
- **`i + 1i64 < n` lookahead guard in a `while` loop** — Kāra's `i64`-throughout discipline keeps the index, the bound check, and the lookahead offset all in the same width; no `usize` round-trip across the bounds check. Same `i64`-throughout shape kata [#11](../11-container-with-most-water/) leans on.
- **`Vec[char]` per-call allocation in the bench's input generator** — the bench reuses kata [#12](../12-integer-to-roman/)'s `int_to_roman` greedy as a per-iter input source, producing a fresh `Vec[char]` with capacity 15 that `roman_to_int` then parses. The per-iter alloc/drop discipline carries over end-to-end.
- **`sum = sum + roman_to_int(r)` reduction in the bench's outer loop** — the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch.
- **Per-iter `Vec[char]` allocate-then-drop discipline in the auto-par worker** — each worker iteration builds + drops a fresh `Vec[char]`; the per-iteration cleanup-frame fix in karac [`0567170`](../../../../karac-rust/) (landed 2026-05-24 against kata #6's leak) is what keeps this kata's auto-par peak RSS bounded.

No `Map`, no `Set`, no shared structs. The educational source uses `String` only as the `s: ref String` input parameter; the bench substitutes `Vec[char]` for the input view to fuse with the kata #12 generator.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   greedy.kara
karac build greedy.kara && ./greedy

# Python
python3 greedy.py

# Verify they agree
diff <(./greedy) <(python3 greedy.py) && echo OK
diff <(karac run greedy.kara) <(python3 greedy.py) && echo OK
```

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **6%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **1.4%** margin against `rustc -O` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`greedy.{kara,rs,c,py}`, `go-seq/main.go`, and the par-lane mirrors `rayon/`, `go-par/`, `greedy_par.c`).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + roman_to_int(r)` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`greedy_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build.
- **`greedy_kara`** — default `karac build` output. Picks up auto-par dispatch (~13 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** K = 10,000,000 outer iters. Per iter: an LCG-shaped `num` in `[1, 3999]` (`(k * 2654435769 + 305419896) mod 3999 + 1`) is converted to Roman by the same unrolled greedy from kata [#12](../12-integer-to-roman/) (the *input generator*), then `roman_to_int` walks the resulting `Vec[char]` and reconstructs the i64 (the *function under measurement*). End-of-iter `Vec` drop. Because the generator and the parser are exact inverses on `[1, 3999]`, the running `sum` of reconstructed values equals the running sum of the LCG-drawn `num`s — a self-checking sink: if either direction has a bug, all five mirrors will disagree. Sink = `19989996724`. The LCG spread defeats branch-predictor memorization on both halves of the per-iter work (generator and parser see every possible decimal pattern across the run rather than a small fixed rotation). All five compiled mirrors agree on the sink before any timing runs; `bench.sh` fails loudly on mismatch.

This is a *fused* kata #12 + #13 workload: roughly 2× the per-iter algorithmic work of kata #12 (generate-then-parse rather than generate-then-sum-codepoints), against the same per-iter allocator-tax cost from the shared `Vec[char]` discipline.

### Runtime — seq lane (apples-to-apples, single-threaded)

M5 Pro, measured 2026-10-31 with karac `g6697158fa` (the v2/MIR backend; [`bench/results.json`](bench/results.json) `measured_at` 2026-11-01T00:54Z UTC), hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | Within-lane ratio |
|---|---|---|---|
| go   greedy | 365.9 ms ± 2.7 ms | 366.6 ms (+72.8 ms system) | 0.88× of Kāra |
| rust greedy (overflow-checks=on) | 400.9 ms ± 12.4 ms | 398.2 ms | 0.97× of Kāra |
| rust greedy (rustc -O) | 409.1 ms ± 11.6 ms | 406.6 ms | 0.99× of Kāra |
| **kāra greedy** (`KARAC_AUTO_PAR=0`) | **414.8 ms ± 12.5 ms** | 412.3 ms | **1.00×** (baseline) |
| c    greedy (clang -O3) | 445.4 ms ± 11.4 ms | 442.6 ms | 1.07× of Kāra |

**Kāra no longer leads the seq lane on this *fused* workload; it ties Rust and is ~7% ahead of C.** Kāra takes **1.13× Go's time**, is **1.01× behind `rustc -O`** (a 1.4% margin, inside the 6% placement spread above) and **1.03× behind `rust -C overflow-checks=on`**, and runs **0.93× C's time**. The Rust/Kāra σ are ~12 ms, so their order is not resolved by this run; C last is. Go's 120% CPU (user + system 439 ms against 366 ms wall) is GC and scheduler work on other cores. Against the previous feed (legacy backend, 2026-07-28) the seq ratios are flat — Kāra/Rust 1.01× → 1.01×, Kāra/C 0.94× → 0.93×, Kāra/Go 1.24× → 1.13× (under the 10% noise band); every comparator ran 5–16% slower this session (machine state), so compare ratios, not ms. *(History, 2026-06-05 legacy snapshot: Kāra led by ~7% over Rust, ~0% over Go and ~12% over C; the Kāra-first ordering had already gone by the 2026-07-28 feed.)* The headline against C needs unpacking, because the mechanism is not what it looks like.

The fused workload is two kernels back to back: `int_to_roman` (the generator) emits a `Vec[char]`, then `roman_to_int` (the parser) reads it back. Profiling each separately (see *Mechanism* below) shows **Kāra's lead over C comes entirely from the generator, and Kāra is actually slightly *slower* than C on the parser** — the kernel this kata is named for.

#### Mechanism — where the 84 ms gap over C actually comes from

The kata #12 README originally attributed Kāra's lead to "Kāra's path through libsystem `_malloc` / `_free` landing at the favorable end of the spread for small-Vec churn." **That was wrong, and is corrected here and in kata #12.** A `DYLD_INSERT_LIBRARIES` malloc-counting shim against both binaries shows Kāra and C make *byte-identical* allocator calls:

| | Kāra-seq | C |
|---|---|---|
| malloc calls | 10,000,028 | 10,000,028 |
| free calls | 10,000,014 | 10,000,014 |
| 60-byte allocs (the hot path) | 10,000,000 | 10,000,000 |

Same count, same 60-byte size class, same totals. There is no allocator-path difference. The real mechanism is in the **generator's algorithmic codegen**: clang -O3 rewrites `int_to_roman`'s `while (n >= 1000) { push 'M'; n -= 1000; }` into Barrett-reduction division by constant plus a `memset_pattern16` bulk-fill call (4 such call sites in the C binary; 0 in Kāra). For the 1–12 byte fills typical of this kata (mean Roman length ~9.5), `memset_pattern16`'s ~3–5 ns cross-module call overhead **exceeds** the inline-store cost — so clang's "optimization" is a pessimization, and Kāra wins by lowering the loop literally and *not* applying that transform.

(Dating note: the "84 ms" in this section's title is the 2026-05-27 fused-lane gap, 372.6 − 288.6; at the 2026-06-05 snapshot the gap is ~36 ms (349.3 − 313.0), the C row having shed its load-inflated outliers. The per-phase breakdown below is from the 2026-05-27 shim/diagnostic session — its absolute ns/iter values carry that snapshot's C wall time, but the *shape* (allocator identical, generator pessimized in C, parser slightly faster in C) is what the section establishes, and that is batch-independent.) On the 2026-10-31 MIR feed the fused-lane gap is ~31 ms (445.4 − 414.8); the per-phase breakdown has not been re-measured on MIR.

Corrected per-iter cost breakdown (all three rows confirmed by the shim + a parse-only diagnostic):

| Phase | Kāra | C |
|---|---|---|
| Allocator round-trip (identical call shape) | ~14.8 ns / iter | ~14.8 ns / iter |
| `int_to_roman` (generator) | ~6 ns / iter | ~14 ns / iter — clang's `memset_pattern16` pessimization |
| `roman_to_int` (parser) | ~8.5 ns / iter | ~7.85 ns / iter — **C wins** |

So the honest framing: **on the parser kernel, C edges Kāra by ~8%, as you'd expect of a mature optimizer. Kāra leads the fused wall only because clang over-zealously vectorizes the generator's small subtract-loops.** That's a real and reproducible observation about clang's heuristics at this output size — not a claim that Kāra's codegen is categorically faster.

#### Parse-only diagnostic

To isolate the parser, a variant pre-stakes two `Vec[char]` inputs outside the timed loop (alternated by `k % 2` to defeat constant-folding) and runs 10M `roman_to_int` calls with **no per-iter allocation**:

| Implementation | Wall time | Ratio |
|---|---|---|
| c parse-only (clang -O3) | **78.5 ms ± 1.1 ms** | **1.00×** (baseline) |
| kāra parse-only (seq) | 85.0 ms ± 2.3 ms | 1.08× of C |

This is the parser kernel's true cross-language order: C ahead by 8%. (The single-input version of this diagnostic ran in 1.9 ms for C because clang constant-folds the whole loop into one multiply — karac does not do that loop-invariant motion across pure calls, which is its own minor codegen gap.)

Every σ in the 2026-10-31 fused table is ≤ 12.5 ms (Go's 2.7 ms tightest). What persists on this machine is batch-level drift of a few % on byte-identical binaries (see kata [#12](../12-integer-to-roman/)'s batch-variance note), which is why the 1.4% Kāra/Rust margin is a tie. The 2026-06-05 ordering — Kāra first — no longer reproduces on the current feed: Go leads, Rust and Kāra tie, C is last.

### Runtime — auto-par regime (kara default, multi-core)

Same session, default `karac build` output against in-lane parallel comparators (`rayon::par_iter`, C pthreads, goroutines + WaitGroup over the same outer reduction), hyperfine `--runs 50`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust greedy (rayon `par_iter`) | **53.8 ms ± 5.4 ms** | 851.4 ms | ~1605% |
| **kāra greedy** (auto-par on reduction) | **59.2 ms ± 4.0 ms** | 787.5 ms | ~1340% (~13.4 cores) |
| c    greedy (pthreads) | **61.1 ms ± 6.1 ms** | 873.1 ms | ~1434% |
| go   greedy (goroutines + WaitGroup) | **235.3 ms ± 2.7 ms** | 688.3 ms (+545.2 ms system) | ~524% |

Karac's auto-par-on-reduction recognizes the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch — verified in the emitted IR (`KARAC_MIR_LL`): the default build carries a call of `karac_mir_task_spawn` and the `KARAC_AUTO_PAR=0` twin does not. Within the par lane Kāra is **1.10× behind rayon**, **0.97× C pthreads' time** (a tie inside σ), and **4.0× ahead of Go**. Against the 2026-07-28 feed that is slightly better: Kāra/rayon 1.20× → 1.10×, Kāra/C 0.96× → 0.97× (flat), Kāra/Go 0.37× → 0.25×.

The wall-time win *over the seq-lane Kāra row above* is **7.0×** (414.8 / 59.2); total CPU time goes up 91% (412.3 → 787.5 ms user) as the cost of dispatch + per-worker fixed overhead. *(History, 2026-06-05 legacy snapshot: 28.1 ms at ~13.9 cores, 11.1× over seq, +26% user CPU.)*

The per-iter alloc/drop discipline holds under auto-par: each worker thread builds + drops its own `Vec[char]` per iteration, the per-iteration cleanup-frame fix in karac [`0567170`](../../../../karac-rust/) keeps the per-worker heap from growing unbounded. Peak RSS under auto-par (1.8 MiB) sits just 0.8 MiB above the seq lane — the small-Vec allocator path scales cleanly across workers.

**Not headlined against the seq-lane C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 7.5× faster than C" by setting the auto-par row against C's seq row would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the par table above is the in-lane parallel comparison, where Kāra gets its parallelism as a *language-level* choice (no source-level annotation; the analyzer recognizes the natural serial reduction) and the comparators write it by hand.

### Codegen vs Python

CPython at K = 1M takes **939.2 ± 3.2 ms** (single-core; last measured 2026-06-05, not re-run — this re-bench did not set `KARA_BENCH_INCLUDE_PY`); projected to K = 10M that's ~9.39 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~23× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~159× faster). Those ratios set the 2026-06-05 Python figure against the 2026-10-31 Kāra rows, so they are cross-session. The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Same session, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `greedy` | **189.8 ± 1.8 ms** | 106.0 ± 1.2 ms | 54.7 ± 1.4 ms |

Karac is **1.79× slower than rustc -O** and **3.47× slower than clang -O3**. *(History, 2026-06-05, legacy backend: karac compiled in 88.9 ms, 1.21× faster than rustc -O and 1.69× slower than clang -O3.)* Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    greedy | 33,576 | 32.8 |
| **kāra greedy (seq)** | **302,872** | **295.8** |
| kāra greedy (auto-par) | 386,152 | 377.1 |
| rust greedy | 466,584 | 455.6 |
| go   greedy | 2,492,578 | 2,434.2 |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger `B-2026-10-28-36`); the seq build here is 295.8 KiB, 1.54× under Rust's. The auto-par variant adds +81 KiB over the seq build to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration). *(History, 2026-06-05, legacy backend: the seq binary was 33.3 KiB, within 0.5 KiB of clang's, auto-par added +263 KiB, and every size was byte-for-byte unchanged from the 2026-05-27 baseline.)*

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    greedy | 1,048,888 | 1.0 |
| **kāra greedy (seq)** | **1,098,064** | **1.0** |
| rust greedy | 1,130,808 | 1.1 |
| kāra greedy (auto-par) | 1,868,208 | 1.8 |
| go   greedy | 9,912,800 | 9.5 |

Kāra-seq's **1.0 MiB peak ties C and Rust** — all three within 0.08 MiB of each other (Kāra 48 KiB over C and 32 KiB under Rust, a few 16-KiB page-clusters inside `/usr/bin/time -l`'s page-granular sampling). The per-iter `Vec[char]` allocate-then-drop cycle keeps steady-state heap usage tiny (one 60-byte buffer in flight at a time on the seq lane), so RSS is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.8 MiB for the lazy-init worker thread stacks — tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets — and peaks below the par-lane comparators (C pthreads 1.6 MiB, rayon 2.3 MiB, goroutines 15.8 MiB). Go's seq 9.5 MiB carries its GC roots + scheduler arena overhead, ~9× the seq-lane minimum on a workload whose steady-state working set fits in <100 bytes.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 greedy.c | 2,703,648 | 2.6 |
| rustc -O greedy.rs | 29,557,288 | 28.2 |
| karac build greedy.kara | 65,159,744 | 62.1 |

Karac peaks at **62.1 MiB** vs rustc's **28.2 MiB** (2.2× higher) and clang's **2.6 MiB** (24× higher). The kara number includes the auto-par recognition pass + reduction codegen. *(History, 2026-06-05, legacy backend: karac peaked at 15.3 MiB, 1.85× under rustc.)*

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).
