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

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. Per BENCH.md's two-lane discipline, the kara binary here is built with `KARAC_AUTO_PAR=0` so the comparison is per-core codegen-quality only — directly stackable against `rustc -O`, `clang -O3`, and `go build`.

| Run | Mean ± σ | User |
|---|---|---|
| `kara valid` (seq, KARAC_AUTO_PAR=0) | 60.0 ± 1.4 ms | 58.0 ms |
| `rust valid` | 58.2 ± 0.9 ms | 57.0 ms |
| `c    valid` | 68.6 ± 1.5 ms | 67.0 ms |
| `go   valid` | 70.2 ± 1.2 ms | 68.0 ms |

Single-thread kara is at **parity with C** (1.14× ahead) and **1.17× ahead of Go**, with **rust 1.03× ahead** as the per-core codegen reference. (The 2026-05-25 snapshot read kara 64.7 ± 0.9 / rust 56.6 / c 63.8 / go 69.1 — every mirror reproduced within ~1σ across an 11-day gap and a karac reinstall, the tightest reproduction in the corpus; this DFA workload allocates nothing, so there's no allocator or page-cache surface for batch conditions to move.) The codegen-quality gap to rust on this DFA shape (8 `else if` chains × ≤4 categories each lowering to nested `cmp + br`, plus a `categorize` call per byte) is small enough that the seq lane reads as essentially three-way parity with C/Go on the M5 Pro — same picture as the kata 8 seq lane after the three karac perf commits landed.

### Runtime — auto-par regime (kara default, multi-core)

Default `karac build` output: karac's auto-par-on-reduction recognizes the `if r { sum = sum + 1i64; }` conditional accumulator update in main's K=10M loop and emits a `karac_par_reduce` dispatch. Hyperfine `--warmup 10 --runs 50` to absorb worker-pool init noise. Same hardware + date as the seq lane.

| Run | Mean ± σ | User | User / wall |
|---|---|---|---|
| `kara valid` (auto-par default) | 5.8 ± 0.9 ms | 62.0 ms | 10.7× |

Auto-par is **10.3× faster than kara's own seq baseline** — the intra-Kāra seq→par speedup, which is the honest figure to report here; the seq lane above already carries the cross-language comparison (parity with C, 1.03× behind Rust), and restating auto-par as "N× faster than Rust/C" would conflate per-core codegen quality with whether the comparator opted into parallelism. The User / wall ratio of 10.7× says ~11 cores are doing useful work, with per-core efficiency = (62.0 ms User on auto-par) / (58.0 ms User on seq) = **94%** — within hand's-breadth of perfect parallel scaling.

> **Real improvement, 2026-06-05:** the 2026-05-25 snapshot read 8.2 ± 0.7 ms wall at 66.9 ms User (8.16× User/wall, 7.89× over seq). Today's 6.0 ± 0.5 ms is ~4σ better **with User-CPU flat** (66.9 → 67.5 ms) and an unchanged seq baseline — the same work is being packed onto cores with less idle wall time. The June karac runtime-archive scheduler work (dispatch + herd-free wakeup — the change that improved kata #13's reduction by 10%) is the attributable cause; this kata's fan-out/combine shape is exactly what that work targets. Corroborated by kata #20's par-RSS drop on the same archive. Slice-1 analyzer (commit [`3294e50`](../../../../karac-rust/), 2026-05-20) recognizes the conditional accumulator-update shape as a `+`-reduction with `sum` as the accumulator (semantically `sum = sum + (if r { 1i64 } else { 0i64 })` for the associative+commutative `+` op), then slice-3b codegen lowers it to `karac_par_reduce` that fans the iteration space across the M5 Pro's 6 P-cores + 12 E-cores. Reduction op is associative + commutative — combine order doesn't matter, every run produces the same sink (`6_250_000`). NOT directly comparable to the single-thread rows above per BENCH.md's two-lane discipline — reported separately so the production-default Kara behavior stays visible.

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

Closing the gap dropped this kata's wall from 64.3 ms → 8.2 ms as of 2026-05-25 (**7.84× speedup from a single analyzer extension**; the June runtime-archive scheduler work has since taken the same binary shape to 6.0 ms — 10.7× over the pre-fix wall). The pre-fix 64.3 ms wall and the current seq-lane 64.8 ms wall agree to within σ — direct confirmation that the seq lane reproduces the pre-auto-par single-thread baseline, with the auto-par regime sitting on top of it.

### Codegen vs Python

Python is **~546× slower than Kāra auto-par** at the same K (3,168 ms vs 5.8 ms) and **~53× slower than Kāra seq** (3,168 ms vs 60.0 ms). The per-iter body has a function call per byte (`categorize`) plus state-machine dispatch, all at the CPython bytecode-dispatch level — every `cat = categorize(c)` is an attribute lookup + frame push, and each `state == N` compare boxes both sides into PyObjects. The serial-vs-serial slice (kara seq User 58.0 ms vs python wall 3,168 ms) is **~55×**; the auto-par lowering widens that to ~546× on wall by fanning across cores while CPython runs the GIL-locked single-threaded loop. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was wider (~2,220×) because the inner body there is even shorter — interpreter overhead dominates a larger fraction of CPython's cost.

