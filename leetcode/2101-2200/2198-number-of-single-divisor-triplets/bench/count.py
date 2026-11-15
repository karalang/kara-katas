# benchmark's Python mirror of count.kara (LeetCode #2198, the ★ arm):
# every ordered triple of the values held.


def single_divisor_triplet(nums):
    count = [0] * 101
    for x in nums:
        count[x] += 1
    total = 0
    for a in range(1, 101):
        if count[a] == 0:
            continue
        for b in range(1, 101):
            if count[b] == 0:
                continue
            for c in range(1, 101):
                if count[c] == 0:
                    continue
                s = a + b + c
                by_a = s % a == 0
                by_b = s % b == 0
                by_c = s % c == 0
                if (by_a and not by_b and not by_c) or (by_b and not by_a and not by_c) or (by_c and not by_a and not by_b):
                    second = count[b] - 1 if b == a else count[b]
                    third = count[c] - (1 if c == a else 0) - (1 if c == b else 0)
                    total += count[a] * second * third
    return total


seed = 2198


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(20):
        top = 81 + a
        arrays.append([next_random() % top + 1 for _ in range(100000)])
    check = 0
    for _ in range(10):
        for nums in arrays:
            check = (check * 31 + single_divisor_triplet(nums) % 1000000007) % 1000000007
    print(f"10 passes over 20 arrays: checksum {check}")


main()
