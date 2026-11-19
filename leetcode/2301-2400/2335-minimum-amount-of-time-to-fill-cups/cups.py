# LeetCode #2335: Minimum Amount of Time to Fill Cups -- the Python mirror
# of the ★ arm: the larger of the most cups of one kind and half of all
# the cups, rounded up.


def fill_cups(amount):
    return max(max(amount), (sum(amount) + 1) // 2)


SEED = [2335]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    print(fill_cups([1, 4, 2]))
    print(fill_cups([5, 4, 4]))
    print(fill_cups([5, 0, 0]))
    print(fill_cups([0, 0, 0]))
    print(fill_cups([100, 100, 100]))
    print(fill_cups([0, 100, 0]))
    print(fill_cups([40, 99, 60]))
    check = 0
    total = 0
    for _ in range(2000):
        amount = []
        for _ in range(3):
            cups = 0 if next_random() % 5 == 0 else next_random() % 101
            amount.append(cups)
        seconds = fill_cups(amount)
        check = (check * 31 + seconds) % 1000000007
        total += seconds
    print(f"2000 cases: checksum {check}, total {total}")


main()
