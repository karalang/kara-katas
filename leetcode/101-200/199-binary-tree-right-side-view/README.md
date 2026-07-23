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

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`256749133`). Workload: level-order right-side-view BFS over an 8191-node complete index-pool tree x 40000 punched passes (per-level allocation churn + pointer-chasing; one node value flipped per pass).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 373.9 ms | 0.47× |
| Rust `-O` | 778.5 ms | 0.99× |
| **Kāra (codegen)** | 788.9 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 808.0 ms | 1.02× |
| Go | 4.09 s | 5.19× |
| Python (scale lane) | 18.06 s | 22.90× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   right_side_view.kara
karac build right_side_view.kara && ./right_side_view
python3 right_side_view.py
diff <(karac run right_side_view.kara) <(python3 right_side_view.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
