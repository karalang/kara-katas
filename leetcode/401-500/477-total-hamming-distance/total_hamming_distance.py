# LeetCode #477: Total Hamming Distance -- Python mirror of the ★ arm
# (total_hamming_distance.kara): one bit at a time, k x (n - k).


def total_hamming_distance(nums):
    n = len(nums)
    total = 0
    for bit in range(30):
        ones = 0
        for x in nums:
            ones += (x >> bit) & 1
        total += ones * (n - ones)
    return total


def show(nums):
    a = ", ".join(str(x) for x in nums)
    print(f"[{a}] -> {total_hamming_distance(nums)}")


seed = 477


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([4, 14, 2])
    show([4, 14, 4])
    show([0])
    show([7, 7, 7])
    show([0, 1000000000])
    show(list(range(16)))
    show([1073741823, 0, 1073741823, 0])
    count = 300
    total = 0
    checksum = 0
    for c in range(count):
        span = 16 if c % 3 == 2 else 1000000001
        nums = []
        for _ in range(1 + next_random() % 40):
            nums.append((next_random() * 32768 + next_random()) % span)
        got = total_hamming_distance(nums)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} random lists: distances add up to {total}, checksum {checksum}")


main()
