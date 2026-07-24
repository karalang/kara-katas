# 274. H-Index

The h-index is the largest `h` such that at least `h` papers have at least `h`
citations each.

## Approach

Sort citations ascending. Then the papers at positions `[i, n)` are the `n − i`
most-cited; if `citations[i] ≥ n − i`, those `n − i` papers each have at least
`n − i` citations, so `n − i` is an achievable h-index. Scanning from the smallest
qualifying `i` yields the maximum such value. `O(n log n)`.

## Files

- [`h_index.kara`](h_index.kara) — Kāra implementation.
- [`h_index.py`](h_index.py) — Python mirror (oracle).

Expected output (both): `3 1 0 1 4 4` (one per line).
