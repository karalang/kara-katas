# LeetCode #2127: Maximum Employees to Be Invited to a Meeting -- the
# benchmark, the same algorithm as invitations.kara.
from collections import deque


def maximum_invitations(favorite):
    n = len(favorite)
    indegree = [0] * n
    for f in favorite:
        indegree[f] += 1
    chain = [0] * n
    queue = deque(i for i in range(n) if indegree[i] == 0)
    while queue:
        i = queue.popleft()
        f = favorite[i]
        chain[f] = max(chain[f], chain[i] + 1)
        indegree[f] -= 1
        if indegree[f] == 0:
            queue.append(f)
    largest_cycle = 0
    pairs = 0
    for i in range(n):
        if indegree[i] == 0:
            continue
        length = 0
        j = i
        while indegree[j] != 0:
            indegree[j] = 0
            length += 1
            j = favorite[j]
        if length == 2:
            pairs += 2 + chain[i] + chain[favorite[i]]
        else:
            largest_cycle = max(largest_cycle, length)
    return max(largest_cycle, pairs)


def main():
    seed = 2127

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def big():
        hi = next_random()
        return hi * 32768 + next_random()

    n = 100000
    tables = []
    for _ in range(20):
        favorite = []
        for i in range(n):
            if i < n // 4:
                favorite.append(i ^ 1)
            else:
                favorite.append((i + 1 + big() % (n - 1)) % n)
        tables.append(favorite)
    total = 0
    check = 0
    for rnd in range(10):
        for t in range(20):
            i = n // 4 + big() % (n - n // 4)
            tables[t][i] = (i + 1 + big() % (n - 1)) % n
            invited = maximum_invitations(tables[t])
            total += invited
            check = (check * 31 + invited + rnd) % 1000000007
    print(f"200 solves: {total} invited, checksum {check}")


main()
