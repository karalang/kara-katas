"""LeetCode 218 — The Skyline Problem (Python mirror / oracle).

Divide and conquer (merge-sort shaped): the skyline of one building is
[[L,H],[R,0]]; merge two contours by sweeping both and emitting a key point
whenever the max of the two current heights changes. Mirrors the Kara version.
"""


def merge(left, right):
    result = []
    nl, nr = len(left), len(right)
    i = j = 0
    h1 = h2 = 0
    while i < nl and j < nr:
        if left[i][0] < right[j][0]:
            x = left[i][0]
            h1 = left[i][1]
            i += 1
        elif left[i][0] > right[j][0]:
            x = right[j][0]
            h2 = right[j][1]
            j += 1
        else:
            x = left[i][0]
            h1 = left[i][1]
            h2 = right[j][1]
            i += 1
            j += 1
        maxh = h1 if h1 > h2 else h2
        if not result or result[-1][1] != maxh:
            result.append([x, maxh])
    while i < nl:
        result.append(left[i])
        i += 1
    while j < nr:
        result.append(right[j])
        j += 1
    return result


def skyline(bs, lo, hi):
    if hi - lo == 1:
        l, r, h = bs[lo]
        return [[l, h], [r, 0]]
    mid = lo + (hi - lo) // 2
    left = skyline(bs, lo, mid)
    right = skyline(bs, mid, hi)
    return merge(left, right)


def report(bs):
    if not bs:
        print("[]")
        return
    sky = skyline(bs, 0, len(bs))
    print(" ".join(f"[{p[0]},{p[1]}]" for p in sky))


def main():
    report([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]])
    report([[0, 2, 3], [2, 5, 3]])
    report([[1, 5, 11]])
    report([[1, 2, 1], [1, 2, 2], [1, 2, 3]])
    report([[1, 3, 4], [5, 7, 6]])
    report([[0, 10, 5], [3, 6, 3]])
    report([])


main()
