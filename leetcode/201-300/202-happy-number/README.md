# 202. Happy Number

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table · Math · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/happy-number](https://leetcode.com/problems/happy-number/)

Repeatedly replace `n` by the sum of the squares of its digits. `n` is **happy** if this eventually reaches `1`.

```
19 -> true   (1²+9²=82 → 68 → 100 → 1)
2  -> false
7  -> true
```

**Constraints:** `1 ≤ n ≤ 2³¹-1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Floyd cycle detection** ★ | [`happy_number.kara`](happy_number.kara) | [`happy_number.py`](happy_number.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The digit-square-sum map is a function, so iterating it either reaches `1` or enters a repeating **cycle**. That's the exact setup for **Floyd's tortoise-and-hare**: advance `slow` one step and `fast` two steps. If `fast` reaches `1`, the number is happy; if the two pointers meet first, there's a cycle that doesn't contain `1`, so it isn't. No visited-set needed — **O(1) extra space** (the alternative is a `Map`/`Set` of seen values).

## Kāra features exercised

- **Digit decomposition** — `x % 10` / `x / 10` with `d*d` accumulation, under Kāra's checked arithmetic (the squared-digit sum stays tiny, so no overflow concern).
- **Two-pointer cycle detection** — `fast = sq_digit_sum(sq_digit_sum(fast))` (double step) vs `slow` single step, terminating on `fast == 1` or `slow == fast`.

## Running

```bash
karac run   happy_number.kara
karac build happy_number.kara && ./happy_number
python3 happy_number.py
diff <(karac run happy_number.kara) <(python3 happy_number.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
