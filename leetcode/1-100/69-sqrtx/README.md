# 69. Sqrt(x)

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/sqrtx](https://leetcode.com/problems/sqrtx/)

Return **⌊√x⌋** — the integer part of the square root of a non-negative integer `x` — computed **without** any floating point or a built-in `sqrt`.

```
x = 4   →  2      exact
x = 8   →  2      ⌊2.828…⌋ = 2   (LeetCode example)
x = 2147483647 → 46340         i32 max, just below 46341² = 2147488281
```

**Constraints:** `0 ≤ x ≤ 2³¹ − 1` (2,147,483,647).

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Binary search** ★ — largest `r` with `r*r ≤ x`, on the monotone predicate | O(log x) | [`sqrtx.kara`](sqrtx.kara) ✓ via `karac run` / `karac build` | [`sqrtx.py`](sqrtx.py) ✓ |
| **Newton's method** — integer `r ← (r + x/r) / 2` until it stops shrinking | O(log log x) iters | [`sqrtx_newton.kara`](sqrtx_newton.kara) ✓ | — |
| **Bit-by-bit** — long-division √ over powers of four; **no multiplication** | O(log x), shift/add only | [`sqrtx_bits.kara`](sqrtx_bits.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all twenty-seven test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## Three routes to the floor

The answer is defined by a monotone predicate — `r*r ≤ x` is true for every `r` up to ⌊√x⌋ and false after — so this is a search for a boundary, and the three solvers are three ways to reach it.

**Binary search** ([`sqrtx.kara`](sqrtx.kara)) is the ★: it reads "largest `r` with `r*r ≤ x`" directly. Halve the interval each step, keep the best `r` whose square fits, and it lands on the floor in ~31 steps for x near 2³¹. It is the same monotone-predicate search template as katas [#35](../35-search-insert-position/) and [#34](../34-find-first-and-last-position/), specialised to the predicate `mid*mid ≤ x`, with `lo + (hi - lo) / 2` avoiding a `lo + hi` overflow.

**Newton's method** ([`sqrtx_newton.kara`](sqrtx_newton.kara)) converges far faster — a handful of steps even at 2³¹. Starting from an overestimate `r = x`, the truncating average `r ← (r + x/r) / 2` monotonically descends to exactly ⌊√x⌋; integer `/` rounding toward zero is precisely what makes it settle on the floor instead of oscillating. `x = 0` is special-cased to avoid the `x / r` division by zero.

**Bit-by-bit** ([`sqrtx_bits.kara`](sqrtx_bits.kara)) is the outlier: it builds the result one binary digit at a time, high to low, using only shifts, adds, and compares — **never a multiplication**. A probe walks down the powers of four (`4ᵏ = (2ᵏ)²`); at each, `res + bit` is the candidate square of "the answer so far with this bit set," accepted (subtract, set the bit, `res = res/2 + bit`) iff the remainder still covers it, else rejected (`res = res/2`). The `res/2` rescales the partial root as the place value drops ×4. It is the method a fixed-point or no-multiplier context reaches for.

## The overflow angle — where Kāra's checks matter

The natural predicate is `mid*mid ≤ x`, and `mid` ranges up to ~`x ≤ 2.1·10⁹` — so `mid*mid` overflows a **32-bit** integer. In C/Java the usual fixes are to compute the product in a wider type or to rewrite it as the division `mid ≤ x / mid` to dodge the overflow. **Kāra checks integer overflow by default**, so a 32-bit `mid*mid` would *trap* rather than silently wrap — surfacing the bug instead of hiding it. Computing in **i64** keeps the honest `mid*mid ≤ x` comparison (largest product on the path ≈ 4.6·10¹⁸ < i64::MAX ≈ 9.2·10¹⁸) with no division-based rewrite. The bit-by-bit method sidesteps the question entirely — it has no product term at all.

## Kāra features exercised

- **`i64` binary search with an overflow-safe midpoint** — `lo + (hi - lo) / 2` and the monotone `mid*mid <= x` predicate, the search template shared with katas [#35](../35-search-insert-position/)/[#34](../34-find-first-and-last-position/), here in i64 so the squaring test never trips Kāra's default overflow trap.
- **Integer Newton iteration** — `r = (r + x / r) / 2` with truncating `/`, plus the `x == 0` guard and a mid-function `return`; the convergence-loop idiom.
- **Pure shift/add bit-twiddling** — the bit-by-bit solver's `bit / 4` power-of-four walk and `res / 2` rescale (all `/` by constant powers of two, i.e. shifts), a multiplication-free numeric kernel — a distinct codegen surface from the squaring solvers.
- **Scalar `report`/`sums:` harness** — one `sqrt(x) = r` per line plus the folded `sums:` checksum, the byte-for-byte diff anchor shared with the numeric katas [#50](../50-powx-n/) and [#29](../29-divide-two-integers/); all three solvers and the Python mirror print it identically.

**v1 note.** All arithmetic is i64. The binary-search and Newton solvers rely on i64 headroom for `mid*mid` / `r*r` (≤ ~4.6·10¹⁸ at x = 2³¹) staying under i64::MAX; the bit-by-bit solver has no product and stays trivially in range. Newton special-cases `x == 0` (its loop would divide by `r = 0`); binary search and bit-by-bit handle 0 with no special case (the search collapses to `ans = 0`, the probe loop leaves `res = 0`).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   sqrtx.kara
karac build sqrtx.kara && ./sqrtx

# The alternative approaches (identical output):
karac run sqrtx_newton.kara
karac run sqrtx_bits.kara

# Python
python3 sqrtx.py

# Verify they all agree
diff <(karac run sqrtx.kara) <(python3 sqrtx.py)         && echo OK
diff <(karac run sqrtx.kara) <(karac run sqrtx_newton.kara) && echo OK
diff <(karac run sqrtx.kara) <(karac run sqrtx_bits.kara)   && echo OK
```
