# 160. Intersection of Two Linked Lists

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers · Weak References &nbsp;·&nbsp; **Source:** [leetcode.com/problems/intersection-of-two-linked-lists](https://leetcode.com/problems/intersection-of-two-linked-lists/)

Two singly linked lists may share a common **suffix**; return the first shared node (or none).

```
A: 4 → 1 ↘
          8 → 4 → 5      ->  intersection at 8
B: 5 → 6 → 1 ↗

A: 2 → 3
B: 1 → 4 → 5             ->  no intersection
```

**Constraints:** `1 ≤ m, n ≤ 3·10⁴`, `1 ≤ Node.val ≤ 10⁵`; the lists either share a suffix or are fully disjoint (no cycles).

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two-pointer length alignment (weak-next)** ★ | [`intersection.kara`](intersection.kara) ✓ | [`intersection.py`](intersection.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The sixth `weak`-next kata in the #141/#142/#143/#147/#148 linked-list cluster. Nodes are `Vec`-owned (strong) with a `weak Node` next overlay; a **shared suffix is just two `next` chains that converge on the same node id** — the pool owns each node once, and both lists' `next` links point at the shared nodes (weak, so no double-ownership).

Align by length: walk each list to its length, advance the longer head by the difference so both are equidistant from the (possible) join, then step both together — the first id where the two pointers coincide is the intersection. Because the tail is physically shared, equality is a plain **id** comparison, no value matching.

## Kāra features exercised

- **Weak-next traversal** — `match nodes[i].next { Some(nx) => nx.id, None => -1 }` (`next_idx`) walks each chain; a shared node is reached from both heads and freed exactly once (the pool's single strong owner), verified leak-free.
- **`ref Vec[Node]` read-only helpers** (`length`, `advance`, `intersection`) over the shared pool.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`13990577`). Workload: two-pointer intersection-find over a 100003-node scrambled (coprime-stride) chain, two suffix lists per pass x 280 passes; cache-hostile pointer-chase walks.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| **Kāra (codegen)** | 428.9 ms | 1.00× |
| C `clang -O3` | 433.9 ms | 1.01× |
| Go | 459.5 ms | 1.07× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 478.4 ms | 1.12× |
| Rust `-O` | 504.8 ms | 1.18× |
| Python (scale lane) | 2.69 s | 6.26× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   intersection.kara
karac build intersection.kara && ./intersection
python3 intersection.py
diff <(karac run intersection.kara) <(python3 intersection.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. A convergence (shared-suffix) structure over the weak-next model; the pool's single-ownership + weak links free the shared tail exactly once. Oracle-only.
