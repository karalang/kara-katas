# LeetCode #1346 bench in Python: the ★ arm (a set of the values seen so
# far, each new value checked for its double and, when even, its half)
# on the same 2000 arrays of 500 values and 100 passes.


def check_if_exist(arr):
    seen = set()
    for x in arr:
        if 2 * x in seen or (x % 2 == 0 and x // 2 in seen):
            return True
        seen.add(x)
    return False


seed = 1346


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[2 * (next_random() % 1000) - 999 for _ in range(500)] for _ in range(2000)]
    check = 0
    for pass_ in range(100):
        for a in range(2000):
            arr = arrays[a]
            arr[check % 500] = (check // 7) % 2001 - 1000
            yes = check_if_exist(arr)
            check = (check * 31 + (2 if yes else 1) + pass_) % 1000000007
    print(f"100 passes over 2000 arrays of 500: checksum {check}")


main()
