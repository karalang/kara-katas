# LeetCode #2425: Bitwise XOR of All Pairings -- the Python mirror of the
# ★ arm: the XOR of `nums1` when `nums2` has odd length, XORed with that
# of `nums2` when `nums1` has odd length.

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


def random_nums(n, top):
    return [(next_random() * 32768 + next_random()) % (top + 1) for _ in range(n)]


def main():
    print(xor_all_nums([2, 1, 3], [10, 2, 5, 0]))
    print(xor_all_nums([1, 2], [3, 4]))
    print(xor_all_nums([7], [9]))
    print(xor_all_nums([1, 2, 4, 8], [16, 32]))
    print(xor_all_nums([1, 2, 4, 8], [16, 32, 64]))
    print(xor_all_nums([1, 2, 4], [16, 32, 64, 128]))
    print(xor_all_nums([5, 5, 5], [5, 5, 5, 5, 5]))
    a = random_nums(100000, 1000000000)
    b = random_nums(3, 1000000000)
    print(f"{xor_all_nums(a, b)} {xor_all_nums(b, a)}")
    c = random_nums(3000, 1000000000)
    d = random_nums(3001, 1000000000)
    print(f"{xor_all_nums(c, d)} {xor_all_nums(d, c)}")
    check = 0
    total = 0
    for _ in range(3000):
        top = 1 + next_random() % 16 if next_random() % 2 == 0 else 1000000000
        n = 1 + next_random() % 12
        m = 1 + next_random() % 12
        x = random_nums(n, top)
        y = random_nums(m, top)
        a = xor_all_nums(x, y)
        check = (check * 31 + a) % 1000000007
        total += a
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
