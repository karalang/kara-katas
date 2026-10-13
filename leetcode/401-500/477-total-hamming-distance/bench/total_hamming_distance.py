# Benchmark for #477: Python mirror of the ★ arm (one bit at a time);
# see total_hamming_distance.kara.


def total_hamming_distance(nums):
    n = len(nums)
    total = 0
    for bit in range(30):
        ones = 0
        for x in nums:
            ones += (x >> bit) & 1
        total += ones * (n - ones)
    return total


seed = 477


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 10000
    rounds = 5000
    nums = []
    for _ in range(n):
        a = next_random()
        b = next_random()
        nums.append((a * 32768 + b) % 1000000001)
    total = 0
    checksum = 0
    for r in range(rounds):
        a = next_random()
        b = next_random()
        nums[r % n] = (a * 32768 + b) % 1000000001
        got = total_hamming_distance(nums)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{rounds} rounds on {n} numbers: distances add up to {total}, checksum {checksum}")


main()
