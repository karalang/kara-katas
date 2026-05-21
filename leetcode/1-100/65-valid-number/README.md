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

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| 8-state DFA over `s.bytes()` with category-based transitions | O(n) time, O(1) extra space (zero-copy byte view) | [`valid.kara`](valid.kara) ✓ via `karac run` / `karac build` | [`valid.py`](valid.py) ✓ |

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
