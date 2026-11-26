def kids_with_candies(candies, extra_candies):
    most = max(candies)
    return [c + extra_candies >= most for c in candies]


def main():
    seed = 1431
    pool = []
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(1 + seed // 65536 % 100)
    check = 0
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % 999901
        seed = (seed * 1103515245 + 12345) % 2147483648
        extra = 1 + seed // 65536 % 50
        bits = 0
        for j, b in enumerate(kids_with_candies(pool[start:start + 100], extra)):
            if b:
                bits += j + 1
        check = (check * 131 + bits) % 1000000007
    print(f"10^6 windows of 100 kids: checksum {check}")


main()
