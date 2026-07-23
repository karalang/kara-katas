"""LeetCode 223 — Rectangle Area (Python mirror / oracle).

Union area by inclusion-exclusion: area(A) + area(B) - area(A ∩ B), with each
intersection span clamped at 0. Mirrors the Kara version.
"""


def clamp0(x):
    return x if x > 0 else 0


def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    overlap_w = clamp0(min(ax2, bx2) - max(ax1, bx1))
    overlap_h = clamp0(min(ay2, by2) - max(ay1, by1))
    overlap = overlap_w * overlap_h
    return area_a + area_b - overlap


def report(*coords):
    print(compute_area(*coords))


def main():
    report(-3, 0, 3, 4, 0, -1, 9, 2)
    report(0, 0, 0, 0, 0, 0, 0, 0)
    report(0, 0, 1, 1, 1, 1, 2, 2)
    report(0, 0, 2, 2, 1, 1, 3, 3)
    report(0, 0, 1, 1, 5, 5, 6, 6)
    report(0, 0, 4, 4, 1, 1, 2, 2)
    report(-2, -2, 2, 2, -1, -1, 1, 1)


main()
