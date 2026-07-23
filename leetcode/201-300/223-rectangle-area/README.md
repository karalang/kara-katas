# 223. Rectangle Area

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math · Geometry &nbsp;·&nbsp; **Source:** [leetcode.com/problems/rectangle-area](https://leetcode.com/problems/rectangle-area/)

Two axis-aligned rectangles are given by their bottom-left and top-right corners — `A = (ax1, ay1, ax2, ay2)` and `B = (bx1, by1, bx2, by2)`. Return the **total area** the two cover together (their union).

```
A=(-3,0,3,4), B=(0,-1,9,2)   ->  45   (areas 24 + 27, overlap 6)
A=(0,0,1,1),  B=(1,1,2,2)    ->  2    (touch at a corner — no overlap)
```

**Constraints:** `-10⁴ ≤ all coordinates ≤ 10⁴`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **inclusion–exclusion** ★ | [`rectangle_area.kara`](rectangle_area.kara) | [`rectangle_area.py`](rectangle_area.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The union area is `area(A) + area(B) − area(A ∩ B)` — add both rectangles, then subtract the part counted twice. The intersection is itself a rectangle: its x-span runs from `max(ax1, bx1)` to `min(ax2, bx2)`, its y-span from `max(ay1, by1)` to `min(ay2, by2)`. If either span comes out non-positive the rectangles don't actually overlap, so **clamping each span at 0** before multiplying makes the disjoint and edge-touching cases produce a 0 overlap with no special-casing. O(1).

## Kāra features exercised

- **Pure integer arithmetic with `min`/`max`/clamp helpers** — the overlap spans fold through small `min_i64` / `max_i64` / `clamp0` functions; overflow-checked `i64` throughout (areas up to ~4·10⁸ stay well within range).
- **Multi-argument signatures** — eight `i64` coordinates threaded through `compute_area` / `report`, no collections involved.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`451466294`). Workload: union area of ~1e8 PRNG rectangle pairs via inclusion-exclusion (scalar ALU, min/max/clamp branches).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 217.0 ms | 0.92× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 220.6 ms | 0.94× |
| C `clang -O3` | 227.8 ms | 0.97× |
| **Kāra (codegen)** | 235.0 ms | 1.00× |
| Go | 294.4 ms | 1.25× |
| Python (scale lane) | 43.31 s | 184.32× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   rectangle_area.kara
karac build rectangle_area.kara && ./rectangle_area
python3 rectangle_area.py
diff <(karac run rectangle_area.kara) <(python3 rectangle_area.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
