# 29. Divide Two Integers

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math, Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/divide-two-integers](https://leetcode.com/problems/divide-two-integers/)

Given two integers `dividend` and `divisor`, divide them **without using multiplication, division, or the modulo operator** and return the quotient truncated toward zero (so `8 / 3 == 2` and `-8 / 3 == -2`).

**Constraints:** both operands are 32-bit signed integers in `[−2³¹, 2³¹ − 1]`, and the divisor is non-zero. The quotient is clamped to that same range: the only result that overflows it is `−2³¹ / −1 = 2³¹`, which saturates to `2³¹ − 1` (`INT_MAX`).

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Bit-shift long division (double-and-subtract) | O(log²n) time, O(1) space | [`bit_shift.kara`](bit_shift.kara) ✓ | [`bit_shift.py`](bit_shift.py) ✓ |

## Why shifting beats repeated subtraction

The naïve "subtract the divisor until you can't" is O(quotient) — up to ~2 billion iterations for `2³¹ / 1`, which times out. The bit-shift method removes one *bit* of the quotient per outer step instead of one *unit*: it doubles the divisor (`temp << 1`) and a running `multiple` (also a shift) until one more doubling would overshoot the remaining dividend, then subtracts that largest shifted divisor and adds its multiple to the result. Each outer pass strips the top set bit of what remains, so the whole thing is O(log²n) compares — no multiply, no divide, no modulo.

Two integer-boundary details carry the correctness:

- **Sign is an XOR of the operand signs.** `(dividend < 0) != (divisor < 0)` is exactly that XOR — `!=` on two `bool`s — computed once, applied at the end.
- **Magnitudes live in i64.** `|INT_MIN| = 2³¹` does not fit back into a signed 32-bit value, so negating it would overflow. Holding both magnitudes in `i64` makes `−dividend` always representable, and the single genuinely-overflowing result (`INT_MIN / −1`) is special-cased and saturated *before* any negation runs. This is the one structural difference from sibling kata [#7 (reverse integer)](../7-reverse-integer/README.md), where the overflow check guards an accumulating product rather than a one-shot negation.

## Kāra features exercised

- **Bit-shift operator `<<`** — the doubling search (`temp << 1`, `multiple << 1`) is the core of the algorithm; the first kata in this group whose hot loop is shift-driven rather than index-driven.
- **`!=` on `bool` as XOR** — `(dividend < 0) != (divisor < 0)` derives the quotient's sign without a branch.
- **Early `return` plus a tail `if`-expression** — the `INT_MIN / −1` guard returns early; the function's value is the tail `if negative { -result } else { result }`, an expression, not a statement.
- **Unary negation under default overflow checking** — `-a`, `-b`, `-result` all run with Kāra's arithmetic-overflow trapping on (design.md § Arithmetic Overflow); i64 magnitudes keep every negation in range so none can trap.
- **Nested `while` loops over scalars** — no arrays, no slices: the whole kata is integer ALU and control flow.

## Running

```bash
karac run bit_shift.kara
python3 bit_shift.py
diff <(karac run bit_shift.kara) <(python3 bit_shift.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go mirror with `go build`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then runs runtime, compile-cost (cold, via a `--prepare` delete step), binary-size, and peak-RSS passes.

| File | What it does |
|---|---|
| [`bench/bit_shift.kara`](bench/bit_shift.kara) | N = 5_000_000 `divide()` calls over LCG-generated `(dividend, divisor)` pairs; sums every quotient |
| [`bench/bit_shift.py`](bench/bit_shift.py) | Algorithmic mirror — same N, LCG, truncating bit-shift divide (not Python's flooring `//`) |
| [`bench/bit_shift.rs`](bench/bit_shift.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/bit_shift.c`](bench/bit_shift.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |

Each of the 5M calls draws a fresh pair from the classic glibc LCG (`a = 1103515245, c = 12345, m = 2³¹`, seeded 1): the dividend spans the signed-31-bit range (`state − 2³⁰`) and the divisor is a small non-zero magnitude in `[−1000, 999]` (zero remapped to 1). Small divisors mean large quotients, so each call's doubling loop does real work (~up to ~20 shifts), and because the dividend and quotient magnitudes vary unpredictably across calls, the `a >= (temp << 1)` test is a genuine data-dependent branch rather than a fixed trip count the predictor can learn. Every implementation steps the identical generator in plain `i64` arithmetic, so all five see byte-identical inputs and print the same sink (the running sum of all quotients); `bench.sh` fails loudly on any mismatch. This is a **seq-only kata** — each LCG draw depends on the prior `state`, so the call stream is strictly serial with no auto-par surface.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded:

| Run | Mean ± σ | Gap |
|---|---|---|
| rust bit_shift | 312.0 ± 2.4 ms | 1.02× ahead of kāra |
| c    bit_shift (clang -O3) | 313.7 ± 2.9 ms | 1.01× ahead of kāra |
| **kāra bit_shift (codegen)** | **319.7 ± 2.4 ms** | — |
| go   bit_shift | 373.1 ± 5.8 ms | kāra 1.17× ahead of Go |

**Kāra is within 2% of both Rust and C** on a branch-bound integer kernel — and this is *with* integer-overflow trapping on by default (design.md § Arithmetic Overflow), which Rust's release build omits. There is no array indexing here, so unlike the array-compaction siblings ([#26](../26-remove-duplicates-from-sorted-array/README.md), [#27](../27-remove-element/README.md)) there is no bounds-check story; the only Kāra-specific cost is the overflow check on the loop body's `a − temp` / `result + multiple`. Those checks don't dominate because the data-dependent `while a >= (temp << 1)` compare and its mispredicts are the real bottleneck — the same regime for all four compilers, which is why they land within a hair of each other. The shifts themselves never trap.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara bit_shift` (codegen) | 319.7 ± 2.4 ms |
| `rust bit_shift` | 312.0 ± 2.4 ms |
| `py bit_shift` | 21622.3 ± 1076.5 ms |

Python is **~68× slower** than Kāra codegen — per-call CPython bytecode dispatch over a nested loop of compares, shifts, and subtractions, 5M times over.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build bit_shift.kara` | 69.1 ± 1.6 ms | 32.8 KiB |
| `rustc -O bit_shift.rs` | 71.6 ± 1.7 ms | 455.4 KiB |
| `clang -O3 bit_shift.c` | 40.8 ± 1.0 ms | 32.6 KiB |
| `go build` | — | 2434.1 KiB |

Kāra compiles this kata **1.04× faster** than `rustc -O` and produces a binary **~93% smaller** than Rust's — **within 144 bytes of C** (33,576 B vs 33,432 B; the delta is the overflow-trap landing pads). The workload reaches `println(i64)` and nothing else from the runtime — no `Vec`, no slice ops — so cross-archive LTO + DCE strips the runtime down to almost nothing, the same lean profile as kata [#27](../27-remove-element/README.md#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara bit_shift` (codegen) | 1.0 MiB |
| `c    bit_shift` | 1.0 MiB |
| `rust bit_shift` | 1.0 MiB |
| `go   bit_shift` | 2.6 MiB |
| `py bit_shift` | 6.8 MiB |

**Byte-identical to C** (1,032,480 B each) — there is no heap working set at all, just two `i64` accumulators and the LCG state, so peak RSS is essentially the loaded image. Rust's +65 KiB is its larger static image; Go's +1.6 MiB is GC arena + runtime; Python's 6.8 MiB is the interpreter itself.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (kāra reaches it here), Go is the cross-runtime data point, and Python is the ergonomic foil.
