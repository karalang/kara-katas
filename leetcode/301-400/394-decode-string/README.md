# 394. Decode String

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Stack, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/decode-string](https://leetcode.com/problems/decode-string/)

Decode `k[encoded]` runs, where the bracketed string repeats `k` times. Runs
nest.

```
"3[a]2[bc]"      →  "aaabcbc"
"3[a2[c]]"       →  "accaccacc"
"2[abc]3[cd]ef"  →  "abcabccdcdcdef"
```

**Constraints:** `1 ≤ s.length ≤ 30`; `s` is lowercase letters, digits, and
brackets; `1 ≤ k ≤ 300`; the decoded output fits in `10⁵`. Every `[` has a
matching `]`; the input is always valid.

## Why this kata — the lexer's escape / repeat machinery

The closest corpus analog to the self-hosted lexer's escape and repeat-count
handling. A single left-to-right byte scan drives the same three moves the
lexer makes when it reads `\u{1F600}` or a counted construct:

| Lexer surface | This kata |
|---|---|
| **digit-run → integer** (`from_str_radix`, the count/codepoint folds) | `k = k*10 + (b - b'0')` over a digit run |
| **nesting stack** (bracket / group depth) | `Vec[String]` + `Vec[i64]` parallel stacks (iterative) or the call stack (recursive) |
| **push / concat output storm** | `cur = prev + cur*count`, plus literal-run appends |
| **byte classification + token-text slice** (§1 + §3) | `is_letter` byte test + zero-copy `s[i..j]` letter-run append |

## Approaches

Two styles, both byte-identical to the Python oracle across all 14 cases,
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Iterative — explicit stacks** ★ | [`decode_string.kara`](decode_string.kara) | `Vec[String]`/`Vec[i64]` stacks; `]` pops + repeats |
| Recursive descent | [`decode_string_recursive.kara`](decode_string_recursive.kara) | `decode_at(s, start) -> (String, i64)`; `k[` recurses, returns segment + close position |
| Reference oracle | [`decode_string.py`](decode_string.py) | known-correct LeetCode answer |

Both follow the [lexer string-scan shape](../../../README.md): scan the line's
zero-copy `bytes()` view with `b'…'` byte literals, classify, and append each
letter run as **one zero-copy slice** `s[i..j]` — not char-by-char `push`. The
repeat step (`cur = prev + cur*count`) appends `cur` `count` times by **borrow**
(`newcur.push_str(cur)` in a loop reuses `cur`, never moving it).

## What this kata uncovered

**Nothing — and that's the signal.** This is the second kata on the
byte-indexed string-scan surface that #722 remove-comments hardened (the
`push_str(ref String)` / chained-`len` / fresh-owned-temp-leak fixes). Every
shape #394 leans on — byte classification, `(b - b'0') as i64` digit folding,
`Vec[String]` stack push/pop with `.unwrap()`, zero-copy `s[i..j]` slice
append, `push_str(cur)` reused-by-borrow in a loop, multi-value `(String, i64)`
return + destructure, and recursion — compiled and ran correctly on the first
probe under both backends. The flat-curve result the array/string katas gave is
holding across the lexer surface; the parser port can lean on it.

## Kāra features exercised

- **Zero-copy slice `s[i..j]` + `push_str`** — maximal letter-run append, no
  per-char `push`, no allocation (the lexer's token-text fast path).
- **`bytes()` byte classification** — `b'0'`/`b'9'`/`b'['`/`b']'` byte
  literals; `(b - b'0') as i64` digit-value widening cast.
- **Parallel `Vec[String]` / `Vec[i64]` stacks** — `push` / `pop().unwrap()`
  for the nesting levels (iterative style).
- **Multi-value return + destructure** — `decode_at` returns `(String, i64)`,
  `let (inner, after) = …` (recursive style).
- **Borrowed `push_str` in a loop** — `newcur.push_str(cur)` / `result.push_str(
  inner)` reuse the source by borrow across the repeat, never moving it.
