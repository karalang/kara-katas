"""Benchmark workload — 8-state DFA for LeetCode #65. Python mirror of
bench/valid.kara. Same N, K, input set, sink formula — see that file's
header for the workload rationale.

CPython's per-bytecode dispatch dominates the inner loop; expect
~100-1000× slowdown vs the codegen path.
"""

from __future__ import annotations

DIGIT = 0
SIGN  = 1
DOT   = 2
EXP   = 3
OTHER = 4


def categorize(c: str) -> int:
    if '0' <= c <= '9':
        return DIGIT
    if c == '+' or c == '-':
        return SIGN
    if c == '.':
        return DOT
    if c == 'e' or c == 'E':
        return EXP
    return OTHER


def is_number(s: str) -> bool:
    state = 0
    for c in s:
        cat = categorize(c)
        if state == 0:
            if   cat == DIGIT: state = 2
            elif cat == SIGN:  state = 1
            elif cat == DOT:   state = 3
            else: return False
        elif state == 1:
            if   cat == DIGIT: state = 2
            elif cat == DOT:   state = 3
            else: return False
        elif state == 2:
            if   cat == DIGIT: state = 2
            elif cat == DOT:   state = 4
            elif cat == EXP:   state = 6
            else: return False
        elif state == 3:
            if   cat == DIGIT: state = 5
            else: return False
        elif state == 4:
            if   cat == DIGIT: state = 5
            elif cat == EXP:   state = 6
            else: return False
        elif state == 5:
            if   cat == DIGIT: state = 5
            elif cat == EXP:   state = 6
            else: return False
        elif state == 6:
            if   cat == DIGIT: state = 8
            elif cat == SIGN:  state = 7
            else: return False
        elif state == 7:
            if   cat == DIGIT: state = 8
            else: return False
        elif state == 8:
            if   cat == DIGIT: state = 8
            else: return False
        else:
            return False
    return state == 2 or state == 4 or state == 5 or state == 8


def main() -> None:
    n = 8
    k_iters = 10_000_000

    inputs = [
        "0",
        "-.9",
        "53.5e93",
        "+6e-1",
        "abc",
        "1e",
        "99e2.5",
        "-123.456e789",
    ]

    total = 0
    for k in range(k_iters):
        if is_number(inputs[k % n]):
            total += 1
    print(total)


if __name__ == "__main__":
    main()
