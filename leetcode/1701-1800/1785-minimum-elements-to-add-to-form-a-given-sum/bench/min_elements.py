# LeetCode #1785: Minimum Elements to Add to Form a Given Sum -- the bench in
# Python, mirroring min_elements.kara: the gap over the limit, rounded up.


def min_elements(nums, limit, goal):
    gap = abs(goal - sum(nums))
    return (gap + limit - 1) // limit


seed = 1785


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(4000):
        nums = []
        for _ in range(100):
            a = next_random()
            b = next_random()
            nums.append((a * 32768 + b) % 2000001 - 1000000)
        lists.append(nums)
    check = 0
    for call in range(6000000):
        nums = lists[(check + call) % 4000]
        limit = 1 + (check + call) % 1000000
        goal = check % 2000000001 - 1000000000
        check = (check * 31 + min_elements(nums, limit, goal)) % 1000000007
    print(f"6000000 calls over 4000 lists: checksum {check}")


main()
