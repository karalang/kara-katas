# LeetCode #2859: Sum of Values at Indices With K Set Bits -- the ★
# arm's mirror: the values at the indices with exactly k set bits.


def sum_indices_with_k_set_bits(nums, k):
    return sum(x for i, x in enumerate(nums) if bin(i).count("1") == k)


seed = 2859


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(f"{sum_indices_with_k_set_bits([5, 10, 1, 5, 2], 1)} {sum_indices_with_k_set_bits([4, 3, 2, 1], 2)}")
    full = [100000] * 1000
    print("[" + ", ".join(str(sum_indices_with_k_set_bits(full, k)) for k in range(11)) + "]")
    total = check = 0
    for c in range(3300):
        small = c < 3000
        n = next_random() % 20 + 1 if small else next_random() % 1000 + 1
        top = 10 if small else 100000
        k = next_random() % 6 if small else next_random() % 11
        nums = [wide() % top + 1 for _ in range(n)]
        s = sum_indices_with_k_set_bits(nums, k)
        total += s
        check = (check * 31 + s) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: sums total {total}, checksum {check}")
            total = check = 0
    print(f"300 long arrays: sums total {total}, checksum {check}")


main()
