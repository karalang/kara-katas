# benchmark's Python mirror of minimal.kara (LeetCode #2195, the ★ arm):
# the gaps walked, each a series.


def run_sum(frm, to):
    return (frm + to) * (to - frm + 1) // 2


def minimal_k_sum(nums, k):
    s = sorted(nums)
    wanted = k
    total = 0
    last = 0
    for x in s:
        if x > last + 1 and wanted > 0:
            take = x - last - 1 if x - last - 1 < wanted else wanted
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


def main():
    nums = []
    for _ in range(100000):
        a = next_random()
        b = next_random()
        nums.append((a * 32768 + b) % 1000000000 + 1)
    check = 0
    for i in range(300):
        k = 100000000 - i * 1000
        check = (check * 31 + minimal_k_sum(nums, k) % 1000000007) % 1000000007
    print(f"300 solves over {len(nums)} numbers: checksum {check}")


main()
