# 150. Evaluate Reverse Polish Notation

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Stack · Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/evaluate-reverse-polish-notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

Evaluate an arithmetic expression given in **Reverse Polish (postfix) notation**. Valid operators are `+`, `-`, `*`, `/`; operands are integers. Division **truncates toward zero**.

```
["2","1","+","3","*"]                                         ->  9     ((2 + 1) * 3)
["4","13","5","/","+"]                                        ->  6     (4 + 13/5)
["10","6","9","3","+","-11","*","/","*","17","+","5","+"]     ->  22
["-7","2","/"]                                                ->  -3    (toward zero, not -4)
["4","-2","/"]                                                ->  -2
["3","-4","*"]                                                ->  -12
```

**Constraints:** `1 ≤ tokens.length ≤ 10⁴`; each token is an operator or an integer in `[-2⁰⁰, 2⁰⁰)`; the expression is always valid and never divides by zero.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **operand stack, single left-to-right scan** ★ | [`eval_rpn.kara`](eval_rpn.kara) ✓ | [`eval_rpn.py`](eval_rpn.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A textbook stack machine. Scan the tokens once, keeping an operand stack (`Vec[i64]`):

- **Operator** — pop the top two operands `a`, `b` (in that order: `b` is the second popped) and push `a ⊕ b`.
- **Operand** — parse the integer and push it.

The one subtlety is lexical: `"-"` the subtraction operator and `"-11"` the negative literal share a leading byte. So a token is an operator **iff it is exactly one byte long and that byte is `+ - * /`** — checked over the token's `bytes()` view, never by trying to parse it as a number first. `parse_int` then reads an optional leading `-` and accumulates base-10 digits. Division uses Kāra's `/`, which truncates toward zero (matching C/Rust and the problem spec) — verified by `-7 / 2 = -3`, not `-4`.

## Kāra features exercised

- **`Vec[i64]` as a stack** — `stack.push(r)` and `stack.pop().unwrap()` (the `Option[i64]` pop).
- **Byte-level string inspection** — `t.bytes()` → `Slice[u8]`, byte literals `b'+'` / `b'0'` / `b'-'`, `(byte as i64)` digit conversion (the self-hosted-lexer idiom, no `Vec[char]` snapshot).
- **`ref String` params** read out of a `Vec[String]` by index (`is_op(tokens[i])`, `parse_int(tokens[i])`) — a borrow, read twice in the loop without a move.
- **`if`-expression chain** selecting the operator to apply.

## Running

```bash
karac run   eval_rpn.kara
karac build eval_rpn.kara && ./eval_rpn
python3 eval_rpn.py
diff <(karac run eval_rpn.kara) <(python3 eval_rpn.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.

**No cross-language benchmark** (oracle-only, like the RC/linked-list cluster). RPN evaluation is a strictly sequential stack machine — the top-of-stack dependency chain forbids parallelization, and the per-token work is a single branch plus one integer op. A benchmark would measure either the stdlib **string-parsing** of the number tokens (a runtime-library comparison, not codegen) or a trivially light arithmetic loop; neither is a clean codegen signal. The compute-bound katas in this range that *are* benched (e.g. [#149](../149-max-points-on-a-line/), [#152](../152-maximum-product-subarray/)) carry a real cross-language workload.
