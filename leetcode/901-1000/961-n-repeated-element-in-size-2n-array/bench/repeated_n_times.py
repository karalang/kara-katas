# Benchmark: LeetCode #961 N-Repeated Element in Size 2N Array -- the ★
# arm, near neighbours, on 10000 numbers with the repeated value at every
# other place. Mirrors repeated_n_times.kara.


def repeated_n_times(nums):
    for k in range(1, 4):
        for i in range(len(nums) - k):
            if nums[i] == nums[i + k]:
                return nums[i]
    return -1


seed = 961


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def alternating(n, first):
    used = [False] * 10001
    r = next_random() % 10001
    used[r] = True
    out = []
    while len(out) < 2 * n:
        v = next_random() % 10001
        if not used[v]:
            used[v] = True
            out += [r, v] if first else [v, r]
    return out


def main():
    rounds = 1000
    cases = [alternating(5000, i % 2 == 0) for i in range(50)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(50):
            c = (r + i) % 50
            p = 2 * (next_random() % 4999) + 1 - c % 2
            cs = cases[c]
            cs[p], cs[p + 2] = cs[p + 2], cs[p]
            a = repeated_n_times(cs)
            total += a
            check = (check * 31 + a + i) % 1000000007
    print(f"{rounds} rounds over 50 cases of 10000 numbers: the repeated ones sum to {total}, checksum {check}")


main()
