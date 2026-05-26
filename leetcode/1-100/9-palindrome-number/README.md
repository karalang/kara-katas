# 9. Palindrome Number

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/palindrome-number](https://leetcode.com/problems/palindrome-number/)

Given an integer `x`, return `true` if `x` reads the same forward and backward as a base-10 numeral, else `false`. LeetCode's follow-up asks: solve it without converting the integer to a string.

```
121          →  true     (reads the same both ways)
-121         →  false    ("-" disqualifies, no leading sign in the reverse)
10           →  false    (reversed = "01" = 1, not "10")
0            →  true     (zero is a single-digit palindrome)
12321        →  true     (odd-length palindrome)
1221         →  true     (even-length palindrome)
1000000001   →  true     (10-digit palindrome, edges only)
```

**Constraints:** `-2³¹ ≤ x ≤ 2³¹ − 1`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Half-reverse with overflow-free i32 | O(log₁₀ \|x\|) time, O(1) space | [`palindrome.kara`](palindrome.kara) ✓ via `karac run` / `karac build` | [`palindrome.py`](palindrome.py) ✓ | [`bench/palindrome.rs`](bench/palindrome.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 20 test cases — the f-string interpolation of negative `i32` values matches between phases after the codegen fix [`2271021`](../../../../karac-rust/) (2026-05-25); pre-fix, `f"is_palindrome({x})"` with `x = -121i32` rendered as `4294967175` from codegen but `-121` from the interpreter.

## Why half-reverse instead of full-reverse

Kata #7's [Reverse Integer](../7-reverse-integer/) carries an INT_MAX/INT_MIN rail because reversing a full i32 can step over the 32-bit boundary (`1534236469` reverses to `9_646_324_351`, well past INT_MAX). The palindrome check side-steps the entire problem: walk the digits only until the unread head meets the accumulated reverse tail. At that midpoint the head holds the *first* half of the input and the tail holds the *second* half reversed; if they're equal (or differ only by a middle digit on odd-length inputs), the input is a palindrome.

```
12321
 ↓ iter 1: digit=1, reversed=1,   x=1232
 ↓ iter 2: digit=2, reversed=12,  x=123
 ↓ iter 3: digit=3, reversed=123, x=12     (x ≤ reversed, exit)
12 == 123 / 10 → true   (drop middle digit '3' from reversed)
```

Half of any i32 fits comfortably in i32: max 5-digit half is `99999`, far below INT_MAX. So no `INT_MAX / 10` rail, no last-digit boundary check — just a single `while x > reversed` loop with a two-case equality test at exit.

## Why one loop covers both palindrome lengths

After the loop, the input has been bisected:
- **Even digit count** (1221): the loop split it exactly in half. `x = 12`, `reversed = 12`. Equal → palindrome.
- **Odd digit count** (12321): the loop ate one extra digit on the right side, so `reversed` is one digit longer. `x = 12`, `reversed = 123`. Drop reversed's low digit: `123 / 10 = 12`. Equal → palindrome.

The middle digit on odd-length inputs doesn't affect symmetry — it reads the same regardless of direction — so dropping it via integer division is exact.

## Early rejects

Two shortcuts fire before the loop:

```
x < 0                      → false   (sign breaks symmetry; no leading '-' in the reverse)
x % 10 == 0 and x != 0     → false   (trailing zero would need leading zero in reverse; e.g. 10 → "01" = 1)
```

The second reject is what `palindrome.py`'s implementation needs to mirror exactly: zero itself is a palindrome (`0 == 0`), but `10`, `100`, `2147483640` are not — their reverses lose the leading-zero structure that an integer can't represent.

## Kāra features exercised

- **`bool`-returning predicate** — `fn is_palindrome(x: i32) -> bool` with `return false;` early-rejects and a tail-expression boolean (`x == reversed or x == reversed / 10i32`). Codegen lowers `bool` to LLVM `i1`; the f-string `{r}` arm renders it as `"true"` / `"false"` via the dedicated bool branch in `compile_fstr_part_to_cstr` (added pre-kata).
- **f-string interpolation of `i32`** — `println(f"is_palindrome({x}): {r}");` exercises both the integer and bool arms of the f-string formatter. The codegen fix landed at [`2271021`](../../../../karac-rust/) (2026-05-25) sign-extends narrow ints to i64 before snprintf's `%lld`, so negative `i32` values render correctly inside f-strings. Pre-fix, the bool arm was right but the int arm produced the unsigned reinterpretation on negatives (`-121` → `4294967175`).
- **Truncated `%` and `/`** — same as kata #7. Here the early `x < 0` reject means the loop only ever sees non-negative values, so Python's floor `//` and Kāra's truncated `/` produce identical results across the algorithm; no `c_div` / `c_mod` helpers needed in [`palindrome.py`](palindrome.py).
- **Compound boolean guard** — `x < 0i32 or (x % 10i32 == 0i32 and x != 0i32)` short-circuits both `or` and `and` arms; `x == reversed or x == reversed / 10i32` is the tail-expression bool that becomes the function's return value.
- **Typed `i32` literals throughout** — `0i32`, `10i32`, every comparison constant carries the suffix; the function signature's `-> bool` carries no widening fallback, so the suffixes are required to keep operands homogeneous (mirrors kata #7's discipline).

No `Vec`, no `String`, no `Map`, no shared structs — pure scalar arithmetic, narrower than even kata #7 (no INT_MAX rail).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   palindrome.kara
karac build palindrome.kara && ./palindrome

# Python
python3 palindrome.py

# Verify they agree
diff <(./palindrome) <(python3 palindrome.py) && echo OK
diff <(karac run palindrome.kara) <(python3 palindrome.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`palindrome.{kara,rs,c,py}`, `go-seq/main.go`).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 50,000,000 outer loop's `sum = sum + (if r { 1i64 } else { 0i64 })` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`palindrome_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`palindrome_kara`** — default `karac build` output. Picks up auto-par dispatch (~10.8 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** N = 1024 LCG-fill i32 inputs (every 16th overwritten to a manufactured 8-digit palindrome → ~1/16 true rate), K = 50,000,000 outer iters, sink = count of `is_palindrome(inputs[k % N])` widened to i64. All four compiled mirrors agree on `3125000` (exactly 64 palindromes × 50M / 1024 expected hit count) before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust palindrome (rustc -O) | **61.7 ms ± 1.1 ms** | 60.3 ms | 98% |
| c    palindrome (clang -O3) | **69.2 ms ± 0.8 ms** | 67.8 ms | 98% |
| **kāra palindrome** (`KARAC_AUTO_PAR=0`) | **69.8 ms ± 0.7 ms** | 68.4 ms | 98% |
| go   palindrome | **107.1 ms ± 0.9 ms** | 105.0 ms | 98% |

Kāra **matches `clang -O3` within σ** (69.8 vs 69.2 ms — measurement-noise parity) and runs **1.13× behind `rustc -O`** (69.8 vs 61.7 ms). Both ratios are within-lane: the same per-core single-threaded codegen-quality comparison the kata corpus is built around.

The Rust win on per-core throughput is plausibly the same shape as kata #4's pre-`bdac0d8` snapshot — rustc inlines `is_palindrome` into `main` while karac currently emits a call. `objdump --syms target/palindrome_kara_seq | grep is_palindrome` will tell us whether the symbol survived; if it did, the post-`bdac0d8` internal-linkage path may have a corner case for `bool`-returning predicates worth investigating. Filing as a follow-up rather than blocking the kata; the current seq-lane result is already 1.13× of Rust which is already good.

The Go gap (~1.55× of Kāra-seq) reflects per-iter slice-bounds checks + the boxed `int32` return that Go can't SROA across the small predicate body.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra palindrome** (auto-par on reduction) | **8.8 ms ± 0.8 ms** | 95.2 ms | ~1080% (~10.8 cores) |

Karac's auto-par-on-reduction recognizes the K=50M reduction in `main` and emits a `karac_par_reduce` dispatch — the binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~10.8 cores active during the run. The wall-time win *over the seq-lane Kāra row above* is **7.9×** (69.8 / 8.8); total CPU time goes up 39% (68.4 → 95.2 ms user) as the cost of dispatch + per-worker fixed overhead. Net: real production wall-time speedup on this workload's shape, paid for in additional CPU and a +263 KiB binary footprint (see § *Binary size* below).

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 7× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the auto-par row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction). A follow-up CR can add a true par lane (`rayon::par_iter` + goroutines variants of the outer reduction) so this number lands against in-lane parallel comparators.

