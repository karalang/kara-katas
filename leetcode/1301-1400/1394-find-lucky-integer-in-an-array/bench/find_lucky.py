# LeetCode #1394 bench, Python mirror of the ★ arm.


def find_lucky(arr):
    count = [0] * 501
    for x in arr:
        count[x] += 1
    for x in range(500, 0, -1):
        if count[x] == x:
            return x
    return -1


seed = 1394


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    n = 500
    arr = [1 + next_random() % 40 for _ in range(n)]
    check = 0
    for _ in range(600000):
        seed = (seed + check) % 2147483648
        i = next_random() % n
        arr[i] = 1 + next_random() % 40
        check = (check * 131 + find_lucky(arr) + 1) % 1000000007
    print(f"600000 rounds over 500 values: checksum {check}")


main()
