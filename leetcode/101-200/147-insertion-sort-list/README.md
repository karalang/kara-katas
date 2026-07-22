# 147. Insertion Sort List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Insertion Sort · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/insertion-sort-list](https://leetcode.com/problems/insertion-sort-list/)

Sort a singly linked list using **insertion sort**: for each node, scan the already-sorted prefix from the head to find its insertion point, then splice it in.

```
[4,2,1,3]      ->  1 2 3 4
[-1,5,3,4,0]   ->  -1 0 3 4 5
[1]            ->  1
[3,1,2,2,1]    ->  1 1 2 2 3
[5,4,3,2,1]    ->  1 2 3 4 5
```

**Constraints:** `1 ≤ n ≤ 5000`, `-5000 ≤ Node.val ≤ 5000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **sorted-prefix scan + weak-next splice** ★ | [`insertion_sort_list.kara`](insertion_sort_list.kara) ✓ | [`insertion_sort_list.py`](insertion_sort_list.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The fourth `weak`-next kata in the #141/#142/#143 linked-list cluster. Nodes are `Vec`-owned (strong) with a `weak Node` next overlay, so re-pointing the links during sorting stays leak-free.

`head` indexes the sorted list's first node (`-1` while empty). For each input node `i`:

- **Empty list** — it becomes the head.
- **Belongs before the head** (`nodes[head].val >= v`) — front-insert: `nodes[i].next = nodes[head]; head = i`.
- **Otherwise** — walk the sorted prefix to the last node `prev` whose successor value is still `< v` (or whose successor is empty), then splice: `nodes[i].next = nodes[prev].next; nodes[prev].next = nodes[i]`.

Then traverse from `head` via `next` (weak reads upgraded to `Option[Node]`) and emit the values.

## Kāra features exercised

- **Weak-next splice** — the mid-chain insertion `nodes[i].next = nodes[prev].next` is a **weak-to-weak** field copy (the successor link is handed to the new node, then repointed), plus front-insert `nodes[i].next = nodes[head]` (weak-from-strong, the #143 shape).
- **Weak-read scan** — `match nodes[prev].next { Some(nxt) => … }` walks the sorted prefix by upgrading each weak link and reading `nxt.id`.
- **`String` join** of the emitted values for output.

## Compiler friction surfaced & fixed by this kata

Insertion-sort splicing on a `weak`-next list surfaced **two** distinct `karac` bugs — both **fixed in the compiler** ([kara `e1ddb43`](https://github.com/karalang/kara/commit/e1ddb43)), neither worked around:

1. **Spurious `E0500` on the weak-to-weak splice** ([kara `B-2026-07-21-20`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)) — the canonical `nodes[i].next = nodes[prev].next` (both sides indexing the same `Vec[shared]`, RHS a `weak`-field read) made `karac check` report `value 'nodes' moved here, used again here`. You cannot move out through an index projection, so the RHS `nodes[prev].next` is a *read* of `nodes`, not a consume — the ownership pass now classifies the container root below an index as `Read`, matching the bare-element form (`nodes[i].next = nodes[prev]`, the #143 shape) which was never flagged.

2. **Double-free / leak when the successor is materialized into a strong temp** ([kara `B-2026-07-21-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)) — writing the splice as `let after: Option[Node] = nodes[prev].next; nodes[i].next = after; …` (upgrade the weak read to a strong `Option[Node]`, then store it back into a `weak` field) leaked the upgraded node (40 bytes/splice) and double-freed across several splices. A weak-field read is a *borrow* (no strong retain), so the `Option[shared]` binding owned no `+1` to balance its scope-exit refcount decrement; codegen now emits the matching balancing inner rc-inc when a weak read initializes such a binding. Both the direct weak-to-weak copy (shipped) and the materialize-then-restore form are now memory-correct.

Both fixes carry regression tests (`ownership::test_weak_field_read_index_assign_no_spurious_move`, `memory_sanitizer::asan_weak_read_into_option_binding_then_weak_store_no_leak`). With them, this kata now `karac check`s cleanly.

## Running

```bash
karac run   insertion_sort_list.kara
karac build insertion_sort_list.kara && ./insertion_sort_list
python3 insertion_sort_list.py
diff <(karac run insertion_sort_list.kara) <(python3 insertion_sort_list.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.
