# 145. Binary Tree Postorder Traversal

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-postorder-traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/)

Return node values in **postorder**: left subtree, then right subtree, then the root.

```
[1,null,2,3]  ->  3 2 1
[]            ->  (empty)
full tree     ->  4 5 2 6 3 1
```

**Constraints:** `0 ≤ n ≤ 100`, `-100 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **recursive DFS** ★ | [`postorder.kara`](postorder.kara) ✓ | [`postorder.py`](postorder.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Postorder = **recurse left, recurse right, then visit** — the mirror of [#144](../144-binary-tree-preorder-traversal/)'s preorder (visit-first), with the `out.push(n.val)` moved after the two recursive calls. Same acyclic tree of strong `Option[TreeNode]` children and the same `mut ref Vec[i64]` accumulator threaded through the recursion.

## Kāra features exercised

- **`mut ref Vec[i64]` accumulator** across a recursive `Option[shared TreeNode]` DFS (call-site `mut` marker at the root call).
- **Strong `Option` tree children** — acyclic, no `weak`.

## Running

```bash
karac run   postorder.kara
karac build postorder.kara && ./postorder
python3 postorder.py
diff <(karac run postorder.kara) <(python3 postorder.py) && echo OK
```

## Notes

The postorder sibling of [#144](../144-binary-tree-preorder-traversal/) — identical structure, only the visit-vs-recurse order differs. Clean pass, no compiler friction.
