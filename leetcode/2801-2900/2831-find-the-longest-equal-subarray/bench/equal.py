# LeetCode #2831: Find the Longest Equal Subarray -- the bench, mirrored
# from equal.kara: positions per value, then two pointers over each list.


def longest_equal_subarray(nums, k):
    n = len(nums)
    places = [[] for _ in range(n + 1)]
    for i in range(n):
        places[nums[i]].append(i)
    best = 0
    for pos in places:
        l = 0
        for r in range(len(pos)):
            while pos[r] - pos[l] - (r - l) > k:
                l += 1
            best = max(best, r - l + 1)
    return best


seed = 2831


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 20, 20, 100000
    arrays = []
    for _ in range(count):
        nums = [next_random() % 1000 + 1 for _ in range(n)]
        arrays.append((nums, next_random() % 1001))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in arrays:
            a = longest_equal_subarray(nums, k)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}")


main()
