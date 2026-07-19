# 132. Palindrome Partitioning II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** DP · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/palindrome-partitioning-ii](https://leetcode.com/problems/palindrome-partitioning-ii/)

Return the **minimum** number of cuts needed so every piece of `s` is a palindrome.

```
"aab"   ->  1   (aa | b)
"aabaa" ->  0   (already a palindrome)
"abcde" ->  4   (a|b|c|d|e)
```

**Constraints:** `1 ≤ s.length ≤ 2000`, lowercase.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **O(n²) palindrome-table DP** ★ | O(n²) time & space | [`min_cut.kara`](min_cut.kara) ✓ | [`min_cut.py`](min_cut.py) ✓ |

`✓` runs end-to-end today: interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`) all agree with the Python mirror. Validated against known values (aab 1, aabaa 0, abcde 4) plus deterministic-LCG strings. Zero diagnostics, valgrind-clean.

## The mechanism

Two DPs. First a boolean table `pal[i][j]` — filled by increasing substring length, `s[i..=j]` is a palindrome iff its ends match and the inner span `pal[i+1][j-1]` is (with the length-2 base case). Then `cut[i]` = minimum cuts for the prefix `s[0..=i]`: `0` when the whole prefix is already a palindrome, else `min(cut[j-1] + 1)` over every `j` where `s[j..=i]` is a palindrome. The answer is `cut[n-1]`. The DP sibling of [#131](../131-palindrome-partitioning/) — where that enumerates every partition, this collapses to one min-cut scalar via a table.

## Kāra features exercised

- **`Vec[Vec[bool]]` DP table with 2-D index-assign** — `pal[lo][hi] = true` in-place, read as `pal[i+1][j-1]`; a boolean-element nested Vec (distinct from [#130](../130-surrounded-regions/)'s `Vec[Vec[i64]]`).
- **`Vec[i64]` cut array** with index-assign `cut[i] = best` and back-references `cut[j-1]`.
- **Length-ordered table fill** — the classic interval-DP loop order (`length` outer, `lo` inner) so `pal[i+1][j-1]` is always resolved before `pal[i][j]`.
- **Overflow-checked byte compares** over `s.bytes()`.

## Running

```bash
karac run   min_cut.kara
karac build min_cut.kara && ./min_cut
python3 min_cut.py
diff <(karac run min_cut.kara) <(python3 min_cut.py) && echo OK
```

## Notes

Dogfood-first interval-DP kata exercising `Vec[Vec[bool]]` 2-D index-assign and length-ordered table fill across every surface.
