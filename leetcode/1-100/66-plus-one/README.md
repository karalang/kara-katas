# 66. Plus One

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/plus-one](https://leetcode.com/problems/plus-one/)

A non-negative integer is given as its decimal **digits**, most-significant first (`[1, 2, 3]` is 123), with no leading zeros except the single `[0]`. Add one and return the digit array of the result.

```
[1, 2, 3]     →  [1, 2, 4]        123 + 1 = 124
[4, 3, 2, 1]  →  [4, 3, 2, 2]     4321 + 1 = 4322
[9]           →  [1, 0]           9 + 1 = 10   (grows by one place)
[9, 9, 9]     →  [1, 0, 0, 0]     999 + 1 = 1000
```

**Constraints:** `1 ≤ digits.length ≤ 100`; `0 ≤ digits[i] ≤ 9`; no leading zeros except `[0]`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Reverse scan, early return** ★ — bump the first digit below 9 and stop; a 9 becomes 0 and the carry ripples left | O(n) time, O(1) extra | [`plus_one.kara`](plus_one.kara) ✓ via `karac run` / `karac build` | [`plus_one.py`](plus_one.py) ✓ |
| **Explicit carry propagation** — seed a carry of 1 and ripple it through every column, LSB-first, then reverse | O(n) time, O(n) space | [`plus_one_carry.kara`](plus_one_carry.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all twelve test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The carry, and the one case the length changes

Adding one only disturbs the tail: the carry dies the instant it meets a digit that is not 9. So the whole problem is a reverse scan with an early exit —

```
digit < 9   →  increment it, done — nothing to the left changes
digit == 9  →  it becomes 0 and the carry ripples one place left
```

The **reverse scan** ([`plus_one.kara`](plus_one.kara)) is the ★. On the common path (a trailing digit below 9) it touches exactly **one** cell and returns. The only case that scans the whole array is **all nines** (`[9, 9, 9]`): the carry falls off the left end and the result is one place **wider** — a leading 1 followed by `n` zeros (`[1, 0, 0, 0]`). That grow-by-one is the kata's entire subtlety and the reason a plain in-place bump is insufficient — the answer array is sometimes longer than the input. The ★ handles it by allocating the widened result only on that path.

The **carry-propagation** form ([`plus_one_carry.kara`](plus_one_carry.kara)) is the general-adder phrasing: seed `carry = 1` and ripple it through every column exactly as kata [#67](../67-add-binary/) adds two binary strings, here in base 10 —

```
sum = digits[i] + carry ;  out = sum % 10 ;  carry = sum / 10
```

A leftover `carry == 1` after the scan *is* the widening, pushed as the new leading digit. It always walks the whole array and builds a fresh result — strictly more work than the ★'s early return — but it is the phrasing that **generalises**: swap the seed `1` for any addend, or `% 10` for another base, and the same loop adds arbitrary values. The digits accumulate least-significant-first and are flipped to most-significant-first at the end, the same LSB-first-then-reverse discipline as [#67](../67-add-binary/) and kata [#2](../2-add-two-numbers/).

## Kāra features exercised

- **`ref Vec[i64]` input + owned `Vec[i64]` result** — the solver borrows the digit array (`digits: ref Vec[i64]`) and builds a fresh `Vec.new()` output; the ★ mid-loop `return out` when the carry stops is the idiomatic early exit, the same shape kata [#55](../55-jump-game/) and [#67](../67-add-binary/) use.
- **Length-changing output** — the all-nines path constructs a `Vec[i64]` one element longer than the input (`push(1)` then `n` zeros), the case that makes this more than an in-place mutation.
- **`% 10` / `/ 10` column arithmetic + LSB-first reverse** — the carry form's `sum % 10` / `sum / 10` and the trailing MSB-first flip, the base-10 sibling of kata [#67](../67-add-binary/)'s base-2 `% 2` / `/ 2`.
- **Nested array literals as test input** — `report([9, 9, 9], mut s)` builds the `Vec[i64]` digit arrays inline; the harness prints each result as a bracketed list plus a positional checksum `Σ (k+1)·out[k]` folded into `sums:`, the byte-for-byte diff anchor shared with katas [#54](../54-spiral-matrix/) and [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/).

**v1 note.** Digits stay in `[0, 9]` and the array length ≤ 100, so every value and every checksum fits i64 comfortably; the arithmetic is i64 for uniformity with the rest of the corpus. The ★ returns from inside the reverse-scan loop the moment the carry is absorbed — a mid-function `return` in a `while`, lowered identically under `karac run` and `karac build`.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   plus_one.kara
karac build plus_one.kara && ./plus_one

# The carry-propagation approach (identical output):
karac run plus_one_carry.kara

# Python
python3 plus_one.py

# Verify they all agree
diff <(karac run plus_one.kara) <(python3 plus_one.py)          && echo OK
diff <(karac run plus_one.kara) <(karac run plus_one_carry.kara) && echo OK
```
