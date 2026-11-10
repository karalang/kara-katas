# LeetCode #2076: Process Restricted Friend Requests -- Python mirror of
# the ★ arm's benchmark (friends.kara): 400 problems of 1000 people, 1000
# restrictions and 1000 requests; a union-find of parents in a list,
# found with path halving, every restriction tried against a request
# between two groups.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def friend_requests(n, restrictions, requests):
    parent = list(range(n))
    answers = []
    for u, v in requests:
        a = find(parent, u)
        b = find(parent, v)
        allowed = True
        if a != b:
            for x0, y0 in restrictions:
                x = find(parent, x0)
                y = find(parent, y0)
                if (x == a and y == b) or (x == b and y == a):
                    allowed = False
                    break
            if allowed:
                parent[a] = b
        answers.append(allowed)
    return answers


seed = 2076


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_pairs(n, count):
    pairs = []
    for _ in range(count):
        a = next_random() % n
        b = (a + 1 + next_random() % (n - 1)) % n
        pairs.append([a, b])
    return pairs


total = 0
check = 0
for _ in range(400):
    restrictions = random_pairs(1000, 1000)
    requests = random_pairs(1000, 1000)
    for a in friend_requests(1000, restrictions, requests):
        bit = 1 if a else 0
        total += bit
        check = (check * 3 + bit + 1) % 1000000007
print(f"400 problems: {total} accepted, checksum {check}")
