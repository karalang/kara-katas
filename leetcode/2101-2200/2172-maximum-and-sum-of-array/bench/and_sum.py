# LeetCode #2172: Maximum AND Sum of Array -- the benchmark's Python
# mirror of and_sum.kara.


def maximum_and_sum(nums, num_slots):
    powers = [3 ** k for k in range(num_slots)]
    p = 3 ** num_slots
    best = [-1] * p
    best[0] = 0
    answer = 0
    for fill in range(p):
        if best[fill] < 0:
            continue
        placed = 0
        rest = fill
        while rest > 0:
            placed += rest % 3
            rest //= 3
        if placed == len(nums):
            answer = max(answer, best[fill])
            continue
        for slot in range(num_slots):
            if fill // powers[slot] % 3 < 2:
                nxt = fill + powers[slot]
                s = best[fill] + (nums[placed] & (slot + 1))
                if s > best[nxt]:
                    best[nxt] = s
    return answer


seed = 2172


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = [next_random() % 15 + 1 for _ in range(100000)]
    check = 0
    for _ in range(200):
        start = next_random() % 99983
        best = maximum_and_sum(row[start:start + 18], 9)
        check = (check * 31 + best) % 1000000007
    print(f"200 solves: checksum {check}")


main()
