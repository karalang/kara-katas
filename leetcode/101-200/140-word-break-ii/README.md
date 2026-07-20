# 140. Word Break II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Backtracking · Dynamic Programming · String · Hash Set &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-break-ii](https://leetcode.com/problems/word-break-ii/)

Given a string `s` and a dictionary, return **every** way to segment `s` into a space-joined sequence of dictionary words (words may be reused). Where [#139](../139-word-break/) asks *whether* a segmentation exists, #140 asks for **all** of them.

```
"catsanddog",        {cat, cats, and, sand, dog}                 ->  "cat sand dog", "cats and dog"
"pineapplepenapple", {apple, pen, applepen, pine, pineapple}     ->  3 sentences
"catsandog",         {cats, dog, sand, and, cat}                 ->  (none)
```

**Constraints:** `1 ≤ |s| ≤ 20`, `1 ≤ dict size ≤ 1000`, `1 ≤ |word| ≤ 10`, all lowercase; the answer set may be large but bounded by the small `|s|`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **suffix backtracking** ★ | [`word_break_ii.kara`](word_break_ii.kara) ✓ | [`word_break_ii.py`](word_break_ii.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. Output is **sorted** so the comparison is order-independent. valgrind/LSan-clean.

## The mechanism

`solve(start)` returns every sentence for the suffix `s[start..]`:

- At `start == n` the suffix is empty, so the one sentence is `""`.
- Otherwise, for each `end` where the piece `s[start..end]` is a dictionary word, prepend that word to **every** sentence returned by `solve(end)`.

Each recursion returns a fresh `Vec[String]` of sentences; the caller prepends its word (`word + " " + tail`) to each. The result is sorted before printing for a deterministic mirror.

## Kāra features exercised

- **Recursion returning `Vec[String]`** — each frame allocates and returns a list of owned sentences, which the parent extends. This is the RC-fallback + heap-`Vec[String]` recursion surface (the [`B-2026-07-18-52`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) class); verified **leak-free** under valgrind across the full recursion.
- **`Set[String]` membership + `String.substring`** — the dictionary lookup on each `s[start..end]` piece.
- **`ref String` read-only recursion** — `s` is borrowed through the whole recursion rather than moved (the idiomatic read-only-param form).
- **In-place `Vec[String].sort()`** — the result is sorted before output.

> **Compiler friction surfaced by this kata.**
> - **`Vec[T].sorted()` is codegen-unimplemented** ([kara `B-2026-07-19-15`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)): the immutable, value-returning `sorted()` runs under `--interp` but fails both `build` and JIT for every element type (in-place `sort()` is fully supported). The kata uses in-place `.sort()` before returning — the supported idiomatic equivalent — and the gap is filed for a later `sorted() = clone + sort` implementation.
> - A `perf[rc-fallback]` note fires on `word` (re-used after the `dict.contains(word)` membership check) — an accepted outcome, not an error: the value is genuinely shared across the check and the sentence-building push, so RC is the correct lowering.

## Running

```bash
karac run   word_break_ii.kara
karac build word_break_ii.kara && ./word_break_ii
python3 word_break_ii.py
diff <(karac run word_break_ii.kara) <(python3 word_break_ii.py) && echo OK
```

## Notes

The backtracking companion to [#139](../139-word-break/). Its recursive `Vec[String]` accumulation is a strong leak-surface dogfood (verified clean), and it surfaced the `Vec.sorted()` codegen gap (`B-2026-07-19-15`).
