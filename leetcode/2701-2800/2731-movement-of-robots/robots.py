# LeetCode #2731: Movement of Robots -- Python mirror of robots.kara (the
# ★ arm): the places after d seconds as if robots pass through each
# other, sorted, each adding k times itself less the sum before it.

MOD = 1000000007


def sum_distance(nums, s, d):
    places = sorted(x - d if w == "L" else x + d for x, w in zip(nums, s))
    total = 0
    before = 0
    for k, p in enumerate(places):
        total = (total + k * p - before) % MOD
        before += p
    return total


seed = 2731


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_robots(n, spread):
    nums = []
    at = -(n * spread // 2)
    for _ in range(n):
        nums.append(at)
        at += next_random() % spread + 1
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    s = "".join("L" if next_random() % 2 == 0 else "R" for _ in range(n))
    return nums, s


def main():
    print(sum_distance([-2, 0, 2], "RLL", 3))
    print(sum_distance([1, 0], "RL", 2))
    print(sum_distance([5], "L", 1000000000))
    print(sum_distance([-2000000000, 2000000000], "LR", 1000000000))
    total_sum = 0
    check = 0
    for c in range(2020):
        if c < 2000:
            n, spread, longest = next_random() % 30 + 1, 10, 51
        else:
            n, spread, longest = 1000, 1000000, 1000000001
        nums, s = random_robots(n, spread)
        d = (next_random() * 32768 + next_random()) % longest
        total = sum_distance(nums, s, d)
        total_sum += total
        check = (check * 31 + total) % 1000000007
        if c == 1999:
            print(f"2000 small cases: sums sum to {total_sum}, checksum {check}")
            total_sum = 0
            check = 0
    print(f"20 cases of 1000 robots: sums sum to {total_sum}, checksum {check}")
    nums, s = random_robots(100000, 40000)
    print(sum_distance(nums, s, 1000000000))


main()
