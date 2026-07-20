"""LeetCode 143 — Reorder List (Python mirror / oracle).

Reorder L0..Ln into L0, Ln, L1, Ln-1, … — the interleaved index order
0, n-1, 1, n-2, … via two inward pointers. The Kāra version rewires a
Vec-owned + `weak` next overlay so the interleaved links stay leak-free.
"""


def reorder(vals):
    n = len(vals)
    order = []
    lo, hi = 0, n - 1
    take_lo = True
    while lo <= hi:
        if take_lo:
            order.append(lo)
            lo += 1
        else:
            order.append(hi)
            hi -= 1
        take_lo = not take_lo
    return [vals[i] for i in order]


def run(vals):
    print(" ".join(str(x) for x in reorder(vals)))


def main():
    run([1, 2, 3, 4])
    run([1, 2, 3, 4, 5])
    run([1])
    run([1, 2])


main()
