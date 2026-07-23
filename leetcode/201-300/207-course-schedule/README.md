# 207. Course Schedule

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Graph · Topological Sort · BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/course-schedule](https://leetcode.com/problems/course-schedule/)

There are `numCourses` courses labelled `0 .. numCourses`. A list of pairs `[a, b]` means **course `b` must be taken before course `a`**. Return `true` iff it is possible to finish all courses — i.e. the prerequisite graph contains no cycle.

```
2, [[1,0]]              ->  true    (take 0, then 1)
2, [[1,0],[0,1]]        ->  false   (0 and 1 depend on each other)
4, [[1,0],[2,0],[3,1],[3,2]]  ->  true   (a diamond)
3, [[0,1],[1,2],[2,0]]  ->  false   (a 3-cycle)
```

**Constraints:** `1 ≤ numCourses ≤ 2000`, `0 ≤ prerequisites.length ≤ 5000`, pairs are distinct.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Kahn's topological sort (BFS)** ★ | [`course_schedule.kara`](course_schedule.kara) | [`course_schedule.py`](course_schedule.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Each pair `[a, b]` becomes a directed edge `b → a`, and every node carries an **in-degree** — the number of prerequisites still blocking it. A course with in-degree 0 has nothing left to wait on, so it can be finished immediately. Kahn's algorithm seeds a queue with all in-degree-0 courses, then repeatedly finishes one and **relaxes** its out-edges: each neighbour's in-degree drops by one, and any that hit zero join the queue. A cycle is a knot whose nodes mutually block each other — none ever reaches in-degree 0 — so the count of finished courses ends up short of `numCourses`. Acyclic ⟺ every course finishes. O(V + E) time.

## Kāra features exercised

- **`Vec[Vec[i64]]` adjacency list** built by pushing onto an indexed element (`adj[b].push(a)`) — mutation of a nested-`Vec` slot in place.
- **`Vec[i64]` in-degree table** with compound index-assign (`indeg[a] = indeg[a] + 1`).
- **Index-pool FIFO** — a `Vec[i64]` plus a `head` cursor, the allocation-free queue idiom (enqueue = `push`, dequeue = read at `head`, advance).
- **`ref Vec[Vec[i64]]`** — the prerequisite graph is borrowed for reading; the caller keeps ownership.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`39968130`). Workload: Kahn topological sort over 8K passes on a 5000-node / 15000-edge CSR graph (BFS traversal kernel).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 392.7 ms | 0.64× |
| Go | 458.7 ms | 0.75× |
| Rust `-O` | 563.9 ms | 0.92× |
| **Kāra (codegen)** | 611.4 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 703.7 ms | 1.15× |
| Python (scale lane) | 21.09 s | 34.49× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   course_schedule.kara
karac build course_schedule.kara && ./course_schedule
python3 course_schedule.py
diff <(karac run course_schedule.kara) <(python3 course_schedule.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
