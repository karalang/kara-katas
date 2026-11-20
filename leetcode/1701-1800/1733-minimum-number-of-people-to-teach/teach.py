# LeetCode #1733: Minimum Number of People to Teach -- the Python mirror
# of the ★ arm, teach.kara: the users of every friendship with no common
# language gathered in a set, and the language most of them already know
# taught to the rest.


def minimum_teachings(n, languages, friendships):
    known = [set(l) for l in languages]
    stuck = set()
    for u, v in friendships:
        u, v = u - 1, v - 1
        if known[u].isdisjoint(known[v]):
            stuck.add(u)
            stuck.add(v)
    speakers = [0] * (n + 1)
    for u in stuck:
        for l in known[u]:
            speakers[l] += 1
    return len(stuck) - max(speakers)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def draw(n, users, pairs, seed):
    languages = []
    for _ in range(users):
        k = next_random(seed) % min(n, 3) + 1
        known = []
        while len(known) < k:
            l = next_random(seed) % n + 1
            if l not in known:
                known.append(l)
        languages.append(known)
    friends = [[False] * users for _ in range(users)]
    friendships = []
    while len(friendships) < pairs:
        u = next_random(seed) % users
        v = next_random(seed) % users
        if u != v and not friends[u][v]:
            friends[u][v] = True
            friends[v][u] = True
            friendships.append([u + 1, v + 1])
    return languages, friendships


def batch(count, most, crowd, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        users = next_random(seed) % (crowd - 1) + 2
        pairs = next_random(seed) % min(users * (users - 1) // 2, 500) + 1
        languages, friendships = draw(n, users, pairs, seed)
        answer = minimum_teachings(n, languages, friendships)
        total += answer
        check = (check * 31 + answer + users) % 1000000007
    print(f"{count} problems of up to {most} languages and {crowd} users: teachings sum to {total}, checksum {check}")


def main():
    print(minimum_teachings(2, [[1], [2], [1, 2]], [[1, 2], [1, 3], [2, 3]]))
    print(minimum_teachings(3, [[2], [1, 3], [1, 2], [3]], [[1, 4], [1, 2], [3, 4], [2, 3]]))
    print(minimum_teachings(2, [[1], [1, 2], [1]], [[1, 2], [2, 3]]))
    print(minimum_teachings(4, [[1], [2], [3], [4]], [[1, 2], [2, 3], [3, 4], [4, 1]]))
    seed = [1733]
    batch(3000, 5, 6, seed)
    batch(300, 50, 100, seed)
    batch(5, 500, 500, seed)


main()
