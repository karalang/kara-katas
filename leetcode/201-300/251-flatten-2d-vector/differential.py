"""LeetCode 251 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same draw order, same generator,
the same three solvers, the same positional checksum and the same report.

The PRNG stays in [0, 2^31) with non-negative operands throughout, so Python's
floor-division/modulo and Kara's truncating pair agree; there is no sign
correction to get wrong.
"""


def make_data(seed):
    """Regenerated per solver rather than cloned -- each run gets an identical
    but independent input, matching the .kara harness."""
    state = seed
    data = []
    state = (state * 1103515245 + 12345) % 2147483648
    rows = (state // 65536) % 13
    for _ in range(rows):
        state = (state * 1103515245 + 12345) % 2147483648
        roll = (state // 65536) % 100
        row = []
        if roll >= 45:
            state = (state * 1103515245 + 12345) % 2147483648
            cols = (state // 65536) % 6 + 1
            for _ in range(cols):
                state = (state * 1103515245 + 12345) % 2147483648
                row.append((state // 65536) % 1000)
        data.append(row)
    return data


def _digest(seq):
    s = 0
    n = 0
    for x in seq:
        s = (s * 31 + x + 1) % 1000000007
        n += 1
    return (s * 7 + n) % 1000000007


def run_cursor(data):
    row = col = 0
    out = []
    while True:
        while row < len(data) and col >= len(data[row]):
            row += 1
            col = 0
        if row >= len(data):
            break
        out.append(data[row][col])
        col += 1
    return _digest(out)


def run_flat(data):
    flat = []
    for r in data:
        for x in r:
            flat.append(x)
    return _digest(flat)


def run_offset(data):
    prefix = [0]
    running = 0
    for r in data:
        running += len(r)
        prefix.append(running)
    total = prefix[-1]
    out = []
    for k in range(total):
        lo, hi = 0, len(prefix) - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if prefix[mid + 1] > k:
                hi = mid
            else:
                lo = mid + 1
        out.append(data[lo][k - prefix[lo]])
    return _digest(out)


def main():
    cases = 4000
    seed = 251251

    mismatches = 0
    total_elems = 0
    total_rows = 0
    empty_rows = 0
    empty_iters = 0
    digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) % 2147483648

        a = run_cursor(make_data(seed))
        b = run_flat(make_data(seed))
        d = run_offset(make_data(seed))

        if a != b or a != d:
            mismatches += 1
        digest = (digest * 131 + a) % 1000000007

        shape = make_data(seed)
        here = 0
        for r in shape:
            total_rows += 1
            if len(r) == 0:
                empty_rows += 1
            here += len(r)
        total_elems += here
        if here == 0:
            empty_iters += 1

    print(f"cases {cases}")
    print(f"rows {total_rows}")
    print(f"empty rows {empty_rows}")
    print(f"elements {total_elems}")
    print(f"empty iterators {empty_iters}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
