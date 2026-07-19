# 130. Surrounded Regions

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** DFS · BFS · Union Find · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/surrounded-regions](https://leetcode.com/problems/surrounded-regions/)

Given an `m × n` board of `'X'` and `'O'`, capture every region of `'O'`s **fully surrounded** by `'X'` (flip it to `'X'`). An `'O'` region touching the border is never captured.

```
X X X X        X X X X
X O O X   ->   X X X X      (the interior O-region is surrounded -> captured)
X O X X        X X X X
X X X O        X X X O      (the border O survives)
```

**Constraints:** `1 ≤ m, n ≤ 200`, cells are `'X'`/`'O'`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Border flood-fill + sweep** ★ | O(m·n) | [`surrounded_regions.kara`](surrounded_regions.kara) ✓ | [`surrounded_regions.py`](surrounded_regions.py) ✓ |

`✓` runs end-to-end today: interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`) all agree with the Python mirror. Verified on a hand case plus deterministic-LCG boards; the final grid is compared by a rolling hash. Zero diagnostics, valgrind-clean.

## The mechanism

The safe cells are exactly those reachable from a **border** `'O'`. So flood-fill from every border `'O'`, marking its whole component **safe** (a third state, `2`); then one sweep resolves the grid — `safe → 'O'`, any surviving `'O' → 'X'`. Grid is `Vec[Vec[i64]]` with `0='X'`, `1='O'`; the flood-fill uses an explicit **position stack** (`Vec[i64]`, `pos = r·cols + c`) rather than recursion, so a 200×200 board can't blow the call stack. O(m·n): each cell is marked safe at most once.

## Kāra features exercised

- **`Vec[Vec[i64]]` grid with 2-D index-assign** — `board[r][c] = 2` in-place mutation through a `mut ref Vec[Vec[i64]]` parameter; the compiler resolves the nested index-store across all surfaces.
- **Call-site `mut` marker** — `solve(mut g, …)`: a fresh owned grid passed to a `mut ref` parameter takes the marker; the in-scope `mut ref` then forwards to `flood(board, …)` without one (Feature 4 call-site-marker rule).
- **Iterative flood-fill on an integer position stack** — `Vec[i64]` `push`/`pop().unwrap()`, positions packed as `r·cols + c`.

## Running

```bash
karac run   surrounded_regions.kara
karac build surrounded_regions.kara && ./surrounded_regions
python3 surrounded_regions.py
diff <(karac run surrounded_regions.kara) <(python3 surrounded_regions.py) && echo OK
```

## Notes

Dogfood-first grid-mutation kata: it exercises `Vec[Vec[i64]]` 2-D index-assign through a borrow parameter — a distinct surface from the pointer-tree and string katas — and confirms it is codegen-correct and leak-clean on every surface.
