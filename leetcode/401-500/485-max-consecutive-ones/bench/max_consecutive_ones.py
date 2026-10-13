# Benchmark for #485: Python mirror of the ★ arm (a running count); see
# max_consecutive_ones.kara.


def find_max_consecutive_ones(nums):
    best = 0
    run = 0
    for x in nums:
        if x == 1:
            run += 1
            if run > best:
                best = run
        else:
            run = 0
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    arrays = []
    seed = [485]
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
