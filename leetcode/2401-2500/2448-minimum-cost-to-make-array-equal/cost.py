# LeetCode #2448: Minimum Cost to Make Array Equal -- Python mirror of the
# ★ arm (cost.kara): the weighted median, the first sorted value whose
# running cost reaches half the total, and every value moved there.


def min_cost(nums, cost):
    pairs = sorted(zip(nums, cost))
    total = sum(cost)
    running = 0
    target = 0
    for value, c in pairs:
        running += c
        if 2 * running >= total:
            target = value
            break
    answer = 0
    for i in range(len(nums)):
        answer += abs(nums[i] - target) * cost[i]
    return answer


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    r = next_random()
    return r * 32768 + next_random()


def main():
    global seed
    print(f"example 1: {min_cost([1, 3, 5, 2], [2, 3, 1, 14])}")
    print(f"example 2: {min_cost([2, 2, 2, 2, 2], [4, 2, 8, 1, 3])}")
    print(f"one value: {min_cost([1000000], [1000000])}")
    print(f"equal costs: {min_cost([1, 1000000], [7, 7])}")
    print(f"one heavy: {min_cost([5, 1, 2, 3, 4, 6, 7], [100, 1, 1, 1, 1, 1, 1])}")
    n = 2000
    seed = 2448
    wide = []
    wide_cost = []
    for _ in range(n):
        wide.append(1 + wide_random() % 1000000)
        wide_cost.append(1 + wide_random() % 1000000)
    print(f"wide: {min_cost(wide, wide_cost)}")
    narrow = []
    narrow_cost = []
    for _ in range(n):
        narrow.append(1 + next_random() % 10)
        narrow_cost.append(1 + wide_random() % 1000000)
    print(f"narrow: {min_cost(narrow, narrow_cost)}")
    spread = [1 + wide_random() % 1000000 for _ in range(n)]
    print(f"every cost 10^6: {min_cost(spread, [1000000] * n)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 8
        nums = []
        cost = []
        for _ in range(length):
            nums.append(1 + next_random() % 10)
            cost.append(1 + next_random() % 10)
        answer = min_cost(nums, cost)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
