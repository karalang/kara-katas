# 186. Reverse Words in a String II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Two Pointers · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-words-in-a-string-ii](https://leetcode.com/problems/reverse-words-in-a-string-ii/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Reverse the **order of the words** in a character array **in place**, with O(1) extra space. Words are separated by single spaces; no leading or trailing spaces.

```
"the sky is blue"  ->  "blue is sky the"
"a b c"            ->  "c b a"
```

**Constraints:** the input is a character array; single-space separators.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **reverse-all then reverse-each-word** ★ | [`reverse_words_ii.kara`](reverse_words_ii.kara) | [`reverse_words_ii.py`](reverse_words_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The classic two-reversal trick, both steps in-place index swaps:

1. **Reverse the entire array.** `"the sky"` → `"yks eht"` — now the words are in the right *order* but each is spelled backwards.
2. **Reverse each word back.** Walk the array; at every space (and the end), reverse the run since the last boundary. `"yks eht"` → `"sky the"`.

No auxiliary buffer, O(n) time, O(1) extra space (the [#151](../151-reverse-words-in-a-string/) contrast collects words into a `Vec` instead — this variant is the in-place one).

## Kāra features exercised

- **In-place `Vec[char]` index swaps** — `reverse_range` swaps `a[i]`/`a[j]` (char is a `Copy` scalar, so no heap churn), driven twice: once over the whole array, then per word.
- **`s.chars().collect()` → `Vec[char]`** for the mutable character array, rebuilt to a `String` with `push` in a `for c in a` loop.
- **`mut ref Vec[char]` parameter** with the `mut` call-site marker on the fresh binding.

## Running

```bash
karac run   reverse_words_ii.kara
karac build reverse_words_ii.kara && ./reverse_words_ii
python3 reverse_words_ii.py
diff <(karac run reverse_words_ii.kara) <(python3 reverse_words_ii.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
