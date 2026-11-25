# LeetCode #1356 -- Python mirror of the ★ arm: one sort keyed by the pair
# (the number of 1 bits, the value).


def sort_by_bits(arr):
    return sorted(arr, key=lambda x: (bin(x).count("1"), x))


seed = [1356]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    print(show(sort_by_bits([0, 1, 2, 3, 4, 5, 6, 7, 8])))
    print(show(sort_by_bits([1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1])))
    powers = [1 << k for k in reversed(range(14))]
    print(f"{show(sort_by_bits([10000]))} {show(sort_by_bits([7, 0, 7, 0]))} {show(sort_by_bits(powers))}")
    big = [next_random() % 10001 for _ in range(500)]
    got = sort_by_bits(big)
    print(f"500 values: first {got[0]}, middle {got[250]}, last {got[499]}")
    check = 0
    for c in range(2000):
        n = 1 + next_random() % 500 if c % 4 == 0 else 1 + next_random() % 20
        top = 16 if c % 3 == 0 else 1001 if c % 3 == 1 else 10001
        arr = [next_random() % top for _ in range(n)]
        for x in sort_by_bits(arr):
            check = (check * 131 + x + 1) % 1000000007
    print(f"2000 random arrays: checksum {check}")


main()
