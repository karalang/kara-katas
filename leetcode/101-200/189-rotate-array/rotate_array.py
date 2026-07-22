"""LeetCode 189 — Rotate Array (Python mirror / oracle).

In-place right rotation by k via the triple-reversal trick: reverse all, then
each of [0,k) and [k,n). Mirrors the Kāra version.
"""


def reverse_range(a, lo, hi):
    i, j = lo, hi
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def rotate(a, k):
    n = len(a)
    if n == 0:
        return
    kk = k % n
    reverse_range(a, 0, n - 1)
    reverse_range(a, 0, kk - 1)
    reverse_range(a, kk, n - 1)


def report(values, k):
    a = list(values)
    rotate(a, k)
    print(" ".join(str(x) for x in a))


def main():
    report([1, 2, 3, 4, 5, 6, 7], 3)
    report([-1, -100, 3, 99], 2)
    report([1], 0)
    report([1, 2, 3], 4)
    report([1, 2, 3, 4, 5, 6], 6)


main()
