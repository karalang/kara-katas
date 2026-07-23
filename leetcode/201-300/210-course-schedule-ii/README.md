# 210. Course Schedule II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Graph · Topological Sort · BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/course-schedule-ii](https://leetcode.com/problems/course-schedule-ii/)

Like [#207](../207-course-schedule/), but return an actual **order** in which all `numCourses` courses can be taken given the prerequisite pairs `[a, b]` ("course `b` before course `a`"). If the graph has a cycle, no order exists — return an empty result.

```
2, [[1,0]]                    ->  0 1
4, [[1,0],[2,0],[3,1],[3,2]]  ->  0 1 2 3
2, [[1,0],[0,1]]              ->  impossible   (cycle)
6, [[2,5],[0,5],[0,4],[1,4],[3,2],[1,3]]  ->  4 5 2 0 3 1
```

**Constraints:** `1 ≤ numCourses ≤ 2000`, `0 ≤ prerequisites.length ≤ numCourses·(numCourses-1)`, pairs distinct.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Kahn's topological sort (BFS)** ★ | [`course_schedule_ii.kara`](course_schedule_ii.kara) | [`course_schedule_ii.py`](course_schedule_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Identical machinery to #207 — edges `b → a`, per-node in-degrees, a FIFO seeded with the in-degree-0 courses — but here the **finish order is recorded**: each course is appended to the result the moment it is popped. Relaxing an out-edge drops a neighbour's in-degree and enqueues it when it hits zero. If every course is emitted, the sequence is a valid topological order; if a cycle starves the queue, fewer than `numCourses` come out and the answer is empty.

Many valid orders can exist. This solution pins a single deterministic one by seeding the queue in **ascending course label** and building adjacency in **pair order** — the Kāra and Python mirrors make the identical choices, so they emit the same order (e.g. `4 5 2 0 3 1` for the 6-course example). O(V + E).

## Kāra features exercised

- **`Vec[i64]` result built during traversal** — the order accumulates via `push` as courses are finished, then is returned by value (owned move out of the function).
- **`Vec[Vec[i64]]` adjacency** built by nested-element push (`adj[b].push(a)`), plus a `Vec[i64]` in-degree table with compound index-assign.
- **Index-pool FIFO** — `Vec[i64]` + `head` cursor, allocation-free.
- **String assembly for output** — the order is space-joined with a `first` flag (no trailing separator).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`400425564371`). Workload: build a 20k-node/80k-edge random DAG once (CSR); run Kahn topo-sort 800 times, punching one blocked course per pass; sink = sum of emitted count + order checksum.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Go | 481.9 ms | 0.83× |
| C `clang -O3` | 484.6 ms | 0.83× |
| Rust `-O` | 536.3 ms | 0.92× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 581.2 ms | 1.00× |
| **Kāra (codegen)** | 582.1 ms | 1.00× |
| Python (scale lane) | 19.98 s | 34.32× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   course_schedule_ii.kara
karac build course_schedule_ii.kara && ./course_schedule_ii
python3 course_schedule_ii.py
diff <(karac run course_schedule_ii.kara) <(python3 course_schedule_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
