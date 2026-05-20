# 7. Reverse Integer

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-integer](https://leetcode.com/problems/reverse-integer/)

Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing causes the value to fall outside the signed 32-bit range `[-2³¹, 2³¹ − 1]`, return `0`. The problem statement forbids storing 64-bit intermediates — the overflow check has to live inside the 32-bit world.

```
123          →  321
-123         →  -321
120          →  21          (trailing zeros drop)
1534236469   →  0           (reversed = 9_646_324_351 > INT_MAX)
```

**Constraints:** `-2³¹ ≤ x ≤ 2³¹ − 1`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Pop-and-push with pre-multiply overflow check | O(log₁₀ \|x\|) time, O(1) space | [`reverse.kara`](reverse.kara) ✓ via `karac run` / `karac build` | [`reverse.py`](reverse.py) ✓ | [`bench/reverse.rs`](bench/reverse.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 14 test cases.

## Why pop-and-push

The textbook formulation walks digits least-significant first:

```
digit  = x % 10
result = result * 10 + digit
x      = x / 10
```

Three operations per digit, all in registers, no allocation. The interesting part is the overflow check, not the digit walk.

### The overflow rails

Doing the multiply first and checking after won't work — the multiply itself is the overflow event. The check has to fire *before* the multiply, against `INT_MAX / 10` and `INT_MIN / 10`:

```
if result >  INT_MAX / 10                                       { return 0; }
if result == INT_MAX / 10 and digit > 7                         { return 0; }
if result <  INT_MIN / 10                                       { return 0; }
if result == INT_MIN / 10 and digit < -8                        { return 0; }
```

The boundary digits (`7` and `-8`) are the last digits of `INT_MAX = 2_147_483_647` and `INT_MIN = -2_147_483_648`. Any input whose reverse fits in i32 cleanly skips both rails; any input that overflows trips one of them before the offending multiply runs.

### Why one loop covers both signs

Kāra's `%` follows C/Rust semantics — the sign of the result matches the *dividend*:

```
(-123) % 10 == -3       (not 7, as Python would give)
(-123) /  10 == -12     (truncated toward zero)
```

So a single `while x != 0` loop walks negatives correctly without a sign flip — `digit` carries the sign of `x`, and `result * 10 + digit` accumulates a negative reversed value. Python's `%` floors instead, so [`reverse.py`](reverse.py) defines `c_div` / `c_mod` helpers to mirror the truncated-division shape. Without that mirror the Python output would diverge on every negative input.

## Kāra features exercised

- **`i32` arithmetic end-to-end** — `let result: i32 = 0i32`, `let digit: i32 = x % 10i32`, comparisons against typed constants like `7i32` and `-8i32`. The LeetCode constraint ("the environment does not allow 64-bit integers") maps directly to keeping every variable in `i32`; the kata refuses to widen to `i64` even for the check.
- **Truncated `%` and `/`** — Kāra inherits Rust's sign-of-dividend modulo, which is what the algorithm needs. The Python mirror has to emulate this with `c_div` / `c_mod` because Python's operators floor instead.
- **Compound boolean guards** — `result > max_div or (result == max_div and digit > 7i32)`. Mixed `or`/`and` with parens parses as expected; the lowering short-circuits both `or` and `and` arms.
- **Early `return` with typed literal** — `return 0i32` inside a function declared `-> i32`. The literal suffix is load-bearing here — bare `0` would be inferred as `i64` and trip a codegen type-mismatch.
- **`println(r)` on a narrow signed int** — direct print of an `i32` renders the signed decimal in both the interpreter and the codegen path. Pre-fix, codegen formatted the value as unsigned (e.g. `-123` printed as `4_294_967_173`) because the printf arm passed the raw `i32` to `%lld` and LLVM zero-padded the varargs slot. The 2026-05-19 codegen fix routes narrow ints through `sext + %lld` (signed) or `zext + %llu` (unsigned) based on the source-level type — surfaced while writing this kata, landed alongside it.

No `Vec`, no `String`, no `Map`, no shared structs — pure scalar arithmetic.

## Edge cases worth exercising

| Input | Expected | Why it's interesting |
|---|---|---|
| `0` | `0` | The `while x != 0` loop body never runs; `result` stays at its `0` init. |
| `1` / `-1` | `1` / `-1` | Single iteration; tests the negative path skips no rail. |
| `10` / `-10` | `1` / `-1` | Trailing-zero drop — `10 % 10 == 0` so the first iter contributes `0`, second iter contributes `1`. |
| `120` | `21` | Trailing-zero drop on a multi-digit input. |
| `1463847412` | `2147483641` | Just under `INT_MAX` — exercises the boundary without tripping it. |
| `1463847413` | `0` | Same shape, last digit increments — should trip the `digit > 7` rail at the boundary. |
| `1534236469` | `0` | Overflows comfortably — trips the `result > max_div` rail before the boundary check. |
| `2147483647` | `0` | `INT_MAX` itself — reversed is `7463847412`, overflows. |
| `-2147483648` | `0` | `INT_MIN` — reversed is `-8463847412`, trips the `min_div` rail. |
| `-1463847412` | `-2147483641` | Mirror of the just-under-INT_MAX case, against the negative rail. |

All 14 cases run in `main` and the output is diffed against [`reverse.py`](reverse.py).

## API shape

`reverse(x: i32) -> i32` is the algorithm; `report(x: i32)` prints the result; `main` calls `report` per test case. Logic is separated from I/O so the function would slot into a future test harness unchanged. The Python file mirrors this with `reverse(x: int) -> int` and the same `report` / `main` shape.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   reverse.kara
karac build reverse.kara && ./reverse

# Python
python3 reverse.py

# Verify they agree
diff <(./reverse) <(python3 reverse.py) && echo OK
diff <(karac run reverse.kara) <(python3 reverse.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs hyperfine for runtime + cold-compile, plus straight `wc` / `time -l` reads for binary size + memory. Python is timed in a separate stanza at K = 1M and projected to K = 50M (a full python sample at K = 50M is ~80 s, too slow for the iterative dev loop).

| File | What it does |
|---|---|
| [`bench/reverse.kara`](bench/reverse.kara) | N = 1024 LCG-fill i32 inputs, K = 50,000,000 outer iters, sink = Σ reverse(inputs[k % N]) as i64 |
| [`bench/reverse.py`](bench/reverse.py) | Algorithmic mirror — same N, K, same LCG fill, same sink formula |
| [`bench/reverse.rs`](bench/reverse.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sink (`-292_465_958_482_676` at the default parameters) so the algorithm's output participates in I/O and can't be elided. The bench's `bench.sh` asserts the kara and rust sinks match before timing; the python stanza prints its own sink (different K, expectedly different value).

### Runtime — parity with Rust (within run-to-run variance)

Snapshot — M5 Pro, 2026-05-19, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`. Requires karac at commit [`4abe70c`](../../../../karac-rust/) (`println` signedness fix — without it the natural `println(r)` on an `i32` prints the unsigned representation) or later.

| Run | Mean ± σ |
|---|---|
| `kara reverse` (codegen) | 418.8 ± 1.8 ms |
| `rust reverse` | 427.6 ± 2.3 ms |
| `py   reverse` (K = 1M, ×50 projection) | 82,765 ms (~83 s projected) |

This kata is **at parity with Rust** within run-to-run variance — kara codegen lands 1.02× ahead at this snapshot, but the within-σ range (kara 416.9–423.5, rust 425.7–433.3) overlaps the bound enough that the directional ratio could bounce on the next reading. The honest claim is parity.

The per-call body is six i32 ops in the common path (mod, two compares for the rails, mul-add, div, loop-back) over ≤10 iters per call. With 50M outer iters and a 1024-entry input array that fits in L1, the algorithm is the bottleneck — no Vec allocations after the one-time input fill, no I/O, no syscalls. Both compilers see the same shape and produce the same arm64 sequence within a couple of fused-multiply-add bundles, which is why the gap is sub-σ.

### Codegen vs Python

Python is **~197× slower than Kāra codegen** at the same K (extrapolated from the K = 1M sample at 1655 ms). The reverse() body is dominated by CPython's per-bytecode dispatch — `c_mod` / `c_div` are pure-python helpers (no `divmod` shortcut for negatives gives the right answer here) so each loop iter spends ~5–10 µs in interpreter overhead vs a handful of nanoseconds in the codegen path. The gap is wider than kata [#6](../6-zigzag-conversion/#codegen-vs-python)'s ~32× because there's no C-implemented `list.append` doing the heavy lifting — every operation is at the bytecode level.

### Runtime memory — parity with Rust

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara reverse` (codegen) | 1.1 MiB |
| `rust reverse` | 1.1 MiB |

Both impls are at the binary-base RSS — the algorithm's working set is one `Vec[i32]` of 1024 entries (4 KiB) plus a handful of scalar locals, well below the steady-state allocator overhead.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-19, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build reverse.kara` | 51.7 ± 0.9 ms | 49.0 KiB |
| `rustc -O reverse.rs` | 73.8 ± 0.9 ms | 455.6 KiB |

Kāra compiles this kata **1.43× faster** than `rustc -O` and produces a binary **~9.3× smaller**. Consistent with the trend across katas [#4](../4-median-of-two-sorted-arrays/#compile-time-and-binary-size), [#6](../6-zigzag-conversion/#compile-time-and-binary-size), [#88](../88-merge-sorted-array/#compile-time-and-binary-size), and [#121](../121-best-time-to-buy-and-sell-stock/#compile-time-and-binary-size) — karac's smaller binary tracks the cross-archive LTO + DCE work landed 2026-05-12.

Compile memory: karac peaks at **8.8 MiB** vs rustc's **26.9 MiB** — ~3× lower compile-time RAM, which matters more at scale (many files in parallel) than for a single-file bench like this one.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. The current result — **parity with Rust on runtime, ~9× smaller binary, ~1.4× faster compile, ~3× lower compile RAM** — shipped on the first bench reading; no follow-up tuning required.
