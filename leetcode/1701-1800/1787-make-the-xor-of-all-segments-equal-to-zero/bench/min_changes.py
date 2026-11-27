# LeetCode #1787: Make the XOR of All Segments Equal to Zero -- the bench in
# Python, mirroring min_changes.kara: a DP over the k groups of positions.


def min_changes(nums, k):
    best = [2**31 // 2 - 1] * 1024
    best[0] = 0
    for g in range(k):
        count = {}
        size = 0
        i = g
        while i < len(nums):
            count[nums[i]] = count.get(nums[i], 0) + 1
            size += 1
            i += k
        floor = min(best) + size
        nxt = [floor] * 1024
        for x in range(1024):
            for v, c in count.items():
                here = best[x ^ v] + size - c
                if here < nxt[x]:
                    nxt[x] = here
        best = nxt
    return best[0]


seed = 1787


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[next_random() % 1024 for _ in range(600)] for _ in range(100)]
    check = 0
    for call in range(300):
        nums = lists[(check + call) % 100]
        k = 1 + (check * 7 + call) % 600
        check = (check * 31 + min_changes(nums, k)) % 1000000007
    print(f"300 calls over 100 lists: checksum {check}")


main()
