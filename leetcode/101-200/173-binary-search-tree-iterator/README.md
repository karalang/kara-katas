# 173. Binary Search Tree Iterator

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Stack · Tree · Design · Binary Search Tree · Binary Tree · Iterator &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-search-tree-iterator](https://leetcode.com/problems/binary-search-tree-iterator/)

Implement an **in-order iterator** over a BST: `next()` returns the next-smallest value, `has_next()` reports whether more remain. Target **O(h) memory** and **amortised O(1)** per `next`.

```
BST [5,3,8,1,4,7,9]  ->  next…  1 3 4 5 7 8 9
```

**Constraints:** `1 ≤ nodes ≤ 10⁵`; `next` is only called when `has_next` is true.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **controlled-recursion stack** ★ | [`bst_iterator.kara`](bst_iterator.kara) | [`bst_iterator.py`](bst_iterator.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Instead of materialising the whole in-order traversal, keep an explicit **stack** holding the path of not-yet-visited nodes — the current **left spine**. `has_next` is "stack non-empty". `next` pops the top (the current smallest), then pushes the left spine of its **right child**. Each node is pushed and popped exactly once over a full traversal, so the amortised cost is O(1) and the stack never exceeds the tree height O(h). This is the standard "flatten lazily" pattern that makes an iterator out of a recursive traversal.

## Kāra features exercised

- **Index-pool tree** — `Vec[Node]` with `i64` `left`/`right` child indices (`-1` = null), the corpus idiom for pointer structures without RC. `insert` appends fresh nodes and rewires `nodes[root].left`/`.right` via index-assign on a struct field.
- **Struct + free functions, no impl blocks** — the "class" (`BstIterator { stack: Vec[i64] }`) is threaded through `mut ref` / `ref` receivers.
- **Recursion under `mut ref Vec[Node]`** — `insert` recurses on the shared node pool; the recursive call *forwards* the already-`mut ref` `nodes` without re-marking, while the top-level call on the fresh `nodes` binding uses the `mut nodes` marker (the call-site mutation-marker rule).
- **`Vec[i64]` as a stack** — `push` / `pop` (→ `Option`, discarded) / peek via `stack[len-1]`.

## Running

```bash
karac run   bst_iterator.kara
karac build bst_iterator.kara && ./bst_iterator
python3 bst_iterator.py
diff <(karac run bst_iterator.kara) <(python3 bst_iterator.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
