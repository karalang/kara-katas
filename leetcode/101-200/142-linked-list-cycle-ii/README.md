# 142. Linked List Cycle II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/linked-list-cycle-ii](https://leetcode.com/problems/linked-list-cycle-ii/)

Return the node where the cycle **begins**, or null if the list is acyclic. Where [#141](../141-linked-list-cycle/) asks *whether* a cycle exists, #142 asks *where* it starts.

```
[3,2,0,-4]   tail -> node 1   ->  node 1   (id 1)
[1,2]        tail -> node 0   ->  node 0   (id 0)
[1]          tail -> null     ->  null     (-1)
[1,2,3,4,5]  linear           ->  null     (-1)
```

**Constraints:** `0 ≤ n ≤ 10⁴`, `-10⁵ ≤ Node.val ≤ 10⁵`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Floyd's two-phase** ★ | [`linked_list_cycle_ii.kara`](linked_list_cycle_ii.kara) ✓ | [`linked_list_cycle_ii.py`](linked_list_cycle_ii.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`), including the cyclic inputs. Output is the entry node's `id`, or `-1`.

## The mechanism

Floyd's two phases:

1. **Meet.** Advance `slow` one step and `fast` two until they meet inside the cycle (or `fast` falls off the end → no cycle).
2. **Locate.** Reset `slow` to the head and advance both pointers one step at a time. They meet exactly at the cycle's entry — the classic distance identity: the head-to-entry length equals the meeting-point-to-entry length (both are `k mod L`).

As in [#141](../141-linked-list-cycle/), nodes are `Vec`-owned (strong) and `next` is a **`weak Node`** overlay, so the cyclic fixture is **leak-free** — reference counting reclaims it because the weak `next` links don't hold the cycle alive.

## Kāra features exercised

- **`weak Node` list link** — both Floyd phases walk `slow = s.next` / `fast = f.next` as weak-field reads upgraded to `Option[Node]`.
- **Vec-owned + weak overlay** — cyclic list reclaimed clean (verified).
- **Two-phase `Option[Node]` traversal** with node-identity (`id`) comparison.

## Running

```bash
karac run   linked_list_cycle_ii.kara
karac build linked_list_cycle_ii.kara && ./linked_list_cycle_ii
python3 linked_list_cycle_ii.py
diff <(karac run linked_list_cycle_ii.kara) <(python3 linked_list_cycle_ii.py) && echo OK
```

## Notes

The locate-the-entry companion to [#141](../141-linked-list-cycle/), sharing the Vec-owned + `weak`-next model that makes a cyclic linked list reclaimable under reference counting. (As with #141, the default auto-par build shows one benign valgrind entry from the parallel runtime's `pthread_create` TLS allocation; the sequential build is fully clean.)
