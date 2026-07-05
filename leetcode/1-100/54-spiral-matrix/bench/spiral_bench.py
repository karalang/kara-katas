"""Bench mirror of spiral_bench.kara — boundary-shrinking spiral over a batch of LCG-filled
24x24 matrices, position-weighted checksum folded into an i64 sink. CPython.
See ../README.md § Benchmarks.

CPython is ~2 orders of magnitude slower on this tight scalar loop, so it is excluded from the
headline table by default (KARA_BENCH_INCLUDE_PY=1 to include).
"""


def main() -> None:
    m = 1103515245        # glibc LCG multiplier
    inc = 12345           # glibc LCG increment
    modulus = 2147483648  # 2^31
    windows = 200000      # number of simulated input matrices
    rows = 24
    cols = 24
    n = 576               # rows * cols

    grid = [0] * 576
    state = 1             # LCG seed
    sink = 0
    for _ in range(windows):
        for idx in range(n):
            state = (state * m + inc) % modulus
            grid[idx] = (state % 100) - 50
        local = 0
        pos = 0
        top, bottom, left, right = 0, rows - 1, 0, cols - 1
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                local += (pos + 1) * grid[top * cols + c]
                pos += 1
            top += 1
            for r in range(top, bottom + 1):
                local += (pos + 1) * grid[r * cols + right]
                pos += 1
            right -= 1
            if top <= bottom:
                for c2 in range(right, left - 1, -1):
                    local += (pos + 1) * grid[bottom * cols + c2]
                    pos += 1
                bottom -= 1
            if left <= right:
                for r2 in range(bottom, top - 1, -1):
                    local += (pos + 1) * grid[r2 * cols + left]
                    pos += 1
                left += 1
        sink += local
    print(sink)


if __name__ == "__main__":
    main()
