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
- **`while n >= 1000 { ... }` with `i64`-typed literals throughout** — the comparison and the subtraction both stay in `i64`; no implicit widening, no `usize` round-trip. Same `i64`-throughout discipline the kata [#11](../11-container-with-most-water/) two-pointer matcher uses.
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

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **10%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **1.1%** margin against `clang -O3` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`greedy.{kara,rs,c,py}`, `go-seq/main.go`, and the par-lane mirrors `rayon/`, `go-par/`, `greedy_par.c`).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + score_roman(r)` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`greedy_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build.
- **`greedy_kara`** — default `karac build` output. Picks up auto-par dispatch (~13 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** K = 10,000,000 outer iters, each driven by an LCG-shaped `num` in `[1, 3999]` (`(k * 2654435769 + 305419896) mod 3999 + 1`). Per iter: one `Vec[char]` allocation with capacity 15, the unrolled greedy fills it with the Roman numeral, then `score_roman` walks the result and sums codepoints. End-of-iter `Vec` drop. The LCG spread defeats branch-predictor memorization — the kernel sees every possible decimal pattern across the run rather than a small fixed rotation. Sink = sum of `score_roman` returns across K iters. All four compiled mirrors agree on `5728709596` before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

M5 Pro, measured 2026-10-31 with karac `g6697158fa` (the v2/MIR backend; [`bench/results.json`](bench/results.json) `measured_at` 2026-11-01T00:52Z UTC), hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | Within-lane ratio |
|---|---|---|---|
| go   greedy | 244.0 ms ± 2.4 ms | 247.6 ms (+87.8 ms system) | 0.75× of Kāra |
| rust greedy (rustc -O) | 312.6 ms ± 12.1 ms | 310.2 ms | 0.96× of Kāra |
| rust greedy (overflow-checks=on) | 317.6 ms ± 12.2 ms | 315.4 ms | 0.97× of Kāra |
| **kāra greedy** (`KARAC_AUTO_PAR=0`) | **326.0 ms ± 9.8 ms** | 323.6 ms | **1.00×** (baseline) |
| c    greedy (clang -O3) | 329.6 ms ± 8.4 ms | 327.2 ms | 1.01× of Kāra |

**Go leads the seq lane; Kāra, Rust and C sit in a ~4% band behind it.** Kāra takes **1.34× Go's time**, is **1.04× behind `rustc -O`** and **1.03× behind `rust -C overflow-checks=on`** (the equal-safety row), and ties C (**0.99×**, a 1.1% margin inside the 10% placement spread above). The three non-Go σ are 8–12 ms, so the Kāra/Rust/C order is not resolved by this run. Go's wall time hides extra cores: its user + system CPU (335 ms) exceeds its 244 ms wall time (137% CPU — GC and scheduler threads), so on CPU spent it is not ahead of the scalar languages by the wall-time margin. Against the previous feed (legacy backend, 2026-07-28) the Kāra/Rust and Kāra/C ratios are flat (1.03× → 1.04×, 0.97× → 0.99×) and Kāra gained on Go (1.51× → 1.34×); every comparator ran 4–19% slower this session (machine state), so compare ratios, not ms. *(History, 2026-06-05 legacy snapshot: Kāra was ~3% behind Go and ~6% ahead of Rust and ~19% ahead of C; that ordering had already dissolved by the 2026-07-28 feed.)*

Per-iter shape: one `Vec[char]` alloc + ~10 char-pushes (the unrolled greedy fill) + ~10 char-reads (the `score_roman` sum) + one Vec drop. At K=10M that's 10⁷ small allocs + 10⁷ drops. A diagnostic C variant that allocates the 60-byte buffer once outside the K-loop and reuses it per iter ([`bench/greedy_reuse.c`](bench/greedy_reuse.c)) ran at **138.9 ms ± 1.0 ms** (2026-06-05; 140.9 on 2026-05-25 — the one row that's rock-stable across snapshots, consistent with it doing no per-iter allocator work; not part of the bench feed, not re-run) — so for C, the per-iter `malloc(60)` + `free` round-trip cost ~112 ms over 10⁷ iters in the 2026-06-05 snapshot (~11.2 ns per pair; the estimate inherits the C row's batch variance, ~8–12 ns across snapshots).

#### Mechanism (corrected 2026-05-27)

An earlier version of this README concluded the ordering was "the four languages pay *different* allocator round-trip costs, and Kāra's path through libsystem `_malloc` / `_free` lands at the favorable end of the spread for small-Vec churn." **That was wrong.** A `DYLD_INSERT_LIBRARIES` malloc-counting shim against the Kāra and C binaries shows they make *byte-identical* allocator calls:

| | Kāra-seq | C |
|---|---|---|
| malloc calls | 10,000,028 | 10,000,028 |
| free calls | 10,000,014 | 10,000,014 |
| 60-byte allocs (the hot path) | 10,000,000 | 10,000,000 |

Same count, same 60-byte size class, same totals (within 28 bytes of startup noise). There is no allocator-path difference — both call libsystem `malloc(60)` / `free` exactly 10⁷ times.

The real mechanism is **clang's "optimization" of the generator is a pessimization here.** clang -O3 rewrites `int_to_roman`'s `while (n >= 1000) { push 'M'; n -= 1000; }` into Barrett-reduction division by constant plus a `memset_pattern16` bulk-fill call — 4 such call sites in the C binary, 0 in Kāra (Kāra lowers the loop literally as `cmp + store + sub + branch`). For the 1–12 byte fills typical of this kata (mean Roman length ~9.5), `memset_pattern16`'s ~3–5 ns cross-module call overhead exceeds the inline-store cost it replaces. So Kāra wins the generator by *not* applying a transform clang applies too eagerly at this output size. This is a reproducible observation about clang's heuristics — not a claim that Kāra's codegen is categorically faster. (See kata [#13](../13-roman-to-integer/#mechanism--where-the-84-ms-gap-over-c-actually-comes-from) for a parse-only diagnostic where, on a kernel clang does *not* over-vectorize, C edges Kāra by ~8% as expected of a mature optimizer.)

*(Note, 31 Oct 2026: this analysis and the figures in the list below are the 2026-06-05 legacy-backend snapshot. On the v2/MIR backend Kāra no longer leads Rust or C — it ties C and trails Rust by 1.04× — and neither the allocator-call identity nor the `cmp + store + sub + branch` lowering has been re-checked on MIR.)*

Corrected reading of the per-language rows — the spread is **algorithmic codegen on the generator**, not allocator cost (which is identical across Kāra/Rust/C and only modestly higher on Go's GC-tracked allocator):

- **Kāra (seq) at 210.1 ms** — literal lowering of the unrolled greedy; no `memset_pattern16`, no Barrett reduction. The 10⁷ × `malloc(60)`/`free` round-trip is in here too (~112 ms, same as C's), so Kāra's pure-algorithm floor is roughly 210 − 112 ≈ **98 ms** — *below* C's reuse-C floor of 139 ms.
- **Rust at 223.2 ms** (1.06× of Kāra) — `Vec::with_capacity(15)` + `push(c)`; rustc applies a milder version of the same loop rewrite than clang, landing between Kāra and C.
- **Go at 204.2 ms** (0.97× of Kāra) — `make([]int32, 0, 15)` adds a per-allocation GC-tracking write-barrier the scalar languages skip, on top of generator codegen comparable to Rust's; edges ahead of both Kāra and Rust in this snapshot.
- **C at 250.6 ms** (1.19× of Kāra) — clang's `memset_pattern16` + Barrett-reduction generator is the slowest of the four at this output size. The reuse-C floor (138.9 ms) is C's no-alloc number but **still carries the pessimized generator** — so it is *not* the "pure algorithm floor" an earlier version of this README called it. Kāra's algorithmic floor (~98 ms) is lower.

Every σ in the 2026-10-31 session is ≤ 12.2 ms (Go's 2.4 ms tightest, the Rust rows loosest). What persists on this machine is batch-level drift: a whole 30-run batch can land ~10% off the next one on byte-identical binaries, so cross-snapshot wall-time deltas of a few % are scheduling state, not codegen — which is why the Kāra/Rust/C order inside their ~4% band is not a result. The robust claim on the current feed is *Go first by a wide margin*; the 2026-06-05 ordering (Go and Kāra near the front, C last) no longer reproduces.

### Runtime — auto-par regime (kara default, multi-core)

Same session, default `karac build` output against in-lane parallel comparators (`rayon::par_iter`, C pthreads, goroutines + WaitGroup over the same outer reduction), hyperfine `--runs 50`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| c    greedy (pthreads) | **14.6 ms ± 2.4 ms** | 153.6 ms | ~1060% |
| rust greedy (rayon `par_iter`) | **43.3 ms ± 5.0 ms** | 676.9 ms | ~1600% |
| **kāra greedy** (auto-par on reduction) | **47.6 ms ± 5.1 ms** | 607.2 ms | ~1285% (~12.9 cores) |
| go   greedy (goroutines + WaitGroup) | **203.1 ms ± 2.2 ms** | 524.5 ms (+490.6 ms system) | ~500% |

Karac's auto-par-on-reduction recognizes the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch — verified in the emitted IR (`KARAC_MIR_LL`): the default build carries a call of `karac_mir_task_spawn` and the `KARAC_AUTO_PAR=0` twin does not; ~13 cores are active during the run. Within the par lane Kāra is **1.10× behind rayon**, **3.27× behind C pthreads**, and **4.3× ahead of Go** (0.23× Go's time). Against the 2026-07-28 feed that is a gain on C (5.01× → 3.27×) and Go (0.35× → 0.23×), and near flat against rayon (1.15× → 1.10×).

The wall-time win *over the seq-lane Kāra row above* is **6.8×** (326.0 / 47.6); total CPU time goes up 88% (323.6 → 607.2 ms user) as the cost of dispatch + per-worker fixed overhead. *(History, 2026-06-05 legacy snapshot: 19.5 ms, 10.8× over seq, +28% user CPU.)*

The per-iter alloc/drop discipline holds under auto-par: each worker thread builds + drops its own `Vec[char]` per iteration, the per-iteration cleanup-frame fix in karac [`0567170`](../../../../karac-rust/) keeps the per-worker heap from growing unbounded. Peak RSS under auto-par (1.8 MiB) sits just ~0.7 MiB above the seq lane — the small-Vec allocator path scales cleanly across workers.

**Not headlined against the seq-lane C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 7× faster than C" by setting the auto-par row against C's seq row would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the par table above is the in-lane parallel comparison, where Kāra gets its parallelism as a *language-level* choice (no source-level annotation; the analyzer recognizes the natural serial reduction) and the comparators write it by hand.

### Codegen vs Python

CPython at K = 1M takes **365.3 ± 2.5 ms** (single-core; last measured 2026-06-05, not re-run — this re-bench did not set `KARA_BENCH_INCLUDE_PY`); projected to K = 10M that's ~3.65 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~11× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~77× faster). Those ratios set the 2026-06-05 Python figure against the 2026-10-31 Kāra rows, so they are cross-session. The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Same session, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `greedy` | **187.5 ± 2.5 ms** | 106.4 ± 2.4 ms | 55.1 ± 0.7 ms |

Karac is **1.76× slower than rustc -O** and **3.40× slower than clang -O3**. *(History, 2026-06-05, legacy backend: karac compiled in 86.6 ms, 1.24× faster than rustc -O and 1.65× slower than clang -O3.)* Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    greedy | 33,576 | 32.8 |
| **kāra greedy (seq)** | **302,872** | **295.8** |
| kāra greedy (auto-par) | 386,152 | 377.1 |
| rust greedy | 466,584 | 455.6 |
| go   greedy | 2,492,546 | 2,434.1 |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger `B-2026-10-28-36`); the seq build here is 295.8 KiB, 1.54× under Rust's. The auto-par variant adds +81 KiB over the seq build to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration). *(History, 2026-06-05, legacy backend: the seq binary was 33.3 KiB, within 0.5 KiB of clang's, auto-par added +263 KiB, and every size was byte-for-byte unchanged from the 2026-05-25 baseline.)*

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    greedy | 1,065,272 | 1.0 |
| **kāra greedy (seq)** | **1,098,064** | **1.0** |
| rust greedy | 1,130,808 | 1.1 |
| kāra greedy (auto-par) | 1,835,440 | 1.8 |
| go   greedy | 10,224,072 | 9.8 |

Kāra-seq's **1.0 MiB peak sits midway between C and Rust** — 32 KiB (two 16-KiB page-clusters) over C and 32 KiB under Rust, effectively a three-way tie given `/usr/bin/time -l`'s page-granular sampling. The per-iter `Vec[char]` allocate-then-drop cycle keeps steady-state heap usage tiny (one 60-byte buffer in flight at a time on the seq lane), so RSS is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.7 MiB for the lazy-init worker thread stacks — tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets — and sits between the par-lane comparators (C pthreads 1.3 MiB, rayon 2.2 MiB, goroutines 17.0 MiB). Go's seq 9.8 MiB carries its GC roots + scheduler arena overhead, ~9.6× the seq-lane minimum on a workload whose steady-state working set fits in <100 bytes.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 greedy.c | 2,703,672 | 2.6 |
| rustc -O greedy.rs | 29,360,704 | 28.0 |
| karac build greedy.kara | 62,931,496 | 60.0 |

Karac peaks at **60.0 MiB** vs rustc's **28.0 MiB** (2.1× higher) and clang's **2.6 MiB** (23× higher). The kara number includes the auto-par recognition pass + reduction codegen. *(History, 2026-06-05, legacy backend: karac peaked at 14.7 MiB, 1.9× under rustc.)*

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Gaps found, in the kara bug ledger:

- **B-2026-10-06-85** — `s.chars().rev()` is refused by `karac build`; it blocks the roman-numeral round-trip differential, which is not checked in until it builds.
- `const` `Array` index / `len` / `for` under `karac build` is the already-open **B-2026-10-06-43** (found again independently).
