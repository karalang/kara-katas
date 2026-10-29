# LeetCode #1014: Best Sightseeing Pair -- bench
# Mirrors sightseeing.kara; see ../README.md § Benchmarks.


def max_score_sightseeing_pair(values):
    best_first = values[0]
    best = 0
    for j in range(1, len(values)):
        best = max(best, best_first + values[j] - j)
        best_first = max(best_first, values[j] + j)
    return best


seed = 1014


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 50000
    rounds = 10000
    values = [1 + next_random() % 1000 for _ in range(count)]
    total = 0
    check = 0
    for _ in range(rounds):
        at = (next_random() * 32768 + next_random()) % count
        values[at] = 1 + next_random() % 1000
        answer = max_score_sightseeing_pair(values)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{rounds} rounds over {count} values: answers sum to {total}, checksum {check}")


main()
