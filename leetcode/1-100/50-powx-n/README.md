# 50. Pow(x, n)

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/powx-n](https://leetcode.com/problems/powx-n/)

Implement `pow(x, n)`, which raises the floating-point base `x` to the integer power `n`.

```
pow(2.00000, 10)    →  1024.00000
pow(2.10000,  3)    →  9.26100
pow(2.00000, -2)    →  0.25000     (2^-2 = 1/2² = 1/4)
```

**Constraints:** `-100 < x < 100`, `-2³¹ ≤ n ≤ 2³¹ - 1`, either `x ≠ 0` or `n > 0`, and the result
is within `-10⁴ … 10⁴`. LeetCode accepts any answer **within `1e-5`** of the true value — a detail
this kata leans on below.

## Why this kata — one idea (squaring), two multiply orders

A naive `x * x * … * x` loop is `O(n)`, and `n` can be `2³¹` — hopeless. **Exponentiation by
squaring** makes it `O(log |n|)` by halving the exponent at every step:

```
x^n = (x^(n/2))²           n even
x^n = (x^(n/2))² · x       n odd
```

Each step strips one bit off `n`, so `~log₂|n|` multiplications suffice. The two solvers here
implement the *same* recurrence but multiply their factors in a **different order**:

| Lens | What it squares | Direction |
|---|---|---|
| **Recursive** ★ | the **partial power** `x^(n/2)`, on the way back up (`half * half`) | top-down, halving `n` |
| **Iterative** | the **base** `x^(2^k)`, folding it in when bit *k* of `n` is set | bottom-up, over the bits of `n` |

Negative exponents use `x^n = 1 / x^(-n)`. The magnitude `-n` is taken in **`i64`** so that
`n = -2³¹` — whose magnitude `2³¹` does not fit back into `i32` — never traps under Kāra's default
arithmetic-overflow checking; `fast_pow` then only ever sees a non-negative exponent.

### The subtlety: two correct algorithms, one ULP apart

Real multiplication is associative, so both orders compute the same *real* number. But **IEEE-754
multiplication is not associative** — each product is rounded to the nearest representable double, and
a different multiply order rounds at different places. So on a base whose powers aren't exactly
representable, the two solvers can land **one ULP apart**:

```
2.1^13   recursive → 15447.237773911951      iterative → 15447.23777391195
1.00001^100  recursive → 1.0010004951617435   iterative → 1.0010004951617477
```

Both are correct to far better than LeetCode's `1e-5` tolerance — they simply aren't *bit*-identical.
This is not a Kāra quirk; the same divergence appears in C, Rust, Go, and Python when you write the
two orders out. It is the whole reason LeetCode grades `pow` on a tolerance rather than equality.

So that the kata stays **byte-diffable** against a single oracle, `main` pins test cases whose results
are **exactly representable** in `f64` — powers of two, integers, and `±1` — where the two orders (and
the Python oracle) agree bit-for-bit. The interesting inexact cases are documented above rather than
printed.

### Printing floats: Kāra uses Rust's `Display`, so the oracle mirrors it

This is the katas' **first float-output** problem, which surfaces a formatting gap against Python.
Kāra prints an `f64` with Rust's `Display`: the **shortest round-trip decimal**, in **plain (never
scientific)** notation, with a bare integer for integer-valued floats — `1024`, not `1024.0`; the
interpreter and codegen agree on this exactly. Python's `print` differs on both counts (`1024.0`,
`1e-05`, `9.5367431640625e-07`). The oracle's `kfmt` helper reproduces Rust's rule (expand any
exponent to plain decimal via `Decimal`, strip a trailing `.0`) so `powx_n.py` diffs byte-for-byte
against both Kāra backends. Because the oracle also mirrors the ★ solver's **exact** recursive
multiply order, the agreement is at the level of f64 *bits*, not just within tolerance.

## Approaches

| Approach | File | Squares |
|---|---|---|
| **Recursive** ★ | [`recursive.kara`](recursive.kara) | the partial power (`half * half`) |
| **Iterative** | [`iterative.kara`](iterative.kara) | the base (`base * base`), over the bits of `n` |
| Oracle | [`powx_n.py`](powx_n.py) | mirrors the recursive order + `kfmt` float formatter |

Everything below `fast_pow` is line-for-line identical between the two `.kara` files — the kata's
point is that the exponent handling is order-agnostic; only the squaring differs.

## What this kata surfaced

**A real codegen gap — now fixed in `karac`.** The solvers compiled clean the first time under both
`karac run` and `karac build`. The gap turned up building this kata's **benchmark**, whose diffable
cross-language sink sums each result's raw IEEE-754 bits (`.to_bits()`) into an integer:

```
error: codegen failed: codegen: no handler for method 'to_bits' on variable 'x'
```

`f64.to_bits()` / `.to_bits32()` and the inverse `i64.bits_as_f64()` / `.bits_as_f32()` had an
interpreter **and** typechecker implementation (they back the protobuf `float`/`double` codecs) but
**no codegen arm** — so a program that round-tripped an `f64` through its bit pattern *ran* under
`karac run` yet *failed* `karac build`: a run/build divergence for a general-purpose method.

Rather than route around it (a sink that avoids `to_bits`), **the compiler was fixed**: these four
methods now lower to **pure LLVM bitcasts** — `to_bits` is `bitcast f64→i64`; `to_bits32` rounds to
f32, bitcasts to i32, and zero-extends; `bits_as_*` width-normalize the receiver then bitcast to the
float. No runtime helper, no allocation, no new C symbol. The codegen result matches the interpreter
**byte-for-byte**, including the sign-bit-only `-0.0` pattern (`-9223372036854775808`). A regression
test pins it: `e2e_float_to_bits_codegen` (positive / `+0.0` / `-0.0`, a `bits_as_f64` round-trip, a
`to_bits32` + `bits_as_f32` round-trip, and the XOR/sum-fold the benchmark relies on).

