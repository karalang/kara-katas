# LeetCode #1287 bench, in Python: the ★ arm (the first i where arr[i]
# equals arr[i + n // 4]) on 100 sorted arrays of 10^5 numbers, built once,
# 1000 rounds, every answer folded into a checksum.


def find_special_integer(arr):
    quarter = len(arr) // 4
    for i in range(len(arr) - quarter):
        if arr[i] == arr[i + quarter]:
            return arr[i]
    return -1


seed = 1287


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def problem(n):
    planted = next_random() % 100001
    times = n // 4 + 1 + next_random() % (n // 4)
    arr = [planted] * times
    while len(arr) < n:
        x = next_random() % 100001
        if x != planted:
            arr.append(x)
    arr.sort()
    return arr


def main():
    problems = [problem(100000) for _ in range(100)]
    check = 0
    for rnd in range(1000):
        for arr in problems:
            check = (check * 131 + find_special_integer(arr) + rnd) % 1000000007
    print(f"1000 rounds of 100 arrays of 100000 numbers: checksum {check}")


if __name__ == "__main__":
    main()
