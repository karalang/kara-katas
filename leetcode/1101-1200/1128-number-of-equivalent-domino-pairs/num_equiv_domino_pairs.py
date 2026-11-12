# LeetCode #1128: Number of Equivalent Domino Pairs -- the Python mirror of
# the ★ arm: each domino read with its smaller number first, as one of 100
# keys, and each new domino pairs with every one already counted under
# its key.


def num_equiv_domino_pairs(dominoes):
    count = [0] * 100
    pairs = 0
    for a, b in dominoes:
        key = min(a, b) * 10 + max(a, b)
        pairs += count[key]
        count[key] += 1
    return pairs


# ---- test harness ----

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    cases = [
        [[1, 2], [2, 1], [3, 4], [5, 6]],
        [[1, 2], [1, 2], [1, 1], [1, 2], [2, 2]],
        [[1, 1]],
        [[1, 1], [1, 1], [1, 1], [1, 1]],
        [[1, 2], [2, 1], [1, 2], [2, 1]],
        [[1, 9], [9, 1], [9, 9], [1, 1]],
        [[3, 4], [4, 5], [5, 3], [4, 3]],
        [[2, 7], [7, 2], [2, 7], [7, 7], [2, 2], [7, 2]],
    ]
    for c in cases:
        print(f"{c} -> {num_equiv_domino_pairs(c)}")
    seed = 1128
    total = 0
    check = 0
    for t in range(2000):
        n = next_random() % 400 + 1
        top = 1 + t % 9
        dominoes = [[next_random() % top + 1, next_random() % top + 1] for _ in range(n)]
        answer = num_equiv_domino_pairs(dominoes)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"2000 random sets: pairs total {total}, checksum {check}")
    big = [[next_random() % 9 + 1, next_random() % 9 + 1] for _ in range(40000)]
    print(f"40000 random dominoes: {num_equiv_domino_pairs(big)} pairs")
    same = [[4, 7] if i % 2 == 0 else [7, 4] for i in range(40000)]
    print(f"40000 alike: {num_equiv_domino_pairs(same)} pairs")


main()
