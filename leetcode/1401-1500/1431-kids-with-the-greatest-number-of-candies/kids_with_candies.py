# LeetCode #1431, Python mirror of kids_with_candies.kara: the most any kid
# has, and each kid against it with the extra.


def kids_with_candies(candies, extra_candies):
    most = max(candies)
    return [c + extra_candies >= most for c in candies]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shown(answer):
    return "".join("T" if b else "F" for b in answer)


def main():
    global seed
    firsts = [
        shown(kids_with_candies([2, 3, 5, 1, 3], 3)),
        shown(kids_with_candies([4, 2, 1, 1, 2], 1)),
        shown(kids_with_candies([12, 1, 12], 10)),
        shown(kids_with_candies([1, 1], 1)),
        shown(kids_with_candies([100, 50], 50)),
        shown(kids_with_candies([100, 49], 50)),
    ]
    print(" ".join(firsts))
    seed = 1431
    kids = [1 + next_random() % 100 for _ in range(100)]
    counts = [str(sum(kids_with_candies(kids, e))) for e in [1, 25, 50]]
    print(f"100 kids: {' '.join(counts)} can have the most")
    check = 0
    total = 0
    for _ in range(2000):
        n = 2 + next_random() % 99
        top = 1 + next_random() % 100
        candies = [1 + next_random() % top for _ in range(n)]
        extra = 1 + next_random() % 50
        for b in kids_with_candies(candies, extra):
            bit = 1 if b else 0
            total += bit
            check = (check * 3 + 1 + bit) % 1000000007
    print(f"2000 random cases: {total} can have the most, checksum {check}")


main()
