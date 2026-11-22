# LeetCode #2749: Minimum Operations to Make the Integer Zero -- the ★ arm
# in Python (zero.kara): the least k from 1 to 60 with t = num1 - k num2
# a sum of k powers of two, its set bits at most k and k at most t.


def make_the_integer_zero(num1, num2):
    for k in range(1, 61):
        t = num1 - k * num2
        if t >= k and bin(t).count("1") <= k:
            return k
    return -1


seed = 2749


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(make_the_integer_zero(3, -2))
    print(make_the_integer_zero(5, 7))
    print(make_the_integer_zero(1, 0))
    print(make_the_integer_zero(1023, 0))
    print(make_the_integer_zero(1000000000, -1000000000))
    print(make_the_integer_zero(1000000000, 1000000000))
    print(make_the_integer_zero(1, -1000000000))
    total = check = 0
    for _ in range(2000):
        num1 = next_random() % 100 + 1
        num2 = next_random() % 21 - 10
        steps = make_the_integer_zero(num1, num2)
        total += steps
        check = (check * 31 + steps + 1) % 1000000007
    print(f"2000 small pairs: steps sum to {total}, checksum {check}")
    total = check = 0
    for _ in range(100000):
        num1 = (next_random() * 32768 + next_random()) % 1000000000 + 1
        size = (next_random() * 32768 + next_random()) % 1000000001
        num2 = size if next_random() % 2 == 0 else -size
        steps = make_the_integer_zero(num1, num2)
        total += steps
        check = (check * 31 + steps + 1) % 1000000007
    print(f"100000 pairs: steps sum to {total}, checksum {check}")


main()
