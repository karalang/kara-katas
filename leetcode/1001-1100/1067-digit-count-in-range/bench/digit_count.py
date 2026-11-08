# LeetCode #1067: Digit Count in Range -- the benchmark's Python mirror of
# digit_count.kara: the same place by place count over a million queries.


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


def main():
    seed = 1067

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    queries = []
    for _ in range(1000000):
        d = next_random() % 10
        a = (next_random() * 32768 + next_random()) % 200000000 + 1
        b = (next_random() * 32768 + next_random()) % 200000000 + 1
        queries.append((d, min(a, b), max(a, b)))
    calls = 0
    total = 0
    check = 0
    for d, low, high in queries:
        answer = digits_count(d, low, high)
        total += answer
        check = (check * 31 + answer) % 1000000007
        calls += 1
    print(f"{calls} calls: answers sum {total}, checksum {check}")


main()
