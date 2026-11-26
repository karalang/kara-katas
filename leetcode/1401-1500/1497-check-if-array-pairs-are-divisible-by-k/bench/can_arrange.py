# LeetCode #1497: Check If Array Pairs Are Divisible by k -- the bench in
# Python, mirroring can_arrange.kara: each value's remainder by k counted.


def can_arrange(arr, k):
    count = [0] * k
    for x in arr:
        count[x % k] += 1
    if count[0] % 2 != 0:
        return False
    for r in range(1, k):
        if count[r] != count[k - r]:
            return False
    return True


def main():
    seed = 1497
    arr = []
    for _ in range(50000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = seed // 65536 * 30011 % 2000000001 - 1000000000
        arr.append(x)
        arr.append(1000 * (seed % 7) - x)
    check = 0
    for call in range(1000):
        k = 1000 if call % 2 == 0 else 1 + (check + call) % 100000
        at = (check * 7 + call) % 100000
        arr[at] += 1000 if call % 4 < 2 else -1000
        yes = can_arrange(arr, k)
        check = (check * 31 + k + (2 if yes else 1)) % 1000000007
    print(f"1000 calls over 100000 values: checksum {check}")


main()