See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) entry **B-2026-07-03-1**.

## Kāra features exercised

- **`f64` arithmetic + recursion** — the fast-power core; the first kata to print `f64` results.
- **`f64.to_bits()`** — the benchmark's diffable sink; the method this kata drove into codegen.
- **`i64` bit ops** — `e & 1`, `e >> 1`, `n / 2`, `n % 2` (the iterative bit walk).
- **`wrapping_add` on `u64`** — the non-trapping accumulator for the bit sum (benchmark).
- **`i64` INT_MIN handling** — `-n` for `n = -2³¹` taken in `i64` so the magnitude `2³¹` never traps.
- **`.to_f64()`** — exact `int → f64` conversion when building the benchmark's inputs.

## Running

```bash
# Kāra — interpreter and codegen produce the same output.
karac run   recursive.kara
karac build recursive.kara && ./recursive

# Python oracle
python3 powx_n.py

# Verify all three agree, byte-for-byte
diff <(karac run recursive.kara) <(python3 powx_n.py) && echo OK
diff <(karac run recursive.kara) <(karac run iterative.kara) && echo OK
```

Both solvers are byte-identical to the oracle under `karac run`, `karac build` (default auto-par),
and `KARAC_AUTO_PAR=0`.

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh          # KARA_BENCH_INCLUDE_PY=1 to include the Python row
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file
with `karac build` (`KARAC_AUTO_PAR=0`), and the Go module with `go build` (all cached in
`bench/target/`, gitignored), then times them with `hyperfine` per the
[BENCH.md protocol](../../../BENCH.md) and writes [`bench/results.json`](bench/results.json).

| File | What it does |
|---|---|
| [`bench/powbench.kara`](bench/powbench.kara) | recursive `fast_pow` over N×K `(x, n)` pairs, summing `.to_bits()` |
| [`bench/powbench.rs`](bench/powbench.rs) | mirror; `f64::to_bits`, `wrapping_add`; `rustc -O` |
| [`bench/powbench.c`](bench/powbench.c) | mirror; `memcpy` bit-reinterpret, `uint64_t` sum; `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | mirror; `math.Float64bits`, `uint64` sum; `go build` |
| [`bench/powbench.py`](bench/powbench.py) | mirror; `struct.pack/unpack` bits; CPython |

**Workload.** `N = 400_000` deterministic `(x, n)` pairs regrouped over `K = 20` reps (`8M`
fast-powers). `x = 1 + h/2048` with `h ∈ [0, 2047]` (a multiple of `2⁻¹¹`, exactly representable);
`n ∈ [-64, 64]`. Both inputs are perturbed by the rep index so the reps aren't identical (defeats
hoisting), and `x ∈ [1, 2)` with `|n| ≤ 64` keeps every result finite and normal. All five languages
fold each result's raw f64 bits into a wrapping 64-bit sum, masked to a non-negative integer — a
**bit-exact, cross-language-diffable sink** (`5910621068131449488`) that makes the pow kernel
observable without any float-formatting ambiguity.

**Seq-only kata.** The per-pair work is a short recursive chain of `f64` multiplies with no
cross-pair parallel structure the auto-par cost model engages, so the Kāra binary is built
`KARAC_AUTO_PAR=0` and the seq row is the apples-to-apples comparator against the native single-file
compilers.

### Runtime

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 5 --runs 30`, medians:

| Run | Median |
|---|---|
| `c    powbench` (clang -O3) | **44.5 ms** |
| `go   powbench` (go build)  | 52.9 ms |
| **`kara powbench` (codegen, seq)** | **73.1 ms** |
| `rust powbench` (rustc -O)  | 75.5 ms |
| `py   powbench` (CPython)   | 3458 ms |

The hot cost is the recursive `fast_pow` chain — `~log₂|n|` `f64` multiplies plus the `to_bits`
fold, run `N × K = 8M` times. Kāra is **essentially tied with Rust** here (1.03× *faster* at this
snapshot), lands **1.64× off C** and **1.38× off Go**, and is **47× faster than CPython**. C and Go
lead on how aggressively their backends flatten the recursive multiply chain; the within-abstraction
comparator — Rust — Kāra matches. The `f64.to_bits()` fold this bench depends on is the codegen arm
this kata added (see above); before the fix the benchmark could not be built at all.

### Compile time, binary size, memory

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 1 --runs 10` (compile, cold via `--prepare`);
size and peak RSS are single deterministic samples.

| Compiler | Compile (cold) | Binary | Peak RSS |
|---|---|---|---|
| `clang -O3` | 38.3 ms | 32.7 KiB | 1.00 MiB |
| **`karac build`** | **71.9 ms** | **32.9 KiB** | **1.02 MiB** |
| `rustc -O` | 69.8 ms | 455.0 KiB | 1.05 MiB |
| `go build` | — (excluded; mixes module + std-lib link) | 2434.2 KiB | 2.66 MiB |

Kāra emits a binary **~14× smaller than Rust** and line-ball with C (32.9 vs 32.7 KiB), and peaks at
**1.02 MiB RSS** — within a hair of C and Rust, ~2.6× under Go and ~6.7× under CPython. Its cold
compile is on par with `rustc -O` (both ~70 ms) and ~1.9× behind `clang`.
