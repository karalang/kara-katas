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

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`greedy.{kara,rs,c,py}`, `go-seq/main.go`).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + roman_to_int(r)` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`greedy_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build.
- **`greedy_kara`** — default `karac build` output. Picks up auto-par dispatch (~11 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** K = 10,000,000 outer iters. Per iter: an LCG-shaped `num` in `[1, 3999]` (`(k * 2654435769 + 305419896) mod 3999 + 1`) is converted to Roman by the same unrolled greedy from kata [#12](../12-integer-to-roman/) (the *input generator*), then `roman_to_int` walks the resulting `Vec[char]` and reconstructs the i64 (the *function under measurement*). End-of-iter `Vec` drop. Because the generator and the parser are exact inverses on `[1, 3999]`, the running `sum` of reconstructed values equals the running sum of the LCG-drawn `num`s — a self-checking sink: if either direction has a bug, all five mirrors will disagree. Sink = `19989996724`. The LCG spread defeats branch-predictor memorization on both halves of the per-iter work (generator and parser see every possible decimal pattern across the run rather than a small fixed rotation). All five compiled mirrors agree on the sink before any timing runs; `bench.sh` fails loudly on mismatch.

This is a *fused* kata #12 + #13 workload: roughly 2× the per-iter algorithmic work of kata #12 (generate-then-parse rather than generate-then-sum-codepoints), against the same per-iter allocator-tax cost from the shared `Vec[char]` discipline.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-27, hyperfine `--warmup 5 --runs 30 --shell=none` (mean of two independent runs; σ from the quieter pass):

| Implementation | Wall time | User-CPU | Within-lane ratio |
|---|---|---|---|
| **kāra greedy** (`KARAC_AUTO_PAR=0`) | **288.6 ms ± 5.6 ms** | 283.1 ms | **1.00×** (baseline) |
| rust greedy (rustc -O) | 330.1 ms ± 3.1 ms | 324.2 ms | 1.14× of Kāra |
| go   greedy | 368.2 ms ± 38.1 ms | 366.8 ms | 1.28× of Kāra |
| c    greedy (clang -O3) | 372.6 ms ± 14.4 ms | 365.0 ms | 1.29× of Kāra |

**Kāra leads the seq lane on this *fused* workload** — by **~14% over Rust, ~28% over Go, ~29% over C**. But the headline needs unpacking, because the mechanism is not what it looks like. Kāra's mean held identically at **288.6 ms** across two independent re-runs (σ 20.5 ms vs 5.6 ms — the lower-σ pass is reported); the within-lane ordering reproduces.

The fused workload is two kernels back to back: `int_to_roman` (the generator) emits a `Vec[char]`, then `roman_to_int` (the parser) reads it back. Profiling each separately (see *Mechanism* below) shows **Kāra's lead comes entirely from the generator, and Kāra is actually slightly *slower* than C on the parser** — the kernel this kata is named for.

#### Mechanism — where the 84 ms gap over C actually comes from

The kata #12 README originally attributed Kāra's lead to "Kāra's path through libsystem `_malloc` / `_free` landing at the favorable end of the spread for small-Vec churn." **That was wrong, and is corrected here and in kata #12.** A `DYLD_INSERT_LIBRARIES` malloc-counting shim against both binaries shows Kāra and C make *byte-identical* allocator calls:

| | Kāra-seq | C |
|---|---|---|
| malloc calls | 10,000,028 | 10,000,028 |
| free calls | 10,000,014 | 10,000,014 |
| 60-byte allocs (the hot path) | 10,000,000 | 10,000,000 |

Same count, same 60-byte size class, same totals. There is no allocator-path difference. The real mechanism is in the **generator's algorithmic codegen**: clang -O3 rewrites `int_to_roman`'s `while (n >= 1000) { push 'M'; n -= 1000; }` into Barrett-reduction division by constant plus a `memset_pattern16` bulk-fill call (4 such call sites in the C binary; 0 in Kāra). For the 1–12 byte fills typical of this kata (mean Roman length ~9.5), `memset_pattern16`'s ~3–5 ns cross-module call overhead **exceeds** the inline-store cost — so clang's "optimization" is a pessimization, and Kāra wins by lowering the loop literally and *not* applying that transform.

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

The σ on the Go and C rows of the fused table is wider than Kāra/Rust (38.1 ms and 14.4 ms vs ~3-6 ms) — same scheduler/cache-state variance kata [#12](../12-integer-to-roman/) calls out. Re-runs reproduce the ordering.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra greedy** (auto-par on reduction) | **28.2 ms ± 1.8 ms** | 352.0 ms | ~1249% (~12 cores) |

Karac's auto-par-on-reduction recognizes the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch — the binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols. The wall-time win *over the seq-lane Kāra row above* is **10.2×** (288.6 / 28.2); total CPU time goes up 24% (283.1 → 352.0 ms user) as the cost of dispatch + per-worker fixed overhead.

The per-iter alloc/drop discipline holds under auto-par: each worker thread builds + drops its own `Vec[char]` per iteration, the per-iteration cleanup-frame fix in karac [`0567170`](../../../../karac-rust/) keeps the per-worker heap from growing unbounded. Peak RSS under auto-par (1.8 MiB) sits just 0.7 MiB above the seq lane — the small-Vec allocator path scales cleanly across workers.

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 13× faster than C" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the auto-par row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction). A follow-up CR can add a true par lane (`rayon::par_iter` + goroutines variants of the outer reduction) so this number lands against in-lane parallel comparators.

### Codegen vs Python

CPython at K = 1M takes **1.034 ± 0.006 s** (single-core); projected to K = 10M that's ~10.34 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~36× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~367× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-27, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `greedy` | **79.4 ± 1.0 ms** | 105.6 ± 0.6 ms | 53.5 ± 0.7 ms |

Karac is **1.33× faster than rustc -O** and **1.48× slower than clang -O3**. Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    greedy | 33,576 | 32.8 |
| **kāra greedy (seq)** | **33,656** | **32.9** |
| kāra greedy (auto-par) | 302,792 | 295.7 |
| rust greedy | 466,568 | 455.6 |
| go   greedy | 2,492,578 | 2,434.2 |

The seq-lane Kāra binary sits **within 0.1 KiB of clang's** (32.9 vs 32.8 KiB) — the same C-class minimum kata [#10](../10-regular-expression-matching/#binary-size), [#11](../11-container-with-most-water/#binary-size), and [#12](../12-integer-to-roman/#binary-size) report. The auto-par variant grows +263 KiB to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration) — same +263 KiB ballast every reduction-shape kata in the corpus carries. Here too the ballast pays for a real within-language wall-time win (10.4×).

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    greedy | 1,147,216 | 1.1 |
| **kāra greedy (seq)** | **1,163,600** | **1.1** |
| rust greedy | 1,179,984 | 1.1 |
| kāra greedy (auto-par) | 1,900,904 | 1.8 |
| go   greedy | 10,879,600 | 10.4 |

Kāra-seq's **1.1 MiB peak ties C and Rust** — all three within 0.04 MiB of each other. The per-iter `Vec[char]` allocate-then-drop cycle keeps steady-state heap usage tiny (one 60-byte buffer in flight at a time on the seq lane), so RSS is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.7 MiB for the lazy-init worker thread stacks — tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets. Go's 10.4 MiB carries its GC roots + scheduler arena overhead, ~9× the seq-lane minimum on a workload whose steady-state working set fits in <100 bytes.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 greedy.c | 2,720,104 | 2.6 |
| karac build greedy.kara | 11,600,352 | 11.1 |
| rustc -O greedy.rs | 29,704,792 | 28.3 |

Karac peaks at **11.1 MiB** vs rustc's **28.3 MiB** (2.6× lower) and clang's **2.6 MiB** (4.3× higher). The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).
