# 199. Binary Tree Right Side View

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-right-side-view](https://leetcode.com/problems/binary-tree-right-side-view/)

Standing to the **right** of a binary tree, return the values visible top to bottom — the last node on each level.

```
    1            [1,2,3,null,5,null,4]  ->  [1,3,4]
   / \
  2   3
   \   \
    5   4
```

**Constraints:** `0 ≤ nodes ≤ 100`, `-100 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **level-order (BFS) rightmost** ★ | [`right_side_view.kara`](right_side_view.kara) | [`right_side_view.py`](right_side_view.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A **breadth-first** sweep makes "right side view" fall out directly: process the tree one level at a time; the **rightmost** node of each level is exactly what you'd see from the right. Record it, then build the next level from the current level's children, left to right. O(n) nodes, each visited once.

## Kāra features exercised

- **Index-pool tree** — `Vec[Node]` with `i64` `left`/`right` indices (`-1` = null), built from a **level-order array** with a NULL sentinel (the standard LeetCode serialization), using a `Vec[i64]` queue + head cursor.
- **BFS frontier as `Vec[i64]`** — each level is a vector of node indices; `level = next` **reassigns** the frontier vector every iteration (a `Vec[i64]` move-reassign in a loop), verified valgrind-clean.
- **Struct-field index-assign** — `nodes[cur].left = li` wires children during the build.

## Running

```bash
karac run   right_side_view.kara
karac build right_side_view.kara && ./right_side_view
python3 right_side_view.py
diff <(karac run right_side_view.kara) <(python3 right_side_view.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
