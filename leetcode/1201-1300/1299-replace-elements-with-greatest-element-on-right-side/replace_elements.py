# LeetCode #1299: Replace Elements with Greatest Element on Right Side --
# Python mirror of the ★ arm (one walk from the right end, each place given
# the greatest seen so far).


def replace_elements(arr):
    n = len(arr)
    out = [-1] * n
    greatest = -1
    for i in range(n - 1, -1, -1):
        out[i] = greatest
        if arr[i] > greatest:
            greatest = arr[i]
    return out


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return ",".join(str(x) for x in v)


def main():
    global seed
    print(f"{show(replace_elements([17, 18, 5, 4, 6, 1]))} {show(replace_elements([400]))}")
    print(f"{show(replace_elements([1, 2, 3, 4]))} {show(replace_elements([4, 3, 2, 1]))} {show(replace_elements([7, 7, 7]))} {show(replace_elements([9, 1, 2]))} {show(replace_elements([1, 2, 9]))}")
    seed = 1299
    total = 0
    check = 0
    for i in range(3001):
        n = 1 + next_random() % 300 if i < 3000 else 3000
        top = 10 if i % 3 == 0 else 1000 if i % 3 == 1 else 100000
        arr = []
        for _ in range(n):
            hi = next_random()
            arr.append(1 + (hi * 32768 + next_random()) % top)
        for x in replace_elements(arr):
            total += x
            check = (check * 131 + x + 1) % 1000000007
    print(f"3001 random arrays: sum of answers {total}, checksum {check}")


main()
