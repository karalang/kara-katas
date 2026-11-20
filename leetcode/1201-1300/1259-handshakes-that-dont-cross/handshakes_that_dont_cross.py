# LeetCode #1259: Handshakes That Don't Cross -- Python mirror of the ★ arm
# (ways[k] for k pairs, summed over where person 0's partner sits), with the
# same harness.


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
    print(f"{number_of_ways(4)} {number_of_ways(6)}")
    total = 0
    check = 0
    for n in range(2, 1001, 2):
        w = number_of_ways(n)
        total = (total + w) % 1000000007
        check = (check * 131 + w) % 1000000007
    print(f"2 to 1000 people: total {total}, checksum {check}")
    small = [number_of_ways(2 * k) for k in range(1, 11)]
    print(f"[{', '.join(map(str, small))}] ... {number_of_ways(1000)}")


main()
