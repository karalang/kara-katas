# 148. Sort List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Merge Sort · Divide & Conquer · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/sort-list](https://leetcode.com/problems/sort-list/)

Sort a singly linked list in **O(n log n)** time using top-down **merge sort**: split the list in half, recursively sort each half, then merge the two sorted halves.

```
[4,2,1,3]      ->  1 2 3 4
[-1,5,3,4,0]   ->  -1 0 3 4 5
[]             ->  (empty)
[1]            ->  1
[3,3,1,2,2]    ->  1 2 2 3 3
[5,4,3,2,1]    ->  1 2 3 4 5
```

**Constraints:** `0 ≤ n ≤ 5·10⁴`, `-10⁵ ≤ Node.val ≤ 10⁵`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **top-down merge sort + weak-next rewire** ★ | [`sort_list.kara`](sort_list.kara) ✓ | [`sort_list.py`](sort_list.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The fifth `weak`-next kata in the #141/#142/#143/#147 linked-list cluster, and the first to use **recursion over the list**. Nodes are `Vec`-owned (strong) with a `weak Node` next overlay, so every split (cut a `next`) and merge (re-point `next` in sorted order) only rewrites weak links and stays leak-free. Chains are tracked by **head index** (`-1` = empty):

- **`split_mid`** — slow/fast pointers walk to the middle; cut the first half's tail (`nodes[slow].next = None`) and return the second half's head.
- **`sort_chain`** (recursive) — base case is an empty or single-node chain; otherwise split, sort each half, merge. Takes `nodes: mut ref Vec[Node]` and threads it through the recursive calls.
- **`merge`** — walk both sorted chains, appending the smaller head each step via `nodes[tail].next = nodes[pick]` (weak-from-strong, the #143 shape), then attach the remaining tail.

Finally, traverse from the sorted head via `next` and emit the values.

## Kāra features exercised

- **Recursion with `mut ref Vec[Node]`** — `sort_chain` calls itself on both halves, mutating the shared node buffer through a `mut ref` param across recursion depth.
- **Weak-next split & merge** — `nodes[slow].next = None` cuts a link (weak-drop the old occupant); `nodes[tail].next = nodes[pick]` re-links (weak-from-strong downgrade).
- **Weak-read navigation** — `match nodes[i].next { Some(nx) => nx.id, None => -1 }` (`next_idx`) walks the chain by index.
- **`if`-expression** (`let rest: i64 = if ai != -1 { ai } else { bi };`) and **`String` join** for output.

## Running

```bash
karac run   sort_list.kara
karac build sort_list.kara && ./sort_list
python3 sort_list.py
diff <(karac run sort_list.kara) <(python3 sort_list.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. The recursive `mut ref Vec` merge sort compiled and ran cleanly on the first try, exercising the weak-ref RC accounting fixed for #147 (kara `B-2026-07-21-20`/`-21`) without re-triggering it.
