# LeetCode #1835: Find XOR Sum of All Pairs Bitwise AND -- the bench in Python: the ★ arm over
# 3000 calls on pairs of 20 lists of 10^5 numbers from 0 to 10^9, built
# once, each call's two lists drawn from the checksum so far. The arm
# borrows both lists, so no call copies one.


def get_xor_sum(arr1, arr2):
    left = 0
    for a in arr1:
        left ^= a
    right = 0
    for b in arr2:
        right ^= b
    return left & right


def main():
    seed = 1835

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    lists = []
    for _ in range(20):
        lst = []
        for _ in range(100000):
            hi = next_random()
            lst.append((hi * 32768 + next_random()) % 1000000001)
        lists.append(lst)
    check = 0
    for call in range(3000):
        i = (check + call) % 20
        j = (check // 20 + call * 7) % 20
        check = (check * 31 + get_xor_sum(lists[i], lists[j])) % 1000000007
    print(f"3000 calls: checksum {check}")


main()
