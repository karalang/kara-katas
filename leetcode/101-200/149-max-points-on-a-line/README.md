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

## Running

```bash
karac run   max_points.kara
karac build max_points.kara && ./max_points
python3 max_points.py
diff <(karac run max_points.kara) <(python3 max_points.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. The `Map[String, i64]` get-then-insert on the same key compiled cleanly (no spurious move on the string key).
