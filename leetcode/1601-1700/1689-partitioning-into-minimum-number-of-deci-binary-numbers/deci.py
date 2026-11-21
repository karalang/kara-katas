# LeetCode #1689: Partitioning Into Minimum Number Of Deci-Binary Numbers --
# mirrors deci.kara, the ★ arm: the largest digit.


def min_partitions(n):
    largest = 0
    for b in n.encode():
        largest = max(largest, b - 48)
    return largest


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, seed):
    digits = "0123456789"
    total = 0
    check = 0
    for _ in range(count):
        length = (seed.next() * 32768 + seed.next()) % most + 1
        top = seed.next() % 9 + 1
        n = digits[seed.next() % top + 1]
        n += "".join(digits[seed.next() % (top + 1)] for _ in range(1, length))
        answer = min_partitions(n)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} numbers of up to {most} digits: answers sum to {total}, checksum {check}")


def main():
    print(min_partitions("32"))
    print(min_partitions("82734"))
    print(min_partitions("27346209830709182346"))
    print(min_partitions("1"))
    print(min_partitions("1000"))
    seed = Seed(1689)
    batch(3000, 10, seed)
    batch(300, 1000, seed)
    batch(10, 100000, seed)


main()
