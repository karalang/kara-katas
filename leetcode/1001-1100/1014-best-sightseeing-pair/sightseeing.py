# LeetCode #1014: Best Sightseeing Pair -- one pass (mirror of sightseeing.kara)


def max_score_sightseeing_pair(values):
    best_first = values[0]
    best = 0
    for j in range(1, len(values)):
        best = max(best, best_first + values[j] - j)
        best_first = max(best_first, values[j] + j)
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_values(seed, length, most):
    return [1 + next_random(seed) % most for _ in range(length)]


def shown(values):
    return "[" + ",".join(str(x) for x in values) + "]"


def main():
    examples = [
        [8, 1, 5, 2, 6],
        [1, 2],
        [1, 1],
        [1000, 1000],
        [1, 1000],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 1, 1, 3],
        [1, 3, 1, 3],
        [7, 1, 1, 1, 1, 1, 8],
        [2, 2, 2, 2, 2],
        [10, 1, 1, 10],
        [1, 1000, 1, 1, 999, 1000],
    ]
    for values in examples:
        print(f"values = {shown(values)} -> {max_score_sightseeing_pair(values)}")
    seed = [1014]
    groups = [(3000, 2, 1000), (3000, 8, 10), (1000, 60, 1000), (200, 1000, 1000), (6, 50000, 1000), (6, 50000, 2)]
    for count, length, most in groups:
        total = 0
        check = 0
        for _ in range(count):
            values = random_values(seed, length, most)
            answer = max_score_sightseeing_pair(values)
            total += answer
            check = (check * 31 + answer) % 1000000007
        print(f"{count} random arrays of {length} values up to {most}: answers sum to {total}, checksum {check}")
    planted = 0
    beaten = 0
    for _ in range(1000):
        values = random_values(seed, 2000, 10)
        gap = 1 + next_random(seed) % 1999
        at = next_random(seed) % (2000 - gap)
        values[at] = 1000
        values[at + gap] = 1000
        answer = max_score_sightseeing_pair(values)
        if answer == 2000 - gap:
            planted += 1
        else:
            beaten += 1
    print(f"1000 planted pairs: {planted} are the best pair, {beaten} beaten")


main()
