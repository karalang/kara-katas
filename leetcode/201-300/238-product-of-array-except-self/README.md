# 238. Product of Array Except Self

Return an array `out` where `out[i]` is the product of every element of `nums`
**except** `nums[i]` — **without division**, in `O(n)` time and `O(1)` extra
space (the output array is not counted against the space bound).

## Approach

Two sweeps over the output array itself:

1. **left → right:** `out[i]` receives the product of everything strictly *left*
   of `i` (a running prefix product).
2. **right → left:** multiply each `out[i]` by a running product of everything
   strictly *right* of `i` (a suffix product folded in).

After both passes `out[i] = (∏ left of i) × (∏ right of i) = ∏ except i`. Zeros
fall out for free: one zero zeroes every other position; two zeros zero
everything.

## Files

- [`product_except_self.kara`](product_except_self.kara) — Kāra implementation.
- [`product_except_self.py`](product_except_self.py) — Python mirror (oracle).

Expected output (both):

```
24 12 8 6
0 0 9 0 0
12 8 6
9 5
```
