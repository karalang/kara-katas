# 156. Binary Tree Upside Down

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Binary Tree · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-upside-down](https://leetcode.com/problems/binary-tree-upside-down/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given a binary tree where every right node is a leaf with a left sibling, flip it upside down: the original left-most node becomes the new root, each old parent becomes the **right** child of its old left child, and the old right sibling becomes the **left** child.

```
    1                4
   / \              / \
  2   3    -->     5   2
 / \                  / \
4   5                3   1
```
Pre-order serialization (`#` = null): `4 5 # # 2 3 # # 1 # #`.

**Constraints:** `0 ≤ n ≤ 10`; every right node is a leaf and has a left sibling.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **iterative left-spine rewire (weak-links)** ★ | [`upside_down.kara`](upside_down.kara) ✓ | [`upside_down.py`](upside_down.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Walk down the left spine, carrying `prev` (the node that becomes the current node's new right child) and `prev_right` (the old right sibling that becomes the new left child). At each node: remember `left` as the next step, set `left = prev_right`, save this node's `right` into `prev_right`, set `right = prev`, then advance. The last node on the spine is the new root.

The tree sibling of the #141–#160 linked-list cluster: nodes are `Vec`-owned (strong) with **`weak` left/right** overlays, so the rewiring only moves weak links — no ownership changes, freed exactly once. The flipped tree is then serialized pre-order (recursively, via weak reads) to a string oracle.

## Kāra features exercised

- **Dual `weak Node` fields** (`left`/`right`) rewired in place — `nodes[cur].left = nodes[target]` (weak-from-strong) and `= None`.
- **Forwarding a `mut ref` param** — `flip` passes its already-`mut ref` `nodes` to `set_left`/`set_right` **without** a call-site `mut` marker (the marker is only for fresh owned bindings; the compiler's `E0219` correctly rejected the redundant marker during authoring).
- **Recursive pre-order serialization** over weak links into a `mut ref String`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`463109432`). Workload: iterative flip of a 50000-node left-spine tree (index pool) x 1100 punched passes; per-pass link reset + pointer rewire + rolling-checksum fold of the result.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 380.3 ms | 0.80× |
| C `clang -O3` | 436.1 ms | 0.92× |
| Go | 441.4 ms | 0.93× |
| **Kāra (codegen)** | 473.5 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 510.2 ms | 1.08× |
| Python (scale lane) | 42.15 s | 89.01× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   upside_down.kara
karac build upside_down.kara && ./upside_down
python3 upside_down.py
diff <(karac run upside_down.kara) <(python3 upside_down.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
