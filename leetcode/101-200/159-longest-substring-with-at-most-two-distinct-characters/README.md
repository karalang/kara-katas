# 159. Longest Substring with At Most Two Distinct Characters

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table · String · Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given a string `s`, return the length of the **longest substring that contains at most two distinct characters**.

```
"eceba"      ->  3   ("ece")
"ccaabbb"    ->  5   ("aabbb")
"abcabcabc"  ->  2
"aaaaaa"     ->  6
```

**Constraints:** `0 ≤ |s|`; `s` consists of English letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **sliding window + count map** ★ | [`longest_two_distinct.kara`](longest_two_distinct.kara) ✓ | [`longest_two_distinct.py`](longest_two_distinct.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A single O(n) sliding window. Grow the right edge one char at a time, recording each char's count in a `Map[char, i64]`. The map's **size** is the number of distinct chars in the window — whenever it exceeds 2, shrink from the left: decrement the leftmost char's count, and `remove` it from the map when the count reaches zero. After each step the window `[left, right]` is valid, so the answer is the running maximum of its width.

## Kāra features exercised

- **`Map[char, i64]`** — `char`-keyed hash map with `.get` → `Option`, `.insert`, `.remove`, and `.len()` as the distinct-count. The `Option` returned by `insert`/`remove` is discarded with `let _ = …` (Kāra treats `Option` as implicitly `#[must_use]`).
- **`s.chars().collect()` → `Vec[char]`** — decode UTF-8 once so the window can index chars in O(1) (`s[i]` on a `String` is deliberately a compile error).
- **`ref Map` parameter** — the `count_of` helper borrows the map read-only.

## Running

```bash
karac run   longest_two_distinct.kara
karac build longest_two_distinct.kara && ./longest_two_distinct
python3 longest_two_distinct.py
diff <(karac run longest_two_distinct.kara) <(python3 longest_two_distinct.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
