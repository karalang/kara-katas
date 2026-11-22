# LeetCode #2829: Determine the Minimum Sum of a k-avoiding Array -- the
# bench's Python mirror of the ★ arm: the numbers walked up from 1, each
# taken unless its partner k - v was taken before it.


def minimum_sum(n, k):
    taken = [False] * (n + k + 1)
    count = 0
    total = 0
    v = 1
    while count < n:
        if v >= k or not taken[k - v]:
            taken[v] = True
            count += 1
            total += v
        v += 1
    return total


def main():
    rounds = 2000
    total = 0
    check = 0
    for r in range(rounds):
        for n in range(1, 51):
            for k in range(1, 51):
                a = minimum_sum(n, k)
                total += a
                check = (check * 31 + a + r) % 1000000007
    print(f"2500 pairs, {rounds} rounds: sums total {total}, checksum {check}")


main()
