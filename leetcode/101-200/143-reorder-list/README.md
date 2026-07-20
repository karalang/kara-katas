# 143. Reorder List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reorder-list](https://leetcode.com/problems/reorder-list/)

Reorder `L0 → L1 → … → Ln-1 → Ln` into `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …` — interleave the list with its own reverse, in place.

```
[1,2,3,4]     ->  1 4 2 3
[1,2,3,4,5]   ->  1 5 2 4 3
[1]           ->  1
[1,2]         ->  1 2
```

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `1 ≤ Node.val ≤ 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **inward two-pointer + weak-next rewire** ★ | [`reorder_list.kara`](reorder_list.kara) ✓ | [`reorder_list.py`](reorder_list.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The reordered **index** sequence is `0, n-1, 1, n-2, 2, n-3, …` — two pointers `lo`/`hi` walking inward from both ends, alternately emitting the low then the high index until they cross. (This is equivalent to the textbook "find middle → reverse second half → merge alternately", collapsed to a single inward sweep since the nodes are randomly addressable.)

The Kāra version then **rewires the weak `next` chain** to follow that order (`nodes[order[i]].next = nodes[order[i+1]]`) and walks it from the head to emit the result — exercising both weak store (the rewire) and weak read (the traversal). As in [#141](../141-linked-list-cycle/)/[#142](../142-linked-list-cycle-ii/), nodes are `Vec`-owned (strong) with a `weak Node` overlay, so re-pointing the links — even into the interleaved order — stays leak-free.

## Kāra features exercised

- **Weak-next rewire + traversal** — indexed weak store to build the new chain, then `cur = c.next` weak reads (upgraded to `Option[Node]`) to walk it.
- **Inward two-pointer index order** with an alternating `not take_lo` toggle.
- **`String` join** of the emitted values for output.

## Running

```bash
karac run   reorder_list.kara
karac build reorder_list.kara && ./reorder_list
python3 reorder_list.py
diff <(karac run reorder_list.kara) <(python3 reorder_list.py) && echo OK
```

## Notes

The third `weak`-next kata in the #141/#142/#143 linked-list cluster. Where #141/#142 only *read* the weak links, #143 *rewrites* them into a new order — a fuller exercise of weak store + read together, verified leak-free.
