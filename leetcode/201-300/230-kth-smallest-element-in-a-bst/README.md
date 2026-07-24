# 230. Kth Smallest Element in a BST

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Binary Search Tree · In-order Traversal · Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/kth-smallest-element-in-a-bst](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

Return the **k-th smallest** value (1-indexed) in a binary search tree.

```
BST of [3,1,4,2], k=1  ->  1
                 k=3   ->  3
BST of [5,3,6,2,4,1], k=3  ->  3
```

**Constraints:** `1 ≤ k ≤ n ≤ 10⁴`, `0 ≤ Node.val ≤ 10⁴`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **iterative in-order** ★ | [`kth_smallest_bst.kara`](kth_smallest_bst.kara) | [`kth_smallest_bst.py`](kth_smallest_bst.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

An **in-order** traversal of a BST — left subtree, node, right subtree — visits values in ascending order. So the k-th node visited *is* the k-th smallest, and the walk can stop the instant its counter hits `k` (no need to traverse the rest).

The traversal is iterative with an explicit stack: push the entire left spine, then repeatedly pop a node (visit it, bumping the count), and descend into its right child, which restarts the spine-pushing from there. The tree itself is built by ordinary BST insertion from a value list — smaller values go left, larger-or-equal go right.

## Kāra features exercised

- **Index-pool BST** — `Vec[Node]` with `i64` `left`/`right` (`-1` = null); insertion recurses and writes back child indices (`nodes[root].left = insert(...)`), with `mut ref Vec[Node]` for the build and `ref Vec[Node]` for the read-only walk.
- **Iterative in-order with a `Vec[i64]` stack** — `push`/`pop` (→ `Option`, matched) drive the spine-and-visit loop, whose condition `cur != -1 or stack.len() > 0` handles both live cursor and pending stack.
- **Early exit** — returns at `count == k` rather than materialising the full sorted order.


## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`151017441029646`). Workload: iterative in-order kth_smallest over a 3000-node BST, 140k queries with varying k (pointer-chasing traversal).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 349.1 ms | 0.56× |
| Rust `-O` | 523.4 ms | 0.84× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 528.1 ms | 0.85× |
| **Kāra (codegen)** | 619.7 ms | 1.00× |
| Go | 748.7 ms | 1.21× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   kth_smallest_bst.kara
karac build kth_smallest_bst.kara && ./kth_smallest_bst
python3 kth_smallest_bst.py
diff <(karac run kth_smallest_bst.kara) <(python3 kth_smallest_bst.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
