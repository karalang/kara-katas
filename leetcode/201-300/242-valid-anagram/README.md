# 242. Valid Anagram

Return whether `t` is an anagram of `s` — i.e. they contain the same characters
with the same multiplicities.

## Approach

Over a lowercase-ASCII alphabet this is a single frequency pass: keep a 26-slot
count, bump it **up** for each letter of `s` and **down** for each letter of `t`.
`t` is an anagram exactly when every count returns to zero (a length mismatch is
rejected up front, so the counts only need to confirm equal multiplicities).
`O(n)` time, `O(1)` space.

## Files

- [`valid_anagram.kara`](valid_anagram.kara) — Kāra implementation.
- [`valid_anagram.py`](valid_anagram.py) — Python mirror (oracle).

Expected output (both): `true false true false true false` (one per line).
