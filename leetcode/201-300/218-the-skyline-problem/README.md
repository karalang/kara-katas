# 218. The Skyline Problem

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Divide and Conquer · Sweep Line · Heap &nbsp;·&nbsp; **Source:** [leetcode.com/problems/the-skyline-problem](https://leetcode.com/problems/the-skyline-problem/)

Each building is a triple `[left, right, height]`. Return the **skyline** — the outer contour formed by all buildings — as the ordered list of **key points** `[x, h]` where the visible height changes. The last key point always drops to height `0`.

```
[[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
   ->  [2,10] [3,15] [7,12] [12,0] [15,10] [20,8] [24,0]
```

**Constraints:** `0 ≤ buildings ≤ 10⁴`, `0 ≤ left < right ≤ 2³¹−1`, `1 ≤ height ≤ 2³¹−1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **divide & conquer (contour merge)** ★ | [`skyline.kara`](skyline.kara) | [`skyline.py`](skyline.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The same shape as merge sort. A **single** building `[L, R, H]` has the trivial skyline `[[L, H], [R, 0]]`. Split the building list in half, compute each half's skyline recursively, then **merge** the two contours into one.

The merge sweeps both contours left to right, remembering the current height of each (`h1`, `h2`). At each x where either contour changes, the combined visible height is `max(h1, h2)`. A key point is emitted **only when that combined height differs from the last one emitted** — that single dedup rule handles every case: equal-height buildings meeting edge-to-edge collapse into one flat span, a taller building hides a shorter one's interior transitions, and redundant points never appear. When one contour is exhausted its trailing height is `0`, so the other's remaining points pass straight through. Each merge is linear and the recursion is log-deep: O(n log n).

Because every single-building skyline is already sorted by x and merge preserves that order, no separate sort of coordinates or events is needed.

## Kāra features exercised

- **Recursion returning an owned `Vec[Point]`** — each level builds and hands back a fresh contour; the merge borrows its two inputs as `ref Vec[Point]` and returns a new owned vector (struct-valued `Vec` ownership across recursion, valgrind-verified — no leak despite many intermediate contours).
- **Struct value types** — `Building` and `Point` are plain two/three-field `i64` structs copied by value out of borrowed vectors (`let b = bs[lo]`, `result.push(left[i])`).
- **`f"[{p.x},{p.h}]"` interpolation** with field access, and the `mut ref Vec[Building]` builder (`add(mut a, …)`) with the call-site `mut` marker.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`64666874995`). Workload: divide-and-conquer skyline over 24000 PRNG buildings, 100 build-once+punch re-runs; sum of x+h over all key points (allocation-heavy).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 509.9 ms | 0.61× |
| **Kāra (codegen)** | 835.6 ms | 1.00× |
| Go | 889.3 ms | 1.06× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 931.6 ms | 1.11× |
| Rust `-O` | 953.5 ms | 1.14× |
| Python (scale lane) | 15.00 s | 17.96× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   skyline.kara
karac build skyline.kara && ./skyline
python3 skyline.py
diff <(karac run skyline.kara) <(python3 skyline.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
