# LeetCode #1814: Count Nice Pairs in an Array -- the bench in Python: the
# ★ arm over 200 calls on runs of 50000 to 99999 numbers cut from one array
# of 10^5, built once, each run's length drawn from the checksum so far.

MOD = 1000000007


def rev(x):
    r = 0
    while x > 0:
        r = r * 10 + x % 10
        x //= 10
    return r


def count_nice_pairs(nums):
    seen = {}
    pairs = 0
    for x in nums:
        d = x - rev(x)
        c = seen.get(d, 0)
        pairs = (pairs + c) % MOD
        seen[d] = c + 1
    return pairs


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1814]
    base = []
    for k in range(100000):
        if k % 2 == 0:
            base.append(next_random(seed) % 10000)
        else:
            base.append((next_random(seed) * 32768 + next_random(seed)) % 1000000001)
    check = 0
    for call in range(200):
        n = 50000 + (check + call) % 50000
        check = (check * 31 + count_nice_pairs(base[:n])) % MOD
    print(f"200 calls: checksum {check}")


main()
