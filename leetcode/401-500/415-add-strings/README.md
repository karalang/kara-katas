# 415. Add Strings

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math, String, Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/add-strings](https://leetcode.com/problems/add-strings/)

Given two non-negative integers as decimal strings `num1` and `num2`, return
their sum as a string. You may **not** convert the inputs to integers directly
or use a bignum library — pure digit arithmetic.

```
"11"  + "123"  →  "134"
"456" + "77"   →  "533"
```

**Constraints:** `1 ≤ num1.length, num2.length ≤ 10⁴`; both contain only digits
and have no leading zero except `"0"` itself.

## Why this kata — base-10 radix arm + digit table

The base-10 sibling of [#67 add-binary](../../1-100/67-add-binary/). Same
column-add carry machinery, but base 10 brings in the piece base 2 didn't need:
a **digit table**. The emitted digit indexes a const `"0123456789"`, the inverse
nibble map of digit *parsing* — exactly the render shape #405 convert-to-hex and
#168 excel-column use to turn a value back into a glyph.

| Lexer surface | This kata |
|---|---|
| **digit char → value** (`from_str_radix`, the decimal int-literal arm) | `(b - b'0') as i64` over the operands' `bytes()` |
| **base-N accumulation / carry** | `sum = carry + da + db`; `digit = sum % 10`; `carry = sum / 10` |
| **value → digit glyph** (the inverse nibble map; §3 slice render) | `DIGITS[d..d+1]` one-byte zero-copy slice, `push_str` |
| **no-bignum constraint** | operands exceed any native int width; arithmetic stays per-digit |

This is item #4 of the [lexer-stress order](../../../../kara/docs/implementation_checklist/phase-12-self-hosting.md),
paired with #67: base-2 isolates the carry; base-10 adds the 10-symbol table.

## Approaches

Two styles, both byte-identical to the Python oracle across all 14 cases,
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Two-pointer — LSB-first + reverse** ★ | [`add_strings.kara`](add_strings.kara) | walk both ends inward; push digit values into a `Vec[i64]`, reverse and render through the digit table |
| Recursive descent | [`add_strings_recursive.kara`](add_strings_recursive.kara) | `add_at(i, j, carry) -> String` recurses on the higher-order digits first, then appends the current digit — MSB-first, no reversal |
| Reference oracle | [`add_strings.py`](add_strings.py) | known-correct LeetCode answer |

Both read the operands through the zero-copy [`bytes()`](../../../README.md)
view and emit each digit as a one-byte slice of the const table — no per-char
byte→char cast (which `karac check` rejects as `E_INT_AS_CHAR`; see below). The
two-pointer style buffers digit values LSB-first and reverses; the recursive
style lets the call stack carry the order and emits MSB-first.

## What this kata uncovered

**Flat curve — no `karac` bug.** Like its base-2 sibling, the whole base-10
surface compiled and ran first-try under both backends: `Vec[i64]` buffer,
`(b - b'0') as i64` widening, `% 10` / `/ 10` carry arithmetic, the
`DIGITS[d..d+1]` digit-table slice render via `push_str`, recursion with a
`(i, j, carry)` frame, and the long-operand cases that exceed any native int
width (the no-bignum point — proof the arithmetic really is per-digit). The
radix-render table sits on the same zero-copy-slice + `push_str` path #722
remove-comments already hardened.

The run-path footgun carried from #67 — [`B-2026-06-13-15`](../../../../kara/docs/bug-ledger.md):
emitting a digit with a `byte as char` cast is a typecheck *error*
(`E_INT_AS_CHAR`), but **`karac run` was type-lenient** — it downgraded hard type
errors to warnings and ran anyway with a placeholder value → silent wrong
output, exit 0. **Fixed in karac `b59eb070`:** `run` now aborts on the
value-corrupting cast family, matching `build`/`check` (soft type errors keep
their leniency). The emit is a digit-table slice regardless — the idiomatic form
— and the kata is gated on `karac check` before its `karac run` output is
trusted.

## Kāra features exercised

- **`bytes()` byte scan + indexing** — two-pointer reverse walk, `b'0'` byte
  literal, `(b - b'0') as i64` widening cast.
- **Base-10 carry arithmetic** — `sum % 10` / `sum / 10`, the decimal
  `from_str_radix` core; correct across operands wider than any native int.
- **Digit-table render** — `DIGITS[d..d+1]` one-byte zero-copy slice +
  `push_str`, the inverse nibble map of digit parsing (two-pointer + recursive
  both).
- **`Vec[i64]` accumulate + reverse** — buffer digit values LSB-first, walk
  back to front (two-pointer style).
- **Recursion with a scalar frame** — `add_at(i, j, carry)` recurses on the
  high-order digits before appending the current one (recursive style).

---

**Bug ledger:** the codegen/radix surface was a flat curve (no miscompile);
shares **`B-2026-06-13-15`** with #67 (the `karac run` type-leniency footgun on
the `byte as char` digit emit) — fixed (`b59eb070`): `run` now aborts on
value-corrupting casts. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
