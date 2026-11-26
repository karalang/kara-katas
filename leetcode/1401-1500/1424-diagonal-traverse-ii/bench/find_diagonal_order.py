def find_diagonal_order(nums):
    diagonals = []
    for i in range(len(nums) - 1, -1, -1):
        row = nums[i]
        for j in range(len(row)):
            while len(diagonals) <= i + j:
                diagonals.append([])
            diagonals[i + j].append(row[j])
    order = []
    for d in diagonals:
        order.extend(d)
    return order


def main():
    seed = 1424
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + seed // 65536 % 9
        row = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            row.append(1 + seed // 65536 % 100000)
        pool.append(row)
    check = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % 80001
        for x in find_diagonal_order(pool[start:start + 20000]):
            check = (check * 131 + x) % 1000000007
    print(f"300 windows of 2 * 10^4 rows: checksum {check}")


main()
