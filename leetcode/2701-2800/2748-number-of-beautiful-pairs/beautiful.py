# LeetCode #2748: Number of Beautiful Pairs -- the ★ arm in Python
# (beautiful.kara): the first digits seen so far counted, each number
# adding the counts of the digits coprime to its last digit.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def count_beautiful_pairs(nums):
    firsts = [0] * 10
    pairs = 0
    for x in nums:
        last = x % 10
        for d in range(1, 10):
            if gcd(d, last) == 1:
                pairs += firsts[d]
        first = x
        while first >= 10:
            first //= 10
        firsts[first] += 1
    return pairs


seed = 2748


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(count_beautiful_pairs([2, 5, 1, 4]))
    print(count_beautiful_pairs([11, 21, 12]))
    print(count_beautiful_pairs([1] * 100))
    print(count_beautiful_pairs([22] * 100))
    print(count_beautiful_pairs([9999, 1, 9999, 1]))
    total = check = 0
    for _ in range(5000):
        n = next_random() % 99 + 2
        nums = []
        for _ in range(n):
            x = next_random() % 9999 + 1
            nums.append(x + 1 if x % 10 == 0 else x)
        pairs = count_beautiful_pairs(nums)
        total += pairs
        check = (check * 31 + pairs) % 1000000007
    print(f"5000 lists: pairs sum to {total}, checksum {check}")


main()
