# LeetCode #1259 bench, in Python: the ★ arm (ways[k] for k pairs, summed over
# where person 0's partner sits, modulo 10^9 + 7) for every even count of
# people from 2 to 1000, 4 rounds; each count folded into a checksum.


def number_of_ways(num_people):
    m = 1000000007
    pairs = num_people // 2
    ways = [0] * (pairs + 1)
    ways[0] = 1
    for k in range(1, pairs + 1):
        for left in range(k):
            ways[k] = (ways[k] + ways[left] * ways[k - 1 - left]) % m
    return ways[pairs]


def main():
    check = 0
    for _ in range(4):
        for n in range(2, 1001, 2):
            check = (check * 131 + number_of_ways(n)) % 1000000007
    print(f"4 rounds of 2 to 1000 people: checksum {check}")


main()
