# LeetCode #2281: Sum of Total Strength of Wizards -- the Python mirror
# of the ★ arm, `wizards.kara`.

MOD = 1000000007


def total_strength(strength):
    n = len(strength)
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        while stack and strength[stack[-1]] >= strength[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and strength[stack[-1]] > strength[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = (prefix[i] + strength[i]) % MOD
    twice = [0] * (n + 2)
    for i in range(n + 1):
        twice[i + 1] = (twice[i] + prefix[i]) % MOD
    total = 0
    for i in range(n):
        l, r = left[i], right[i]
        ends = (i - l) * ((twice[r + 1] - twice[i + 1] + MOD) % MOD) % MOD
        starts = (r - i) * ((twice[i + 1] - twice[l + 1] + MOD) % MOD) % MOD
        groups = (ends - starts + MOD) % MOD
        total = (total + strength[i] % MOD * groups) % MOD
    return total


# ---- test harness ---------------------------------------------------------

seed = 2281


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [[1, 3, 1, 2], [5, 4, 6], [7], [1000000000], [2, 2, 2], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]]
    for strength in examples:
        print(f"{show(strength)} -> {total_strength(strength)}")
    check = 0
    for t in range(2000):
        n = next_random() % 40 + 1
        high = [3, 100, 1000000000][t % 3]
        strength = [wide_random() % high + 1 for _ in range(n)]
        check = (check * 31 + total_strength(strength)) % 1000000007
    print(f"2000 armies: checksum {check}")
    random = [wide_random() % 1000000000 + 1 for _ in range(100000)]
    alike = [1000000000] * 100000
    rising = list(range(1, 100001))
    answers = [total_strength(random), total_strength(alike), total_strength(rising)]
    print(f"10^5 wizards: {show(answers)}")


main()
