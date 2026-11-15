# LeetCode #2197: Replace Non-Coprime Numbers in Array -- Python mirror of
# replace.kara (the ★ arm): a stack of the numbers settled so far; each
# number, before it is pushed, merges with the top while the two share a
# factor, the pair replaced by its LCM. O(n log m).


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


# ---- test harness ---------------------------------------------------------

seed = 2197


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> [{', '.join(map(str, replace_non_coprimes(nums)))}]")


def fold(v, check):
    for x in v:
        check = (check * 31 + x) % 1000000007
    return (check * 31 + len(v)) % 1000000007


def divisors(m):
    return [d for d in range(1, 100001) if m % d == 0]


def main():
    show([6, 4, 3, 2, 7, 6, 2])
    show([2, 2, 1, 1, 3, 3, 3])
    show([5])
    show([2, 3, 5, 7, 11, 13])
    show([3, 5, 7, 11, 2, 2, 22])
    show([2, 6, 15, 35, 77, 143])
    pools = [divisors(10810800), divisors(1674432), [1, 99991, 99989, 99971, 99961, 99929, 99923]]
    check = 0
    kept = 0
    for rnd in range(3000):
        n = next_random() % 40 + 1
        pool = pools[rnd % 3]
        nums = [pool[wide_random() % len(pool)] for _ in range(n)]
        out = replace_non_coprimes(nums)
        kept += len(out)
        check = fold(out, check)
    print(f"3000 arrays: {kept} kept, checksum {check}")
    first = []
    third = []
    for _ in range(100000):
        first.append(pools[0][wide_random() % len(pools[0])])
        third.append(pools[2][wide_random() % len(pools[2])])
    a = replace_non_coprimes(first)
    b = replace_non_coprimes(third)
    print(f"10^5 numbers: {len(a)} kept, checksum {fold(a, 0)}; near primes: {len(b)} kept, checksum {fold(b, 0)}")


main()
