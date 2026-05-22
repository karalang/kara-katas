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
| Bottom-up DP with a 2-cell rolling window | O(n) time, O(1) extra space | [`decode_ways.kara`](decode_ways.kara) ✓ via `karac run` | [`decode_ways.py`](decode_ways.py) ✓ |

`✓` runs end-to-end today. Output is byte-for-byte identical to the Python mirror across all 22 test cases.

## Why a rolling window, not a full DP table

The recurrence touches at most two prior cells:

```
dp[i] = (1 ≤ s[i-1] ≤ 9 ? dp[i-1] : 0)              // peel one digit off the end
      + (10 ≤ 10·s[i-2] + s[i-1] ≤ 26 ? dp[i-2] : 0) // peel two digits off the end
```

with `dp[0] = 1` (the empty suffix has exactly one — vacuous — decoding) and, once we've rejected a leading `'0'`, `dp[1] = 1`. Because the right-hand side reads only `dp[i-1]` and `dp[i-2]`, the full table is wasted memory — two `i64` cells (`prev2`, `prev1`) carry the entire state, advanced in lockstep with `i`. Same shape as the [Fibonacci rolling pair](../121-best-time-to-buy-and-sell-stock/one_pass.kara) trick: keep what the recurrence reads, drop what it doesn't.

### Why the early-bail on a leading `'0'` is load-bearing

Once we know `bytes[0] != '0'`, the invariant `dp[1] = 1` holds and the loop's first step (`i = 1`) can read both `prev2` and `prev1` as live cells. Without the bail, `dp[1] = 0` for a leading-zero string, which then propagates correctly through the recurrence — but seeding `prev1 = 0` would make the implementation re-derive that zero on every step rather than short-circuit, and the code reads cleaner with the precondition stated explicitly up front.

### Why mid-stream zeros don't need a special case

A digit `'0'` at position `i` makes `d1 = 0`, so the one-digit branch (`1 ≤ d1 ≤ 9`) is skipped automatically. The two-digit branch is the only path that contributes — and it contributes iff `s[i-1]` is `'1'` or `'2'` (anything else makes `10·s[i-2] + 0 ≥ 30`). For a `"30"`, `"40"`, …, `"00"` adjacency, both branches reject and `dp[i] = 0`; the zero then propagates through every subsequent step. That's exactly the right answer (the string is undecodable past that point), and it falls out of the recurrence with no extra logic — `"100"`, `"230"`, `"301"` all return 0 via the same arithmetic that handles `"12"` and `"226"`.

### One pass, two integer cells

```
prev2 = 1
prev1 = 1
for i in 1..n:
    d1  = bytes[i]   - '0'
    d0  = bytes[i-1] - '0'
    two = 10*d0 + d1
    cur = 0
    if 1  <= d1  <= 9:  cur += prev1
    if 10 <= two <= 26: cur += prev2
    prev2 = prev1
    prev1 = cur
return prev1
```

O(1) extra space, one indexed read per byte, no branching on history beyond the immediately-preceding digit.

## Kāra features exercised

- **`ref String` parameter + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view over the String's UTF-8 storage. The LeetCode alphabet is digits only, so each byte is the codepoint and `bytes[i]` is the right primitive — same shape as kata [#8](../8-string-to-integer-atoi/) and kata [#65](../65-valid-number/).
- **`u8` → `i32` digit math** — `(bytes[i] as i32) - (zero as i32)` widens before subtracting so the arithmetic is safe across the whole `'0'..'9'` range without worrying about unsigned underflow on a non-digit. `zero` is `b'0'` — the byte literal form spelled directly per design.md § Byte and Byte-String Literals (type `u8`, lex-time-rejected for non-ASCII).
- **`and` / `or` short-circuit in range guards** — `d1 >= 1i32 and d1 <= 9i32` and `two >= 10i32 and two <= 26i32` both rely on left-to-right evaluation; the second comparison is skipped when the first fails.
- **`while` loop with mutable `i64` index and per-iter `let mut` accumulator** — `cur` is freshly bound inside the loop body and committed to `prev1` at the end of each iteration. The two `prev` cells are mutated across iterations; `cur` is a per-iter scratch.
- **F-string interpolation of `ref String` and `i64`** — `f"decode_ways \"{s}\": {decode_ways(s)}"` interpolates a string borrow and an integer in one call. The embedded `\"` escape produces literal quotes around the input for grep-friendly output diffing.
- **Early `return 0` from a guard clause** — both the empty-input check and the leading-zero check exit before the loop runs, keeping the recurrence's preconditions visible at the top of the function.

