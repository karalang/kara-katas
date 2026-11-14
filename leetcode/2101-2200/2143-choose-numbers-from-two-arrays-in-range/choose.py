# LeetCode #2143: Choose Numbers From Two Arrays in Range -- the Python
# mirror of choose.kara's ★ arm.

MOD = 1000000007


def count_subranges(nums1, nums2):
    low = sum(nums2)
    high = sum(nums1)
    width = low + high + 1
    ways = [0] * width
    balanced = 0
    for i in range(len(nums1)):
        ways[low] += 1
        nxt = [0] * width
        for d in range(width):
            if ways[d] > 0:
                nxt[d + nums1[i]] = (nxt[d + nums1[i]] + ways[d]) % MOD
                nxt[d - nums2[i]] = (nxt[d - nums2[i]] + ways[d]) % MOD
        ways = nxt
        balanced = (balanced + ways[low]) % MOD
    return balanced


seed = 2143


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums1, nums2):
    a = ", ".join(map(str, nums1))
    b = ", ".join(map(str, nums2))
    print(f"[{a}] [{b}] -> {count_subranges(nums1, nums2)}")


def main():
    show([1, 2, 5], [2, 6, 3])
    show([0, 1], [1, 0])
    show([0], [0])
    show([5], [5])
    show([3, 3], [3, 3])
    show([1, 1, 1, 1], [1, 1, 1, 1])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        top = [10, 3, 101][rnd % 3]
        nums1 = [next_random() % top for _ in range(n)]
        nums2 = [next_random() % top for _ in range(n)]
        ways = count_subranges(nums1, nums2)
        total += ways
        check = (check * 31 + ways + n) % 1000000007
    print(f"2000 pairs: {total} ranges in all, checksum {check}")
    zeros = [0] * 100
    full = [100] * 100
    random1 = [next_random() % 101 for _ in range(100)]
    random2 = [next_random() % 101 for _ in range(100)]
    x = count_subranges(zeros, zeros)
    y = count_subranges(full, full)
    z = count_subranges(random1, random2)
    print(f"100 pairs: {x} all 0, {y} all 100, {z} at random")


main()
