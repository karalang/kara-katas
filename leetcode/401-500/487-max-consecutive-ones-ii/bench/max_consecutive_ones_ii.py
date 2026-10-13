# Benchmark for #487: Python mirror of the ★ arm (the run before the
# last 0); see max_consecutive_ones_ii.kara.


def find_max_consecutive_ones(nums):
    best = 0
    before = 0
    run = 0
    for x in nums:
        if x == 1:
            run += 1
        else:
            before = run + 1
            run = 0
        if before + run > best:
            best = before + run
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    arrays = []
    seed = [487]
    for a in range(20):
        arrays.append([1 if next_random(seed) % 100 < 80 + a else 0 for _ in range(100000)])
    total = 0
    checksum = 0
    for _ in range(50):
        for nums in arrays:
            best = find_max_consecutive_ones(nums)
            total += best
            checksum = (checksum * 31 + best) % 1000000007
    print(f"1000 scans of 100000 numbers: runs add up to {total}, checksum {checksum}")


main()
