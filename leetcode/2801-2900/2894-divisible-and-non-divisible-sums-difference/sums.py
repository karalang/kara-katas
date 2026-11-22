# LeetCode #2894: Divisible and Non-divisible Sums Difference -- the
# Python mirror of the ★ arm (sums.kara): the whole sum less twice the
# multiples of m, by formula.


def difference_of_sums(n, m):
    k = n // m
    return n * (n + 1) // 2 - m * k * (k + 1)


def main():
    print(f"{difference_of_sums(10, 3)} {difference_of_sums(5, 6)} {difference_of_sums(5, 1)} {difference_of_sums(1000, 1000)}")
    total = 0
    check = 0
    for n in range(1, 201):
        for m in range(1, 201):
            d = difference_of_sums(n, m)
            total += d
            check = ((check * 31 + d) % 1000000007 + 1000000007) % 1000000007
    print(f"40000 pairs: differences total {total}, checksum {check}")


main()
