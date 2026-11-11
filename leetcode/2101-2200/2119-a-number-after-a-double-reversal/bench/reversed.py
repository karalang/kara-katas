# LeetCode #2119: A Number After a Double Reversal -- the benchmark, the
# same algorithm as reversed.kara: each number's digits reversed by % 10
# and // 10, twice.


def reverse(num):
    n = num
    out = 0
    while n > 0:
        out = out * 10 + n % 10
        n //= 10
    return out


def is_same_after_reversals(num):
    return reverse(reverse(num)) == num


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2119]
    nums = []
    for _ in range(1000000):
        num = next_random(seed) % 1000001
        if next_random(seed) % 3 == 0:
            num = num // 1000 * 1000
        nums.append(num)
    same = 0
    check = 0
    for rnd in range(100):
        nums[rnd * 7919 % 1000000] += 1
        for num in nums:
            if is_same_after_reversals(num):
                same += 1
                check = (check * 31 + num % 1000) % 1000000007
    print(f"100000000 checks: {same} the same, checksum {check}")


main()
