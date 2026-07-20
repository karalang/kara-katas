# 141. Linked List Cycle

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/linked-list-cycle](https://leetcode.com/problems/linked-list-cycle/)

Does the linked list contain a cycle? Return `true` if some node can be reached again by following `next` pointers, `false` otherwise.

```
[3,2,0,-4]   tail -> node 1   ->  true
[1,2]        tail -> node 0   ->  true
[1]          tail -> null     ->  false
[1,2,3,4,5]  linear           ->  false
```

**Constraints:** `0 ≤ n ≤ 10⁴`, `-10⁵ ≤ Node.val ≤ 10⁵`; the cycle target (if any) is a valid node index.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Floyd's tortoise & hare** ★ | [`linked_list_cycle.kara`](linked_list_cycle.kara) ✓ | [`linked_list_cycle.py`](linked_list_cycle.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`: 0 errors / 0 leaks — **including the cyclic inputs**).

## The mechanism — and why `next` is `weak`

**Floyd's cycle detection:** a `slow` pointer advances one node per step, a `fast` pointer two. If the list cycles, `fast` laps `slow` and they meet; if `fast` reaches the end (`null`), there is no cycle. Nodes are compared by a unique `id` (identity).

**The RC twist:** the input to this problem *is* a cyclic linked list. Under reference counting a cycle formed by strong `next: Option[Node]` links would be **uncollectable** — every node in the loop keeps a positive strong count forever. So the nodes are owned by a `Vec[Node]` (the strong owners) and `next` is a **`weak Node`** overlay link:

```kara
shared struct Node {
    val: i64,
    id: i64,
    mut next: weak Node,   // weak — the list structure is a non-owning overlay
}
```

A `next` cycle is therefore **leak-free**: the `Vec` owns each node once, and the weak links (which don't contribute to the strong count) simply describe the traversal order. This is `weak` used as the *primary* link mechanism, not just a back-edge — the idiomatic reference-counted way to hold a cyclic structure. Traversal reads a `weak` field as `Option[Node]` (the upgrade), which Floyd's two-pointer walk consumes directly.

## Kāra features exercised

- **`weak Node` as the list link** — every `slow = s.next` / `fast = f2.next` is a weak-field read upgraded to `Option[Node]`; the cyclic fixture is built by indexed weak store (`nodes[i].next = nodes[nxt[i]]`).
- **`Vec[Node]` strong ownership + weak overlay** — the cycle is reclaimed cleanly (verified), the concrete payoff of the `weak` feature.
- **`Option[Node]` two-pointer walk** — nested `match` over the fast/slow cursors, comparing node identity by `id`.

## Running

```bash
karac run   linked_list_cycle.kara
karac build linked_list_cycle.kara && ./linked_list_cycle
python3 linked_list_cycle.py
diff <(karac run linked_list_cycle.kara) <(python3 linked_list_cycle.py) && echo OK
```

## Notes

The second `weak`-reference kata (after [#138](../138-copy-list-with-random-pointer/)), and the first to use `weak` as the **primary** list link rather than a back-edge. It demonstrates the headline `weak` payoff directly: a cyclic linked list that reference counting reclaims leak-free. (The default auto-par build shows one benign valgrind entry — the parallel runtime's `pthread_create` TLS allocation, not a kata defect; the sequential `KARAC_AUTO_PAR=0` build is fully clean.)
