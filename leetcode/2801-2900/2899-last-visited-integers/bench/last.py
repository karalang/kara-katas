# LeetCode #2899: Last Visited Integers -- the bench's Python mirror (last.kara):
# the same draw, the same reading back from the end.


def last_visited_integers(nums):
    seen = []
    ans = []
    k = 0
    for v in nums:
        if v == -1:
            k += 1
            ans.append(seen[len(seen) - k] if k <= len(seen) else -1)
        else:
            seen.append(v)
            k = 0
    return ans


seed = 2899


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 10000, 20, 100
    cases = []
    for _ in range(count):
        nums = []
        for _ in range(n):
            if next_random() % 3 == 0:
                nums.append(-1)
            else:
                nums.append(next_random() % 100 + 1)
        cases.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            ans = last_visited_integers(nums)
            check = (check * 31 + len(ans) + r) % 1000000007
            for v in ans:
                total += v
                check = (check * 31 + v + 2) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: answers total {total}, checksum {check}")


main()
