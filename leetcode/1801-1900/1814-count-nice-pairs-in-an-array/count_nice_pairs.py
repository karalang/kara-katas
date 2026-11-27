# LeetCode #1814: Count Nice Pairs in an Array -- the ★ arm in Python: a
# pair is nice exactly when its two numbers less their reverses agree, so
# each number's difference is counted in a dict as the array is walked, and
# each number makes a nice pair with every earlier one of its difference.

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
    # LeetCode's two examples
    print(count_nice_pairs([42, 11, 1, 97]), count_nice_pairs([13, 10, 35, 24, 76]))
    # the edges: one number; two zeros; a number and its reverse with a
    # trailing zero; palindromes only; the largest numbers
    print(
        count_nice_pairs([5]),
        count_nice_pairs([0, 0]),
        count_nice_pairs([10, 1]),
        count_nice_pairs([121, 7, 44, 9009, 0]),
        count_nice_pairs([1000000000, 999999999, 1]),
        count_nice_pairs([21, 12, 32, 43, 54, 65]),
    )
    # the constraints' most: 10^5 equal numbers, and 10^5 numbers counting up
    print(
        "the most:",
        count_nice_pairs([123] * 100000),
        count_nice_pairs([k * 9973 for k in range(100000)]),
    )
    # 3000 random arrays of 1 to 40 numbers, small or up to 10^9
    seed = [1814]
    check = 0
    for _ in range(3000):
        n = 1 + next_random(seed) % 40
        big = next_random(seed) % 2 == 0
        nums = []
        for _ in range(n):
            if big:
                nums.append((next_random(seed) * 32768 + next_random(seed)) % 1000000001)
            else:
                nums.append(next_random(seed) % 200)
        check = (check * 31 + count_nice_pairs(nums)) % MOD
    print(f"3000 random arrays: checksum {check}")


main()
