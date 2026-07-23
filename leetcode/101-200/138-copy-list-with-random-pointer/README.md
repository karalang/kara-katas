# 138. Copy List with Random Pointer

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Hash Table · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/copy-list-with-random-pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)

A linked list where each node carries a `next` pointer **and** a `random` pointer that may target **any** node in the list (forward, backward, itself) or be null. Return a **deep copy**: a brand-new list whose `next`/`random` structure mirrors the original, sharing no nodes with it.

```
vals   = [7, 13, 11, 10, 1]
random = [-1, 0, 4, 2, 0]      # index each node's `random` points at (-1 = null)

  ->  7|-1   13|7   11|1   10|11   1|7      # each copied node's  val|random.val
```

**Constraints:** `0 ≤ n ≤ 1000`, `-10⁴ ≤ Node.val ≤ 10⁴`, `random` is null or points to a node in the list.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **id-indexed clone + re-wire** (`next` owns, `random` is `weak`) ★ | [`copy_random_list.kara`](copy_random_list.kara) ✓ | [`copy_random_list.py`](copy_random_list.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. Zero diagnostics, valgrind/LSan-clean — **including the `random`-cyclic graph**, which plain reference counting cannot collect.

## The mechanism — `weak` breaks the cycle

The `random` edges make the object graph **cyclic** (`13.random → 7`, `1.random → 7`, and a node can point at itself). Under pure reference counting a cycle is never collected — every node in it keeps a positive strong count forever. Kāra's escape hatch (design.md § Cycles, Swift-like) is the **`weak` reference**: a `weak Node` field does **not** contribute to the target's strong count, so the `next` chain alone owns the nodes and the whole structure is reclaimed when the owning `Vec`/chain drops.

```kara
shared struct Node {
    val: i64,
    id: i64,
    mut next: Option[Node],   // strong — owns the chain
    mut random: weak Node,     // weak — non-owning back/cross edge
}
```

- **Store (downgrade):** `copies[i].random = copies[r.id];` — assigning a strong handle to a `weak` field downgrades it (adds a weak count, no strong retain).
- **Read (upgrade):** `match orig[i].random { Some(r) => …, None => … }` — a `weak` field **reads as `Option[Node]`**: `Some(node)` while a strong reference to the target still exists, `None` once the last one is gone (never a dangling read).

The deep-copy is the canonical two-pass map algorithm, indexed by a stable per-node `id`: pass 1 clones every node; pass 2 re-wires `next` (strong) and `random` (weak) against the **fresh** copies.

## Kāra features exercised

- **`weak T` references** — the flagship feature this kata drove into existence: downgrade-on-store, upgrade-to-`Option[T]`-on-read, cycle-free reclamation. First corpus kata to use them.
- **`Vec[shared struct]` with indexed field access** — `orig[i].val`, `copies[i].next = …`, indexed `weak` store/read `copies[i].random = copies[r.id]`.
- **`Option[shared]` `next` chains + `match` traversal.**

> **Compiler friction surfaced & fixed by this kata.**
> 1. **`weak` was declaration-only** ([kara `B-2026-07-19-8`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)): the modifier parsed and satisfied the cycle checker, but there was no way to construct, store, or read a weak value — the feature was unusable. Now fully implemented (runtime two-count control block, typechecker coercion + `Option[T]` read typing, downgrade/upgrade/weak-drop codegen) across interpreter, JIT, and AOT.
> 2. **Indexed-read field-offset drift** ([kara `B-2026-07-19-13`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)): the `nodes[i].field` **read** hardcoded heap offset `idx + 1` instead of routing through `shared_gep_layout`, so a weak-headered node (which carries an extra `{ strong, weak }` control word) read the weak **count** where the value should be — a silent run-vs-build divergence. Fixed by the same funnel that already governs the store side (`B-2026-07-19-6`).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`3634862639337`). Workload: index-pool deep copy of a 3000-node random-pointer list x 40K passes (build-once + punch); Kara uses weak-ref Nodes, C/Rust/Go/Py a flat old->new map; sink=structure checksum.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 372.1 ms | 0.07× |
| C `clang -O3` | 407.0 ms | 0.08× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 448.1 ms | 0.09× |
| Go | 514.5 ms | 0.10× |
| **Kāra (codegen)** | 5.18 s | 1.00× |
| Python (scale lane) | 29.45 s | 5.69× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   copy_random_list.kara
karac build copy_random_list.kara && ./copy_random_list
python3 copy_random_list.py
diff <(karac run copy_random_list.kara) <(python3 copy_random_list.py) && echo OK
```

## Notes

The first corpus kata built on `weak` references. It exercises the full weak lifecycle — downgrade, upgrade-to-`Option`, and cycle-free drop — and surfaced two real compiler defects (`B-2026-07-19-8`, `B-2026-07-19-13`), both fixed in the compiler rather than worked around in the kata.
