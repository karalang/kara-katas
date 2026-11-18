# LeetCode #2320: Count Number of Ways to Place Houses -- the ★ arm in
# Python. The two sides never touch, so the answer is one side's count
# squared; on one side, the placements ending in an empty plot and in a
# house are rolled forward a plot at a time. O(n).


def count_house_placements(n):
    modulus = 1000000007
    empty, house = 1, 1
    for _ in range(1, n):
        empty, house = (empty + house) % modulus, empty
    side = (empty + house) % modulus
    return side * side % modulus


def main():
    for n in [1, 2, 3, 10, 100, 10000]:
        print(f"{n}: {count_house_placements(n)}")
    check = 0
    total = 0
    for n in range(1, 301):
        ways = count_house_placements(n)
        check = (check * 31 + ways) % 1000000007
        total += ways
    print(f"300 counts: checksum {check}, {total} in all")


main()
