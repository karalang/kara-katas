# LeetCode #870: Advantage Shuffle -- Python mirror of the bench program
# (the ★ arm, greedy from the largest).


def advantage_count(nums1, nums2):
    n = len(nums1)
    srt = sorted(nums1)
    order = sorted(range(n), key=lambda i: -nums2[i])
    result = [0] * n
    lo, hi = 0, n - 1
    for i in order:
        if srt[hi] > nums2[i]:
            result[i] = srt[hi]
            hi -= 1
        else:
            result[i] = srt[lo]
            lo += 1
    return result


seed = 870


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_vec(n):
    v = []
    for _ in range(n):
        hi = next_random()
        lo = next_random()
        v.append((hi * 32768 + lo) % 1000000001)
    return v


def main():
    wins = 0
    check = 0
    for _ in range(20):
        nums1 = random_vec(100000)
        nums2 = random_vec(100000)
        result = advantage_count(nums1, nums2)
        for i in range(len(result)):
            if result[i] > nums2[i]:
                wins += 1
            check = (check + result[i] * (i + 1)) % 1000000007
    print(f"20 pairs of 100000 values: {wins} wins, checksum {check}")


main()
