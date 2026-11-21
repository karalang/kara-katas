# LeetCode #2350: Shortest Impossible Sequence of Rolls -- the Python
# mirror of the ★ arm: the rolls cut greedily into pieces that each hold
# every face from 1 to k; with m whole pieces every sequence of length m
# can be taken and some sequence of length m + 1 cannot.


def shortest_sequence(rolls, k):
    seen = [False] * (k + 1)
    distinct = 0
    pieces = 0
    for r in rolls:
        if not seen[r]:
            seen[r] = True
            distinct += 1
            if distinct == k:
                pieces += 1
                distinct = 0
                seen = [False] * (k + 1)
    return pieces + 1


SEED = [2350]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's three examples; then one face rolled 10^5 times, 10^5
    # rolls cycling through 1000 faces, and 10^5 faces each rolled once
    print(shortest_sequence([4, 2, 1, 2, 3, 3, 2, 4, 1], 4))
    print(shortest_sequence([1, 1, 2, 2], 2))
    print(shortest_sequence([1, 1, 3, 2, 2, 2, 3, 3], 4))
    print(shortest_sequence([1] * 100000, 1))
    print(shortest_sequence([i % 1000 + 1 for i in range(100000)], 1000))
    print(shortest_sequence([100000 - i for i in range(100000)], 100000))
    # 2000 random cases of 1 to 40 rolls of a die with 1 to 6 faces
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        k = 1 + next_random() % 6
        rolls = [1 + next_random() % k for _ in range(n)]
        answer = shortest_sequence(rolls, k)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"2000 cases: checksum {check}, sum {total}")


main()
