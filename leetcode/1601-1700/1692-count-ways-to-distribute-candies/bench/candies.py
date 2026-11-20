# LeetCode #1692: Count Ways to Distribute Candies -- the bench's Python
# mirror: the ★ arm on 200 problems of 1000 candies, each with a random
# number of bags up to 1000, all drawn first, each answered 8 times.


def ways_to_distribute(n, k):
    modulus = 1000000007
    ways = [0] * (k + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            ways[j] = (j * ways[j] + ways[j - 1]) % modulus
        ways[0] = 0
    return ways[k]


seed = 1692


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 200, 8, 1000
    bags = [next_random() % n + 1 for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for k in bags:
            answer = ways_to_distribute(n, k)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} candies, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
