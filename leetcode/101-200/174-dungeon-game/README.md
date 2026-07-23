# 174. Dungeon Game

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/dungeon-game](https://leetcode.com/problems/dungeon-game/)

A knight starts top-left and must reach the princess bottom-right, moving only **right** or **down**. Each cell adds to (or drains) his health; if health ever hits 0 he dies. Return the **minimum initial health** that lets him survive some path.

```
[[-2,-3, 3],
 [-5,-10,1],
 [10,30,-5]]   ->  7
```

**Constraints:** `1 ≤ m, n ≤ 200`, `-1000 ≤ dungeon[i][j] ≤ 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **backward 2D DP** ★ | [`dungeon_game.kara`](dungeon_game.kara) | [`dungeon_game.py`](dungeon_game.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Forward DP fails: the best cell to occupy depends on both current health *and* future needs, which don't separate. Working **backwards** fixes it. Define `dp[i][j]` = the minimum health needed **on entering** cell `(i,j)` to survive to the end. From `(i,j)` the knight takes the cheaper exit, so `dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j])` — the `max(1, …)` enforces that health must stay strictly positive. Fill from the bottom-right corner outward; the answer is `dp[0][0]`. O(m·n) time and space.

## Kāra features exercised

- **`Vec[Vec[i64]]` grid** — built from nested vector literals for the input, and a fresh `m×n` `dp` grid grown with a `push` loop.
- **Nested index-assign** — `dp[i][j] = need` writes a scalar into an inner `Vec[i64]` of an outer `Vec[Vec[i64]]` (the compound-index-assign path); verified valgrind-clean.
- **Backward-iterating `while` loops** (`i = m-1 … 0`) with `max`/`min` helpers lowering to branchless selects.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`5417974`). Workload: build a 200x200 signed PRNG dungeon once, then 2000 backward min-health DP passes with a per-pass cell sign-flip punch; sink=sum of dp[0][0] over passes.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 167.5 ms | 0.76× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 174.8 ms | 0.79× |
| **Kāra (codegen)** | 220.2 ms | 1.00× |
| Go | 238.9 ms | 1.09× |
| C `clang -O3` | 313.6 ms | 1.42× |
| Python (scale lane) | 37.47 s | 170.21× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   dungeon_game.kara
karac build dungeon_game.kara && ./dungeon_game
python3 dungeon_game.py
diff <(karac run dungeon_game.kara) <(python3 dungeon_game.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
