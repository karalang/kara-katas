# 279. Perfect Squares

Return the least number of perfect-square numbers (`1, 4, 9, 16, …`) that sum to
`n`.

## Approach

Bottom-up DP over amounts. `dp[i]` = fewest squares summing to `i`:

```
dp[0] = 0
dp[i] = 1 + min over all squares j² ≤ i of dp[i − j²]
```

Every amount is one square added to a smaller amount, so scanning all squares
`j² ≤ i` and taking the minimum builds the table in `O(n·√n)` time, `O(n)` space.

## Files

- [`perfect_squares.kara`](perfect_squares.kara) — Kāra implementation.
- [`perfect_squares.py`](perfect_squares.py) — Python mirror (oracle).

Expected output (both): `3 2 1 2 1 3 1` (one per line).
