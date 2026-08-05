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

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`65640802092`). Workload: 32M PRNG get/put ops, cap=1024 key-range=4096; index-pool DLL + key->slot map (C flat table, others hashmap), constant eviction.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-08-05 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 197.6 ms | 0.84× |
| **Kāra (codegen)** | 236.6 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 768.6 ms | 3.25× |
| Rust `-O` | 778.2 ms | 3.29× |
| Go | 977.0 ms | 4.13× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac 2ed967c9f1c1); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   lru_cache.kara
karac build lru_cache.kara && ./lru_cache
python3 lru_cache.py
diff <(karac run lru_cache.kara) <(python3 lru_cache.py) && echo OK
```

## Notes

The first *design-a-data-structure* kata in the corpus. It implements a real O(1) LRU (hash map + sentinel doubly-linked list) via an index-based node pool, and surfaced the discarded-`Map.remove`-of-shared-value leak (`B-2026-07-19-16`).

It has since surfaced a second, larger one — now **fixed**, and the fix left this kata faster than it has ever been.

**`B-2026-08-05-4` (fixed) — Kāra's row regressed 1.76× (231.7 ms → 422.9 ms) between the 2026-07-28 and 2026-08-04 measurements**, with the kata source unchanged. Root-caused by holding the compiler fixed and swapping only the runtime archive: the cause was `B-2026-07-31-21`'s fix, which stopped the map's capacity from ratcheting on total removals and instead performed a **same-width compacting rehash** when the live count sat at or below ⅜ of capacity. An LRU is the canonical remove-heavy map — every insert past capacity evicts — so the live count parks near that threshold and the O(len) compaction re-fires on eviction after eviction, where the old code paid one doubling and then stopped rehashing. That fix bought a large RSS win (297 MB → 10 MB on a sliding window) and was never a revert candidate; the wall-time it cost a churn-dominated map was simply the half nobody had measured, because no bench in the corpus covered that shape. This kata is now that bench.

It was closed in two independent parts, and the second one is why the row above beats the pre-regression baseline rather than merely restoring it:

- **The compaction band widened from ⅜ to ³⁄₁₆** (`73237002`), making the compacting rehash fire ~3× less often. At the ⅜ edge a churning table re-hashes its *entire live set once per operation*, forever — `rehash_from` cannot skip the per-key hash because buckets store no hash. That alone recovered the regression.
- **Removal stopped manufacturing the tombstones that drive the rehash** (`45398dd9`). A tombstone only needs to exist when a probe chain can continue past the bucket; when the next bucket is already `EMPTY`, none can, so the slot is released outright. Lookups then stop walking tombstone runs — a win no capacity policy can buy, and the reason this lands *below* the old baseline.

The two stack rather than subsume each other: compaction re-hash work on the runtime's sliding-window churn test is 15.52% of the workload at ⅜ with tombstoning, 6.29% at ³⁄₁₆, 7.06% at ⅜ with the release, and **1.92%** with both.

**What the numbers cost.** Kāra's runtime peak RSS on this workload rose 1.36 MB → 1.41 MB (+3.6%) — the ³⁄₁₆ band deliberately holds the table one doubling wider than ⅜ did. That is the trade the fix makes, and at 48 KB against a 1.79× speedup it is the right side of it. Note also that every reference language in the table above reads ~5% slower than the 2026-08-04 snapshot despite byte-identical binaries; that is machine state between sessions, not a toolchain change, so Kāra's improvement here is if anything understated.
