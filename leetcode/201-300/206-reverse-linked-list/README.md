# 206. Reverse Linked List

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List · Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-linked-list](https://leetcode.com/problems/reverse-linked-list/)

Reverse a singly-linked list and return the new head.

```
[1,2,3,4,5]  ->  [5,4,3,2,1]
[1,2]        ->  [2,1]
[]           ->  []
```

**Constraints:** `0 ≤ nodes ≤ 5000`, `-5000 ≤ Node.val ≤ 5000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **iterative three-cursor** ★ | [`reverse_list.kara`](reverse_list.kara) | [`reverse_list.py`](reverse_list.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Keep three cursors: `prev` (the reversed portion built so far, initially empty), `cur` (the node being flipped), and a **saved `nxt`** so the forward link isn't lost when `cur.next` is rewired backwards. Each step: stash `nxt = cur.next`, point `cur.next` at `prev`, then slide all three forward (`prev = cur; cur = nxt`). When `cur` falls off the end, `prev` is the new head. O(n) time, O(1) extra space — the canonical linked-list warm-up.

## Kāra features exercised

- **Index-pool singly-linked list** — `Vec[Node]` with an `i64` `next` (`-1` = null). Reversal rewires `next` indices (`nodes[cur].next = prev`) — a struct-field index-assign, no allocation.
- **Three-cursor pointer dance** with the saved-`nxt` idiom, and `mut ref Vec[Node]` for the mutation vs `ref Vec[Node]` for the read-only traversal.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`10067210720000`). Workload: relink + in-place reverse + position-weighted walk over 40K passes on a 3000-node index-pool list (pointer-chase kernel).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-28 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 206.2 ms | 0.62× |
| Go | 227.1 ms | 0.69× |
| Rust `-O` | 252.8 ms | 0.76× |
| C `clang -O3` | 298.3 ms | 0.90× |
| **Kāra (codegen)** | 330.5 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   reverse_list.kara
karac build reverse_list.kara && ./reverse_list
python3 reverse_list.py
diff <(karac run reverse_list.kara) <(python3 reverse_list.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
