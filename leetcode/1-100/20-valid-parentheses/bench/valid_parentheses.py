"""Benchmark workload — Valid Parentheses (LeetCode #20).

Python mirror of bench/valid_parentheses.kara. Same byte-buffer build +
stack-of-expected-closers validate + count-valid sink. Runs a scaled-down
K = 100_000 (the compiled mirrors run K = 500_000) — timed separately, not
in the cross-mirror sink check. Sink at K = 100_000: corrupt fires on
k % 7 == 0 (⌈100000/7⌉ = 14286 iters), so valid = 100000 − 14286 = 85714.
See ../README.md § Benchmarks.
"""

from __future__ import annotations

_CLOSER = {ord("("): ord(")"), ord("["): ord("]"), ord("{"): ord("}")}


def is_valid_bytes(data: bytes) -> bool:
    stack: list[int] = []
    for b in data:
        c = _CLOSER.get(b)
        if c is not None:
            stack.append(c)
        else:
            if not stack or stack.pop() != b:
                return False
    return not stack


def build_brackets(depth: int, kind: int, corrupt: bool) -> bytes:
    op, cl, wrong = (ord("("), ord(")"), ord("]"))
    if kind == 1:
        op, cl, wrong = (ord("["), ord("]"), ord(")"))
    elif kind == 2:
        op, cl, wrong = (ord("{"), ord("}"), ord(")"))
    buf = bytearray()
    buf.extend(op for _ in range(depth))
    buf.extend(cl for _ in range(depth - 1))
    buf.append(wrong if corrupt else cl)
    return bytes(buf)


def main() -> None:
    depth = 1000
    k_iters = 100_000

    count = 0
    for k in range(k_iters):
        kind = k % 3
        corrupt = (k % 7) == 0
        buf = build_brackets(depth, kind, corrupt)
        if is_valid_bytes(buf):
            count += 1
    print(count)


if __name__ == "__main__":
    main()