### Codegen vs Python

Python at K = 1M takes 159 ms (single-core); projected to K = 50M that's ~7.95 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~114× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~903× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `palindrome` | **61.2 ms ± 3.0 ms** | 80.9 ms ± 1.0 ms | 44.4 ms ± 1.4 ms |

Karac is **1.32× faster than rustc -O** and **1.38× slower than clang -O3**. Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc`/`clang`/`karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    palindrome | 33,520 | 32.7 |
| **kāra palindrome (seq)** | **33,656** | **32.9** |
| kāra palindrome (auto-par) | 302,872 | 295.8 |
| rust palindrome | 466,584 | 455.6 |
| go   palindrome | 2,492,546 | 2,434.1 |

The seq-lane Kāra binary sits **within 0.2 KiB of clang's** (32.9 vs 32.7 KiB) — the cross-archive LTO + DCE work (landed 2026-05-12) plus the post-`e76f42b` `__TEXT,__jittmpl` segment compaction has the seq binary at C-class minimum. The auto-par variant grows +263 KiB to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration) — same +263 KiB ballast kata [#4](../4-median-of-two-sorted-arrays/#binary-size) carries when its outer reduction goes auto-par. Here too the ballast pays for a real within-language wall-time win.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    palindrome | 1,114,448 | 1.1 |
| **kāra palindrome (seq)** | **1,114,448** | **1.1** |
| rust palindrome | 1,163,600 | 1.1 |
| kāra palindrome (auto-par) | 1,540,480 | 1.5 |
| go   palindrome | 3,113,536 | 3.0 |

Kāra-seq is **byte-exact with C** (both at 1,114,448 bytes — the 4 KiB inputs Vec dominates steady state; everything else is libc + ELF/Mach-O loader overhead). Auto-par Kāra adds ~0.4 MiB for the lazy-init worker thread stacks — same overhead documented in [kata #7](../7-reverse-integer/) and [kata #4](../4-median-of-two-sorted-arrays/). Tunable downward via `KARAC_PAR_WORKERS` ([`d33b389`](../../../../karac-rust/)) for memory-constrained targets. Go's 3.0 MiB carries its GC roots + scheduler arena overhead.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 palindrome.c | 2,736,488 | 2.6 |
| karac build palindrome.kara | 9,814,496 | 9.4 |
| rustc -O palindrome.rs | 28,574,344 | 27.3 |

Karac peaks at **9.4 MiB** vs rustc's **27.3 MiB** (2.9× lower) and clang's **2.6 MiB** (3.6× higher). The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site — the seq build path would shave a small constant off but not materially change the ratio.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).
