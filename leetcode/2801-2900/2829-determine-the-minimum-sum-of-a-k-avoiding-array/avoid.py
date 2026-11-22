# LeetCode #2829: Determine the Minimum Sum of a k-avoiding Array -- the
# Python mirror of the ★ arm: the numbers walked up from 1, each taken
# unless its partner k - v was taken before it.


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


# ---- the harness: the same in every arm --------------------------------


def main():
    print(minimum_sum(5, 4))
    print(minimum_sum(2, 6))
    print(minimum_sum(1, 50))
    print(minimum_sum(50, 1))
    print(minimum_sum(50, 50))
    total = 0
    check = 0
    for n in range(1, 51):
        for k in range(1, 51):
            a = minimum_sum(n, k)
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"2500 pairs: sums total {total}, checksum {check}")


main()
