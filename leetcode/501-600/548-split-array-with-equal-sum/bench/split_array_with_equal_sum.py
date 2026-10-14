# Benchmark for #548: Python mirror of the ★ arm (a set of left sums per
# middle cut); see split_array_with_equal_sum.kara.


def split_array(nums):
    n = len(nums)
    if n < 7:
        return False
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    for j in range(3, n - 3):
        sums = set()
        for i in range(1, j - 1):
            if prefix[i] == prefix[j] - prefix[i + 1]:
                sums.add(prefix[i])
        for k in range(j + 2, n - 1):
            third = prefix[k] - prefix[j + 1]
            if third == prefix[n] - prefix[k + 1] and third in sums:
                return True
    return False


seed = 548


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n = 10, 2000
    all_a = []
    for g in range(count):
        spread = 1 + g % 5 * 25
        all_a.append([next_random() % (2 * spread + 1) - spread for _ in range(n)])
    yes = checksum = 0
    for rnd in range(20):
        for g in range(count):
            a = all_a[g]
            i = (rnd * 31 + g * 7) % n
            a[i] = 0 - a[i]
            bit = 1 if split_array(a) else 0
            yes += bit
            checksum = (checksum * 31 + bit + 7 * g) % 1000000007
    print(f"{count} arrays, 20 rounds each: {yes} can be split, checksum {checksum}")


main()
