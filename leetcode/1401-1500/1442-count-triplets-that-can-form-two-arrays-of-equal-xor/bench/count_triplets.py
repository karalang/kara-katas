# The Python mirror of count_triplets.kara.


def count_triplets(arr):
    seen = {0: (1, 0)}
    x = 0
    count = 0
    for k, a in enumerate(arr):
        x ^= a
        times, places = seen.get(x, (0, 0))
        count += times * k - places
        seen[x] = (times + 1, places + k + 1)
    return count


def main():
    seed = 1442
    arrays = []
    for _ in range(2000):
        arr = []
        for _ in range(300):
            seed = (seed * 1103515245 + 12345) % 2147483648
            arr.append(1 + seed // 65536 % 1023)
        arrays.append(arr)
    check = 0
    for _ in range(50):
        for arr in arrays:
            check = (check * 131 + count_triplets(arr)) % 1000000007
    print(f"10^5 arrays of 300: checksum {check}")


main()
