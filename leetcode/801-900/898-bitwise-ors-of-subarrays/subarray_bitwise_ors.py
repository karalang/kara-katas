# LeetCode #898: Bitwise ORs of Subarrays -- Python mirror of the
# ORs-ending-at-each-place solution in subarray_bitwise_ors.kara, with the
# same test harness.
#
# The ORs of the subarrays ending at i are the ORs ending at i - 1, each
# with arr[i] put in, and arr[i] alone. Extending a subarray to the left
# only ever adds bits, so there are at most 31 different ones (one more
# for each bit added). Keep that set from place to place and gather
# every one of them. O(n * 31).


def subarray_bitwise_ors(arr):
    every = set()
    ending = set()
    for x in arr:
        nxt = {x}
        for y in ending:
            nxt.add(y | x)
        every |= nxt
        ending = nxt
    return len(every)


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr):
    print(f"arr = [{', '.join(str(x) for x in arr)}] -> {subarray_bitwise_ors(arr)}")


# `len` random numbers below 2^bits; with `sparse`, each is AND-ed with a
# second one, so it has about a quarter of the bits rather than half
def random_case(length, bits, sparse):
    mask = (1 << bits) - 1
    arr = []
    for _ in range(length):
        v = next_random() * 32768
        v = (v + next_random()) & mask
        if sparse:
            w = next_random() * 32768
            v = v & (w + next_random())
        arr.append(v)
    return arr


def main():
    global seed
    show([0])
    show([1, 1, 2])
    show([1, 2, 4])
    show([0, 0, 0])
    show([7, 7, 7, 7])
    show([1, 2, 4, 8, 16, 32, 64, 128])
    show([3, 5, 6, 0, 1])
    show([1000000000, 0, 999999999, 536870912])
    # random cases of up to 1000 numbers, a third of them up to 8, below
    # 2^1 to 2^30, half of them sparse
    seed = 898
    total = 0
    check = 0
    for c in range(300):
        length = 1 + next_random() % 8 if c % 3 == 0 else 1 + next_random() % 1000
        bits = 1 + next_random() % 30
        got = subarray_bitwise_ors(random_case(length, bits, c % 2 == 0))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"300 cases of up to 1000 numbers: {total} ORs in all, checksum {check}")
    # LeetCode's largest: 50000 numbers up to 10^9, and 50000 below 2^12
    big = []
    for _ in range(50000):
        v = next_random() * 32768
        big.append((v + next_random()) % 1000000001)
    print(f"50000 numbers up to 10^9 -> {subarray_bitwise_ors(big)}")
    print(f"50000 sparse numbers below 2^12 -> {subarray_bitwise_ors(random_case(50000, 12, True))}")


main()
