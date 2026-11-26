# LeetCode #1442: Count Triplets That Can Form Two Arrays of Equal XOR --
# the Python mirror of count_triplets.kara: for each prefix xor met, how
# many times and the sum of the places it was met at


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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, top):
    out = []
    for _ in range(n):
        hi = next_random()
        out.append(1 + (hi * 32768 + next_random()) % top)
    return out


def main():
    global seed
    cases = [[2, 3, 1, 6, 7], [1, 1, 1, 1, 1], [2, 3], [1, 3, 5, 7, 9], [7, 11, 12, 9, 5, 2, 7, 17, 22], [1], [5, 5], [1, 2, 3]]
    print(" ".join(str(count_triplets(arr)) for arr in cases))
    seed = 1442
    ones = [1] * 300
    large = drawn(300, 100000000)
    small = drawn(300, 4)
    print(f"300 numbers: {count_triplets(ones)} {count_triplets(large)} {count_triplets(small)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        top = [1, 3, 15, 100000000][next_random() % 4]
        got = count_triplets(drawn(n, top))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {total} triplets, checksum {check}")


main()
