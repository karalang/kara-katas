# 149. Max Points on a Line

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Hash Map · Math · Geometry &nbsp;·&nbsp; **Source:** [leetcode.com/problems/max-points-on-a-line](https://leetcode.com/problems/max-points-on-a-line/)

Given points on a plane, return the maximum number that lie on the same straight line.

```
[[1,1],[2,2],[3,3]]                          ->  3
[[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]        ->  4
[[0,0]]                                       ->  1
[[0,0],[1,1]]                                 ->  2
[[1,1],[1,1],[2,2]]        (duplicate anchor) ->  3
[[1,1],[1,2],[1,3],[2,1]]  (vertical + off)   ->  3
```

**Constraints:** `1 ≤ n ≤ 300`, `-10⁴ ≤ xᵢ, yᵢ ≤ 10⁴`, all points distinct in the base problem (this kata also handles coincident points).

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **anchor + exact-slope Map count** ★ | [`max_points.kara`](max_points.kara) ✓ | [`max_points.py`](max_points.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

O(n²): **anchor** each point `i`, then for every later point `j` classify the line `i→j` by its slope and count how many `j` share it. The largest bucket + the anchor + any coincident duplicates is a candidate; the max over all anchors is the answer.

Slopes are kept **exact** — no floating point, no precision loss. The direction `(dx, dy)` is reduced by `g = gcd(|dx|, |dy|)` and **sign-normalized** so that `(dx, dy)` and `(−dx, −dy)` collapse to one key (force `dx > 0`, or `dy > 0` on a vertical line where `dx == 0`). The reduced pair becomes a `"dx/dy"` string key in a `Map[String, i64]`, and a running `local` max avoids a second pass over the map.

## Kāra features exercised

- **`Map[String, i64]`** — `match slopes.get(key) { Some(v) => v, None => 0 }` for get-or-default, then `slopes.insert(key, c + 1)` (the key is read then re-inserted in the same iteration).
- **Integer-exact geometry** — `gcd` (Euclid), `abs_i64`, sign normalization; overflow-checked `i64` arithmetic throughout.
- **`Vec[Point]`** of a plain (Copy-ish) struct, indexed field reads `pts[j].x` / `pts[i].y` in the hot double loop.


## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`696`). Workload: sort-based slope-run count, N=1200 K=8.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 121.9 ms | 0.93× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 124.7 ms | 0.96× |
| **Kāra (codegen)** | 130.5 ms | 1.00× |
| C `clang -O3` | 246.4 ms | 1.89× |
| Go | 321.2 ms | 2.46× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Kāra is 1.05× equal-safety Rust (1.07× `rustc -O`) and ahead of C (0.53×) and Go (0.41×) — flat against the 2026-07-28 measurement in ratio terms.

**Auto-par lane (Kāra only).** The default build auto-parallelises the anchor loop (the par binary's emitted IR (`KARAC_MIR_LL`) carries a call of `karac_mir_task_spawn`; the `KARAC_AUTO_PAR=0` twin's does not). It runs in 20.5 ms ± 0.2 ms, 6.36× faster than Kāra's own seq lane. No comparator has a parallel version, so this row is not part of the cross-language comparison above.

Single-machine snapshot (`bench/results.json`, karac g6697158fa, 2026-11-01); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   max_points.kara
karac build max_points.kara && ./max_points
python3 max_points.py
diff <(karac run max_points.kara) <(python3 max_points.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. The `Map[String, i64]` get-then-insert on the same key compiled cleanly (no spurious move on the string key).
