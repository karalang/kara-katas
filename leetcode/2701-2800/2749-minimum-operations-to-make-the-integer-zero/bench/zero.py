# LeetCode #2749: Minimum Operations to Make the Integer Zero -- the bench
# (zero.kara in Python): the least k with t = num1 - k num2 a sum of k
# powers of two, by `int.bit_count`.


def make_the_integer_zero(num1, num2):
    for k in range(1, 61):
        t = num1 - k * num2
        if t >= k and t.bit_count() <= k:
            return k
    return -1


seed = 2749


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 1000000, 10
    pairs = []
    for _ in range(count):
        num1 = (next_random() * 32768 + next_random()) % 1000000000 + 1
        size = (next_random() * 32768 + next_random()) % 1000000001
        num2 = size if next_random() % 2 == 0 else -size
        pairs.append((num1, num2))
    total = check = 0
    for r in range(rounds):
        for num1, num2 in pairs:
            steps = make_the_integer_zero(num1, num2)
            total += steps
            check = (check * 31 + steps + 1 + r) % 1000000007
    print(f"{count} pairs, {rounds} rounds: steps sum to {total}, checksum {check}")


main()
