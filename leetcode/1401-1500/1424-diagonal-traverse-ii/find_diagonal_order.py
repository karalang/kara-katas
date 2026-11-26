# LeetCode #1424, Python mirror of find_diagonal_order.kara: a bucket for
# each diagonal i + j, the rows walked from the last up so that each
# bucket fills from the bottom left, then the buckets in turn.


def find_diagonal_order(nums):
    diagonals = []
    for i in range(len(nums) - 1, -1, -1):
        for j in range(len(nums[i])):
            while len(diagonals) <= i + j:
                diagonals.append([])
            diagonals[i + j].append(nums[i][j])
    order = []
    for d in diagonals:
        order.extend(d)
    return order


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(rows, wide, top):
    nums = []
    for _ in range(rows):
        n = 1 + next_random() % wide
        nums.append([1 + next_random() % top for _ in range(n)])
    return nums


def shown(order):
    return ",".join(str(x) for x in order)


def folded(order):
    check = 0
    for x in order:
        check = (check * 131 + x) % 1000000007
    return check


def main():
    global seed
    print(shown(find_diagonal_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]])))
    print(shown(find_diagonal_order([[1, 2, 3, 4, 5], [6, 7], [8], [9, 10, 11], [12, 13, 14, 15, 16]])))
    print(shown(find_diagonal_order([[1, 2, 3]])))
    print(shown(find_diagonal_order([[1], [2], [3]])))
    print(shown(find_diagonal_order([[1], [2, 3, 4], [5], [6, 7]])))
    seed = 1424
    row = [list(range(1, 100001))]
    column = [[x] for x in range(1, 100001)]
    jagged = drawn(330, 600, 100000)
    count = sum(len(r) for r in jagged)
    while count > 100000:
        count -= len(jagged.pop())
    print(f"10^5 values: {folded(find_diagonal_order(row))} {folded(find_diagonal_order(column))} {count} {folded(find_diagonal_order(jagged))}")
    check = 0
    total = 0
    for _ in range(2000):
        rows = 1 + next_random() % 12
        wide = [1, 4, 12][next_random() % 3]
        order = find_diagonal_order(drawn(rows, wide, 100))
        total += len(order)
        check = (check * 131 + folded(order)) % 1000000007
    print(f"2000 random cases: {total} values, checksum {check}")


main()
