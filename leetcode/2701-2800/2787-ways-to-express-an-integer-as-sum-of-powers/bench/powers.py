# LeetCode #2787: Ways to Express an Integer as Sum of Powers -- the bench
# in Python: the ★ arm over every n from 1 to 300 with every x from 1 to
# 5, 20 times over.


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
    rounds = 20
    total = 0
    check = 0
    for r in range(rounds):
        for n in range(1, 301):
            for x in range(1, 6):
                w = number_of_ways(n, x)
                total += w
                check = (check * 31 + w + r) % 1000000007
    print(f"1500 pairs, {rounds} rounds: ways sum to {total}, checksum {check}")


main()
