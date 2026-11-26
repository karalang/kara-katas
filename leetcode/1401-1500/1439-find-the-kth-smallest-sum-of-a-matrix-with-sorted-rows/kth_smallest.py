# LeetCode #1439: Find the Kth Smallest Sum of a Matrix With Sorted Rows --
# the Python mirror of kth_smallest.kara: the k smallest sums of the rows
# so far, each next row added to every one of them, sorted and cut to k


def kth_smallest(mat, k):
    sums = [0]
    for row in mat:
        nxt = [s + x for s in sums for x in row]
        nxt.sort()
        sums = nxt[:k]
    return sums[k - 1]


# ---- test harness ---------------------------------------------------------

seed = 1439


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(m, n, top):
    mat = []
    for _ in range(m):
        row = sorted(1 + next_random() % top for _ in range(n))
        mat.append(row)
    return mat


def sums_up_to_200(m, n):
    count = 1
    for _ in range(m):
        count = min(count * n, 200)
    return count


def main():
    cases = [([[1, 3, 11], [2, 4, 6]], 5), ([[1, 3, 11], [2, 4, 6]], 9), ([[1, 10, 10], [1, 4, 5], [2, 3, 6]], 7),
             ([[1, 1, 10], [2, 2, 9]], 7), ([[5]], 1), ([[1, 2, 3, 4, 5]], 4), ([[1], [2], [3]], 1),
             ([[1, 5000], [1, 5000], [1, 5000]], 8)]
    print(" ".join(str(kth_smallest(m, k)) for m, k in cases))
    big = drawn(40, 40, 5000)
    alike = [[5000] * 40 for _ in range(40)]
    print(f"40 rows of 40: {kth_smallest(big, 1)} {kth_smallest(big, 200)} {kth_smallest(alike, 200)}")
    check = 0
    total = 0
    for _ in range(2000):
        m = 1 + next_random() % 6
        n = 1 + next_random() % 6
        top = [10, 100, 5000][next_random() % 3]
        mat = drawn(m, n, top)
        k = 1 + next_random() % sums_up_to_200(m, n)
        got = kth_smallest(mat, k)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {total} in all, checksum {check}")


main()
