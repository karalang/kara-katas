# LeetCode #1815: Maximum Number of Groups Getting Fresh Donuts -- the
# bench in Python: the ★ arm over 3000 cases of 30 groups at a batch of 7
# to 9, each group's remainder drawn from the batch's lower half, so that
# no two groups pair off and the search meets the most states.


def max_happy_groups(batch_size, groups):
    b = batch_size
    count = [0] * b
    for g in groups:
        count[g % b] += 1
    happy = count[0]
    count[0] = 0
    for r in range(1, b):
        s = b - r
        if r < s:
            k = min(count[r], count[s])
            happy += k
            count[r] -= k
            count[s] -= k
        elif r == s:
            happy += count[r] // 2
            count[r] %= 2
    memo = {}

    def best(left):
        key = tuple(count)
        if key in memo:
            return memo[key]
        top = 0
        for r in range(1, b):
            if count[r] > 0:
                count[r] -= 1
                top = max(top, best((left + r) % b))
                count[r] += 1
        top += 1 if left == 0 and any(count) else 0
        memo[key] = top
        return top

    return happy + best(0)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1815]
    check = 0
    for _ in range(3000):
        b = 7 + next_random(seed) % 3
        groups = [next_random(seed) * b + 1 + next_random(seed) % ((b - 1) // 2) for _ in range(30)]
        check = (check * 31 + max_happy_groups(b, groups)) % 1000000007
    print(f"3000 cases: checksum {check}")


main()
