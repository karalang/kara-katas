"""LeetCode #351: Android Unlock Patterns — Python mirror.

Mirrors unlock_patterns.kara: a depth-first search with a skip table, run
from keys 1, 2 and 5 and weighted 4, 4 and 1 by the grid's symmetry.
Prints the same lines.
"""


def skip_table():
    skip = [0] * 100
    for a, b, mid in [(1, 3, 2), (4, 6, 5), (7, 9, 8), (1, 7, 4), (2, 8, 5), (3, 9, 6), (1, 9, 5), (3, 7, 5)]:
        skip[a * 10 + b] = mid
        skip[b * 10 + a] = mid
    return skip


def count_from(key, length, m, n, visited, skip):
    total = 0
    if length >= m:
        total += 1
    if length == n:
        return total
    visited[key] = True
    for nxt in range(1, 10):
        mid = skip[key * 10 + nxt]
        if not visited[nxt] and (mid == 0 or visited[mid]):
            total += count_from(nxt, length + 1, m, n, visited, skip)
    visited[key] = False
    return total


def number_of_patterns(m, n):
    if m > n:
        return 0
    skip = skip_table()
    visited = [False] * 10
    corner = count_from(1, 1, m, n, visited, skip)
    edge = count_from(2, 1, m, n, visited, skip)
    center = count_from(5, 1, m, n, visited, skip)
    return 4 * corner + 4 * edge + center


def main():
    print(f"m=1 n=1 -> {number_of_patterns(1, 1)}")
    print(f"m=1 n=2 -> {number_of_patterns(1, 2)}")
    total = 0
    for k in range(1, 10):
        c = number_of_patterns(k, k)
        print(f"length {k}: {c}")
        total += c
    print(f"lengths 1..9 one at a time: {total}")
    print(f"m=1 n=9 -> {number_of_patterns(1, 9)}")
    print(f"m=4 n=9 -> {number_of_patterns(4, 9)}")
    print(f"m=3 n=5 -> {number_of_patterns(3, 5)}")
    print(f"m=9 n=1 -> {number_of_patterns(9, 1)}")


if __name__ == "__main__":
    main()
