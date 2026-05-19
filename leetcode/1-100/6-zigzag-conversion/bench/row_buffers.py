"""Benchmark workload — row-buffer Zigzag Conversion. Python mirror of
bench/row_buffers.kara. Same N, R, K, num_rows, same input pattern,
same sink formula — see that file's header for the workload rationale
and sink derivation."""

from __future__ import annotations


def convert_off(
    chars: list[str], off: int, length: int, num_rows: int
) -> list[str]:
    if num_rows <= 1 or num_rows >= length:
        # Pass-through: never fires at the bench's N=10000, num_rows=4
        # parameters. The explicit list-build (rather than `chars[off:off+length]`)
        # keeps the per-iter shape identical to the main path so the
        # branch's cost stays comparable to the Kāra version.
        return [chars[off + i] for i in range(length)]

    rows: list[list[str]] = [[] for _ in range(num_rows)]
    cur = 0
    going_down = False
    for i in range(length):
        rows[cur].append(chars[off + i])
        if cur == 0 or cur == num_rows - 1:
            going_down = not going_down
        cur += 1 if going_down else -1

    out: list[str] = []
    for row in rows:
        out.extend(row)
    return out


def main() -> None:
    n = 10_000
    r_period = 1_000
    k_iters = 10_000
    num_rows = 4

    pattern = list("PAYPALISHIRING")
    need = n + r_period
    chars: list[str] = []
    while len(chars) < need:
        chars.extend(pattern)

    total = 0
    for k in range(k_iters):
        off = k % r_period
        result = convert_off(chars, off, n, num_rows)
        last = len(result) - 1
        total += ord(result[0]) + ord(result[last])
    print(total)


if __name__ == "__main__":
    main()
