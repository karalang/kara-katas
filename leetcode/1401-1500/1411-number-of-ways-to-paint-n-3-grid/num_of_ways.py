# LeetCode #1411, Python mirror of num_of_ways.kara: rows of two colours
# (`aba`) and of three (`abc`), 6 of each in the first row; below an `aba`
# row go 3 `aba` and 2 `abc` rows, below an `abc` row 2 of each.

MODULUS = 1000000007


def num_of_ways(n):
    two, three = 6, 6
    for _ in range(1, n):
        two, three = (3 * two + 2 * three) % MODULUS, (2 * two + 2 * three) % MODULUS
    return (two + three) % MODULUS


def main():
    small = " ".join(str(num_of_ways(n)) for n in range(1, 11))
    print(f"{num_of_ways(1)} {num_of_ways(5000)} | {small}")
    print(f"n = 4998..5000: {num_of_ways(4998)} {num_of_ways(4999)} {num_of_ways(5000)}")
    check = 0
    for n in range(1, 601):
        check = (check * 131 + num_of_ways(n)) % 1000000007
    print(f"n = 1..600: checksum {check}")


main()
