# LeetCode #1356 -- bench, Python: one sort keyed by the pair (the number of
# 1 bits, the value).


def sort_by_bits(arr):
    return sorted(arr, key=lambda x: (bin(x).count("1"), x))


seed = [1356]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # 20 arrays of 500 values from 0 to 10^4, the constraints' most, built
    # once; then 2 * 10^4 rounds, each setting one place of one array to a
    # value, all drawn from the checksum so far, sorting it, and folding
    # three values of the answer into the checksum
    arrays = [[next_random() % 10001 for _ in range(500)] for _ in range(20)]
    check = 0
    for r in range(20000):
        k = check % 20
        arrays[k][(check // 20) % 500] = (check // 10000) % 10001
        got = sort_by_bits(arrays[k])
        check = (check * 31 + got[0] + got[check % 500] * 7 + got[499] * 13 + r) % 1000000007
    print(f"20000 rounds over 20 arrays of 500 values: checksum {check}")


main()
