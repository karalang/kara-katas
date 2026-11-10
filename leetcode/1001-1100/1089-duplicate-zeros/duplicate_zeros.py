# LeetCode #1089: Duplicate Zeros -- mirrors duplicate_zeros.kara: count the
# zeros, then walk back from the end, writing each digit at its place shifted
# by the zeros up to it, and a 0 before it when it is a 0.


def duplicate_zeros(arr):
    n = len(arr)
    zeros = sum(1 for x in arr if x == 0)
    for i in range(n - 1, -1, -1):
        if i + zeros < n:
            arr[i + zeros] = arr[i]
        if arr[i] == 0:
            zeros -= 1
            if i + zeros < n:
                arr[i + zeros] = 0


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr):
    return ", ".join(str(x) for x in arr)


def random_digits(length):
    arr = []
    for _ in range(length):
        r = next_random() % 15
        arr.append(0 if r < 5 else r - 5)
    return arr


def main():
    global seed
    cases = [
        [1, 0, 2, 3, 0, 4, 5, 0],
        [1, 2, 3],
        [0],
        [7],
        [0, 0],
        [1, 0],
        [0, 1, 7],
        [8, 4, 5, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0],
        [9, 9, 0],
        [0, 9, 0, 9, 0, 9],
        [1, 5, 2, 0, 6, 8, 0, 6, 0],
    ]
    for case in cases:
        arr = list(case)
        duplicate_zeros(arr)
        print(f"[{show(case)}] -> [{show(arr)}]")
    seed = 1089
    h = 0
    zeros = 0
    for _ in range(2000):
        length = next_random() % 20 + 1
        arr = random_digits(length)
        duplicate_zeros(arr)
        for x in arr:
            h = (h * 31 + x + 1) % 1000000007
            if x == 0:
                zeros += 1
    print(f"2000 random arrays: {zeros} zeros after, checksum {h}")
    arr = random_digits(10000)
    duplicate_zeros(arr)
    h = 0
    for i, x in enumerate(arr):
        h = (h * 31 + x * (i % 7 + 1)) % 1000000007
    print(f"10000 digits: length {len(arr)}, checksum {h}")


main()