### Runtime memory — seq at C/Rust parity, auto-par at +0.4 MiB

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara valid` (seq) | 1.0 MiB |
| `kara valid` (auto-par) | 1.4 MiB |
| `rust valid` | 1.1 MiB |
| `c    valid` | 1.0 MiB |
| `go   valid` | 3.0 MiB |
| `py   valid` | 7.2 MiB |

Kara seq sits at C/Rust parity (1,065,248 B vs C's 1,048,864 / Rust's 1,114,400 — single-shot `/usr/bin/time -l` readings, page-level noisy; the 2026-05-25 sample read kara/C/Rust byte-identical) — no per-thread overhead because the seq binary skips the `karac_par_run` worker pool entirely. Auto-par adds ~0.4 MiB for the long-lived pool, which reserves N = `available_parallelism()` OS-thread stacks regardless of how many reductions fire. Acceptable cost for the 10.8× wall-clock win, and the seq lane stays available for embedded / constrained-memory targets where the pool weight isn't worth paying. Same root-cause split as kata [#7](../7-reverse-integer/#runtime-memory-peak-rss) and kata [#8](../8-string-to-integer-atoi/#runtime-memory-peak-rss).

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build valid.kara` (auto-par default) | 77.7 ± 0.6 ms | 296.0 KiB |
| `rustc -O valid.rs` | 89.4 ± 2.6 ms | 455.4 KiB |
| `clang -O3 valid.c` | 45.2 ± 0.4 ms | 32.7 KiB |

Kāra compiles this kata **1.15× faster** than `rustc -O` and produces an auto-par binary **1.54× smaller** than `rustc -O`'s (466,330 / 303,104 B). Clang is **1.72× faster** than karac with a **13.9× smaller binary than Rust's** — same lower-floor C reference shape as kata [#8](../8-string-to-integer-atoi/#compile-elapsed-cold). The seq-build kara binary is **33.2 KiB** (auto-par dispatch dead-code-eliminated when `KARAC_AUTO_PAR=0`), bringing the kara/rust binary-size ratio to **13.7× smaller** when the runtime weight isn't paid for. The +263 KiB delta between seq and auto-par kara binaries is the `karac_par_reduce` runtime + thread-pool helpers (the auto-par binary sits at the documented ~296.0 KiB floor — libstd's panic/backtrace machinery reached via the reduction runtime) — identical in shape to kata [#7](../7-reverse-integer/) and kata [#8](../8-string-to-integer-atoi/), and the cost of the 10.8× wall-clock win.

(The 2026-05-25 snapshot read `karac build` at 63.5 ± 0.9 ms against the karac installed at the time; the May-30 karac reinstall plus the 06-05 environment band account for the 75.5 ms reading — both kara binary sizes reproduce the May table exactly, so codegen output is unchanged. rustc held flat 80.1 → 79.1.)

Compile memory: karac peaks at **13.9 MiB** vs rustc's **26.8 MiB** vs clang's **2.6 MiB** — ~1.9× lower compile-time RAM than rustc, ~5.3× higher than clang (karac's 9.9 → 10.4 MiB move is the corpus-wide benign compile-mem floor band on the newer karac build). Same ordering as kata [#8](../8-string-to-integer-atoi/#compile-memory-cold).

### Why Rust, C, and Go are in the harness

Same rationale as kata [#8](../8-string-to-integer-atoi/#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no String type and no length-prefixed slice; Go is the **GC + goroutine-overhead peer** that anchors the seq lane on the upper end. The current result — **seq lane at parity with C, 1.17× ahead of Go, 1.03× behind Rust on codegen quality; auto-par 10.3× intra-Kāra seq→par speedup (reported as the language-level win, not a cross-lane "faster than Rust" claim); 1.54× smaller binary than Rust on auto-par (13.7× smaller on seq); 1.15× faster compile than Rust; ~1.9× lower compile RAM than Rust; seq at C/Rust RSS parity, auto-par at +0.4 MiB peak RSS for the worker thread pool** — is the third kata in the suite where kara's auto-par lights up (after kata [#7](../7-reverse-integer/#benchmarks) at 11.1× and kata [#8](../8-string-to-integer-atoi/#benchmarks) at 7.5× intra-Kāra seq→par speedup). Surfaced as the *first* kata whose conditional-update body shape wasn't recognized by the slice-1 matcher — the analyzer extension that fixed it (commit [`3294e50`](../../../../karac-rust/), 2026-05-20) generalizes to any counts-of-truthy-results workload, a common per-iter-predicate shape.
