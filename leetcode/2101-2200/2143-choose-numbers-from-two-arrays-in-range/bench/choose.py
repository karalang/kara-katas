# LeetCode #2143: Choose Numbers From Two Arrays in Range -- the
# benchmark, the same algorithm as choose.kara.

MOD = 1000000007
seed = 2143


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_subranges(nums1, nums2):
    low = sum(nums2)
    high = sum(nums1)
    width = low + high + 1
    ways = [0] * width
    balanced = 0
    for i in range(len(nums1)):
        ways[low] += 1
        nxt = [0] * width
        a = nums1[i]
        b = nums2[i]
        for d in range(width):
            if ways[d] > 0:
                nxt[d + a] = (nxt[d + a] + ways[d]) % MOD
                nxt[d - b] = (nxt[d - b] + ways[d]) % MOD
        ways = nxt
        balanced = (balanced + ways[low]) % MOD
    return balanced


def main():
    firsts = []
    seconds = []
    for _ in range(4):
        firsts.append([next_random() % 101 for _ in range(100)])
        seconds.append([next_random() % 101 for _ in range(100)])
    total = check = 0
    for rnd in range(50):
        for p in range(4):
            at = next_random() % 100
            firsts[p][at] = next_random() % 101
            seconds[p][at] = next_random() % 101
            ways = count_subranges(firsts[p], seconds[p])
            total += ways
            check = (check * 31 + ways + rnd) % 1000000007
    print(f"200 solves: {total} ranges in all, checksum {check}")


main()
