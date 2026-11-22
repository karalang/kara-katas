# LeetCode #2894: Divisible and Non-divisible Sums Difference -- the
# bench, as sums.kara: every n and m from 1 to 1000, 100 rounds, by the
# formula arm.


def difference_of_sums(n, m):
    k = n // m
    return n * (n + 1) // 2 - m * k * (k + 1)


def main():
    rounds, top = 100, 1000
    total = 0
    check = 0
    for r in range(rounds):
        for n in range(1, top + 1):
            for m in range(1, top + 1):
                d = difference_of_sums(n, (m + r) % top + 1)
                total += d
                check = (check * 31 + d + 1000000) % 1000000007
    print(f"{top} by {top} pairs, {rounds} rounds: differences total {total}, checksum {check}")


main()
