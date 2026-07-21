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

## Compiler friction surfaced by this kata

Insertion-sort splicing on a `weak`-next list surfaced **two** distinct `karac` bugs — both filed, neither worked around:

1. **Spurious `E0500` on the weak-to-weak splice** — the canonical `nodes[i].next = nodes[prev].next` (both sides indexing the same `Vec[shared]`, RHS a `weak`-field read) makes `karac check` report `value 'nodes' moved here, used again here`, while `karac build`/`run` compile and run it **correctly** and **valgrind-clean** (the reuse takes the advisory RC fallback). A strong-element RHS (`nodes[i].next = nodes[prev]`, the #143 shape) is not flagged — the false-positive is specific to the extra `weak`-field access on the RHS. Advisory (ownership errors other than aliased exclusive borrows do not block the build), so the kata keeps the natural splice. Filed as [kara `B-2026-07-21-20`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl).

2. **Double-free / leak when the successor is materialized into a strong temp** — writing the splice as `let after: Option[Node] = nodes[prev].next; nodes[i].next = after; …` (upgrade the weak read to a strong `Option[Node]`, then store it back into a `weak` field) `check`s clean but **leaks the upgraded node** (40 bytes for a single splice) and **double-frees** across multiple splices (`free(): double free detected`). The direct weak-to-weak copy above avoids the strong round-trip and is memory-correct. Filed as [kara `B-2026-07-21-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl).

## Running

```bash
karac run   insertion_sort_list.kara
karac build insertion_sort_list.kara && ./insertion_sort_list
python3 insertion_sort_list.py
diff <(karac run insertion_sort_list.kara) <(python3 insertion_sort_list.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.
