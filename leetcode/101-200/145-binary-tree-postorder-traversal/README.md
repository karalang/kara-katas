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

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **47%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **2.8%** margin against `go build` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`6827796872623535`). Workload: iterative postorder (two explicit index-pool stacks) over a 50k-node BST x 250 passes, pointer-chase.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 45.4 ms | 0.96× |
| **Kāra (codegen)** | 47.3 ms | 1.00× |
| Go | 48.7 ms | 1.03× |
| Rust `-O` | 70.0 ms | 1.48× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 73.2 ms | 1.55× |

Against the previous run (2026-07-28, karac 0.1.0, legacy backend), Kāra's ratio moved from 1.03× to 0.68× `rustc -O`, 1.58× to 1.04× C, and 1.73× to 0.97× Go: now ahead of Rust and Go and level with C. The Rust lead (Rust takes 1.48× Kāra's time) is about the size of this kata's 47% placement spread, so treat it as provisional too.

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   postorder.kara
karac build postorder.kara && ./postorder
python3 postorder.py
diff <(karac run postorder.kara) <(python3 postorder.py) && echo OK
```

## Notes

The postorder sibling of [#144](../144-binary-tree-preorder-traversal/) — identical structure, only the visit-vs-recurse order differs. Clean pass, no compiler friction.
