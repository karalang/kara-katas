# LeetCode #1411 bench, Python: rows of two colours and of three, 6 of each
# in the first row, workload and checksum as num_of_ways.kara.

MODULUS = 1000000007


def num_of_ways(n):
    two, three = 6, 6
    for _ in range(1, n):
        two, three = (3 * two + 2 * three) % MODULUS, (2 * two + 2 * three) % MODULUS
    return (two + three) % MODULUS


def main():
    check = 0
    for k in range(40000):
        n = 1 + (check + k) % 5000
        check = (check * 131 + num_of_ways(n)) % 1000000007
    print(f"40000 grids of up to 5000 rows: checksum {check}")


main()
