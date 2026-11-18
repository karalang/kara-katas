# LeetCode #2305: Fair Distribution of Cookies -- the ★ arm in Python.
# Backtrack: each bag in turn goes to each child whose load would stay
# under the best unfairness found so far, and only the first child with
# no bags yet is tried, since children with nothing are interchangeable.
# A full distribution's largest load lowers the best.


def distribute_cookies(cookies, k):
    loads = [0] * k
    best = [float("inf")]

    def place(i):
        if i == len(cookies):
            best[0] = min(best[0], max(loads))
            return
        for c in range(k):
            if loads[c] + cookies[i] < best[0]:
                loads[c] += cookies[i]
                place(i + 1)
                loads[c] -= cookies[i]
            if loads[c] == 0:
                break

    place(0)
    return best[0]


seed = 2305


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(distribute_cookies([8, 15, 10, 20, 8], 2))
    print(distribute_cookies([6, 1, 3, 2, 2, 4, 1, 2], 3))
    print(distribute_cookies([5, 9, 1, 7], 4))
    print(distribute_cookies([100000] * 8, 2))
    print(distribute_cookies([9, 7, 5, 4, 3, 2, 1, 1], 3))
    check = 0
    total = 0
    for _ in range(500):
        n = next_random() % 5 + 2
        k = next_random() % (n - 1) + 2
        cookies = []
        for _ in range(n):
            hi = next_random()
            cookies.append((hi * 32768 + next_random()) % 100000 + 1)
        unfairness = distribute_cookies(cookies, k)
        check = (check * 31 + unfairness) % 1000000007
        total += unfairness
    print(f"500 cases: checksum {check}, {total} in all")


main()
