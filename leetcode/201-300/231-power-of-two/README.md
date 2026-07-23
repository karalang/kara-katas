# 231. Power of Two

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/power-of-two](https://leetcode.com/problems/power-of-two/)

Return `true` iff `n` is a power of two (`n == 2^x` for some `x ≥ 0`).

```
1  ->  true    (2^0)
16 ->  true
3  ->  false
0  ->  false
```

**Constraints:** `-2³¹ ≤ n ≤ 2³¹−1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **`n & (n-1)` bit trick** ★ | [`power_of_two.kara`](power_of_two.kara) | [`power_of_two.py`](power_of_two.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A positive power of two has exactly **one** set bit. Subtracting 1 flips that bit off and turns every lower bit on — `1000 → 0111` — so the two share no bits and `n & (n - 1) == 0`. Any other positive number has at least two set bits, and clearing the lowest one with `n & (n - 1)` leaves something non-zero. Non-positive `n` is never a power of two, so it's rejected up front. O(1), no loop.

## Kāra features exercised

- **Bitwise AND and subtraction on `i64`** — `n & (n - 1)`, the single-expression test, including the `2^31` / `2^30` cases well within `i64` range.
- **Guard-then-return** — the `n <= 0` early return keeps the bit test on the domain where it's meaningful.

## Running

```bash
karac run   power_of_two.kara
karac build power_of_two.kara && ./power_of_two
python3 power_of_two.py
diff <(karac run power_of_two.kara) <(python3 power_of_two.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
