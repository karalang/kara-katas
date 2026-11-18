# LeetCode #2305: Fair Distribution of Cookies -- the bench, the ★ arm in
# Python. Backtrack each bag over the children whose load stays under
# the best so far, trying only the first child with nothing yet.

seed = 2305


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distribute_cookies(cookies, k):
    loads = [0] * k
    best = [float("inf")]
    n = len(cookies)

    def place(i):
        if i == n:
            best[0] = min(best[0], max(loads))
            return
        bag = cookies[i]
        for c in range(k):
            if loads[c] + bag < best[0]:
                loads[c] += bag
                place(i + 1)
                loads[c] -= bag
            if loads[c] == 0:
                break

    place(0)
    return best[0]


def main():
    lists = []
    for _ in range(2000):
        cookies = []
        for _ in range(8):
            hi = next_random()
            cookies.append((hi * 32768 + next_random()) % 100000 + 1)
        lists.append(cookies)
    check = 0
    for p in range(50):
        for a in range(2000):
            check = (check * 31 + distribute_cookies(lists[a], 2 + (a + p) % 7)) % 1000000007
    print(f"50 passes over 2000 lists of 8 bags: checksum {check}")


main()
