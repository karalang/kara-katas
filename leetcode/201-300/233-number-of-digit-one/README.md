# 233. Number of Digit One

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Math · Recursion / Digit Counting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/number-of-digit-one](https://leetcode.com/problems/number-of-digit-one/)

Count the total number of times the digit `1` appears across **all** non-negative integers from `0` to `n`.

```
n=13   ->  6     (1, 10, 11, 12, 13 contribute 1+1+2+1+1)
n=0    ->  0
n=100  ->  21
```

**Constraints:** `0 ≤ n ≤ 10⁹`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **per-position counting** ★ | [`number_of_digit_one.kara`](number_of_digit_one.kara) | [`number_of_digit_one.py`](number_of_digit_one.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Enumerating every number is O(n); counting per **digit position** is O(log n). For each place value `pos` (1, 10, 100, …), split `n` into the digits above, at, and below that position:

```
high = n / (pos*10)     cur = (n / pos) % 10     low = n % pos
```

Then the number of `1`s contributed *at this position* over `0..n` is:

- `cur == 0` → `high * pos` — only the fully-completed high cycles put a 1 here;
- `cur == 1` → `high * pos + low + 1` — plus one partial cycle covering `0..low`;
- `cur ≥ 2` → `(high + 1) * pos` — this digit's whole block of 1s is fully covered.

Summing that over every position gives the answer. Place values climb by `×10` until they exceed `n`; `pos*10` reaches at most 10¹⁰, comfortably inside `i64`, so Kāra's overflow-checked arithmetic never trips.

## Kāra features exercised

- **Pure integer digit arithmetic** — `/`, `%`, and a climbing `pos` power of ten, all overflow-checked `i64`; the three-way `cur` branch is the whole kernel.
- **O(log n) loop** — one iteration per decimal position rather than per integer.

## Running

```bash
karac run   number_of_digit_one.kara
karac build number_of_digit_one.kara && ./number_of_digit_one
python3 number_of_digit_one.py
diff <(karac run number_of_digit_one.kara) <(python3 number_of_digit_one.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
