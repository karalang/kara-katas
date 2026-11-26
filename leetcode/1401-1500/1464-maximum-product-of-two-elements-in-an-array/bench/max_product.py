# LeetCode #1464 bench in Python: the ★ arm (one pass keeping the two
# largest values) on the same 1000 arrays of 500 values and 100 passes.


def max_product(nums):
    first = 0
    second = 0
    for x in nums:
        if x > first:
            second = first
            first = x
        elif x > second:
            second = x
    return (first - 1) * (second - 1)


seed = 1464


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[1 + next_random() % 1000 for _ in range(500)] for _ in range(1000)]
    check = 0
    for pass_ in range(100):
        for p in range(1000):
            k = check % 500
            arrays[p][k] = 1 + (check // 7) % 1000
            got = max_product(arrays[p])
            check = (check * 31 + got + pass_) % 1000000007
    print(f"100 passes over 1000 arrays of 500 values: checksum {check}")


main()
