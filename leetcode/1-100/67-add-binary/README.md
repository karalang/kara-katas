# 67. Add Binary

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math, String, Bit Manipulation, Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/add-binary](https://leetcode.com/problems/add-binary/)

Given two binary strings `a` and `b`, return their sum as a binary string.

```
a = "11",    b = "1"     →  "100"
a = "1010",  b = "1011"  →  "10101"
```

**Constraints:** `1 ≤ a.length, b.length ≤ 10⁴`; each string is `'0'`/`'1'`
with no leading zeros except the value `"0"` itself.

## Why this kata — the lexer's radix arm

The corpus's most direct hit on the self-hosted lexer's **number-parsing
surface**. Adding two binary strings runs the exact digit arithmetic
`from_str_radix` walks for a `0b…` literal — `b - b'0'` digit-value extraction
and base-N carry — at base 2, where the carry logic is at its purest.

| Lexer surface | This kata |
|---|---|
| **digit char → value** (`from_str_radix`, the `0x`/`0b`/`0o` arms) | `(b - b'0') as i64` over `b'0'`/`b'1'` byte literals |
| **base-N accumulation / carry** | `sum = carry + da + db`; `bit = sum % 2`; `carry = sum / 2` |
| **byte-indexed scan of `Vec[u8]`** (§1) | two pointers walking `a.bytes()` / `b.bytes()` from the right |
| **token-text emit** (§2 push, §3 slice) | char-literal `push('0')`/`push('1')` into the answer |

This is item #4 of the [lexer-stress order](../../../../kara/docs/implementation_checklist/phase-12-self-hosting.md)
(paired with [#415 add-strings](../../401-500/415-add-strings/), the base-10
sibling): base-2 isolates the carry machinery; base-10 adds the 10-symbol digit
table.

## Approaches

Two styles, both byte-identical to the Python oracle across all 11 cases,
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Two-pointer — LSB-first + reverse** ★ | [`add_binary.kara`](add_binary.kara) | walk both ends inward; push bits into a `Vec[u8]`, reverse into the answer |
| Recursive descent | [`add_binary_recursive.kara`](add_binary_recursive.kara) | `add_at(i, j, carry) -> String` recurses on the higher-order bits first, then appends the current bit — MSB-first, no reversal |
| Reference oracle | [`add_binary.py`](add_binary.py) | known-correct LeetCode answer |

Both read the operands through the zero-copy [`bytes()`](../../../README.md)
view with `b'0'`/`b'1'` byte literals — no per-char allocation on the scan
side. The two-pointer style emits least-significant first and reverses a
`Vec[u8]` of bit values; the recursive style lets the call stack carry the
order, so it emits MSB-first with no buffer.

## What this kata uncovered

**Flat curve — no `karac` bug.** The whole radix surface compiled and ran
first-try under both backends: two-pointer `Vec[u8]` scan, `(b - b'0') as i64`
digit widening, `% 2` / `/ 2` carry arithmetic, `Vec[u8]` push/index/reverse,
char-literal `String.push`, recursion with a `(i, j, carry)` frame, and the
`f"…\"{a}\"…"` escaped-quote interpolation in `report`. This is the same
flat-curve signal the array/string katas gave — the base-2 carry machinery sits
on codegen primitives the earlier katas (#7 reverse-integer, #8 atoi, #394
decode-string) already hardened.

One **correct-by-design** rejection worth recording for the lexer port: a
direct `byte as char` cast is a typecheck error (`E_INT_AS_CHAR` — not every
`u8` is a valid scalar). Because `karac run` bypasses typecheck, an `as char`
slip would *silently* yield an empty string rather than fault — so the digit
emit uses a char literal (`push('0')`) here and a digit-table slice in #415,
never a byte→char cast. Caught with `karac check` (full typecheck) before
trusting `karac run` output.

## Kāra features exercised

- **`bytes()` byte classification + indexing** — `b'0'`/`b'1'` byte literals,
  two-pointer reverse walk over `Vec[u8]`, `(b - b'0') as i64` widening cast.
- **Base-N carry arithmetic** — `sum % 2` / `sum / 2` integer division and
  modulo, the `from_str_radix` core at base 2.
- **`Vec[u8]` accumulate + reverse** — push bit values LSB-first, walk back to
  front to emit (two-pointer style).
- **Char-literal `String.push`** — `push('0')` / `push('1')`, the two-symbol
  emit (no digit table needed at base 2).
- **Recursion with a scalar frame** — `add_at(i, j, carry)` recurses on the
  high-order bits before appending the current one (recursive style).

---

**Bug ledger:** flat curve — this kata surfaced no `karac` defect. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md) for the running count.
