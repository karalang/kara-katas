# 268. Missing Number

`nums` holds `n` distinct values from `[0, n]`, so exactly one value in that range
is absent. Return it in `O(n)` time, `O(1)` space.

## Approach

XOR-fold every index `0..n` together with every array value. Each present value
cancels against its matching index, leaving only the one index whose value never
appeared — the missing number. XOR avoids the overflow the Gauss-sum method risks
(Kāra checks integer overflow by default, so XOR is the clean choice).

## Files

- [`missing_number.kara`](missing_number.kara) — Kāra implementation.
- [`missing_number.py`](missing_number.py) — Python mirror (oracle).

Expected output (both): `2 2 8 1 0` (one per line).
