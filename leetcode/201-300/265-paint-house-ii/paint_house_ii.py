"""LeetCode 265 — Paint House II (Python mirror / oracle).

Mirrors paint_house_ii.kara algorithm-for-algorithm: one pass per row for the
minimum, its index, and the second minimum WITH MULTIPLICITY, then O(k) to fill
the next row. Returns -1 when no painting exists (k = 1 with n >= 2).
"""

INF = 1000000000000


def min_cost(costs, k):
    n = len(costs)
    if n == 0:
        return 0
    prev = [costs[0][c] for c in range(k)]
    for i in range(1, n):
        min1, idx1, min2 = INF, -1, INF
        for j in range(k):
            if prev[j] < min1:
                min2 = min1
                min1 = prev[j]
                idx1 = j
            elif prev[j] < min2:
                min2 = prev[j]
        prev = [costs[i][t] + (min2 if t == idx1 else min1) for t in range(k)]
    answer = min(prev)
    return -1 if answer >= INF else answer


def report(label, costs, k):
    print(f"{label} -> {min_cost(costs, k)}")


def main():
    report("[] k=3", [], 3)
    report("[[1,5,3],[2,9,4]] k=3", [[1, 5, 3], [2, 9, 4]], 3)
    report("[[7,6,2]] k=3", [[7, 6, 2]], 3)
    report("[[4]] k=1", [[4]], 1)
    report("[[4],[9]] k=1", [[4], [9]], 1)
    report("[[1,100]x3] k=2", [[1, 100], [1, 100], [1, 100]], 2)
    report("[[3,3,5],[1,50,50]] k=3", [[3, 3, 5], [1, 50, 50]], 3)
    report("5 colours, 4 houses",
           [[8, 1, 6, 7, 9], [2, 9, 3, 4, 1], [5, 5, 5, 5, 5], [9, 2, 8, 1, 7]], 5)


main()
