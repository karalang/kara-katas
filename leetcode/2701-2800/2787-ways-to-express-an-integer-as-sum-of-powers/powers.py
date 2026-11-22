# LeetCode #2787: Ways to Express an Integer as Sum of Powers -- the ★ arm
# in Python (powers.kara): a 0/1 knapsack over the powers i^x, each
# added by walking the sums down from n.


def number_of_ways(n, x):
    modulus = 1000000007
    ways = [0] * (n + 1)
    ways[0] = 1
    i = 1
    while i ** x <= n:
        p = i ** x
        for s in range(n, p - 1, -1):
            ways[s] = (ways[s] + ways[s - p]) % modulus
        i += 1
    return ways[n]


def main():
    print(number_of_ways(10, 2))
    print(number_of_ways(4, 1))
    for x in range(1, 6):
        print(number_of_ways(300, x))
    nonzero = 0
    check = 0
    for n in range(1, 301):
        for x in range(1, 6):
            w = number_of_ways(n, x)
            if w > 0:
                nonzero += 1
            check = (check * 31 + w) % 1000000007
    print(f"1500 pairs: {nonzero} with a way, checksum {check}")


main()
