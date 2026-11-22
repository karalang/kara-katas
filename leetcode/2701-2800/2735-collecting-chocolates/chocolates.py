# LeetCode #2735: Collecting Chocolates -- Python mirror of
# chocolates.kara (the ★ arm): each type's cheapest price within k turns,
# narrowed one turn at a time, and the least of k x plus their sum.


def min_cost(nums, x):
    n = len(nums)
    cheapest = list(nums)
    best = sum(nums)
    for k in range(1, n):
        for t in range(n):
            cheapest[t] = min(cheapest[t], nums[(t - k + n) % n])
        best = min(best, k * x + sum(cheapest))
    return best


seed = 2735


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_up_to(most):
    return (next_random() * 32768 + next_random()) % most + 1


def main():
    print(min_cost([20, 1, 15], 5))
    print(min_cost([1, 2, 3], 4))
    print(min_cost([7], 3))
    print(min_cost([5, 9, 2, 8], 1000))
    print(min_cost([5, 9, 2, 8], 1))
    total = 0
    check = 0
    for c in range(2020):
        if c < 2000:
            n, most = next_random() % 20 + 1, 100
        else:
            n, most = 1000, 1000000000
        nums = [random_up_to(most) for _ in range(n)]
        x = random_up_to(most)
        cost = min_cost(nums, x)
        total += cost
        check = (check * 31 + cost) % 1000000007
        if c == 1999:
            print(f"2000 small cases: costs sum to {total}, checksum {check}")
            total = 0
            check = 0
    print(f"20 cases of 1000 chocolates: costs sum to {total}, checksum {check}")


main()
