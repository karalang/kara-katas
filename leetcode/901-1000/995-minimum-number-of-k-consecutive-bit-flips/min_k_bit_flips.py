# LeetCode #995: Minimum Number of K Consecutive Bit Flips -- mirror of
# the ★ arm (min_k_bit_flips.kara), the greedy with a running parity.


def min_k_bit_flips(nums, k):
    n = len(nums)
    ends = [False] * (n + 1)
    flipped = False
    flips = 0
    for i in range(n):
        if ends[i]:
            flipped = not flipped
        if (nums[i] == 1) == flipped:
            if i + k > n:
                return -1
            flips += 1
            flipped = not flipped
            ends[i + k] = True
    return flips


seed = 995


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([0, 1, 0], 1),
        ([1, 1, 0], 2),
        ([0, 0, 0, 1, 0, 1, 1, 0], 3),
        ([1], 1),
        ([0], 1),
        ([0, 0], 2),
        ([0, 1, 0], 2),
        ([1, 0, 1], 3),
        ([1, 1, 1, 1], 3),
        ([0, 0, 1, 1, 0, 0], 2),
    ]
    for nums, k in cases:
        text = "[" + ",".join(str(b) for b in nums) + "]"
        print(f"nums = {text}, k = {k} -> {min_k_bit_flips(nums, k)}")
    zeros = [0] * 100000
    print(f"100000 zeros, k = 1: {min_k_bit_flips(zeros, 1)}")
    print(f"100000 zeros, k = 100000: {min_k_bit_flips(zeros, 100000)}")
    print(f"100000 zeros, k = 3: {min_k_bit_flips(zeros, 3)}")
    print(f"100000 zeros, k = 4: {min_k_bit_flips(zeros, 4)}")
    alternate = [i % 2 for i in range(100000)]
    print(f"0 and 1 in turn, 100000 bits, k = 2: {min_k_bit_flips(alternate, 2)}")
    print(f"0 and 1 in turn, 100000 bits, k = 50000: {min_k_bit_flips(alternate, 50000)}")
    # random arrays, half of them all ones put through random flips, so
    # that they can be made all ones again
    for count, most in ((300, 8), (3000, 60), (300, 1000), (3, 100000)):
        bits = 0
        stuck = 0
        total = 0
        check = 0
        for _ in range(count):
            n = most if most == 100000 else 1 + next_random() % most
            k = 1 + next_random() % min(n, 20)
            if next_random() % 2 == 0:
                nums = [next_random() % 2 for _ in range(n)]
            else:
                nums = [1] * n
                for i in range(n - k + 1):
                    if next_random() % 4 == 0:
                        for j in range(i, i + k):
                            nums[j] = 1 - nums[j]
            bits += n
            got = min_k_bit_flips(nums, k)
            if got < 0:
                stuck += 1
            else:
                total += got
            check = (check * 31 + got + 2) % 1000000007
        print(f"{count} random arrays of {bits} bits: {stuck} impossible, {total} flips, checksum {check}")

main()
