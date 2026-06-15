# UTF-8 Codepoints (bespoke — the L2 lexer-stress gap)

> **Bespoke kata** (not LeetCode) &nbsp;·&nbsp; **Topics:** UTF-8 decoding, Unicode scalar values, codepoint vs. byte counting, `char` classification

Given a UTF-8 string, report — per input — its **byte length**, its **codepoint
count**, each codepoint's **Unicode scalar value**, and a **letter / number /
other** tally:

```
"<s>" B<bytes> C<codepoints> | <scalar> <scalar> ... | L<letters> N<numbers> O<other>
```

## Why this kata — the one surface LeetCode can't reach

The self-hosted lexer ([`kara/selfhost/src/main.kara`](../../../kara/selfhost/src/main.kara))
is, by op-count, almost all byte-indexed ASCII scanning — and the corpus's
LeetCode katas cover that thoroughly. But the lexer also has a **multi-byte
(L2)** surface that LeetCode's ASCII-centric problems structurally cannot
exercise: reading a non-ASCII codepoint from its UTF-8 bytes, advancing the
cursor by codepoint (not byte), and classifying the codepoint with Unicode-aware
predicates. This kata is built to hammer exactly that surface.

| Self-hosted lexer move | Where in `main.kara` | This kata |
|---|---|---|
| **1..4 byte length from a lead byte** | `fn utf8_byte_len` | `utf8_byte_len` — identical `u8` range compares |
| **UTF-8 bytes → scalar value** | `scan_unicode_escape` / `char.try_from(cp)` | lead-mask + `cp = (cp << 6) \| (cont & 0x3F)` fold |
| **column advances ONE per codepoint** | `advance_codepoint` (`column += 1`, any width) | codepoint count, independent of byte width |
| **non-ASCII identifier-class dispatch** | `non_ascii_at_lead` (the `#13` classifier) | `char.is_alphabetic()` / `is_numeric()` tally |
| **codepoint → `char` → UTF-8 encode** | `\u{..}` escape body | `char.try_from(cp)` + `push(char)` (corpus build) |

## Dual oracle

Each line is checked against an **external known-correct answer**, not just
"interp == codegen agree": the [Python oracle](utf8_codepoints.py) computes the
codepoint count with `len(s)`, each scalar with `ord(c)`, and the classes with
`str.isalpha()` / `str.isnumeric()`. A bug both Kāra backends shared would be
invisible to agreement alone — `ord` / `len` catch it.

The corpus is defined as **explicit Unicode scalar-value lists** (not
source-level glyphs or escapes) so the byte sequence is editor-, terminal-, and
normalization-proof and provably identical, codepoint for codepoint, between the
Kāra programs and the oracle. It spans all four UTF-8 byte-lengths, the exact
length boundaries (U+007F/0080, U+07FF/0800, U+FFFF/10000, U+10FFFF), Latin /
Greek / Cyrillic / CJK letters, ASCII digits, and "other" symbols (emoji,
musical symbols, the middle dot).

## Approaches

Three styles, all byte-identical to the oracle under `karac run` **and**
`karac build`.

| Approach | File | Shape |
|---|---|---|
| **Byte-indexed manual decoder** ★ | [`utf8_codepoints.kara`](utf8_codepoints.kara) | decode each codepoint from the bytes by hand (`utf8_byte_len` + continuation fold), classify via `char.try_from` |
| High-level `chars()` | [`utf8_codepoints_chars.kara`](utf8_codepoints_chars.kara) | walk `s.chars()`, read each scalar with `c as u32`, classify directly |
| Recursive descent | [`utf8_codepoints_recursive.kara`](utf8_codepoints_recursive.kara) | `walk(bytes, i) -> (count, L, N, O, vals)`; one frame per codepoint, totals folded on the way up |
| Reference oracle | [`utf8_codepoints.py`](utf8_codepoints.py) | known-correct answer (`ord` / `len` / `isalpha` / `isnumeric`) |

The ★ decoder is the highest-fidelity mirror: it is the only style that touches
raw bytes, doing the same lead-mask + 6-bit continuation fold a real lexer must.

## What this kata uncovered

**Flushed a HIGH-value ownership-checker false positive — [B-2026-06-14-27](../../../kara/docs/bug-ledger.jsonl).**
The **recursive-descent** style returns a 5-tuple `(count, letters, numbers,
other, vals)` — four `i64`s plus a `String` — and reuses a Copy field (`count`)
both in an `if` guard and in tail/return position while the `String` sibling is
moved. `karac check` rejected it with a spurious
`value 'count' moved here, used again here`, even though `count` is an `i64`
(Copy) that can never be moved. (`karac run` / `karac build` both produced the
**correct** output — the footgun is that `run`/`build` do not gate on the
ownership checker, so only `karac check` surfaced it.)

Root cause: the use-classifier's let-binding type recorder
(`use_classifier.rs`) assigned the **whole tuple type** to *every* binding of a
destructure. A tuple containing a `String` is non-Copy, so the Copy field
`count` inherited a non-Copy type, its reads in consuming position were
misclassified as `Consume`, and the use-after-move predicate fired. The fix
decomposes a tuple destructure **field-by-field** so each binding is keyed to its
own type (`assign_binding_types`), leaving genuine use-after-move of the
move-typed sibling intact (regression-guarded both directions in
`tests/ownership.rs`).

**Port-side classification: latent.** The self-hosted lexer uses no `let (a, b)
= …` tuple destructure today, so the bug was latent there — but the **parser**
port (the next self-hosting step) leans on recursive descent returning
`(node, position)` tuples, where it would have become live. Fixing it here lands
it exactly before the parser needs it.

The other two styles (byte-indexed decoder, `chars()`) were a flat curve: the
whole L2 decode surface — `utf8_byte_len` range compares, `(lead & mask) as i64`
narrow-int masking, the `(cp << 6) | (cont & 0x3F)` fold, `char.try_from(cp)`
classification, and `push(char)` encode — compiled first-try under both backends.

## Kāra features exercised

- **Manual UTF-8 decode** — `utf8_byte_len` lead classification + `u8` bit
  masking (`& 0x1F` / `0x0F` / `0x07` / `0x3F`) widened to `i64`, folded with
  `<<` / `|`.
- **`char` ↔ scalar** — `c as u32` (char → Unicode scalar) and
  `char.try_from(cp)` (scalar → char, fallible) round-trip.
- **Unicode classification** — `char.is_alphabetic()` / `is_numeric()`, the
  property the lexer's non-ASCII identifier recovery dispatches on.
- **Codepoint-granular counting** — count advances one per codepoint regardless
  of 1..4 byte width (the lexer's `column` semantics).
- **Recursive multi-value return** — `walk` returns
  `(i64, i64, i64, i64, String)`, one frame per codepoint.

---

**Bug ledger:** [B-2026-06-14-27](../../../kara/docs/bug-ledger.jsonl) (ownership,
med) — tuple-destructure Copy sibling misclassified as a move. With this kata
green, the lexer-stress surface reads quiet across both ASCII (LeetCode) and the
bespoke multi-byte L2 gap; the next self-hosting step is the **parser** port.
