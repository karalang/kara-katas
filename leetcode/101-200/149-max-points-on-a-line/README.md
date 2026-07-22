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

> **Machine.** Container-only reference run so far — a shared **x86-64 Linux cloud container** ([`bench/results.container-x86.json`](bench/results.container-x86.json)); canonical Apple-M5 numbers (`bench/results.json`) are pending a maintainer run. Absolute times are noisy on the shared host; **within-run cross-language ratios are the signal.**

The `bench/` workload is a **map-free, sort-based** variant of the shipped kata (same anchor + normalized-slope algorithm, but each anchor's reduced-integer slope keys `dx*4096+dy` are collected into an array, **sorted**, and the longest equal run is counted) — chosen so C can mirror it with `qsort` and no hand-rolled hash map. `N = 1200` deterministic LCG points, `K = 8` outer iterations; all five mirrors print the same sink (`696`), and `bench.sh` fails loudly on mismatch.

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Two lanes: seq codegen, and the auto-par headline

Container snapshot, hyperfine `--warmup 5 --runs 30`:

| Lane | Run | Mean ± σ | vs kāra-seq |
|---|---|---|---|
| par | **kāra `max_points` (codegen, auto-par)** | **152.2 ± 8.9 ms** | **3.9× faster** |
| seq | rust `max_points` (`-O`) | 297.9 ± 5.4 ms | 1.98× ahead |
| seq | rust `max_points` (`overflow-checks=on`) | 302.9 ± 8.7 ms | 1.95× ahead |
| seq | **kāra `max_points` (codegen, `KARAC_AUTO_PAR=0`)** | **591.4 ± 6.2 ms** | — |
| seq | c `max_points` (`clang -O3`, `qsort`) | 649.6 ± 8.6 ms | kāra 1.10× ahead |
| seq | go `max_points` (`sort.Slice`) | 802.5 ± 11.7 ms | kāra 1.36× ahead |
| — | python `max_points` | 2385 ± 52 ms | (scale only) |

**Seq lane (single-threaded, fair).** Kāra's sequential codegen is ~2× behind `rust -O`, but **ahead of both C and Go**. The reason is the per-anchor sort: C's `qsort` and Go's `sort.Slice` call their comparator through a function pointer / closure (not inlined), a well-known indirect-call tax, while `rust`'s `sort_unstable` and Kāra's `Vec.sort()` inline the `i64` comparison. So Rust leads and Kāra lands between Rust and C.

**Auto-par lane (the headline).** The outer loop over anchors is embarrassingly parallel — each anchor's slope tally is independent — and the **default** `karac build` **auto-parallelizes it with zero source annotation**. That is a **3.9× wall-clock speedup** over Kāra's own seq lane, and it beats even single-threaded `rust -O` by **~1.95×** (and C by 4.3×, Go by 5.3×) on the container's 4 cores. Both Kāra lanes agree with all mirrors on the sink; correctness is verified across interp / JIT / AOT and `run == build == auto-par` (see below). This is the flagship auto-parallelization doing real work on an idiomatic O(n²) kernel — the same source, no `par` blocks, no threads written by hand.

## Running

```bash
karac run   max_points.kara
karac build max_points.kara && ./max_points
python3 max_points.py
diff <(karac run max_points.kara) <(python3 max_points.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. The `Map[String, i64]` get-then-insert on the same key compiled cleanly (no spurious move on the string key).
