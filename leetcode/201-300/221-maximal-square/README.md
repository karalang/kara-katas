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

## Running

```bash
karac run   maximal_square.kara
karac build maximal_square.kara && ./maximal_square
python3 maximal_square.py
diff <(karac run maximal_square.kara) <(python3 maximal_square.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
