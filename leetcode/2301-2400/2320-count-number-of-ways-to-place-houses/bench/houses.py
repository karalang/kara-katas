# LeetCode #2320: Count Number of Ways to Place Houses -- the bench, the
# ★ arm in Python. One side's placements ending in an empty plot and in
# a house rolled forward a plot at a time, and their sum squared. O(n).


def count_house_placements(n):
    modulus = 1000000007
    empty = 1
    house = 1
    for _ in range(1, n):
        next_empty = (empty + house) % modulus
        house = empty
        empty = next_empty
    side = (empty + house) % modulus
    return side * side % modulus


def main():
    check = 0
    for p in range(10):
        for n in range(1, 10001):
            check = (check * 31 + count_house_placements(n) + p) % 1000000007
    print(f"10 passes over every count of plots up to 10^4: checksum {check}")


main()
