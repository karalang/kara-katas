# LeetCode #905: Sort Array By Parity -- bench program, Python.
#
# The two pointers from both ends, over 1,000,000 numbers below 5001 built
# once. Each round sorts a copy by parity, folds the evens in front and
# one number of the answer into a checksum and changes one number.


def sort_array_by_parity(nums):
    out = nums
    i = 0
    j = len(out) - 1
    while i < j:
        if out[i] % 2 == 0:
            i += 1
        elif out[j] % 2 == 1:
            j -= 1
        else:
            out[i], out[j] = out[j], out[i]
            i += 1
            j -= 1
    return out


seed = 905


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 1000000
    rounds = 100
    nums = [next_random() % 5001 for _ in range(n)]
    check = 0
    total = 0
    for r in range(rounds):
        out = sort_array_by_parity(list(nums))
        lead = 0
        while out[lead] % 2 == 0:
            lead += 1
        total += lead
        check = (check * 31 + lead) % 1000000007
        check = (check * 31 + out[r * 7919 % n]) % 1000000007
        nums[r * 7919 % n] = next_random() % 5001
    print(f"{rounds} rounds over {n} numbers: {total} evens in front, checksum {check}")


main()
