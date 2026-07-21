# 146. LRU Cache

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table · Linked List · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/lru-cache](https://leetcode.com/problems/lru-cache/)

Design a cache with a fixed capacity supporting `get(key)` and `put(key, value)` in **O(1)** each. When a `put` would exceed capacity, evict the **least-recently-used** entry. A `get` or a value-updating `put` counts as a use.

```
LRUCache(2)
put(1,1) put(2,2) get(1)→1 put(3,3)[evict 2] get(2)→-1 put(4,4)[evict 1] get(1)→-1 get(3)→3 get(4)→4

  ->  1  -1  -1  3  4        # the get results, in order
```

**Constraints:** `1 ≤ capacity ≤ 3000`, `0 ≤ key,value ≤ 10⁵`, up to `2·10⁵` calls.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **hash map + index-pool doubly-linked list** ★ | [`lru_cache.kara`](lru_cache.kara) ✓ | [`lru_cache.py`](lru_cache.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`: 0 errors / 0 leaks).

## The mechanism

The textbook O(1) LRU is a **hash map + doubly-linked list**: the map gives O(1) key lookup, the list orders entries by recency (front = most recent, back = least). `get`/`put` move the touched node to the front; an over-capacity `put` evicts the node just before the back.

This implementation uses an **index-based node pool** rather than heap pointers — a common, robust LRU representation:

- `pool: Vec[DNode]` owns every node. `pool[0]` is the **head sentinel**, `pool[1]` the **tail sentinel**, real nodes at index 2+. Sentinels remove all null-edge branching from `unlink`/`push_front`.
- `prev`/`next` are `i64` **pool indices** — a pointer-free doubly-linked list.
- `map: Map[i64, i64]` maps each key to its pool index.

Every operation (`unlink`, `push_front`, `move_front`, evict) is O(1) index arithmetic. Because the pool owns the nodes, there is no reference counting to get wrong — and no cycle, since the list links are plain integers.

## Kāra features exercised

- **`Vec[struct]` with indexed mutable-field stores** — `pool[i].next = n`, `pool[i].val = v`, threaded through `mut ref Vec[DNode]` helpers (`unlink`/`push_front`) with the call-site `mut` marker at fresh-binding call sites and bare forwarding where `pool` is already a `mut ref`.
- **`Map[i64, i64]`** — `contains_key` / `get().unwrap()` / `insert` / `remove` for the key→index directory.
- **Sentinel-node doubly-linked list** — a self-contained O(1) design in plain Kāra.

> **Compiler friction surfaced by this kata.** A `Map[K, shared V]` value store was the first design considered (nodes held directly in the map). That path hit [kara `B-2026-07-19-16`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): a **discarded** `m.remove(k);` over a `Map` of shared values leaks the removed node (the value is moved out into `Some(old)`, which the discarded expression statement never drops; binding + consuming it is clean). The kata uses the **index-pool** design instead — a legitimate, common LRU technique that keeps the map's values plain `i64` indices, avoiding shared-value ownership in the map entirely — and the gap is filed for a later fix.

## Running

```bash
karac run   lru_cache.kara
karac build lru_cache.kara && ./lru_cache
python3 lru_cache.py
diff <(karac run lru_cache.kara) <(python3 lru_cache.py) && echo OK
```

## Notes

The first *design-a-data-structure* kata in the corpus. It implements a real O(1) LRU (hash map + sentinel doubly-linked list) via an index-based node pool, and surfaced the discarded-`Map.remove`-of-shared-value leak (`B-2026-07-19-16`).
