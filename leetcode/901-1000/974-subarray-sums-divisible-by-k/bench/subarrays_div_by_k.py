# Benchmark: LeetCode #974 Subarray Sums Divisible by K -- the ★ arm,
# counts of prefix remainders, on 20 arrays of 30000 random numbers.
# Mirrors subarrays_div_by_k.kara, .rs, .c and go-seq/.


def subarrays_div_by_k(nums, k):
    count = [0] * k
    count[0] = 1
    s = total = 0
    for x in nums:
        s += x
        r = (s % k + k) % k
        total += count[r]
        count[r] += 1
    return total


seed = 974


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count = 200, 20
    cases = []
    for _ in range(count):
        nums = [next_random() % 20001 - 10000 for _ in range(30000)]
        k = 2 + next_random() % 9999
        cases.append((nums, k))
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            nums, k = cases[(r + i) % count]
            got = subarrays_div_by_k(nums, k)
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"{rounds} rounds over {count} arrays of 30000 numbers: "
          f"{total} subarrays, checksum {check}")


main()
