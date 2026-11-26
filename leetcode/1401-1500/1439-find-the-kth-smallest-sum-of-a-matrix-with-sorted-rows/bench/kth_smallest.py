def kth_smallest(mat, k):
    sums = [0]
    for row in mat:
        nxt = [s + x for s in sums for x in row]
        nxt.sort()
        sums = nxt[:k]
    return sums[k - 1]


def main():
    seed = 1439
    check = 0
    for _ in range(300):
        mat = []
        for _ in range(40):
            row = []
            for _ in range(40):
                seed = (seed * 1103515245 + 12345) % 2147483648
                row.append(1 + seed // 65536 % 5000)
            row.sort()
            mat.append(row)
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + seed // 65536 % 200
        check = (check * 131 + kth_smallest(mat, k)) % 1000000007
    print(f"300 matrices of 40 by 40: checksum {check}")


main()
