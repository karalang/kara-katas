# 200. Number of Islands

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Depth-First Search · Breadth-First Search · Union Find · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/number-of-islands](https://leetcode.com/problems/number-of-islands/)

Count the islands in a grid of land (`1`) and water (`0`), where land cells connect **4-directionally**.

```
[[1,1,0,0,0],
 [1,1,0,0,0],
 [0,0,1,0,0],   ->  3
 [0,0,0,1,1]]
```

**Constraints:** `1 ≤ m, n ≤ 300`, each cell is `0` or `1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **iterative flood fill** ★ | [`number_of_islands.kara`](number_of_islands.kara) | [`number_of_islands.py`](number_of_islands.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Scan the grid. Each time an **unvisited land cell** is found, it must belong to a *new* island, so bump the count and then **flood-fill** the whole connected component to `0` (sinking it) so its other cells aren't recounted. The fill is **iterative** — an explicit stack of encoded `row*cols + col` positions — rather than recursive, so a single large island (up to 300×300 cells) can't overflow the call stack. Each cell is pushed and sunk at most once, so the whole scan is O(m·n).

## Kāra features exercised

- **Mutable `Vec[Vec[i64]]` grid** — the fill marks visited cells via **nested index-assign** `grid[cr-1][cc] = 0` (the compound-index-assign path on a heap-of-heaps); verified valgrind-clean.
- **`Vec[i64]` explicit stack** — `push` / peek / `pop` (→ `Option`, discarded) driving iterative DFS; positions packed as `r*cols + c` and unpacked with `/` and `%`.
- **`mut ref Vec[Vec[i64]]` parameter** — the grid is consumed by value in `report` (`let mut g = grid`) then passed with the `mut` marker to the mutating `num_islands`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`6469639`). Workload: iterative stack flood-fill island count over an 80x80 PRNG 0/1 grid x 13000 passes, grid restored from a persistently-punched master each pass (data-dependent stack growth, non-vectorizing).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 423.4 ms | 0.50× |
| **Kāra (codegen)** | 850.6 ms | 1.00× |
| Rust `-O` | 866.0 ms | 1.02× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 891.6 ms | 1.05× |
| Go | 1.33 s | 1.57× |
| Python (scale lane) | 28.58 s | 33.61× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   number_of_islands.kara
karac build number_of_islands.kara && ./number_of_islands
python3 number_of_islands.py
diff <(karac run number_of_islands.kara) <(python3 number_of_islands.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
