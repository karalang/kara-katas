# LeetCode #1689: Partitioning Into Minimum Number Of Deci-Binary Numbers --
# the bench's Python mirror: the ★ arm on 100 random numbers of 100000
# digits, all drawn first, each answered 50 times.


def min_partitions(n):
    largest = 0
    for b in n.encode():
        largest = max(largest, b - 48)
    return largest


seed = 1689


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 100, 100000, 50
    digits = "0123456789"
    numbers = []
    for _ in range(count):
        top = next_random() % 9 + 1
        n = [digits[next_random() % top + 1]]
        for _ in range(1, size):
            n.append(digits[next_random() % (top + 1)])
        numbers.append("".join(n))
    total = 0
    check = 0
    for r in range(rounds):
        for n in numbers:
            answer = min_partitions(n)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} numbers of {size} digits, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
