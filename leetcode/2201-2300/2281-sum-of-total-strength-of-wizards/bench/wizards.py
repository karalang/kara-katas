# LeetCode #2281: Sum of Total Strength of Wizards -- the bench, the ★
# arm.

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


# ---- bench harness ---------------------------------------------------------

seed = 2281


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(30):
        strength = []
        for _ in range(100000):
            high = next_random()
            strength.append((high * 32768 + next_random()) % 1000000000 + 1)
        check = (check * 31 + total_strength(strength)) % 1000000007
    print(f"30 armies of 10^5: checksum {check}")


main()
