"""Benchmark workload for LeetCode #351 — Python mirror of unlock_patterns.kara."""

ROUNDS = 48


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
    sink = 0
    for rnd in range(ROUNDS):
        for m in range(1, 10):
            for n in range(1, 10):
                c = number_of_patterns(m, n)
                sink = (sink * 31 + c + rnd) % 1000000007
    print(f"sink {sink}")


if __name__ == "__main__":
    main()
