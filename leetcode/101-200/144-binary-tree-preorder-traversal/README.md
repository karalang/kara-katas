# 144. Binary Tree Preorder Traversal

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-preorder-traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/)

Return node values in **preorder**: root first, then the left subtree, then the right.

```
    1              1
     \           /   \
      2          2     3
     /          / \   /
    3          4   5 6

[1,null,2,3]  ->  1 2 3
[]            ->  (empty)
full tree     ->  1 2 4 5 3 6
```

**Constraints:** `0 ≤ n ≤ 100`, `-100 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **recursive DFS** ★ | [`preorder.kara`](preorder.kara) ✓ | [`preorder.py`](preorder.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Preorder = **visit, then recurse left, then recurse right**. The recursion accumulates values into a shared output buffer:

```kara
fn preorder(node: Option[TreeNode], out: mut ref Vec[i64]) {
    match node {
        None => {}
        Some(n) => {
            out.push(n.val);
            preorder(n.left, out);
            preorder(n.right, out);
        }
    }
}
```

Because a binary tree is **acyclic**, `left`/`right` are ordinary strong `Option[TreeNode]` children — no `weak` needed. The whole tree is reclaimed by reference counting when the root handle drops.

## Kāra features exercised

- **`mut ref Vec[i64]` accumulator** — the output buffer is threaded through the recursion by mutable borrow. The top-level call marks the argument (`preorder(root, mut out)`, the call-site mutation marker); the recursive calls forward the already-`mut ref` binding without re-marking.
- **`Option[shared TreeNode]` recursion** — `match` on each child; a null child is the base case.
- **Strong `Option` tree children** — acyclic, so no `weak` (contrast the #141–143 linked-list cluster, where cycles forced weak links).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`10924394284840801`). Workload: iterative preorder (explicit index-pool stack) over a 50k-node BST x 400 passes, pointer-chase.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 288.9 ms | 0.87× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 292.4 ms | 0.88× |
| Go | 299.0 ms | 0.90× |
| Rust `-O` | 314.8 ms | 0.95× |
| **Kāra (codegen)** | 330.8 ms | 1.00× |
| Python (scale lane) | 6.87 s | 20.77× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   preorder.kara
karac build preorder.kara && ./preorder
python3 preorder.py
diff <(karac run preorder.kara) <(python3 preorder.py) && echo OK
```

## Notes

First tree kata of the traversal cluster (144/145). Clean dogfood of `mut ref Vec` accumulation across a recursive `Option[shared]` DFS — no compiler friction beyond the expected call-site `mut` marker.
