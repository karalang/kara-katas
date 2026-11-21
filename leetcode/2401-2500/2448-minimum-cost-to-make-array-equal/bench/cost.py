# LeetCode #2448: Minimum Cost to Make Array Equal -- the bench, the ★
# arm: the pairs sorted, the weighted median the first value whose
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


seed = 2448


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    nums = []
    cost = []
    for _ in range(n):
        r = next_random()
        nums.append(1 + (r * 32768 + next_random()) % 1000000)
        r = next_random()
        cost.append(1 + (r * 32768 + next_random()) % 1000000)
    check = 0
    for p in range(200):
        for t in range(1000):
            cost[(1000 * p + t) % n] = 1 + next_random() * 30
        check = (check * 31 + min_cost(nums, cost) % 1000000007 + p) % 1000000007
    print(f"200 passes over 10^5 values: checksum {check}")


main()
