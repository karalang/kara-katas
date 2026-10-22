# LeetCode #845: Longest Mountain in Array -- Python mirror of the ★ arm and its harness.


def longest_mountain(arr):
    best = 0
    up = 0
    down = 0
    for i in range(1, len(arr)):
        if (down > 0 and arr[i - 1] < arr[i]) or arr[i - 1] == arr[i]:
            up = 0
            down = 0
        if arr[i - 1] < arr[i]:
            up += 1
        elif arr[i - 1] > arr[i]:
            down += 1
        if up > 0 and down > 0:
            best = max(best, up + down + 1)
    return best


def show(arr):
    print(f"[{', '.join(map(str, arr))}] -> {longest_mountain(arr)}")


seed = 845


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for arr in [[2, 1, 4, 7, 3, 2, 5], [2, 2, 2], [0], [0, 1], [1, 2, 3], [3, 2, 1], [1, 3, 2],
                [0, 1, 0, 1, 0], [1, 2, 2, 1], [1, 2, 3, 2, 1, 2, 3, 4, 3],
                [2, 1, 2, 3, 4, 3, 3, 2, 1], [0, 10000, 0],
                [1, 2, 1, 2, 3, 2, 1, 1, 2, 3, 4, 5, 4]]:
        show(arr)
    one = [i if i < 5000 else 10000 - i for i in range(10000)]
    print(f"one mountain of 10000: {longest_mountain(one)}")
    zigzag = [i % 2 for i in range(10000)]
    print(f"zigzag of 10000: {longest_mountain(zigzag)}")
    print(f"10000 equal values: {longest_mountain([10000] * 10000)}")
    long = [next_random() % 10001 for _ in range(10000)]
    print(f"10000 random values: {longest_mountain(long)}")
    total = 0
    check = 0
    for _ in range(500):
        n = 1 + next_random() % 40
        top = 1 + next_random() % 6
        arr = [next_random() % top for _ in range(n)]
        m = longest_mountain(arr)
        total += m
        check = (check * 31 + m) % 1000000007
    print(f"500 random arrays: lengths sum to {total}, checksum {check}")


main()
