# LeetCode #2425: Bitwise XOR of All Pairings -- the bench, the ★ arm: the
# XOR of `nums1` when `nums2` has odd length, XORed with that of `nums2`
# when `nums1` has odd length.

seed = 2425


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def xor_all_nums(nums1, nums2):
    answer = 0
    if len(nums2) % 2 == 1:
        for x in nums1:
            answer ^= x
    if len(nums1) % 2 == 1:
        for y in nums2:
            answer ^= y
    return answer


def main():
    firsts = []
    seconds = []
    for i in range(10):
        for which, n in ((0, 100000 - i), (1, 100000 - i // 2 - 1)):
            nums = []
            for _ in range(n):
                a = next_random()
                nums.append((a * 32768 + next_random()) % 1000000001)
            (firsts if which == 0 else seconds).append(nums)
    check = 0
    for p in range(500):
        for i in range(10):
            at = (p * 7919) % len(firsts[i])
            firsts[i][at] ^= p % 1024
            check = (check * 31 + xor_all_nums(firsts[i], seconds[i]) + p) % 1000000007
    print(f"500 passes over 10 pairs of 10^5 values: checksum {check}")


main()
