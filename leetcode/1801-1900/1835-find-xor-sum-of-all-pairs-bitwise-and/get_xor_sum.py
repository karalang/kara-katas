# LeetCode #1835: Find XOR Sum of All Pairs Bitwise AND -- the ★ arm in
# Python


def get_xor_sum(arr1, arr2):
    left = 0
    for a in arr1:
        left ^= a
    right = 0
    for b in arr2:
        right ^= b
    return left & right


seed = 1835


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{get_xor_sum([1, 2, 3], [6, 5])} {get_xor_sum([12], [4])}")
    print(f"{get_xor_sum([7], [5])} {get_xor_sum([0], [1000000000])} {get_xor_sum([1000000000, 999999999], [1000000000])} {get_xor_sum([9, 9], [1, 2, 3])} {get_xor_sum([1, 4, 16], [2, 8, 32])} {get_xor_sum([3, 5, 6, 10], [3, 5, 6, 10])}")
    first = [(next_random() * 32768 + next_random()) % 1000000001 for _ in range(100000)]
    second = [(next_random() * 32768 + next_random()) % 1000000001 for _ in range(100000)]
    print(f"the most: {get_xor_sum(first, second)} {get_xor_sum(first, [1000000000])}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 8
        arr1 = [next_random() % 64 for _ in range(n)]
        m = 1 + next_random() % 8
        arr2 = [next_random() % 64 for _ in range(m)]
        check = (check * 31 + get_xor_sum(arr1, arr2)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
