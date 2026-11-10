# LeetCode #2110: Number of Smooth Descent Periods of a Stock -- Python
# mirror of descent.kara: the descent run's length up to each day, summed.
# O(n).


def get_descent_periods(prices):
    run = 1
    total = 1
    for i in range(1, len(prices)):
        if prices[i - 1] - prices[i] == 1:
            run += 1
        else:
            run = 1
        total += run
    return total


seed = 2110


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [[3, 2, 1, 4], [8, 6, 7, 7], [1], [5, 4, 3, 2, 1], [1, 2, 3], [3, 2, 2, 1]]
    for prices in examples:
        print(f"{show(prices)} -> {get_descent_periods(prices)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 40 + 1
        prices = [next_random() % 5 + 1 for _ in range(n)]
        got = get_descent_periods(prices)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 arrays: {total} periods, checksum {check}")
    falling = [100000 - i for i in range(100000)]
    saw = [1000 - i % 1000 for i in range(100000)]
    print(f"one descent -> {get_descent_periods(falling)}")
    print(f"a saw of 1000s -> {get_descent_periods(saw)}")


main()
