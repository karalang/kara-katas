# 85. Maximal Rectangle

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Stack · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximal-rectangle](https://leetcode.com/problems/maximal-rectangle/)

Given a binary matrix, find the largest rectangle containing only `1`s and return its area.

```
[[1,0,1,0,0],
 [1,0,1,1,1],
 [1,1,1,1,1],     ->  6
 [1,0,0,1,0]]

[[0]] -> 0    [[1]] -> 1    [[1,1],[1,1]] -> 4
```

**Constraints:** `1 ≤ rows, cols ≤ 200`; each cell is `0` or `1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **row histograms + monotonic stack** ★ | [`maximal_rectangle.kara`](maximal_rectangle.kara) ✓ | [`maximal_rectangle.py`](maximal_rectangle.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Reduce the 2-D problem to a series of 1-D ones. Scan the rows top to bottom, maintaining `heights[c]` = the number of consecutive `1`s ending at the current row in column `c` (reset to `0` on a `0`). Each row's `heights` is a histogram, and the maximal all-`1`s rectangle whose bottom edge lies on that row is exactly the **largest rectangle in that histogram**.

The histogram pass is O(cols) with a **monotonic stack** of column indices with strictly increasing heights. When a shorter bar arrives (or the sentinel `0` past the end), pop each taller bar and settle its widest rectangle: the popped bar's height times the span between the new stack top (exclusive) and the current index (exclusive). The global maximum over all rows is the answer — O(R·C) overall.

## Kāra features exercised

- **`Vec[Vec[i64]]` matrix** with `matrix[r][c]` double indexing.
- **Monotonic `Vec[i64]` stack** with `push`/`pop` and **nested index reads** `heights[stack[stack.len()-1]]` (an index expression used as an index) in the pop-condition and width computation.
- **`if`-expressions** for the sentinel height and the stack-empty width branch.

## Running

```bash
karac run   maximal_rectangle.kara
karac build maximal_rectangle.kara && ./maximal_rectangle
python3 maximal_rectangle.py
diff <(karac run maximal_rectangle.kara) <(python3 maximal_rectangle.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. The nested-index reads (`heights[stack[...]]`) and `Vec[Vec[i64]]` double indexing compiled cleanly. Oracle-only.
