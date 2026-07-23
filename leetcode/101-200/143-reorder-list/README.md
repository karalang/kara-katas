# 143. Reorder List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reorder-list](https://leetcode.com/problems/reorder-list/)

Reorder `L0 → L1 → … → Ln-1 → Ln` into `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …` — interleave the list with its own reverse, in place.

```
[1,2,3,4]     ->  1 4 2 3
[1,2,3,4,5]   ->  1 5 2 4 3
[1]           ->  1
[1,2]         ->  1 2
```

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `1 ≤ Node.val ≤ 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **inward two-pointer + weak-next rewire** ★ | [`reorder_list.kara`](reorder_list.kara) ✓ | [`reorder_list.py`](reorder_list.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The reordered **index** sequence is `0, n-1, 1, n-2, 2, n-3, …` — two pointers `lo`/`hi` walking inward from both ends, alternately emitting the low then the high index until they cross. (This is equivalent to the textbook "find middle → reverse second half → merge alternately", collapsed to a single inward sweep since the nodes are randomly addressable.)

The Kāra version then **rewires the weak `next` chain** to follow that order (`nodes[order[i]].next = nodes[order[i+1]]`) and walks it from the head to emit the result — exercising both weak store (the rewire) and weak read (the traversal). As in [#141](../141-linked-list-cycle/)/[#142](../142-linked-list-cycle-ii/), nodes are `Vec`-owned (strong) with a `weak Node` overlay, so re-pointing the links — even into the interleaved order — stays leak-free.

## Kāra features exercised

- **Weak-next rewire + traversal** — indexed weak store to build the new chain, then `cur = c.next` weak reads (upgraded to `Option[Node]`) to walk it.
- **Inward two-pointer index order** with an alternating `not take_lo` toggle.
- **`String` join** of the emitted values for output.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`24750936645771`). Workload: in-place L0->Ln->L1->... reorder of a 100K-node index-pool list x 1000 perturbed passes; position-weighted checksum.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 420.2 ms | 0.97× |
| C `clang -O3` | 426.7 ms | 0.98× |
| **Kāra (codegen)** | 434.6 ms | 1.00× |
| Rust `-O` | 453.9 ms | 1.04× |
| Go | 512.3 ms | 1.18× |
| Python (scale lane) | 27.70 s | 63.74× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   reorder_list.kara
karac build reorder_list.kara && ./reorder_list
python3 reorder_list.py
diff <(karac run reorder_list.kara) <(python3 reorder_list.py) && echo OK
```

## Notes

The third `weak`-next kata in the #141/#142/#143 linked-list cluster. Where #141/#142 only *read* the weak links, #143 *rewrites* them into a new order — a fuller exercise of weak store + read together, verified leak-free.
