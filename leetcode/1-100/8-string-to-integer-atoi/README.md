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

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| One-pass scan over `s.bytes()` with pre-multiply overflow rail | O(n) time, O(1) extra space (zero-copy byte view) | [`atoi.kara`](atoi.kara) ✓ via `karac run` / `karac build` | [`atoi.py`](atoi.py) ✓ |

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
- **`u8` comparisons against char-derived constants** — `bytes[i] == space`, `b < zero`, `b > nine`, etc., where each constant is `' ' as u32 as u8`. design.md rejects the direct `'x' as u8` cast (the Unicode scalar range doesn't fit in 8 bits); the `as u32 as u8` chain is the documented escape hatch for the ASCII-only inputs this kata's alphabet guarantees. Comparisons are unsigned and total over `u8`, which matches the ASCII-range guarantee.
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
