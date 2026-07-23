# 227. Basic Calculator II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String · Stack · Math · Parsing &nbsp;·&nbsp; **Source:** [leetcode.com/problems/basic-calculator-ii](https://leetcode.com/problems/basic-calculator-ii/)

Evaluate a string expression of non-negative integers with `+`, `-`, `*`, `/` and spaces (no parentheses). `*` and `/` bind tighter than `+` and `-`, and integer division **truncates toward zero**.

```
"3+2*2"      ->  7
" 3/2 "      ->  1
"14-3/2"     ->  13
```

**Constraints:** `1 ≤ |s| ≤ 3·10⁵`; the expression is valid and fits in a 32-bit result.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **term stack (precedence)** ★ | [`basic_calculator_ii.kara`](basic_calculator_ii.kara) | [`basic_calculator_ii.py`](basic_calculator_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Precedence is resolved with a stack of terms, in a single pass. Accumulate the current number; when the next operator (or end of string) is reached, apply the **previous** operator to it:

- `+` → push `num`, `-` → push `-num` (deferred, to be summed later);
- `*` → pop the top and push `top * num`, `/` → pop the top and push `top / num` (folded in immediately, honouring tight binding).

Because `*` and `/` collapse into the stack top right away while `+`/`-` only leave signed values behind, the final answer is simply the **sum of the stack**. Kāra's `/` truncates toward zero, which is exactly the required division rule — the Python mirror uses an explicit truncating helper (its `//` floors) so the two agree on the sign edge cases.

## Kāra features exercised

- **`s.bytes()` scan with a term stack** — digit accumulation via `b'0'` byte literals, a `Vec[i64]` stack with `push` and `pop` (→ `Option`, matched via a `pop_or_zero` helper) for the `*`/`/` fold.
- **Truncating integer division** — `t / num` relies on Kāra's toward-zero `/`; the mirror replicates it explicitly to stay byte-identical on negatives.
- **"Apply on operator or last char"** — a single condition drives both the mid-string operator handling and the trailing flush.

## Running

```bash
karac run   basic_calculator_ii.kara
karac build basic_calculator_ii.kara && ./basic_calculator_ii
python3 basic_calculator_ii.py
diff <(karac run basic_calculator_ii.kara) <(python3 basic_calculator_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