No `Vec`, no `Map`, no shared structs — `Slice[u8]` view + two scalar `i64` cells.

## Edge cases worth exercising

| Input | Expected | Why it's interesting |
|---|---|---|
| `"12"` | `2` | The reference small case — both one-digit and two-digit splits contribute. |
| `"226"` | `3` | Classic three-way split — exercises the recurrence over three positions. |
| `"06"` | `0` | Leading zero — the early-bail at the top of the function. |
| `"10"` | `1` | Trailing `'0'` attaches to the preceding `'1'` — only the two-digit branch fires. |
| `"100"` | `0` | `'00'` is not a key and `'0'` alone is not a key — the zero propagates. |
| `"101"` | `1` | Mid-stream `'0'` doesn't poison the rest of the string — `"J,A"` is the only decoding. |
| `"110"` | `1` | Tail `"10"` forces the prefix `"1"` to be `'K' (11,0)`? No — `'11,0'` has a bare `'0'` and is invalid; only `"K,J"` survives. |
| `"301"` | `0` | Leading `'3'` then `'0'` — `"30"` is out of range as a two-digit key and `'0'` alone is invalid. |
| `"230"` | `0` | Trailing `"30"` is out of range as a two-digit key, and the alternate `'23,0'` has a bare `'0'`. |
| `"27"` | `1` | `27` exceeds the two-digit limit — only the `"BG" (2,7)` split survives. |
| `""` | `0` | Empty input — guarded at the top. |
| `"0"` | `0` | Single `'0'` — guarded at the top. |
| `"1"` / `"9"` | `1` | Single non-zero digit — the loop never runs and `prev1 = 1` is the answer. |
| `"11"` … `"111111"` | `2, 3, 5, 8, 13` | All-ones (or all-twos) strings of length `n` produce the `(n+1)`th Fibonacci number, since every adjacent pair is a valid two-digit key — the cleanest stress test for the rolling window. |
| `"123123"` | `9` | Mixed valid one- and two-digit splits — the recurrence diverges from Fibonacci. |
| `"1234567"` | `3` | Only the first two pairs are two-digit-valid; the rest are forced one-digit. |
| `"2611055971756562"` | `4` | Long mixed string — exercises the rolling window over many steps, including a mid-stream `'0'` at position 5. |

All 22 cases run in `main` and the output is diffed against [`decode_ways.py`](decode_ways.py).

## API shape

`decode_ways(s: ref String) -> i64` is the algorithm; `report(s: ref String)` prints the result; `main` calls `report` per case. Logic is separated from I/O so the function would slot into a future test harness unchanged. The Python file mirrors this with `decode_ways(s: str) -> int` and the same `report` / `main` shape.

Each Kāra `main` case passes its string literal directly to `report` — `ref String` accepts any source per design.md § Part 1½ Rule 4, and the codegen materializes the literal into a stack temp at the call site automatically.

## Output format

One line per case in the form `decode_ways "<input>": <count>`. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
decode_ways "12": 2
decode_ways "226": 3
decode_ways "06": 0
decode_ways "10": 1
decode_ways "100": 0
decode_ways "101": 1
decode_ways "110": 1
decode_ways "301": 0
decode_ways "230": 0
decode_ways "27": 1
decode_ways "": 0
decode_ways "0": 0
decode_ways "1": 1
decode_ways "9": 1
decode_ways "11": 2
decode_ways "111": 3
decode_ways "1111": 5
decode_ways "11111": 8
decode_ways "111111": 13
decode_ways "123123": 9
decode_ways "1234567": 3
decode_ways "2611055971756562": 4
```

## Running

```bash
# Kāra
karac run decode_ways.kara

# Python
python3 decode_ways.py

# Verify they agree
diff <(karac run decode_ways.kara) <(python3 decode_ways.py) && echo OK
```
