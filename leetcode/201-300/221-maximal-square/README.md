# 221. Maximal Square

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximal-square](https://leetcode.com/problems/maximal-square/)

Given a binary grid of `0`/`1`, find the largest axis-aligned square containing only `1`s and return its **area**.

```
[[1,0,1,0,0],
 [1,0,1,1,1],
 [1,1,1,1,1],   ->  4    (a 2x2 square of 1s)
 [1,0,0,1,0]]
```

**Constraints:** `1 ≤ rows, cols ≤ 300`, each cell is `0` or `1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **bottom-right corner DP** ★ | [`maximal_square.kara`](maximal_square.kara) | [`maximal_square.py`](maximal_square.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Let `dp[i][j]` be the side length of the largest all-ones square whose **bottom-right corner** is cell `(i, j)`. A `0` cell ends no square, so `dp = 0`. A `1` cell extends the squares ending just above, just left, and diagonally up-left — but a bigger square needs **all three** neighbours to support it, so it can only grow as far as the smallest of them: `dp[i][j] = 1 + min(top, left, diag)`. Cells in the first row or column can only ever be a 1×1 square. Track the largest side encountered; the area is its square. O(rows·cols) time.

## Kāra features exercised

- **`Vec.filled(rows, Vec.filled(cols, 0))`** — a runtime-sized `Vec[Vec[i64]]` DP table whose rows are independent copies (value semantics), the book's grid idiom.
- **Nested index read and assign** — `dp[i][j] = …` writes a cell; `dp[i-1][j]` / `dp[i][j-1]` / `dp[i-1][j-1]` read the three neighbours (`grid` borrowed as `ref Vec[Vec[i64]]`).
- **`min3` + running max** — the recurrence folded through a small helper, overflow-checked `i64` throughout.

## Benchmarks

The kata's tiny fixed grids aren't a workload, so [`bench/`](bench/) carries a
scaled compute variant: an 800×800 0/1 grid built once with a deterministic
LCG, then the **space-optimized 1-D DP** run over it 150 times (a single-cell
flip before each pass defeats hoisting — build-once + punch). The 1-D DP's
`cur[j] → cur[j-1]` left dependency is loop-carried, so it does **not**
vectorize — a genuine scalar compute + streaming-memory kernel, not a
SIMD-erased one. All five implementations share the identical algorithm and PRNG
and agree on the sink (`600`).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-02, karac g6697158fa (0.9.0-dev.14057, the v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 195.1 ± 2.0 ms | 0.85× |
| Rust `-O` | 196.3 ± 1.6 ms | 0.85× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 203.5 ± 1.8 ms | 0.89× |
| **Kāra (codegen)** | **229.9 ± 2.9 ms** | **1.00×** |
| Go | 298.6 ± 2.5 ms | 1.30× |
| Python (scale lane) | 9 896 ms | last measured on the x86 container (undated snapshot), not re-run |

**Equal-safety framing:** Kāra checks integer overflow by default, so the honest
comparison is against `rustc -O -C overflow-checks=on` (203.5 ms) — Kāra is
**1.13×** behind it on this scalar DP, 1.17× behind `rustc -O`, 1.18× behind C,
and ahead of Go (0.77× of Go's time).

Against the 2026-07-27 M5 run (karac 0.1.0, legacy backend) the ranking is
unchanged and the language ratios are flat: Kāra/Rust `-O` 1.21× → 1.17×,
Kāra/equal-safety Rust 1.16× → 1.13×, Kāra/C 1.22× → 1.18×, Kāra/Go 0.79× →
0.77×. Every comparator also ran ~11% slower this session (machine state), so
compare the ratios, not the milliseconds.

Binary size: C 33,616 B · **Kāra 302,880 B** · Rust 466,336 B · Go 2,492,530 B.
Every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

> **History.** An earlier, undated x86 container snapshot put Kāra at 451.6 ms,
> within ~13% of `rust_ovf` (399.7 ms), ~7% behind C (423.4 ms), ahead of Go
> (592.4 ms) and ~22× faster than CPython (9 896 ms). The container feed
> ([`bench/results.container-x86.json`](bench/results.container-x86.json)) has
> since been re-measured (2026-10-30); neither is the M5 result above.

Numbers are a single-machine snapshot (`bench/results.json`, karac g6697158fa); see
[`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with
`bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   maximal_square.kara
karac build maximal_square.kara && ./maximal_square
python3 maximal_square.py
diff <(karac run maximal_square.kara) <(python3 maximal_square.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
