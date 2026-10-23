# LeetCode #927: Three Equal Parts -- three pointers (Python mirror).


def three_equal_parts(arr):
    n = len(arr)
    ones = sum(arr)
    if ones == 0:
        return [0, n - 1]
    if ones % 3 != 0:
        return [-1, -1]
    third = ones // 3
    starts = []
    seen = 0
    for k in range(n):
        if arr[k] == 1:
            if seen % third == 0:
                starts.append(k)
            seen += 1
    a, b, c = starts
    while c < n and arr[a] == arr[b] and arr[b] == arr[c]:
        a += 1
        b += 1
        c += 1
    if c == n:
        return [a - 1, b]
    return [-1, -1]


seed = 927


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr):
    got = three_equal_parts(arr)
    print(f"[{','.join(str(v) for v in arr)}]: [{got[0]},{got[1]}]")


def random_case(width, pad):
    w = 1 + next_random() % width
    value = [next_random() % 2 for _ in range(w)]
    arr = []
    for _ in range(3):
        zeros = next_random() % (pad + 1)
        arr.extend([0] * zeros)
        arr.extend(value)
    if next_random() % 2 == 0:
        at = next_random() % len(arr)
        arr[at] = 1 - arr[at]
    return arr


def main():
    show([1, 0, 1, 0, 1])
    show([1, 1, 0, 1, 1])
    show([1, 1, 0, 0, 1])
    show([0, 0, 0, 0])
    show([1, 0, 1, 1, 1])
    show([0, 1, 0, 0, 1, 0, 0, 0, 1, 0])
    show([1, 0, 1, 1, 0, 0])
    show([1, 1, 1])
    show([0, 1, 1, 0, 1, 1, 0, 0, 1, 1])
    found = 0
    check = 0
    for _ in range(300):
        got = three_equal_parts(random_case(300, 100))
        if got[0] >= 0:
            found += 1
        check = (check * 1000003 + got[0] + 1) % 1000000007
        check = (check * 1000003 + got[1] + 1) % 1000000007
    print(f"300 random arrays: {found} split, checksum {check}")
    a = three_equal_parts([0] * 30000)
    b = three_equal_parts([1] * 30000)
    c = three_equal_parts([1 if k >= 3 and k % 3 == 0 else 0 for k in range(30000)])
    print(f"30000 digits: all 0s [{a[0]},{a[1]}], all 1s [{b[0]},{b[1]}], 100 repeated [{c[0]},{c[1]}]")


main()
