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

The naive approach is two rails (one each against `INT_MAX / 10` and `INT_MIN / 10`), as kata [#7](../7-reverse-integer/#the-overflow-rails) does. atoi can be simpler: build `result` as a *positive* i32 with the sign tracked separately as `±1`, and only multiply by the sign at the end. The accumulator's range is `[0, INT_MAX]`, so a single positive rail against `INT_MAX / 10` is sufficient. `-result` at the end fits in i32 worst-case at `INT_MIN + 1`, so no extra negation rail either.

The boundary case `result == max_div and digit == 8` deserves a note. For positive, this is overflow (`214_748_364 * 10 + 8 = 2_147_483_648 > INT_MAX`); we clamp to `INT_MAX`. For negative, the magnitude `2_147_483_648` is *exactly* `|INT_MIN|`, so the value `−2_147_483_648` fits — but we still return `INT_MIN` from the same clamp arm, which happens to be the correct answer. Both signs route through one code path because `INT_MIN` is the answer for negative-side magnitudes ≥ `2_147_483_648` regardless of whether the equality case is "exactly representable" or "underflow by one". No branch on the digit value is needed.

## Kāra features exercised

- **`ref String` parameter + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view over the String's UTF-8 storage. The LeetCode constraints pin the input to ASCII (`s` consists of English letters, digits, `' '`, `'+'`, `'-'`, `'.'`), so each byte is the codepoint and `bytes[i]` is the right primitive for the three-phase walk — no `Vec[char]` snapshot needed. Same `ref String` borrow shape as katas [#3](../3-longest-substring-without-repeating-characters/), [#5](../5-longest-palindromic-substring/), and [#6](../6-zigzag-conversion/).
- **`u8` byte-literal constants in comparisons** — `bytes[i] == space`, `b < zero`, `b > nine`, etc., where each constant is a `b'X'` byte literal (type `u8`, per design.md § Byte and Byte-String Literals). Comparisons are unsigned and total over `u8`, which matches the ASCII-range guarantee.
- **`u8 as i32` cast → digit subtraction** — `(b as i32) - (zero as i32)` turns a digit byte into its 0–9 numeric value. The same codepath caught a real interpreter bug during the early version of this kata: `ExprKind::Cast` was a no-op in the interpreter (codegen lowered it correctly via LLVM `int_cast`), so the cast silently left the wrong `Value` variant and the downstream subtraction mis-typed. The fix mirrors the typechecker's `check_cast_pair` accepted shapes (numeric↔numeric, bool→int, char→wide-int) — landed alongside this kata.
- **i32 arithmetic end-to-end** — `let result: i32 = 0i32`, `result * 10i32 + digit`, comparisons against `2147483647i32` / `-2147483648i32` / typed `7i32`. The LeetCode "no 64-bit storage" constraint maps directly; the accumulator is `i32` throughout and the overflow rail catches the multiply before it fires.
- **Compound boolean guards** — `result > max_div or (result == max_div and digit > 7i32)`, mixed `or`/`and` with parens. Same shape as kata [#7](../7-reverse-integer/#kāra-features-exercised); short-circuit evaluation works as expected.
- **Early `return` with typed literal** — `return int_max` / `return int_min` inside a function declared `-> i32`. The clamp arms exit the loop directly rather than letting `result` reach a broken intermediate.
- **`else if` chain in sign detection** — guards `bytes[i] == plus` then `bytes[i] == minus` then fall-through. Mutual exclusion gives the spec's "at most one sign character" behavior for free; the next-iter `+-12` and `-+12` cases land in the digit loop, see a non-digit, and break with `result = 0`.

No `Vec.collect()`, no `Map`, no shared structs — `Slice[u8]` view + scalar arithmetic.

## Edge cases worth exercising

| Input | Expected | Why it's interesting |
|---|---|---|
| `"42"` | `42` | The base case — no whitespace, no sign, no overflow. |
| `"   -42"` | `-42` | Leading spaces, then sign. Tests phase-1 → phase-2 transition. |
| `"4193 with words"` | `4193` | Trailing non-digits — stop at first non-digit, don't error. |
| `"words and 987"` | `0` | Non-digit prefix — the digit loop never runs, returns 0. |
| `"-91283472332"` | `-2147483648` | Underflow clamp. |
| `"91283472332"` | `2147483647` | Overflow clamp. |
| `"+1"` | `1` | Explicit `+` sign. |
| `""` | `0` | Empty input — no phases enter. |
| `"   "` | `0` | Whitespace-only — phase 1 consumes all, phases 2-3 see EOF. |
| `"+-12"` | `0` | Sign then non-digit — phase 2 takes the `+`, phase 3 sees `-` and breaks. |
| `"-+12"` | `0` | Symmetric — phase 2 takes the `-`, phase 3 sees `+` and breaks. |
| `"  0000000000012345678"` | `12345678` | Leading zeros after sign — multiply-by-10 absorbs them. |
| `"2147483647"` | `2147483647` | `INT_MAX` exactly — rail's `>` (not `>=`) preserves the boundary. |
| `"-2147483648"` | `-2147483648` | `INT_MIN` exactly — boundary digit 8 with `sign == -1` lands on the exact representable value. |
| `"2147483648"` | `2147483647` | One past `INT_MAX` — digit 8 at the boundary, positive sign → clamp to `INT_MAX`. |
| `"-2147483649"` | `-2147483648` | One past `INT_MIN` — digit 9 at the boundary → clamp to `INT_MIN`. |
| `"  +0 123"` | `0` | Trailing space + digits after a zero — phase 3 breaks at the space. |
| `"00000-42a1234"` | `0` | Digits then non-digit — `00000` reads as 0, then `-` breaks. The leading-zero sequence still counts as digits consumed. |
| `"  -0012a42"` | `-12` | Leading zeros after a sign, then digits, then a letter. |
| `"+"` | `0` | Sign with no digits — phase 3 sees EOF, returns the untouched `result = 0`. |

All 20 cases run in `main` and the output is diffed against [`atoi.py`](atoi.py).

## API shape

`my_atoi(s: ref String) -> i32` is the algorithm; `report(s: ref String)` prints the result; `main` calls `report` per case. Logic is separated from I/O so the function would slot into a future test harness unchanged. The Python file mirrors this with `my_atoi(s: str) -> int` and the same `report` / `main` shape.

Each Kāra `main` case passes its string literal directly to `report` — `ref String` accepts any source per design.md § Part 1½ Rule 4, and the codegen materializes the literal into a stack temp at the call site automatically (the `let c1 = "..."; report(c1)` workaround earlier versions of this kata used is no longer needed).

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

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then runs hyperfine for runtime + cold-compile, plus straight `wc` / `time -l` reads for binary size + memory. Python is timed in the same hyperfine pass at the same K = 10M — the per-call body is short enough that even CPython finishes in ~4 s, so the K = 50M / projection-only dance kata [#7](../7-reverse-integer/#benchmarks) needs isn't required here.

| File | What it does |
|---|---|
| [`bench/atoi.kara`](bench/atoi.kara) | N = 8 distinct inputs cycled by `k % N` (every arm of the three-phase scan exercised), K = 10,000,000 outer iters, sink = Σ my_atoi(inputs[k % N]) widened to i64 |
| [`bench/atoi.py`](bench/atoi.py) | Algorithmic mirror — same N, K, same input set, same sink formula |
| [`bench/atoi.rs`](bench/atoi.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/atoi.c`](bench/atoi.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |

The N = 8 inputs are picked to exercise every arm of the three-phase scan — bare positive (`"42"`), whitespace + sign (`"   -42"`), phase-3 early-exit at first non-digit (`"4193 with words"`), positive overflow rail (`"91283472332"`), explicit `+` (`"+1"`), leading zeros after sign (`"  0000000000012345678"`), INT_MIN boundary (`"-2147483648"`), and whitespace + sign + leading-zero + non-digit break (`"  -0012a42"`) — so no single branch dominates the predictor's history. All four impls print the same sink (`15_437_323_750_000` at the default parameters) so the algorithm's output participates in I/O and can't be elided. The bench's `bench.sh` asserts the kara, rust, c, and py sinks all match before timing.

### Runtime — 6.92× ahead of Rust, 7.50× ahead of C, via auto-par reduction

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build`, `rustc -O`, and `clang -O3`. Requires karac at commit [`28d76af`](../../../../karac-rust/) (slice 3b.4 + 3b.6 auto-par reduction lowering, plus the three par-reduce single-thread perf commits — [`a9e51c8`](../../../../karac-rust/) const-prop top-level let-init captures, [`1712d51`](../../../../karac-rust/) assume non-negative loop var, [`28d76af`](../../../../karac-rust/) vec-bounds-check hoist via modulo) or later.

| Run | Mean ± σ | User |
|---|---|---|
| `kara atoi` (codegen) | 6.5 ± 0.5 ms | 61.0 ms |
| `rust atoi` | 45.1 ± 0.5 ms | 43.7 ms |
| `c    atoi` | 48.9 ± 0.5 ms | 47.6 ms |
| `py   atoi` | 4,037 ± 38 ms | 4,025 ms |

The K = 10M outer loop is `let mut sum = 0i64; let mut k = 0i64; while k < k_iters { let idx = k % n; sum = sum + (my_atoi(inputs[idx]) as i64); k = k + 1i64; }` — the same reduction shape kata [#7](../7-reverse-integer/#runtime--987-ahead-of-rust-via-auto-par-reduction) hits, with `n` and `k_iters` as top-level `let` bindings. The slice-1 concurrency analyzer recognizes the pattern (`karac build --concurrency-report bench/atoi.kara` prints `reduction { op: +, accumulator: sum }`); the slice-3b codegen lowers it to a `karac_par_reduce` call that fans the iteration space across the M5 Pro's 6 P-cores + 12 E-cores, each thread accumulating into a private partial slot, then a final serial combine pass folds the partials into the parent's `sum`. The reduction op is associative + commutative (the slice-1 allow-list constraint), so the combine order doesn't affect the result — every run produces the same sink (`15_437_323_750_000`) regardless of how the work was split. **No source-level changes** to express the parallelism: the analyzer recognizes the shape from the natural serial source.

CPU utilization tells the parallelism story: hyperfine's reading is **User 61.0 ms / wall 6.5 ms ≈ 9.4× CPU usage** — close to perfect parallel scaling on the per-iter call shape. The per-iter work is meaningful (~10–20 bytes processed by `my_atoi` per outer iter, plus the function call) but the call is bounded by `strlen`-like behavior in C and `bytes().len()` in Kāra, so the inputs table reads dominate L1 cache traffic. Rust and C stay single-threaded (no rayon / pthreads annotation in the mirrors) and land within ~8% of each other; C is slightly slower than Rust at this workload because `strlen(s)` is recomputed every call from a raw `char *`, whereas Rust's `&str` carries the length in the slice header so `bytes.len()` is a single field load. Kara's `s.bytes().len()` mirrors Rust's behavior — String stores the byte length in its header — so the kara single-thread baseline tracks Rust, not C, on the per-call work.

### Single-thread CPU — within 1.30× of C after three karac perf commits

The wall-clock win above is parallelism; the **single-thread user time** is a separate read of how much work karac generates per worker. Pre-optimization, the user time was **92.0 ms** vs C's **47.6 ms** — Kāra was 1.93× slower than C on the same algorithm. Three perf commits closed most of the gap:

| Commit | What it removes | Worker user-time |
|---|---|---|
| (baseline, pre-perf) | — | 92.0 ms (1.93× of C) |
| [`a9e51c8`](../../../../karac-rust/) const-prop top-level let-init captures | `n = 8` arrives at worker as a constant, not a 24-byte heap load per iter | 72.5 ms (1.52× of C) |
| [`1712d51`](../../../../karac-rust/) assume non-neg loop var | ARM64 signed-mod-pow2 collapses from `negs/and/and/csneg` (4 instr) to `and #N-1` (1 instr) | 67.8 ms (1.42× of C) |
| [`28d76af`](../../../../karac-rust/) hoist vec bounds check via modulo | `inputs[k % 8]` bounds check moves from per-iter to function entry | 61.0 ms (**1.28× of C**) |

The residual ~30% over C is the `Vec[String]` stride (24-byte `{ptr, len, cap}` per element vs C's `const char *inputs[8]` 8-byte stride) — `umaddl` to compute the element address vs `ldr` with a shifted offset. Closing that gap requires a borrowed-view string type (`StringSlice`, analogous to `Slice[u8]` but UTF-8-aware), which is a non-trivial language-level slice not justified by a single kata. Tracked as "implement when a parsing kata demands it" in the slice tracker.

### Codegen vs Python

Python is **619× slower than Kāra codegen** at the same K. The per-iter body is dominated by CPython's per-bytecode dispatch — every `s[i] == ' '`, `s[i] < '0'`, and `ord(c) - ord('0')` is a fresh interpreter dispatch with object boxing for the integer arithmetic. The serial-vs-serial gap (using kara's single-thread user time of 61.0 ms vs python's 4025 ms) is **~66×**; the auto-par lowering widens that to 619× on wall by fanning across cores while CPython runs the GIL-locked single-threaded loop. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was wider (~1,950×) because the per-iter body there is even shorter (4 i32 ops vs ~15 bytes × ~5 ops/byte here) so interpreter overhead dominates a larger fraction.

### Runtime memory — slightly above Rust (worker thread overhead)

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara atoi` (codegen) | 1.4 MiB |
| `rust atoi` | 1.1 MiB |
| `c    atoi` | 1.1 MiB |
| `py   atoi` | 7.1 MiB |

Kara is ~0.3 MiB above the C/Rust baseline. Same root cause as kata [#7](../7-reverse-integer/#runtime-memory--slightly-above-rust-worker-thread-overhead): the `karac_par_reduce` call dispatches onto the long-lived `karac_par_run` pool, which reserves N = `available_parallelism()` OS-thread stacks regardless of how many reductions actually fire. Acceptable cost for the 7× wall-clock win.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build atoi.kara` | 60.8 ± 1.1 ms | 311.9 KiB |
| `rustc -O atoi.rs` | 79.2 ± 1.2 ms | 455.4 KiB |
| `clang -O3 atoi.c` | 40.8 ± 0.8 ms | 32.7 KiB |

Kāra compiles this kata **1.30× faster** than `rustc -O` and produces a binary **1.46× smaller**. Clang is **1.49× faster** than karac and produces a binary **9.5× smaller** — neither is surprising: C is the lower-floor reference for both axes, no runtime to link in, no thread-pool helpers, no String/Vec machinery. The kara binary's 312 KiB carries the auto-par reduction runtime (`karac_par_reduce`, `karac_par_run`, worker dispatch, partials combine, thread-pool init) — the same runtime weight kata [#7](../7-reverse-integer/#compile-time-and-binary-size) carries. Compared against a fair "comparable runtime" baseline (Rust, which also lazily pulls in the libstd thread machinery as needed), kara stays smaller thanks to the cross-archive LTO + DCE work.

Compile memory: karac peaks at **9.3 MiB** vs rustc's **26.6 MiB** vs clang's **2.6 MiB** — ~3× lower compile-time RAM than rustc, ~3.6× higher than clang. Same ordering as kata [#7](../7-reverse-integer/#compile-time-and-binary-size).

### Why Rust and C are in the harness

Same rationale as kata [#7](../7-reverse-integer/#why-rust-is-in-the-harness) for Rust: it's Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap. C is added here as the **lower-floor reference** — the hand-rolled scalar baseline with no String type, no length-prefixed slice, just `strlen` + raw `char *` per call. That tells us how much of the kara-vs-rust gap is "kara's auto-par advantage" (the wall-clock) vs how much would be left after a hypothetical zero-overhead source rewrite (the single-thread user time vs C). The current result — **6.92× faster than Rust on wall, 7.50× faster than C on wall, 1.28× of C on single-thread user time, 1.46× smaller binary than Rust, 1.30× faster compile than Rust, ~3× lower compile RAM than Rust, +0.3 MiB peak RSS for the worker thread pool** — is the second kata where kara's auto-concurrency lights up against serial baselines, with the gap to a hand-rolled C baseline shrunk to a stride-driven 1.3× by the three karac perf commits above.
