# LeetCode #1049: Last Stone Weight II -- Python mirror of last_stone.kara.
#
# The same table: which sums up to half the total some set of the stones
# makes, filled one stone at a time and walked downward.


def last_stone_weight_ii(stones):
    total = sum(stones)
    half = total // 2
    made = [False] * (half + 1)
    made[0] = True
    for s in stones:
        t = half
        while t >= s:
            if made[t - s]:
                made[t] = True
            t -= 1
    best = half
    while not made[best]:
        best -= 1
    return total - 2 * best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_stones(count, heaviest):
    return [next_random() % heaviest + 1 for _ in range(count)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [2, 7, 4, 1, 8, 1],
        [31, 26, 33, 21, 40],
        [1],
        [1, 1],
        [1, 2],
        [100, 1],
        [3, 3, 3],
        [1, 1, 4, 2, 2],
        [8, 9, 10, 25],
        [2] * 29 + [99],
    ]
    for stones in examples:
        print(f"{show(stones)} -> {last_stone_weight_ii(stones)}")
    seed = 1049
    total = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 8 + 1
        answer = last_stone_weight_ii(random_stones(count, 20))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"3000 random lists of 1 to 8 stones of 1 to 20: total {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(500):
        count = next_random() % 30 + 1
        answer = last_stone_weight_ii(random_stones(count, 100))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"500 random lists of 1 to 30 stones of 1 to 100: total {total}, checksum {check}")
    heavy = [100] * 29 + [99]
    print(f"29 stones of 100 and one of 99 -> {last_stone_weight_ii(heavy)}")
    odd = [1 + 2 * (i % 50) for i in range(30)]
    print(f"30 odd stones 1 to 59 -> {last_stone_weight_ii(odd)}")


main()
