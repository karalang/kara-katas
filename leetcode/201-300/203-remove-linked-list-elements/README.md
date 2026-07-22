# 203. Remove Linked List Elements

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List · Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-linked-list-elements](https://leetcode.com/problems/remove-linked-list-elements/)

Remove every node whose value equals `val` from a singly-linked list and return the new head.

```
[1,2,6,3,4,5,6], val=6  ->  [1,2,3,4,5]
[7,7,7,7],       val=7  ->  []
[7,7,1,7,2],     val=7  ->  [1,2]
```

**Constraints:** `0 ≤ nodes ≤ 10⁴`, `1 ≤ Node.val ≤ 50`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **head-skip + splice** ★ | [`remove_elements.kara`](remove_elements.kara) | [`remove_elements.py`](remove_elements.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Two cases a beginner meets here. **Leading matches** move the head, so first advance the head past any run of matching nodes. Then walk the rest with a trailing `prev`: on a match, **splice** `prev.next` past the removed node (leaving `prev` where it is); otherwise advance `prev`. In both cases `cur` marches forward on the removed node's original `next`. O(n) single pass.

## Kāra features exercised

- **Index-pool singly-linked list** — `Vec[Node]` with an `i64` `next` (`-1` = null), the corpus idiom for pointer structures. "Removing" a node is a `next`-index rewire (`nodes[prev].next = nodes[cur].next`) — a struct-field index-assign, no allocation.
- **`mut ref Vec[Node]`** threaded through the mutating `remove_elements`, with `ref Vec[Node]` for the read-only `show`.
- **`if`-expression** for the `next` link during build and the head-skip / splice control flow.

## Running

```bash
karac run   remove_elements.kara
karac build remove_elements.kara && ./remove_elements
python3 remove_elements.py
diff <(karac run remove_elements.kara) <(python3 remove_elements.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
