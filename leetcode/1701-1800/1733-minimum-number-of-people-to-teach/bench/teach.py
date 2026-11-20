# LeetCode #1733: Minimum Number of People to Teach -- the bench
# (teach.kara): the stuck users gathered in a set, and the language most
# of them know.


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


def main():
    count = 50
    rounds = 200
    n, users, pairs = 500, 500, 500
    seed = [1733]
    problems = []
    for _ in range(count):
        languages = []
        for _ in range(users):
            k = next_random(seed) % 10 + 1
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
        problems.append((languages, friendships))
    total = 0
    check = 0
    for r in range(rounds):
        for languages, friendships in problems:
            answer = minimum_teachings(n, languages, friendships)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {users} users, {n} languages and {pairs} friendships, {rounds} rounds: teachings sum to {total}, checksum {check}")


main()
