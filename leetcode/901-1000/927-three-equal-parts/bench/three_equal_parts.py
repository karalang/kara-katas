# LeetCode #927: Three Equal Parts -- bench: three pointers.
# Mirrors three_equal_parts.kara.


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


def main():
    rounds, count = 30, 100
    # count arrays of 30000 digits, built once: a value of 9000 digits
    # written three times, each copy after up to 1000 leading 0s and the
    # array filled up with 0s in front, and every other array with one
    # digit flipped
    arrays = []
    for a in range(count):
        value = [next_random() % 2 for _ in range(9000)]
        parts = []
        for _ in range(3):
            parts.extend([0] * (next_random() % 1001))
            parts.extend(value)
        arr = [0] * (30000 - len(parts)) + parts
        if a % 2 == 1:
            at = next_random() % 30000
            arr[at] = 1 - arr[at]
        arrays.append(arr)
    found = 0
    check = 0
    for r in range(rounds):
        # each round visits every array, starting from a different one
        for i in range(count):
            got = three_equal_parts(arrays[(r + i) % count])
            if got[0] >= 0:
                found += 1
            check = (check * 1000003 + got[0] + 1) % 1000000007
            check = (check * 1000003 + got[1] + 1) % 1000000007
    print(f"{rounds} rounds over {count} arrays of 30000: {found} split, checksum {check}")


main()
