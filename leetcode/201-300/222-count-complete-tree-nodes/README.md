# 222. Count Complete Tree Nodes

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Binary Tree · Binary Search · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/count-complete-tree-nodes](https://leetcode.com/problems/count-complete-tree-nodes/)

Count the nodes of a **complete** binary tree — every level full except possibly the last, which fills left to right — in better than O(n).

```
[1,2,3,4,5,6]      ->  6
[1,2,3,4,5,6,7]    ->  7   (a perfect tree)
[]                 ->  0
```

**Constraints:** `0 ≤ nodes ≤ 5·10⁴`; the tree is guaranteed complete.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **spine-height recursion** ★ | [`count_nodes.kara`](count_nodes.kara) | [`count_nodes.py`](count_nodes.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Naively counting is O(n); completeness lets us do O(log²n). For a subtree, walk its **far-left spine** and its **far-right spine** and compare heights:

- **Equal heights** → the subtree is *perfect*, so it holds exactly `2^h - 1` nodes (computed with a bit shift `1 << h`) — no need to visit any of them.
- **Different heights** → the last level is only partially filled; recurse into both children and return `1 + count(left) + count(right)`.

At most one of the two children can itself be non-perfect at each level, so the recursion depth is O(log n) and each level does O(log n) height work: O(log²n) total.

## Kāra features exercised

- **Index-pool binary tree** — `Vec[Node]` with `i64` `left`/`right` (`-1` = null), built from a complete-tree level-order array (children of `i` are `2i+1`, `2i+2`).
- **Bit shift for powers of two** — `(1 << h) - 1` counts a perfect subtree without a loop.
- **`ref Vec[Node]` recursion** — the spine walks and `count_nodes` borrow the pool read-only; recursion follows `nodes[idx].left` / `.right` indices.

## Running

```bash
karac run   count_nodes.kara
karac build count_nodes.kara && ./count_nodes
python3 count_nodes.py
diff <(karac run count_nodes.kara) <(python3 count_nodes.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
