# 234. Palindrome Linked List

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers · Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/palindrome-linked-list](https://leetcode.com/problems/palindrome-linked-list/)

Return `true` iff a singly-linked list reads the same forwards and backwards, using **O(1)** extra space.

```
[1,2,2,1]  ->  true
[1,2]      ->  false
[1,2,3,2,1] -> true
```

**Constraints:** `1 ≤ nodes ≤ 10⁵`, `0 ≤ Node.val ≤ 9`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **midpoint + reverse-half compare** ★ | [`palindrome_list.kara`](palindrome_list.kara) | [`palindrome_list.py`](palindrome_list.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Three moves, all in place:

1. **Find the middle** with slow/fast pointers — fast advances two nodes per step, so when it falls off the end, slow is at the midpoint.
2. **Reverse the second half** (everything after slow) with the three-cursor rewire — the same in-place reversal as [#206](../206-reverse-linked-list/).
3. **Compare** the first half from the head and the reversed second half from its new head, node by node; a single mismatch returns false.

The second half is never longer than the first, so for odd length the middle node is the natural pivot and is simply not compared. O(n) time, O(1) extra space (no value array).

## Kāra features exercised

- **Index-pool singly-linked list** — `Vec[Node]` with a `mut` `i64` `next` (`-1` = null); the reversal rewires `next` indices in place (`nodes[cur].next = prev`).
- **Two-hop pointer arithmetic** — the midpoint loop reads `nodes[nodes[fast].next].next`, a double index through the pool, guarded so it never dereferences past the end.
- **`mut ref Vec[Node]`** — `is_palindrome` mutates the list (it reverses a half), so it takes `mut ref` and forwards it to `reverse`; the driver passes the owned list with the `mut` marker.

## Running

```bash
karac run   palindrome_list.kara
karac build palindrome_list.kara && ./palindrome_list
python3 palindrome_list.py
diff <(karac run palindrome_list.kara) <(python3 palindrome_list.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
