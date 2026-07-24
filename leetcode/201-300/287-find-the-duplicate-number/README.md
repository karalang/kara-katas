# 287. Find the Duplicate Number

`nums` has `n+1` values in `[1, n]`, so by pigeonhole at least one repeats. Find
it **without modifying** the array and in `O(1)` extra space.

## Approach

Read index `i` as a pointer to index `nums[i]`. Every value lies in `[1, n]`, so
walking these pointers from index 0 stays in-bounds; because a value repeats, two
indices point to the same place, making the functional graph contain a cycle
whose **entrance is the duplicate**. Floyd's tortoise-and-hare:

- **Phase 1:** advance `slow` by 1 and `fast` by 2 until they meet in the cycle.
- **Phase 2:** reset one walker to the start; advance both by 1 — they meet at the
  cycle entrance = the duplicate.

`O(n)` time, `O(1)` space, array untouched.

## Files

- [`find_duplicate.kara`](find_duplicate.kara) — Kāra implementation.
- [`find_duplicate.py`](find_duplicate.py) — Python mirror (oracle).

Expected output (both): `2 3 1 2 6` (one per line).
