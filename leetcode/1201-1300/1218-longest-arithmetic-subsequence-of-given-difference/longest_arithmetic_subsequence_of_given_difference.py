# LeetCode #1218: Longest Arithmetic Subsequence of Given Difference -- a
# Python mirror of the ★ arm: a dict from each value to the longest such
# subsequence seen so far that ends with it, a value extending the one
# ending at itself minus the difference.


def longest_subsequence(arr, difference):
    ending = {}
    best = 0
    for x in arr:
        length = ending.get(x - difference, 0) + 1
        ending[x] = length
        best = max(best, length)
    return best


seed = 1218


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        ([1, 2, 3, 4], 1),
        ([1, 3, 5, 7], 1),
        ([1, 5, 7, 8, 5, 3, 4, 2, 1], -2),
        ([5], 0),
        ([3, 3, 3], 0),
        ([-10000, 0, 10000], 10000),
        ([10000, 0, -10000], -10000),
        ([4, 1, 3, 2], -1),
    ]
    for arr, d in cases:
        print(f"{show(arr)} {d}: {longest_subsequence(arr, d)}")
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 12 + 1
        spread = next_random() % 8 + 1
        arr = [next_random() % (2 * spread + 1) - spread for _ in range(n)]
        d = next_random() % 5 - 2
        answer = longest_subsequence(arr, d)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000 small cases: lengths total {total}, checksum {check}")
    arr = [next_random() % 20001 - 10000 for _ in range(100000)]
    print(f"10^5 random values, difference 3: {longest_subsequence(arr, 3)}, difference -7: {longest_subsequence(arr, -7)}, difference 0: {longest_subsequence(arr, 0)}")
    rising = [i % 20001 - 10000 for i in range(100000)]
    print(f"-10^4 to 10^4 over and over, difference 1: {longest_subsequence(rising, 1)}, difference -1: {longest_subsequence(rising, -1)}")
    ends = [-10000 if i % 2 == 0 else 10000 for i in range(100000)]
    print(f"-10^4 and 10^4 in turn, difference 10^4: {longest_subsequence(ends, 10000)}, difference 0: {longest_subsequence(ends, 0)}")


main()
