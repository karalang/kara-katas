# 91. Decode Ways

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/decode-ways](https://leetcode.com/problems/decode-ways/)

A message containing letters from A–Z is encoded by the mapping `'A' → "1"`, `'B' → "2"`, …, `'Z' → "26"`. To *decode* a digit string you partition it into a sequence of pieces, each of which is a key in that mapping; the answer for a string `s` is the number of distinct partitions. Strings containing partitions that map to a key with a leading zero (`"06"`, `"00"`, etc.) are **not** valid encodings — `'0'` is not in the alphabet on its own, and `"06"` is not the same key as `"6"`.

Return the number of ways to decode `s`. The answer is guaranteed to fit in a 32-bit integer.

```
"12"      →  2     "AB" (1,2) | "L" (12)
"226"     →  3     "BBF" (2,2,6) | "BZ" (2,26) | "VF" (22,6)
"06"      →  0     leading zero — no valid partition starts with '0'
"10"      →  1     "J" (10)         — the '0' attaches to the preceding '1'
"100"     →  0     '00' is not a key; '0' alone is not a key
"27"      →  1     "BG" (2,7)       — 27 is out of range, so two-digit split is illegal
```

**Constraints:** `1 ≤ s.length ≤ 100`, `s` consists of digits `'0'–'9'` only.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Bottom-up DP with a 2-cell rolling window | O(n) time, O(1) extra space | [`src/main.kara`](src/main.kara) ✓ | [`decode_ways.py`](decode_ways.py) ✓ |

`karac test` runs the 22-case block-form suite in [`src/main_test.kara`](src/main_test.kara) as the primary correctness loop; case titles name input + expected count, so a failure surfaces both without consulting the test source.

## Why a rolling window

The recurrence touches at most two prior cells:

```
dp[i] = (1 ≤ s[i-1] ≤ 9 ? dp[i-1] : 0)              // peel one digit off the end
      + (10 ≤ 10·s[i-2] + s[i-1] ≤ 26 ? dp[i-2] : 0) // peel two digits off the end
```

with `dp[0] = 1` (empty suffix has one decoding) and `dp[1] = 1` once a leading `'0'` has been rejected. Two `i64` cells (`prev2`, `prev1`) carry the entire state. The header comment in [`src/main.kara`](src/main.kara) covers the leading-zero bail and mid-stream-zero propagation.

## Kāra features exercised

- **`ref String` + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view; LeetCode alphabet is digits only, so byte == codepoint and indexing is O(1) with no `Vec[char]` snapshot.
- **`u8` → `i32` digit math** — `(bytes[i] as i32) - (zero as i32)` widens before subtracting; `zero` is `b'0'` per design.md § Byte and Byte-String Literals.
- **`and` short-circuit range guards** — `d1 >= 1 and d1 <= 9` skips the second compare when the first fails.

No `Vec`, no `Map`, no shared structs — `Slice[u8]` view + two scalar `i64` cells.

## Running

```bash
# Primary correctness loop — 22-case block-form suite, JSONL on stdout.
karac test

# Cross-language reference — preserved as a paper-trail.
karac run src/main.kara
python3 decode_ways.py
diff <(karac run src/main.kara) <(python3 decode_ways.py) && echo OK
```

`karac test --filter <substring>` runs only cases whose name contains the substring (e.g. `karac test "leading"` runs just `"leading zero is invalid"`).
