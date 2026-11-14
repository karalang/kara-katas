# LeetCode #2127: Maximum Employees to Be Invited to a Meeting -- the
# mirror of invitations.kara: Kahn's order peels the people no one favors,
# carrying the longest chain into each person; what is left are cycles.
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(favorite):
    print(f"[{', '.join(map(str, favorite))}] -> {maximum_invitations(favorite)}")


def main():
    show([2, 2, 1, 2])
    show([1, 2, 0])
    show([3, 0, 1, 4, 1])
    show([1, 0])
    show([1, 0, 3, 2, 0, 2])
    show([1, 2, 0, 4, 3])
    seed = [2127]
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random(seed) % 11 + 2
        favorite = [(i + 1 + next_random(seed) % (n - 1)) % n for i in range(n)]
        invited = maximum_invitations(favorite)
        total += invited
        check = (check * 31 + invited) % 1000000007
    print(f"3000 tables: {total} invited, checksum {check}")
    n = 100000
    ring = [(i + 1) % n for i in range(n)]
    tail = [1 - i if i < 2 else i - 1 for i in range(n)]
    rand = []
    for i in range(n):
        hi = next_random(seed)
        rand.append((i + 1 + (hi * 32768 + next_random(seed)) % (n - 1)) % n)
    a = maximum_invitations(ring)
    b = maximum_invitations(tail)
    c = maximum_invitations(rand)
    print(f"100000 employees: {a} in a ring, {b} with a tail, {c} at random")


main()
