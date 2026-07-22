# 206. Reverse Linked List

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List · Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-linked-list](https://leetcode.com/problems/reverse-linked-list/)

Reverse a singly-linked list and return the new head.

```
[1,2,3,4,5]  ->  [5,4,3,2,1]
[1,2]        ->  [2,1]
[]           ->  []
```

**Constraints:** `0 ≤ nodes ≤ 5000`, `-5000 ≤ Node.val ≤ 5000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **iterative three-cursor** ★ | [`reverse_list.kara`](reverse_list.kara) | [`reverse_list.py`](reverse_list.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Keep three cursors: `prev` (the reversed portion built so far, initially empty), `cur` (the node being flipped), and a **saved `nxt`** so the forward link isn't lost when `cur.next` is rewired backwards. Each step: stash `nxt = cur.next`, point `cur.next` at `prev`, then slide all three forward (`prev = cur; cur = nxt`). When `cur` falls off the end, `prev` is the new head. O(n) time, O(1) extra space — the canonical linked-list warm-up.

## Kāra features exercised

- **Index-pool singly-linked list** — `Vec[Node]` with an `i64` `next` (`-1` = null). Reversal rewires `next` indices (`nodes[cur].next = prev`) — a struct-field index-assign, no allocation.
- **Three-cursor pointer dance** with the saved-`nxt` idiom, and `mut ref Vec[Node]` for the mutation vs `ref Vec[Node]` for the read-only traversal.

## Running

```bash
karac run   reverse_list.kara
karac build reverse_list.kara && ./reverse_list
python3 reverse_list.py
diff <(karac run reverse_list.kara) <(python3 reverse_list.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
