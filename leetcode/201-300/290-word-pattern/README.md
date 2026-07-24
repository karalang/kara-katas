# 290. Word Pattern

Given a `pattern` of letters and a space-separated string `s`, decide whether the
letters map to the words following a **bijection**: each letter maps to exactly
one word and each word to exactly one letter, position by position.

`"abba"` + `"dog cat cat dog"` → true; `"abba"` + `"dog dog dog dog"` → false
(`a` and `b` would both map to `"dog"`).

## Approach

Split `s` into words, reject a length mismatch, then walk pattern and words in
lockstep with **two** maps — letter→word and word→letter. A conflict in *either*
direction (a letter already bound to a different word, or a word already bound to
a different letter) breaks the bijection.

## Compiler surfaces exercised

A deliberately collection/string-heavy kata: `Map[i64, String]`, `Map[String, i64]`,
`Vec[String]`, String equality, and `u8 as char` when building words from a
`Slice[u8]`. It surfaced a real compiler gap — `u8 as char` (the one infallible
integer→char cast) was wrongly rejected at typecheck, and the interpreter left it
an integer rather than a character — fixed in the sibling `kara` repo (ledger
`B-2026-07-24-3`).

## Files

- [`word_pattern.kara`](word_pattern.kara) — Kāra implementation.
- [`word_pattern.py`](word_pattern.py) — Python mirror (oracle).

Expected output (both): `true false false false true false` (one per line).
