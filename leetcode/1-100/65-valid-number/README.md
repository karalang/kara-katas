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
- **`u8` comparisons against char-derived constants** — `b >= zero and b <= nine`, `b == plus`, `b == lower_e or b == upper_e`. Each constant is `'x' as u32 as u8` per design.md (the direct `'x' as u8` cast is rejected because the Unicode scalar range doesn't fit in 8 bits). Comparisons are unsigned and total over `u8`.
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

### Runtime — single-thread codegen, within 1.15× of Rust

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build`, `rustc -O`, and `clang -O3`. Auto-par reduction did **not** fire on this workload (see the next subsection); these are single-thread numbers across the board.

| Run | Mean ± σ | User |
|---|---|---|
| `rust valid` | 56.1 ± 0.8 ms | 54.7 ms |
| `c    valid` | 63.6 ± 1.6 ms | 62.3 ms |
| `kara valid` (codegen) | 64.3 ± 1.1 ms | 62.5 ms |
| `py   valid` | 3,227 ± 48 ms | 3,205 ms |

Ratios: rust is **1.13× faster than c**, **1.15× faster than kara**, **57× faster than python**. Kara is ~tied with C on the per-call work and ~15% behind Rust — the gap to Rust is driven by Rust's tighter inlining of `is_ascii_digit()` plus the `&str` `.as_bytes()` no-op, where Kara still pays for `s.bytes()` returning a `Slice[u8]` view object. The kata 8 single-thread perf commits (const-prop captures, assume non-neg loop var, BCE-hoist via modulo) all apply equally here — they're general per-worker codegen wins, not par-reduce-specific.

User ≈ wall (User 62.5 ms / wall 64.3 ms ≈ 1.0× CPU usage) — confirming the workload ran fully serial on a single core.

### Why auto-par didn't fire — analyzer doesn't recognize conditional accumulator updates

`karac build --concurrency-report bench/valid.kara` reports `<no parallelization opportunities detected>`. The body of the outer loop is:

```kara
let r: bool = is_number(inputs[idx]);
if r {
    sum = sum + 1i64;
}
```

The slice-1 analyzer's reduction-pattern matcher recognizes `acc = acc + EXPR` as a reducible add-accumulator but does not recognize the **conditional accumulator update** `if cond { acc = acc + DELTA }` — even though it's semantically equivalent to `acc = acc + (if cond { DELTA } else { 0 })`, which the analyzer **does** accept.

Verified via a 22-line probe (single bool function + a sum loop): rewriting the same workload as `let val: i64 = if r { 1i64 } else { 0i64 }; sum = sum + val;` produces `reduction { op: +, accumulator: sum }` and triggers the auto-par lowering. So the gap is purely in the assignment-site shape matcher: it looks at the syntactic form of the accumulator update rather than the data-flow contribution per iteration.

Closing this gap is a karac slice (extend the analyzer to lift single-arm `if cond { acc = acc + delta }` and `if cond { acc = acc + delta } else { /* nothing */ }` to the unconditional reduction shape). Once that lands, this kata should pick up the same ~9-10× wall-clock multiplier kata [#8](../8-string-to-integer-atoi/#benchmarks) gets — the per-iter work shape is similar (single-call body over an 8-input table) and the call cost is enough to amortize thread-spawn overhead.

The README intentionally **does not** rewrite the source to the `if cond { delta } else { 0 }` workaround. Per the project's `no workarounds — fix the compiler` discipline, the workload's natural shape is the test case; the analyzer extends to recognize it.

### Codegen vs Python

Python is **57× slower than Kāra codegen** at the same K (3,227 ms vs 64.3 ms). The per-iter body has a function call per byte (`categorize`) plus state-machine dispatch, all at the CPython bytecode-dispatch level — every `cat = categorize(c)` is an attribute lookup + frame push, and each `state == N` compare boxes both sides into PyObjects. Even with no auto-par advantage on the kara side, the codegen single-thread baseline beats CPython by ~57× on this shape. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was wider (~2,220×) because (a) the inner body there is even shorter and (b) auto-par fanned the work across cores there; the serial-vs-serial slice (kara user time vs python wall) was ~151×.

### Runtime memory — at parity with C/Rust

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara valid` (codegen) | 1.1 MiB |
| `rust valid` | 1.1 MiB |
| `c    valid` | 1.1 MiB |
| `py   valid` | 7.3 MiB |

Kara is at parity with rust and c here — no worker thread stacks because auto-par didn't fire. (Kata [#8](../8-string-to-integer-atoi/#runtime-memory--slightly-above-rust-worker-thread-overhead) and [#7](../7-reverse-integer/#runtime-memory--slightly-above-rust-worker-thread-overhead) both carry a +0.3 to +0.4 MiB delta for the `karac_par_reduce` pool reservations.) Closing the analyzer gap above will move kara to that +0.3 MiB shape; that's an acceptable cost for the wall-clock win.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-20, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build valid.kara` | 55.7 ± 0.4 ms | **49.0 KiB** |
| `rustc -O valid.rs` | 76.4 ± 1.5 ms | 455.4 KiB |
| `clang -O3 valid.c` | 38.8 ± 0.4 ms | 32.7 KiB |

Kāra compiles this kata **1.37× faster** than `rustc -O` and produces a binary **9.3× smaller**. Clang is **1.44× faster** and produces a binary **1.5× smaller** — same lower-floor C reference shape as kata [#8](../8-string-to-integer-atoi/#compile-time-and-binary-size).

The 49 KiB kara binary is notably small because **auto-par didn't fire** so the `karac_par_reduce` runtime + thread-pool helpers are dead-code-eliminated out. Compare kata [#8](../8-string-to-integer-atoi/) (312 KiB) and kata [#7](../7-reverse-integer/) (312 KiB), which both link in the par-reduce runtime. Once the analyzer gap above is closed, this binary will grow to a similar ~312 KiB — the runtime weight is the cost of the auto-par win.

Compile memory: karac peaks at **9.6 MiB** vs rustc's **26.8 MiB** vs clang's **2.6 MiB** — ~2.8× lower compile-time RAM than rustc, ~3.7× higher than clang. Same ordering as kata [#8](../8-string-to-integer-atoi/#compile-time-and-binary-size).

### Why Rust and C are in the harness

Same rationale as kata [#8](../8-string-to-integer-atoi/#why-rust-and-c-are-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no String type and no length-prefixed slice. The current result — **1.15× slower than Rust on wall (no auto-par), ~tied with C on wall, 9.3× smaller binary than Rust, 1.37× faster compile than Rust, ~2.8× lower compile RAM than Rust, at-parity peak RSS** — is the first kata where kara's auto-par analyzer **misses** a workload that should reduce. Closing the analyzer gap is tracked as a separate karac slice; once it lands this README's `runtime` table will move to the `kara dominant on wall, ~1.3× of c on single-thread user` shape kata [#8](../8-string-to-integer-atoi/#runtime--692-ahead-of-rust-750-ahead-of-c-via-auto-par-reduction) lands.
