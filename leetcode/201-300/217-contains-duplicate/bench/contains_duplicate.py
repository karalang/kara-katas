"""Benchmark workload for LeetCode #217 — Contains Duplicate (Python; scale lane)."""


def window_has_dup(base, w, width):
    seen = set()
    for t in range(width):
        x = base[w + t]
        if x in seen:
            return True
        seen.add(x)
    return False


def main():
    big = 240000
    width = 800
    m = 2000000

    base = []
    state = 12345
    for _ in range(big):
        state = (state * 1103515245 + 12345) & 2147483647
        base.append(state % m)

    windows = big - width
    sink = 0
    for w in range(windows):
        if window_has_dup(base, w, width):
            sink += 1
    print(sink)


main()
