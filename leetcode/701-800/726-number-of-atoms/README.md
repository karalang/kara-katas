# 726. Number of Atoms

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Hash Table, String, Stack, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/number-of-atoms](https://leetcode.com/problems/number-of-atoms/)

Given a chemical `formula`, count every atom and render the tally with element
names in sorted order, each name followed by its count when that count is > 1.

```
"H2O"            →  "H2O"
"Mg(OH)2"        →  "H2MgO2"
"K4(ON(SO3)2)2"  →  "K4N2O14S4"
```

**Grammar.** An element is `Uppercase Lowercase* Digit*` (`"Mg"`, `"O2"`, `"H"`);
a group is `'(' formula ')' Digit*` (`"(OH)2"`); formulas concatenate. A missing
count is 1.

**Constraints:** `1 ≤ formula.length ≤ 1000`; the input is always a valid
formula; counts fit in a 32-bit integer.

## Why this kata — the lexer's *combined* surface

Every other lexer-stress kata isolates **one** move; this one is the only corpus
entry that hammers the self-hosted lexer's moves *together*, in a single
left-to-right scan, exactly as the real lexer reads an identifier-then-number run
inside nested delimiters:

| Lexer surface | This kata |
|---|---|
| **uppercase/lowercase run → name token** (§1 classify + §3 slice) | `is_upper` + maximal `is_lower` run → one zero-copy `s[i..j]` |
| **digit run → integer** (§4 `from_str_radix`) | `c = c*10 + (b - b'0')` over a digit run (count / multiplier) |
| **delimiter nesting** (§6 group depth) | `Vec[i64]` paren-position stack (or the call stack) |
| **group multiplier fold-back** | `counts[k] *= mult` over the emitted range |
| **keyword-dispatch byte compare** (§7) | `str_less` byte-lexicographic name ordering |

This is item **#5** of the [lexer-stress order](../../../../kara/docs/implementation_checklist/phase-12-self-hosting.md)
— the "full mini-tokenizer" pick: classification + number-scan + nesting in one
program.

**No `Map`/`TreeMap`.** Counts live in a parallel `Vec[String]` / `Vec[i64]`
emit list, not a hash map. A group's trailing multiplier scales every atom
emitted since its `(` — a **range mutation** that wants indexed assignment
(`counts[k] = counts[k] * mult`), not tuple-field mutation. The final tally and
sorted render stay on the hardened byte-compare + slice surface the lexer's
keyword dispatch already stands on, and sidestep `Map`'s unspecified iteration
order (sorted output would need `TreeMap`, which v1 codegen does not yet emit).

## Approaches

Three styles, all byte-identical to the Python oracle across **17 cases**, under
`karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Iterative — paren-position stack** ★ | [`number_of_atoms.kara`](number_of_atoms.kara) | one byte scan; `(` pushes `names.len()`, `)`+mult scales the emitted range |
| Recursive descent | [`number_of_atoms_recursive.kara`](number_of_atoms_recursive.kara) | `parse_at(s, i) -> (Vec[String], Vec[i64], i64)`; nesting rides the call stack |
| Lex-then-evaluate | [`number_of_atoms_tokens.kara`](number_of_atoms_tokens.kara) | pass 1 lexes bytes → token vecs; pass 2 consumes the token stream |
| Reference oracle | [`number_of_atoms.py`](number_of_atoms.py) | known-correct LeetCode answer |

All three read the source through the zero-copy [`bytes()`](../../../README.md)
view with `b'…'` byte literals and append each element name as **one** maximal
`s[i..j]` slice — not char-by-char `push`. The **lex-then-evaluate** style is the
most faithful mirror of the real pipeline: it materialises an explicit token
stream first (kind / name-text / number, in parallel vecs) and only then folds
multipliers — "bytes → tokens → value," the same split the self-hosted compiler
draws between its lexer and parser.

Sorted output is produced **without moving any `String` out of its `Vec`**: an
index permutation (`Vec[i64]`) is insertion-sorted by `str_less`, then rendered
through the permutation. That keeps the element names borrowed throughout and
avoids the conditional-move-out-of-collection that would otherwise force an RC
fallback.

## What this kata uncovered

**Flat curve — no karac bug.** The entire combined surface compiled and ran
first-try under both backends across all three styles: byte classification
(`is_upper`/`is_lower`/`is_digit`), `(b - b'0') as i64` digit folding, the
`Vec[i64]` paren-position stack, **range mutation through indexed assignment**
(`counts[k] = counts[k] * mult`), parallel `Vec[String]`/`Vec[i64]` emit lists, a
recursive function returning a **3-tuple carrying two Vecs**
(`(Vec[String], Vec[i64], i64)` — heavier than #394's `(String, i64)`), an
explicit two-pass lex/eval token stream, byte-lexicographic `str_less` ordering,
the index-permutation insertion sort, and `f"{c}"` count interpolation into
`push_str`. This is the same flat-curve signal #67/#415 gave — the tokenizer's
combined machinery sits entirely on codegen primitives the earlier lexer-stress
katas (#394 stack+repeat, #722 slice+scan, #125 narrow-int classify, #67/#415
radix) already hardened.

**One diagnostic, resolved by design, not a bug.** The first draft bound the
emit-list name to an owned local (`let nm = names[e]`) and then *conditionally*
consumed it (push on a first sighting, drop on a merge) — a genuine conditional
move, which `karac check` correctly flagged as a `perf[rc-fallback]`. The fix is
a data-flow one: borrow the name for the linear search and `.clone()` the (tiny,
≤2-byte) element name only on the store branch, so the merge case never copies
and no RC is inserted. The diagnostic did its job — it pointed at a real
ownership ambiguity, and the clean restructure silenced it without
`#[allow(rc_fallback)]`.

## Kāra features exercised

- **Combined byte tokenizing** — `is_upper`/`is_lower`/`is_digit` classification,
  maximal-run `s[i..j]` name slices, and `c*10 + (b - b'0')` number folding in
  one scan.
- **Range mutation via indexed assignment** — `counts[k] = counts[k] * mult` to
  fold a group multiplier back over a `Vec[i64]` slice (not tuple-field mutation).
- **Parallel-Vec emit list** — `Vec[String]` names + `Vec[i64]` counts as a
  Map-free tally with deterministic, sorted output.
- **Recursive multi-value return** — `parse_at` returns
  `(Vec[String], Vec[i64], i64)`; the call stack carries paren nesting.
- **Two-pass lex/evaluate** — an explicit token stream (parallel kind/text/num
  vecs) consumed by a second pass, mirroring the lexer/parser split.
- **Move-free sort** — an index permutation insertion-sorted by a hand-written
  byte-lexicographic `str_less`, avoiding a move-out-of-`Vec` RC fallback.

---

**Bug ledger:** flat curve — the combined classify + number-scan + nesting
surface produced no miscompile under either backend across all three styles, the
same signal #67/#415 gave. No new [`karac` bug-ledger](../../../../kara/docs/bug-ledger.md)
entry. With #726 green, the lexer-stress surface reads quiet: the remaining picks
(#405/#171 radix render, a bespoke non-ASCII codepoint kata) are render/encoding
variations on already-hardened ground.
