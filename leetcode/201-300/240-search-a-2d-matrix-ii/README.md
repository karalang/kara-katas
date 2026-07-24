# 240. Search a 2D Matrix II

Search a matrix for `target`, where every row is sorted left→right **and** every
column is sorted top→bottom.

## Approach

Start at the **top-right** corner and walk a staircase:

- `matrix[r][c] == target` → found;
- `matrix[r][c] > target` → the whole column below is even larger, so step **left**;
- `matrix[r][c] < target` → the whole row to the left is even smaller, so step **down**.

Each step eliminates an entire row or column, so the walk visits at most `m + n`
cells → `O(m + n)` time, `O(1)` space. (Symmetric from the bottom-left corner.)

The matrix is passed as a flat row-major `Slice[i64]` with `rows`/`cols`, so
`matrix[r][c] = flat[r * cols + c]`.

## Files

- [`search_matrix.kara`](search_matrix.kara) — Kāra implementation.
- [`search_matrix.py`](search_matrix.py) — Python mirror (oracle).

Expected output (both): `true false true true false false true` (one per line).
