# 155. Min Stack

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Stack · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/min-stack](https://leetcode.com/problems/min-stack/)

Design a stack supporting **push, pop, top, and getMin all in O(1)**.

```
push(-2); push(0); push(-3);
getMin() -> -3
pop();
top()    -> 0
getMin() -> -2
```

**Constraints:** `-2³¹ ≤ val ≤ 2³¹-1`; `pop`, `top`, `getMin` are only called on a non-empty stack; up to `3·10⁴` calls.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **parallel running-min stack** ★ | [`min_stack.kara`](min_stack.kara) ✓ | [`min_stack.py`](min_stack.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Keep two stacks. `data` holds the values; `mins` is a parallel stack whose top is always the **minimum of everything at or below it**. On `push(x)`, push `x` onto `data` and `min(x, mins.last())` onto `mins`; on `pop`, discard both tops together. Then `getMin` is just `mins.last()` — O(1), no scan. Because the two stacks move in lockstep, popping never leaves `mins` stale.

Modelled in the corpus's method-free style: a plain `struct MinStack { data, mins }` plus free functions `ms_push` / `ms_pop` / `ms_top` / `ms_get_min` taking `mut ref` / `ref MinStack` (the same shape as [#146](../146-lru-cache/)'s pool functions).

## Kāra features exercised

- **`mut ref` struct receiver** — `ms_push(mut st, x)` mutates both `Vec[i64]` fields through a borrowed struct; `ref MinStack` for the read-only `top` / `get_min`.
- **Call-site `mut` markers** on the fresh `let mut st` binding (`ms_push(mut st, …)`).
- **`Vec[i64]` push/pop and last-element reads** as the stack primitives.

## Running

```bash
karac run   min_stack.kara
karac build min_stack.kara && ./min_stack
python3 min_stack.py
diff <(karac run min_stack.kara) <(python3 min_stack.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only (a design/data-structure kata, not a compute benchmark).
