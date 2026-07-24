# 260. Single Number III

Exactly two elements of `nums` appear once; every other appears twice. Return the
two singles, in `O(n)` time and `O(1)` space.

## Approach

1. **XOR everything** → `x = a ^ b` (paired elements cancel). Since `a ≠ b`, `x`
   is non-zero.
2. **Isolate its lowest set bit** `bit = x & (-x)`. `a` and `b` differ in that
   bit, so it splits the array into two groups — one holding `a`, the other `b`,
   with each duplicate pair landing together in one group.
3. **XOR each group** independently → the two singles fall out.

Result sorted ascending for a deterministic line.

## Files

- [`single_number_iii.kara`](single_number_iii.kara) — Kāra implementation.
- [`single_number_iii.py`](single_number_iii.py) — Python mirror (oracle).

Expected output (both): `3 5` / `-1 0` / `0 1` / `4 12` / `5 8` (one pair per line).
