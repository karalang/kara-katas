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

| Approach | Complexity | Kāra | Python | Rust | C |
|---|---|---|---|---|---|
| 8-state DFA over `s.bytes()` with category-based transitions | O(n) time, O(1) extra space (zero-copy byte view) | [`valid.kara`](valid.kara) ✓ via `karac run` / `karac build` | [`valid.py`](valid.py) ✓ | [`bench/valid.rs`](bench/valid.rs) ✓ (bench quad) | [`bench/valid.c`](bench/valid.c) ✓ (bench quad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 29 test cases.

## Why a DFA, not regex or ad-hoc branching

The grammar has eight distinct "places we can be in" while reading the string — *before any input*, *after a sign*, *inside the integer part*, *just after a dot*, *inside a fraction*, *just after `e`/`E`*, *after a sign in the exponent*, *inside the exponent*. Each place has a fixed set of categories it accepts (`digit`, `sign`, `dot`, `exp`, `other`) and a fixed next state for each accepted category. That's the textbook shape of a deterministic finite automaton; expressing it as a state table is shorter, faster, and more obviously correct than any nested `if`/`else if` over the input position.

A regex would also work (`^[+-]?((\d+\.?\d*)|(\.\d+))([eE][+-]?\d+)?$`) but pulls in a regex runtime and an O(n) match overhead per call. An ad-hoc branching version drifts toward bugs at the boundary cases (`"4."` vs `".4"` vs `".e1"`) because the structure of "what's been seen so far" lives implicitly in which line of code is executing. The DFA makes it explicit.

### States and accepting set

```
0: start
1: sign seen, awaiting integer-or-dot
2: integer digits accumulated                          (accepting)
3: dot with no preceding digit, awaiting fractional
4: dot with preceding digit                            (accepting)
5: fractional digits                                   (accepting)
6: 'e' / 'E' seen, awaiting optional sign + exponent integer
7: sign after 'e', awaiting exponent integer
8: exponent digits                                     (accepting)
```

State 2 is accepting because `"42"` is a valid integer.
State 4 is accepting because `"4."` is a valid decimal (digits-then-dot, no fractional required).
State 5 is accepting because `".9"` and `"3.14"` are valid decimals (the dot was either preceded by digits — state 4→5 — or not — state 3→5).
State 8 is accepting because the exponent must have at least one digit; once any digit is seen we land here.

Notice **state 3 is not accepting** — `"."` alone is invalid because no digit ever joined the fraction; you need to leave state 3 by consuming a digit (`→ 5`) before end-of-input.
Notice **state 6 is not accepting** — `"1e"` is invalid; the exponent integer is required.

### One pass, one byte at a time

The whole loop is `for each byte: cat = categorize(byte); state = transition[state][cat]; if no transition: return false;`. Categorize runs in O(1) (five comparisons against ASCII range / literal bytes), transitions are O(1), so the total cost is one pass + O(1) per byte. No backtracking, no lookahead — the DFA recognition is single-pass by construction.

## Kāra features exercised

- **`ref String` parameter + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view over the String's UTF-8 storage. The LeetCode alphabet (`[A-Za-z0-9+\-.]`) is pure ASCII, so each byte is the codepoint and `bytes[i]` is the right primitive. Same `ref String` borrow shape as kata [#8](../8-string-to-integer-atoi/).
- **`-> bool` return type with `false` / `true` literals** — `is_number` returns `bool` directly; the early-`return false` inside each state arm exits the loop as soon as the input proves invalid. `println` interpolates the bool via f-string (`f"{is_number(s)}"`) which renders `true`/`false` in lowercase.
- **`u8` byte-literal constants in comparisons** — `b >= b'0' and b <= b'9'`, `b == b'+'`, `b == b'e' or b == b'E'`. Each constant is a `b'X'` byte literal (type `u8`, per design.md § Byte and Byte-String Literals — lex-time-rejected for non-ASCII). Comparisons are unsigned and total over `u8`.
- **`and` / `or` short-circuit** — `b >= zero and b <= nine` shortcuts the second compare when the first fails, matching the behavior the digit-range check needs.
- **Long `if`/`else if` chains in a tight inner loop** — the DFA dispatch (9 outer states × up to 4 categories each) lowers to nested `cmp` + `br` in LLVM. design.md doesn't have a `switch` statement so `if`/`else if` is the explicit-jump-table replacement; clippy-equivalent karac lints don't flag the chain since it has no shared structure to factor.
- **Early `return false` from inside a `while` over a `Slice[u8]`** — the loop's outer `while i < n` doesn't need an explicit `break` for the reject case; returning `false` exits the function directly.
- **Multi-statement `if` blocks on one line** — `if cat == 0i32 { state = 2i32; }` keeps the transition table dense and grep-friendly. Kara accepts a single semicolon-terminated statement inside braces on the same line as the brace; this is the same shape design.md uses in compound `if/else if` blocks elsewhere.

No `Vec`, no `Map`, no shared structs — `Slice[u8]` view + scalar i32 state machine.

## Edge cases worth exercising

| Input | Expected | Why it's interesting |
|---|---|---|
| `"0"` | `true` | Single digit — minimal accepting integer. |
| `"0089"` | `true` | Leading zeros are fine — the spec doesn't require canonical form. |
| `"-0.1"` / `"+3.14"` | `true` | Sign + decimal with both integer and fractional parts. |
| `"4."` | `true` | Digits-then-dot is a decimal; state 4 must accept. |
| `"-.9"` | `true` | Dot-then-digits is also a decimal; state 5 (via 3) must accept. |
| `"2e10"` / `"-90E3"` | `true` | Exponent on an integer; both lowercase and uppercase `e` work. |
| `"3e+7"` / `"+6e-1"` | `true` | Sign inside the exponent — state 6 → 7 → 8 path. |
| `"53.5e93"` | `true` | Decimal + exponent — covers the full grammar. |
| `"-123.456e789"` | `true` | Sign on the decimal *and* unsigned exponent — longest valid case. |
| `"abc"` | `false` | All `OTHER` — state 0 rejects immediately. |
| `"1a"` | `false` | Digit then letter — state 2 has no `OTHER` transition. |
| `"1e"` | `false` | Exponent without integer — state 6 is not accepting. |
| `"e3"` | `false` | Exp at start — state 0 has no `EXP` transition. |
| `"99e2.5"` | `false` | Dot inside exponent — state 8 has no `DOT` transition. |
| `"--6"` | `false` | Double sign — state 1 has no `SIGN` transition. |
| `"-+3"` | `false` | Mixed sign — same reason as `"--6"`. |
| `"95a54e53"` | `false` | Letter in the middle of digits — state 2 has no `OTHER` transition. |
| `"."` | `false` | Dot alone — state 3 is not accepting. |
| `".e1"` | `false` | Dot then exp with no fractional digit between — state 3 has no `EXP` transition. |
| `"+."` | `false` | Sign + dot with no digits anywhere — state 3 is not accepting. |
| `"+"` | `false` | Sign alone — state 1 is not accepting. |
| `"4e+"` | `false` | Exponent sign with no exponent digits — state 7 is not accepting. |
| `"6+1"` | `false` | Sign mid-stream, not after `e` — state 2 has no `SIGN` transition. |
| `" 1"` / `"1 "` | `false` | Space is not in the alphabet — `OTHER` from any state rejects. |

All 29 cases run in `main` and the output is diffed against [`valid.py`](valid.py).

## API shape

`is_number(s: ref String) -> bool` is the algorithm; `report(s: ref String)` prints the result; `main` calls `report` per case. Logic is separated from I/O so the function would slot into a future test harness unchanged. The Python file mirrors this with `is_number(s: str) -> bool` and the same `report` / `main` shape.

Each Kāra `main` case passes its string literal directly to `report` — `ref String` accepts any source per design.md § Part 1½ Rule 4, and the codegen materializes the literal into a stack temp at the call site automatically.

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

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then runs hyperfine for runtime + cold-compile, plus straight `wc` / `time -l` reads for binary size + memory. Python is timed in the same hyperfine pass at the same K = 10M.

| File | What it does |
|---|---|
| [`bench/valid.kara`](bench/valid.kara) | N = 8 distinct inputs cycled by `k % N` (every DFA path exercised), K = 10,000,000 outer iters, sink = count of accepted inputs (i64) |
| [`bench/valid.py`](bench/valid.py) | Algorithmic mirror — same N, K, same input set, same sink formula |
| [`bench/valid.rs`](bench/valid.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/valid.c`](bench/valid.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |

The N = 8 inputs are picked to exercise every transition path through the DFA so no single branch dominates the predictor's history — single-byte accept (`"0"`), sign + bare-dot + fractional (`"-.9"`), full grammar (`"53.5e93"`), exponent with sign (`"+6e-1"`), early reject at state 0 (`"abc"`), accept-prefix-into-non-accepting-EOF (`"1e"`), mid-stream reject inside exponent (`"99e2.5"`), and the longest valid case (`"-123.456e789"`). 5 of the 8 are valid numbers so each 8-input cycle adds 5 to the sink; K = 10M / 8 cycles × 5 = **6,250,000** at the default parameters. All four impls print the same sink before timing.

### Runtime — 6.21× ahead of Rust, 7.12× ahead of C, via auto-par reduction

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build`, `rustc -O`, and `clang -O3`. Requires karac at commit [`3294e50`](../../../../karac-rust/) (analyzer extension that recognizes the conditional accumulator-update shape `if cond { acc = acc + delta }`, landed 2026-05-20) or later.

| Run | Mean ± σ | User |
|---|---|---|
| `kara valid` (codegen) | 8.9 ± 0.2 ms | 67.1 ms |
| `rust valid` | 55.6 ± 0.6 ms | 54.2 ms |
| `c    valid` | 63.6 ± 1.1 ms | 62.1 ms |
| `py   valid` | 3,241 ± 35 ms | 3,220 ms |

Ratios: kara is **6.21× faster than rust**, **7.12× faster than c**, **362× faster than python**.

CPU utilization tells the parallelism story: hyperfine's reading is **User 67.1 ms / wall 8.9 ms ≈ 7.5× CPU usage** — close to perfect parallel scaling on the per-iter call shape. The outer loop body is

```kara
let r: bool = is_number(inputs[idx]);
if r {
    sum = sum + 1i64;
}
```

— a conditional accumulator update. The slice-1 analyzer recognizes this as a `+`-reduction with `sum` as the accumulator (treating it as semantically equivalent to `sum = sum + (if r { 1i64 } else { 0i64 })` for the associative+commutative `+` op), then the slice-3b codegen lowers it to a `karac_par_reduce` call that fans the iteration space across the M5 Pro's 6 P-cores + 12 E-cores. The reduction op is associative + commutative, so combine order doesn't matter — every run produces the same sink (`6_250_000`).

Rust and C stay single-threaded — neither `rustc -O` nor `clang -O3` auto-parallelizes the analogous for-loop without explicit rayon / OpenMP annotation. The kata 8 per-worker single-thread perf commits (const-prop captures, assume non-neg loop var, BCE-hoist via modulo) all apply equally here, so the per-worker user-time-divided-by-CPU-count tracks kata 8's shape.

### Pre-fix snapshot — how the auto-par gap surfaced

**Pre-2026-05-20 snapshot** (same hardware, same workload, karac before commit [`3294e50`](../../../../karac-rust/)): kara 64.3 ± 1.1 ms wall / User 62.5 ms (User ≈ wall — no parallelism). The analyzer reported `<no parallelization opportunities detected>` because its reduction-pattern matcher recognized `acc = acc + EXPR` but rejected the conditional shape `if cond { acc = acc + DELTA }`, even though the two forms are semantically equivalent for any associative+commutative op with a known identity. The gap was purely in the assignment-site syntactic matcher — verified via a 22-line probe where rewriting the workload to `let val: i64 = if r { 1i64 } else { 0i64 }; sum = sum + val;` *did* trigger recognition.

Per the project's `no workarounds — fix the compiler` discipline, the workload kept its natural shape and the analyzer was extended (commit [`3294e50`](../../../../karac-rust/)) with a new `conditional_acc_update_shape` matcher that lifts single-arm `if cond { acc = acc + delta }` (and the trivially-equivalent two-arm form with an empty else) to the unconditional reduction. Three guards prevent unsoundness: the else branch must be empty, the then-block must be exactly one update statement of the recognized shape, and the condition must not read the accumulator (otherwise the per-iter decision is order-dependent and not preserved by the fan-out / combine model).

Closing the gap dropped this kata's wall from 64.3 ms → 8.9 ms (**7.2× speedup from a single analyzer extension**), moving kara from 1.15× slower than rust to 6.21× faster.

### Codegen vs Python

Python is **362× slower than Kāra codegen** at the same K (3,241 ms vs 8.9 ms). The per-iter body has a function call per byte (`categorize`) plus state-machine dispatch, all at the CPython bytecode-dispatch level — every `cat = categorize(c)` is an attribute lookup + frame push, and each `state == N` compare boxes both sides into PyObjects. The serial-vs-serial slice (kara user time 67.1 ms vs python wall 3,241 ms) is **~48×**; the auto-par lowering widens that to 362× on wall by fanning across cores while CPython runs the GIL-locked single-threaded loop. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was wider (~2,220×) because the inner body there is even shorter — interpreter overhead dominates a larger fraction of CPython's cost.

### Runtime memory — slightly above Rust (worker thread overhead)

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara valid` (codegen) | 1.5 MiB |
| `rust valid` | 1.1 MiB |
| `c    valid` | 1.1 MiB |
| `py   valid` | 7.2 MiB |

Kara is ~0.4 MiB above the C/Rust baseline. Same root cause as kata [#7](../7-reverse-integer/#runtime-memory--slightly-above-rust-worker-thread-overhead) and kata [#8](../8-string-to-integer-atoi/#runtime-memory--slightly-above-rust-worker-thread-overhead): the `karac_par_reduce` call dispatches onto the long-lived `karac_par_run` pool, which reserves N = `available_parallelism()` OS-thread stacks regardless of how many reductions fire. Acceptable cost for the 6.21× wall-clock win — pre-fix this kata was at 1.1 MiB parity with C/Rust precisely *because* auto-par didn't fire and the pool wasn't initialized.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build valid.kara` | 58.0 ± 0.3 ms | 311.9 KiB |
| `rustc -O valid.rs` | 75.5 ± 0.5 ms | 455.4 KiB |
| `clang -O3 valid.c` | 39.1 ± 0.5 ms | 32.7 KiB |

Kāra compiles this kata **1.30× faster** than `rustc -O` and produces a binary **1.46× smaller**. Clang is **1.48× faster** and produces a binary **9.5× smaller** — same lower-floor C reference shape as kata [#8](../8-string-to-integer-atoi/#compile-time-and-binary-size).

The kara binary is 311.9 KiB — same shape as kata [#8](../8-string-to-integer-atoi/) (312 KiB) and kata [#7](../7-reverse-integer/) (312 KiB), all linking in the `karac_par_reduce` runtime + thread-pool helpers. Pre-fix snapshot (auto-par didn't fire): the binary was 49 KiB because the runtime got dead-code-eliminated. The +263 KiB delta is the runtime weight, and the cost of the 6.21× wall-clock win.

Compile memory: karac peaks at **9.8 MiB** vs rustc's **26.8 MiB** vs clang's **2.6 MiB** — ~2.7× lower compile-time RAM than rustc, ~3.8× higher than clang. Same ordering as kata [#8](../8-string-to-integer-atoi/#compile-time-and-binary-size).

### Why Rust and C are in the harness

Same rationale as kata [#8](../8-string-to-integer-atoi/#why-rust-and-c-are-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no String type and no length-prefixed slice. The current result — **6.21× faster than Rust on wall, 7.12× faster than C on wall, 1.46× smaller binary than Rust, 1.30× faster compile than Rust, ~2.7× lower compile RAM than Rust, +0.4 MiB peak RSS for the worker thread pool** — is the third kata in the suite where kara's auto-par lights up against serial baselines (after kata [#7](../7-reverse-integer/#benchmarks) at 11.18× and kata [#8](../8-string-to-integer-atoi/#benchmarks) at 6.92×). Surfaced as the *first* kata whose conditional-update body shape wasn't recognized by the slice-1 matcher — the analyzer extension that fixed it (commit [`3294e50`](../../../../karac-rust/), 2026-05-20) generalizes to any counts-of-truthy-results workload, a common per-iter-predicate shape.
