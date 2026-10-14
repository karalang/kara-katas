# Benchmark for #560: Python mirror of the ★ arm (prefix sums in a dict);
# see subarray_sum.kara.


def subarray_sum(nums, k):
    seen = {0: 1}
    total = 0
    count = 0
    for x in nums:
        total += x
        count += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return count


# ---- benchmark --------------------------------------------------------------

def main():
    count = 100
    n = 20000
    rounds = 20
    seed = 560

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(count):
        arrays.append([step() % 2001 - 1000 for _ in range(n)])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            k = step() % 2001 - 1000
            c = subarray_sum(arrays[(rnd * 7 + g) % count], k)
            total += c
            checksum = (checksum * 31 + c) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: {total} subarrays, checksum {checksum}")


main()
