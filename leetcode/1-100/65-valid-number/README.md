# 65. Valid Number

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/valid-number](https://leetcode.com/problems/valid-number/)

Given a string `s`, return `true` if `s` is a valid number. A valid number can be split up into these components (in order):

1. A *decimal number* or an *integer*.
2. (Optional) An `'e'` or `'E'`, followed by an *integer*.

A *decimal number* is an optional sign character (`+`/`-`) followed by one of:
- one or more digits, then `'.'`
- one or more digits, then `'.'`, then one or more digits
- `'.'`, then one or more digits

An *integer* is an optional sign character followed by one or more digits.

```
"0"           →  true
"-0.1"        →  true
"+3.14"       →  true
"4."          →  true        (digits-then-dot is a decimal)
"-.9"         →  true        (dot-then-digits is also a decimal)
"2e10"        →  true
"-90E3"       →  true
"53.5e93"     →  true
"e"           →  false       (no integer or decimal before exp)
"."           →  false       (dot alone is not a number)
"99e2.5"      →  false       (exponent must be an integer)
"--6"         →  false       (only one sign allowed)
```

**Constraints:** `1 ≤ s.length ≤ 20`, `s` consists of English letters (upper- and lowercase), digits `0–9`, and `+`, `-`, `.` — no whitespace inside the alphabet, so leading/trailing space is itself a reject.

## Approaches

| Approach | Complexity | Kāra | Python | Rust | C | Go |
|---|---|---|---|---|---|---|
| 8-state DFA over `s.bytes()` with category-based transitions | O(n) time, O(1) extra space (zero-copy byte view) | [`valid.kara`](valid.kara) ✓ via `karac run` / `karac build` | [`valid.py`](valid.py) ✓ | [`bench/valid.rs`](bench/valid.rs) ✓ (bench quint) | [`bench/valid.c`](bench/valid.c) ✓ (bench quint) | [`bench/go-seq/main.go`](bench/go-seq/main.go) ✓ (bench quint) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 29 test cases.

## Why a DFA, not regex or ad-hoc branching

The grammar has eight distinct "places we can be in" while reading the string — *before any input*, *after a sign*, *inside the integer part*, *just after a dot*, *inside a fraction*, *just after `e`/`E`*, *after a sign in the exponent*, *inside the exponent*. Each place has a fixed set of categories it accepts (`digit`, `sign`, `dot`, `exp`, `other`) and a fixed next state for each accepted category. That's the textbook shape of a deterministic finite automaton; expressing it as a state table is shorter, faster, and more obviously correct than any nested `if`/`else if` over the input position.

A regex would also work (`^[+-]?((\d+\.?\d*)|(\.\d+))([eE][+-]?\d+)?$`) but pulls in a regex runtime and an O(n) match overhead per call. An ad-hoc branching version drifts toward bugs at the boundary cases (`"4."` vs `".4"` vs `".e1"`) because the structure of "what's been seen so far" lives implicitly in which line of code is executing. The DFA makes it explicit. The header comment in [`valid.kara`](valid.kara) carries the state legend and accepting set.

## Kāra features exercised

- **`ref String` + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view over the String's UTF-8 storage; LeetCode alphabet is pure ASCII so byte == codepoint.
- **`u8` byte-literal constants in comparisons** — `b'0'`, `b'+'`, `b'e'`, etc. (design.md § Byte and Byte-String Literals — lex-time-rejected for non-ASCII).
- **`and` / `or` short-circuit** — digit-range guards (`b >= b'0' and b <= b'9'`) and sign/exp checks shortcut on the first false.
- **Long `if`/`else if` chains as a jump table** — design.md has no `switch`, so the 9 outer states × ≤4 categories each lower to nested `cmp` + `br`.
- **Early `return false` inside a `while` over `Slice[u8]`** — the loop exits the function directly on the first invalid transition; no break flag needed.

No `Vec`, no `Map`, no shared structs — `Slice[u8]` view + scalar i32 state machine.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   valid.kara
karac build valid.kara && ./valid

# Python
python3 valid.py

# Verify they agree
diff <(./valid) <(python3 valid.py) && echo OK
diff <(karac run valid.kara) <(python3 valid.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go file with `go build`, and the Kāra file twice — default `karac build` (auto-par regime) plus a second `KARAC_AUTO_PAR=0 karac build` (seq lane, apples-to-apples with `rustc -O` / `clang -O3` / `go build`). All cached in `bench/target/`, gitignored. Hyperfine runs the two lanes as separate sub-runs; straight `wc` / `time -l` reads cover binary size + memory. Python is timed in a long-workload pass at the same K = 10M.

| File | What it does |
|---|---|
| [`bench/valid.kara`](bench/valid.kara) | N = 8 distinct inputs cycled by `k % N` (every DFA path exercised), K = 10,000,000 outer iters, sink = count of accepted inputs (i64) |
| [`bench/valid.py`](bench/valid.py) | Algorithmic mirror — same N, K, same input set, same sink formula |
| [`bench/valid.rs`](bench/valid.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/valid.c`](bench/valid.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |

The N = 8 inputs are picked to exercise every transition path through the DFA so no single branch dominates the predictor's history — single-byte accept (`"0"`), sign + bare-dot + fractional (`"-.9"`), full grammar (`"53.5e93"`), exponent with sign (`"+6e-1"`), early reject at state 0 (`"abc"`), accept-prefix-into-non-accepting-EOF (`"1e"`), mid-stream reject inside exponent (`"99e2.5"`), and the longest valid case (`"-123.456e789"`). 5 of the 8 are valid numbers so each 8-input cycle adds 5 to the sink; K = 10M / 8 cycles × 5 = **6,250,000** at the default parameters. All five compiled impls print the same sink before timing.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 5 --runs 30 --shell=none`. Per BENCH.md's two-lane discipline, the kara binary here is built with `KARAC_AUTO_PAR=0` so the comparison is per-core codegen-quality only — directly stackable against `rustc -O`, `clang -O3`, and `go build`.

| Run | Mean ± σ | User |
|---|---|---|
| `kara valid` (seq, KARAC_AUTO_PAR=0) | 64.7 ± 0.9 ms | 62.8 ms |
| `rust valid` | 56.6 ± 0.6 ms | 54.8 ms |
| `c    valid` | 63.8 ± 1.1 ms | 61.9 ms |
| `go   valid` | 69.1 ± 0.8 ms | 66.7 ms |

Single-thread kara is at **parity with C** (1.01× ahead) and **1.07× ahead of Go**, with **rust 1.14× ahead** as the per-core codegen reference. The codegen-quality gap to rust on this DFA shape (8 `else if` chains × ≤4 categories each lowering to nested `cmp + br`, plus a `categorize` call per byte) is small enough that the seq lane reads as essentially three-way parity with C/Go on the M5 Pro — same picture as the kata 8 seq lane after the three karac perf commits landed.

### Runtime — auto-par regime (kara default, multi-core)

Default `karac build` output: karac's auto-par-on-reduction recognizes the `if r { sum = sum + 1i64; }` conditional accumulator update in main's K=10M loop and emits a `karac_par_reduce` dispatch. Hyperfine `--warmup 10 --runs 50` to absorb worker-pool init noise. Same hardware + date as the seq lane.

| Run | Mean ± σ | User | User / wall |
|---|---|---|---|
| `kara valid` (auto-par default) | 8.2 ± 0.7 ms | 66.9 ms | 8.16× |

Auto-par is **7.89× faster than kara's own seq baseline**, **6.90× faster than rust**, and **7.78× faster than c**. The User / wall ratio of 8.16× says ~8 cores are doing useful work, with per-core efficiency = (66.9 ms User on auto-par) / (62.8 ms User on seq) = **94%** — within hand's-breadth of perfect parallel scaling. Slice-1 analyzer (commit [`3294e50`](../../../../karac-rust/), 2026-05-20) recognizes the conditional accumulator-update shape as a `+`-reduction with `sum` as the accumulator (semantically `sum = sum + (if r { 1i64 } else { 0i64 })` for the associative+commutative `+` op), then slice-3b codegen lowers it to `karac_par_reduce` that fans the iteration space across the M5 Pro's 6 P-cores + 12 E-cores. Reduction op is associative + commutative — combine order doesn't matter, every run produces the same sink (`6_250_000`). NOT directly comparable to the single-thread rows above per BENCH.md's two-lane discipline — reported separately so the production-default Kara behavior stays visible.

The outer loop body that lights this up:

```kara
let r: bool = is_number(inputs[idx]);
if r {
    sum = sum + 1i64;
}
```

Rust and C stay single-threaded — neither `rustc -O` nor `clang -O3` auto-parallelizes the analogous for-loop without explicit rayon / OpenMP annotation, and `go build` doesn't either (the Go mirror is intentionally a single goroutine for the seq comparison).

### Pre-fix snapshot — how the auto-par gap surfaced

**Pre-2026-05-20 snapshot** (same hardware, same workload, karac before commit [`3294e50`](../../../../karac-rust/)): kara 64.3 ± 1.1 ms wall / User 62.5 ms (User ≈ wall — no parallelism). The analyzer reported `<no parallelization opportunities detected>` because its reduction-pattern matcher recognized `acc = acc + EXPR` but rejected the conditional shape `if cond { acc = acc + DELTA }`, even though the two forms are semantically equivalent for any associative+commutative op with a known identity. The gap was purely in the assignment-site syntactic matcher — verified via a 22-line probe where rewriting the workload to `let val: i64 = if r { 1i64 } else { 0i64 }; sum = sum + val;` *did* trigger recognition.

Per the project's `no workarounds — fix the compiler` discipline, the workload kept its natural shape and the analyzer was extended (commit [`3294e50`](../../../../karac-rust/)) with a new `conditional_acc_update_shape` matcher that lifts single-arm `if cond { acc = acc + delta }` (and the trivially-equivalent two-arm form with an empty else) to the unconditional reduction. Three guards prevent unsoundness: the else branch must be empty, the then-block must be exactly one update statement of the recognized shape, and the condition must not read the accumulator (otherwise the per-iter decision is order-dependent and not preserved by the fan-out / combine model).

Closing the gap dropped this kata's wall from 64.3 ms → 8.2 ms (**7.84× speedup from a single analyzer extension**), moving kara from 1.15× slower than rust to 6.90× faster on wall. The pre-fix 64.3 ms wall and today's seq-lane 64.7 ms wall agree to within σ — direct confirmation that the seq lane reproduces the pre-auto-par single-thread baseline, with the auto-par regime sitting on top of it.

### Codegen vs Python

Python is **400× slower than Kāra auto-par** at the same K (3,276 ms vs 8.2 ms) and **51× slower than Kāra seq** (3,276 ms vs 64.7 ms). The per-iter body has a function call per byte (`categorize`) plus state-machine dispatch, all at the CPython bytecode-dispatch level — every `cat = categorize(c)` is an attribute lookup + frame push, and each `state == N` compare boxes both sides into PyObjects. The serial-vs-serial slice (kara seq User 62.8 ms vs python wall 3,276 ms) is **~52×**; the auto-par lowering widens that to 400× on wall by fanning across cores while CPython runs the GIL-locked single-threaded loop. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was wider (~2,220×) because the inner body there is even shorter — interpreter overhead dominates a larger fraction of CPython's cost.

### Runtime memory — seq at C/Rust parity, auto-par at +0.4 MiB

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara valid` (seq) | 1.1 MiB |
| `kara valid` (auto-par) | 1.5 MiB |
| `rust valid` | 1.1 MiB |
| `c    valid` | 1.1 MiB |
| `go   valid` | 2.9 MiB |
| `py   valid` | 7.3 MiB |

Kara seq matches C/Rust **byte-for-byte** at 1.1 MiB — no per-thread overhead because the seq binary skips the `karac_par_run` worker pool entirely. Auto-par adds ~0.4 MiB for the long-lived pool, which reserves N = `available_parallelism()` OS-thread stacks regardless of how many reductions fire. Acceptable cost for the 7.89× wall-clock win, and the seq lane stays available for embedded / constrained-memory targets where the pool weight isn't worth paying. Same root-cause split as kata [#7](../7-reverse-integer/#runtime-memory--slightly-above-rust-worker-thread-overhead) and kata [#8](../8-string-to-integer-atoi/#runtime-memory-peak-rss).

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build valid.kara` (auto-par default) | 63.5 ± 0.9 ms | 311.9 KiB |
| `rustc -O valid.rs` | 80.1 ± 0.8 ms | 455.4 KiB |
| `clang -O3 valid.c` | 43.4 ± 0.7 ms | 32.7 KiB |

Kāra compiles this kata **1.26× faster** than `rustc -O` and produces an auto-par binary **1.46× smaller** than `rustc -O`'s. Clang is **1.47× faster** and produces a binary **9.5× smaller** — same lower-floor C reference shape as kata [#8](../8-string-to-integer-atoi/#compile-elapsed-cold). The seq-build kara binary is **49.0 KiB** (auto-par dispatch dead-code-eliminated when `KARAC_AUTO_PAR=0`), bringing the kara/rust binary-size ratio to **9.3× smaller** when the runtime weight isn't paid for. The +263 KiB delta between seq and auto-par kara binaries is the `karac_par_reduce` runtime + thread-pool helpers — identical in shape to kata [#7](../7-reverse-integer/) and kata [#8](../8-string-to-integer-atoi/), and the cost of the 7.89× wall-clock win.

Compile memory: karac peaks at **9.9 MiB** vs rustc's **26.8 MiB** vs clang's **2.6 MiB** — ~2.7× lower compile-time RAM than rustc, ~3.8× higher than clang. Same ordering as kata [#8](../8-string-to-integer-atoi/#compile-memory-cold).

### Why Rust, C, and Go are in the harness

Same rationale as kata [#8](../8-string-to-integer-atoi/#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no String type and no length-prefixed slice; Go is the **GC + goroutine-overhead peer** that anchors the seq lane on the upper end. The current result — **seq lane at parity with C, 1.07× ahead of Go, 1.14× behind Rust on codegen quality; auto-par 6.90× faster than Rust on wall, 7.78× faster than C on wall; 1.46× smaller binary than Rust on auto-par (9.3× smaller on seq); 1.26× faster compile than Rust; ~2.7× lower compile RAM than Rust; seq at C/Rust RSS parity, auto-par at +0.4 MiB peak RSS for the worker thread pool** — is the third kata in the suite where kara's auto-par lights up against serial baselines (after kata [#7](../7-reverse-integer/#benchmarks) at 11.18× and kata [#8](../8-string-to-integer-atoi/#benchmarks) at 6.92×). Surfaced as the *first* kata whose conditional-update body shape wasn't recognized by the slice-1 matcher — the analyzer extension that fixed it (commit [`3294e50`](../../../../karac-rust/), 2026-05-20) generalizes to any counts-of-truthy-results workload, a common per-iter-predicate shape.
