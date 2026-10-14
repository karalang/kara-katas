# Benchmark for #561: Python mirror of the ★ arm (sort, then every other
# number); see array_partition.kara.


def array_pair_sum(nums):
    nums.sort()
    return sum(nums[0::2])


# ---- benchmark --------------------------------------------------------------

def main():
    count = 100
    n = 20000
    rounds = 50
    seed = 561

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(count):
        arrays.append([step() % 20001 - 10000 for _ in range(n)])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            s = array_pair_sum(list(arrays[(rnd * 7 + g) % count]))
            total += s
            checksum = (checksum * 31 + s + 1000000000) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: total {total}, checksum {checksum}")


main()
