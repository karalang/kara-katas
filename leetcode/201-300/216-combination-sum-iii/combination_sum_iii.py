"""LeetCode 216 — Combination Sum III (Python mirror / oracle).

Backtracking over ascending digits 1..9: place k distinct digits summing to n,
pruning once a digit exceeds the remaining sum. Mirrors the Kara version.
"""


def backtrack(start, k, remaining, path, results):
    if k == 0:
        if remaining == 0:
            results.append(list(path))
        return
    d = start
    while d <= 9:
        if d > remaining:
            return
        path.append(d)
        backtrack(d + 1, k - 1, remaining - d, path, results)
        path.pop()
        d += 1


def solve(k, n):
    results = []
    backtrack(1, k, n, [], results)
    return results


def report(k, n):
    print(f"k={k} n={n}:")
    results = solve(k, n)
    if not results:
        print("  (none)")
        return
    for combo in results:
        print("  " + " ".join(str(x) for x in combo))


def main():
    report(3, 7)
    report(3, 9)
    report(4, 1)
    report(2, 18)
    report(1, 5)
    report(3, 15)
    report(9, 45)
    report(2, 6)


main()
