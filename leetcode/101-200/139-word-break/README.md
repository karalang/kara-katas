# 139. Word Break

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Dynamic Programming · String · Hash Set &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-break](https://leetcode.com/problems/word-break/)

Given a string `s` and a dictionary of words, decide whether `s` can be segmented into a space-separated sequence of one or more dictionary words. Words may be reused.

```
"leetcode",      {leet, code}                 ->  true    # leet + code
"applepenapple", {apple, pen}                 ->  true    # apple + pen + apple
"catsandog",     {cats, dog, sand, and, cat}  ->  false
"aaaaaaaa",      {a, aa, aaa}                  ->  true
```

**Constraints:** `1 ≤ |s| ≤ 300`, `1 ≤ dict size ≤ 1000`, `1 ≤ |word| ≤ 20`, all lowercase.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **prefix DP** ★ | [`word_break.kara`](word_break.kara) ✓ | [`word_break.py`](word_break.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. Zero diagnostics, valgrind-clean.

## The mechanism

`dp[i]` is true when the prefix `s[0..i]` segments cleanly. `dp[0]` is the empty prefix (trivially true). For each end `i`, scan every split point `j < i`: if the prefix `s[0..j]` already segments (`dp[j]`) **and** the piece `s[j..i]` is a dictionary word, then `s[0..i]` segments too. The answer is `dp[n]`. `O(n²)` split points × the substring/Set-lookup cost.

## Kāra features exercised

- **`Set[String]` membership** — `dict.contains(piece)` over a hash set of owned `String`s; the dictionary is built with `.insert`.
- **`String.substring(j, i)`** — the `s[j..i]` prefix-piece extraction inside the double loop (a fresh heap `String` per probe — a real allocation/leak surface, verified clean).
- **`Vec[bool]` DP table** — filled to length `n + 1`, indexed both as a read (`dp[j]`) and a write (`dp[i] = true`).

## Running

```bash
karac run   word_break.kara
karac build word_break.kara && ./word_break
python3 word_break.py
diff <(karac run word_break.kara) <(python3 word_break.py) && echo OK
```

## Notes

Clean first-pass dogfood: `Set[String]` + per-probe `substring` allocation + `Vec[bool]` DP, compiled correctly with no friction (interp == build == Python, valgrind-clean). Sets up #140 Word Break II (enumerate every segmentation), which needs backtracking rather than a boolean table.
