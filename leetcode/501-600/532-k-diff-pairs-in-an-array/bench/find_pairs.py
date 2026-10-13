# Benchmark for #532: Python mirror of the ★ arm (count each number); see
# find_pairs.kara.


def find_pairs(nums, k):
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    pairs = 0
    for v, c in counts.items():
        if k == 0:
            if c >= 2:
                pairs += 1
        elif v + k in counts:
            pairs += 1
    return pairs


def main():
    # 20 arrays of 10,000 numbers made once, the a-th drawn from
    # -1,000(a + 1) to 1,000(a + 1); then each array is answered for 200
    # values of k from 0 to 19.
    seed = 532
    arrays = []
    for a in range(20):
        half = 1000 * (a + 1)
        nums = []
        for _ in range(10000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append(seed // 65536 % (2 * half + 1) - half)
        arrays.append(nums)
    total = checksum = 0
    for _ in range(200):
        for a in range(len(arrays)):
            seed = (seed * 1103515245 + 12345) % 2147483648
            answer = find_pairs(arrays[a], seed // 65536 % 20)
            total += answer
            checksum = (checksum * 31 + answer) % 1000000007
    print(f"20 arrays of 10000, 200 values of k each: total {total}, checksum {checksum}")


main()
