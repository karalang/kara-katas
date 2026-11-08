# LeetCode #1067: Digit Count in Range -- the Python mirror of
# digit_count.kara (the ★ arm): place by place, the count over [1, high]
# less the count over [1, low - 1].


def count_to(d, n):
    total = 0
    p = 1
    while p <= n:
        above = n // (p * 10)
        digit = n // p % 10
        below = n % p
        if d == 0:
            if above == 0:
                break
            total += (above - 1) * p
        else:
            total += above * p
        if digit > d:
            total += p
        elif digit == d:
            total += below + 1
        p *= 10
    return total


def digits_count(d, low, high):
    return count_to(d, high) - count_to(d, low - 1)


seed = 1067


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        (1, 1, 13),
        (3, 100, 250),
        (0, 1, 10),
        (0, 1, 100),
        (0, 100, 100),
        (7, 77, 77),
        (5, 123456, 654321),
        (0, 1000, 1999),
        (9, 1, 200000000),
        (0, 1, 200000000),
    ]
    for d, low, high in examples:
        print(f"d = {d}, [{low}, {high}] -> {digits_count(d, low, high)}")
    total = 0
    check = 0
    for _ in range(3000):
        d = next_random() % 10
        low = next_random() % 10000 + 1
        high = low + next_random() % 2000
        answer = digits_count(d, low, high)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"3000 ranges below 12000: sum {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(300):
        d = next_random() % 10
        a = (next_random() * 32768 + next_random()) % 200000000 + 1
        b = (next_random() * 32768 + next_random()) % 200000000 + 1
        answer = digits_count(d, min(a, b), max(a, b))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"300 ranges up to 200000000: sum {total}, checksum {check}")
    every = [digits_count(d, 1, 200000000) for d in range(10)]
    print(f"1 to 200000000, each digit: {show(every)}")
    zeros = [digits_count(0, 1, 10**k) for k in range(1, 9)]
    print(f"0 from 1 to each power of ten: {show(zeros)}")
    ones = [digits_count(1, 10 ** (k - 1), 10**k - 1) for k in range(1, 9)]
    print(f"1 over each length of number: {show(ones)}")
    single = [digits_count(d, 199999990, 199999990) for d in range(10)]
    print(f"199999990 alone, each digit: {show(single)}")


main()
