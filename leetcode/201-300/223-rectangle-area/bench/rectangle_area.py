"""Benchmark workload for LeetCode #223 — Rectangle Area (Python; scale lane)."""


def clamp0(x):
    return x if x > 0 else 0


def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    overlap_w = clamp0(min(ax2, bx2) - max(ax1, bx1))
    overlap_h = clamp0(min(ay2, by2) - max(ay1, by1))
    overlap = overlap_w * overlap_h
    return area_a + area_b - overlap


def main():
    pairs = 20000000
    mask = 16383
    modulus = 1000000007
    state = 12345
    sink = 0
    for _ in range(pairs):
        state = (state * 1103515245 + 12345) & 2147483647
        ax1 = state & mask
        state = (state * 1103515245 + 12345) & 2147483647
        ax2 = ax1 + (state & mask)
        state = (state * 1103515245 + 12345) & 2147483647
        ay1 = state & mask
        state = (state * 1103515245 + 12345) & 2147483647
        ay2 = ay1 + (state & mask)
        state = (state * 1103515245 + 12345) & 2147483647
        bx1 = state & mask
        state = (state * 1103515245 + 12345) & 2147483647
        bx2 = bx1 + (state & mask)
        state = (state * 1103515245 + 12345) & 2147483647
        by1 = state & mask
        state = (state * 1103515245 + 12345) & 2147483647
        by2 = by1 + (state & mask)
        area = compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2)
        sink = (sink + area) % modulus
    print(sink)


main()
