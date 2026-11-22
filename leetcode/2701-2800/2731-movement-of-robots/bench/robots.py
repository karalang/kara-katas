# LeetCode #2731: Movement of Robots -- the bench (robots.kara in
# Python): the places after d seconds, robots passing through each other
# in effect, sorted, each adding its distance to all those before it.

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


def main():
    cases, n, rounds = 10, 100000, 10
    problems = []
    for _ in range(cases):
        nums = []
        at = -2000000000
        for _ in range(n):
            nums.append(at)
            at += (next_random() * 32768 + next_random()) % 40000 + 1
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        s = "".join("L" if next_random() % 2 == 0 else "R" for _ in range(n))
        d = (next_random() * 32768 + next_random()) % 1000000001
        problems.append((nums, s, d))
    total_sum = 0
    check = 0
    for r in range(rounds):
        for nums, s, d in problems:
            total = sum_distance(nums, s, d)
            total_sum += total
            check = (check * 31 + total + r) % 1000000007
    print(f"{cases} cases of {n} robots, {rounds} rounds: sums mod p sum to {total_sum}, checksum {check}")


main()
