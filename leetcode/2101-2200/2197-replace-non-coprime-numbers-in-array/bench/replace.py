# benchmark's Python mirror of replace.kara (LeetCode #2197, the ★ arm): a
# stack merged at its top.


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def replace_non_coprimes(nums):
    stack = []
    for x in nums:
        cur = x
        while stack:
            top = stack[-1]
            g = gcd(top, cur)
            if g == 1:
                break
            cur = top // g * cur
            stack.pop()
        stack.append(cur)
    return stack


seed = 2197


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def divisors(m):
    return [d for d in range(1, 100001) if m % d == 0]


def main():
    pools = [divisors(10810800), divisors(1674432), [1, 99991, 99989, 99971, 99961, 99929, 99923]]
    arrays = []
    for a in range(12):
        pool = pools[a % 3]
        arrays.append([pool[wide_random() % len(pool)] for _ in range(100000)])
    check = 0
    for _ in range(100):
        for nums in arrays:
            out = replace_non_coprimes(nums)
            check = (check * 31 + len(out)) % 1000000007
            check = (check * 31 + out[len(out) // 2]) % 1000000007
    print(f"100 passes over 12 arrays: checksum {check}")


main()
