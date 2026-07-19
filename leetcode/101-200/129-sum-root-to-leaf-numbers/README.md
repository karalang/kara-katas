# 129. Sum Root to Leaf Numbers

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · DFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/sum-root-to-leaf-numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/)

Each root-to-leaf path spells a base-10 number (digits top to bottom). Return the sum over all such paths.

```
    1            4               1·2 = 12, 1·3 = 13  -> 25
   / \          / \
  2   3        9   0             4·9·5=495, 4·9·1=491, 4·0=40 -> 1026
              / \
             5   1
```

**Constraints:** node count `1..1000`, each `0 ≤ node.val ≤ 9`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **DFS with a running path-number** ★ | [`sum_numbers.kara`](sum_numbers.kara) ✓ | [`sum_numbers.py`](sum_numbers.py) ✓ |

`✓` runs end-to-end today: interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`) all agree with the Python mirror. Validated against the known answers (25, 1026, single-node 7). Zero diagnostics, valgrind-clean.

## The mechanism

One DFS carrying a running value `cur = cur * 10 + node.val` down each branch; at a leaf, `cur` **is** the path number, so it is returned directly, and internal nodes sum their two subtrees. O(n), O(h) stack. Node type is the `shared struct TreeNode` (RC) shared with [#112](../112-path-sum/)/[#124](../124-binary-tree-maximum-path-sum/).

## Kāra features exercised

- **`shared struct TreeNode` (RC)** post-order-style DFS over `Option[TreeNode]`, borrowing each child.
- **Leaf detection via `match n.left { None => … }`** — the two-child `None` test that distinguishes a leaf from an internal node.
- **Overflow-checked digit accumulation** — `cur * 10 + val` under kāra's default trap; the modular sink fold keeps the digest in i64.

## Running

```bash
karac run   sum_numbers.kara
karac build sum_numbers.kara && ./sum_numbers
python3 sum_numbers.py
diff <(karac run sum_numbers.kara) <(python3 sum_numbers.py) && echo OK
```

## Notes

Dogfood-first tree kata; [#124](../124-binary-tree-maximum-path-sum/) is the neighbouring tree-traversal benchmark.
