# 239. Sliding Window Maximum

Given `nums` and a window width `k`, return the maximum of every contiguous
window of size `k` as the window slides left to right.

## Approach

A naive per-window scan is `O(n·k)`. The **monotonic deque** method is `O(n)`:
keep a deque of *indices* whose values are strictly decreasing front→back, so the
front index always holds the current window's maximum.

- Before pushing `i`, pop from the **back** every index whose value is `≤ nums[i]`
  — none of them can be the max while `i` is in the window and at least as large.
- Pop from the **front** any index that has slid out of the window (`≤ i − k`).
- Once the first full window exists (`i ≥ k − 1`), the front index's value is that
  window's answer.

Each index is pushed and popped at most once → `O(n)` total.

The deque is a `Vec[i64]` of indices with an explicit `head` cursor: front-pop
advances `head`, back-pop is `Vec.pop()`, and the live span is `dq[head..len]`.

## Files

- [`sliding_window_max.kara`](sliding_window_max.kara) — Kāra implementation.
- [`sliding_window_max.py`](sliding_window_max.py) — Python mirror (oracle).

Expected output (both):

```
3 3 5 5 6 7
1
11
4 3 2 5 5
7
```
