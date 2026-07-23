# 214. Shortest Palindrome

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String · KMP · Rolling Hash &nbsp;·&nbsp; **Source:** [leetcode.com/problems/shortest-palindrome](https://leetcode.com/problems/shortest-palindrome/)

Prepend the **minimum** number of characters to the front of `s` so the result is a palindrome, and return that shortest palindrome.

```
"aacecaaa"  ->  "aaacecaaa"
"abcd"      ->  "dcbabcd"
"aabba"     ->  "abbaabba"
"a"         ->  "a"
```

**Constraints:** `0 ≤ |s| ≤ 5·10⁴`, `s` is lowercase English letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **KMP prefix-function** ★ | [`shortest_palindrome.kara`](shortest_palindrome.kara) | [`shortest_palindrome.py`](shortest_palindrome.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The characters you must prepend are exactly the reverse of the part of `s` that lies **after its longest palindromic prefix** — the more of `s` that is already a palindrome from the front, the less you add.

Finding that prefix is the KMP trick. Concatenate `s + '#' + reverse(s)` and compute the **prefix-function** (failure table): `fail[i]` is the length of the longest proper prefix of the string up to `i` that is also a suffix there. The `'#'` separator (a character outside the alphabet) prevents a match from straddling the join, so the table's last entry is the longest prefix of `s` that equals a suffix of `reverse(s)` — i.e. the longest palindromic prefix of `s`. Prepend the reverse of the remaining tail, then append `s`. O(n) time.

## Kāra features exercised

- **`s.chars().collect()` → `Vec[char]`** for O(1) indexing, and a built `Vec[char]` concatenation (`s + '#' + reverse`) assembled by pushes.
- **KMP failure table in a `Vec[i64]`** — the two-cursor prefix-function with the `len = fail[len-1]` fallback, driven entirely by index arithmetic and `char` equality.
- **`String` assembled with `push(char)`** — the reversed tail then the original, the "read as indices, build with chars" idiom.

## Running

```bash
karac run   shortest_palindrome.kara
karac build shortest_palindrome.kara && ./shortest_palindrome
python3 shortest_palindrome.py
diff <(karac run shortest_palindrome.kara) <(python3 shortest_palindrome.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
