# Python mirror of minimal.kara (LeetCode #2195, the ★ arm): the numbers
# sorted, the gaps between them walked from 0 up, each gap's missing
# numbers added as a run by an arithmetic series.


def run_sum(lo, hi):
    return (lo + hi) * (hi - lo + 1) // 2


def minimal_k_sum(nums, k):
    wanted, total, last = k, 0, 0
    for x in sorted(nums):
        if x > last + 1 and wanted > 0:
            take = min(x - last - 1, wanted)
            total += run_sum(last + 1, last + take)
            wanted -= take
        if x > last:
            last = x
    if wanted > 0:
        total += run_sum(last + 1, last + wanted)
    return total


seed = 2195


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def show(nums, k):
    print(f"[{', '.join(map(str, nums))}], {k} -> {minimal_k_sum(nums, k)}")


show([1, 4, 25, 10, 25], 2)
show([5, 6], 6)
show([1], 1)
show([3, 1, 2, 5, 4], 3)
show([2, 2, 2, 7, 7], 4)
show([1000000000], 100000000)
check = 0
for rnd in range(3000):
    n = next_random() % 30 + 1
    top = [10, 100, 1000000000][rnd % 3]
    reach = [50, 1000, 100000000][(rnd // 3) % 3]
    nums = [big_random() % top + 1 for _ in range(n)]
    k = big_random() % reach + 1
    check = (check * 31 + minimal_k_sum(nums, k) % 1000000007) % 1000000007
print(f"3000 cases: checksum {check}")
wide = [big_random() % 1000000000 + 1 for _ in range(100000)]
full = list(range(1, 100001))
for i in range(99999, 0, -1):
    j = big_random() % (i + 1)
    full[i], full[j] = full[j], full[i]
print(f"10^5 numbers: {minimal_k_sum(wide, 100000000)} {minimal_k_sum(full, 1)}")
