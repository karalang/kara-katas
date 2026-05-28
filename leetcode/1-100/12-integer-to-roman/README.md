# 12. Integer to Roman

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table, Math, String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/integer-to-roman](https://leetcode.com/problems/integer-to-roman/)

Convert an integer in `[1, 3999]` to its Roman-numeral form. The seven base symbols are `I, V, X, L, C, D, M` for `1, 5, 10, 50, 100, 500, 1000`. The system encodes `4` and `9` in each place via subtractive pairs: `IV`, `IX`, `XL`, `XC`, `CD`, `CM`. All other digits are pure additive (e.g., `III = 3`, `VIII = 8`, `LXX = 70`).

```
3      → "III"
4      → "IV"
9      → "IX"
58     → "LVIII"               (50 + 5 + 3)
1994   → "MCMXCIV"             (1000 + 900 + 90 + 4)
3888   → "MMMDCCCLXXXVIII"     (15 chars — the longest output in range)
3999   → "MMMCMXCIX"           (LeetCode upper bound)
```

**Constraints:** `1 ≤ num ≤ 3999`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Greedy unrolled-table | O(1) time, O(1) space modulo output | [`greedy.kara`](greedy.kara) ✓ via `karac run` / `karac build` | [`greedy.py`](greedy.py) ✓ | [`bench/greedy.rs`](bench/greedy.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 12 test cases.

## Why the unrolled greedy

The textbook approach builds two parallel arrays — `values = [1000, 900, 500, ..., 1]` and `symbols = ["M", "CM", "D", ..., "I"]` — then runs a loop over both:

```python
for v, s in zip(values, symbols):
    while num >= v:
        out.append(s)
        num -= v
```

That's clean, but each iteration of the outer loop pays the index-table-lookup cost on every step. With only **13 entries** in the table and **6 subtractive cases** that each fire **at most once** (the digit they encode — 4 or 9 — is unique within its decimal place), the body can be unrolled into 13 if/while branches:

```
while n >= 1000 { push 'M'; n -= 1000 }
if    n >= 900  { push 'C'; push 'M'; n -= 900 }
if    n >= 500  { push 'D'; n -= 500 }
if    n >= 400  { push 'C'; push 'D'; n -= 400 }
while n >= 100  { push 'C'; n -= 100 }   ← runs 0..3 times
...
while n >= 1    { push 'I'; n -= 1 }     ← runs 0..3 times
```

The four `while` blocks are the **pure-additive** cases (M / C / X / I) and each runs at most 3 times — because the next subtractive case above (CM / XC / IX, or `4`) would have absorbed any 4th repetition. The nine `if` blocks are the **subtractive** cases plus the five-of-a-place cases (D / L / V).

Per-call worst case: 15 char-pushes (`MMMDCCCLXXXVIII` for 3888 — `3 + 1 + 1 + 3 + 1 + 1 + 3 + 1 + 1 = 15` glyphs across all four places). Per-call mean over the full `1..3999` sweep: ~9.5 char-pushes. No nested loops, no table indexing, no string-building helper — just a comparison + a fixed pair of constants on every line.

This is the same shape LeetCode's "Approach 1" reference uses, except the unroll makes the subtractive-pair rule visible at every step instead of buried in the data, and the optimizer constant-folds every comparison against a literal.

## Kāra features exercised

- **`Vec[char]` per-call allocation + `Vec.with_capacity(15)`** — pre-sized to the worst-case output length, so all 12 LeetCode test cases push at most one growth-free fill. Same `with_capacity` shape kata [#6](../6-zigzag-conversion/) leans on after karac [`092180e`](../../../../karac-rust/) closed the check-mode element-type unification gap.
- **`out.push('M')`-style `char` literals on a Vec** — single-quote `char` is the source-level constant form; codegen lowers each literal to an i32 codepoint and the Vec's element type is pinned to `char` via the `Vec.with_capacity(15)` annotation, so the push site doesn't need explicit casts.
- **`while n >= 1000 { ... }` with `i64`-typed literals throughout** — the comparison and the subtraction both stay in `i64`; no implicit widening, no `usize` round-trip. Same `i64`-throughout discipline that kept the kata [#11](../11-container-with-most-water/) two-pointer matcher tied with C.
- **`print(c)` followed by `println("")`** — per-char UTF-8 glyph print (no newline) plus a single newline at end-of-line, building the Roman numeral on one output line. Same `print` arm kata [#6](../6-zigzag-conversion/) uses for its glyph emission, here in a "print every char in the buffer" sweep instead of "print one char per line".
- **`sum = sum + score_roman(r)` reduction in the bench's outer loop** — the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch.
- **Per-iter `Vec[char]` allocate-then-drop discipline in the auto-par worker** — each worker iteration builds + drops a fresh `Vec[char]`; the per-iteration cleanup-frame fix in karac [`0567170`](../../../../karac-rust/) (landed 2026-05-24 against kata #6's leak) is what keeps this kata's auto-par peak RSS bounded.

No `Map`, no `Set`, no shared structs; `String` only appears as a `println("")` literal at end-of-line.

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

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + score_roman(r)` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`greedy_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build.
- **`greedy_kara`** — default `karac build` output. Picks up auto-par dispatch (~11 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** K = 10,000,000 outer iters, each driven by an LCG-shaped `num` in `[1, 3999]` (`(k * 2654435769 + 305419896) mod 3999 + 1`). Per iter: one `Vec[char]` allocation with capacity 15, the unrolled greedy fills it with the Roman numeral, then `score_roman` walks the result and sums codepoints. End-of-iter `Vec` drop. The LCG spread defeats branch-predictor memorization — the kernel sees every possible decimal pattern across the run rather than a small fixed rotation. Sink = sum of `score_roman` returns across K iters. All four compiled mirrors agree on `5728709596` before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | Within-lane ratio |
|---|---|---|---|
| **kāra greedy** (`KARAC_AUTO_PAR=0`) | **200.2 ms ± 7.0 ms** | 197.8 ms | **1.00×** (baseline) |
| rust greedy (rustc -O) | 209.8 ms ± 6.8 ms | 207.3 ms | 1.05× of Kāra |
| go   greedy | 220.7 ms ± 16.1 ms | 230.3 ms | 1.10× of Kāra |
| c    greedy (clang -O3) | 242.9 ms ± 18.6 ms | 237.9 ms | 1.21× of Kāra |

**Kāra leads the seq lane on this workload's shape** — by **~5% over Rust, ~10% over Go, ~21% over C**. The mechanism behind that lead is subtle and was originally mis-attributed in this README; the corrected analysis is below.

Per-iter shape: one `Vec[char]` alloc + ~10 char-pushes (the unrolled greedy fill) + ~10 char-reads (the `score_roman` sum) + one Vec drop. At K=10M that's 10⁷ small allocs + 10⁷ drops. A diagnostic C variant that allocates the 60-byte buffer once outside the K-loop and reuses it per iter ([`bench/greedy_reuse.c`](bench/greedy_reuse.c)) runs at **140.9 ms ± 1.0 ms** — so for C, the per-iter `malloc(60)` + `free` round-trip costs ~84 ms over 10⁷ iters (~8.4 ns per pair).

#### Mechanism (corrected 2026-05-27)

An earlier version of this README concluded the ordering was "the four languages pay *different* allocator round-trip costs, and Kāra's path through libsystem `_malloc` / `_free` lands at the favorable end of the spread for small-Vec churn." **That was wrong.** A `DYLD_INSERT_LIBRARIES` malloc-counting shim against the Kāra and C binaries shows they make *byte-identical* allocator calls:

| | Kāra-seq | C |
|---|---|---|
| malloc calls | 10,000,028 | 10,000,028 |
| free calls | 10,000,014 | 10,000,014 |
| 60-byte allocs (the hot path) | 10,000,000 | 10,000,000 |

Same count, same 60-byte size class, same totals (within 28 bytes of startup noise). There is no allocator-path difference — both call libsystem `malloc(60)` / `free` exactly 10⁷ times.

The real mechanism is **clang's "optimization" of the generator is a pessimization here.** clang -O3 rewrites `int_to_roman`'s `while (n >= 1000) { push 'M'; n -= 1000; }` into Barrett-reduction division by constant plus a `memset_pattern16` bulk-fill call — 4 such call sites in the C binary, 0 in Kāra (Kāra lowers the loop literally as `cmp + store + sub + branch`). For the 1–12 byte fills typical of this kata (mean Roman length ~9.5), `memset_pattern16`'s ~3–5 ns cross-module call overhead exceeds the inline-store cost it replaces. So Kāra wins the generator by *not* applying a transform clang applies too eagerly at this output size. This is a reproducible observation about clang's heuristics — not a claim that Kāra's codegen is categorically faster. (See kata [#13](../13-roman-to-integer/#mechanism--where-the-84-ms-gap-over-c-actually-comes-from) for a parse-only diagnostic where, on a kernel clang does *not* over-vectorize, C edges Kāra by ~8% as expected of a mature optimizer.)

Corrected reading of the per-language rows — the spread is **algorithmic codegen on the generator**, not allocator cost (which is identical across Kāra/Rust/C and only modestly higher on Go's GC-tracked allocator):

- **Kāra (seq) at 200.2 ms** — literal lowering of the unrolled greedy; no `memset_pattern16`, no Barrett reduction. The 10⁷ × `malloc(60)`/`free` round-trip is in here too (~84 ms, same as C's), so Kāra's pure-algorithm floor is roughly 200 − 84 ≈ **116 ms** — *below* C's reuse-C floor of 141 ms.
- **Rust at 209.8 ms** (1.05× of Kāra) — `Vec::with_capacity(15)` + `push(c)`; rustc applies a milder version of the same loop rewrite than clang, landing between Kāra and C.
- **Go at 220.7 ms** (1.10× of Kāra) — `make([]int32, 0, 15)` adds a per-allocation GC-tracking write-barrier the scalar languages skip, on top of generator codegen comparable to Rust's.
- **C at 242.9 ms** (1.21× of Kāra) — clang's `memset_pattern16` + Barrett-reduction generator is the slowest of the four at this output size. The reuse-C floor (140.9 ms) is C's no-alloc number but **still carries the pessimized generator** — so it is *not* the "pure algorithm floor" an earlier version of this README called it. Kāra's algorithmic floor (~116 ms) is lower.

The σ on the C and Go rows is wider than Kāra/Rust (18.6 ms and 16.1 ms vs ~7 ms) because of higher cache-state variance at this scale — both had a few outliers above 300 ms while the bulk landed near the mean. Re-runs reproduce the ordering.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra greedy** (auto-par on reduction) | **21.4 ms ± 2.7 ms** | 247.2 ms | ~1156% (~11 cores) |

Karac's auto-par-on-reduction recognizes the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch — the binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~11 cores active during the run. The wall-time win *over the seq-lane Kāra row above* is **9.4×** (200.2 / 21.4); total CPU time goes up 25% (197.8 → 247.2 ms user) as the cost of dispatch + per-worker fixed overhead.

The per-iter alloc/drop discipline holds under auto-par: each worker thread builds + drops its own `Vec[char]` per iteration, the per-iteration cleanup-frame fix in karac [`0567170`](../../../../karac-rust/) keeps the per-worker heap from growing unbounded. Peak RSS under auto-par (1.8 MiB) sits just 0.7 MiB above the seq lane — the small-Vec allocator path scales cleanly across workers.

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 11× faster than C" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the auto-par row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction). A follow-up CR can add a true par lane (`rayon::par_iter` + goroutines variants of the outer reduction) so this number lands against in-lane parallel comparators.

### Codegen vs Python

CPython at K = 1M takes **379.0 ± 4.2 ms** (single-core); projected to K = 10M that's ~3.79 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~19× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~177× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `greedy` | **82.4 ± 20.6 ms** | 99.5 ± 0.9 ms | 52.2 ± 0.7 ms |

Karac is **1.21× faster than rustc -O** and **1.58× slower than clang -O3**. The Karac σ is wider than usual on this workload — one cold-cache outlier at 138.9 ms pulled the spread; the median is ~75 ms. Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    greedy | 33,576 | 32.8 |
| **kāra greedy (seq)** | **33,656** | **32.9** |
| kāra greedy (auto-par) | 302,792 | 295.7 |
| rust greedy | 466,568 | 455.6 |
| go   greedy | 2,492,546 | 2,434.1 |

The seq-lane Kāra binary sits **within 0.1 KiB of clang's** (32.9 vs 32.8 KiB) — the same C-class minimum kata [#10](../10-regular-expression-matching/#binary-size) and [#11](../11-container-with-most-water/#binary-size) report. The auto-par variant grows +263 KiB to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration) — same +263 KiB ballast kata [#4](../4-median-of-two-sorted-arrays/#binary-size), [#8](../8-string-to-integer-atoi/#binary-size), [#9](../9-palindrome-number/#binary-size), [#10](../10-regular-expression-matching/#binary-size), and [#11](../11-container-with-most-water/#binary-size) carry when their outer reductions go auto-par. Here too the ballast pays for a real within-language wall-time win (9.4×).

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| **kāra greedy (seq)** | **1,147,216** | **1.1** |
| c    greedy | 1,163,600 | 1.1 |
| rust greedy | 1,179,984 | 1.1 |
| kāra greedy (auto-par) | 1,884,520 | 1.8 |
| go   greedy | 9,880,104 | 9.4 |

Kāra-seq's **1.1 MiB peak ties C and Rust** — all three within 0.04 MiB of each other. The per-iter `Vec[char]` allocate-then-drop cycle keeps steady-state heap usage tiny (one 60-byte buffer in flight at a time on the seq lane), so RSS is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.7 MiB for the lazy-init worker thread stacks — tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets. Go's 9.4 MiB carries its GC roots + scheduler arena overhead, ~8× the seq-lane minimum on a workload whose steady-state working set fits in <100 bytes.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 greedy.c | 2,687,336 | 2.6 |
| karac build greedy.kara | 11,076,064 | 10.6 |
| rustc -O greedy.rs | 29,475,440 | 28.1 |

Karac peaks at **10.6 MiB** vs rustc's **28.1 MiB** (2.7× lower) and clang's **2.6 MiB** (4.1× higher). The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).
