# Benchmark: LeetCode #941 Valid Mountain Array -- the ★ arm, a walk up
# and a walk down, on 100 arrays of 10000 values, LeetCode's longest, in
# 200 rounds. Mirrors valid_mountain_array.kara, .c, .rs and go-seq/.


def valid_mountain_array(arr):
    n = len(arr)
    i = 0
    while i + 1 < n and arr[i] < arr[i + 1]:
        i += 1
    if i == 0 or i == n - 1:
        return False
    while i + 1 < n and arr[i] > arr[i + 1]:
        i += 1
    return i == n - 1


seed = 941


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 200
    count = 100
    arrays = []
    for a in range(count):
        top = 1 + next_random() % 9998
        least = 0 if top < 10000 - top else 2 * top - 9999
        arr = [(i if i <= top else 2 * top - i) - least for i in range(10000)]
        if a % 2 == 1:
            hi = next_random()
            j = (hi * 32768 + next_random()) % 10000
            arr[j] = next_random() % 10001
        arrays.append(arr)
    mountains = check = 0
    for r in range(rounds):
        for i in range(count):
            c = (r + i) % count
            if valid_mountain_array(arrays[c]):
                mountains += 1
                check = (check * 1000003 + c + 1) % 1000000007
    print(f"{rounds} rounds over {count} arrays of 10000 values: {mountains} mountains, checksum {check}")


main()
