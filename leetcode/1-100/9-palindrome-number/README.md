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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`palindrome.{kara,rs,c,py}`, `go-seq/main.go`, plus the par-lane mirrors).

Snapshot for every table below unless marked otherwise: Apple M5 Pro (6P+12E), karac `0.9.0-dev.14057+g6697158fa` (the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, go 1.26.3, hyperfine 1.20.0, measured 2026-10-31 (feed `measured_at` 2026-11-01T00:47Z UTC). Source of truth: [`bench/results.json`](bench/results.json).

> **Re-bench 2026-10-31 — what moved.** Quoted as language ratios, because every comparator ran 10–22% slower in absolute terms this session (machine state).
>
> - **Seq lane: Kāra/Rust 1.42× → 1.61×, Kāra/C 1.30× → 1.43×** (previous feed: 2026-07-28, legacy backend) — a ~1.1× relative loss; the MIR build executes 1.11× legacy's instructions.
> - **Par lane: Kāra/rayon 1.21× → 2.10×, Kāra/C-pthreads 1.17× → 2.09×, Kāra/Go 0.76× → 1.29×.** The par build executes a constant +75% of the seq build's instructions as soon as it has two or more workers (2.46 G at 1 worker, 4.31 G at 2–18), filed as [`B-2026-10-31-39`](../../../../kara/docs/bugs-v2.md) — see [Bug ledger](#bug-ledger).
> - **Binary size: 33.5 → 295.8 KiB (seq)** — see [Binary size](#binary-size).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 50,000,000 outer loop's `sum = sum + (if r { 1i64 } else { 0i64 })` accumulator is a textbook associative + commutative reduction, which the concurrency analyzer recognizes and codegen parallelizes *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`palindrome_kara_seq`** — built with `KARAC_AUTO_PAR=0` (the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc-O / clang-O3 / go build. Its IR carries no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`).
- **`palindrome_kara`** — default `karac build` output, whose IR carries the `karac_mir_task_spawn` call. Picks up auto-par dispatch (~13 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** N = 1024 LCG-fill i32 inputs (every 16th overwritten to a manufactured 8-digit palindrome → ~1/16 true rate), K = 50,000,000 outer iters, sink = count of `is_palindrome(inputs[k % N])` widened to i64. All four compiled mirrors agree on `3125000` (exactly 64 palindromes × 50M / 1024 expected hit count) before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

M5 Pro, 2026-10-31, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust palindrome (rustc -O) | **67.3 ms ± 1.3 ms** | 66.3 ms | 99% |
| c    palindrome (clang -O3) | **75.7 ms ± 0.6 ms** | 74.8 ms | 100% |
| rust palindrome (`-C overflow-checks=on`) | **91.7 ms ± 4.5 ms** | 90.7 ms | 100% |
| **kāra palindrome** (`KARAC_AUTO_PAR=0`) | **108.3 ms ± 1.3 ms** | 107.2 ms | 100% |
| go   palindrome | **116.4 ms ± 1.6 ms** | 115.1 ms | 100% |

**Read the two Rust rows together — that's the apples-to-apples story.** Kāra
traps on integer overflow *by default* (design.md § Arithmetic Overflow: "defined
behavior, never undefined"); `rustc -O` **silently wraps**. So the equal-safety
build — Rust with `-C overflow-checks=on` — is the comparison that holds the
safety constant. Against it Kāra is **1.18× behind**: 108.3 ms vs 91.7 ms, a gap
that is per-core codegen, not a safety difference (it was 1.06× on the legacy
backend). The wider 1.61× against `rustc -O`'s default adds the silent-wraparound
bug class Kāra refuses to ship and Rust release opts out of — the half-reverse
digit walk here never overflows i32, but Kāra still checks every `reversed * 10`
like the language guarantees. (C and Go also wrap; they are the unsafe-but-fast
floor, not safety peers.) Against `clang -O3` Kāra runs 1.43× behind (108.3 vs
75.7 ms), within-lane.

The Rust win on per-core throughput is plausibly the same shape as kata #4's pre-`bdac0d8` snapshot — rustc inlines `is_palindrome` into `main` while karac may emit a call. The emitted IR (`KARAC_MIR_LL`) will tell us whether the call survived (symbols are no longer visible to `objdump`/`nm` on macOS: the executable exports `main` alone since kara a54f99f726). Filing as a follow-up rather than blocking the kata; the current seq-lane result is 1.18× behind equal-safety Rust and 1.61× behind wrapping `rustc -O`.

The Go gap (Go at 1.07× of Kāra-seq) reflects per-iter slice-bounds checks + the boxed `int32` return that Go can't SROA across the small predicate body.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output, hyperfine `--warmup 10 --runs 50`. All four languages parallelize the same K = 50M reduction; the difference is what the programmer wrote.

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust palindrome (rayon) | **9.8 ms ± 0.3 ms** | 117.9 ms | ~1306% |
| c    palindrome (pthreads) | 9.8 ms ± 0.8 ms | 111.4 ms | ~1141% |
| go   palindrome (goroutines) | 16.0 ms ± 1.3 ms | 166.9 ms | ~1056% |
| **kāra palindrome** (auto-par on reduction) | **20.6 ms ± 0.6 ms** | 258.9 ms | ~1281% (~13 cores) |

Karac's auto-par recognizes the K=50M reduction in `main` and dispatches it across workers, ~13 cores active during the run. **Kāra with zero parallel source is 2.10× behind rayon, 2.09× behind C+pthreads and 1.29× behind Go** — on the legacy backend it was 1.21× / 1.17× and 0.76× (ahead of Go). The wall-time win *over the seq-lane Kāra row above* is **5.3×** (108.3 / 20.6); total CPU time goes up 2.42× (107.2 → 258.9 ms user), more than twice any comparator's par user-CPU. That excess is [`B-2026-10-31-39`](../../../../kara/docs/bugs-v2.md): the par build runs +75% of the seq build's instructions as soon as it has two or more workers.

**Not headlined against the seq rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 3× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the par table is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction), set against the hand-written parallel mirrors.

### Codegen vs Python

Last measured 2026-06-16, not re-run (this run did not set `KARA_BENCH_INCLUDE_PY`). Python at K = 1M took 159 ms (single-core); projected to K = 50M that's ~7.95 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: at that snapshot Kāra-seq vs CPython was the within-lane per-core comparison (~93× faster), and Kāra-auto-par vs CPython the cross-lane regime comparison (~729× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

M5 Pro, 2026-10-31, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `palindrome` | **152.7 ms ± 2.4 ms** | 88.4 ms ± 1.0 ms | 48.3 ms ± 1.0 ms |

Karac is now **1.73× slower than rustc -O** and **3.16× slower than clang -O3**; on the legacy backend (2026-07-28 feed) it was 1.23× of rustc's time, and 1.18× faster than rustc in the 2026-05-31 snapshot. Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc`/`clang`/`karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    palindrome | 33,520 | 32.7 |
| **kāra palindrome (seq)** | **302,872** | **295.8** |
| kāra palindrome (auto-par) | 386,152 | 377.1 |
| rust palindrome | 466,584 | 455.6 |
| go   palindrome | 2,492,546 | 2,434.1 |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); the seq binary was 34,312 B on the legacy backend, within ~0.8 KiB of clang's. It is 1.54× under Rust's 455.6 KiB. The auto-par variant carries +81 KiB over seq for the parallel-dispatch machinery.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    palindrome | 1,065,272 | 1.0 |
| **kāra palindrome (seq)** | **1,098,040** | **1.0** |
| rust palindrome | 1,130,808 | 1.1 |
| c    palindrome (pthreads) | 1,360,208 | 1.3 |
| kāra palindrome (auto-par) | 1,556,936 | 1.5 |
| rust palindrome (rayon) | 2,064,720 | 2.0 |
| go   palindrome | 2,802,096 | 2.7 |
| go   palindrome (goroutines) | 4,325,880 | 4.1 |

Kāra-seq is now **a hair over C** (1,098,040 vs 1,065,272 bytes, +32 KiB) and under Rust. The 4 KiB inputs Vec dominates; everything else is libc + ELF/Mach-O loader overhead. Auto-par Kāra adds ~0.4 MiB for the lazy-init worker thread stacks — same overhead documented in [kata #7](../7-reverse-integer/) and [kata #4](../4-median-of-two-sorted-arrays/), still under rayon's 2.0 MiB. Tunable downward via `KARAC_PAR_WORKERS` ([`d33b389`](../../../../karac-rust/)) for memory-constrained targets. Go's 2.7 MiB carries its GC roots + scheduler arena overhead.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 palindrome.c | 2,736,416 | 2.6 |
| rustc -O palindrome.rs | 28,475,944 | 27.2 |
| karac build palindrome.kara | 60,736,040 | 57.9 |

Karac now peaks at **57.9 MiB** vs rustc's **27.2 MiB** (2.13× higher) and clang's **2.6 MiB**; on the legacy backend (2026-07-28 feed) it peaked at 24.8 MiB, under rustc. The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site — the seq build path would shave a small constant off but not materially change the ratio.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).

## Bug ledger

**Surfaced [`B-2026-10-31-39`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the v2/MIR backend this kata's auto-par build executes a constant +75% of the seq build's instructions as soon as it has two or more workers (2.46 G at 1 worker, 4.31 G at 2–18 workers, flat across that range), so the par lane went from 1.21× to 2.10× rayon's time.
