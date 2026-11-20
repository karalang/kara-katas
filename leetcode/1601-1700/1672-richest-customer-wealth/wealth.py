# LeetCode #1672: Richest Customer Wealth -- the Python mirror of the ★ arm:
# each row summed, the largest kept.


def maximum_wealth(accounts):
    return max(sum(row) for row in accounts)


# ---- the harness: the same as the Kāra arms -------------------------------

seed = 1672


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, money):
    total = 0
    check = 0
    for _ in range(count):
        m = next_random() % most + 1
        n = next_random() % most + 1
        accounts = [[next_random() % money + 1 for _ in range(n)] for _ in range(m)]
        richest = maximum_wealth(accounts)
        total += richest
        check = (check * 31 + richest + m * n) % 1000000007
    print(f"{count} grids of up to {most} by {most}, up to {money} in each account: answers sum to {total}, checksum {check}")


print(maximum_wealth([[1, 2, 3], [3, 2, 1]]))
print(maximum_wealth([[1, 5], [7, 3], [3, 5]]))
print(maximum_wealth([[2, 8, 7], [7, 1, 3], [1, 9, 5]]))
print(maximum_wealth([[4, 4, 4, 4]]))
print(maximum_wealth([[3], [9], [2]]))
print(maximum_wealth([[1, 1], [1, 1], [100, 100]]))
batch(3000, 5, 10)
batch(1000, 50, 100)
