# LeetCode #646: Maximum Length of Pair Chain -- earliest end first.
# Mirrors the ★ arm (pair_chain.kara) and its test harness.


def find_longest_chain(pairs):
    order = sorted(pairs, key=lambda p: p[1])
    count = 0
    end = 0
    for p in order:
        if count == 0 or p[0] > end:
            count += 1
            end = p[1]
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(pairs):
    print(f"{pairs} -> {find_longest_chain(pairs)}")


def random_pairs(count, low, high, longest):
    pairs = []
    for _ in range(count):
        left = low + next_random() % (high - low)
        right = left + 1 + next_random() % longest
        pairs.append([left, right])
    return pairs


def main():
    global seed
    show([[1, 2], [2, 3], [3, 4]])
    show([[1, 2], [7, 8], [4, 5]])
    show([[-1000, 1000]])
    show([[3, 4], [3, 4], [3, 4]])
    show([[1, 100], [2, 3], [4, 5]])
    show([[2, 3], [4, 5], [1, 100], [6, 7]])
    show([[1, 2], [-4, 0], [-10, -5], [-3, -2]])
    show([[5, 6], [4, 5], [3, 4], [2, 3], [1, 2]])
    show([[-1000, -999], [999, 1000], [-999, 999]])
    seed = 646
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        c = find_longest_chain(random_pairs(n, -50, 50, 20))
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    print(f"1000 pairs: {find_longest_chain(random_pairs(1000, -1000, 900, 100))}")
    print(f"1000 short pairs: {find_longest_chain(random_pairs(1000, -1000, 997, 3))}")


main()
